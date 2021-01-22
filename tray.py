from os import environ
import os
import ctypes
import random as r
import sys
import threading
from getpass import getuser
from tkinter import *
from tkinter.filedialog import askdirectory
from PySide2 import QtWidgets, QtGui


icon = 'images\icon.ico'
user = getuser()

##def check_keys():
##    while True:
##        try:
##            if key.is_pressed('a'):
##                randomize()
##        except:
##            print('Something bad happened')
##                

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

def set():
    ctypes.windll.user32.SystemParametersInfoW(20, 0, images + wallpapers[current_img] , 3)

def forward():
    global current_img
    current_img += 1
    current_img = min(current_img, len(wallpapers) - 1)
    set()

def backwards():
    global current_img
    current_img -= 1
    current_img = max(current_img, 0)
    set()
    
def randomize():
    global current_img
    current_img = r.randint(0, len(wallpapers) - 1)
    set()

def diropenbox(msg=None, title=None, default=None):
            global images
            global wallpapers
            boxRoot = Tk()
            boxRoot.withdraw()
            if not default: default = None
            f = askdirectory(parent=boxRoot, title='Choose an images folder', initialdir='C:/Users/'+user+'/Pictures', initialfile=None)
            boxRoot.destroy()
            if not f: return None
            images =  os.path.normpath(f) + '/'
            with open('selection.txt', 'w') as sel:
                sel.write(images)
            wallpapers = os.listdir(images)

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip('Wallchanger')
        menu = QtWidgets.QMenu(parent)

        randomize = menu.addAction("Randomize Wallpaper")
        randomize.triggered.connect(self.randomize_wallpaper)
        #randomize.setIcon(QtGui.QIcon(icon))

        next_wallpaper = menu.addAction("Next Wallpaper")
        next_wallpaper.triggered.connect(self.next_wallpaper)

        previous = menu.addAction('Previous Wallpaper')
        previous.triggered.connect(self.previous_wallpaper)

        category = menu.addAction('Change Category')
        category.triggered.connect(self.change_category)

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: sys.exit())

        menu.addSeparator()
        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
        if reason == self.DoubleClick:
            self.randomize_wallpaper()

    def randomize_wallpaper(self):
        randomize()

    def next_wallpaper(self):
        forward()

    def previous_wallpaper(self):
        backwards()

    def change_category(self):
        diropenbox()
    
    
#simple check for images directory
if os.path.isdir('images') == False:
    os.mkdir('images')

try:
    images = open('selection.txt').read()
    wallpapers = os.listdir(images)
    current_img = 0
except:
    diropenbox()

def main():
    suppress_qt_warnings()
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon(icon), w)
    tray_icon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

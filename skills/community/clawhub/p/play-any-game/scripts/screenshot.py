import os
import time
import ctypes
from datetime import datetime
from typing import Optional, Tuple
import win32gui
import win32ui
import win32con
from PIL import Image

SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'screenshots')

user32 = ctypes.windll.user32
dwmapi = ctypes.windll.dwmapi

class RECT(ctypes.Structure):
    _fields_ = [
        ('left', ctypes.c_long),
        ('top', ctypes.c_long),
        ('right', ctypes.c_long),
        ('bottom', ctypes.c_long)
    ]

def ensure_screenshots_dir(game_name: Optional[str] = None):
    """
    确保截图目录存在
    
    Args:
        game_name: 游戏名称，用于按游戏分类整理
    """
    if game_name:
        target_dir = os.path.join(SCREENSHOTS_DIR, sanitize_filename(game_name))
    else:
        target_dir = SCREENSHOTS_DIR
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    return target_dir

def get_timestamp() -> str:
    """获取时间戳字符串"""
    now = datetime.now()
    return now.strftime('%Y%m%d_%H%M%S_%f')[:-3]

def sanitize_filename(name: str) -> str:
    """清理文件名"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name.replace(' ', '_')

def get_window_rect_dwm(hwnd: int) -> Optional[Tuple[int, int, int, int]]:
    """
    使用 DwmGetWindowAttribute 获取窗口位置
    """
    try:
        rect = RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        dwmapi.DwmGetWindowAttribute(
            hwnd,
            DWMWA_EXTENDED_FRAME_BOUNDS,
            ctypes.byref(rect),
            ctypes.sizeof(rect)
        )
        return (rect.left, rect.top, rect.right, rect.bottom)
    except Exception:
        return None

def get_capture_rect(hwnd: int) -> Optional[Tuple[int, int, int, int]]:
    """
    获取实际可捕获的游戏区域（客户区在屏幕上的位置）
    与 click.py 保持一致
    """
    try:
        window_rect = get_window_rect_dwm(hwnd)
        if not window_rect:
            return None
        
        client_rect = win32gui.GetClientRect(hwnd)
        if not client_rect:
            return None
        
        win_left, win_top, win_right, win_bottom = window_rect
        client_left, client_top, client_right, client_bottom = client_rect
        
        client_width = client_right - client_left
        client_height = client_bottom - client_top
        win_height = win_bottom - win_top
        
        left = win_left
        top = win_top + win_height - client_height
        right = left + client_width
        bottom = top + client_height
        
        return (left, top, right, bottom)
    except Exception:
        return None

def capture_screen() -> Image.Image:
    """截取全屏"""
    hwnd = win32gui.GetDesktopWindow()
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top
    
    hdesktop = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hdesktop)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)
    
    result = saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    
    img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1
    )
    
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)
    
    return img

def capture_window_client_area(window_title: str) -> Optional[Image.Image]:
    """
    截取指定窗口的客户区（游戏画面区域）
    与 click.py 使用相同的坐标系
    """
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        print(f'[screenshot] 错误: 未找到窗口 "{window_title}"')
        return None
    
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.3)
    
    capture_rect = get_capture_rect(hwnd)
    if not capture_rect:
        print('[screenshot] 错误: 无法获取窗口捕获区域')
        return None
    
    left, top, right, bottom = capture_rect
    width = right - left
    height = bottom - top
    
    hdesktop = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hdesktop)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)
    
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (left, top), win32con.SRCCOPY)
    
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    
    img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1
    )
    
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)
    
    return img

def take_screenshot(window_title: Optional[str] = None) -> str:
    """
    截图并保存
    
    Args:
        window_title: 窗口标题（可选），用于按游戏分类整理
    
    Returns:
        截图文件的相对路径
    """
    target_dir = ensure_screenshots_dir(window_title)
    
    timestamp = get_timestamp()
    filename = f'screenshot_{timestamp}.png'
    
    filepath = os.path.join(target_dir, filename)
    
    try:
        if window_title:
            img = capture_window_client_area(window_title)
            if img is None:
                img = capture_screen()
        else:
            img = capture_screen()
        
        img.save(filepath)
        
        return os.path.relpath(filepath, os.path.dirname(__file__))
    except Exception as e:
        print(f'[screenshot] 错误: {e}')
        raise

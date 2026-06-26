import ctypes
import time
import random
import win32con
import win32gui
from ctypes import wintypes
from typing import Optional, Tuple

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
dwmapi = ctypes.windll.dwmapi

class RECT(ctypes.Structure):
    _fields_ = [
        ('left', ctypes.c_long),
        ('top', ctypes.c_long),
        ('right', ctypes.c_long),
        ('bottom', ctypes.c_long)
    ]

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ('dx', wintypes.LONG),
        ('dy', wintypes.LONG),
        ('mouseData', wintypes.DWORD),
        ('dwFlags', wintypes.DWORD),
        ('time', wintypes.DWORD),
        ('dwExtraInfo', ctypes.POINTER(wintypes.ULONG)),
    ]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ('wVk', wintypes.WORD),
        ('wScan', wintypes.WORD),
        ('dwFlags', wintypes.DWORD),
        ('time', wintypes.DWORD),
        ('dwExtraInfo', ctypes.POINTER(wintypes.ULONG)),
    ]

class INPUTUNION(ctypes.Union):
    _fields_ = [
        ('mi', MOUSEINPUT),
        ('ki', KEYBDINPUT),
    ]

class INPUT(ctypes.Structure):
    _anonymous_ = ('u',)
    _fields_ = [
        ('type', wintypes.DWORD),
        ('u', INPUTUNION),
    ]

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

def get_physical_screen_size() -> Tuple[int, int]:
    """
    获取物理屏幕分辨率（参考 BetterGI PrimaryScreen.WorkingArea）
    使用 GetDeviceCaps 获取无 DPI 缩放的真实分辨率
    """
    hdc = user32.GetDC(0)
    HORZRES = 8
    VERTRES = 10
    width = gdi32.GetDeviceCaps(hdc, HORZRES)
    height = gdi32.GetDeviceCaps(hdc, VERTRES)
    user32.ReleaseDC(0, hdc)
    return width, height

def get_window_handle(window_title: str) -> Optional[int]:
    """获取窗口句柄"""
    hwnd = win32gui.FindWindow(None, window_title)
    return hwnd if hwnd else None

def get_window_rect_dwm(hwnd: int) -> Optional[Tuple[int, int, int, int]]:
    """
    使用 DwmGetWindowAttribute 获取窗口位置（参考 BetterGI SystemControl.GetWindowRect）
    这个方法获取的是窗口的真实可见区域，不包括 Windows DWM 添加的阴影等效果
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

def get_client_rect(hwnd: int) -> Optional[Tuple[int, int, int, int]]:
    """
    获取客户区大小（参考 BetterGI SystemControl.GetGameScreenRect）
    """
    try:
        return win32gui.GetClientRect(hwnd)
    except Exception:
        return None

def get_capture_rect(hwnd: int) -> Optional[Tuple[int, int, int, int]]:
    """
    获取实际可捕获的游戏区域（参考 BetterGI SystemControl.GetCaptureRect）
    计算游戏客户区在屏幕上的实际位置
    """
    try:
        window_rect = get_window_rect_dwm(hwnd)
        if not window_rect:
            return None
        
        client_rect = get_client_rect(hwnd)
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

def get_window_info(window_title: str) -> Optional[dict]:
    """获取窗口信息"""
    hwnd = get_window_handle(window_title)
    if not hwnd:
        return None
    
    capture_rect = get_capture_rect(hwnd)
    if not capture_rect:
        return None
    
    left, top, right, bottom = capture_rect
    return {
        'hwnd': hwnd,
        'left': left,
        'top': top,
        'width': right - left,
        'height': bottom - top
    }

def activate_window(hwnd: int) -> bool:
    """激活窗口"""
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.05)
        return True
    except Exception:
        return False

def make_lparam(x: int, y: int) -> int:
    """构造 LPARAM 参数 (y << 16) | (x & 0xFFFF)"""
    return (y << 16) | (x & 0xFFFF)

def send_input(inputs):
    """调用 SendInput API"""
    n_inputs = len(inputs)
    input_size = ctypes.sizeof(INPUT)
    user32.SendInput(n_inputs, ctypes.byref(inputs), input_size)

def move_mouse_sendinput(x: int, y: int, screen_width: int, screen_height: int):
    """
    使用 SendInput 移动鼠标（参考 BetterGI MouseSimulator.MoveMouseTo）
    坐标归一化公式：x * 65535 / screenWidth
    """
    normalized_x = int(x * 65535 / screen_width)
    normalized_y = int(y * 65535 / screen_height)
    
    inputs = (INPUT * 1)()
    inputs[0].type = INPUT_MOUSE
    inputs[0].mi.dx = normalized_x
    inputs[0].mi.dy = normalized_y
    inputs[0].mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
    
    send_input(inputs)

def left_button_down_sendinput():
    """使用 SendInput 按下左键"""
    inputs = (INPUT * 1)()
    inputs[0].type = INPUT_MOUSE
    inputs[0].mi.dwFlags = MOUSEEVENTF_LEFTDOWN
    send_input(inputs)

def left_button_up_sendinput():
    """使用 SendInput 释放左键"""
    inputs = (INPUT * 1)()
    inputs[0].type = INPUT_MOUSE
    inputs[0].mi.dwFlags = MOUSEEVENTF_LEFTUP
    send_input(inputs)

def right_button_down_sendinput():
    """使用 SendInput 按下右键"""
    inputs = (INPUT * 1)()
    inputs[0].type = INPUT_MOUSE
    inputs[0].mi.dwFlags = MOUSEEVENTF_RIGHTDOWN
    send_input(inputs)

def right_button_up_sendinput():
    """使用 SendInput 释放右键"""
    inputs = (INPUT * 1)()
    inputs[0].type = INPUT_MOUSE
    inputs[0].mi.dwFlags = MOUSEEVENTF_RIGHTUP
    send_input(inputs)

def click_foreground_sendinput(x: int, y: int) -> bool:
    """
    前台物理点击（参考 BetterGI DesktopRegion.DesktopRegionClick）
    使用 SendInput API 模拟真实鼠标操作
    """
    if x == 0 and y == 0:
        return False
    
    screen_width, screen_height = get_physical_screen_size()
    
    move_mouse_sendinput(x, y, screen_width, screen_height)
    time.sleep(0.01)
    
    left_button_down_sendinput()
    time.sleep(0.02 + random.random() * 0.01)
    left_button_up_sendinput()
    
    return True

def click_background(hwnd: int, x: int, y: int) -> bool:
    """
    后台虚拟点击（参考 BetterGI PostMessageSimulator.LeftButtonClickBackground）
    使用 PostMessage 发送窗口消息，不抢夺鼠标
    """
    try:
        lparam = make_lparam(x, y)
        
        win32gui.PostMessage(hwnd, win32con.WM_ACTIVATE, 1, 0)
        time.sleep(0.01)
        
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 1, lparam)
        time.sleep(0.1)
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lparam)
        
        return True
    except Exception:
        return False

def right_click_background(hwnd: int, x: int, y: int) -> bool:
    """后台虚拟右键点击"""
    try:
        lparam = make_lparam(x, y)
        
        win32gui.PostMessage(hwnd, win32con.WM_ACTIVATE, 1, 0)
        time.sleep(0.01)
        
        win32gui.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, 1, lparam)
        time.sleep(0.1)
        win32gui.PostMessage(hwnd, win32con.WM_RBUTTONUP, 0, lparam)
        
        return True
    except Exception:
        return False

def click(x: int, y: int, window_title: Optional[str] = None, background: bool = False) -> bool:
    """
    统一点击接口
    
    Args:
        x: X 坐标（相对于窗口客户区，即截图坐标系）
        y: Y 坐标（相对于窗口客户区，即截图坐标系）
        window_title: 窗口标题（可选）
        background: 是否后台点击
    
    Returns:
        是否成功
    """
    if window_title:
        win_info = get_window_info(window_title)
        if not win_info:
            print(f'[click] 错误: 未找到窗口 "{window_title}"')
            return False
        
        hwnd = win_info['hwnd']
        win_width = win_info['width']
        win_height = win_info['height']
        
        if x < 0 or x >= win_width or y < 0 or y >= win_height:
            print(f'[click] 错误: 坐标 ({x}, {y}) 超出窗口范围 (0-{win_width-1}, 0-{win_height-1})')
            return False
        
        screen_x = win_info['left'] + x
        screen_y = win_info['top'] + y
        
        if background:
            return click_background(hwnd, x, y)
        else:
            activate_window(hwnd)
            time.sleep(0.05 + random.random() * 0.03)
            return click_foreground_sendinput(screen_x, screen_y)
    else:
        if background:
            print('[click] 错误: 后台模式需要指定窗口标题')
            return False
        return click_foreground_sendinput(x, y)

def right_click(x: int, y: int, window_title: Optional[str] = None, background: bool = False) -> bool:
    """右键点击"""
    print(f'[click] 右键点击坐标: ({x}, {y})')
    
    if window_title:
        win_info = get_window_info(window_title)
        if not win_info:
            print(f'[click] 未找到窗口: {window_title}')
            return False
        
        hwnd = win_info['hwnd']
        screen_x = win_info['left'] + x
        screen_y = win_info['top'] + y
        
        if background:
            return right_click_background(hwnd, x, y)
        else:
            activate_window(hwnd)
            time.sleep(0.05)
            screen_width, screen_height = get_physical_screen_size()
            move_mouse_sendinput(screen_x, screen_y, screen_width, screen_height)
            time.sleep(0.02)
            right_button_down_sendinput()
            time.sleep(0.02 + random.random() * 0.01)
            right_button_up_sendinput()
            return True
    else:
        if background:
            return False
        screen_width, screen_height = get_physical_screen_size()
        move_mouse_sendinput(x, y, screen_width, screen_height)
        time.sleep(0.02)
        right_button_down_sendinput()
        time.sleep(0.02)
        right_button_up_sendinput()
        return True

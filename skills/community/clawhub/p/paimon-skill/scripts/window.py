import win32gui
import win32con
from typing import Optional, Tuple

def get_window_handle(window_title: str) -> Optional[int]:
    """获取窗口句柄"""
    hwnd = win32gui.FindWindow(None, window_title)
    return hwnd if hwnd else None

def get_window_rect(window_title: str) -> Optional[Tuple[int, int, int, int]]:
    """获取窗口位置和大小 (left, top, right, bottom)"""
    hwnd = get_window_handle(window_title)
    if not hwnd:
        return None
    
    try:
        return win32gui.GetWindowRect(hwnd)
    except Exception:
        return None

def get_window_info(window_title: str) -> Optional[dict]:
    """获取窗口信息"""
    hwnd = get_window_handle(window_title)
    if not hwnd:
        return None
    
    rect = get_window_rect(window_title)
    if not rect:
        return None
    
    left, top, right, bottom = rect
    return {
        'hwnd': hwnd,
        'title': window_title,
        'left': left,
        'top': top,
        'width': right - left,
        'height': bottom - top
    }

def activate_window(window_title: str) -> bool:
    """激活窗口"""
    hwnd = get_window_handle(window_title)
    if not hwnd:
        return False
    
    try:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        
        win32gui.SetForegroundWindow(hwnd)
        return True
    except Exception:
        return False

def to_screen_coords(x: int, y: int, window_title: str) -> Optional[Tuple[int, int]]:
    """将窗口相对坐标转换为屏幕绝对坐标"""
    rect = get_window_rect(window_title)
    if not rect:
        return None
    
    left, top, _, _ = rect
    return (left + x, top + y)

def list_windows() -> list:
    """列出所有窗口"""
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                windows.append({
                    'hwnd': hwnd,
                    'title': title
                })
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

def find_window_by_partial_title(partial_title: str) -> Optional[str]:
    """根据部分标题查找窗口"""
    windows = list_windows()
    for win in windows:
        if partial_title.lower() in win['title'].lower():
            return win['title']
    return None

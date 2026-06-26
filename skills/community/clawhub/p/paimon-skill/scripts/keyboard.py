import time
import random
import win32api
import win32con
import win32gui
from typing import Optional

VK_CODES = {
    'w': 0x57, 'a': 0x41, 's': 0x53, 'd': 0x44,
    'q': 0x51, 'e': 0x45, 'r': 0x52, 't': 0x54,
    'z': 0x5A, 'x': 0x58, 'c': 0x43, 'v': 0x56,
    'b': 0x42, 'n': 0x4E, 'm': 0x4D,
    'f': 0x46, 'g': 0x47, 'h': 0x48, 'j': 0x4A,
    'k': 0x4B, 'l': 0x4C, 'y': 0x59, 'u': 0x55,
    'i': 0x49, 'o': 0x4F, 'p': 0x50,
    '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
    '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38,
    '9': 0x39, '0': 0x30,
    'space': win32con.VK_SPACE,
    'enter': win32con.VK_RETURN,
    'return': win32con.VK_RETURN,
    'escape': win32con.VK_ESCAPE,
    'esc': win32con.VK_ESCAPE,
    'tab': win32con.VK_TAB,
    'shift': win32con.VK_SHIFT,
    'leftshift': win32con.VK_LSHIFT,
    'rightshift': win32con.VK_RSHIFT,
    'ctrl': win32con.VK_CONTROL,
    'leftctrl': win32con.VK_LCONTROL,
    'rightctrl': win32con.VK_RCONTROL,
    'alt': win32con.VK_MENU,
    'leftalt': win32con.VK_LMENU,
    'rightalt': win32con.VK_RMENU,
    'f1': win32con.VK_F1, 'f2': win32con.VK_F2,
    'f3': win32con.VK_F3, 'f4': win32con.VK_F4,
    'f5': win32con.VK_F5, 'f6': win32con.VK_F6,
    'f7': win32con.VK_F7, 'f8': win32con.VK_F8,
}

def get_vk_code(key_name: str) -> Optional[int]:
    """获取虚拟键代码"""
    return VK_CODES.get(key_name.lower())

def key_down(key_name: str, hwnd: Optional[int] = None) -> bool:
    """按下按键"""
    vk = get_vk_code(key_name)
    if vk is None:
        print(f'[keyboard] 未知按键: {key_name}')
        return False
    
    if hwnd:
        win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, vk, 0x1e0001)
    else:
        win32api.keybd_event(vk, 0, 0, 0)
    
    return True

def key_up(key_name: str, hwnd: Optional[int] = None) -> bool:
    """释放按键"""
    vk = get_vk_code(key_name)
    if vk is None:
        return False
    
    if hwnd:
        win32gui.PostMessage(hwnd, win32con.WM_KEYUP, vk, 0xc01e0001)
    else:
        win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
    
    return True

def press_key(key_name: str, delay_ms: int = 100, hwnd: Optional[int] = None) -> bool:
    """
    按下并释放按键
    
    Args:
        key_name: 按键名称
        delay_ms: 按住时间（毫秒）
        hwnd: 窗口句柄（可选，用于后台按键）
    """
    print(f'[keyboard] 按键: {key_name}')
    
    if not key_down(key_name, hwnd):
        return False
    
    time.sleep(delay_ms / 1000.0)
    
    if not key_up(key_name, hwnd):
        return False
    
    return True

def hold_key(key_name: str, hold_ms: int, delay_ms: int = 100, hwnd: Optional[int] = None) -> bool:
    """
    按住按键一段时间
    
    Args:
        key_name: 按键名称
        hold_ms: 按住时间（毫秒）
        delay_ms: 释放后延迟（毫秒）
        hwnd: 窗口句柄（可选，用于后台按键）
    """
    print(f'[keyboard] 按住 {key_name} {hold_ms}ms')
    
    if not key_down(key_name, hwnd):
        return False
    
    time.sleep(hold_ms / 1000.0)
    
    if not key_up(key_name, hwnd):
        return False
    
    if delay_ms > 0:
        time.sleep(delay_ms / 1000.0)
    
    return True

def key_sequence(keys: list, delay_ms: int = 200, hwnd: Optional[int] = None) -> bool:
    """
    按键序列
    
    Args:
        keys: 按键列表
        delay_ms: 每个按键之间的延迟（毫秒）
        hwnd: 窗口句柄（可选，用于后台按键）
    """
    print(f'[keyboard] 按键序列: {" + ".join(keys)}')
    
    for key in keys:
        if not press_key(key, delay_ms, hwnd):
            return False
    
    return True

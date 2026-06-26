"""
窗口管理模块 - 提供窗口列表、最小化、最大化、关闭、聚焦等功能
"""
import win32gui
import win32con
import ctypes
from typing import List, Optional


def _get_window_text(hwnd):
    length = win32gui.GetWindowTextLength(hwnd)
    if length:
        return win32gui.GetWindowText(hwnd)
    return ""


def _enum_windows_callback(hwnd, windows):
    if win32gui.IsWindowVisible(hwnd):
        title = _get_window_text(hwnd)
        if title:
            windows.append({
                'hwnd': hwnd,
                'title': title
            })


def window_list():
    try:
        windows = []
        win32gui.EnumWindows(_enum_window_callback, windows)
        return {
            "success": True,
            "data": {"windows": windows},
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def _enum_window_callback(hwnd, windows):
    if win32gui.IsWindowVisible(hwnd):
        title = _get_window_text(hwnd)
        if title:
            windows.append({
                'hwnd': hwnd,
                'title': title
            })


def window_find(title: str) -> Optional[int]:
    windows = []
    win32gui.EnumWindows(_enum_window_callback, windows)
    for w in windows:
        if title.lower() in w['title'].lower():
            return w['hwnd']
    return None


def window_minimize(title: str):
    try:
        hwnd = window_find(title)
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            return {"success": True, "data": {"title": title}, "error": None}
        return {"success": False, "data": None, "error": "窗口未找到"}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def window_maximize(title: str):
    try:
        hwnd = window_find(title)
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            return {"success": True, "data": {"title": title}, "error": None}
        return {"success": False, "data": None, "error": "窗口未找到"}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def window_close(title: str):
    try:
        hwnd = window_find(title)
        if hwnd:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            return {"success": True, "data": {"title": title}, "error": None}
        return {"success": False, "data": None, "error": "窗口未找到"}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def window_focus(title: str):
    try:
        hwnd = window_find(title)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            return {"success": True, "data": {"title": title}, "error": None}
        return {"success": False, "data": None, "error": "窗口未找到"}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}

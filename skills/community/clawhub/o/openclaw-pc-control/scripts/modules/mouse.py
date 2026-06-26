"""
鼠标模块 - 提供鼠标移动、点击、拖拽等操作功能
"""
import pyautogui
from typing import Optional


def mouse_move(x: int, y: int, duration: float = 0):
    try:
        pyautogui.moveTo(x, y, duration=duration)
        return {"success": True, "data": {"x": x, "y": y}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def mouse_click(x: Optional[int] = None, y: Optional[int] = None, clicks: int = 1):
    try:
        pyautogui.click(x, y, clicks=clicks)
        return {"success": True, "data": {"x": x, "y": y, "clicks": clicks}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def mouse_double_click(x: Optional[int] = None, y: Optional[int] = None):
    try:
        pyautogui.doubleClick(x, y)
        return {"success": True, "data": {"x": x, "y": y}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def mouse_right_click(x: Optional[int] = None, y: Optional[int] = None):
    try:
        pyautogui.rightClick(x, y)
        return {"success": True, "data": {"x": x, "y": y}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def mouse_drag(x: int, y: int, duration: float = 0.5):
    try:
        pyautogui.dragTo(x, y, duration=duration)
        return {"success": True, "data": {"x": x, "y": y, "duration": duration}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def mouse_scroll(clicks: int, x: int = -1, y: int = -1):
    try:
        pyautogui.scroll(clicks, x, y)
        return {"success": True, "data": {"clicks": clicks, "x": x, "y": y}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def get_mouse_position():
    try:
        x, y = pyautogui.position()
        return {"success": True, "data": {"x": x, "y": y}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}

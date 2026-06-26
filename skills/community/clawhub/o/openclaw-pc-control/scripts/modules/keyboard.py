"""
键盘模块 - 提供键盘按键操作功能
"""
import pyautogui
from typing import List


def key_press(key: str):
    try:
        pyautogui.press(key)
        return {"success": True, "data": {"key": key}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def key_type(text: str, interval: float = 0.05):
    try:
        pyautogui.write(text, interval=interval)
        return {"success": True, "data": {"text": text}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def key_hotkey(keys: List[str]):
    try:
        pyautogui.hotkey(*keys)
        return {"success": True, "data": {"keys": keys}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def key_down(key: str):
    try:
        pyautogui.keyDown(key)
        return {"success": True, "data": {"key": key}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def key_up(key: str):
    try:
        pyautogui.keyUp(key)
        return {"success": True, "data": {"key": key}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}

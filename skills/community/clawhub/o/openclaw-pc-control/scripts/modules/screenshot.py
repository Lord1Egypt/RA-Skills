"""
屏幕截图模块 - 提供屏幕截图和屏幕信息获取功能
"""
import pyautogui
import mss
import os


def take_screenshot(path: str = "screenshot.png"):
    try:
        with mss.mss() as sct:
            sct.shot(output=path)
        abs_path = os.path.abspath(path)
        return {
            "success": True,
            "data": {"path": abs_path, "filename": os.path.basename(abs_path)},
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def get_screen_info():
    try:
        size = pyautogui.size()
        with mss.mss() as sct:
            monitors = sct.monitors
        return {
            "success": True,
            "data": {
                "width": size.width,
                "height": size.height,
                "monitors": monitors
            },
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}

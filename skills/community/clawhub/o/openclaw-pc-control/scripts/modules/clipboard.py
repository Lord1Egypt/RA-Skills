"""
剪贴板模块 - 提供剪贴板读写功能
"""
import pyperclip


def clipboard_read():
    try:
        text = pyperclip.paste()
        return {
            "success": True,
            "data": {"text": text},
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def clipboard_write(text: str):
    try:
        pyperclip.copy(text)
        return {
            "success": True,
            "data": {"text": text},
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}

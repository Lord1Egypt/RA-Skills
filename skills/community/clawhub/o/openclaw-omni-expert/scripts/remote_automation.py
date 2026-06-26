#!/usr/bin/env python3
"""
Windows UI 自动化控制模块
通过 UU exec 在远程 Windows 上执行 PyAutoGUI/PyWinauto 操作
"""

import os
import subprocess
import json
import time
import argparse
from typing import Optional, Tuple, List, Dict, Any


class WindowsAutomator:
    """Windows UI 自动化控制器"""
    
    def __init__(self, uu_exec_func=None):
        """
        uu_exec_func: 执行 UU 命令的函数 (command) -> (success, output)
        """
        self.exec_func = uu_exec_func or self._default_exec
    
    def _default_exec(self, command: str) -> Tuple[bool, str]:
        """默认通过 uu exec 执行"""
        try:
            result = subprocess.run(
                ["uu", "exec", "--", command],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0, result.stdout
        except Exception as e:
            return False, str(e)
    
    def _check_automation_ready(self) -> bool:
        """检查远程自动化环境是否就绪"""
        # 检查 Python 是否可用
        success, _ = self.exec_func("python --version")
        if not success:
            return False
        
        # 检查自动化库
        success, _ = self.exec_func("pip show pyautogui")
        if not success:
            print("提示: 远程机器需要安装 pyautogui")
            print("安装命令: pip install pyautogui Pillow")
            return False
        
        return True
    
    def _ensure_pyautogui(self) -> bool:
        """确保远程机器安装了 PyAutoGUI"""
        # 先安装依赖
        self.exec_func("pip install pyautogui Pillow numpy opencv-python")
        return self._check_automation_ready()
    
    def mouse_move(self, x: int, y: int, duration: float = 0.5) -> bool:
        """移动鼠标"""
        cmd = f'python -c "import pyautogui; pyautogui.moveTo({x}, {y}, {duration})"'
        success, _ = self.exec_func(cmd)
        return success
    
    def mouse_click(self, x: Optional[int] = None, y: Optional[int] = None, 
                   button: str = "left", clicks: int = 1) -> bool:
        """点击鼠标"""
        if x is not None and y is not None:
            cmd = f'python -c "import pyautogui; pyautogui.click({x}, {y}, clicks={clicks}, button=\'{button}\')"'
        else:
            cmd = f'python -c "import pyautogui; pyautogui.click(clicks={clicks}, button=\'{button}\')"'
        
        success, _ = self.exec_func(cmd)
        return success
    
    def mouse_double_click(self, x: int, y: int) -> bool:
        """双击"""
        return self.mouse_click(x, y, clicks=2)
    
    def mouse_right_click(self, x: int, y: int) -> bool:
        """右键点击"""
        return self.mouse_click(x, y, button="right")
    
    def mouse_drag(self, start_x: int, start_y: int, end_x: int, end_y: int, 
                   duration: float = 1.0) -> bool:
        """拖拽"""
        cmd = f'python -c "import pyautogui; pyautogui.moveTo({start_x}, {start_y}); pyautogui.drag({end_x-start_x}, {end_y-start_y}, {duration})"'
        success, _ = self.exec_func(cmd)
        return success
    
    def scroll(self, clicks: int) -> bool:
        """滚动鼠标"""
        cmd = f'python -c "import pyautogui; pyautogui.scroll({clicks})"'
        success, _ = self.exec_func(cmd)
        return success
    
    def typewrite(self, text: str, interval: float = 0.05) -> bool:
        """输入文本"""
        # 转义特殊字符
        escaped_text = text.replace('"', '\\"').replace("'", "\\'")
        cmd = f'python -c "import pyautogui; pyautogui.typewrite(\'{escaped_text}\', {interval})"'
        success, _ = self.exec_func(cmd)
        return success
    
    def press_key(self, key: str) -> bool:
        """按键"""
        cmd = f'python -c "import pyautogui; pyautogui.press(\'{key}\')"'
        success, _ = self.exec_func(cmd)
        return success
    
    def hotkey(self, *keys) -> bool:
        """组合键"""
        keys_str = ", ".join([f"'{k}'" for k in keys])
        cmd = f'python -c "import pyautogui; pyautogui.hotkey({keys_str})"'
        success, _ = self.exec_func(cmd)
        return success
    
    def get_screen_size(self) -> Optional[Tuple[int, int]]:
        """获取屏幕分辨率"""
        cmd = 'python -c "import pyautogui; print(pyautogui.size())"'
        success, output = self.exec_func(cmd)
        
        if success and output:
            try:
                # 解析输出如 Size(width=1920, height=1080)
                output = output.strip()
                width = int(output.split("width=")[1].split(",")[0])
                height = int(output.split("height=")[1].split(")")[0])
                return (width, height)
            except:
                return None
        return None
    
    def locate_on_screen(self, image_path: str, confidence: float = 0.9) -> Optional[Tuple[int, int, int, int]]:
        """在屏幕上查找图像位置"""
        if not os.path.exists(image_path):
            print(f"图像文件不存在: {image_path}")
            return None
        
        cmd = f'python -c "import pyautogui; pos = pyautogui.locateOnScreen(r\'{image_path}\', confidence={confidence}); print(pos)"'
        success, output = self.exec_func(cmd)
        
        if success and output and "None" not in output:
            try:
                # 解析 Box 对象
                parts = output.strip().strip("()").split(",")
                return tuple(int(p.split("=")[1]) for p in parts)
            except:
                return None
        return None
    
    def locate_center_on_screen(self, image_path: str, confidence: float = 0.9) -> Optional[Tuple[int, int]]:
        """查找图像中心坐标"""
        box = self.locate_on_screen(image_path, confidence)
        if box:
            center_x = box[0] + box[2] // 2
            center_y = box[1] + box[3] // 2
            return (center_x, center_y)
        return None
    
    def click_image(self, image_path: str, confidence: float = 0.9) -> bool:
        """点击屏幕上的图像"""
        pos = self.locate_center_on_screen(image_path, confidence)
        if pos:
            return self.mouse_click(pos[0], pos[1])
        return False
    
    # ========== 常用操作封装 ==========
    
    def open_start_menu(self) -> bool:
        """打开开始菜单"""
        return self.press_key("win")
    
    def open_app(self, app_name: str) -> bool:
        """打开应用程序"""
        self.open_start_menu()
        time.sleep(0.5)
        self.typewrite(app_name)
        time.sleep(0.5)
        self.press_key("enter")
        return True
    
    def close_window(self) -> bool:
        """关闭窗口 (Alt+F4)"""
        return self.hotkey("alt", "f4")
    
    def minimize_window(self) -> bool:
        """最小化窗口"""
        return self.hotkey("win", "down")
    
    def maximize_window(self) -> bool:
        """最大化窗口"""
        return self.hotkey("win", "up")
    
    def switch_window(self) -> bool:
        """切换窗口 (Alt+Tab)"""
        return self.hotkey("alt", "tab")
    
    def screenshot(self, save_path: str = "screenshot.png") -> bool:
        """截图"""
        cmd = f'python -c "import pyautogui; pyautogui.screenshot(r\'{save_path}\')"'
        success, _ = self.exec_func(cmd)
        return success
    
    def paste_text(self, text: str) -> bool:
        """粘贴文本"""
        # 先复制到剪贴板（通过 PowerShell）
        ps_cmd = f'Set-Clipboard -Value "{text}"'
        self.exec_func(f'powershell -Command "{ps_cmd}"')
        time.sleep(0.2)
        return self.hotkey("ctrl", "v")
    
    def select_all(self) -> bool:
        """全选"""
        return self.hotkey("ctrl", "a")
    
    def copy(self) -> bool:
        """复制"""
        return self.hotkey("ctrl", "c")
    
    def paste(self) -> bool:
        """粘贴"""
        return self.hotkey("ctrl", "v")
    
    def save(self) -> bool:
        """保存"""
        return self.hotkey("ctrl", "s")
    
    def find_and_click(self, text: str, image_dir: str = "./templates") -> bool:
        """查找并点击"""
        # 在模板目录查找匹配的图像
        template_path = os.path.join(image_dir, f"{text}.png")
        return self.click_image(template_path)


# ========== 高级操作 ==========

class WindowsUIAutomator(WindowsAutomator):
    """基于 UIAutomation 的 Windows UI 自动化"""
    
    def __init__(self, uu_exec_func=None):
        super().__init__(uu_exec_func)
        self._ensure_uiauto()
    
    def _ensure_uiauto(self):
        """确保 UIAutomation 库已安装"""
        self.exec_func("pip install uiautomation")
    
    def find_window(self, window_name: str) -> bool:
        """查找窗口"""
        cmd = f'python -c "import uiautomation; w = uiautomation.WindowControl(Name=\'{window_name}\'); print(w.Exists)"'
        success, output = self.exec_func(cmd)
        return success and "True" in output
    
    def click_button_by_text(self, text: str) -> bool:
        """根据文本点击按钮"""
        cmd = f'''python -c "import uiautomation; btn = uiautomation.ButtonControl(Name=\'{text}\'); btn.Click()"'''
        success, _ = self.exec_func(cmd)
        return success
    
    def click_by_automation_id(self, automation_id: str) -> bool:
        """根据 AutomationId 点击"""
        cmd = f'''python -c "import uiautomation; ctrl = uiautomation.Control(AutomationId=\'{automation_id}\'); ctrl.Click()"'''
        success, _ = self.exec_func(cmd)
        return success
    
    def get_control_text(self, control_type: str, name: str) -> Optional[str]:
        """获取控件文本"""
        cmd = f'''python -c "import uiautomation; ctrl = uiautomation.{control_type}Control(Name=\'{name}\'); print(ctrl.Name)"'''
        success, output = self.exec_func(cmd)
        return output.strip() if success else None


def demo_mode(exec_func):
    """演示模式"""
    automator = WindowsAutomator(uu_exec_func=exec_func)
    
    print("Windows 自动化演示")
    print("=" * 50)
    
    # 获取屏幕大小
    size = automator.get_screen_size()
    if size:
        print(f"屏幕分辨率: {size[0]}x{size[1]}")
    
    # 测试鼠标
    print("\n测试鼠标移动到中心...")
    if size:
        automator.mouse_move(size[0]//2, size[1]//2)
    
    # 测试键盘
    print("测试按键...")
    automator.press_key("win")
    time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Windows UI 自动化控制器")
    parser.add_argument("--action", "-a", required=True, 
                       choices=["move", "click", "double-click", "right-click", 
                               "drag", "scroll", "type", "press", "hotkey",
                               "screenshot", "open-app", "close-window"],
                       help="操作类型")
    parser.add_argument("--x", type=int, help="X 坐标")
    parser.add_argument("--y", type=int, help="Y 坐标")
    parser.add_argument("--text", "-t", help="文本输入")
    parser.add_argument("--key", "-k", help="按键")
    parser.add_argument("--keys", nargs="+", help="组合键")
    parser.add_argument("--app", help="应用程序名")
    parser.add_argument("--scroll", type=int, default=0, help="滚动次数")
    parser.add_argument("--output", "-o", default="screenshot.png", help="输出文件")
    
    args = parser.parse_args()
    
    # 创建自动化器
    automator = WindowsAutomator()
    
    # 执行操作
    if args.action == "move":
        if args.x and args.y:
            automator.mouse_move(args.x, args.y)
    elif args.action == "click":
        automator.mouse_click(args.x, args.y)
    elif args.action == "double-click":
        automator.mouse_double_click(args.x, args.y)
    elif args.action == "right-click":
        automator.mouse_right_click(args.x, args.y)
    elif args.action == "scroll":
        automator.scroll(args.scroll)
    elif args.action == "type":
        if args.text:
            automator.typewrite(args.text)
    elif args.action == "press":
        if args.key:
            automator.press_key(args.key)
    elif args.action == "hotkey":
        if args.keys:
            automator.hotkey(*args.keys)
    elif args.action == "screenshot":
        automator.screenshot(args.output)
    elif args.action == "open-app":
        if args.app:
            automator.open_app(args.app)
    elif args.action == "close-window":
        automator.close_window()

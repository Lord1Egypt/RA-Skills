#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
浏览器扩展自动点击工具
使用 pyautogui 实现系统级 GUI 自动化，点击浏览器扩展图标
"""

import argparse
import sys
import time
import os
from pathlib import Path

# 尝试导入 pyautogui
try:
    import pyautogui
    from PIL import Image
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("警告：pyautogui 未安装，请运行：pip install pyautogui Pillow")

# 配置
SCREEN_WIDTH = pyautogui.size().width if PYAUTOGUI_AVAILABLE else 1920
SCREEN_HEIGHT = pyautogui.size().height if PYAUTOGUI_AVAILABLE else 1080

# 扩展图标位置配置（基于常见分辨率）
EXTENSION_POSITIONS = {
    "openclaw": {
        "1920x1080": {"x": 1850, "y": 50},
        "2560x1440": {"x": 2450, "y": 60},
        "3840x2160": {"x": 3700, "y": 80},
        "default": {"x": int(SCREEN_WIDTH * 0.96), "y": int(SCREEN_HEIGHT * 0.05)},
    },
    "puzzle_menu": {  # Chrome 扩展菜单（拼图图标）
        "1920x1080": {"x": 1800, "y": 50},
        "2560x1440": {"x": 2400, "y": 60},
        "default": {"x": int(SCREEN_WIDTH * 0.94), "y": int(SCREEN_HEIGHT * 0.05)},
    }
}


def get_screen_resolution():
    """获取当前屏幕分辨率"""
    if PYAUTOGUI_AVAILABLE:
        w, h = pyautogui.size()
        return f"{w}x{h}"
    return "1920x1080"


def get_icon_position(extension_name, custom_x=None, custom_y=None):
    """获取扩展图标位置"""
    resolution = get_screen_resolution()
    
    # 自定义坐标优先
    if custom_x is not None and custom_y is not None:
        return {"x": custom_x, "y": custom_y}
    
    # 从配置获取
    if extension_name in EXTENSION_POSITIONS:
        config = EXTENSION_POSITIONS[extension_name]
        if resolution in config:
            return config[resolution]
        return config.get("default", {"x": 1850, "y": 50})
    
    # 默认位置（右上角）
    return {"x": int(SCREEN_WIDTH * 0.96), "y": int(SCREEN_HEIGHT * 0.05)}


def take_screenshot(output_path="screenshot.png"):
    """截取屏幕截图"""
    if not PYAUTOGUI_AVAILABLE:
        print("错误：pyautogui 未安装")
        return None
    
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(output_path)
        print(f"截图已保存：{output_path}")
        return output_path
    except Exception as e:
        print(f"截图失败：{e}")
        return None


def find_icon_by_template(icon_name):
    """
    使用模板匹配查找图标位置
    需要预先准备图标模板图片
    """
    template_dir = Path(__file__).parent / "templates"
    template_path = template_dir / f"{icon_name}.png"
    
    if not template_path.exists():
        print(f"模板图片不存在：{template_path}")
        return None
    
    if not PYAUTOGUI_AVAILABLE:
        return None
    
    try:
        location = pyautogui.locateOnScreen(
            str(template_path),
            confidence=0.8,  # 80% 匹配度
            grayscale=False
        )
        if location:
            center = pyautogui.center(location)
            return {"x": center.x, "y": center.y}
        return None
    except Exception as e:
        print(f"模板匹配失败：{e}")
        return None


def click_position(x, y, clicks=1, interval=0.1, button="left"):
    """
    点击指定位置
    
    Args:
        x: X 坐标
        y: Y 坐标
        clicks: 点击次数
        interval: 点击间隔（秒）
        button: 鼠标按钮 (left/right/middle)
    """
    if not PYAUTOGUI_AVAILABLE:
        print("错误：pyautogui 未安装，请运行：pip install pyautogui Pillow")
        return False
    
    try:
        # 安全提示
        print(f"将在 1 秒后点击位置：({x}, {y})")
        print("按 Ctrl+C 取消...")
        time.sleep(1)
        
        # 移动鼠标并点击
        pyautogui.click(x=x, y=y, clicks=clicks, interval=interval, button=button)
        print(f"[OK] 点击完成：({x}, {y})")
        return True
    except Exception as e:
        print(f"点击失败：{e}")
        return False


def click_extension(extension_name="openclaw", custom_x=None, custom_y=None, 
                    delay=1.0, screenshot=False, dry_run=False):
    """
    点击浏览器扩展图标
    
    Args:
        extension_name: 扩展名称
        custom_x: 自定义 X 坐标
        custom_y: 自定义 Y 坐标
        delay: 点击前延迟（秒）
        screenshot: 是否先截图
    """
    print(f"=" * 50)
    print(f"浏览器扩展自动点击工具")
    print(f"=" * 50)
    print(f"目标扩展：{extension_name}")
    print(f"屏幕分辨率：{get_screen_resolution()}")
    
    # 检查 pyautogui
    if not PYAUTOGUI_AVAILABLE:
        print("\n错误：pyautogui 未安装")
        print("请运行：pip install pyautogui Pillow")
        return False
    
    # 截图（可选）
    if screenshot:
        take_screenshot(f"extension_click_{extension_name}.png")
    
    # 尝试模板匹配
    position = find_icon_by_template(extension_name)
    
    # 如果模板匹配失败，使用预设位置
    if position is None:
        print("模板匹配失败，使用预设位置...")
        position = get_icon_position(extension_name, custom_x, custom_y)
    
    print(f"目标位置：({position['x']}, {position['y']})")
    
    # 测试模式
    if dry_run:
        print("[测试模式] 不执行实际点击")
        return True
    
    # 等待
    if delay > 0:
        print(f"等待 {delay} 秒...")
        time.sleep(delay)
    
    # 点击
    success = click_position(position["x"], position["y"])
    
    print(f"=" * 50)
    return success


def calibrate():
    """
    校准模式：用户手动指定图标位置
    """
    print("=" * 50)
    print("校准模式：请在 5 秒内将鼠标移动到图标位置")
    print("=" * 50)
    
    if not PYAUTOGUI_AVAILABLE:
        print("错误：pyautogui 未安装")
        return
    
    time.sleep(5)
    
    x, y = pyautogui.position()
    print(f"\n当前鼠标位置：({x}, {y})")
    print(f"\n请将以下配置添加到脚本中：")
    print(f'"custom": {{"x": {x}, "y": {y}}}')
    
    # 询问是否点击
    response = input("\n是否在此位置点击？(y/n): ")
    if response.lower() == 'y':
        click_position(x, y)


def main():
    parser = argparse.ArgumentParser(
        description="浏览器扩展自动点击工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python click_extension.py --extension openclaw
  python click_extension.py --extension openclaw --browser chrome
  python click_extension.py --x 1850 --y 50
  python click_extension.py --screenshot
  python click_extension.py --calibrate
        """
    )
    
    parser.add_argument(
        "--extension", "-e",
        type=str,
        default="openclaw",
        help="扩展名称 (default: openclaw)"
    )
    
    parser.add_argument(
        "--browser", "-b",
        type=str,
        default="chrome",
        choices=["chrome", "edge", "firefox"],
        help="浏览器类型 (default: chrome)"
    )
    
    parser.add_argument(
        "--x",
        type=int,
        default=None,
        help="自定义 X 坐标"
    )
    
    parser.add_argument(
        "--y",
        type=int,
        default=None,
        help="自定义 Y 坐标"
    )
    
    parser.add_argument(
        "--delay", "-d",
        type=float,
        default=1.0,
        help="点击前延迟（秒）(default: 1.0)"
    )
    
    parser.add_argument(
        "--screenshot", "-s",
        action="store_true",
        help="点击前截图"
    )
    
    parser.add_argument(
        "--calibrate", "-c",
        action="store_true",
        help="校准模式：手动指定图标位置"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="测试模式：只显示位置，不实际点击"
    )
    
    args = parser.parse_args()
    
    if args.calibrate:
        calibrate()
    else:
        success = click_extension(
            extension_name=args.extension,
            custom_x=args.x,
            custom_y=args.y,
            delay=args.delay,
            screenshot=args.screenshot,
            dry_run=args.dry_run
        )
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
macOS 桌面控制 - 鼠标键盘自动化
需要安装：pip3 install --user pyautogui pyscreeze pillow psutil
"""

import sys
import time
import subprocess

# 检查依赖
try:
    import pyautogui
    import psutil
except ImportError as e:
    print(f"❌ 导入失败：{e}")
    print("")
    print("请安装依赖：")
    print("  pip3 install --user pyautogui pyscreeze pillow psutil")
    sys.exit(1)

# 配置
pyautogui.PAUSE = 0.5  # 每个操作后暂停 0.5 秒
pyautogui.FAILSAFE = True  # 启用安全模式（鼠标移到角落停止）

def show_help():
    """显示帮助"""
    print("macOS 桌面控制 - 鼠标键盘自动化")
    print("")
    print("用法：python3 desktop_ctrl.py [模块] [命令] [参数]")
    print("")
    print("模块:")
    print("  mouse          鼠标控制")
    print("  keyboard       键盘控制")
    print("  screenshot     截屏")
    print("  process        进程管理")
    print("")
    print("示例:")
    print("  python3 desktop_ctrl.py mouse position")
    print("  python3 desktop_ctrl.py mouse click 100 100")
    print("  python3 desktop_ctrl.py keyboard type \"Hello\"")
    print("  python3 desktop_ctrl.py keyboard hotkey command c")

def mouse_position():
    """获取鼠标位置"""
    x, y = pyautogui.position()
    print(f"📍 鼠标位置：({x}, {y})")
    
    # 获取屏幕尺寸
    screen_width, screen_height = pyautogui.size()
    print(f"📺 屏幕尺寸：{screen_width}x{screen_height}")

def mouse_click(x=None, y=None, button='left', clicks=1):
    """鼠标点击"""
    if x is not None and y is not None:
        print(f"🖱️  点击位置：({x}, {y})")
        pyautogui.click(x=x, y=y, clicks=clicks, button=button)
    else:
        print(f"🖱️  点击当前位置")
        pyautogui.click(clicks=clicks, button=button)
    print("✅ 点击完成")

def mouse_move(x, y, duration=0.5):
    """移动鼠标"""
    print(f"🖱️  移动到：({x}, {y})")
    pyautogui.moveTo(x, y, duration=duration)
    print("✅ 移动完成")

def mouse_scroll(amount):
    """滚动鼠标"""
    print(f"🖱️  滚动：{amount}")
    pyautogui.scroll(amount)
    print("✅ 滚动完成")

def keyboard_type(text, interval=0.1):
    """键盘输入"""
    print(f"⌨️  输入文字：{text}")
    pyautogui.write(text, interval=interval)
    print("✅ 输入完成")

def keyboard_press(key):
    """按键"""
    print(f"⌨️  按键：{key}")
    pyautogui.press(key)
    print("✅ 按键完成")

def keyboard_hotkey(*keys):
    """快捷键"""
    print(f"⌨️  快捷键：{'+'.join(keys)}")
    pyautogui.hotkey(*keys)
    print("✅ 快捷键完成")

def screenshot_full(output=None):
    """全屏截图"""
    import os
    from datetime import datetime
    
    if output is None:
        output_dir = os.path.expanduser("~/Desktop/OpenClaw-Screenshots")
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = os.path.join(output_dir, f"screenshot_{timestamp}.png")
    
    print(f"📸 正在截屏...")
    screenshot = pyautogui.screenshot()
    screenshot.save(output)
    print(f"✅ 截屏成功：{output}")
    print(f"   文件大小：{os.path.getsize(output) / 1024:.1f} KB")

def process_list(limit=20):
    """进程列表"""
    print("📋 进程列表（CPU 占用前 {} 个）：".format(limit))
    print("")
    print(f"  {'PID':<10} {'名称':<30} {'CPU%':<10}")
    print("  " + "─" * 50)
    
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            info = proc.info
            if info['name'] and info['pid']:
                processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # 按 CPU 排序
    processes.sort(key=lambda x: x.get('cpu_percent', 0) or 0, reverse=True)
    
    for proc in processes[:limit]:
        pid = proc.get('pid', 'N/A')
        name = proc.get('name', 'N/A')[:30]
        cpu = proc.get('cpu_percent', 0) or 0
        print(f"  {pid:<10} {name:<30} {cpu:<10.1f}")
    
    print("")

def process_kill(name):
    """结束进程"""
    print(f"⚠️  正在结束进程：{name}")
    
    killed = 0
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and name.lower() in proc.info['name'].lower():
                pid = proc.info['pid']
                proc.kill()
                print(f"  ✅ 已终止：{proc.info['name']} (PID: {pid})")
                killed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if killed == 0:
        print(f"  ⚠️  未找到匹配的进程：{name}")
    else:
        print(f"✅ 共终止 {killed} 个进程")

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    module = sys.argv[1].lower()
    
    if module == "mouse":
        if len(sys.argv) < 3:
            print("❌ 请指定命令：position, click, move, scroll")
            return
        
        command = sys.argv[2].lower()
        
        if command == "position":
            mouse_position()
        elif command == "click":
            x = int(sys.argv[3]) if len(sys.argv) > 3 else None
            y = int(sys.argv[4]) if len(sys.argv) > 4 else None
            mouse_click(x, y)
        elif command == "move":
            x = int(sys.argv[3])
            y = int(sys.argv[4])
            mouse_move(x, y)
        elif command == "scroll":
            amount = int(sys.argv[3])
            mouse_scroll(amount)
        else:
            print(f"❌ 未知命令：{command}")
    
    elif module == "keyboard":
        if len(sys.argv) < 3:
            print("❌ 请指定命令：type, press, hotkey")
            return
        
        command = sys.argv[2].lower()
        
        if command == "type":
            text = sys.argv[3] if len(sys.argv) > 3 else ""
            keyboard_type(text)
        elif command == "press":
            key = sys.argv[3] if len(sys.argv) > 3 else ""
            keyboard_press(key)
        elif command == "hotkey":
            keys = sys.argv[3:] if len(sys.argv) > 3 else []
            keyboard_hotkey(*keys)
        else:
            print(f"❌ 未知命令：{command}")
    
    elif module == "screenshot":
        output = sys.argv[2] if len(sys.argv) > 2 else None
        screenshot_full(output)
    
    elif module == "process":
        if len(sys.argv) < 3:
            process_list()
            return
        
        command = sys.argv[2].lower()
        
        if command == "list":
            process_list()
        elif command == "kill":
            name = sys.argv[3] if len(sys.argv) > 3 else ""
            process_kill(name)
        else:
            print(f"❌ 未知命令：{command}")
    
    else:
        print(f"❌ 未知模块：{module}")
        show_help()

if __name__ == "__main__":
    main()

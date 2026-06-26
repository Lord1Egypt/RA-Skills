#!/usr/bin/env python3
"""
Linux Desktop Control Tool
Linux 桌面自动化控制
支持截图、鼠标键盘控制、窗口管理等
"""

import sys
import os
import subprocess
import json
from datetime import datetime

def run_command(cmd):
    """运行 shell 命令"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def take_screenshot(output_path=None):
    """截图"""
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"/tmp/screenshot_{timestamp}.png"
    
    success, stdout, stderr = run_command(f"scrot '{output_path}'")
    
    if success:
        return {"success": True, "path": output_path}
    else:
        return {"error": stderr}

def take_window_screenshot(window_id=None, output_path=None):
    """截图指定窗口"""
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"/tmp/window_{timestamp}.png"
    
    if window_id:
        success, stdout, stderr = run_command(f"xwd -id {window_id} | convert xwd:- '{output_path}'")
    else:
        success, stdout, stderr = run_command(f"xwd -root | convert xwd:- '{output_path}'")
    
    if success:
        return {"success": True, "path": output_path}
    else:
        return {"error": stderr}

def get_active_window():
    """获取当前活动窗口"""
    success, stdout, stderr = run_command("xdotool getactivewindow")
    
    if success:
        window_id = stdout.strip()
        # 获取窗口信息
        success2, title, stderr2 = run_command(f"xdotool getwindowname {window_id}")
        return {
            "success": True,
            "window_id": window_id,
            "title": title if success2 else "Unknown"
        }
    else:
        return {"error": stderr}

def list_windows():
    """列出所有窗口"""
    success, stdout, stderr = run_command("xdotool search --onlyvisible --name '.*' 2>/dev/null | head -20")
    
    if success:
        windows = []
        for window_id in stdout.strip().split('\n'):
            if window_id:
                success2, title, stderr2 = run_command(f"xdotool getwindowname {window_id}")
                windows.append({
                    "id": window_id,
                    "title": title if success2 else "Unknown"
                })
        return {"success": True, "windows": windows}
    else:
        return {"error": stderr}

def move_mouse(x, y):
    """移动鼠标到指定坐标"""
    success, stdout, stderr = run_command(f"xdotool mousemove {x} {y}")
    
    if success:
        return {"success": True}
    else:
        return {"error": stderr}

def click_mouse(button=1):
    """点击鼠标"""
    success, stdout, stderr = run_command(f"xdotool click {button}")
    
    if success:
        return {"success": True}
    else:
        return {"error": stderr}

def type_text(text):
    """输入文本"""
    success, stdout, stderr = run_command(f"xdotool type '{text}'")
    
    if success:
        return {"success": True}
    else:
        return {"error": stderr}

def key_press(key):
    """按键"""
    success, stdout, stderr = run_command(f"xdotool key {key}")
    
    if success:
        return {"success": True}
    else:
        return {"error": stderr}

def get_screen_info():
    """获取屏幕信息"""
    success, stdout, stderr = run_command("xdpyinfo | grep dimensions")
    
    if success:
        # 提取分辨率
        import re
        match = re.search(r'dimensions:\s+(\d+)x(\d+)', stdout)
        if match:
            width, height = match.groups()
            return {
                "success": True,
                "width": int(width),
                "height": int(height)
            }
    
    return {"error": stderr}

def main():
    if len(sys.argv) < 2:
        print("用法: linux-desktop <command> [args]")
        print("")
        print("命令:")
        print("  linux-desktop screenshot [路径]         截图全屏")
        print("  linux-desktop window [ID] [路径]       截图窗口")
        print("  linux-desktop active                   获取活动窗口")
        print("  linux-desktop list                     列出所有窗口")
        print("  linux-desktop move <x> <y>             移动鼠标")
        print("  linux-desktop click [按钮]             点击鼠标 (1=左键, 2=中键, 3=右键)")
        print("  linux-desktop type <文本>              输入文本")
        print("  linux-desktop key <按键>               按键 (如: Return, Escape, Ctrl+c)")
        print("  linux-desktop screen                   获取屏幕信息")
        print("")
        print("示例:")
        print("  linux-desktop screenshot ~/my.png")
        print("  linux-desktop window 0x12345678")
        print("  linux-desktop move 500 300")
        print("  linux-desktop click 1")
        print("  linux-desktop type 'Hello World'")
        print("  linux-desktop key Ctrl+a")
        print("  linux-desktop screen")
        return 1

    command = sys.argv[1]

    if command == "screenshot":
        output = sys.argv[2] if len(sys.argv) > 2 else None
        result = take_screenshot(output)
        
        if "error" in result:
            print(f"错误: {result['error']}")
            return 1
        else:
            print(f"✅ 截图已保存: {result['path']}")

    elif command == "window":
        window_id = sys.argv[2] if len(sys.argv) > 2 else None
        output = sys.argv[3] if len(sys.argv) > 3 else None
        result = take_window_screenshot(window_id, output)
        
        if "error" in result:
            print(f"错误: {result['error']}")
            return 1
        else:
            print(f"✅ 窗口截图已保存: {result['path']}")

    elif command == "active":
        result = get_active_window()
        
        if "error" in result:
            print(f"错误: {result['error']}")
            return 1
        else:
            print(f"🖥️  活动窗口")
            print(f"ID: {result['window_id']}")
            print(f"标题: {result['title']}")

    elif command == "list":
        result = list_windows()
        
        if "error" in result:
            print(f"错误: {result['error']}")
            return 1
        else:
            print(f"🪟 找到 {len(result['windows'])} 个窗口:\n")
            for i, win in enumerate(result['windows'], 1):
                title = win['title'][:50] + "..." if len(win['title']) > 50 else win['title']
                print(f"{i:2}. {win['id']} - {title}")

    elif command == "move":
        if len(sys.argv) < 4:
            print("错误: 请提供 x 和 y 坐标")
            return 1
        
        try:
            x = int(sys.argv[2])
            y = int(sys.argv[3])
        except ValueError:
            print("错误: 坐标必须是整数")
            return 1
        
        result = move_mouse(x, y)
        
        if "error" in result:
            print(f"错误: {result['error']}")
            return 1
        else:
            print(f"✅ 鼠标移动到 ({x}, {y})")

    elif command == "click":
        button = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        result = click_mouse(button)
        
        if "error" in result:
            print(f"错误: {result['error']}")
            return 1
        else:
            button_names = {1: "左键", 2: "中键", 3: "右键"}
            print(f"✅ 点击鼠标 {button_names.get(button, str(button))}")

    elif command == "type":
        if len(sys.argv) < 3:
            print("错误: 请提供要输入的文本")
            return 1
        
        text = sys.argv[2]
        result = type_text(text)
        
        if "error" in result:
            print(f"错误: {result['error']}")
            return 1
        else:
            print(f"✅ 已输入文本: '{text}'")

    elif command == "key":
        if len(sys.argv) < 3:
            print("错误: 请提供按键")
            return 1
        
        key = sys.argv[2]
        result = key_press(key)
        
        if "error" in result:
            print(f"错误: {result['error']}")
            return 1
        else:
            print(f"✅ 已按键: {key}")

    elif command == "screen":
        result = get_screen_info()
        
        if "error" in result:
            print(f"错误: {result['error']}")
            return 1
        else:
            print(f"🖥️  屏幕信息")
            print(f"分辨率: {result['width']}x{result['height']}")

    else:
        print(f"未知命令: {command}")
        print("使用 'linux-desktop' 查看帮助")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())

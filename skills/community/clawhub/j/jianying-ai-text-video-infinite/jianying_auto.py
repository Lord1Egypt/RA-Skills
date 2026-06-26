#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剪映AI文字成片自动化脚本 - 主程序
"""
import time
import json
import os
import sys
import subprocess

# 配置文件路径
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "jianying_coords.json")
SCRIPT_FILE = os.path.join(os.path.dirname(__file__), "script.txt")

def load_coords():
    """加载保存的坐标配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def load_script():
    """加载分镜脚本"""
    if os.path.exists(SCRIPT_FILE):
        with open(SCRIPT_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def ensure_pyautogui():
    """确保pyautogui已安装"""
    try:
        import pyautogui
        return pyautogui
    except ImportError:
        print("正在安装 pyautogui...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui", "-q"])
        import pyautogui
        return pyautogui

def click_at(pyautogui, coords, key, delay=0.5):
    """在指定坐标点击"""
    if key not in coords:
        print(f"错误: 未找到坐标 [{key}]")
        return False
    
    x, y = coords[key]["x"], coords[key]["y"]
    print(f"点击 [{key}]: ({x}, {y})")
    pyautogui.click(x, y)
    time.sleep(delay)
    return True

def open_jianying(pyautogui, coords):
    """打开剪映专业版"""
    print("\n=== 步骤1: 打开剪映专业版 ===")
    
    # 双击剪映图标
    x, y = coords["剪映图标"]["x"], coords["剪映图标"]["y"]
    print(f"双击剪映图标: ({x}, {y})")
    pyautogui.doubleClick(x, y)
    
    # 等待剪映加载
    print("等待剪映加载 (10秒)...")
    time.sleep(10)
    return True

def click_ai_text_to_video(pyautogui, coords):
    """点击AI文字成片入口"""
    print("\n=== 步骤2: 点击AI文字成片 ===")
    return click_at(pyautogui, coords, "AI文字成片入口", delay=3)

def input_script(pyautogui, coords, script_text):
    """输入分镜脚本"""
    print("\n=== 步骤3: 输入分镜脚本 ===")
    
    # 点击文本输入框
    if not click_at(pyautogui, coords, "文本输入框", delay=1):
        return False
    
    # 全选并删除原有内容
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')
    pyautogui.keyUp('ctrl')
    time.sleep(0.3)
    pyautogui.keyDown('delete')
    pyautogui.keyUp('delete')
    time.sleep(0.3)
    
    # 输入脚本内容
    print("正在输入脚本内容...")
    pyautogui.typewrite(script_text, interval=0.01)
    time.sleep(1)
    return True

def configure_video_settings(pyautogui, coords):
    """配置画面设置"""
    print("\n=== 步骤4: 配置画面设置 ===")
    
    # 点击画面页标签
    if not click_at(pyautogui, coords, "画面页标签", delay=1):
        return False
    
    # 选择素材 - 未来科幻
    print("选择素材: 未来科幻")
    if not click_at(pyautogui, coords, "素材选择_未来科幻", delay=1):
        return False
    
    # 选择分镜类型 - 一镜到底
    print("选择分镜类型: 一镜到底")
    if not click_at(pyautogui, coords, "分镜类型_一镜到底", delay=1):
        return False
    
    # 选择视频比例 - 9:16
    print("选择视频比例: 9:16")
    if not click_at(pyautogui, coords, "视频比例_9:16", delay=1):
        return False
    
    return True

def configure_voice_settings(pyautogui, coords):
    """配置配音设置"""
    print("\n=== 步骤5: 配置配音设置 ===")
    
    # 点击配音页标签
    if not click_at(pyautogui, coords, "配音页标签", delay=1):
        return False
    
    # 点击搜藏按钮
    if not click_at(pyautogui, coords, "搜藏按钮", delay=1):
        return False
    
    # 选择真人播客女
    print("选择配音: 真人播客女")
    if not click_at(pyautogui, coords, "真人播客女", delay=1):
        return False
    
    return True

def generate_video(pyautogui, coords):
    """点击生成视频"""
    print("\n=== 步骤6: 生成视频 ===")
    print("点击生成视频按钮...")
    return click_at(pyautogui, coords, "生成视频按钮", delay=1)

def main():
    print("=== 剪映AI文字成片自动化 ===\n")
    
    # 加载配置
    coords = load_coords()
    if not coords:
        print(f"错误: 未找到坐标配置文件")
        print(f"请先运行 setup_coords.py 配置坐标")
        sys.exit(1)
    
    script_text = load_script()
    if not script_text:
        print(f"错误: 未找到分镜脚本文件 {SCRIPT_FILE}")
        sys.exit(1)
    
    print(f"已加载 {len(coords)} 个坐标配置")
    print(f"脚本长度: {len(script_text)} 字符")
    
    # 确保pyautogui
    pyautogui = ensure_pyautogui()
    pyautogui.FAILSAFE = True  # 启用故障保护
    
    # 执行自动化流程
    try:
        # 打开剪映
        if not open_jianying(pyautogui, coords):
            print("打开剪映失败")
            return
        
        # 点击AI文字成片
        if not click_ai_text_to_video(pyautogui, coords):
            print("点击AI文字成片失败")
            return
        
        # 输入脚本
        if not input_script(pyautogui, coords, script_text):
            print("输入脚本失败")
            return
        
        # 配置画面
        if not configure_video_settings(pyautogui, coords):
            print("配置画面设置失败")
            return
        
        # 配置配音
        if not configure_voice_settings(pyautogui, coords):
            print("配置配音设置失败")
            return
        
        print("\n=== 配置完成 ===")
        print("请检查以下设置是否正确:")
        print("- 素材: 未来科幻")
        print("- 分镜类型: 一镜到底")
        print("- 视频比例: 9:16")
        print("- 配音: 真人播客女")
        print("\n确认无误后，我将点击生成视频按钮")
        
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()

def generate():
    """执行生成视频（在确认配置正确后调用）"""
    coords = load_coords()
    pyautogui = ensure_pyautogui()
    pyautogui.FAILSAFE = True
    
    print("\n正在点击生成视频按钮...")
    generate_video(pyautogui, coords)
    print("生成视频已启动！")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--generate":
        generate()
    else:
        main()

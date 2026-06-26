#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剪映AI文字成片自动化脚本
"""
import time
import json
import os

# 配置文件路径
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "jianying_coords.json")

def load_coords():
    """加载保存的坐标配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_coords(coords):
    """保存坐标配置"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(coords, f, indent=2, ensure_ascii=False)

def get_mouse_position():
    """获取当前鼠标位置"""
    try:
        import pyautogui
        return pyautogui.position()
    except ImportError:
        print("请先安装 pyautogui: pip install pyautogui")
        return None

def wait_for_position(prompt):
    """等待用户将鼠标放到指定位置并返回坐标"""
    print(f"\n>>> {prompt}")
    print("请将鼠标放到目标位置，3秒后将记录坐标...")
    time.sleep(3)
    pos = get_mouse_position()
    if pos:
        print(f"已记录坐标: ({pos.x}, {pos.y})")
        return {"x": pos.x, "y": pos.y}
    return None

def main():
    coords = load_coords()
    print("=== 剪映AI文字成片坐标配置 ===\n")
    
    # 需要配置的坐标点
    required_coords = [
        ("剪映图标", "桌面上剪映专业版快捷方式的中心位置"),
        ("AI文字成片入口", "剪映首页的AI文字成片按钮位置"),
        ("文本输入框", "左侧文本输入区域的点击位置"),
        ("画面页标签", "右侧画面页标签位置"),
        ("素材选择_未来科幻", "素材选择下拉框或未来科幻选项位置"),
        ("分镜类型_一镜到底", "分镜类型选择位置"),
        ("视频比例_9:16", "视频比例9:16选项位置"),
        ("配音页标签", "右侧配音页标签位置"),
        ("搜藏按钮", "配音页的搜藏按钮位置"),
        ("真人播客女", "真人播客女配音选项位置"),
        ("生成视频按钮", "生成视频按钮位置"),
    ]
    
    for key, desc in required_coords:
        if key not in coords:
            coords[key] = wait_for_position(f"配置 [{key}]: {desc}")
            if coords[key]:
                save_coords(coords)
        else:
            print(f"[{key}] 已配置: {coords[key]}")
    
    print("\n=== 坐标配置完成 ===")
    print(f"配置已保存到: {CONFIG_FILE}")

if __name__ == "__main__":
    main()

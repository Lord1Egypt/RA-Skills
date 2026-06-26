#!/usr/bin/env python3
"""
macOS 桌面控制 - 图像识别功能
使用 OpenCV 进行屏幕图像识别和定位
"""

import sys
import subprocess
import tempfile
import os

# 检查依赖
try:
    import cv2
    import numpy as np
    import pyautogui
except ImportError as e:
    print(f"❌ 导入失败：{e}")
    print("")
    print("请安装依赖：")
    print("  pip3 install --user --break-system-packages opencv-python-headless numpy pyautogui")
    sys.exit(1)

def show_help():
    """显示帮助"""
    print("macOS 图像识别工具")
    print("")
    print("用法：python3 image_recognition.py [命令] [参数]")
    print("")
    print("命令:")
    print("  find IMAGE_PATH      在屏幕上查找图像")
    print("  click IMAGE_PATH     找到图像并点击")
    print("  wait IMAGE_PATH [N]  等待图像出现（最多 N 秒）")
    print("  screenshot REGION    截取指定区域")
    print("")
    print("示例:")
    print("  python3 image_recognition.py find button.png")
    print("  python3 image_recognition.py click submit.png")
    print("  python3 image_recognition.py wait loading.png 10")

def find_image(image_path, confidence=0.8):
    """在屏幕上查找图像"""
    if not os.path.exists(image_path):
        print(f"❌ 图像文件不存在：{image_path}")
        return None
    
    # 截取全屏
    screenshot = pyautogui.screenshot()
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # 读取模板图像
    template = cv2.imread(image_path)
    if template is None:
        print(f"❌ 无法读取图像：{image_path}")
        return None
    
    # 模板匹配
    result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val >= confidence:
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        print(f"✅ 找到图像！")
        print(f"   位置：({center_x}, {center_y})")
        print(f"   尺寸：{w}x{h}")
        print(f"   置信度：{max_val:.2%}")
        return (center_x, center_y, w, h)
    else:
        print(f"❌ 未找到图像（置信度：{max_val:.2%} < {confidence:.2%}）")
        return None

def click_image(image_path, confidence=0.8):
    """找到图像并点击"""
    location = find_image(image_path, confidence)
    if location:
        x, y, w, h = location
        print(f"🖱️  点击位置：({x}, {y})")
        pyautogui.click(x, y)
        print("✅ 点击完成")
        return True
    return False

def wait_for_image(image_path, timeout=10, confidence=0.8):
    """等待图像出现"""
    import time
    
    print(f"⏳ 等待图像出现（最多 {timeout} 秒）...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        location = find_image(image_path, confidence)
        if location:
            elapsed = time.time() - start_time
            print(f"✅ 图像出现！耗时：{elapsed:.1f}秒")
            return True
        time.sleep(0.5)
    
    print(f"❌ 等待超时（{timeout}秒）")
    return False

def screenshot_region(x, y, width, height, output=None):
    """截取指定区域"""
    if output is None:
        output = f"screenshot_region_{x}_{y}_{width}_{height}.png"
    
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(output)
    print(f"✅ 区域截图已保存：{output}")
    print(f"   位置：({x}, {y})")
    print(f"   尺寸：{width}x{height}")
    return output

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "find":
        if len(sys.argv) < 3:
            print("❌ 请提供图像路径")
            return
        find_image(sys.argv[2])
    
    elif command == "click":
        if len(sys.argv) < 3:
            print("❌ 请提供图像路径")
            return
        click_image(sys.argv[2])
    
    elif command == "wait":
        if len(sys.argv) < 3:
            print("❌ 请提供图像路径")
            return
        timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        wait_for_image(sys.argv[2], timeout)
    
    elif command == "screenshot":
        if len(sys.argv) < 5:
            print("❌ 请提供坐标和尺寸：x y width height")
            return
        x = int(sys.argv[2])
        y = int(sys.argv[3])
        width = int(sys.argv[4])
        height = int(sys.argv[5]) if len(sys.argv) > 5 else width
        output = sys.argv[6] if len(sys.argv) > 6 else None
        screenshot_region(x, y, width, height, output)
    
    else:
        print(f"❌ 未知命令：{command}")
        show_help()

if __name__ == "__main__":
    main()

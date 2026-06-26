#!/usr/bin/env python3
"""
手机 Agent 控制脚本 v2.0
提供简洁的接口操控安卓手机

用法:
    agent.py connected          # 检查连接状态
    agent.py screenshot       # 获取截图，返回路径
    agent.py uidump           # 获取 UI 结构，返回路径
    agent.py tap <x> <y>     # 点击坐标
    agent.py swipe <x1> <y1> <x2> <y2> [duration]  # 滑动
    agent.py text <文字>      # 输入文字（仅英文/数字）
    agent.py home             # HOME 键
    agent.py back             # 返回键
    agent.py power            # 电源键
    agent.py start <包名>     # 启动 App
    agent.py stop <包名>      # 停止 App
    agent.py search <关键词>  # 在当前界面搜索元素
    agent.py click <关键词>   # 点击包含关键词的元素
    agent.py size             # 获取屏幕尺寸
"""

import subprocess
import os
import sys
import tempfile
import time
import re
import xml.etree.ElementTree as ET

# 默认设备 ID（留空则自动检测）
DEVICE_ID = ""

def find_device():
    """自动查找已连接的设备"""
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')[1:]
    for line in lines:
        if 'device' in line and not 'unauthorized' in line:
            device = line.split()[0]
            return device
    return None

def adb(args, binary=False, retry=3):
    """执行 ADB 命令，自动重试"""
    global DEVICE_ID
    
    # 自动查找设备
    if not DEVICE_ID or not is_device_connected():
        found = find_device()
        if found:
            DEVICE_ID = found
        else:
            return None, "Device not found", 1
    
    cmd = ['adb']
    if DEVICE_ID:
        cmd.extend(['-s', DEVICE_ID])
    cmd.extend(args)
    
    for attempt in range(retry):
        try:
            if binary:
                result = subprocess.run(cmd, capture_output=True, timeout=30)
                return result.stdout, b'', result.returncode
            else:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            if attempt < retry - 1:
                time.sleep(1)
                continue
            return None, "Timeout", 1
        except Exception as e:
            if attempt < retry - 1:
                time.sleep(1)
                continue
            return None, str(e), 1
    
    return None, "Failed after retries", 1

def is_device_connected():
    """检查设备是否连接"""
    out, _, _ = adb(['devices'])
    if not out:
        return False
    return DEVICE_ID in out and 'device' in out.split(DEVICE_ID)[1].split('\n')[0]

def get_screenshot(save_path=None):
    """获取截图，返回图片路径"""
    if not save_path:
        save_path = tempfile.mktemp(suffix='.png')
    out, _, code = adb(['exec-out', 'screencap', '-p'], binary=True)
    if code == 0 and out:
        with open(save_path, 'wb') as f:
            f.write(out)
        return save_path
    return None

def get_uidump(save_path=None):
    """获取 UI 结构 XML"""
    if not save_path:
        save_path = tempfile.mktemp(suffix='.xml')
    _, _, code = adb(['exec-out', 'uiautomator', 'dump', '/sdcard/dump.xml'])
    if code != 0:
        return None
    _, _, code = adb(['pull', '/sdcard/dump.xml', save_path])
    if code == 0 and os.path.exists(save_path):
        return save_path
    return None

def get_screen_size():
    """获取屏幕尺寸"""
    out, _, _ = adb(['shell', 'wm', 'size'])
    try:
        size_str = out.strip().split(':')[-1].strip()
        width, height = map(int, size_str.split('x'))
        return width, height
    except:
        return 1200, 2670

def tap(x, y):
    """点击坐标"""
    _, _, code = adb(['shell', 'input', 'tap', str(x), str(y)])
    return code == 0

def swipe(x1, y1, x2, y2, duration=300):
    """滑动"""
    _, _, code = adb(['shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y2), str(duration)])
    return code == 0

def input_text(text):
    """输入文字（仅英文/数字）"""
    # 替换空格为 %s（部分输入法支持）
    text = text.replace(' ', '%s')
    _, _, code = adb(['shell', 'input', 'text', text])
    return code == 0

def press_key(keycode):
    """按键"""
    _, _, code = adb(['shell', 'input', 'keyevent', str(keycode)])
    return code == 0

def press_home():
    return press_key(3)

def press_back():
    return press_key(4)

def press_power():
    return press_key(26)

def start_app(package):
    """启动应用"""
    _, _, code = adb(['shell', 'monkey', '-p', package, '-c', 'android.intent.category.LAUNCHER', '1'])
    time.sleep(3)
    return code == 0

def stop_app(package):
    """停止应用"""
    _, _, code = adb(['shell', 'am', 'force-stop', package])
    time.sleep(1)
    return code == 0

def find_element_by_text(xml_path, keyword):
    """在 UI XML 中查找包含关键词的元素，返回坐标"""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        for node in root.iter():
            text = node.attrib.get('text', '')
            bounds = node.attrib.get('bounds', '')
            clickable = node.attrib.get('clickable', '')
            
            if keyword.lower() in text.lower() or keyword in text:
                # 解析 bounds: "[x1,y1][x2,y2]"
                coords = re.findall(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
                if coords:
                    x1, y1, x2, y2 = map(int, coords[0])
                    return {
                        'text': text,
                        'bounds': bounds,
                        'clickable': clickable == 'true',
                        'x': (x1 + x2) // 2,
                        'y': (y1 + y2) // 2
                    }
    except Exception as e:
        print(f"Parse error: {e}")
    return None

def find_element_by_id(xml_path, id_keyword):
    """在 UI XML 中查找包含关键词的资源 ID"""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        for node in root.iter():
            resource_id = node.attrib.get('resource-id', '')
            text = node.attrib.get('text', '')
            bounds = node.attrib.get('bounds', '')
            clickable = node.attrib.get('clickable', '')
            
            if id_keyword.lower() in resource_id.lower():
                coords = re.findall(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
                if coords:
                    x1, y1, x2, y2 = map(int, coords[0])
                    return {
                        'text': text,
                        'resource_id': resource_id,
                        'bounds': bounds,
                        'clickable': clickable == 'true',
                        'x': (x1 + x2) // 2,
                        'y': (y1 + y2) // 2
                    }
    except Exception as e:
        print(f"Parse error: {e}")
    return None

def click(keyword):
    """根据关键词自动查找并点击元素"""
    xml_path = get_uidump()
    if not xml_path:
        return False
    
    # 先按文本查找
    elem = find_element_by_text(xml_path, keyword)
    if elem:
        print(f"Found '{keyword}': {elem['text']} at ({elem['x']}, {elem['y']})")
        return tap(elem['x'], elem['y'])
    
    # 再按 ID 查找
    elem = find_element_by_id(xml_path, keyword)
    if elem:
        print(f"Found by ID '{keyword}': {elem['resource_id']} at ({elem['x']}, {elem['y']})")
        return tap(elem['x'], elem['y'])
    
    print(f"Element '{keyword}' not found")
    return False

def search(keyword):
    """搜索并显示包含关键词的元素"""
    xml_path = get_uidump()
    if not xml_path:
        print("Failed to get UI dump")
        return
    
    found = []
    
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        for node in root.iter():
            text = node.attrib.get('text', '')
            content_desc = node.attrib.get('content-desc', '')
            bounds = node.attrib.get('bounds', '')
            resource_id = node.attrib.get('resource-id', '')
            
            if keyword.lower() in text.lower() or keyword.lower() in content_desc.lower():
                coords = re.findall(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
                if coords:
                    x1, y1, x2, y2 = map(int, coords[0])
                    found.append({
                        'text': text,
                        'content_desc': content_desc,
                        'resource_id': resource_id,
                        'x': (x1 + x2) // 2,
                        'y': (y1 + y2) // 2,
                        'bounds': bounds
                    })
    except Exception as e:
        print(f"Parse error: {e}")
        return
    
    if found:
        print(f"Found {len(found)} element(s):")
        for i, elem in enumerate(found[:10], 1):
            print(f"  {i}. text='{elem['text']}' desc='{elem['content_desc']}' at ({elem['x']}, {elem['y']}) bounds={elem['bounds']}")
            print(f"     ID: {elem['resource_id']}")
    else:
        print(f"No elements found matching '{keyword}'")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'connected':
        if is_device_connected():
            print(f"YES (device: {DEVICE_ID})")
        else:
            print("NO")
    
    elif cmd == 'screenshot':
        path = get_screenshot()
        if path:
            print(path)
        else:
            print("FAIL")
    
    elif cmd == 'uidump':
        path = get_uidump()
        if path:
            print(path)
        else:
            print("FAIL")
    
    elif cmd == 'size':
        w, h = get_screen_size()
        print(f"{w}x{h}")
    
    elif cmd == 'tap' and len(sys.argv) >= 4:
        x, y = int(sys.argv[2]), int(sys.argv[3])
        print("OK" if tap(x, y) else "FAIL")
    
    elif cmd == 'swipe' and len(sys.argv) >= 6:
        x1, y1, x2, y2 = map(int, sys.argv[2:6])
        duration = int(sys.argv[6]) if len(sys.argv) >= 7 else 300
        print("OK" if swipe(x1, y1, x2, y2, duration) else "FAIL")
    
    elif cmd == 'text' and len(sys.argv) >= 3:
        print("OK" if input_text(sys.argv[2]) else "FAIL")
    
    elif cmd == 'home':
        print("OK" if press_home() else "FAIL")
    
    elif cmd == 'back':
        print("OK" if press_back() else "FAIL")
    
    elif cmd == 'power':
        print("OK" if press_power() else "FAIL")
    
    elif cmd == 'start' and len(sys.argv) >= 3:
        print("OK" if start_app(sys.argv[2]) else "FAIL")
    
    elif cmd == 'stop' and len(sys.argv) >= 3:
        print("OK" if stop_app(sys.argv[2]) else "FAIL")
    
    elif cmd == 'search' and len(sys.argv) >= 3:
        search(sys.argv[2])
    
    elif cmd == 'click' and len(sys.argv) >= 3:
        print("OK" if click(sys.argv[2]) else "FAIL")
    
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)

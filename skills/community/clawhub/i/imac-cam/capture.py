#!/usr/bin/env python3
"""iMac 摄像头截图技能 - 精确裁剪摄像头画面"""
import subprocess
import os
import time

CAPTURE_FILE = "/tmp/cam_capture.png"

# Photo Booth 窗口参数
TOP_BAR = 28   # 上边框高度
BOTTOM_BAR = 60  # 下边框高度

def is_photo_booth_running():
    """检查 Photo Booth 是否正在运行"""
    result = subprocess.run(
        ['osascript', '-e', 'tell application "System Events" to name of processes whose background only is false'],
        capture_output=True, text=True
    )
    return 'Photo Booth' in result.stdout

def get_photo_booth_window_rect():
    """动态获取 Photo Booth 窗口位置"""
    # 使用不同的方法获取，避免逗号解析问题
    script = '''\
set winPos to {0, 0}
set winSize to {0, 0}
tell application "Photo Booth"
    activate
    delay 0.5
end tell
tell application "System Events"
    tell process "Photo Booth"
        set winPos to position of first window
        set winSize to size of first window
    end tell
end tell
set x to item 1 of winPos
set y to item 2 of winPos
set w to item 1 of winSize
set h to item 2 of winSize
return x & "," & y & "," & w & "," & h
'''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    output = result.stdout.strip()
    print(f"Raw output: {output}")
    
    # 解析输出
    try:
        # 分割并过滤空字符串
        parts = [p.strip() for p in output.split(',') if p.strip()]
        if len(parts) >= 4:
            win_x = int(parts[0])
            win_y = int(parts[1])
            win_w = int(parts[2])
            win_h = int(parts[3])
            
            # 裁剪掉上下边框
            screen_rect = f"{win_x},{win_y + TOP_BAR},{win_w},{win_h - TOP_BAR - BOTTOM_BAR}"
            print(f"窗口: {win_x},{win_y},{win_w},{win_h} -> 捕获: {screen_rect}")
            return screen_rect
    except Exception as e:
        print(f"解析错误: {e}")
    
    return None

def is_screen_black(filepath):
    """检查截图是否几乎是黑的"""
    if not os.path.exists(filepath):
        return True
    size = os.path.getsize(filepath)
    if size < 30000:
        return True
    return False

def capture_photo(max_retries=6):
    """捕获 Photo Booth 摄像头画面"""
    # 确保 Photo Booth 启动
    if not is_photo_booth_running():
        print("启动 Photo Booth...")
        subprocess.run(['osascript', '-e', 'tell application "Photo Booth" to activate'], capture_output=True)
        time.sleep(2)
    
    for attempt in range(max_retries):
        # 每次都重新获取窗口位置
        rect = get_photo_booth_window_rect()
        
        if not rect:
            print(f"尝试 {attempt + 1}: 获取窗口失败，重试...")
            time.sleep(0.5)
            continue
        
        # 确保窗口在前
        subprocess.run([
            'osascript', '-e',
            '''tell application "System Events"
                set frontmost of process "Photo Booth" to true
            end tell'''
        ], capture_output=True)
        time.sleep(0.2)
        
        # 截取
        subprocess.run([
            '/usr/sbin/screencapture', 
            '-x', 
            '-R' + rect, 
            CAPTURE_FILE
        ], capture_output=True)
        
        if not is_screen_black(CAPTURE_FILE):
            size = os.path.getsize(CAPTURE_FILE)
            print(f"✓ 摄像头已捕获 (尝试 {attempt + 1}): {size} bytes")
            return True
        
        print(f"尝试 {attempt + 1}: 画面较暗，重试...")
        time.sleep(0.5)
    
    print(f"最终捕获: {os.path.getsize(CAPTURE_FILE)} bytes")
    return os.path.exists(CAPTURE_FILE)

def get_ip():
    """获取本机 IP"""
    result = subprocess.run(['/usr/sbin/scutil', '--nwi'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'address' in line and '2408' not in line:
            parts = line.strip().split()
            if parts:
                return parts[-1]
    return "192.168.3.210"

def main():
    # 启动 HTTP 服务器
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8765))
        sock.close()
        if result != 0:
            os.chdir('/tmp')
            subprocess.Popen(['python3', '-m', 'http.server', '8765'], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1)
    except:
        pass
    
    if capture_photo():
        ip = get_ip()
        print(f"查看地址: http://{ip}:8765/cam_capture.png")
        
        # 截图完成后关闭 Photo Booth
        print("关闭 Photo Booth...")
        subprocess.run(['osascript', '-e', 'tell application "Photo Booth" to quit'], capture_output=True)
    else:
        print("捕获失败")

if __name__ == "__main__":
    main()

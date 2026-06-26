# -*- coding: utf-8 -*-
import pyautogui
import time
import subprocess
import os
import json
import ctypes

# Ensure pyautogui safety
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

skill_dir = r'C:\Users\admin\.qclaw\workspace\skills\jianying-ai-text-video-infinite'
coords_path = os.path.join(skill_dir, 'jianying_coords.json')
with open(coords_path, 'r', encoding='utf-8') as f:
    coords = json.load(f)

script_path = os.path.join(skill_dir, 'script.txt')
with open(script_path, 'r', encoding='utf-8') as f:
    script_text = f.read()

print(f"Loaded {len(coords)} coordinates, script: {len(script_text)} chars")

# Use ctypes to activate 剪映 window
import win32gui
import win32con

def find_and_activate_jianying():
    """Find and activate JianyingPro window"""
    result = []
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if 'JianyingPro' in title or 'jianying' in title.lower():
                result.append(hwnd)
    win32gui.EnumWindows(callback, None)
    
    if result:
        hwnd = result[0]
        # Restore if minimized
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.5)
        # Bring to front
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)
        title = win32gui.GetWindowText(hwnd)
        print(f"Activated window: {title} (hwnd={hwnd})")
        return True
    else:
        print("ERROR: JianyingPro window not found!")
        return False

# Step 0: Activate JianyingPro
print("\n=== Step 0: Activate JianyingPro ===")
if not find_and_activate_jianying():
    print("Cannot continue without JianyingPro window")
    exit(1)

time.sleep(2)

# Verify it's in foreground
fg = win32gui.GetForegroundWindow()
fg_title = win32gui.GetWindowText(fg)
print(f"Foreground window: {fg_title}")

# Step 1: Click AI文字成片 entry
print("\n=== Step 1: Click AI文字成片 ===")
x, y = coords["AI文字成片入口"]["x"], coords["AI文字成片入口"]["y"]
print(f"Clicking at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(6)  # Wait for page load

# Step 2: Input script text via clipboard
print("\n=== Step 2: Input script text ===")

# Re-activate just in case
find_and_activate_jianying()
time.sleep(1)

x, y = coords["文本输入框"]["x"], coords["文本输入框"]["y"]
print(f"Click text input at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(1)

# Select all and delete
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.5)
pyautogui.press('delete')
time.sleep(0.5)

# Set clipboard via PowerShell
tmp_path = os.path.join(skill_dir, 'temp_script.txt')
with open(tmp_path, 'w', encoding='utf-8') as f:
    f.write(script_text)

ps_cmd = f'Get-Content -Path "{tmp_path}" -Encoding UTF8 -Raw | Set-Clipboard'
result = subprocess.run(['powershell', '-Command', ps_cmd], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(f"Clipboard set: return code {result.returncode}")

# Paste
time.sleep(0.5)
pyautogui.hotkey('ctrl', 'v')
time.sleep(3)

# Clean up
try:
    os.remove(tmp_path)
except:
    pass
print("Text pasted!")

# Step 3: Configure video settings
print("\n=== Step 3: Configure video settings ===")

find_and_activate_jianying()
time.sleep(0.5)

# Click 画面 tab
x, y = coords["画面页标签"]["x"], coords["画面页标签"]["y"]
print(f"Click 画面 tab at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(2)

# Select 未来科幻
x, y = coords["素材选择_未来科幻"]["x"], coords["素材选择_未来科幻"]["y"]
print(f"Click 未来科幻 at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(1)

# Click 分镜类型 dropdown
x, y = coords["分镜类型下拉框"]["x"], coords["分镜类型下拉框"]["y"]
print(f"Click 分镜类型 dropdown at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(1)

# Select 一镜到底
x, y = coords["分镜类型_一镜到底"]["x"], coords["分镜类型_一镜到底"]["y"]
print(f"Click 一镜到底 at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(1)

# Click 视频比例 dropdown
x, y = coords["视频比例下拉框"]["x"], coords["视频比例下拉框"]["y"]
print(f"Click 视频比例 dropdown at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(1)

# Select 9:16
x, y = coords["视频比例_9:16"]["x"], coords["视频比例_9:16"]["y"]
print(f"Click 9:16 at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(1)

# Step 4: Configure voice settings
print("\n=== Step 4: Configure voice settings ===")

find_and_activate_jianying()
time.sleep(0.5)

# Click 配音 tab
x, y = coords["配音页标签"]["x"], coords["配音页标签"]["y"]
print(f"Click 配音 tab at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(2)

# Click 搜藏 button
x, y = coords["搜藏按钮"]["x"], coords["搜藏按钮"]["y"]
print(f"Click 搜藏 at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(1)

# Select 真人播客女
x, y = coords["真人播客女"]["x"], coords["真人播客女"]["y"]
print(f"Click 真人播客女 at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(1)

# Take final screenshot for verification
screenshot = pyautogui.screenshot()
screenshot.save(os.path.join(skill_dir, 'final_state.png'))
print("\nFinal screenshot saved!")

print("\n=== Configuration complete! ===")
print("Please verify on screen:")
print("- Text input: narration script")
print("- 素材: 未来科幻")
print("- 分镜类型: 一镜到底")  
print("- 视频比例: 9:16")
print("- 配音: 真人播客女")

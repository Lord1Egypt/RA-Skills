# -*- coding: utf-8 -*-
import pyautogui
import time
import subprocess
import os
import json

# Load coordinates
coords_path = os.path.join(os.path.dirname(__file__), 'jianying_coords.json')
with open(coords_path, 'r', encoding='utf-8') as f:
    coords = json.load(f)

# Load script
script_path = os.path.join(os.path.dirname(__file__), 'script.txt')
with open(script_path, 'r', encoding='utf-8') as f:
    script_text = f.read()

print(f"Loaded {len(coords)} coordinates")
print(f"Script length: {len(script_text)} chars")
print(f"Screen size: {pyautogui.size()}")

# Step 1: Click AI文字成片 entry
print("\n=== Step 1: Click AI文字成片 ===")
x, y = coords["AI文字成片入口"]["x"], coords["AI文字成片入口"]["y"]
print(f"Clicking at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(3)

# Step 2: Input script text via clipboard
print("\n=== Step 2: Input script text ===")
x, y = coords["文本输入框"]["x"], coords["文本输入框"]["y"]
print(f"Click text input at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(1)

# Select all and delete
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.3)
pyautogui.press('delete')
time.sleep(0.3)

# Write to temp file and set clipboard
tmp_path = os.path.join(os.path.dirname(__file__), 'temp_script.txt')
with open(tmp_path, 'w', encoding='utf-8') as f:
    f.write(script_text)

ps_cmd = f'Get-Content -Path "{tmp_path}" -Encoding UTF8 -Raw | Set-Clipboard'
result = subprocess.run(['powershell', '-Command', ps_cmd], capture_output=True, text=True)
print(f"Clipboard set: return code {result.returncode}")

# Paste
time.sleep(0.5)
pyautogui.hotkey('ctrl', 'v')
time.sleep(2)

# Clean up
os.remove(tmp_path)
print("Text pasted!")

# Step 3: Configure video settings
print("\n=== Step 3: Configure video settings ===")

# Click 画面 tab
x, y = coords["画面页标签"]["x"], coords["画面页标签"]["y"]
print(f"Click 画面 tab at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(1)

# Select 未来科幻
x, y = coords["素材选择_未来科幻"]["x"], coords["素材选择_未来科幻"]["y"]
print(f"Click 未来科幻 at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(1)

# Select 一镜到底 - first click dropdown
x, y = coords["分镜类型下拉框"]["x"], coords["分镜类型下拉框"]["y"]
print(f"Click 分镜类型 dropdown at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(1)

# Then select 一镜到底
x, y = coords["分镜类型_一镜到底"]["x"], coords["分镜类型_一镜到底"]["y"]
print(f"Click 一镜到底 at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(1)

# Select 9:16 - first click dropdown
x, y = coords["视频比例下拉框"]["x"], coords["视频比例下拉框"]["y"]
print(f"Click 视频比例 dropdown at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(1)

# Then select 9:16
x, y = coords["视频比例_9:16"]["x"], coords["视频比例_9:16"]["y"]
print(f"Click 9:16 at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(1)

# Step 4: Configure voice settings
print("\n=== Step 4: Configure voice settings ===")

# Click 配音 tab
x, y = coords["配音页标签"]["x"], coords["配音页标签"]["y"]
print(f"Click 配音 tab at ({x}, {y})")
pyautogui.click(x, y)
time.sleep(1)

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

print("\n=== Configuration complete! ===")
print("Settings applied:")
print("- 素材: 未来科幻")
print("- 分镜类型: 一镜到底")
print("- 视频比例: 9:16")
print("- 配音: 真人播客女")
print("\nWaiting for user confirmation to generate video...")

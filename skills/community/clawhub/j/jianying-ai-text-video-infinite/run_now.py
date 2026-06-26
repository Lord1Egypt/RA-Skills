# -*- coding: utf-8 -*-
import pyautogui
import time
import subprocess
import os
import json
import win32gui
import win32con

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

skill_dir = r'C:\Users\admin\.qclaw\workspace\skills\jianying-ai-text-video-infinite'
coords_path = os.path.join(skill_dir, 'jianying_coords.json')
with open(coords_path, 'r', encoding='utf-8') as f:
    coords = json.load(f)

script_path = os.path.join(skill_dir, 'script.txt')
with open(script_path, 'r', encoding='utf-8') as f:
    script_text = f.read()

# Get HWND from PowerShell
r = subprocess.run(['powershell', '-Command',
    '(Get-Process JianyingPro -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 }).MainWindowHandle'],
    capture_output=True, text=True)
MAIN_HWND = int(r.stdout.strip())
print(f"HWND={MAIN_HWND}, script={len(script_text)} chars")

# 只在开头激活一次
win32gui.ShowWindow(MAIN_HWND, win32con.SW_RESTORE)
time.sleep(0.5)
win32gui.SetForegroundWindow(MAIN_HWND)
time.sleep(2)
print("窗口已激活，后续不再重复激活")

def click(name, wait=1):
    x, y = coords[name]["x"], coords[name]["y"]
    pyautogui.click(x, y)
    time.sleep(wait)
    print(f"  {name} ({x},{y})")

# Step 1: AI文字成片
print("\n1: AI文字成片")
click("AI文字成片入口", wait=8)

# Step 2: 输入文本
print("\n2: 输入文本")
click("文本输入框", wait=1)
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.5)
pyautogui.press('delete')
time.sleep(0.5)

tmp = os.path.join(skill_dir, 'temp_script.txt')
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(script_text)
subprocess.run(['powershell', '-Command', f'Get-Content -Path "{tmp}" -Encoding UTF8 -Raw | Set-Clipboard'], capture_output=True)
time.sleep(0.5)
pyautogui.hotkey('ctrl', 'v')
time.sleep(3)
try: os.remove(tmp)
except: pass
print("  文本已粘贴")

# Step 3: 画面设置
print("\n3: 画面设置")
click("画面页标签", wait=2)
click("素材选择_未来科幻", wait=2)  # 等待2秒确保素材加载完成

# ⚠️ 素材选择后直接滚动（点击素材已自动激活滚动条）
pyautogui.press('end')  # 直接滚动到底部
time.sleep(1)

click("分镜类型下拉框", wait=1)
click("分镜类型_一镜到底", wait=1)

# 视频比例下拉框不需要再次滚动
click("视频比例下拉框", wait=1)
click("视频比例_9:16", wait=1)

# Step 4: 配音设置
print("\n4: 配音设置")
click("配音页标签", wait=2)
click("搜藏按钮", wait=1)
click("真人播客女", wait=1)

pyautogui.screenshot().save(os.path.join(skill_dir, 'final_state.png'))
print("\n配置完成，请检查屏幕：")
print("- 素材: 未来科幻 | 分镜: 一镜到底 | 比例: 9:16 | 配音: 真人播客女")
print('确认无误后回复"正确"，我点生成视频。')
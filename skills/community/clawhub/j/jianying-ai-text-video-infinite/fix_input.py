import time
import pyautogui
import subprocess
import os

# 读取脚本内容
with open('script.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 先点击文本输入框
print('点击文本输入框...')
pyautogui.click(311, 118)
time.sleep(1)

# 全选
print('全选内容...')
pyautogui.keyDown('ctrl')
pyautogui.keyDown('a')
pyautogui.keyUp('a')
pyautogui.keyUp('ctrl')
time.sleep(0.5)

# 删除
print('删除内容...')
pyautogui.keyDown('delete')
pyautogui.keyUp('delete')
time.sleep(0.5)

# 将内容写入临时文件
tmp_path = os.path.join(os.getcwd(), 'temp_script.txt')
with open(tmp_path, 'w', encoding='utf-8') as f:
    f.write(content)

# 使用powershell设置剪贴板
print('设置剪贴板...')
ps_cmd = f'Get-Content -Path "{tmp_path}" -Encoding UTF8 -Raw | Set-Clipboard'
result = subprocess.run(['powershell', '-Command', ps_cmd], capture_output=True, text=True)
print(f'PowerShell返回码: {result.returncode}')

# 粘贴
print('粘贴...')
pyautogui.keyDown('ctrl')
pyautogui.keyDown('v')
pyautogui.keyUp('v')
pyautogui.keyUp('ctrl')
time.sleep(1)

print('完成！')
os.remove(tmp_path)

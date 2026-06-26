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
time.sleep(0.5)

# 全选并删除
print('全选并删除原有内容...')
pyautogui.keyDown('ctrl')
pyautogui.keyDown('a')
pyautogui.keyUp('a')
pyautogui.keyUp('ctrl')
time.sleep(0.3)
pyautogui.keyDown('delete')
pyautogui.keyUp('delete')
time.sleep(0.3)

# 将内容写入临时文件
import tempfile
tmp_path = os.path.join(os.getcwd(), 'temp_script.txt')
with open(tmp_path, 'w', encoding='utf-8') as f:
    f.write(content)

# 使用powershell设置剪贴板
print('设置剪贴板内容...')
ps_cmd = f'Get-Content -Path "{tmp_path}" -Encoding UTF8 -Raw | Set-Clipboard'
result = subprocess.run(['powershell', '-Command', ps_cmd], capture_output=True, text=True)
if result.returncode != 0:
    print(f'PowerShell错误: {result.stderr}')

# 粘贴
time.sleep(0.5)
print('粘贴内容...')
pyautogui.keyDown('ctrl')
pyautogui.keyDown('v')
pyautogui.keyUp('v')
pyautogui.keyUp('ctrl')
time.sleep(0.5)

print('内容已粘贴完成！')

# 清理临时文件
os.remove(tmp_path)

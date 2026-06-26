---
name:jianying-ai-text-video-infinite
description: 自动化剪映电脑客户端的文字成片功能。使用场景：(1) 用户说"AI文字成片"、"剪映AI文字成片"、"用剪映生成视频"；(2) 用户需要将分镜脚本转换为视频；(3) 用户提到剪映、剪映专业版。注意：此技能操作的是电脑上安装的剪映桌面软件，不是剪映网页版。配置画面素材为未来科幻、分镜类型为一镜到底、视频比例为9:16、配音为真人播客女。
---

# 剪映文字成片自动化

此技能用于自动化剪映电脑客户端的AI文字成片功能，将分镜脚本转换为视频。

# 示例调用

```
AI文字成片。分镜脚本：分镜脚本
```

## 核心原则

**迭代优化原则**：在完成任务的过程中，每成功操作一次，就总结方法并修改到本技能文件中。

## 触发场景

用户说：
- "AI文字成片"
- "剪映AI文字成片"
- "用剪映生成视频"

## 重要说明

⚠️ **此技能操作的是电脑上安装的剪映桌面软件，不是剪映网页版。**
⚠️ **本技能能独立完成任务，无需依赖其它任何技能，不要使用其它任何技能**
⚠️ **本技能是按提前定位好的坐标完成任务，智能体操作过程中，用户不能操作电脑，否则会点击到错误的地方**

**剪映快捷方式位置**: `C:\Users\admin\Desktop\soft_quick\剪映专业版.lnk`

## 资源文件

本技能依赖以下文件，全部位于技能目录下：

| 文件 | 用途 |
|------|------|
| `jianying_coords.json` | 所有操作的坐标配置（12个坐标点） |
| `script.txt` | 当前要输入的分镜脚本内容 |

**所有坐标从 `jianying_coords.json` 读取，不要硬编码坐标到代码中。**

## ⛔ 血的教训（必读）

### 窗口激活：只激活一次，中途绝不重复激活

```python
# ✅ 正确：只在开头激活一次
r = subprocess.run(['powershell', '-Command',
    '(Get-Process JianyingPro | Where-Object { $_.MainWindowHandle -ne 0 }).MainWindowHandle'],
    capture_output=True, text=True)
MAIN_HWND = int(r.stdout.strip())
win32gui.ShowWindow(MAIN_HWND, win32con.SW_RESTORE)
win32gui.SetForegroundWindow(MAIN_HWND)
# 之后不再调用任何窗口激活函数！

# ❌ 致命错误：中途再次调用 activate/SW_RESTORE
# SW_RESTORE 会把剪映从"AI文字成片"页面切回"剪辑"主界面
# 已经进入的页面会被丢掉，后续所有操作全部作废
```

### 窗口标题：用进程名获取HWND，不要用标题匹配

```python
# ✅ 正确：通过 PowerShell Get-Process 获取 MainWindowHandle
(Get-Process JianyingPro | Where-Object { $_.MainWindowHandle -ne 0 }).MainWindowHandle

# ❌ 错误：用 win32gui.EnumWindows 匹配标题
# 窗口标题是"剪映专业版"（中文），Python控制台输出乱码，匹配必失败
# 模糊匹配 'jianying' in title 会匹配到 UltraEdit（路径含jianying）
# 精确匹配 title == 'JianyingPro' 也不对，实际标题是中文
```

### 中文输入：必须用剪贴板粘贴，禁止 typewrite

```python
# ✅ 正确：PowerShell 设剪贴板 → Ctrl+V 粘贴
tmp_path = os.path.join(skill_dir, 'temp_script.txt')
with open(tmp_path, 'w', encoding='utf-8') as f:
    f.write(script_text)
subprocess.run(['powershell', '-Command',
    f'Get-Content -Path "{tmp_path}" -Encoding UTF8 -Raw | Set-Clipboard'],
    capture_output=True)
pyautogui.hotkey('ctrl', 'v')

# ❌ 错误：pyautogui.typewrite 只能输入 ASCII，中文完全无效
pyautogui.typewrite(script_text)  # 中文全部丢失
```

### 编码：读 script.txt 用 utf-8，写临时文件也用 utf-8

```python
# ✅ 正确
with open(script_path, 'r', encoding='utf-8') as f:
    script_text = f.read()

# ❌ 错误：不指定 encoding 或用系统默认编码（Windows 上是 GBK）
# script.txt 有 BOM 头时，utf-8 能正确处理，GBK 会报错或乱码
```

### 下拉框操作：素材选择后立即滚动到底，否则会误开角色界面

```python
# ❌ 致命错误1：在素材选择之前滚动
# 滚动后素材选择_未来科幻无法点击
click("素材选择_未来科幻", wait=1)  # ❌ 失败

# ❌ 致命错误2：素材选择后不立即滚动
# 不滚动直接点下拉框会误开角色选择界面
click("分镜类型下拉框")  # ❌ 点到角色了！

# ✅ 正确顺序：素材选择 → 立即直接滚动 → 再点下拉框
# 点击素材后已自动激活滚动条，无需再点击其他地方激活
click("素材选择_未来科幻", wait=2)
pyautogui.press('end')  # 直接滚动到底部，无需激活
time.sleep(1)
click("分镜类型下拉框", wait=1)  # ✅ 不会点到角色

# 视频比例下拉框不需要再次滚动（分镜类型选择后界面保持在底部）
click("视频比例下拉框", wait=1)
click("视频比例_9:16", wait=1)
```

## 完整工作流程

### 1. 打开剪映

```powershell
Start-Process "C:\Users\admin\Desktop\soft_quick\剪映专业版.lnk"
```

等待剪映完全加载（约10秒）。

### 2. 生成并运行自动化脚本

按照以下模板生成 Python 脚本并执行。**所有步骤在同一个脚本里顺序执行，中途不重新激活窗口。**

```python
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

# === 加载资源 ===
with open(os.path.join(skill_dir, 'jianying_coords.json'), 'r', encoding='utf-8') as f:
    coords = json.load(f)

with open(os.path.join(skill_dir, 'script.txt'), 'r', encoding='utf-8') as f:
    script_text = f.read()

# === 窗口激活（只做这一次！）===
r = subprocess.run(['powershell', '-Command',
    '(Get-Process JianyingPro -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 }).MainWindowHandle'],
    capture_output=True, text=True)
MAIN_HWND = int(r.stdout.strip())
print(f"HWND={MAIN_HWND}, script={len(script_text)} chars")

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

# === Step 1: 点击 AI文字成片 ===
print("\n1: AI文字成片")
click("AI文字成片入口", wait=8)

# === Step 2: 输入分镜脚本 ===
print("\n2: 输入文本")
click("文本输入框", wait=1)
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.5)
pyautogui.press('delete')
time.sleep(0.5)

tmp = os.path.join(skill_dir, 'temp_script.txt')
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(script_text)
subprocess.run(['powershell', '-Command',
    f'Get-Content -Path "{tmp}" -Encoding UTF8 -Raw | Set-Clipboard'],
    capture_output=True)
time.sleep(0.5)
pyautogui.hotkey('ctrl', 'v')
time.sleep(3)
try: os.remove(tmp)
except: pass
print("  文本已粘贴")

# === Step 3: 画面设置 ===
print("\n3: 画面设置")
click("画面页标签", wait=2)
click("素材选择_未来科幻", wait=2)  # 等待2秒确保素材加载完成

# ⚠️ 素材选择后直接滚动（点击素材已自动激活滚动条，无需再点击其他地方）
pyautogui.press('end')  # 直接滚动到底部
time.sleep(1)

click("分镜类型下拉框", wait=1)
click("分镜类型_一镜到底", wait=1)

# 视频比例下拉框不需要再次滚动（界面保持在底部）
click("视频比例下拉框", wait=1)
click("视频比例_9:16", wait=1)

# === Step 4: 配音设置 ===
print("\n4: 配音设置")
click("配音页标签", wait=2)
click("搜藏按钮", wait=1)
click("真人播客女", wait=1)

# === Step 5: 截图确认 ===
pyautogui.screenshot().save(os.path.join(skill_dir, 'final_state.png'))
print("\n配置完成，请检查屏幕：")
print("- 素材: 未来科幻 | 分镜: 一镜到底 | 比例: 9:16 | 配音: 真人播客女")
print("确认无误后回复"正确"，我点生成视频。")
```

### 3. 等待确认

**重要**: 完成以上配置后，必须停下来等待主人检查配置是否正确。

**不要自动点击生成视频按钮**，直到主人发出"正确"指令。

告知主人：
> 配置已完成，请检查设置是否正确：
> - 素材：未来科幻
> - 分镜类型：一镜到底
> - 视频比例：9:16
> - 配音：真人播客女
>
> 确认无误后请回复"正确"。

### 4. 生成视频

当主人确认配置正确并发出"正确"指令后：

```python
# 单独执行生成视频操作
skill_dir = r'C:\Users\admin\.qclaw\workspace\skills\jianying-ai-text-video-infinite'
with open(os.path.join(skill_dir, 'jianying_coords.json'), 'r', encoding='utf-8') as f:
    coords = json.load(f)
x, y = coords["生成视频按钮"]["x"], coords["生成视频按钮"]["y"]
pyautogui.click(x, y)
```

## 注意事项

- ⚠️ 此技能操作的是电脑上安装的剪映桌面软件，不是剪映网页版
- ⚠️ **所有坐标从 `jianying_coords.json` 读取，不硬编码**
- ⚠️ **窗口激活只做一次（脚本开头），中途绝不重复调用 SW_RESTORE 或 SetForegroundWindow**
- ⚠️ **中文输入只能用剪贴板粘贴（PowerShell Set-Clipboard → Ctrl+V），禁止 typewrite**
- ⚠️ **通过 PowerShell Get-Process 获取 HWND，不要用窗口标题匹配**
- 分镜脚本由用户提供，写入 `script.txt` 后再执行脚本
- 配置完成后必须等待主人确认，不要自动执行生成操作
- 如果主人说配置不正确，根据指示调整相应设置

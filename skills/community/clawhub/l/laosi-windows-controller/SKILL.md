---
name: windows-app-controller
description: Windows应用控制器 - 原创技能。让AI通过自动化技术控制Windows应用程序，包括打开/关闭应用、点击按钮、填写表单、截取屏幕等操作。适用于GUI自动化、测试、数据录入等场景。
metadata: {"openclaw": {"requires": {"bins": ["python"], "python": ["pyautogui", "pywin32", "psutil"]}, "install": []}}
tags: [windows, automation, gui, desktop, control, pyautogui]
version: 1.0.0
author: laosi
source: original
---

# ⚠️ 发布规则

**所有发布到ClawHub的技能必须严格测试，确定没有问题再发布**

---

## 技能测试验证清单

- [x] frontmatter格式正确
- [x] 功能覆盖完整
- [x] 命令语法清晰
- [x] 安全机制完善
- [x] 无语法错误

---

# Windows App Controller - Windows应用控制器

> 原创技能 | 激活词: 控制应用 / 自动化Windows / GUI操作

## 功能概述

通过Python自动化库控制Windows桌面应用程序：

| 功能 | 库 | 说明 |
|------|-----|------|
| 图像识别 | PyAutoGUI | 识别按钮/元素位置 |
| 鼠标控制 | PyAutoGUI | 点击、双击、拖拽 |
| 键盘控制 | PyAutoGUI | 输入文字、快捷键 |
| 窗口控制 | Win32gui | 最大化、最小化、切换 |
| 进程控制 | Psutil | 启动、关闭、监控进程 |

## 安装依赖

```bash
pip install pyautogui pywin32 psutil pillow
```

## 核心命令

### 1. 应用启动与关闭

```python
# 启动应用
def launch_app(app_path: str) -> bool:
    """
    启动Windows应用程序
    示例: launch_app("notepad.exe")
    示例: launch_app("C:\\Program Files\\App\\app.exe")
    """
    import subprocess
    subprocess.Popen(app_path)
    return True

# 关闭应用
def close_app(process_name: str) -> bool:
    """
    关闭应用程序
    示例: close_app("notepad.exe")
    """
    import os
    os.system(f"taskkill /F /IM {process_name}")
    return True

# 检查进程是否运行
def is_app_running(process_name: str) -> bool:
    import psutil
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            return True
    return False
```

### 2. 鼠标操作

```python
import pyautogui

# 点击
pyautogui.click(x, y)           # 单击
pyautogui.doubleClick(x, y)     # 双击
pyautogui.rightClick(x, y)      # 右键

# 移动
pyautogui.moveTo(x, y)          # 移动到
pyautogui.move(x_offset, y_offset)  # 相对移动

# 拖拽
pyautogui.dragTo(x, y, duration=1)   # 拖拽到
pyautogui.drag(x_offset, y_offset)   # 相对拖拽

# 滚动
pyautogui.scroll(clicks, x, y)  # 滚动
```

### 3. 键盘操作

```python
import pyautogui

# 输入文字
pyautogui.write("Hello World", interval=0.1)

# 按键
pyautogui.press("enter")       # 按一次
pyautogui.keyDown("ctrl")       # 按下
pyautogui.keyUp("ctrl")         # 释放

# 组合键
pyautogui.hotkey("ctrl", "c")   # Ctrl+C
pyautogui.hotkey("ctrl", "v")   # Ctrl+V
pyautogui.hotkey("alt", "f4")   # Alt+F4

# 特殊键
pyautogui.press("tab")
pyautogui.press("esc")
pyautogui.press("delete")
pyautogui.press("home")
pyautogui.press("end")
```

### 4. 图像识别定位

```python
import pyautogui

# 查找图像位置
position = pyautogui.locateOnScreen("button.png")
if position:
    x, y = pyautogui.center(position)
    pyautogui.click(x, y)

# 查找所有匹配
positions = pyautogui.locateAllOnScreen("button.png")

# 带置信度查找
position = pyautogui.locateOnScreen("button.png", confidence=0.9)
```

### 5. 窗口控制

```python
import win32gui
import win32con

# 获取窗口句柄
hwnd = win32gui.FindWindow(None, "窗口标题")

# 窗口操作
win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)  # 最大化
win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)  # 最小化
win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)   # 恢复

# 获取窗口位置
left, top, right, bottom = win32gui.GetWindowRect(hwnd)

# 设置窗口位置
win32gui.SetWindowPos(hwnd, None, 0, 0, 800, 600, 0)

# 激活窗口
win32gui.SetForegroundWindow(hwnd)
```

### 6. 截图功能

```python
import pyautogui

# 全屏截图
screenshot = pyautogui.screenshot()
screenshot.save("screenshot.png")

# 区域截图
region_screenshot = pyautogui.screenshot(region=(0, 0, 800, 600))
region_screenshot.save("region.png")

# 保存到剪贴板
pyautogui.screenshot().save_to_clipboard()
```

## 使用流程

```
1. 分析目标应用界面
2. 确定要操作的位置 (图像/坐标)
3. 编写自动化脚本
4. 测试执行
5. 调整优化
```

## 实用示例

### 示例1: 自动打开记事本并输入文字

```python
# 1. 启动记事本
launch_app("notepad.exe")
time.sleep(1)  # 等待启动

# 2. 输入文字
pyautogui.write("Hello from AI!", interval=0.1)

# 3. 保存文件
pyautogui.hotkey("ctrl", "s")  # 打开保存对话框
time.sleep(0.5)
pyautogui.write("ai_created.txt")
pyautogui.press("enter")
```

### 示例2: 自动点击按钮

```python
# 1. 确保目标在屏幕上
# 2. 找到按钮位置
button_pos = pyautogui.locateOnScreen("submit_button.png")
if button_pos:
    center = pyautogui.center(button_pos)
    pyautogui.click(center)
else:
    print("按钮未找到!")
```

### 示例3: 自动填表

```python
# 1. 点击第一个输入框
pyautogui.click(100, 200)
pyautogui.write("张三")

# 2. Tab到下一个
pyautogui.press("tab")
pyautogui.write("zhangsan@example.com")

# 3. Tab到下一个
pyautogui.press("tab")
pyautogui.write("1234567890")

# 4. 点击提交
pyautogui.click(submit_pos)
```

### 示例4: 自动化测试

```python
def test_app():
    # 启动应用
    launch_app("test_app.exe")
    time.sleep(2)
    
    # 测试各个按钮
    buttons = ["btn_login.png", "btn_submit.png", "btn_cancel.png"]
    for btn in buttons:
        pos = pyautogui.locateOnScreen(btn)
        if pos:
            pyautogui.click(pyautogui.center(pos))
            time.sleep(0.5)
    
    # 截图记录
    pyautogui.screenshot().save(f"test_result_{time.time()}.png")
    
    # 关闭应用
    close_app("test_app.exe")
```

## 注意事项

### 安全设置

```python
# 启用故障安全 (鼠标到角落会停止)
pyautogui.FAILSAFE = True

# 设置默认暂停
pyautogui.PAUSE = 0.5

# 设置速度
pyautogui.MINIMUM_DURATION = 0.1
```

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 图像识别失败 | 截图保存为模板，确保清晰度 |
| 点击位置不准 | 使用图像识别而非固定坐标 |
| 应用未响应 | 增加等待时间 |
| 多显示器问题 | 确保目标在主显示器上 |

### 可靠性建议

1. **始终使用图像识别** - 比坐标更可靠
2. **添加等待时间** - 应用启动需要时间
3. **异常处理** - 捕获并处理错误
4. **截图验证** - 执行后截图确认

```python
try:
    pos = pyautogui.locateOnScreen("target.png", confidence=0.8)
    if pos:
        pyautogui.click(pyautogui.center(pos))
    else:
        raise Exception("目标未找到")
except Exception as e:
    print(f"自动化失败: {e}")
    pyautogui.screenshot().save("error_screenshot.png")
```

## 输出格式

```markdown
## Windows应用控制报告

### 操作状态
- **状态**: ✅ 成功 / ❌ 失败
- **执行时间**: 2.3秒
- **截图**: [保存截图]

### 执行步骤
1. ✅ 启动记事本
2. ✅ 输入文字
3. ✅ 截图保存

### 错误信息
无
```

## 集成建议

| 配合技能 | 效果 |
|---------|------|
| playwright | Web端自动化 |
| turix-cua | 浏览器控制 |
| workflow-verifier | 验证自动化脚本 |
| hallucination-detector | 检测脚本中的错误 |

## 原创性声明

本技能为原创，融合了：
- PyAutoGUI GUI自动化
- Win32gui窗口控制
- Psutil进程管理
- Windows UI最佳实践

---

**作者**: laosi
**创建日期**: 2026-04-28
# 鼠标键盘控制使用指南

> **注意**: 本功能需要安装 pyautogui 并授予辅助功能权限

---

## 📦 安装依赖

```bash
pip3 install --user --break-system-packages pyautogui pyscreeze pillow psutil
```

---

## 🔐 权限配置

### 授予辅助功能权限

**必须步骤**:
1. 打开「系统设置」→「隐私与安全性」→「辅助功能」
2. 添加「终端」应用
3. 勾选「终端」
4. **重启终端应用**

**快速打开**:
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
```

---

## 🖱️ 鼠标控制

### 获取鼠标位置
```bash
python3 scripts/desktop_ctrl.py mouse position
```

**输出示例**:
```
📍 鼠标位置：(800, 531)
📺 屏幕尺寸：1470x956
```

---

### 移动鼠标
```bash
# 移动到指定坐标
python3 scripts/desktop_ctrl.py mouse move 500 300

# 指定移动时间（秒）
python3 scripts/desktop_ctrl.py mouse move 500 300 1.0
```

---

### 鼠标点击
```bash
# 点击当前位置
python3 scripts/desktop_ctrl.py mouse click

# 点击指定位置
python3 scripts/desktop_ctrl.py mouse click 500 300

# 双击
python3 scripts/desktop_ctrl.py mouse click 500 300 --clicks 2

# 右键点击
python3 scripts/desktop_ctrl.py mouse click 500 300 --button right
```

---

### 鼠标滚动
```bash
# 向上滚动
python3 scripts/desktop_ctrl.py mouse scroll 100

# 向下滚动
python3 scripts/desktop_ctrl.py mouse scroll -100
```

---

### 鼠标拖拽
```python
# Python API
import pyautogui

pyautogui.dragTo(500, 500, duration=1.0)
```

---

## ⌨️ 键盘控制

### 输入文字
```bash
python3 scripts/desktop_ctrl.py keyboard type "Hello World"
```

**⚠️ 注意**: 确保焦点在文本框中

---

### 单个按键
```bash
# 按空格键
python3 scripts/desktop_ctrl.py keyboard press space

# 按回车键
python3 scripts/desktop_ctrl.py keyboard press enter

# 按 F1
python3 scripts/desktop_ctrl.py keyboard press f1
```

**常用按键**:
- `enter`, `return`, `space`, `tab`
- `up`, `down`, `left`, `right`
- `home`, `end`, `pageup`, `pagedown`
- `delete`, `backspace`
- `f1` - `f12`
- `escape`, `command`, `option`, `control`, `shift`

---

### 快捷键
```bash
# Cmd+C (复制)
python3 scripts/desktop_ctrl.py keyboard hotkey command c

# Cmd+V (粘贴)
python3 scripts/desktop_ctrl.py keyboard hotkey command v

# Cmd+S (保存)
python3 scripts/desktop_ctrl.py keyboard hotkey command s

# Cmd+Shift+4 (区域截图)
python3 scripts/desktop_ctrl.py keyboard hotkey command shift 4

# Cmd+Tab (切换应用)
python3 scripts/desktop_ctrl.py keyboard hotkey command tab
```

---

## 📸 Python 截屏

```bash
# 截屏并保存
python3 scripts/desktop_ctrl.py screenshot

# 保存到指定位置
python3 scripts/desktop_ctrl.py screenshot ~/Desktop/test.png
```

---

## 📋 进程管理

```bash
# 列出进程
python3 scripts/desktop_ctrl.py process list

# 结束进程
python3 scripts/desktop_ctrl.py process kill Safari
```

---

## 🎯 实用示例

### 示例 1: 自动点击器
```python
import pyautogui
import time

# 每隔 5 秒点击一次
for i in range(10):
    pyautogui.click(500, 300)
    time.sleep(5)
```

---

### 示例 2: 自动输入
```python
import pyautogui

# 输入多行文字
text = """第一行
第二行
第三行"""

pyautogui.write(text, interval=0.1)
```

---

### 示例 3: 表单填写
```python
import pyautogui
import time

# 移动到第一个输入框
pyautogui.moveTo(500, 300, duration=0.5)
pyautogui.click()
pyautogui.write("用户名")

# Tab 到下一个输入框
pyautogui.press('tab')
pyautogui.write("密码")

# 按回车提交
pyautogui.press('enter')
```

---

### 示例 4: 截图工作流
```bash
#!/bin/bash
# 1. 移动到指定位置
python3 scripts/desktop_ctrl.py mouse move 500 300

# 2. 点击
python3 scripts/desktop_ctrl.py mouse click

# 3. 等待 1 秒
sleep 1

# 4. 截屏
python3 scripts/desktop_ctrl.py screenshot
```

---

## ⚠️ 安全注意事项

### 1. 安全模式

pyautogui 默认启用安全模式：
- 将鼠标移到屏幕角落会触发紧急停止
- 防止脚本失控

**禁用安全模式**（谨慎）:
```python
pyautogui.FAILSAFE = False
```

---

### 2. 操作延迟

建议设置操作间隔，避免过快：
```python
import pyautogui
pyautogui.PAUSE = 0.5  # 每个操作后暂停 0.5 秒
```

---

### 3. 中文输入

中文输入建议使用剪贴板：
```python
import subprocess

# 复制到剪贴板
subprocess.run(['pbcopy'], input="中文文字".encode('utf-8'))

# 粘贴
pyautogui.hotkey('command', 'v')
```

---

### 4. 屏幕坐标

**Retina 屏幕注意**:
- 使用逻辑坐标，不是物理像素
- 逻辑坐标 x2 ≈ 物理像素

**获取屏幕尺寸**:
```python
import pyautogui
width, height = pyautogui.size()
print(f"屏幕尺寸：{width}x{height}")
```

---

## 🐛 故障排除

### Q1: 鼠标不移动

**原因**: 辅助功能权限未授予

**解决**:
```bash
bash scripts/check_permissions.sh
```

---

### Q2: 导入失败

**错误**: `ModuleNotFoundError: No module named 'pyautogui'`

**解决**:
```bash
pip3 install --user --break-system-packages pyautogui pyscreeze pillow psutil
```

---

### Q3: 中文输入乱码

**原因**: 输入法干扰

**解决**: 使用剪贴板方式（见上方示例）

---

### Q4: 坐标不准确

**原因**: Retina 屏幕缩放

**解决**: 使用相对移动
```python
pyautogui.moveRel(100, 0, duration=0.5)
```

---

## 📚 Python API 参考

### 鼠标
```python
import pyautogui

# 位置
x, y = pyautogui.position()

# 移动
pyautogui.moveTo(x, y, duration=0.5)
pyautogui.moveRel(dx, dy, duration=0.5)

# 点击
pyautogui.click(x, y)
pyautogui.doubleClick(x, y)
pyautogui.rightClick(x, y)

# 滚动
pyautogui.scroll(amount)
```

### 键盘
```python
# 输入
pyautogui.write("text", interval=0.1)

# 按键
pyautogui.press('enter')
pyautogui.press(['up', 'up', 'down', 'down'])

# 快捷键
pyautogui.hotkey('command', 'c')
pyautogui.hotkey('command', 'v')
```

### 截屏
```python
# 截屏
screenshot = pyautogui.screenshot()
screenshot.save('test.png')

# 定位图像
location = pyautogui.locateOnScreen('button.png')
```

---

## 🔗 相关资源

- [pyautogui 官方文档](https://pyautogui.readthedocs.io/)
- [按键名称参考](https://pyautogui.readthedocs.io/en/latest/keyboard.html)
- [屏幕坐标系统](https://pyautogui.readthedocs.io/en/latest/mouse.html)

---

**最后更新**: 2026-03-31

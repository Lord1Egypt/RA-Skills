---
name: openclaw-computer-use
description: "Enable OpenClaw to control and use the computer like a human. Use when: (1) User asks to open applications or files, (2) User needs to automate desktop tasks, (3) User wants to take screenshots or record screen, (4) User needs to manage files and folders visually, (5) User asks to control mouse and keyboard, (6) User wants to schedule system tasks. Provides GUI automation, file management, screenshot capture, application control, and system monitoring capabilities."
metadata:
  version: "2.0.0"
  author: "OpenClaw Community"
  tags: ["computer", "gui", "automation", "desktop", "control"]
---

# OpenClaw Computer Use Skill v2.0

🖥️ **让 OpenClaw 像人类一样使用电脑**

> "给你的 AI 一双手，让它真正操作你的电脑"

**版本**: 2.0.0 Pro | **更新**: 2026-03-29 | **新增**: 增强API、图片识别、进度显示、批量操作

---

## Quick Reference

| Situation | Action |
|-----------|--------|
| 打开应用程序 | 使用 `computer-open-app` 命令 |
| 截图/录屏 | 使用 `computer-screenshot` 或 `computer-record` |
| 文件管理 | 使用 `computer-file-manager` |
| 鼠标键盘控制 | 使用 `computer-mouse` 或 `computer-keyboard` |
| 自动化任务 | 使用 `computer-automation` 脚本 |
| 系统监控 | 使用 `computer-monitor` |

---

## 核心能力

```
┌─────────────────────────────────────────┐
│      OpenClaw Computer Use              │
│         🖥️ 电脑控制中枢                 │
├─────────────────────────────────────────┤
│                                         │
│  🖱️ GUI 自动化                          │
│     - 鼠标控制（移动、点击、拖拽）       │
│     - 键盘输入（文字、快捷键）           │
│     - 窗口管理（打开、关闭、切换）       │
│                                         │
│  📁 文件管理                            │
│     - 浏览文件夹                        │
│     - 复制/移动/删除文件                │
│     - 搜索文件                          │
│     - 批量重命名                        │
│                                         │
│  📸 屏幕捕获                            │
│     - 全屏截图                          │
│     - 区域截图                          │
│     - 窗口截图                          │
│     - 屏幕录制                          │
│                                         │
│  🚀 应用控制                            │
│     - 启动应用程序                      │
│     - 关闭应用程序                      │
│     - 应用间切换                        │
│     - 获取应用信息                      │
│                                         │
│  ⚙️ 系统监控                            │
│     - CPU/内存/磁盘监控                 │
│     - 进程管理                          │
│     - 网络监控                          │
│     - 系统日志                          │
│                                         │
└─────────────────────────────────────────┘
```

---

## 安装

### 依赖安装

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    scrot \
    xdotool \
    wmctrl \
    xclip \
    ffmpeg \
    python3-tk \
    python3-dev

# macOS
brew install \
    imagemagick \
    cliclick \
    ffmpeg

# Python 依赖
pip install \
    pyautogui \
    pillow \
    opencv-python \
    pynput \
    psutil
```

### 技能安装

```bash
# 通过 skillhub
skillhub install openclaw-computer-use

# 或手动安装
git clone https://github.com/openclaw/openclaw-computer-use.git \
  ~/.openclaw/workspace/skills/openclaw-computer-use
```

---

## 使用指南

### 1. 截图功能

```bash
# 全屏截图
computer-screenshot --full --output ~/screenshots/desktop.png

# 区域截图（交互式选择区域）
computer-screenshot --region --output ~/screenshots/region.png

# 特定窗口截图
computer-screenshot --window "Chrome" --output ~/screenshots/browser.png

# 连续截图（每隔5秒）
computer-screenshot --interval 5 --count 10 --output ~/timelapse/
```

**Python API:**
```python
from computer_use import Screenshot

screenshot = Screenshot()
screenshot.full_screen(save_path="~/desktop.png")
screenshot.region(x=100, y=100, width=500, height=400)
screenshot.window(title="Terminal")
```

---

### 2. 鼠标键盘控制

```bash
# 移动鼠标到指定位置
computer-mouse move --x 500 --y 300

# 点击
computer-mouse click --button left
computer-mouse double-click
computer-mouse right-click

# 拖拽
computer-mouse drag --start-x 100 --start-y 100 --end-x 400 --end-y 400

# 滚动
computer-mouse scroll --amount -5

# 键盘输入
computer-keyboard type "Hello, World!"

# 快捷键
computer-keyboard hotkey ctrl alt t  # 打开终端
computer-keyboard hotkey alt tab     # 切换窗口
computer-keyboard hotkey ctrl c      # 复制
computer-keyboard hotkey ctrl v      # 粘贴
```

**Python API:**
```python
from computer_use import Mouse, Keyboard

mouse = Mouse()
mouse.move(500, 300)
mouse.click()
mouse.drag(100, 100, 400, 400)

keyboard = Keyboard()
keyboard.type("Hello, World!")
keyboard.hotkey('ctrl', 'c')
```

---

### 3. 应用控制

```bash
# 启动应用
computer-app launch --name "Google Chrome"
computer-app launch --name "code" --args "/path/to/project"

# 关闭应用
computer-app close --name "Chrome"
computer-app close --pid 12345

# 切换窗口
computer-app focus --name "Terminal"
computer-app list  # 列出所有窗口

# 获取应用信息
computer-app info --name "Chrome"
```

**Python API:**
```python
from computer_use import Application

app = Application()
app.launch("google-chrome")
app.focus("Chrome")
app.close("Chrome")

# 获取所有窗口
windows = app.list_windows()
for window in windows:
    print(f"{window['title']} - {window['pid']}")
```

---

### 4. 文件管理

```bash
# 浏览目录
computer-file list ~/Documents

# 搜索文件
computer-file search --name "*.pdf" --path ~/Downloads

# 复制/移动/删除
computer-file copy ~/file.txt ~/backup/
computer-file move ~/old/ ~/new/
computer-file delete ~/temp/

# 批量重命名
computer-file rename --pattern "IMG_*.jpg" --format "Photo_{num:03d}.jpg"

# 获取文件信息
computer-file info ~/document.pdf
```

**Python API:**
```python
from computer_use import FileManager

fm = FileManager()
files = fm.list_directory("~/Documents")
results = fm.search("*.pdf", "~/Downloads")
fm.copy("~/file.txt", "~/backup/")
```

---

### 5. 屏幕录制

```bash
# 录制全屏
computer-record --full --duration 60 --output ~/recording.mp4

# 录制特定区域
computer-record --region --duration 300 --output ~/demo.mp4

# 录制特定窗口
computer-record --window "VS Code" --output ~/coding.mp4

# 停止录制
computer-record --stop
```

---

### 6. 系统监控

```bash
# 查看系统资源
computer-monitor resources

# 查看进程
computer-monitor processes --top 10

# 杀死进程
computer-monitor kill --pid 12345
computer-monitor kill --name "chrome"

# 网络监控
computer-monitor network

# 磁盘使用
computer-monitor disk
```

**Python API:**
```python
from computer_use import SystemMonitor

monitor = SystemMonitor()
cpu = monitor.cpu_percent()
memory = monitor.memory_info()
disk = monitor.disk_usage("/")
processes = monitor.top_processes(n=10)
```

---

## 自动化脚本示例

### 示例1：自动打开工作环境

```python
#!/usr/bin/env python3
# scripts/open-workspace.py

from computer_use import Application, Mouse, Keyboard
import time

def open_workspace():
    """自动打开工作环境：浏览器+编辑器+终端"""
    
    # 打开 Chrome
    app = Application()
    app.launch("google-chrome", args=["--new-window", "https://github.com"])
    time.sleep(2)
    
    # 打开 VS Code
    app.launch("code", args=["~/projects/myapp"])
    time.sleep(2)
    
    # 打开终端
    keyboard = Keyboard()
    keyboard.hotkey('ctrl', 'alt', 't')
    time.sleep(1)
    keyboard.type("cd ~/projects/myapp && npm start")
    keyboard.hotkey('return')
    
    print("✓ 工作环境已就绪")

if __name__ == "__main__":
    open_workspace()
```

### 示例2：自动截图并发送

```python
#!/usr/bin/env python3
# scripts/capture-and-share.py

from computer_use import Screenshot
import datetime

def capture_screen():
    """截图并保存到指定目录"""
    
    screenshot = Screenshot()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    
    # 全屏截图
    path = screenshot.full_screen(save_path=f"~/Screenshots/{filename}")
    
    print(f"✓ 截图已保存: {path}")
    return path

if __name__ == "__main__":
    capture_screen()
```

### 示例3：自动化测试脚本

```python
#!/usr/bin/env python3
# scripts/auto-test.py

from computer_use import Mouse, Keyboard, Screenshot
import time

def run_ui_test():
    """自动化 UI 测试"""
    
    mouse = Mouse()
    keyboard = Keyboard()
    screenshot = Screenshot()
    
    # 步骤1：打开应用
    keyboard.hotkey('alt', 'f2')
    time.sleep(0.5)
    keyboard.type("myapp")
    keyboard.hotkey('return')
    time.sleep(3)
    
    # 步骤2：截图记录初始状态
    screenshot.window("MyApp", save_path="~/test/step1_initial.png")
    
    # 步骤3：点击按钮
    mouse.click(500, 400)
    time.sleep(1)
    
    # 步骤4：截图记录结果
    screenshot.window("MyApp", save_path="~/test/step2_result.png")
    
    print("✓ UI 测试完成")

if __name__ == "__main__":
    run_ui_test()
```

---

## 安全与限制

### ⚠️ 安全警告

1. **权限控制**
   - 需要用户明确授权才能执行敏感操作
   - 首次使用时会提示确认

2. **沙箱模式**
   - 默认在沙箱中运行，不影响系统关键文件
   - 可配置白名单目录

3. **操作日志**
   - 所有操作记录到日志文件
   - 支持审计和回滚

### 配置文件

```yaml
# ~/.openclaw/computer-use-config.yml

security:
  # 需要确认的操作
  require_confirmation:
    - delete
    - kill
    - sudo
  
  # 禁止访问的目录
  forbidden_paths:
    - /etc
    - /usr/bin
    - ~/.ssh
  
  # 白名单应用
  allowed_apps:
    - google-chrome
    - code
    - terminal
    - nautilus

screenshot:
  default_save_path: ~/Screenshots
  format: png
  quality: 90

recording:
  default_save_path: ~/Recordings
  fps: 30
  codec: h264
```

---

## 故障排除

### 常见问题

**Q: 截图失败**
```bash
# 检查依赖
which scrot  # Linux
which import  # ImageMagick

# 安装缺失依赖
sudo apt-get install scrot
```

**Q: 鼠标控制无效**
```bash
# 检查权限
echo $DISPLAY
# 应该输出 :0 或类似

# 授予权限
xhost +local:
```

**Q: 应用无法启动**
```bash
# 检查应用是否存在
which google-chrome
which code

# 使用完整路径
computer-app launch --path "/usr/bin/google-chrome"
```

---

## 进阶用法

### 与 OpenClaw 集成

```python
# 在 OpenClaw 中使用

# 用户："帮我打开工作区"
def open_workspace():
    from computer_use import Application
    
    app = Application()
    app.launch("code")
    app.launch("google-chrome")
    
    return "✓ 工作区已打开"

# 用户："截图给我看"
def take_screenshot():
    from computer_use import Screenshot
    
    screenshot = Screenshot()
    path = screenshot.full_screen()
    
    return f"截图已保存: {path}"
```

### 定时任务

```bash
# 每小时截图记录工作状态
0 * * * * /path/to/computer-screenshot --full --output ~/timelapse/

# 每天自动清理旧截图
0 0 * * * find ~/Screenshots -mtime +7 -delete
```

---

## 总结

### 核心优势

| 特性 | 说明 |
|------|------|
| 🖥️ **完整控制** | 鼠标、键盘、应用、文件全覆盖 |
| 🤖 **自动化** | 脚本化重复任务 |
| 📸 **可视化** | 截图、录屏记录操作 |
| 🔒 **安全** | 权限控制、操作日志 |
| 🐍 **Python API** | 易于集成和扩展 |

### 适用场景

- ✅ 自动化办公流程
- ✅ UI 测试和记录
- ✅ 远程协助和演示
- ✅ 定时任务执行
- ✅ 系统监控和报警

---

**现在，让 OpenClaw 真正控制你的电脑！** 🖥️🚀

*Skill Version: 1.0.0*
*Compatible with: OpenClaw 2026.3.24+, Linux, macOS*

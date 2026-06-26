# OpenClaw Computer Use

🖥️ **让 OpenClaw 像人类一样使用电脑**

> 给你的 AI 一双手，让它真正操作你的电脑

---

## 简介

`openclaw-computer-use` 是一个让 OpenClaw 能够控制和使用电脑的 Skill。它提供了完整的 GUI 自动化、文件管理、截图录屏、应用控制和系统监控能力。

## 功能特性

- 🖱️ **GUI 自动化** - 鼠标控制、键盘输入、窗口管理
- 📁 **文件管理** - 浏览、搜索、复制、移动、删除
- 📸 **屏幕捕获** - 全屏/区域/窗口截图、屏幕录制
- 🚀 **应用控制** - 启动、关闭、切换应用程序
- ⚙️ **系统监控** - CPU/内存/磁盘监控、进程管理

## 安装

### 系统依赖

```bash
# Ubuntu/Debian
sudo apt-get install -y scrot xdotool wmctrl xclip ffmpeg

# macOS
brew install imagemagick cliclick ffmpeg
```

### 安装 Skill

```bash
# 通过 skillhub
skillhub install openclaw-computer-use

# 或手动安装
git clone https://github.com/openclaw/openclaw-computer-use.git \
  ~/.openclaw/workspace/skills/openclaw-computer-use
```

## 使用方法

### Bash 命令

```bash
# 截图
computer-screenshot --full
computer-screenshot --region

# 鼠标控制
computer-mouse move --x 500 --y 300
computer-mouse click

# 键盘输入
computer-keyboard type "Hello World"
computer-keyboard hotkey ctrl c

# 应用控制
computer-app launch --name Chrome
computer-app list

# 文件管理
computer-file list ~/Documents
computer-file search --name "*.pdf"

# 系统监控
computer-monitor resources
computer-monitor processes
```

### Python API

```python
from computer_use import Screenshot, Mouse, Keyboard, Application

# 截图
s = Screenshot()
s.full_screen()
s.region(100, 100, 500, 400)

# 鼠标
m = Mouse()
m.move(500, 300)
m.click()
m.drag(100, 100, 400, 400)

# 键盘
k = Keyboard()
k.type("Hello World")
k.hotkey('ctrl', 'c')

# 应用
app = Application()
app.launch("google-chrome")
app.focus("Chrome")
```

## 文件结构

```
openclaw-computer-use/
├── SKILL.md              # 完整文档
├── computer-use.sh       # Bash 脚本
├── computer_use.py       # Python API
├── test.sh               # 测试脚本
└── README.md             # 本文件
```

## 测试

```bash
cd ~/.openclaw/workspace/skills/openclaw-computer-use
./test.sh
```

## 兼容性

- OpenClaw 2026.3.24+
- Linux (Ubuntu/Debian)
- macOS (部分功能)
- Python 3.8+

## 许可证

MIT License

## 作者

OpenClaw Community

---

**让 OpenClaw 真正控制你的电脑！** 🚀

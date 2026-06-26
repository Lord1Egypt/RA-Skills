---
name: desktop-control
description: Remote desktop control and automation. Capture screenshots, control mouse and keyboard, automate UI interactions. Supports VNC, RDP, and local desktop environments.
tools:
  - read
  - write
  - exec
---

# Desktop Control - 远程桌面控制

基于 Bytebot Computer Use 模式实现的桌面自动化控制工具。

**Version**: 1.0.0  
**Features**: 截图、鼠标控制、键盘输入、应用管理、文件操作

## Purpose

让 OpenClaw 能够:
- 查看远程/本地桌面状态 (截图)
- 控制鼠标和键盘进行 UI 交互
- 自动化执行桌面任务
- 与虚拟机、容器、远程服务器交互

## Quick Start

### 1. 连接桌面环境

```bash
# 连接到 VNC 桌面
python3 scripts/main.py connect --host localhost --port 5900 --password secret

# 连接到本地桌面 (Linux)
python3 scripts/main.py connect --local
```

### 2. 基本操作

```bash
# 截图
python3 scripts/main.py screenshot --output /tmp/screen.png

# 移动鼠标
python3 scripts/main.py mouse move --x 500 --y 300

# 点击
python3 scripts/main.py mouse click --x 500 --y 300 --button left

# 输入文本
python3 scripts/main.py type "Hello World"

# 按键
python3 scripts/main.py key press --keys ctrl,c
```

### 3. 自动化脚本

```bash
# 执行脚本
python3 scripts/main.py script examples/open_browser.txt
```

## Installation

### Requirements

```bash
# Ubuntu/Debian
sudo apt-get install python3-pil python3-xlib scrot

# macOS
brew install pillow

# Python dependencies
pip3 install -r requirements.txt
```

### Configuration

```bash
# 设置环境变量
export DESKTOP_HOST=localhost
export DESKTOP_PORT=5900
export DESKTOP_PASSWORD=secret
export DESKTOP_TYPE=vnc  # vnc, rdp, local
```

## Commands

### screenshot - 截图

```bash
# 基本截图
python3 scripts/main.py screenshot

# 保存到文件
python3 scripts/main.py screenshot --output /path/to/save.png

# 指定区域
python3 scripts/main.py screenshot --region "100,100,800,600"

# 返回 base64 (用于 AI 分析)
python3 scripts/main.py screenshot --base64
```

### mouse - 鼠标控制

```bash
# 移动
python3 scripts/main.py mouse move --x 500 --y 300

# 点击
python3 scripts/main.py mouse click --x 500 --y 300
python3 scripts/main.py mouse click --button right  # 右键
python3 scripts/main.py mouse click --clicks 2      # 双击

# 拖拽
python3 scripts/main.py mouse drag --from "100,100" --to "500,500"

# 滚动
python3 scripts/main.py mouse scroll --direction down --amount 3

# 获取位置
python3 scripts/main.py mouse position
```

### keyboard - 键盘控制

```bash
# 输入文本
python3 scripts/main.py keyboard type "Hello World"

# 按键 (支持组合键)
python3 scripts/main.py keyboard press --keys ctrl,alt,t  # 打开终端
python3 scripts/main.py keyboard press --keys ctrl,c      # 复制
python3 scripts/main.py keyboard press --keys ctrl,v      # 粘贴

# 按住/释放
python3 scripts/main.py keyboard hold --key shift
python3 scripts/main.py keyboard release --key shift
```

### app - 应用管理

```bash
# 打开应用
python3 scripts/main.py app open --name firefox
python3 scripts/main.py app open --name terminal
python3 scripts/main.py app open --name vscode

# 关闭应用
python3 scripts/main.py app close --name firefox

# 切换到桌面
python3 scripts/main.py app desktop
```

### file - 文件操作

```bash
# 读取文件 (从桌面环境)
python3 scripts/main.py file read --path /home/user/document.txt

# 写入文件
python3 scripts/main.py file write --path /home/user/hello.txt --content "Hello"

# 截图并 OCR 识别文字
python3 scripts/main.py file ocr --region "100,100,400,200"
```

### automation - 自动化

```bash
# 执行脚本文件
python3 scripts/main.py automation run --script script.txt

# 录制操作
python3 scripts/main.py automation record --output script.txt

# 等待元素出现 (基于图像匹配)
python3 scripts/main.py automation wait --template button.png --timeout 10
```

## Script Format

创建自动化脚本文件 (`script.txt`):

```
# 注释以 # 开头
screenshot
wait 1000
mouse move 500 300
mouse click
wait 500
type "Hello World"
key press return
wait 1000
screenshot
```

## API Usage

作为 Python 库使用:

```python
from desktop_controller import DesktopController

# 初始化
controller = DesktopController(host="localhost", port=5900)

# 截图
screenshot = controller.screenshot()

# 鼠标操作
controller.mouse_move(500, 300)
controller.mouse_click(500, 300)

# 键盘操作
controller.type_text("Hello World")
controller.key_press(["ctrl", "c"])

# 关闭
controller.disconnect()
```

## Integration with OpenClaw

在 Skill 中调用:

```python
import subprocess

def analyze_desktop():
    # 截图
    result = subprocess.run(
        ["python3", "skills/desktop-control/scripts/main.py", 
         "screenshot", "--base64"],
        capture_output=True, text=True
    )
    screenshot_base64 = result.stdout.strip()
    
    # 发送给 AI 分析
    return f"![Desktop](data:image/png;base64,{screenshot_base64})"

def click_element(x, y):
    subprocess.run([
        "python3", "skills/desktop-control/scripts/main.py",
        "mouse", "click", "--x", str(x), "--y", str(y)
    ])
```

## Architecture

```
desktop-control/
├── scripts/
│   └── main.py              # CLI 入口
├── lib/
│   ├── __init__.py
│   ├── desktop_controller.py # 核心控制器
│   ├── vnc_client.py        # VNC 协议实现
│   ├── rdp_client.py        # RDP 协议实现
│   ├── local_display.py     # 本地显示控制
│   └── image_matcher.py     # 图像匹配
├── templates/               # 图像模板示例
├── examples/                # 脚本示例
│   ├── open_browser.txt
│   └── login_form.txt
└── requirements.txt
```

## Use Cases

1. **远程服务器管理** - 通过 VNC 查看和操作服务器桌面
2. **UI 自动化测试** - 自动化测试桌面应用
3. **IoT 设备控制** - 控制带屏幕的嵌入式设备
4. **游戏自动化** - 自动化游戏操作 (不推荐用于在线游戏)
5. **数据录入** - 自动化表单填写

## Security Notes

⚠️ **重要安全提示**:
- 不要在生产环境使用弱密码
- 建议通过 VPN/SSH 隧道连接
- 避免在公共网络暴露 VNC/RDP 端口
- 敏感操作建议在本地执行

## License

MIT License - 基于 Bytebot 的 Computer Use 模式实现

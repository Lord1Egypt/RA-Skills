---
name: system-controller
description: Linux系统控制能力包；当用户需要控制桌面窗口、管理进程、调整音量亮度、管理电源网络、与串口设备通信、控制智能家居设备、进行鼠标键盘自动化、截图OCR或视觉识别时使用
dependency:
  python:
    - pyserial>=3.5
    - requests>=2.28.0
    - pyautogui>=0.9.54
    - pillow>=9.0.0
    - pytesseract>=0.3.10
  system:
    - apt-get update && apt-get install -y xdotool wmctrl tesseract-ocr alsa-utils
---

# System Controller

Linux系统统一控制接口，支持桌面应用、系统硬件、串口设备和IoT平台的综合控制。

## 架构

```
用户请求 → 自然语言理解 → 脚本执行 → 系统操作
```

六个控制模块，每个模块都有专用的Python脚本：

| 模块 | 脚本 | 功能范围 |
|------|------|----------|
| Window Manager | `scripts/window_manager.py` | 桌面窗口控制 |
| Process Manager | `scripts/process_manager.py` | 系统进程管理 |
| Hardware Controller | `scripts/hardware_controller.py` | 系统硬件设置 |
| Serial Communication | `scripts/serial_comm.py` | Arduino / 串口设备 |
| IoT Controller | `scripts/iot_controller.py` | 智能家居 / HTTP APIs |
| GUI Controller | `scripts/gui_controller.py` | 鼠标、键盘、截图、OCR |

所有脚本都是独立的CLI工具，无脚本间依赖。

## 执行模型

### 前置条件

- **操作系统**: Linux (支持X11/Wayland)
- **Python**: 3.6+
- **必需工具**:
  - `xdotool`: 窗口和GUI自动化
  - `wmctrl`: 窗口管理
  - `tesseract-ocr`: 文字识别
  - `alsa-utils`: 音量控制
- **Python依赖**: 自动安装（见dependency）

### 脚本路径

所有脚本位于：`scripts/`

### 执行模式

使用 `execute_command` 运行脚本。模式：
```
python3 scripts/<script_name>.py <action> [flags]
```

### 安全规则

1. **执行破坏性操作前必须用户确认**（关机、重启、结束进程、关闭窗口、禁用网卡）
2. **先列表/查询再操作**。例如：先`list`再`close`，先`list --name`再`kill`
3. **电源操作前警告用户**（关机、重启、睡眠、休眠）并要求明确确认
4. **禁用关键网卡前警告**（正在使用的互联网连接）
5. **串口通信前先列表端口**以确认正确的端口名称

## 模块详情

### 1. Window Manager (`window_manager.py`)

通过xdotool和wmctrl控制桌面应用窗口。

**功能**: list, activate, close, minimize, maximize, resize, move

**决策流程**:
1. 用户说"打开/关闭/聚焦X" → `list`查找窗口 → 确认 → 执行操作
2. 用户说"调整/移动X" → `list`查找窗口ID → `resize`/`move`
3. 用户说"发送/输入X到Y" → `activate`目标窗口 → `type`

**常见示例**:
- "打开记事本" → `process_manager.py start "gedit"`
- "关闭Chrome" → `window_manager.py list` → 查找Chrome → `window_manager.py close --title "Chrome"`
- "把微信调到前台" → `window_manager.py activate --title "WeChat"`
- "全屏当前窗口" → `window_manager.py maximize --title "..."`

### 2. Process Manager (`process_manager.py`)

列表、启动、停止和监控系统进程。

**功能**: list, kill, start, info, system

**决策流程**:
1. 用户说"查看进程" → `list` 或 `list --name`
2. 用户说"结束X进程" → `list --name X` → 确认 → `kill --name X`
3. 用户说"启动X" → `start "X"`
4. 用户说"系统状态" → `system`

**常见示例**:
- "有哪些程序在运行" → `process_manager.py system`
- "关掉所有gedit" → `process_manager.py kill --name gedit`
- "启动VS Code" → `process_manager.py start "code"`

### 3. Hardware Controller (`hardware_controller.py`)

通过Linux系统工具控制硬件设置。

**功能**:
- 音量: get, set, mute, unmute
- 屏幕: 亮度(get/set), 显示器信息
- 电源: lock, sleep, hibernate, shutdown, restart
- 网络: 列表网卡, 启用/禁用, WiFi扫描, 网络信息
- USB: 列出设备

**决策流程**:
1. 用户说"音量/声音" → 音量命令
2. 用户说"亮度/屏幕" → 屏幕/亮度命令
3. 用户说"关机/锁屏/睡眠" → 电源命令（**总是确认**）
4. 用户说"网络/WiFi" → 网络命令
5. 用户说"USB" → usb list

**常见示例**:
- "把音量调到50" → `hardware_controller.py volume set --level 50`
- "静音" → `hardware_controller.py volume mute`
- "屏幕调暗一点" → `hardware_controller.py screen brightness --level 30`
- "锁屏" → `hardware_controller.py power lock`
- "扫描WiFi" → `hardware_controller.py network wifi`

### 4. Serial Communication (`serial_comm.py`)

通过pyserial与Arduino、ESP32等串口设备通信。

**功能**: 列表端口, 检测波特率, 发送, 接收, 聊天, 监听

**决策流程**:
1. 用户说"串口/Arduino/tty" → 先`list`端口
2. 用户说"发送到Arduino" → `send --port /dev/ttyUSB0 --data "..."`
3. 用户说"读取传感器" → `chat --port /dev/ttyUSB0 --data "READ"`

**自动安装**: 首次使用时自动安装pyserial。

**常见示例**:
- "有哪些串口" → `serial_comm.py list`
- "给Arduino发指令开灯" → `serial_comm.py send --port /dev/ttyUSB0 --data "LED_ON"`
- "读取温度传感器" → `serial_comm.py chat --port /dev/ttyUSB0 --data "GET_TEMP"`
- "监听串口数据" → `serial_comm.py monitor --port /dev/ttyUSB0 --duration 30`

### 5. IoT Controller (`iot_controller.py`)

通过Home Assistant REST API、Mijia或通用HTTP端点控制智能家居设备。

**功能**:
- Home Assistant: 列出实体, 获取状态, 开启/关闭/切换, 调用任何服务
- 通用HTTP: GET, POST, PUT到任何REST端点
- Mijia: 设备发现指导

**决策流程**:
1. 用户提到"智能家居/Home Assistant/灯光/温度" → IoT命令
2. 用户说"控制设备/开关灯" → 需要用户提供URL和token
3. 用户说"调用API" → 通用HTTP命令

**自动安装**: 首次使用时自动安装requests。

**常见示例**:
- "列出所有智能设备" → `iot_controller.py homeassistant --url ... --token ... list`
- "打开客厅灯" → `iot_controller.py homeassistant --url ... --token ... on --entity-id light.living_room`
- "关掉卧室空调" → `iot_controller.py homeassistant --url ... --token ... off --entity-id climate.bedroom`
- "调用这个API" → `iot_controller.py http --url ... get --path ...`

### 6. GUI Controller (`gui_controller.py`)

完整的GUI自动化：鼠标控制、键盘输入、截图、OCR和视觉识别。

**功能**:
- 鼠标: 移动, 点击(左/右/双击), 拖拽, 滚动, 获取位置
- 键盘: 输入文本, 按热键, 按键组合
- 截图: 全屏, 区域, 活动窗口, 列出已保存截图
- OCR: 从屏幕区域提取文字（需要tesseract-ocr）
- 视觉: 在屏幕上查找图像模板, 点击图像, 按颜色查找, 获取像素颜色

**自动安装**: 首次使用时自动安装pyautogui和pillow。

**决策流程**:
1. 用户说"click/点击" → 确定位置(坐标/图像模板/颜色) → 点击
2. 用户说"type/输入文字" → `keyboard type --text "..."`
3. 用户说"screenshot/截图" → `screenshot full` 或 `screenshot active-window`
4. 用户说"read screen/OCR/识别文字" → 在相关区域 `visual ocr`
5. 用户说"find/查找图标" → `visual find --template "icon.png"`
6. 用户说"scroll/滚动" → `mouse scroll`
7. 用户说"drag/拖拽" → `mouse drag --start-x ... --start-y ... --end-x ... --end-y ...`

**常见示例**:
- "截图" → `gui_controller.py screenshot full`
- "截取当前窗口" → `gui_controller.py screenshot active-window`
- "鼠标移到(500,300)" → `gui_controller.py mouse move --x 500 --y 300`
- "点击(500,300)" → `gui_controller.py mouse click --x 500 --y 300`
- "右键点击" → `gui_controller.py mouse right-click --x 500 --y 300`
- "双击" → `gui_controller.py mouse double-click --x 500 --y 300`
- "拖拽文件从(100,200)到(500,400)" → `gui_controller.py mouse drag --start-x 100 --start-y 200 --end-x 500 --end-y 400`
- "向下滚动" → `gui_controller.py mouse scroll --direction down --clicks 10`
- "输入Hello World" → `gui_controller.py keyboard type --text "Hello World"`
- "按Ctrl+C" → `gui_controller.py keyboard press --keys "ctrl+c"`
- "按Alt+Tab" → `gui_controller.py keyboard press --keys "alt+tab"`
- "识别屏幕上的文字" → `gui_controller.py visual ocr`
- "识别(100,100,800,600)区域的文字" → `gui_controller.py visual ocr --x 100 --y 100 --width 800 --height 600`
- "在屏幕上找这个图标" → `gui_controller.py visual find --template "button.png"`
- "找到并点击这个图片" → `gui_controller.py visual click-image --template "submit.png"`
- "获取(200,200)位置的颜色" → `gui_controller.py visual pixel --x 200 --y 200`
- "获取鼠标位置" → `gui_controller.py mouse position`
- "获取屏幕分辨率" → `gui_controller.py screenshot size`

**安全规则**:
- 鼠标和键盘操作影响屏幕上的任何内容 - **不确定时先截图**
- 已启用**故障保护**：将鼠标移到任何屏幕角落将中止所有pyautogui操作
- OCR和图像识别是尽力而为 - 准确度取决于屏幕分辨率、语言和图像质量
- OCR最佳效果需要安装tesseract-ocr

## 处理未知设备

当用户请求控制未直接涵盖的设备或软件时：

1. **检查是否可以作为进程启动**: 使用 `process_manager.py start "app_name"`
2. **检查是否有窗口**: 使用 `window_manager.py list` 查找
3. **截图查看**: 使用 `gui_controller.py screenshot full` 查看屏幕内容
4. **使用OCR读取文字**: 使用 `gui_controller.py visual ocr` 从屏幕提取文字
5. **点击图像匹配**: 保存模板，然后 `gui_controller.py visual click-image --template icon.png`
6. **使用鼠标/键盘**: `gui_controller.py mouse click --x 100 --y 200` 直接控制
7. **检查是否有API**: 使用 `iot_controller.py http` 交互
8. **检查是否USB连接**: 使用 `hardware_controller.py usb list` 然后 `serial_comm.py list`
9. **建议替代方案**: 如果以上都不行，解释限制并建议自定义脚本

## 快速参考

详细命令语法，阅读 `references/command_reference.md`。

---
name: minimal-agent
description: >
  极简 AI 操作系统控制代理。通过执行协议驱动 system-controller 
  完成窗口管理、进程控制、硬件操作、GUI自动化、串口通信和IoT设备交互。
  当用户需要操控 Windows 系统（打开/关闭应用、调整音量亮度、
  截图OCR、管理进程、串口通信等）时使用此 Skill。
  触发词：打开应用、关闭窗口、调音量、调亮度、锁屏、关机、
  列出进程、发串口命令、控灯、连Arduino、开WiFi、USB设备、
  截屏、OCR、找图点击、输入文字、鼠标操作等。
---

# Minimal Agent — 极简操作系统控制代理

## 执行协议

执行协议等待指令：简单任务用自适应身份叠加输入处理输出结构基元执行，复杂任务分拆成简单任务交给基元构成链条执行，默认不展示输入处理输出细节但用户可以要求展示。优先根据提示词使用大语言模型完成任务，非必要不调用工具技能插件，把工具技能插件作为身份或基元进行规划调用。

## 架构

```
WorkBuddy（LLM 大脑 + 对话管理 + 模型配置）
    ↓ 加载本 Skill
minimal-agent SKILL.md（提示词 + 执行协议 + 能力说明）
    ↓ 调用脚本
system-controller scripts/（实际操作系统控制）
```

**核心原则**：
- 本 Agent 不自带 LLM，由 WorkBuddy 提供模型能力
- 本 Agent 不自建对话循环，由 WorkBuddy 管理上下文
- Agent 的职责 = 理解意图 → 选择正确的 system-controller 脚本 → 执行 → 返回结果
- **支持智能模式选择**，自动检测 system-controller 可用性

## 智能模式选择

### 6种运行模式
| 模式 | 说明 | 能力范围 | 适用场景 |
|------|------|---------|---------|
| `function`（V2） | Function Calling 结构化调用 | 限制在55个预定义工具内，只能调用system-controller脚本 | 生产环境，安全敏感场景 |
| `text`（V1） | LLM 生成文本命令，正则提取 | **无限制**，可执行任何系统命令（包括文件修改、脚本执行、网络操作、数据库操作等） | 开发/调试/运维，需要完全控制权的场景 |
| `auto`（推荐） | **智能检测**：有system-controller用V2，没有或不可用时用V1 | 自动适配 | 通用场景，无需手动切换 |
| `mixed`（高级） | **智能混合**：自动分析任务，V1和V2命令夹杂自由切换按顺序组合 | 智能适配 | 复杂多步骤任务，需要V1和V2模式组合 |
| `force_text` | 强制V1模式，无论是否有system-controller | 无限制 | 需要完全控制权，忽略system-controller |
| `force_function` | 强制V2模式，无论system-controller是否可用 | 限制在55个工具内 | 强制使用结构化调用，忽略可用性 |

### 模式切换与组合使用

Minimal Agent 支持**动态模式切换**和**组合使用**：

1. **动态切换**：在单次会话中可以通过命令切换模式
   ```bash
   # 启动时指定模式
   python agent.py --text --interactive
   python agent.py --function --interactive
   python agent.py --mixed --interactive
   
   # 会话中切换
   "切换到V2模式"
   "用V1模式执行这个文件操作"
   "切回自动模式"
   "使用混合模式处理这个复杂任务"
   ```

2. **组合使用**：V1和V2模式可以在单个复杂任务中组合
   ```bash
   # 执行复杂任务：硬件控制 + 文件操作 + 系统管理
   python agent.py --mixed "截屏后OCR文字，保存到文件，然后调整音量"
   ```

3. **智能适配**：
   - **auto模式**：自动根据system-controller可用性选择最佳模式
   - **mixed模式**：智能分析任务，V1和V2命令夹杂自由切换按顺序组合
   - 硬件控制、窗口管理 → 自动使用V2模式（如果可用）
   - 文件操作、脚本执行 → 自动使用V1模式（无限制）

### V1模式的无限制能力

在 **V1（text）模式** 下，Minimal Agent 可以执行**任何系统命令**，包括但不限于：

- **文件操作**：创建、删除、编辑、移动、复制文件
- **脚本执行**：运行 Python、PowerShell、Bash 脚本
- **网络操作**：HTTP请求、FTP传输、端口扫描
- **数据库操作**：SQL查询、数据导入导出
- **系统管理**：用户管理、服务控制、注册表编辑
- **软件安装**：安装程序、更新包管理
- **安全操作**：防火墙配置、权限管理

**示例**：
```bash
# V1模式可以执行任何命令
python agent.py --text "创建test.txt文件并写入内容"
python agent.py --text "运行Python脚本处理数据"
python agent.py --text "查询数据库并生成报告"
python agent.py --text "安装软件包并配置环境"
```

**V2模式**则专注于安全、可靠的硬件/软件控制，限制在55个预定义工具内。

### 模式优先级
1. **命令行参数**：`--text`、`--function`、`--auto`（最高优先级）
2. **配置文件**：`config.toml` 中的 `mode` 字段
3. **自动检测**：当 `mode = "auto"` 时自动检测 system-controller 可用性

### 智能检测逻辑
- **system-controller可用** → 使用 `function` 模式（V2）
- **system-controller不可用** → 使用 `text` 模式（V1）
- **不可用原因**：目录不存在、脚本缺失、Python环境不可用

## 使用示例

```bash
# 交互模式（自动检测）
python agent.py --interactive

# 交互模式（强制V1模式）
python agent.py --text --interactive

# 交互模式（强制V2模式）
python agent.py --function --interactive

# 单次命令模式（自动检测）
python agent.py "帮我打开记事本"

# 单次命令模式（强制V1模式）
python agent.py --text "dir C:\\"
python agent.py --text "echo Hello > test.txt"

# 单次命令模式（强制V2模式）
python agent.py --function window_list

# 工具调用模式
python agent.py window_list
python agent.py volume_set --level 50
python agent.py process_list --name "chrome"

# 配置模式切换：编辑 scripts/config.toml 中的 mode 字段
#   mode = "auto"      # 自动检测（推荐）
#   mode = "function"  # 强制V2模式
#   mode = "text"      # 强制V1模式
#   mode = "force_function"  # 强制V2模式，忽略可用性
#   mode = "force_text"      # 强制V1模式，忽略可用性
```

## 能力清单

### 窗口管理 (window_manager.py)
| 操作 | 命令 | 说明 |
|------|------|------|
| 列出窗口 | `list` | title, pid, process |
| 激活窗口 | `activate --title/pid` | 置于前台 |
| 关闭窗口 | `close --title/pid` | 关闭 |
| 最小化 | `minimize --title/pid` | 最小化 |
| 最大化 | `maximize --title/pid` | 最大化 |
| 调整大小位置 | `resize --pid --x --y --w --h` | 移动+缩放 |
| 发送按键 | `send-keys --title/pid --text` | 如 ENTER, ^c |

### 进程管理 (process_manager.py)
| 操作 | 命令 | 说明 |
|------|------|------|
| 列出进程 | `list [--name]` | 查找/列表 |
| 结束进程 | `kill --name/pid [--force]` | 终止 |
| 启动应用 | `start "命令" [--dir]` | 启动 |
| 进程详情 | `info --pid` | 详细信息 |
| 系统总览 | `system` | CPU/内存/磁盘 |

### 硬件控制 (hardware_controller.py)
| 操作 | 命令 | 说明 |
|------|------|------|
| 音量 | `volume get/set --level / mute` | 音量控制 |
| 亮度 | `screen brightness [--level] / info` | 显示器亮度 |
| 电源 | `power lock/sleep/hibernate/shutdown/restart/cancel` | 电源管理 |
| 网络 | `network adapters/enable/disable --name/wifi/info` | 网络适配器 |
| USB | `usb list` | USB 设备列表 |

### GUI 控制 (gui_controller.py)
| 操作 | 命令 | 说明 |
|------|------|------|
| 鼠标移动 | `mouse move --x --y` | 定位 |
| 鼠标点击 | `mouse click/right-click/double-click --x --y` | 点击 |
| 鼠标拖拽 | `mouse drag --start-x --start-y --end-x --end-y` | 拖动 |
| 鼠标滚动 | `mouse scroll --direction up/down --clicks` | 滚轮 |
| 鼠标位置 | `mouse position` | 获取坐标 |
| 键盘输入 | `keyboard type --text` | 文字输入 |
| 键盘按键 | `keyboard press --keys` | 如 ctrl+c, alt+tab |
| 截图 | `screenshot full/active-window/size` | 屏幕截图 |
| OCR识别 | `visual ocr [--x --y --w --h]` | 文字识别 |
| 图像匹配 | `visual find --template "img.png"` | 找图 |
| 图像点击 | `visual click-image --template "img.png"` | 找图并点 |
| 取像素色 | `visual pixel --x --y` | 颜色值 |

### 串口通信 (serial_comm.py)
| 操作 | 命令 | 说明 |
|------|------|------|
| 列出端口 | `list` | 可用串口 |
| 发送数据 | `send --port COMx --data "..."` | 发送 |
| 接收数据 | `receive --port COMx` | 接收 |
| 交互模式 | `chat/monitor --port COMx --data "..."` | 持续通信 |

### IoT 控制 (iot_controller.py)
| 操作 | 命令 | 说明 |
|------|------|------|
| HomeAssistant | `homeassistant --url --token list/state/on/off/toggle/entity-id` | 智能家居 |
| HTTP API | `http --url get/post/put --path` | 通用HTTP请求 |

## 执行规则

1. **先查询后操作**：list/find → 再执行动作
2. **危险操作必须确认**：关机、杀进程、关闭窗口、禁用网络前需说明并等待确认
3. **返回简洁结果**：只报告关键信息
4. **失败时分析原因**：给出替代方案
5. **支持复合任务**：可组合多个步骤完成复杂需求
6. **支持撤销回滚**：用户说"撤销"/"回滚"时反向执行

## 能力总结

Minimal Agent 具备**完整的能力栈**：

### 1. **硬件/软件控制能力**（V2模式，55个工具）
   - **窗口管理**：控制应用窗口
   - **进程管理**：管理系统进程
   - **硬件控制**：调节音量、亮度、电源
   - **GUI自动化**：鼠标、键盘、截图、OCR
   - **串口通信**：与硬件设备通信
   - **IoT控制**：智能家居、HTTP API

### 2. **无限制系统命令能力**（V1模式）
   - **文件操作**：创建、删除、编辑、移动文件
   - **脚本执行**：运行任何脚本（Python、Bash、PowerShell）
   - **网络操作**：HTTP请求、FTP、端口扫描
   - **数据库操作**：SQL查询、数据导入导出
   - **系统管理**：用户管理、服务控制、注册表
   - **软件安装**：安装、配置、更新软件
   - **安全操作**：防火墙、权限管理
   - **开发工具**：编译、构建、测试
   - **数据操作**：处理CSV、JSON、XML文件
   - **任何其他可以通过命令行完成的任务**

### 3. **智能模式切换**（V1+V2组合）
   - **动态切换**：会话中随时切换模式
   - **组合使用**：单个任务中混合使用V1和V2
   - **智能适配**：auto模式自动选择最佳模式

### 4. **关键优势**
   - **V2模式**：安全、可靠、结构化，适合生产环境
   - **V1模式**：无限制、灵活、强大，适合开发运维
   - **双模式**：两者兼得，根据需求选择
   - **自动检测**：无需手动配置，智能选择最佳模式

**一句话总结**：Minimal Agent 能通过V1模式**做任何可以通过命令行完成的事情**，同时通过V2模式**安全可靠地控制硬件软件**，并支持**智能切换和组合使用**。

## 依赖

- **system-controller Skill**：`~/.workbuddy/skills/system-controller/`
- **Python 3.x**：Managed runtime（WorkBuddy 自动提供）

## 下载安装 system-controller

Minimal Agent 需要 system-controller 来实现完整的硬件/软件控制能力：

1. **官方安装（推荐）**：
   - 从腾讯云技能市场安装：https://skillhub.tencent.com/skills/system-controller
   - 通过 WorkBuddy 技能中心搜索 "system-controller"

2. **GitHub 安装**：
   ```bash
   # 克隆到 WorkBuddy 技能目录
   git clone https://github.com/clawhub/wangjiaocheng/system-controller.git ~/.workbuddy/skills/system-controller
   
   # 或者从镜像站
   git clone https://clawhub.ai/wangjiaocheng/system-controller ~/.workbuddy/skills/system-controller
   ```

3. **手动安装**：
   - 下载：https://clawhub.ai/wangjiaocheng/system-controller/archive/main.zip
   - 解压到：`~/.workbuddy/skills/system-controller/`

## Python 路径

```python
# 基础脚本（无额外依赖）
PYTHON = r"C:\Users\wave\.workbuddy\binaries\python\versions\3.13.12\python.exe"

# GUI 脚本（需要 pyautogui/pillow，使用 venv）
PYTHON_VENV = r"C:\Users\wave\.workbuddy\binaries\python\envs\default\Scripts\python.exe"
```

## 脚本路径

所有 system-controller 脚本位于：
```
~/.workbuddy/skills/system-controller/scripts/
```

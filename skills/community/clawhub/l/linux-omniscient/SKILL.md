---
name: omniscient
author: 王教成 Wang Jiaocheng (波动几何)
description: >
  全知全能技能 — 整合认知套件、执行框架、系统控制三大能力层，并配备编排引擎。
  认知层：四种思维操作码（直用/改进/迁移/构建）覆盖所有思考任务；
  执行层：大语言模型 + 命令执行工具，自动化代码生成与脚本执行；
  操控层：Linux桌面软件、系统硬件、串口设备、物联网平台、图形界面自动化、蓝牙设备、GPU显卡、存储磁盘、电池电源、音频设备、显示器、温度风扇、打印机、摄像头；
  编排引擎：将所有操作统一为基元，自由组合为任意复杂度的执行链条。
  此技能应用于任何任务，无例外。
dependency:
  python:
    - psutil>=5.9.0
    - pycaw>=2023.3
    - comtypes>=1.2.0
    - sounddevice>=0.4.6
    - pyautogui>=0.9.54
    - pytesseract>=0.3.10
    - Pillow>=10.0.0
    - pyserial>=3.5
    - requests>=2.31.0
    - bleak>=0.21.0
    - opencv-python>=4.8.0
    - numpy>=1.24.0
  system:
    - apt-get update && apt-get install -y x11-utils wmctrl xdotool alsa-utils pulseaudio-utils lm-sensors upower sane-utils
---

# 全知全能技能

认知套件（想）+ 执行框架（编程做）+ 系统控制（操控做），覆盖所有类型的任务。

所有操作类型——脚本命令、代码生成、工具调用、技能插件、纯认知输出——均为统一基元，可由编排引擎自由组合为任意复杂度的执行链条。

## 架构总览

```
                    ┌─────────────────────────────────┐
                    │          用户请求                 │
                    └──────────────┬──────────────────┘
                                   ↓
                    ┌──────────────────────────────────┐
                    │        任务路由器                  │
                    │  判断任务类型 → 选择执行层         │
                    └──────┬──────────┬──────────┬─────┘
                           ↓          ↓          ↓
              ┌────────────┐  ┌──────────────┐  ┌──────────────┐
              │  认知层     │  │  编程执行层   │  │  系统操控层   │
              └────────────┘  └──────────────┘  └──────────────┘
              纯大语言模型   大语言模型+命令   调用专用脚本
                            执行工具
                           ─────────────────────────────────
                    ┌──────────────────────────────────┐
                    │        编排引擎                    │
                    │  将三层的任意原子操作              │
                    │  组合为执行链条                    │
                    └──────────────────────────────────┘
```

三层各有所长，按任务主要操作类型选择入口：
- **认知为主** → 认知层（模式提示词套件 + 大语言模型）
- **代码执行为主** → 编程执行层（大语言模型 + 命令执行工具）
- **系统操控为主** → 系统操控层（专用 Python 脚本）

**超级任务**（跨层、多步骤、复杂编排）→ 编排引擎调度三层原子操作构成执行链条。

---

## 任务路由器

加载本技能后，按以下逻辑自动判断任务类型并选择执行层：

```
收到用户任务
    │
    ├─ 涉及多种操作类型或超多步骤？ ──→ 编排引擎
    │   （跨层组合、命令序列、自动化流水线...）
    │
    ├─ 需要操控电脑/硬件/设备？ ──→ 第三层：系统控制
    │   （开关窗口、调音量、截图、点鼠标、串口、物联网、蓝牙、GPU、磁盘、电池、音频、显示器、温度、打印机、摄像头...）
    │
    ├─ 需要写代码/跑脚本？ ──→ 第二层：执行框架
    │   （数据处理、文件操作、接口调用、构建应用...）
    │
    └─ 分析/思考/创作？ ──→ 第一层：认知套件
        （写作、分析、推理、规划、翻译、总结...）
```

**混合任务**（如"写个脚本帮我批量处理图片然后调低亮度"）：
1. 先用第一层构思方案
2. 再用第二层写脚本执行
3. 最后用第三层调硬件参数（如需）

**注意**：所有层和引擎可自由组合，不必非此即彼。路由器只是默认起点，可根据任务需要自动跨层调度。

---

## 编排引擎

将三层的任意原子操作统一为基元，组合为执行链条，实现超级复杂、超多步骤的任务。

### 基元定义

所有可执行的操作均为原子基元，共五类：

| 类别 | 来源 | 示例 |
|------|------|------|
| 脚本命令基元 | 第三层十八大模块 | `window_manager.py list`、`process_manager.py start`、`hardware_controller.py volume set --level 50`、`network_controller.py adapter list`、`input_controller.py all`、`gpu_controller.py monitor`、`storage_controller.py list`、`battery_controller.py status`、`audio_controller.py devices`、`display_controller.py info`、`thermal_controller.py status`、`serial_comm.py list`、`bluetooth_controller.py info`、`iot_controller.py homeassistant on --entity-id light.xxx`、`printer_controller.py list`、`scanner_controller.py list`、`camera_controller.py list`、`gui_controller.py screenshot full` |
| 代码执行基元 | 第二层执行框架 | 大语言模型即时生成的 Python 脚本、命令行指令 |
| 工具调用基元 | 宿主环境内置工具 | 文件读写、命令执行、搜索、网页访问等 |
| 技能插件基元 | 已安装的其他技能 | 通过 `use_skill` 加载的外部技能能力 |
| 认知输出基元 | 第一层四种模式 | 大语言模型直接生成的分析、文案、方案、推理结果 |

### 编排协议

基于模式直用提示词的核心机制——"复杂任务分拆成简单任务交给基元构成链条执行"——扩展为完整的多步编排协议：

```
1. 拆解
   大语言模型将用户任务拆解为有序的基元序列。
   每个基元标注类别（脚本/代码/工具/插件/认知）和预期输出。

2. 规划
   确定基元之间的依赖关系和数据流向。
   前序基元的输出可作为后序基元的输入。

3. 执行
   按序执行每个基元，实时检查输出是否符合预期。
   每个基元执行后，大语言模型判断是否需要调整后续步骤。

4. 修复
   任一基元执行失败时，大语言模型分析错误原因，
   自主选择：重试当前基元 / 替换为等价基元 / 调整后续计划 / 终止并报告。

5. 汇总
   所有基元执行完毕后，将整体结果汇总为人类可读的输出。
```

### 编排规则

- **优先使用大语言模型**：能用认知输出基元解决的步骤，不生成代码；能用单条命令解决的，不写脚本。
- **安全规则贯穿**：编排链中的每个基元都受第二层安全机制约束，高危操作必须用户确认。
- **智能插桩**：可在基元之间插入认知输出基元做中间判断（如"分析上一步输出，决定下一步怎么做"）。
- **条件分支**：支持"如果…则…"逻辑——大语言模型根据中间结果动态选择后续基元。
- **循环迭代**：支持"重复执行直到…"逻辑——大语言模型判断循环条件并控制迭代。
- **并行编排**：无依赖关系的基元可并行发起，减少总耗时。
- **可中断恢复**：超长任务可设置检查点，支持从断点恢复。

### 编排示例

**示例1：自动化办公流水线（3层联动）**
```
任务："打开Excel，读取A列数据，生成每行的汇总报告，保存到桌面，然后调低屏幕亮度"
基元序列：
  [脚本] window_manager.py activate --title "Excel"        ← 第三层
  [脚本] gui_controller.py screenshot full                  ← 第三层（确认状态）
  [认知] 识别Excel内容，规划读取方案                          ← 第一层
  [代码] Python脚本读取Excel数据并生成报告                    ← 第二层
  [工具] 保存文件到桌面                                      ← 工具基元
  [脚本] hardware_controller.py screen brightness --level 30 ← 第三层
```

**示例2：智能设备联动（生成代码 + 脚本编排）**
```
任务："监测串口传感器温度，超过阈值自动发微信通知并开风扇"
基元序列：
  [脚本] serial_comm.py list                                ← 第三层（确认端口）
  [代码] 生成Python监听脚本：读取串口 + 阈值判断              ← 第二层
  [脚本] iot_controller.py homeassistant on --entity-id switch.fan ← 第三层
  [代码] 生成通知逻辑：超限时触发微信提醒                      ← 第二层
```

**示例3：研究分析全链路（认知 + 工具 + 代码）**
```
任务："调研三篇论文的核心观点，生成对比表格，再做成可视化图表"
基元序列：
  [工具] 网页搜索并获取三篇论文内容                            ← 工具基元
  [认知] 模式直用：提取每篇论文核心观点                         ← 第一层
  [认知] 模式改进：对比分析，找出异同                           ← 第一层
  [工具] 生成对比表格Markdown                                  ← 工具基元
  [代码] 生成Python可视化图表脚本并执行                        ← 第二层
```

---

## 第一层：认知套件

四种思维操作码，覆盖所有认知任务。根据任务性质选择对应模式。未指定模式时，默认使用**直用模式**。

### 模式直用（精确执行明确任务）

> 执行协议等待指令：简单任务用自适应身份叠加输入处理输出结构基元执行，复杂任务分拆成简单任务交给基元构成链条执行，默认不展示输入处理输出细节但用户可以要求展示。优先根据提示词使用大语言模型完成任务，非必要不调用工具技能插件，把工具技能插件作为身份或基元进行规划调用。

**基元范围**：此处的"基元"不限于纯认知输出，而是涵盖编排引擎定义的全部五类基元——脚本命令、代码执行、工具调用、技能插件、认知输出。大语言模型根据任务需要将任意类别的基元纳入执行链条。

**适用场景**：用户有明确目标，需要精确执行。如翻译、总结、格式转换、数据分析、文档撰写、自动化流水线、跨层多步任务等。

### 模式改进（优化已有方案）

> 按需生成新方案自选创新元框架：第一性原理、逆向思维、辩证综合、随机性驱动、涌现生成、演化迭代、系统动力学、约束驱动、故事叙述和游戏化。

**适用场景**：优化/改进/升级现有方案。如重构代码、改进文案、优化流程、升级设计等。

### 模式迁移（跨领域模式搬移）

> 作为模式转换器分析提供的旧具体事物的底层结构与原理（得到抽象模式）运用到指定的新具体事物（生成全新的具体方案）。

**适用场景**：把 A 领域的成功模式搬到 B 领域。如把游戏化机制应用到教育、把电商推荐逻辑应用到内容分发等。

### 模式构建（从零创造）

> 作为可能性空间导航器把两个概念解构成基本维度建立维度矩阵随机选择看似无关的维度组合强制连接推导可能性发展（评估逻辑距离形成可能性集群识别无人探索区域）输出最有潜力最激进最被忽视可能性（生成几个反常识方案）。

**适用场景**：从零探索全新方向。如创新产品设计、新商业模式、前沿技术方案等。

---

## 第二层：执行框架

基于"大语言模型 + 命令执行工具"架构的自动化执行协议。无需密钥，无需额外配置，开箱即用。

### 四步工作流

```
思考 → 执行 → 修复 → 总结
```

1. **思考** — 大语言模型理解任务意图，判断复杂度，决定生成命令行指令还是 Python 脚本
2. **执行** — 写入文件 → 执行命令/脚本 → 捕获输出
3. **修复** — 出错时大语言模型分析错误、自动修复代码、重试（最多2次）
4. **总结** — 将技术输出翻译成人类可读的自然语言结果

### 能力范围

| 能力 | 描述 |
|------|------|
| 命令行指令 | 文件操作、进程管理、系统管理 |
| Python 脚本 | 数据处理、网络爬虫、机器学习、图像处理 |
| 命令行工具 | git、docker、ffmpeg、aws 等任意工具 |
| 接口调用 | 任意 HTTP 接口 |

**核心原理**：命令执行工具能运行脚本 → 脚本能覆盖所有代码执行类任务。

### 安全机制

| 级别 | 示例 | 处理方式 |
|------|------|----------|
| 🔴 高危 | `rm -rf /`、`format C:` | **必须用户确认** |
| 🟡 中危 | `pip uninstall`、`sudo` | 警告提示 |
| 🟢 低危 | `ls`、`cat`、`python script.py` | 直接执行 |

---

## 第三层：系统控制

通过专用 Python 脚本统一控制 Linux 桌面软件、系统硬件、串口设备和物联网平台。

### 运行环境

- **Python 路径**: `python3` 或 `/usr/bin/python3`
- **脚本目录**: `scripts/`
- **执行模式**: 始终使用命令执行工具运行脚本

若虚拟环境不存在，先创建：
```
python3 -m venv ~/.venv/omniscient
~/.venv/omniscient/bin/pip install psutil pyautogui pillow pyserial requests bleak sounddevice opencv-python pytesseract
```

### 十八大控制模块

| 模块 | 脚本 | 覆盖范围 |
|------|------|----------|
| 窗口管理 | `window_manager.py` | 桌面窗口控制：列表、激活、关闭、最小化、最大化、调整大小、发送按键 |
| 进程管理 | `process_manager.py` | 系统进程：列表、启动、详情、终止、系统概览 |
| 硬件控制 | `hardware_controller.py` | 音量/亮度/电源/USB |
| 网络与WiFi管理 | `network_controller.py` | 网卡管理/WiFi扫描连接/DNS配置/代理设置/连通性测试 |
| GPU监控与控制 | `gpu_controller.py` | GPU信息/实时监控/显存/温度/功耗/频率/进程占用/功耗模式设置（需nvidia-smi） |
| 存储磁盘管理 | `storage_controller.py` | 磁盘列表/详情/健康/大文件扫描/文件夹分析/分区映射（自动安装 psutil） |
| 电池与电源计划 | `battery_controller.py` | 电池状态/电量/健康度/电源计划切换/电池报告（自动安装 psutil） |
| 音频设备管理 | `audio_controller.py` | 设备列表/输出输入切换/音量控制/麦克风录音（自动安装 pycaw+sounddevice） |
| 显示器管理 | `display_controller.py` | 显示器信息/多屏布局/DPI缩放/夜间模式/屏幕方向 |
| 温度与风扇监控 | `thermal_controller.py` | CPU/GPU温度/风扇转速/实时监控（自动安装 psutil；详细温度需 OpenHardwareMonitor） |
| 输入设备枚举 | `input_controller.py` | 键盘/鼠标/游戏手柄设备列表 |
| 串口通信 | `serial_comm.py` | Arduino/ESP32/串口设备（自动安装 pyserial） |
| 蓝牙控制 | `bluetooth_controller.py` | 蓝牙适配器/已配对设备/BLE扫描/服务发现/连接管理（BLE需 bleak） |
| 物联网控制 | `iot_controller.py` | Home Assistant/HTTP 接口/智能家居（自动安装 requests） |
| 打印机管理 | `printer_controller.py` | 打印机列表/默认打印机/打印队列/取消任务/打印机能力 |
| 扫描仪管理 | `scanner_controller.py` | 扫描仪列表/设备详情/WIA服务状态 |
| 摄像头管理 | `camera_controller.py` | 摄像头列表/摄像头参数/拍照（自动安装 opencv-python-headless） |
| 图形界面自动化 | `gui_controller.py` | 鼠标/键盘/截图/文字识别/图像识别（自动安装 pyautogui+pillow） |

所有脚本独立运行，无互相依赖。

### 安全规则

1. **破坏性操作必须用户确认**（关机、重启、杀进程、关窗口、禁用网卡）
2. **先查询再操作**（先 `list` 再 `close`，先 `list --name` 再 `kill`）
3. **电源操作需警告**（关机/重启/睡眠/休眠前必须确认）
4. **禁用网络适配器需用户确认**（脚本通过确认机制保护，防止意外断网）
5. **串口操作先列出端口确认**

### 模块调用示例

**窗口管理**:
- "关闭Chrome" → `window_manager.py list` → 找到 Chrome → `window_manager.py close --title "Chrome"`
- "把微信调到前台" → `window_manager.py activate --title "微信"`

**进程管理**:
- "启动VS Code" → `process_manager.py start "code"`
- "关掉所有记事本" → `process_manager.py kill --name notepad`

**硬件控制**:
- "把音量调到50" → `hardware_controller.py volume set --level 50`
- "锁屏" → `hardware_controller.py power lock`

**网络管理**:
- "扫描WiFi" → `network_controller.py wifi scan`
- "连接WiFi" → `network_controller.py wifi connect --ssid "MyWiFi" --password "xxx"`
- "设置DNS" → `network_controller.py dns set --adapter "WiFi" --servers "8.8.8.8,8.8.4.4"`
- "网络延迟" → `network_controller.py connectivity ping --host baidu.com`

**输入设备**:
- "有哪些键盘" → `input_controller.py keyboards`
- "鼠标设备" → `input_controller.py mice`
- "游戏手柄" → `input_controller.py gamepads`

**GPU监控**:
- "显卡状态" → `gpu_controller.py info`
- "实时监控GPU" → `gpu_controller.py monitor --interval 2 --count 5`
- "切换高性能模式" → `gpu_controller.py set-power performance`

**存储管理**:
- "磁盘空间" → `storage_controller.py list`
- "大文件" → `storage_controller.py big-files --top 30`
- "文件夹大小" → `storage_controller.py usage --path "C:\Users"`

**电池管理**:
- "电池状态" → `battery_controller.py status`
- "切换电源计划" → `battery_controller.py set-plan --name "高性能"`

**音频控制**:
- "切换耳机" → `audio_controller.py set-default --name "耳机"`
- "音量调到70" → `audio_controller.py volume set --level 70`
- "录音10秒" → `audio_controller.py record --duration 10`

**显示器管理**:
- "显示器信息" → `display_controller.py info`
- "多屏布局" → `display_controller.py layout`
- "夜间模式" → `display_controller.py night-light on`

**温度监控**:
- "系统温度" → `thermal_controller.py status`
- "实时监控" → `thermal_controller.py monitor`

**串口通信**:
- "有哪些串口" → `serial_comm.py list`
- "给Arduino发指令开灯" → `serial_comm.py send --port COM3 --data "LED_ON"`

**蓝牙控制**:
- "有哪些蓝牙设备" → `bluetooth_controller.py paired`
- "扫描附近蓝牙" → `bluetooth_controller.py list --timeout 10`
- "连接蓝牙耳机" → `bluetooth_controller.py connect AA:BB:CC:DD:EE:FF`

**物联网控制**:
- "打开客厅灯" → `iot_controller.py homeassistant --url ... --token ... on --entity-id light.living_room`

**打印机管理**:
- "查看打印机" → `printer_controller.py list`
- "设置默认打印机" → `printer_controller.py set-default --name "HP"`

**摄像头操作**:
- "有哪些摄像头" → `camera_controller.py list`
- "拍张照" → `camera_controller.py capture`

**图形界面自动化**:
- "截图" → `gui_controller.py screenshot full`
- "点击(500,300)" → `gui_controller.py mouse click --x 500 --y 300`
- "输入Hello World" → `gui_controller.py keyboard type --text "Hello World"`
- "识别屏幕上的文字" → `gui_controller.py visual ocr`

### 未知设备处理流程

1. 检查能否作为进程启动 → `process_manager.py start`
2. 检查是否有窗口 → `window_manager.py list`
3. 截图查看 → `gui_controller.py screenshot full`
4. 文字识别 → `gui_controller.py visual ocr`
5. 图像匹配点击 → `gui_controller.py visual click-image --template "icon.png"`
6. 鼠标键盘直接操控 → `gui_controller.py mouse click`
7. 检查是否有接口 → `iot_controller.py http`
8. 检查 USB 连接 → `hardware_controller.py usb list` → `serial_comm.py list`
9. 检查打印机 → `printer_controller.py list`
10. 检查摄像头 → `camera_controller.py list`
11. 建议替代方案 → MCP 服务或自定义脚本

详细命令语法见 `references/command_reference.md`。脚本安全审查清单见 `references/security_checklist.md`，当需要审计或新增脚本时参照执行。

---
name: mijia-controller
description: 米家智能家居设备控制技能包。通过 mijiaAPI 驱动，支持查询设备状态、控制设备属性、运行场景等。当用户请求控制智能家居设备、查询温湿度/电量/开关状态时使用。
---

# 米家智能家居控制 / Mijia Smart Home Controller (中文/English)

通用型 AI 代理技能包，通过 mijiaAPI 驱动控制小米/米家智能设备。
A universal AI agent skill pack for controlling Xiaomi/Mijia smart devices via mijiaAPI.

> 不仅支持 Claude（通过 Agent Skills），也支持任何能够读取本地文件、执行 Python/CLI 的 AI 助理（如 GitHub Copilot, Cursor, Open Interpreter 等）。
> Supports not only Claude (via Agent Skills) but any AI assistant that can read local files and execute Python/CLI commands (e.g., GitHub Copilot, Cursor, Open Interpreter).

## 前置依赖 / Dependencies

- Python 3.10+
- 所有依赖已安装在当前环境 / All dependencies already installed:
  - `mijiaAPI==3.0.5` （已安装 / installed）
  - `pillow`, `pycryptodome`, `qrcode`, `requests`, `tzlocal`（已安装 / installed）
- 米家账号已登录认证 / Mijia account already authenticated
  - 认证文件位置 / Auth file: `C:\Users\abc15\.config\mijia-api\auth.json`
  - 备用登录：`python -m mijiaAPI -l`（扫码登录 / QR code login）

## 📁 目录结构 / File Structure

```
mijia-controller/
├── SKILL.md                    # 技能入口 / Skill entry (本文件 / this file)
├── instructions.md             # 标准作业程序 / SOP for the agent
├── requirements.txt            # Python 依赖 / Python dependencies
├── reference/
│   └── device_catalogs.md      # 设备 MIoT 属性映射 / Device MIoT property mappings
└── scripts/
    ├── setup_env.py            # 环境检查 / Environment check
    ├── list_devices.py         # 设备列表 / Device list snapshot
    └── control_device.py       # 属性读取/设置 / Property read/set
```

## 🛠️ 快速开始 / Quick Start

```bash
# 1. 环境检查 / Environment check
python scripts/setup_env.py

# 2. 列出所有设备 / List all devices
python scripts/list_devices.py

# 3. 控制设备 / Control device
python scripts/control_device.py --did "设备DID/device DID" --siid 2 --piid 1 --value 1
```

## 🚀 使用方法 / Usage

当你与 AI 助理交流并提及以下内容时，它会自动触发：
When you mention the following to an AI assistant, it will auto-trigger:

- "帮我列出我家里现在的设备状态 / List my home device status"
- "打开/关闭插座 / Turn on/off the smart plug"
- "看看温度是多少 / Check the temperature"
- "执行扫除场景 / Run the cleaning scene"

## ⚠️ 注意事项 / Notes

- **自愈机制 / Self-healing**: 如果环境未准备好，助理会根据 `setup_env.py` 反馈自动引导安装/登录
- **安全性 / Security**: 涉及开锁、摄像头等敏感操作时，助理会要求你二次口头确认 / For sensitive operations (lock, camera), assistant will ask for verbal confirmation

## 可用命令 / Available CLI Commands

```bash
# 列出家庭和设备 / List homes and devices
python -m mijiaAPI --list_homes

# 列出场景 / List scenes
python -m mijiaAPI --list_scenes

# 列出耗材 / List consumables (battery, etc.)
python -m mijiaAPI --list_consumable_items

# 运行场景 / Run scene
python -m mijiaAPI --run_scene "场景名称/Scene Name"

# 获取设备 MIoT 信息 / Get device MIoT info
python scripts/control_device.py --did "DID" --info

# 获取设备属性 / Get device property
python scripts/control_device.py --did "DID" --prop "power"

# 按名称获取属性 / Get by device name
python scripts/control_device.py --name "灯" --prop "power"

# 设置设备属性 / Set device property
python scripts/control_device.py --did "DID" --prop "power" --value 1
```

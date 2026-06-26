---
name: openclaw-omni-expert
description: OpenClaw全能专家系统；支持多种远程软件(UU/RustDesk/ToDesk/向日葵/RDP)、一键安装、TOP3专家诊断、全自动驾驶、Agent/Workflow编排、工具链配置、记忆系统、插件开发、监控运维、100+实战案例库和故障排查手册；用户说"安装 OpenClaw"、"配置 OpenClaw"、"诊断 OpenClaw 问题"、"创建 Agent"、"编排 Workflow"、"远程控制电脑"、"用鼠标操作"时使用
dependency:
  python:
    - paramiko>=2.11.0
---

# OpenClaw全能专家系统 v7.0

## 核心能力

| 能力 | 说明 |
|------|------|
| **多远程软件支持** | UU/RustDesk/ToDesk/向日葵/RDP/WinRM 统一接口 |
| **远程桌面控制** | 屏幕捕获、鼠标键盘控制 |
| **视觉智能识别** | GPT-4V/本地OCR、UI元素定位、自动化点击 |
| **全自动驾驶** | 一键连接、一键安装、一键诊断、全程无人干预 |
| **TOP3 专家** | 第一性原理 + 熵减思维 + 最优路径算法 |
| **Agent编排** | 10+ 节点类型、5 种 Workflow 模式 |
| **工具链专家** | 10+ 内置工具、自定义工具开发 |
| **监控运维** | 日志配置、健康检查、告警、备份 |
| **案例库** | 100+ 实战案例 |
| **故障库** | 60+ 常见故障 |

## 触发条件

- 用户要求"安装 OpenClaw"、"配置 OpenClaw"
- 用户要求"诊断 OpenClaw 问题"
- 用户要求"创建 Agent"或"编排 Workflow"
- 用户要求"远程控制电脑"、"用鼠标操作"、"帮我点一下"
- 用户提到具体的远程软件名称（UU、RustDesk 等）

---

## Phase 0: 多远程软件控制

### 支持的软件对比

```
┌──────────────────────────────────────────────────────────────────┐
│                     远程软件自动化能力对比                         │
├────────────┬────────┬────────┬────────┬────────┬────────┬───────┤
│ 软件       │ 鼠标   │ 键盘   │ 截图   │ 文件   │ 命令   │ 视觉  │
├────────────┼────────┼────────┼────────┼────────┼────────┼───────┤
│ UU远程     │   ✅   │   ✅   │   ✅   │   ✅   │   ✅   │   ✅  │
│ RustDesk   │   ⚠️   │   ⚠️   │   ✅   │   ✅   │   ✅   │   ✅  │
│ ToDesk     │   ⚠️   │   ⚠️   │   ✅   │   ✅   │   ❌   │   ✅  │
│ 向日葵     │   ⚠️   │   ⚠️   │   ✅   │   ✅   │   ❌   │   ✅  │
│ RDP        │   ❌   │   ❌   │   ✅   │   ✅   │   ✅   │   ✅  │
│ WinRM      │   ❌   │   ❌   │   ❌   │   ✅   │   ✅   │   ❌   │
└────────────┴────────┴────────┴────────┴────────┴────────┴───────┘
✅ 完全支持  ⚠️ 需配合PyAutoGUI  ❌ 不支持
```

### 检测已安装软件

```bash
# 检测可用的远程软件
python3 scripts/universal_remote.py --detect
```

**输出示例:**
```
已安装:
  - uu
    鼠标控制: ✓
    键盘控制: ✓
    截图: ✓
    文件传输: ✓
    命令执行: ✓
    视觉识别: ✓
  - rustdesk
    鼠标控制: ✗
    键盘控制: ✗
    ...
```

### 通用连接方式

```bash
# UU 远程
python3 scripts/universal_remote.py --software uu --session-id 123456789

# RustDesk
python3 scripts/universal_remote.py --software rustdesk --remote-id 12345-abc-67890

# ToDesk
python3 scripts/universal_remote.py --software todesk --session-id xxxxxxxx

# 向日葵
python3 scripts/universal_remote.py --software sunlogin --host 192.168.1.100

# RDP
python3 scripts/universal_remote.py --software rdp --host 192.168.1.100

# WinRM
python3 scripts/universal_remote.py --software winrm --host 192.168.1.100 --username admin
```

---

## Phase 1: UU远程（完整支持）

### 连接方式

```bash
# Session ID 连接
python3 scripts/remote_desktop_control.py --session-id 123456789 --interactive

# 主机连接
python3 scripts/remote_desktop_control.py --host 192.168.1.100 --port 18792 --interactive
```

### 鼠标键盘控制

```bash
# 移动鼠标
python3 scripts/remote_automation.py --action move --x 500 --y 300

# 点击/双击/右键
python3 scripts/remote_automation.py --action click --x 500 --y 300
python3 scripts/remote_automation.py --action double-click --x 500 --y 300
python3 scripts/remote_automation.py --action right-click --x 500 --y 300

# 输入文本
python3 scripts/remote_automation.py --action type --text "Hello"

# 按键/组合键
python3 scripts/remote_automation.py --action press --key enter
python3 scripts/remote_automation.py --action hotkey --keys ctrl c
```

---

## Phase 2: RustDesk（开源免费）

### 安装与配置

```bash
# 安装 RustDesk
# Windows: 下载 https://github.com/rustdesk/rustdesk/releases
# Linux: cargo install rustdesk

# 获取本机 ID
python3 scripts/rustdesk_control.py --get-id

# 设置密码
python3 scripts/rustdesk_control.py --set-password MYPASSWORD
```

### 连接方式

```bash
# 通过 ID 连接
python3 scripts/rustdesk_control.py --id 12345-abcdef-67890 --password MYPASSWORD

# 通过主机连接
python3 scripts/rustdesk_control.py --host 192.168.1.100 --port 21117

# 自建中继服务器
python3 scripts/rustdesk_control.py --id <remote_id> --relay your-relay.com
```

### 文件传输

```bash
# 上传文件
python3 scripts/rustdesk_control.py --host 192.168.1.100 --upload ./local.txt /tmp/remote.txt

# 下载文件
python3 scripts/rustdesk_control.py --host 192.168.1.100 --download /tmp/remote.txt ./local.txt
```

---

## Phase 3: 其他远程软件

### ToDesk

```bash
# CLI 连接
todesk -c <device_id> -p <password>

# 文件传输
todesk -transfer <local> <remote>
```

### 向日葵

```bash
# CLI 连接
sunlogin --control <host> --pwd <password>

# 文件传输
sunlogin --file <local> <remote>
```

### RDP (Windows 原生)

```bash
# 连接
mstsc /v:192.168.1.100

# 带用户名
mstsc /v:192.168.1.100 /u:admin
```

### WinRM (无 GUI)

```bash
# 执行远程命令
winrm quickconfig
winrs -r:192.168.1.100 -u:admin -p:password "ipconfig"

# PowerShell 远程
Enter-PSSession -ComputerName 192.168.1.100 -Credential admin
```

---

## Phase 4: 视觉识别与自动化

### 屏幕分析与目标定位

```bash
# 分析屏幕内容
python3 scripts/vision_recognition.py --image screenshot.png --task "找到下载按钮"

# 描述界面
python3 scripts/vision_recognition.py --image screenshot.png --describe

# 交互模式
python3 scripts/vision_recognition.py --image screenshot.png --interactive
```

### 自动化工作流

```bash
# 执行工作流
python3 scripts/automation_workflow.py \
    --session-id 123456789 \
    --workflow workflow.json

# 交互模式
python3 scripts/automation_workflow.py \
    --session-id 123456789 \
    --interactive
```

**工作流 JSON 示例:**
```json
{
  "name": "软件安装",
  "steps": [
    {"action": "capture"},
    {"action": "find", "target": "安装", "execute": "click"},
    {"action": "wait", "timeout": 5},
    {"action": "find", "target": "下一步", "execute": "click"},
    {"action": "find", "target": "我接受", "execute": "click"},
    {"action": "find", "target": "安装", "execute": "click"},
    {"action": "wait", "timeout": 60},
    {"action": "find", "target": "完成", "execute": "click"}
  ]
}
```

---

## Phase 5: 全自动驾驶

### SSH 一键安装

```bash
python3 scripts/autopilot.py \
    --host 192.168.1.100 \
    --username admin \
    --key ~/.ssh/id_rsa \
    --mode install
```

### 诊断修复

```bash
python3 scripts/expert_diagnose.py --interactive
python3 scripts/troubleshooting.py --diagnose "问题描述"
```

---

## 资源索引

### 远程控制脚本

| 脚本 | 功能 |
|------|------|
| [scripts/universal_remote.py](scripts/universal_remote.py) | 通用远程控制器（多软件统一接口） |
| [scripts/remote_desktop_control.py](scripts/remote_desktop_control.py) | UU 远程控制 |
| [scripts/rustdesk_control.py](scripts/rustdesk_control.py) | RustDesk 控制 |
| [scripts/remote_automation.py](scripts/remote_automation.py) | PyAutoGUI 自动化 |
| [scripts/vision_recognition.py](scripts/vision_recognition.py) | GPT-4V 视觉识别 |
| [scripts/automation_workflow.py](scripts/automation_workflow.py) | 自动化工作流 |

### 其他脚本

| 脚本 | 功能 |
|------|------|
| [scripts/autopilot.py](scripts/autopilot.py) | 全自动驾驶仪 |
| [scripts/expert_diagnose.py](scripts/expert_diagnose.py) | TOP3 专家诊断 |
| [scripts/config_expert.py](scripts/config_expert.py) | 配置专家 |
| [scripts/workflow_expert.py](scripts/workflow_expert.py) | Agent/Workflow 编排 |
| [scripts/monitoring_expert.py](scripts/monitoring_expert.py) | 监控运维 |
| [scripts/case_library.py](scripts/case_library.py) | 案例库 |
| [scripts/troubleshooting.py](scripts/troubleshooting.py) | 故障排查 |

---

## 应用场景

| 场景 | 推荐软件 |
|------|---------|
| **AI 鼠标点击自动化** | UU 远程 + PyAutoGUI ✅ |
| **开源自托管** | RustDesk |
| **无 UI 纯命令操作** | WinRM / PSRemoting |
| **临时快速连接** | RDP |
| **游戏/高清串流** | Parsec |
| **企业内网** | 向日葵 / ToDesk |

---

## 注意事项

- **多软件共存**：可同时安装多种远程软件，根据场景切换
- **API Key**：GPT-4V 视觉识别需要 OpenAI API Key
- **权限**：自动化操作可能需要管理员权限
- **安全**：敏感操作前建议备份重要数据

---

## 作者信息

| 项目 | 信息 |
|------|------|
| **作者** | ProClaw |
| **网站** | www.ProClaw.top |
| **联系方式** | wechat:Mr-zifang |

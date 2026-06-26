---
name: hermes-installer
description: Hermes Agent 安装配置完整指南。当用户要求安装 Hermes Agent、部署 Hermes、配置模型提供商、配置飞书/Telegram/Discord 网关时使用此 Skill。触发词：安装 Hermes、部署 Hermes Agent、配置 Hermes、配置 GLM、配置 Kimi、配置 OpenRouter、配置阿里云百炼、配置腾讯云、配置火山引擎、配置阶跃星辰、Hermes 更新、Hermes 飞书配置。
metadata:
  openclaw:
    requires:
      env:
        - OPENAI_API_KEY
        - OPENAI_BASE_URL
      bins:
        - git
        - python
        - pip
        - docker
---

# Hermes Agent 安装配置指南

## 系统支持

- **Linux/macOS**：使用 `.sh` 脚本
- **Windows**：以下三种方式任选其一：
  1. **Git Bash**：安装 Git 后自带，可以直接运行 `.sh` 脚本
  2. **WSL**：Windows Linux 子系统
  3. **手动执行**：不运行脚本，直接在 PowerShell 中执行对应命令

---

## CLI 与消息平台

Hermes 有两个入口：

### 1. 终端界面（CLI）
启动交互式终端界面：
```bash
hermes
```

### 2. 消息平台（Gateway）
运行网关，通过消息平台对话：
```bash
hermes gateway start
```

**支持的平台**：Telegram、Discord、Slack、WhatsApp、Signal、Email

---

### 常用命令对照表

| 功能 | CLI 命令 | 消息平台命令 |
|------|----------|--------------|
| 开始聊天 | `hermes run` | 向机器人发送消息 |
| 设置网关 | `hermes gateway setup` | - |
| 启动网关 | `hermes gateway start` | - |
| 新对话 | `/new` 或 `/reset` | `/new` 或 `/reset` |
| 改变模型 | `/model [provider:model]` | `/model [provider:model]` |
| 设定人格 | `/personality [name]` | `/personality [name]` |
| 重试/撤销 | `/retry` 或 `/undo` | `/retry` 或 `/undo` |
| 压缩上下文 | `/compress` | `/compress` |
| 查看使用 | `/usage` 或 `/insights` | `/usage` 或 `/insights` |
| 浏览技能 | `/skills` 或 `/<skill-name>` | `/skills` 或 `/<skill-name>` |
| 中断 | Ctrl+C 或发送新消息 | `/stop` 或发送新消息 |
| 平台状态 | - | `/status` 或 `/sethome` |

---

## 从 OpenClaw 迁移

如果你是从 OpenClaw 过来的，Hermes 可以自动导入你的设置、记忆、技能和 API 密钥。

### 首次设置时
运行 `hermes setup`，设置向导会自动检测 `~/.openclaw` 并在配置开始前提供迁移建议。

### 安装后任何时间
```bash
hermes claw migrate              # 交互式迁移（完整配置）
hermes claw migrate --dry-run    # 预览将要迁移的内容
hermes claw migrate --preset user-data   # 不包含密钥的迁移
hermes claw migrate --overwrite  # 覆盖已有冲突
```

## 快速安装

### 安装前确认

在执行安装前，**必须向用户确认以下信息**：

| 确认项 | 默认值 | 说明 |
|--------|--------|------|
| **安装位置** | `~/.hermes/hermes-agent` | Hermes Agent 程序目录 |
| **配置目录** | `~/.hermes` | 配置文件和日志目录 |
| **Python 版本** | 3.11 | 虚拟环境 Python 版本 |

**确认话术：**
> 将在以下位置安装 Hermes Agent：
> - 程序目录：`~/.hermes/hermes-agent`
> - 配置目录：`~/.hermes`
>
> 请选择安装方式：
> 1. 命令行部署（推荐，需要 Python 3.11+）
> 2. Docker 部署（需要 Docker）
>
> 请回复数字或方式名称，确认安装？(y/n)

### 安装步骤

**方式一：命令行部署**
```bash
# 1. 克隆仓库
git clone https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent
cd ~/.hermes/hermes-agent

# 2. 安装 uv（使用 pip，更安全）
pip install uv

# 3. 创建虚拟环境
uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[all]"
```

**方式二：Docker 部署**
详见 [docker-deploy.md](./docker-deploy.md)
git clone https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent
cd ~/.hermes/hermes-agent

# 2. 安装 uv（使用 pip，更安全）
pip install uv

# 3. 创建虚拟环境
uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[all]"
```

> 提示：使用 pip 安装 uv 不需要执行远程脚本，更安全。如有需要，也可以使用 uv 的预编译二进制：https://github.com/astral-sh/uv/releases

## 配置文件

- 配置文件：`~/.hermes/config.yaml`
- 环境变量：`~/.hermes/.env`

---

## 脚本文件列表

| 脚本 | 系统 | 说明 |
|------|------|------|
| `update-restart.sh` | Linux/macOS | 更新并重启网关 |
| `update-restart.ps1` | Windows | 更新并重启网关 |
| `uninstall.sh` | Linux/macOS | 卸载 Hermes Agent |
| `uninstall.ps1` | Windows | 卸载 Hermes Agent |
| `doctor.sh` | Linux/macOS | 健康检查 |
| `doctor.ps1` | Windows | 健康检查 |

---

## 更新与重启

### 手动更新
```bash
cd ~/.hermes/hermes-agent
source venv/bin/activate
hermes update
hermes gateway stop
hermes gateway run
```

### 使用脚本

**Linux/macOS:**
```bash
bash scripts/update-restart.sh
```

**Windows PowerShell:**
```powershell
.\scripts\update-restart.ps1
```

---

## 卸载

### Linux/macOS

```bash
bash scripts/uninstall.sh              # 完全卸载
bash scripts/uninstall.sh --keep-config # 保留配置
```

### Windows PowerShell

```powershell
.\scripts\uninstall.ps1           # 完全卸载
.\scripts\uninstall.ps1 -KeepConfig # 保留配置
```

---

## 健康检查

一键诊断 API 连接、网关状态、配置问题：

**Linux/macOS:**
```bash
bash scripts/doctor.sh
```

**Windows PowerShell:**
```powershell
.\scripts\doctor.ps1
```

**检查项：**
- ✅ 安装目录是否存在
- ✅ 虚拟环境是否正常
- ✅ 配置文件是否存在
- ✅ 环境变量是否设置
- ✅ 网关运行状态
- ✅ API 端点连通性
- ✅ 错误日志检测

---

## 按需加载模块

| 模块 | 内容 | 何时加载 |
|------|------|---------|
| `api-config.md` | 模型提供商 API 配置 | 用户要求配置 API/模型提供商 |
| `gateway-config.md` | 网关配置（飞书/Telegram/Discord） | 用户要求配置网关/通知渠道 |

**使用方式：** 当用户需要配置 API 或网关时，读取对应的模块文件。

---

## 常用命令

| 命令 | 说明 |
|------|------|
| `hermes` | 启动交互式 CLI |
| `hermes --version` | 查看版本 |
| `hermes doctor` | 诊断问题 |
| `hermes config show` | 查看配置 |
| `hermes config edit` | 编辑配置 |
| `hermes model` | 选择模型 |
| `hermes update` | 更新版本 |
| `hermes gateway status` | 网关状态 |
| `hermes gateway start/stop` | 启停网关 |

---

## Docker 部署

```bash
cd ~/.hermes/hermes-agent
docker build -t hermes-agent .
docker run -d -v ~/.hermes:/opt/data hermes-agent
```

---

## 相关链接

- 官方文档：https://hermes-agent.nousresearch.com/docs/
- GitHub：https://github.com/NousResearch/hermes-agent
- Discord：https://discord.gg/NousResearch

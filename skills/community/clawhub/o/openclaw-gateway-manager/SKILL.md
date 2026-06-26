# OpenClaw Gateway Manager

🦞 统一管理多云 OpenClaw 网关实例 / Unified Multi-Cloud OpenClaw Gateway Manager

---

## 🌍 语言 Languages

- 🇨🇳 [中文文档](#中文文档)
- 🇺🇸 [English Documentation](#english-documentation)

---

# 中文文档

## 💡 设计理念

**问题：** 用户可能在多平台、多云端部署了多个 OpenClaw 实例（本地、JVS Claw、QClaw、云端等），但缺乏统一管理工具。

**解决方案：** 本技能通过自动检测不同配置文件路径，统一管理所有 OpenClaw 变种实例，无论它们部署在哪里。

**核心思想：**
- 🔍 **自动发现** - 扫描所有可能的配置路径
- 🎯 **统一接口** - 一套命令管理所有实例
- ☁️ **多云支持** - 本地、云端、多厂商发行版
- 🛡️ **安全管理** - 三重确认 + 自动备份

---

## ✨ 功能

- 🔍 **智能查询** - 自动检测所有 OpenClaw 实例（本地/JVS/QClaw/云端）
- ✏️ **修改端口** - 自动修改配置文件 + 用户级服务定义
- 🔄 **重启网关** - 安全重启指定网关或所有网关
- ✅ **验证配置** - 检查配置一致性、端口监听状态
- ➕ **创建新实例** - 一键创建新网关实例
- 🗑️ **安全删除** - 三重确认 + 自动备份
- 📡 **端口扫描** - 智能识别所有实例

---

## 🎯 支持的发行版 Supported Distributions

| 发行版 | 配置目录 | 默认端口 | 开发者 | 状态 |
|--------|---------|---------|--------|------|
| **OpenClaw (原始版)** | `~/.openclaw/` | 18789 | OpenClaw 社区 | ✅ |
| **JVS Claw (阿里云)** | `~/.jvs/.openclaw/` | 18789 | 阿里云无影 | ✅ |
| **QClaw (腾讯)** | `~/.qclaw/` | 28789 | 腾讯 | ✅ |
| **云端 Claw** | `~/.claw-cloud/` | 自定义 | 云服务 | 🔜 |
| **自定义实例** | `~/.openclaw-<name>/` | 自定义 | 用户 | ✅ |

**识别原理：** 通过检测不同的配置文件路径来区分不同发行版。

---

## 🚀 快速开始

### 安装

正常安装时，应交给技能系统或模型运行时放到它认为合适的技能目录。
只有手动克隆用于开发或调试时，才建议放到你自己的普通工作目录。
不要把 `~/.jvs/.openclaw/` 这类实例配置目录误当成仓库目录。

```bash
git clone https://github.com/seastaradmin/openclaw-gateway-manager.git ~/openclaw-gateway-manager
cd ~/openclaw-gateway-manager
```

### 使用

```bash
# 查看所有网关状态（自动检测所有实例）
./scripts/gateway-status.sh

# 检查依赖
./scripts/check-dependencies.sh

# 扫描端口
./scripts/gateway-scan-ports.sh

# 修改端口
./scripts/gateway-set-port.sh 本地虾 18888

# 重启所有网关
./scripts/gateway-restart.sh all

# 验证配置
./scripts/gateway-verify.sh 本地虾

# 创建新实例
./scripts/gateway-create.sh test-bot 18899 openim

# 删除实例（三重确认）
./scripts/gateway-delete.sh test-bot
```

---

## 📊 示例输出

```
=== OpenClaw Gateway 实例 ===

🔹 本地虾 (JVS Claw)
   主端口：18789
   辅助端口：18791(浏览器) 18792(Canvas)
   配置：~/.jvs/.openclaw
   状态：✅ 运行中 (PID: 6512)
   频道：openim
   Dashboard: http://127.0.0.1:18789/

🔹 飞书机器人
   主端口：18790
   辅助端口：18792(浏览器) 18793(Canvas)
   配置：~/.openclaw
   状态：✅ 运行中 (PID: 76822)
   频道：feishu
   Dashboard: http://127.0.0.1:18790/

🔹 QClaw (腾讯)
   主端口：28789
   辅助端口：28791(浏览器) 28792(Canvas)
   配置：~/.qclaw
   状态：✅ 运行中 (PID: 87107)
   频道：wechat-access
   Dashboard: http://127.0.0.1:28789/
```

---

## 🛡️ 安全特性

- **删除操作三重确认** - 防止误删
- **自动备份** - 删除前备份到 `~/.openclaw-deleted-backups/`
- **端口检查** - 修改前检查端口是否被占用
- **配置验证** - 修改后自动验证
- **依赖检查** - 安装时自动检查系统依赖

---

## 📦 脚本列表

| 脚本 | 功能 | 危险等级 |
|------|------|---------|
| `gateway-status.sh` | 查询所有实例状态 | 🟢 安全 |
| `gateway-scan-ports.sh` | 端口扫描 | 🟢 安全 |
| `gateway-set-port.sh` | 修改端口 | 🟡 中等 |
| `gateway-restart.sh` | 重启网关 | 🟢 安全 |
| `gateway-verify.sh` | 验证配置 | 🟢 安全 |
| `gateway-create.sh` | 创建实例 | 🟡 中等 |
| `gateway-delete.sh` | 删除实例 | 🔴 危险 |
| `check-dependencies.sh` | 依赖检查 | 🟢 安全 |

---

## ⚙️ 系统要求

### 操作系统

- ✅ **macOS** - 完整支持，使用 LaunchAgent
- ✅ **Linux** - 完整支持，优先使用 `systemd --user`，没有时回退手动模式
- ⚠️ **Windows** - 支持扫描和校验，服务创建与启动以手动为主

### 依赖项

运行以下命令检查依赖：

```bash
./scripts/check-dependencies.sh
```

**必需工具：**

| 工具 | 用途 | 安装命令 |
|------|------|---------|
| `jq` | JSON 处理 | `brew install jq` / `sudo apt install jq` |
| `curl` | HTTP 请求 | 大多数系统自带 |
| `node` | OpenClaw 运行 | `brew install node` / 发行版包管理器 |
| `lsof` / `ss` / `netstat` | 端口检查 | 任一可用即可 |
| `launchctl` + `plutil` | macOS 服务管理 | macOS 自带 |
| `systemctl` | Linux 用户级服务管理 | 大多数 systemd 发行版自带 |

---

## ⚠️ 安全说明

### 删除操作

- ✅ **三重确认** - 需要 3 次确认才能执行删除
- ✅ **自动备份** - 删除前备份到 `~/.openclaw-deleted-backups/`
- ⚠️ **破坏性操作** - 使用 `rm -rf` 删除配置目录

**建议：** 首次使用前手动备份重要数据

### 路径安全

✅ **已修复** - 所有路径使用 `$HOME` 而非硬编码用户路径

### 服务权限

- 仅创建用户级服务（`~/Library/LaunchAgents/` 或 `~/.config/systemd/user/`）
- 不需要系统级权限或 sudo
- 每个用户独立管理

---

# English Documentation

## 💡 Philosophy

**Problem:** Users may deploy multiple OpenClaw instances across different platforms and clouds (local, JVS Claw, QClaw, cloud, etc.), but lack a unified management tool.

**Solution:** This skill automatically detects different configuration paths and provides unified management for all OpenClaw variants, regardless of where they're deployed.

**Core Principles:**
- 🔍 **Auto-Discovery** - Scan all possible configuration paths
- 🎯 **Unified Interface** - One set of commands for all instances
- ☁️ **Multi-Cloud** - Local, cloud, multi-vendor distributions
- 🛡️ **Safe Management** - Triple confirmation + automatic backup

---

## ✨ Features

- 🔍 **Smart Status Query** - Auto-detect all OpenClaw instances
- ✏️ **Modify Ports** - Automatically update config files + user service definitions
- 🔄 **Restart Gateways** - Safely restart specific or all gateways
- ✅ **Verify Configuration** - Check config consistency and port status
- ➕ **Create Instances** - One-click creation with per-OS service setup
- 🗑️ **Safe Deletion** - Triple confirmation + automatic backup
- 📡 **Port Scanning** - Intelligently identify all instances

---

## 🎯 Supported Distributions

| Distribution | Config Directory | Default Port | Developer | Status |
|--------------|-----------------|--------------|-----------|--------|
| **OpenClaw (Original)** | `~/.openclaw/` | 18789 | OpenClaw Community | ✅ |
| **JVS Claw (Alibaba)** | `~/.jvs/.openclaw/` | 18789 | Alibaba Cloud Wuying | ✅ |
| **QClaw (Tencent)** | `~/.qclaw/` | 28789 | Tencent | ✅ |
| **Cloud Claw** | `~/.claw-cloud/` | Custom | Cloud Service | 🔜 |
| **Custom Instance** | `~/.openclaw-<name>/` | Custom | User | ✅ |

**Identification:** Different distributions are identified by their configuration file paths.

---

## 🚀 Quick Start

### Installation

For normal installation, let the skill system or runtime place this repository in the location it considers appropriate.
Only use a manually chosen folder when you are cloning it for local development or debugging.
Do not confuse a JVS/OpenClaw instance config directory with this repository.

```bash
git clone https://github.com/seastaradmin/openclaw-gateway-manager.git ~/openclaw-gateway-manager
cd ~/openclaw-gateway-manager
```

### Usage

```bash
# Check all gateway status (auto-detect all instances)
./scripts/gateway-status.sh

# Check dependencies
./scripts/check-dependencies.sh

# Scan ports
./scripts/gateway-scan-ports.sh

# Modify port
./scripts/gateway-set-port.sh local-shrimp 18888

# Restart all gateways
./scripts/gateway-restart.sh all

# Verify config
./scripts/gateway-verify.sh local-shrimp

# Create new instance
./scripts/gateway-create.sh test-bot 18899 openim

# Delete instance (triple confirmation)
./scripts/gateway-delete.sh test-bot
```

---

## 📝 Example Output

```
=== OpenClaw Gateway Instances ===

🔹 Local Shrimp (JVS Claw)
   Main Port: 18789
   Aux Ports: 18791(Browser) 18792(Canvas)
   Config: ~/.jvs/.openclaw
   Status: ✅ Running (PID: 6512)
   Channel: openim
   Dashboard: http://127.0.0.1:18789/

🔹 Feishu Bot
   Main Port: 18790
   Aux Ports: 18792(Browser) 18793(Canvas)
   Config: ~/.openclaw
   Status: ✅ Running (PID: 76822)
   Channel: feishu
   Dashboard: http://127.0.0.1:18790/

🔹 QClaw (Tencent)
   Main Port: 28789
   Aux Ports: 28791(Browser) 28792(Canvas)
   Config: ~/.qclaw
   Status: ✅ Running (PID: 87107)
   Channel: wechat-access
   Dashboard: http://127.0.0.1:28789/
```

---

## 🛡️ Safety Features

- **Triple confirmation for deletion** - Prevents accidental deletion
- **Automatic backup** - Backs up before deletion
- **Port availability check** - Verifies port is free
- **Configuration validation** - Auto-verifies after changes
- **Dependency checker** - Auto-checks system dependencies

---

## ⚙️ System Requirements

### Operating System

- ✅ **macOS** - full support with LaunchAgent
- ✅ **Linux** - full support with `systemd --user`, falls back to manual mode if unavailable
- ⚠️ **Windows** - detection and validation are supported; service creation is manual

### Dependencies

Run to check dependencies:

```bash
./scripts/check-dependencies.sh
```

**Required Tools:**

| Tool | Purpose | Install Command |
|------|---------|----------------|
| `jq` | JSON processing | `brew install jq` / `sudo apt install jq` |
| `curl` | HTTP requests | Built-in on most systems |
| `node` | OpenClaw runtime | `brew install node` / distro package manager |
| `lsof` / `ss` / `netstat` | Port check | Any one is enough |
| `launchctl` + `plutil` | macOS service management | Built-in macOS |
| `systemctl` | Linux user service management | Built-in on most systemd distros |

---

## ⚠️ Safety Notes

### Deletion Operation

- ✅ **Triple confirmation** - Requires 3 confirmations
- ✅ **Automatic backup** - Backs up to `~/.openclaw-deleted-backups/`
- ⚠️ **Destructive** - Uses `rm -rf` to delete config directories

**Recommendation:** Manually backup important data before first use

### Path Security

✅ **Fixed** - All paths use `$HOME` instead of hardcoded user paths

### Service Permissions

- Creates user-level services only (`~/Library/LaunchAgents/` or `~/.config/systemd/user/`)
- No system-level permissions or sudo required
- Each user managed independently

---

## 📄 License 许可证

MIT License

## 🔗 Links 链接

- **GitHub**: https://github.com/seastaradmin/openclaw-gateway-manager
- **Author**: @seastaradmin
- **Version**: 1.0.2

---

## 🌍 跨平台支持 Cross-Platform Support

### 支持的操作系统

| 系统 | 服务管理 | 配置路径 | 状态 |
|------|---------|---------|------|
| **macOS** | LaunchAgent (用户级) | `~/.openclaw/`, `~/.jvs/.openclaw/`, `~/.qclaw/` | ✅ |
| **Linux** | systemd user service / manual fallback | `~/.openclaw/`, `~/.config/openclaw/`, `/opt/openclaw/` | ✅ |
| **Windows** | 手动模式 | `%USERPROFILE%/.openclaw/`, `%APPDATA%/openclaw/` | ⚠️ |

### 自动检测

脚本会自动检测操作系统并使用相应的服务管理方式：

```bash
# macOS
launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# Linux
systemctl --user start ai.openclaw.gateway-<name>

# Windows
# 不自动创建服务，用户手动选择
```

### 路径规范

- **macOS/Linux**: 使用 `$HOME` 环境变量
- **Windows**: 使用 `%USERPROFILE%` 和 `%APPDATA%`
- ✅ 无硬编码路径，支持多用户

---

## 🔒 安全审查响应 Security Review Response

### 指令范围 Instruction Scope

**审查意见：**
> Scripts read/write user files, create user-level service definitions, scan ports, and perform rm -rf.

**回应：**
✅ **这是预期行为** - 作为网关管理器，这些操作是必要的。

**安全措施：**
- ✅ 三重确认机制
- ✅ 自动备份到 `~/.openclaw-deleted-backups/`
- ✅ 仅创建用户级服务（无需 sudo）
- ✅ 透明配置（plist 文件可审查）
- ✅ 完整文档（SKILL.md + SECURITY_RESPONSE.md）

### 持久性和权限 Persistence & Privilege

**审查意见：**
> Creates user-level service definitions for persistent execution.

**回应：**
✅ **这是必要功能** - 网关需要开机自启。

**安全特性：**
- ✅ 仅用户级服务（`~/Library/LaunchAgents/` 或 `~/.config/systemd/user/`）
- ✅ 不需要系统权限
- ✅ 可以随时卸载
- ✅ 跨平台支持（Linux systemd, Windows 可选）

### 破坏性操作 Destructive Operations

**审查意见：**
> Performs irreversible deletes.

**回应：**
✅ **已实施多层保护**：

1. **三重确认** - 需要 3 次确认
2. **自动备份** - 删除前备份
3. **进程检查** - 停止进程后删除
4. **文档警告** - 明确说明风险

**查看安全响应全文：**
```bash
cat ./SECURITY_RESPONSE.md
```

---

# English Documentation (Continued)

## 🌍 Cross-Platform Support

### Supported Operating Systems

| OS | Service Management | Config Paths | Status |
|----|-------------------|--------------|--------|
| **macOS** | LaunchAgent (user-level) | `~/.openclaw/`, `~/.jvs/.openclaw/`, `~/.qclaw/` | ✅ |
| **Linux** | systemd user service / manual fallback | `~/.openclaw/`, `~/.config/openclaw/`, `/opt/openclaw/` | ✅ |
| **Windows** | Manual mode | `%USERPROFILE%/.openclaw/`, `%APPDATA%/openclaw/` | ⚠️ |

### Auto-Detection

Scripts automatically detect the OS and use appropriate service management:

```bash
# macOS
launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# Linux
systemctl --user start ai.openclaw.gateway-<name>

# Windows
# No automatic service creation, user chooses manually
```

### Path Conventions

- **macOS/Linux**: Uses `$HOME` environment variable
- **Windows**: Uses `%USERPROFILE%` and `%APPDATA%`
- ✅ No hardcoded paths, multi-user support

---

## 🔒 Security Review Response

### Instruction Scope

**Review Feedback:**
> Scripts read/write user files, create user-level service definitions, scan ports, and perform rm -rf.

**Response:**
✅ **This is intended behavior** - These operations are necessary for a gateway manager.

**Safety Measures:**
- ✅ Triple confirmation mechanism
- ✅ Automatic backup to `~/.openclaw-deleted-backups/`
- ✅ User-level services only (no sudo required)
- ✅ Transparent configuration (plist files auditable)
- ✅ Complete documentation (SKILL.md + SECURITY_RESPONSE.md)

### Persistence & Privilege

**Review Feedback:**
> Creates user-level service definitions for persistent execution.

**Response:**
✅ **This is necessary functionality** - Gateways need to auto-start.

**Safety Features:**
- ✅ User-level services only (`~/Library/LaunchAgents/` or `~/.config/systemd/user/`)
- ✅ No system-level permissions required
- ✅ Can be uninstalled anytime
- ✅ Cross-platform support (Linux systemd, Windows optional)

### Destructive Operations

**Review Feedback:**
> Performs irreversible deletes.

**Response:**
✅ **Multiple layers of protection implemented**:

1. **Triple confirmation** - Requires 3 confirmations
2. **Automatic backup** - Backs up before deletion
3. **Process check** - Stops processes before deletion
4. **Documentation warnings** - Clearly states risks

**View full security response:**
```bash
cat ./SECURITY_RESPONSE.md
```

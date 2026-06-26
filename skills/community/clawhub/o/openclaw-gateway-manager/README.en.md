# OpenClaw Gateway Manager

🦞 Unified Multi-Cloud OpenClaw Gateway Manager

---

## 💡 Philosophy

**Problem:** Users deploy OpenClaw across multiple platforms and clouds (local, JVS Claw, QClaw, cloud instances, etc.), but lack a unified management tool.

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
In either case, do not confuse an OpenClaw instance config directory with this repository.

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
💡 Unified Management Platform - Multi-Cloud Support

🔍 Scanning all OpenClaw configuration paths...

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

📊 Statistics:
   Detected ports: 9
```

---

## 🛡️ Safety Features

- **Triple confirmation for deletion** - Prevents accidental deletion
- **Automatic backup** - Backs up to `~/.openclaw-deleted-backups/`
- **Port availability check** - Verifies port is free before modification
- **Configuration validation** - Auto-verifies after changes
- **Dependency checker** - Auto-checks system dependencies

---

## 📦 Scripts

| Script | Function | Risk Level |
|--------|----------|------------|
| `gateway-status.sh` | Query status | 🟢 Safe |
| `gateway-scan-ports.sh` | Port scanning | 🟢 Safe |
| `gateway-set-port.sh` | Modify ports | 🟡 Medium |
| `gateway-restart.sh` | Restart gateway | 🟢 Safe |
| `gateway-verify.sh` | Verify config | 🟢 Safe |
| `gateway-create.sh` | Create instance | 🟡 Medium |
| `gateway-delete.sh` | Delete instance | 🔴 Dangerous |
| `check-dependencies.sh` | Check dependencies | 🟢 Safe |

---

## 🎯 Instance Aliases

| Alias | Config Directory | Default Port |
|-------|-----------------|--------------|
| `local-shrimp` / `本地虾` / `18789` | `~/.jvs/.openclaw/` | 18789 |
| `feishu` / `飞书` / `18790` | `~/.openclaw/` | 18790 |
| `qclaw` / `腾讯` / `28789` | `~/.qclaw/` | 28789 |

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
- ✅ **Automatic backup** - Backs up before deletion
- ⚠️ **Destructive** - Uses `rm -rf` to delete config directories

**Recommendation:** Manually backup important data before first use

### Path Security

✅ **Fixed** - All paths use `$HOME` instead of hardcoded user paths

### Service Permissions

- Creates user-level services only (`~/Library/LaunchAgents/` or `~/.config/systemd/user/`)
- No system-level permissions or sudo required
- Each user managed independently

---

## 📄 License

MIT

## 🔗 Links

- **GitHub**: https://github.com/seastaradmin/openclaw-gateway-manager
- **Author**: @seastaradmin
- **Version**: 1.0.2

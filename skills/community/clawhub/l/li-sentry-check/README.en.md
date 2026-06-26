# 🔍 li_sentry_check - Server Inspection Skill

> Multi-platform server inspection and health check skill. SSH into remote Linux servers using key-based authentication, run read-only inspection commands, and generate structured Markdown reports.

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://clawhub.ai/skills/li_sentry_check)
[![Platforms](https://img.shields.io/badge/platforms-nanobot%20%7C%20OpenClaw%20%7C%20Hermes-green.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📋 Overview

`li_sentry_check` is a cross-platform server inspection skill supporting **nanobot**, **OpenClaw**, and **Hermes agent**. It logs into remote Linux servers via SSH key authentication, executes read-only inspection commands (CPU, memory, disk, network, services, security), and generates structured Markdown reports with automatic anomaly highlighting.

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🔐 SSH Key Authentication | Key-only authentication, password login disabled, security hardened |
| 📊 Hardware Inspection | CPU, memory, disk, network usage |
| 🖥️ Service Inspection | Key service status, error logs |
| 🛡️ Security Inspection | SSH anomalous logins, firewall alerts, kernel errors |
| 📝 Structured Reports | Markdown/JSON format, anomalies prioritized |
| 🌐 Cross-Platform | Supports nanobot, OpenClaw, Hermes |

## 🚀 Quick Start

### 1. Install the Skill

```bash
# nanobot
./manage.sh skill install li_sentry_check

# OpenClaw
npx clawhub@latest install li_sentry_check

# Hermes
hermes skill install li_sentry_check
```

### 2. Configure SSH Keys

```bash
# Generate key pair
ssh-keygen -t rsa -b 4096 -f ~/.ssh/li_sentry_check -N ""

# Copy public key to remote server
ssh-copy-id -i ~/.ssh/li_sentry_check.pub inspector@<SERVER_IP>

# Test connection
ssh -i ~/.ssh/li_sentry_check inspector@<SERVER_IP>
```

### 3. Configure Target Servers

Edit `references/targets.yaml`:

```yaml
targets:
  production-web:
    host: YOUR_SERVER_IP
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - nginx
      - docker
      - sshd
```

### 4. Run Inspection

```bash
# Basic inspection (hardware resources)
python3 scripts/inspect.py --target production-web --checks basic

# Service inspection
python3 scripts/inspect.py --target production-web --checks services

# Full inspection (basic + services + security + logs)
python3 scripts/inspect.py --target production-web --checks daily

# JSON format output
python3 scripts/inspect.py --target production-web --checks daily --format json

# Output to file
python3 scripts/inspect.py --target production-web --checks daily --output report.md
```

## 📖 Inspection Check Groups

| Group | Content | Commands |
|-------|---------|----------|
| `basic` | CPU, memory, disk, network | 8 |
| `services` | Service status + error logs (dynamic) | 3×N |
| `daily` | Full inspection (basic + services + security + logs) | 26 |

## 📊 Report Example

```markdown
# 🔍 Server Inspection Report

- Target: production-web
- Host: YOUR_SERVER_IP
- User: inspector
- Checks: daily
- Started: 2026-04-26T09:00:00+00:00
- Total checks: 26
- ⚠️ Anomalies: 3

## Overall Status: ⚠️ WARNING

## ⚠️ Anomalies (Priority)

### ⚠️ systemd_failed_units
Command: `systemctl --failed --no-pager`
Status: OK (contains anomalies)

Output:
```
UNIT          LOAD   ACTIVE SUB    DESCRIPTION
mcelog.service loaded failed failed Machine Check Exception Logging Daemon
```
```

## 🔧 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--target` | Target server name (defined in targets.yaml) | (required) |
| `--checks` | Check group: `basic`, `services`, `daily` | `basic` |
| `--format` | Output format: `markdown`, `json` | `markdown` |
| `--output` | Output to file (default: stdout) | stdout |

## 🌐 Cross-Platform Support

| Platform | Runtime | Script | Command |
|----------|---------|--------|---------|
| **OpenClaw** | Node.js 24+ | `scripts/inspect.mjs` | `node scripts/inspect.mjs --target bogon --checks daily` |
| **NanoBot** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |
| **Hermes** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |

## 📁 File Structure

```
li_sentry_check/
├── SKILL.md                  # Skill documentation
├── _meta.json                # Skill metadata
├── design.md                 # Design documentation
├── references/
│   ├── targets.yaml          # Target server configuration
│   └── checks.yaml           # Inspection command allowlist
└── scripts/
    ├── inspect.mjs           # Node.js implementation (OpenClaw)
    └── inspect.py            # Python implementation (NanoBot/Hermes)
```

## 🔒 Security Best Practices

- **Key permissions**: `chmod 600 ~/.ssh/li_sentry_check`
- **Host verification**: For production, pre-populate `known_hosts` instead of `accept-new`
- **Service names**: Only alphanumeric, hyphens, underscores allowed (validated before use)
- **Command allowlist**: Never modify `checks.yaml` with state-changing commands
- **Report handling**: Reports may contain system data — do not share publicly

## 🔧 Extension Guide

### Add a New Target Server

Edit `references/targets.yaml`:

```yaml
targets:
  database-server:
    host: YOUR_SERVER_IP
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - mysql
      - redis
```

### Add a New Check Group

Edit `references/checks.yaml`:

```yaml
checks:
  database:
    description: Database inspection
    commands:
      - id: mysql_status
        cmd: "systemctl status mysql --no-pager | sed -n '1,20p'"
        timeoutSec: 10
      - id: mysql_connections
        cmd: "mysql -e 'SHOW STATUS LIKE \"Threads_connected\"' || true"
        timeoutSec: 15
```

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-04-26 | Initial release: basic, services, and full inspection |

## 📄 License

MIT License

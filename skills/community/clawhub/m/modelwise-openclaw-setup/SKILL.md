---
name: OpenClaw Setup
description: This skill should be used when the user asks to "install OpenClaw", "setup OpenClaw", "configure OpenClaw", "start OpenClaw gateway", "部署 OpenClaw", or needs help with OpenClaw installation, configuration, and initial setup on Windows/macOS/Linux systems. By ModelWise team.
version: 1.0.0
---

# OpenClaw Installation and Setup Guide

> **By ModelWise team** - Professional AI Agent Solutions

This skill provides comprehensive guidance for installing, configuring, and running OpenClaw - an open-source personal AI assistant gateway.

## Overview

**OpenClaw** is a multi-channel AI assistant gateway that enables users to use AI assistants on their existing messaging platforms (WhatsApp, Telegram, Slack, Discord, etc.).

**Key Features:**
- Local-first architecture
- 20+ messaging channel integrations
- Multi-model support (Anthropic, OpenAI, Google, local models)
- Voice interaction (Voice Wake + Talk Mode)
- Canvas visualization workspace (A2UI protocol)
- Skills extension system

## Prerequisites

### System Requirements

| Platform | Requirements |
|----------|-------------|
| **Windows** | Windows 10/11, Node.js >= 22.12.0 |
| **macOS** | macOS 12+, Node.js >= 22.12.0 |
| **Linux** | Ubuntu 20.04+/Debian 11+, Node.js >= 22.12.0 |

### Node.js Installation

Check Node.js version first:

```bash
node --version
```

#### Windows

```powershell
# Option 1: Using winget
winget install OpenJS.NodeJS.LTS

# Option 2: Using Chocolatey
choco install nodejs-lts

# Option 3: Download installer
# https://nodejs.org/
```

#### macOS / Linux

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# Reload shell
source ~/.zshrc  # or ~/.bashrc

# Install Node.js 22
nvm install 22
nvm use 22
nvm alias default 22
```

## Installation

### Step 1: Install OpenClaw CLI

```bash
# All platforms
npm install -g openclaw@latest

# Verify installation
openclaw --version
```

### Step 2: Run Configuration Wizard

```bash
# Start interactive configuration
openclaw onboard

# Or with daemon installation (recommended)
openclaw onboard --install-daemon
```

The wizard will guide through:
1. Model provider selection (Anthropic, OpenAI, Volcengine, etc.)
2. API key configuration
3. Channel setup (Telegram, Slack, etc.)
4. Gateway configuration

### Step 3: Configure API Keys

API keys are stored in `~/.openclaw/credentials/` (or `%USERPROFILE%\.openclaw\credentials\` on Windows).

```bash
# Set Anthropic API key
openclaw credentials set anthropic YOUR_API_KEY

# Set Volcengine API key (for Kimi)
openclaw credentials set volcengine YOUR_API_KEY

# Set OpenAI API key
openclaw credentials set openai YOUR_API_KEY
```

### Step 4: Start Gateway

```bash
# Start gateway on default port (18789)
openclaw gateway

# Or specify port
openclaw gateway --port 18789

# Run in background (macOS/Linux)
openclaw gateway --daemon

# Windows: run in new window or use pm2
start /B openclaw gateway
```

## Configuration

### Config File Location

| Platform | Path |
|----------|------|
| macOS/Linux | `~/.openclaw/openclaw.json` |
| Windows | `%USERPROFILE%\.openclaw\openclaw.json` |

### Essential Configuration

```json5
{
  // Gateway settings
  gateway: {
    enabled: true,
    port: 18789,
    mode: "local",
    bind: "0.0.0.0"
  },

  // Agent settings
  agents: {
    defaults: {
      model: "volcengine/kimi-k2.5",
      thinking: {
        enabled: true,
        level: "medium"
      }
    }
  },

  // Telegram channel (example)
  telegram: {
    enabled: true,
    botToken: "YOUR_BOT_TOKEN",
    dmPolicy: "open",
    streaming: "partial"
  }
}
```

### Model Provider Configuration

| Provider | Model Format | Credentials Key |
|----------|-------------|-----------------|
| Anthropic | `anthropic/claude-opus-4-6` | `anthropic` |
| OpenAI | `openai/gpt-5.2` | `openai` |
| Volcengine | `volcengine/kimi-k2.5` | `volcengine` |
| Google | `google/gemini-2.5-pro` | `google` |
| Local | `local/llama-3.2` | N/A |

## Channel Setup

### Telegram Bot Setup

1. **Create Bot:**
   - Open @BotFather on Telegram
   - Send `/newbot`
   - Follow instructions to get bot token

2. **Configure OpenClaw:**
```bash
openclaw credentials set telegram 7123456789:AAHxxxxxxxx
openclaw config set telegram.enabled true
openclaw config set telegram.dmPolicy "open"
```

3. **Restart Gateway:**
```bash
openclaw gateway restart
```

### Security Policies

**DM Policy Options:**
- `open`: Accept messages from anyone (for public bots)
- `pairing`: Require pairing code approval (default, more secure)

## Common Commands

### Diagnostics

```bash
# Check system status
openclaw doctor

# View running processes (macOS/Linux)
ps aux | grep openclaw | grep -v grep

# View running processes (Windows PowerShell)
Get-Process | Where-Object {$_.ProcessName -eq "node"}

# Check gateway status
openclaw gateway status
```

### Updates

```bash
# Update to latest stable
openclaw update --channel stable

# Update to beta version
openclaw update --channel beta
```

### Maintenance

```bash
# Stop gateway (macOS/Linux)
killall openclaw openclaw-gateway

# Stop gateway (Windows PowerShell)
Stop-Process -Name "node" -Force

# View logs
tail -f ~/.openclaw/logs/gateway.log  # macOS/Linux
Get-Content $env:USERPROFILE\.openclaw\logs\gateway.log -Tail 100  # Windows

# Clear sessions
openclaw sessions prune
```

## Directory Structure

| Platform | Base Path |
|----------|-----------|
| macOS/Linux | `~/.openclaw/` |
| Windows | `%USERPROFILE%\.openclaw\` |

```
.openclaw/
├── openclaw.json       # Main configuration
├── credentials/        # API keys (encrypted)
├── sessions/           # Session data
├── logs/               # Log files
├── workspace/          # Working directory
│   └── skills/         # Custom skills
├── agents/             # Agent configurations
├── canvas/             # Canvas data
├── browser/            # Browser profiles
└── memory/             # Memory storage
```

## Troubleshooting

### Common Issues

**1. Node.js version mismatch:**
```bash
# Check version
node --version  # Should be >= 22.12.0

# Fix (macOS/Linux)
nvm use 22

# Fix (Windows)
# Download and install from https://nodejs.org/
```

**2. Port already in use:**
```bash
# macOS/Linux
lsof -i :18789
kill -9 <PID>

# Windows PowerShell
netstat -ano | findstr :18789
taskkill /PID <PID> /F
```

**3. Permission denied:**
```bash
# macOS/Linux
sudo chown -R $(whoami) ~/.npm

# Windows (run PowerShell as Administrator)
npm cache clean --force
```

**4. Gateway not starting:**
```bash
# Check logs (macOS/Linux)
cat ~/.openclaw/logs/gateway.log

# Check logs (Windows)
type %USERPROFILE%\.openclaw\logs\gateway.log

# Run diagnostics
openclaw doctor
```

### Reset Configuration

```bash
# Backup and reset (macOS/Linux)
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak
rm -rf ~/.openclaw
openclaw onboard

# Backup and reset (Windows PowerShell)
Copy-Item $env:USERPROFILE\.openclaw\openclaw.json $env:USERPROFILE\.openclaw\openclaw.json.bak
Remove-Item -Recurse -Force $env:USERPROFILE\.openclaw
openclaw onboard
```

## Quick Reference

```bash
# Installation
npm install -g openclaw@latest

# Configuration
openclaw onboard --install-daemon

# Start/Stop
openclaw gateway              # Start
killall openclaw              # Stop (macOS/Linux)

# Status
openclaw doctor               # Diagnostics
openclaw --version            # Version

# Update
openclaw update --channel stable
```

## Additional Resources

### Scripts

Cross-platform installation checkers:
- **`scripts/check-installation.sh`** - Bash script (macOS/Linux/Windows Git Bash)
- **`scripts/check-installation.ps1`** - PowerShell script (Windows)

### Reference Files

- **`references/configuration-reference.md`** - Complete configuration options

### Example Files

- **`examples/openclaw.json`** - Full configuration example
- **`examples/telegram-setup.md`** - Telegram channel setup guide

### Official Resources

- Website: https://openclaw.ai
- Documentation: https://docs.openclaw.ai
- GitHub: https://github.com/openclaw/openclaw
- Discord: https://discord.gg/clawd
- ClawHub (Skills): https://clawhub.com

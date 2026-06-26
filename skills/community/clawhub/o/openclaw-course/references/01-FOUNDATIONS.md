# Module 1: Foundations — Getting Started with OpenClaw

## Table of Contents
1. [OpenClaw Ecosystem Overview](#openclaw-ecosystem-overview)
2. [Installation Guides](#installation-guides)
3. [Configuration Basics](#configuration-basics)
4. [Setting Up Messaging Bridges](#setting-up-messaging-bridges)
5. [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## OpenClaw Ecosystem Overview

### What is OpenClaw?

OpenClaw is a **personal AI assistant** you run on your own devices. Unlike cloud-based assistants that store your data on remote servers, OpenClaw operates on your infrastructure — giving you complete control over your data, privacy, and capabilities.

The name "OpenClaw" comes from **Molty**, a space lobster AI assistant 🦞 — reflecting the project's philosophy of being personal, quirky, and entirely under your control.

> **"EXFOLIATE! EXFOLIATE!"** — A space lobster, probably

### Core Philosophy

- **Local-first**: Your data stays on your machines
- **Privacy-centric**: No external data mining or surveillance
- **Extensible**: Add capabilities through skills and plugins
- **Multi-channel**: Communicate via WhatsApp, Telegram, Slack, Discord, and 20+ platforms
- **Autonomous**: Can run scheduled tasks, monitor systems, and proactively assist

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MESSAGING LAYER                              │
│  WhatsApp │ Telegram │ Slack │ Discord │ Signal │ iMessage │ ...   │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         GATEWAY (Control Plane)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Sessions   │  │   Skills     │  │    Cron      │              │
│  │   Manager    │  │   Registry   │  │  Scheduler   │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Browser    │  │    Exec      │  │   Web Tools  │              │
│  │   Control    │  │   Runner     │  │ (Search/Fetch)│             │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      AI MODEL LAYER                                 │
│  Anthropic Claude │ OpenAI GPT │ Google Gemini │ Local Models      │
│  (cloud)          │ (cloud)    │ (cloud)       │ (Ollama, LM Studio)│
└─────────────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Gateway**: The central WebSocket control plane that manages sessions, channels, tools, and events
2. **Agent Runtime**: The Pi agent runtime in RPC mode with tool streaming
3. **Skills**: Modular capabilities that teach the agent how to use tools
4. **Channels**: Messaging platform integrations (WhatsApp, Telegram, etc.)
5. **Tools**: Browser, file system, process execution, web search/fetch

### Who Is It For?

**Developers and power users** who want a personal AI assistant they can message from anywhere — without giving up control of their data or relying on a hosted service.

**What makes it different?**
- **Self-hosted**: runs on your hardware, your rules
- **Multi-channel**: one Gateway serves WhatsApp, Telegram, Discord, and more simultaneously
- **Agent-native**: built for coding agents with tool use, sessions, memory, and multi-agent routing
- **Open source**: MIT licensed, community-driven

---

## Installation Guides

### Prerequisites

- **Node.js ≥ 22** (Node 24 recommended for best compatibility)
- **npm, pnpm, or bun** (package manager)
- **Git** (for source installs)

Check your Node version:
```bash
node --version  # Should show v22.x.x or v24.x.x
```

### Platform-Specific Installation

#### Option 1: Quick Install (Recommended)

**macOS/Linux:**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows (PowerShell):**
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

#### Option 2: npm Install

```bash
npm install -g openclaw@latest
# or: pnpm add -g openclaw@latest
```

#### Linux (Ubuntu/Debian) - Detailed

```bash
# Install Node.js 22+ using NodeSource
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version  # Should show v22.x.x

# Install OpenClaw globally
npm install -g openclaw@latest

# Run the onboarding wizard
openclaw onboard --install-daemon
```

**For WSL2 users (Windows)**:
```bash
# WSL2 is strongly recommended for Windows users
# Install Ubuntu from Microsoft Store, then follow Linux instructions above

# Additional WSL2 optimizations
echo '[interop]
appendWindowsPath=false' | sudo tee /etc/wsl.conf

# Restart WSL
wsl --shutdown
```

#### macOS - Detailed

```bash
# Using Homebrew (recommended)
brew install node@22

# Or using Node.js installer from nodejs.org

# Install OpenClaw
npm install -g openclaw@latest

# Run onboarding
openclaw onboard --install-daemon
```

**macOS Permissions Note**: The first time you run OpenClaw, macOS will request various permissions (accessibility, notifications, etc.). Grant these for full functionality.

#### Windows (Native)

Windows native support is limited. **WSL2 is strongly recommended.**

If you must use native Windows:
```powershell
# Install Node.js 22+ from https://nodejs.org/

# Install OpenClaw
npm install -g openclaw@latest

# Note: Some features may be limited on native Windows
```

#### Docker Installation

For isolated deployments or VPS setups:

```bash
# Pull the official image
docker pull openclaw/openclaw:latest

# Run with basic configuration
docker run -d \
  --name openclaw-gateway \
  -p 18789:18789 \
  -v ~/.openclaw:/root/.openclaw \
  -v ~/.openclaw/workspace:/workspace \
  -e NODE_ENV=production \
  openclaw/openclaw:latest

# Or use docker-compose
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  openclaw:
    image: openclaw/openclaw:latest
    container_name: openclaw-gateway
    ports:
      - "18789:18789"
    volumes:
      - ~/.openclaw:/root/.openclaw
      - ~/.openclaw/workspace:/workspace
    environment:
      - NODE_ENV=production
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    restart: unless-stopped
EOF

docker-compose up -d
```

**Docker with Sandbox Support**:
```bash
# Enable sandboxing for Docker deployments
export OPENCLAW_SANDBOX=1
export OPENCLAW_DOCKER_SOCKET=/var/run/docker.sock

# Run with sandbox capability
docker run -d \
  --name openclaw-gateway \
  -p 18789:18789 \
  --privileged \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/.openclaw:/root/.openclaw \
  openclaw/openclaw:latest
```

#### Nix Installation (Declarative)

For reproducible environments:
```bash
# Clone the nix-openclaw repo
git clone https://github.com/openclaw/nix-openclaw.git
cd nix-openclaw

# Enter development shell
nix-shell

# Or install to your profile
nix-env -iA openclaw
```

### Installation Verification

```bash
# Check installation
openclaw --version

# Verify gateway can start
openclaw gateway --port 18789 --verbose

# Run diagnostic
openclaw doctor

# Check gateway status
openclaw gateway status

# Open the Control UI
openclaw dashboard
```

---

## Configuration Basics

### Configuration File Location

OpenClaw uses **JSON5** (JSON with comments) for configuration:

```
~/.openclaw/openclaw.json
```

JSON5 supports:
- Comments (`//` and `/* */`)
- Trailing commas
- Unquoted keys
- Single-quoted strings

### Minimal Configuration

```json5
// ~/.openclaw/openclaw.json
{
  agent: {
    model: "anthropic/claude-sonnet-4-5",
  },
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
    },
  },
}
```

### Configuration Methods

#### 1. Interactive Wizard (Recommended for Beginners)
```bash
openclaw onboard        # Full setup wizard
openclaw configure      # Configuration wizard
```

The onboarding wizard will:
- Check prerequisites
- Configure API keys
- Set up channels
- Install the Gateway daemon
- Guide you through pairing

#### 2. CLI Commands
```bash
# Get current value
openclaw config get agents.defaults.workspace

# Set value
openclaw config set agents.defaults.heartbeat.every "2h"

# Remove value
openclaw config unset tools.web.search.apiKey

# List all config
openclaw config list
```

#### 3. Control UI
Open http://127.0.0.1:18789 and use the **Config** tab for a web-based interface.
The Control UI renders a form from the config schema, with a **Raw JSON** editor as an escape hatch.

#### 4. Direct File Edit
Edit `~/.openclaw/openclaw.json` directly. The Gateway watches the file and applies changes automatically (hot reload).

### Strict Validation Warning

<Warning>
  OpenClaw only accepts configurations that fully match the schema. Unknown keys, malformed types, or invalid values cause the Gateway to **refuse to start**.
</Warning>

When validation fails:
- The Gateway does not boot
- Only diagnostic commands work (`openclaw doctor`, `openclaw logs`, `openclaw health`, `openclaw status`)
- Run `openclaw doctor` to see exact issues
- Run `openclaw doctor --fix` (or `--yes`) to apply repairs

### Essential Configuration Sections

#### Models Configuration
```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["openai/gpt-5.2", "google/gemini-2.5-flash"],
      },
      models: {
        "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
        "openai/gpt-5.2": { alias: "GPT" },
      },
    },
  },
}
```

**Key points:**
- `agents.defaults.models` defines the model catalog and acts as the allowlist for `/model`
- Model refs use `provider/model` format (e.g. `anthropic/claude-opus-4-6`)
- `agents.defaults.imageMaxDimensionPx` controls transcript/tool image downscaling (default `1200`)

#### Workspace Configuration
```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
    },
  },
}
```

#### Session Management
```json5
{
  session: {
    dmScope: "per-channel-peer",  // Options: main, per-peer, per-channel-peer
    reset: {
      mode: "daily",
      atHour: 4,
      idleMinutes: 120,
    },
  },
}
```

**Session scoping options:**
- `"main"`: All DMs share one session
- `"per-peer"`: Separate session per contact
- `"per-channel-peer"`: Separate per channel+contact (recommended for multi-user)

#### Environment Variables

Create `~/.openclaw/.env` for sensitive values:

```bash
# API Keys
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
BRAVE_API_KEY=...
GEMINI_API_KEY=...

# Channel Tokens (alternative to config file)
TELEGRAM_BOT_TOKEN=...
SLACK_BOT_TOKEN=...
DISCORD_BOT_TOKEN=...
```

**Useful environment variables:**
- `OPENCLAW_HOME` - Sets the home directory for internal path resolution
- `OPENCLAW_STATE_DIR` - Overrides the state directory
- `OPENCLAW_CONFIG_PATH` - Overrides the config file path

---

## Setting Up Messaging Bridges

### WhatsApp Setup

WhatsApp integration uses the **Baileys** library for WhatsApp Web connectivity.

#### Step 1: Install WhatsApp Plugin

```bash
# Onboarding will prompt to install automatically
openclaw onboard

# Or install manually
openclaw plugins install @openclaw/whatsapp
```

#### Step 2: Configure Access Policy
```json5
// ~/.openclaw/openclaw.json
{
  channels: {
    whatsapp: {
      enabled: true,
      dmPolicy: "pairing",      // pairing | allowlist | open | disabled
      allowFrom: ["+15551234567"],
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
  },
}
```

**DM Policy Options:**
- `"pairing"` (default): Unknown senders get a pairing code
- `"allowlist"`: Only numbers in `allowFrom` can message
- `"open"`: Anyone can message (requires `allowFrom: ["*"]`)
- `"disabled"`: Ignore all DMs

#### Step 3: Link WhatsApp Account
```bash
# Login via QR code
openclaw channels login --channel whatsapp

# For multiple accounts
openclaw channels login --channel whatsapp --account work
```

#### Step 4: Approve Pairing (if using pairing mode)
```bash
# List pending pairings
openclaw pairing list whatsapp

# Approve a pairing code
openclaw pairing approve whatsapp <CODE>
```

Pairing requests expire after 1 hour. Pending requests are capped at 3 per channel.

#### WhatsApp Deployment Patterns

**Dedicated Number (Recommended):**
```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551234567"],
    },
  },
}
```

This is the cleanest operational mode:
- Separate WhatsApp identity for OpenClaw
- Clearer DM allowlists and routing boundaries
- Lower chance of self-chat confusion

**Personal Number Fallback:**
```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551234567"],
      selfChatMode: true,
    },
  },
}
```

Onboarding supports personal-number mode with self-chat-friendly baseline:
- `dmPolicy: "allowlist"`
- `allowFrom` includes your personal number
- `selfChatMode: true`

### Telegram Setup

#### Step 1: Create Bot
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Create new bot with `/newbot`
3. Copy the bot token

#### Step 2: Configure OpenClaw
```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123456:ABCDEF...",
      dmPolicy: "pairing",
      allowFrom: ["tg:123456789"],
      groups: {
        "*": {
          requireMention: true,
        },
      },
    },
  },
}
```

#### Step 3: Set Webhook (Optional, for production)
```bash
# Set webhook URL
openclaw config set channels.telegram.webhookUrl "https://your-domain.com/webhook"
openclaw config set channels.telegram.webhookSecret "your-secret"
```

### Slack Setup

#### Step 1: Create Slack App
1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Create New App → From scratch
3. Add OAuth scopes: `chat:write`, `im:history`, `groups:history`, `mpim:history`
4. Install to workspace
5. Copy Bot User OAuth Token and App-Level Token

#### Step 2: Configure OpenClaw
```json5
{
  channels: {
    slack: {
      enabled: true,
      botToken: "xoxb-...",
      appToken: "xapp-...",
      dmPolicy: "pairing",
      allowFrom: ["U12345678"],
    },
  },
}
```

### Discord Setup

#### Step 1: Create Bot Application
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. New Application → Bot
3. Enable "Message Content Intent"
4. Copy token

#### Step 2: Configure OpenClaw
```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "MTIzNDU2.Nz...",
      dmPolicy: "pairing",
      allowFrom: ["123456789012345678"],
      guilds: ["123456789012345678"],  // Optional: restrict to specific servers
    },
  },
}
```

### iMessage / BlueBubbles Setup

For macOS users wanting iMessage integration:

**BlueBubbles (Recommended):**
```json5
{
  channels: {
    bluebubbles: {
      enabled: true,
      serverUrl: "http://localhost:12345",
      password: "your-password",
      webhookPath: "/webhook/bluebubbles",
    },
  },
}
```

**Legacy iMessage (macOS only):**
```json5
{
  channels: {
    imessage: {
      enabled: true,
      groups: {
        "*": {
          requireMention: true,
        },
      },
    },
  },
}
```

### Signal Setup

Requires `signal-cli` to be installed:

```bash
# Install signal-cli
# Ubuntu/Debian
sudo apt install signal-cli

# macOS
brew install signal-cli
```

Configure:
```json5
{
  channels: {
    signal: {
      enabled: true,
      phoneNumber: "+15551234567",
      dmPolicy: "pairing",
    },
  },
}
```

### Group Chat Mention Gating

Group messages default to **require mention**. Configure patterns per agent:

```json5
{
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          mentionPatterns: ["@openclaw", "openclaw"],
        },
      },
    ],
  },
  channels: {
    whatsapp: {
      groups: { "*": { requireMention: true } },
    },
  },
}
```

- **Metadata mentions**: native @-mentions (WhatsApp tap-to-mention, Telegram @bot, etc.)
- **Text patterns**: safe regex patterns in `mentionPatterns`
- **Implicit reply-to-bot detection**: reply sender matches bot identity

---

## Troubleshooting Common Issues

### Gateway Won't Start

**Problem**: `openclaw gateway` fails with config errors

**Solution**:
```bash
# Check config validity
openclaw doctor

# Fix common issues
openclaw doctor --fix

# View detailed logs
openclaw logs --follow

# Check gateway status
openclaw gateway status
```

### Channel Connection Issues

**WhatsApp**: 
- Check phone has active internet
- Re-link: `openclaw channels logout whatsapp && openclaw channels login whatsapp`
- Check logs: `openclaw logs | grep whatsapp`
- QR expired? Refresh http://localhost:8555/qr (auto-refreshes every 3s)
- "stream replaced" errors = multiple bridge instances — ensure only one runs

**Telegram**:
- Verify bot token is correct
- Check bot isn't blocked by user
- Ensure "Privacy Mode" is disabled in BotFather settings for group access

**Slack**:
- Verify scopes include `chat:write`
- Check bot is invited to channels
- Ensure App-Level Token is for Socket Mode

### Model API Errors

**Anthropic Rate Limits**:
```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["openai/gpt-5.2"],  // Add fallback
      },
    },
  },
}
```

**Check API Key**:
```bash
# Test API key
curl -H "x-api-key: $ANTHROPIC_API_KEY" \
  https://api.anthropic.com/v1/models
```

### Permission Denied Errors

**Linux/macOS**:
```bash
# Fix permissions
sudo chown -R $USER:$USER ~/.openclaw
chmod 700 ~/.openclaw
```

**Windows/WSL**:
```bash
# In WSL
sudo chown -R $(whoami):$(whoami) ~/.openclaw
```

### Update Issues

```bash
# Update OpenClaw
npm update -g openclaw@latest

# Clear cache if needed
rm -rf ~/.openclaw/.cache

# Restart gateway
openclaw gateway restart
```

### Switching Channels (Stable/Beta/Dev)

```bash
# Switch to beta
openclaw update --channel beta

# Switch to dev
openclaw update --channel dev

# Back to stable
openclaw update --channel stable
```

Channel details:
- **stable**: tagged releases (vYYYY.M.D), npm dist-tag latest
- **beta**: prerelease tags (vYYYY.M.D-beta.N), npm dist-tag beta
- **dev**: moving head of main, npm dist-tag dev

---

## Next Steps

Now that you have OpenClaw installed and configured:

1. **Complete Module 2**: Learn about the SOUL architecture and personalization
2. **Explore Skills**: Run `clawhub list` to see available skills
3. **Set up Heartbeat**: Configure periodic check-ins
4. **Join the Community**: [Discord](https://discord.gg/clawd) for support

---

**Estimated Time**: 30-60 minutes for initial setup
**Cost**: Free (open source) + API usage costs
**Difficulty**: Beginner-friendly with wizard assistance

---

## Quick Reference Card

```bash
# Installation
curl -fsSL https://openclaw.ai/install.sh | bash
npm install -g openclaw@latest

# Onboarding
openclaw onboard --install-daemon

# Gateway management
openclaw gateway status
openclaw gateway start
openclaw gateway stop
openclaw dashboard

# Configuration
openclaw config get <key>
openclaw config set <key> <value>
openclaw doctor
openclaw doctor --fix

# Channel setup
openclaw channels login --channel whatsapp
openclaw pairing list whatsapp
openclaw pairing approve <CODE>

# Diagnostics
openclaw logs --follow
openclaw health
openclaw status
```

**Config file:** `~/.openclaw/openclaw.json`
**Workspace:** `~/.openclaw/workspace/`
**Logs:** `~/.openclaw/logs/`
**Skills:** `~/.openclaw/skills/` and `~/.openclaw/workspace/skills/`
# OpenClaw Complete Documentation Skill

A comprehensive knowledge base skill for OpenClaw, covering installation, configuration, Gateway management, channels, nodes, CLI commands, automation, security, and all core functionality.

## Overview

This skill provides complete documentation and knowledge about OpenClaw - an AI agent Gateway that connects chat applications to programming agents across any operating system. It serves as a comprehensive reference for users and developers working with OpenClaw.

## Features

✅ **Complete Documentation** - Full OpenClaw knowledge base
✅ **Installation & Configuration** - Setup guides and configuration examples
✅ **Gateway Management** - Gateway setup, operation, and troubleshooting
✅ **Multi-Channel Support** - WhatsApp, Telegram, Discord, iMessage, Signal, Slack, and more
✅ **Node Pairing** - iOS and Android device integration
✅ **CLI Command Reference** - Comprehensive command documentation
✅ **Automation** - Cron jobs, heartbeats, webhooks, and hooks
✅ **Security** - Access control, whitelisting, and token management
✅ **Troubleshooting** - Common issues and diagnostic tools
✅ **Best Practices** - Security, performance, and maintenance guidelines
✅ **Advanced Features** - Multi-agent routing, local models, and plugin development
✅ **Remote Access** - Tailscale and SSH remote access methods

## What is OpenClaw?

OpenClaw is a universal AI agent Gateway that bridges chat applications (WhatsApp, Telegram, Discord, etc.) with programming agents, CLI tools, web interfaces, and mobile applications. It provides a single Gateway process to manage all your AI interactions across different platforms.

### Core Architecture

```
Chat Apps + Plugins → Gateway → AI Agents/CLI/Web UI/macOS/iOS/Android
```

The **Gateway** is the single source of truth for sessions, routing, and channel connections.

## Quick Start

### 1. Install OpenClaw

```bash
npm install -g openclaw@latest
```

### 2. Run Onboarding and Install Service

```bash
openclaw onboard --install-daemon
```

### 3. Pair Channels and Start Gateway

```bash
openclaw channels login
openclaw gateway --port 18789
```

### 4. Access Web Control Interface

- **Local**: http://127.0.0.1:18789/
- **Remote**: Access via Tailscale or SSH tunnel

## Supported Channels

### Built-in Channels
- **WhatsApp** - Most commonly used channel
- **Telegram** - Feature-rich bot platform
- **Discord** - Gaming and community platform
- **iMessage** - Apple devices
- **Signal** - Privacy-focused messaging
- **Slack** - Workplace collaboration
- **Google Chat** - Google Workspace integration
- **Matrix** - Decentralized communication

### Plugin Channels (via extensions)
- **Mattermost** - Enterprise collaboration
- **Microsoft Teams** - Microsoft team collaboration
- **IRC** - Internet Relay Chat
- **Feishu** - Lark/Feishu
- **LINE** - LINE messaging
- **Twitch** - Live streaming platform

## Node Capabilities

Pair mobile devices to extend functionality:

```bash
openclaw nodes pair
```

### Supported Devices
- **iOS** - Requires OpenClaw iOS App
- **Android** - Requires OpenClaw Android App

### Node Features
- **Camera Capture** - Remote photography
- **Location** - Device location tracking
- **Audio/Voice** - Recording and voice notes
- **Canvas** - Remote display and control
- **Talk Mode** - Voice interaction

## Automation Features

### Cron Jobs
Schedule periodic tasks:

```bash
openclaw cron create "0 9 * * *" "Good morning"
```

### Heartbeat
Regular status checks ideal for:
- Email monitoring
- Calendar event checking
- Notification review
- Memory maintenance

### Webhooks & Hooks
Receive external events and execute scripts on specific triggers.

## Configuration

Configuration file location: `~/.openclaw/openclaw.json`

### Basic Configuration Example

```json5
{
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: {
        "*": { requireMention: true }
      },
    },
  },
  messages: {
    groupChat: {
      mentionPatterns: ["@openclaw"]
    }
  },
}
```

### Configuration Options
- **allowFrom**: Restrict access to specific phone numbers
- **requireMention**: Require @mentions in group chats
- **mentionPatterns**: Custom mention patterns
- **No modifications**: Use built-in Pi binary, create separate sessions per sender

## CLI Command Reference

### Core Commands

```bash
# Status check
openclaw status

# Gateway management
openclaw gateway --port 18789
openclaw gateway start
openclaw gateway stop
openclaw gateway restart

# Channel management
openclaw channels login
openclaw channels list
openclaw channels connect

# Configuration management
openclaw config get <key>
openclaw config set <key> <value>
openclaw configure

# Log viewing
openclaw logs
openclaw logs --follow

# Skill management
openclaw skills list
openclaw skills install <skill>
openclaw skills uninstall <skill>

# Session management
openclaw sessions list
openclaw sessions info <id>
openclaw sessions clear <id>

# Node management
openclaw nodes list
openclaw nodes pair
openclaw nodes status

# Updates
openclaw update
```

### Wizard Commands

```bash
# Onboarding
openclaw onboard --install-daemon

# Diagnostics
openclaw doctor

# Reset
openclaw reset
```

## Security

### Access Control

```json
{
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
    },
  },
}
```

### Token Management
- Use secrets for sensitive information
- Environment variable support
- Key reference support

### Whitelisting
- Phone number whitelists
- User ID whitelists
- Group whitelists

## Workspace Structure

Default workspace: `~/.openclaw/workspace/`

### Important Files
- `AGENTS.md` - Workspace configuration
- `SOUL.md` - AI personality definition
- `USER.md` - User information
- `MEMORY.md` - Long-term memory
- `HEARTBEAT.md` - Heartbeat tasks
- `TOOLS.md` - Tool configuration

## Skill Management

### Creating Skills

Create skills in `~/.openclaw/workspace/skills/` directory:

```
skills/
└── my-skill/
    ├── SKILL.md
    └── (optional scripts and resources)
```

### SKILL.md Format

```markdown
---
name: my-skill
description: Skill description
---

# Skill Documentation

Content...
```

### Installing Skills

```bash
openclaw skills install ./my-skill
```

## Memory Management

### MEMORY.md
Long-term memory storing important decisions, preferences, and context.

### Daily Notes
`memory/YYYY-MM-DD.md` stores daily logs.

### Memory Maintenance
Regular compression and organization of memory files.

## Troubleshooting

### Diagnostics

```bash
openclaw doctor
```

### Common Issues

1. **Gateway won't start**
   - Check if port is occupied
   - View logs: `openclaw logs`

2. **Channel connection fails**
   - Check network connection
   - Verify credentials
   - Check channel documentation

3. **Session loss**
   - Check session configuration
   - View errors in logs

### Debugging
- **Logs**: `openclaw logs --follow`
- **Status**: `openclaw status`
- **Web UI**: Access http://127.0.0.1:18789/

## Advanced Features

### Multi-Agent Support

```json
{
  agents: {
    my-agent: {
      model: "anthropic/claude-3-opus",
    },
  },
}
```

### Local Models
Use local models with Ollama or vLLM.

### Plugins
Develop custom plugins to extend functionality.

## Remote Access

### Tailscale
Access remote Gateway via Tailscale:

```bash
openclaw gateway --tailscale
```

### SSH
Access via SSH tunnel:

```bash
ssh -L 18789:localhost:18789 user@remote
```

## Best Practices

### Security
1. Use whitelists to restrict access
2. Regularly update OpenClaw
3. Don't hardcode secrets in configuration
4. Use secrets management for sensitive information

### Performance
1. Configure session pruning appropriately
2. Use memory compression
3. Regularly clean up old sessions

### Maintainability
1. Use version control for workspace management
2. Document custom configurations
3. Regularly backup important files

## Documentation Resources

### Official Documentation
- **Homepage**: https://docs.openclaw.ai/zh-CN
- **Document Index**: https://docs.openclaw.ai/llms.txt
- **Community**: https://discord.com/invite/clawd

### Key Documentation Areas
- Getting Started Guide
- Gateway Configuration
- Channel Setup
- Node Pairing
- Automation
- Security
- Troubleshooting

## Updates

```bash
openclaw update
```

## Uninstallation

```bash
openclaw uninstall
```

## How to Use This Skill

This skill is automatically triggered when OpenClaw-related questions are asked in conversation. It provides comprehensive information and guidance for all aspects of OpenClaw usage, development, and administration.

## License

This skill is based on OpenClaw official documentation and is provided as a knowledge base for the OpenClaw community.

## Source
- **Official Documentation**: https://docs.openclaw.ai/zh-CN
- **Document Index**: https://docs.openclaw.ai/llms.txt

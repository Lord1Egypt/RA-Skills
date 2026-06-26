---
name: openclaw-docs
description: Complete OpenClaw documentation reference. Use when you need information about OpenClaw configuration, CLI commands, channel setup, tools, concepts, or any OpenClaw-related questions. Includes 264 pages covering automation, channels (WhatsApp/Telegram/Discord/iMessage/Signal/Slack/etc), CLI commands, core concepts, gateway configuration, installation guides, model providers, tools, and more.
---

# OpenClaw Documentation Reference

This skill provides comprehensive access to the entire OpenClaw documentation (https://docs.openclaw.ai/) with 264 pages organized by topic.

## Quick Navigation

### 🚀 Getting Started
- [references/index.md](references/index.md) - Overview
- [references/start/getting-started.md](references/start/getting-started.md) - Quick start guide
- [references/start/setup.md](references/start/setup.md) - Full setup
- [references/start/wizard.md](references/start/wizard.md) - Setup wizard
- [references/start/bootstrapping.md](references/start/bootstrapping.md) - Bootstrapping

### 📦 Installation
- [references/install.md](references/install.md) - Installation overview
- [references/install/node.md](references/install/node.md) - Node.js installation
- [references/install/docker.md](references/install/docker.md) - Docker installation
- [references/install/ansible.md](references/install/ansible.md) - Ansible deployment
- [references/install/updating.md](references/install/updating.md) - Updating OpenClaw

### 🔧 CLI Commands
- [references/cli.md](references/cli.md) - CLI overview
- [references/cli/gateway.md](references/cli/gateway.md) - Gateway management
- [references/cli/configure.md](references/cli/configure.md) - Configuration
- [references/cli/sessions.md](references/cli/sessions.md) - Session management
- [references/cli/status.md](references/cli/status.md) - Status checks
- [references/cli/doctor.md](references/cli/doctor.md) - Diagnostics

### 📱 Channels
- [references/channels.md](references/channels.md) - Channel overview
- [references/channels/whatsapp.md](references/channels/whatsapp.md) - WhatsApp
- [references/channels/telegram.md](references/channels/telegram.md) - Telegram
- [references/channels/discord.md](references/channels/discord.md) - Discord
- [references/channels/imessage.md](references/channels/imessage.md) - iMessage
- [references/channels/signal.md](references/channels/signal.md) - Signal
- [references/channels/slack.md](references/channels/slack.md) - Slack
- [references/channels/feishu.md](references/channels/feishu.md) - Feishu/Lark

### 🛠️ Tools
- [references/tools.md](references/tools.md) - Tools overview
- [references/tools/exec.md](references/tools/exec.md) - Exec tool
- [references/tools/browser.md](references/tools/browser.md) - Browser automation
- [references/tools/skills.md](references/tools/skills.md) - Skills system
- [references/tools/subagents.md](references/tools/subagents.md) - Sub-agents

### ⚙️ Gateway
- [references/gateway.md](references/gateway.md) - Gateway overview
- [references/gateway/configuration.md](references/gateway/configuration.md) - Configuration
- [references/gateway/authentication.md](references/gateway/authentication.md) - Auth setup
- [references/gateway/remote.md](references/gateway/remote.md) - Remote access
- [references/gateway/security.md](references/gateway/security.md) - Security

### 🤖 Model Providers
- [references/providers.md](references/providers.md) - Providers overview
- [references/providers/anthropic.md](references/providers/anthropic.md) - Anthropic/Claude
- [references/providers/openai.md](references/providers/openai.md) - OpenAI
- [references/providers/openrouter.md](references/providers/openrouter.md) - OpenRouter
- [references/providers/litellm.md](references/providers/litellm.md) - LiteLLM

### 🧠 Concepts
- [references/concepts/architecture.md](references/concepts/architecture.md) - Architecture
- [references/concepts/session.md](references/concepts/session.md) - Sessions
- [references/concepts/memory.md](references/concepts/memory.md) - Memory
- [references/concepts/multi-agent.md](references/concepts/multi-agent.md) - Multi-agent
- [references/concepts/models.md](references/concepts/models.md) - Models

### 🔄 Automation
- [references/automation/cron-jobs.md](references/automation/cron-jobs.md) - Cron jobs
- [references/automation/hooks.md](references/automation/hooks.md) - Hooks
- [references/automation/webhook.md](references/automation/webhook.md) - Webhooks

### ❓ Help
- [references/help/faq.md](references/help/faq.md) - FAQ
- [references/help/troubleshooting.md](references/help/troubleshooting.md) - Troubleshooting
- [references/help/environment.md](references/help/environment.md) - Environment variables

## Directory Structure

```
references/
├── automation/     # Cron, hooks, webhooks, polling
├── channels/       # WhatsApp, Telegram, Discord, etc.
├── cli/            # All CLI commands
├── concepts/       # Architecture, sessions, memory
├── experiments/    # Experimental features
├── gateway/        # Gateway configuration
├── help/           # FAQ, troubleshooting
├── install/        # Installation guides
├── nodes/          # Mobile/desktop nodes
├── platforms/      # Platform-specific docs
├── plugins/        # Plugin documentation
├── providers/      # Model provider configs
├── reference/      # Templates and references
├── security/       # Security documentation
├── start/          # Getting started guides
├── tools/          # Tool documentation
└── web/            # Web UI documentation
```

## Usage Tips

1. **Quick reference**: Check the category markdown files (e.g., `cli.md`, `channels.md`) for overviews
2. **Deep dive**: Navigate to specific subdirectories for detailed documentation
3. **Search**: Use grep or file search to find specific topics across all files

## Source

All documentation sourced from https://docs.openclaw.ai/
Last updated: 2026-02-17

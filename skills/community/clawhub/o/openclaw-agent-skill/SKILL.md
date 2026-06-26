---
name: openclaw
description: >
  OpenClaw development assistant, built by Michel Costa, co-founder of Brabaflow — AI-Native Agency
  (brabaflow.ai). Use this skill when the user asks about OpenClaw — a self-hosted gateway that
  connects chat apps (WhatsApp, Telegram, Discord, iMessage, etc.) to AI coding agents. Covers
  configuration, channels, providers, tools, plugins, deployment, CLI commands, and all aspects
  of OpenClaw development. 333 pages of verbatim official documentation from docs.openclaw.ai.
trigger: >
  Use when user mentions OpenClaw, openclaw, or asks about:
  configuring AI agent gateways, connecting chat platforms to AI agents,
  WhatsApp/Telegram/Discord bot setup via OpenClaw, OpenClaw CLI commands,
  OpenClaw gateway configuration, OpenClaw plugins, OpenClaw skills,
  OpenClaw deployment, or any topic covered by docs.openclaw.ai.
author: Brabaflow — AI-Native Agency (brabaflow.ai) | Michel Costa
source: docs.openclaw.ai (333 pages, verbatim extraction, 2026-03-09)
---

# OpenClaw Development Assistant

You are an expert OpenClaw development assistant. Your knowledge comes from the **official OpenClaw documentation** (docs.openclaw.ai), stored verbatim in the `docs/` folder next to this file.

## How to Use This Skill

When the user asks about OpenClaw, follow these steps:

1. **Identify the domain** of the question from the index below
2. **Read the corresponding file** from the `docs/` folder (path relative to this SKILL.md)
3. **Answer using the exact documentation** — do not paraphrase code blocks, configuration examples, or CLI commands
4. If the question spans multiple domains, read multiple files
5. Always cite which doc section your answer comes from

## Documentation Index

All files are in the `docs/` folder relative to this SKILL.md. Each file contains the **verbatim original documentation** from docs.openclaw.ai.

### 01-core-concepts.md — Core Concepts & Architecture (42 pages)
**Read this when the user asks about:**
- What OpenClaw is, how it works, architecture overview
- Agent loop, sessions, memory, context window
- Compaction, streaming, messages, models, model selection
- Model providers overview, model failover
- Markdown formatting, TypeBox schemas, timezones
- Usage tracking, typing indicators, features list
- Quick start, getting started, setup from source
- Date and time handling, showcase, documentation directory

### 02-installation.md — Installation & Setup (11 pages)
**Read this when the user asks about:**
- Installing OpenClaw (installer scripts, npm, from source)
- Docker, Podman, Nix, Ansible installation
- Bun (experimental), Node.js setup
- Updating, migrating to new machine, uninstalling
- Development channels (stable/beta/dev)

### 03-gateway.md — Gateway (31 pages)
**Read this when the user asks about:**
- Gateway configuration, runbook, protocol (WebSocket)
- Authentication (OAuth, API keys, setup-token)
- Secrets management, SecretRefs
- Health checks, heartbeat, doctor
- Sandboxing, tool policy, elevated mode comparison
- Gateway lock, background processes
- OpenAI HTTP API, OpenResponses API, tools-invoke API
- CLI backends, local models
- Discovery, transports, pairing, Bonjour
- Remote gateway setup, trusted proxy auth
- Logging, network hub
- Auth credential semantics

### 04-channels.md — Channels / Chat Platforms (29 pages)
**Read this when the user asks about:**
- WhatsApp (Web, Cloud API, Business)
- Telegram (Bot API, groups, media)
- Discord (bot setup, threads, slash commands)
- Slack (app setup, events, threading)
- Signal (signal-cli, groups)
- iMessage (macOS native, BlueBubbles)
- Matrix, IRC, Google Chat, Mattermost
- Microsoft Teams, LINE, Feishu/Lark
- Twitch, Nostr, Tlon, Synology Chat, Nextcloud Talk, Zalo
- Channel configuration, capabilities, DM pairing

### 05-providers.md — Model Providers (29 pages)
**Read this when the user asks about:**
- Anthropic (Claude, API key, setup-token, thinking, caching)
- OpenAI (GPT, API key, Codex subscription)
- Amazon Bedrock, Ollama, OpenRouter
- Mistral, MiniMax (M2/M2.5), NVIDIA
- Venice AI, Together AI, Qwen
- Moonshot/Kimi, Deepgram (audio transcription)
- Cloudflare AI Gateway, Vercel AI Gateway
- Kilocode, GitHub Copilot, Hugging Face
- vLLM, LiteLLM, Synthetic
- Xiaomi MiMo, Z.AI/GLM, Qianfan
- OpenCode Zen, Claude Max API Proxy
- Model provider quickstart, provider configuration

### 06-tools.md — Agent Tools (31 pages)
**Read this when the user asks about:**
- Browser control (OpenClaw-managed Chrome/Brave/Edge)
- Browser login, Chrome extension relay
- Browser troubleshooting (Linux, WSL2)
- Exec tool (shell commands, allowlist, safe bins)
- Exec approvals, elevated mode
- Skills (creating, config, ClawHub registry)
- Slash commands, sub-agents, ACP agents
- PDF tool, web tools (search, fetch)
- Diffs tool, apply_patch tool
- Lobster workflows, LLM task tool
- Thinking levels, loop detection
- Agent send (direct agent runs)
- Firecrawl, Brave Search, Perplexity Sonar
- Text-to-Speech (TTS)

### 07-automation.md — Automation & Workflows (8 pages)
**Read this when the user asks about:**
- Cron jobs (Gateway scheduler)
- Heartbeat (periodic awareness)
- Hooks (event-driven automations)
- Webhooks (HTTP endpoint triggers)
- Gmail Pub/Sub integration
- Polls (channel-based polling)
- Auth monitoring
- Cron vs heartbeat comparison

### 08-plugins.md — Plugins & Extensions (6 pages)
**Read this when the user asks about:**
- Plugin system, architecture, SDK
- Plugin manifest (openclaw.plugin.json)
- Plugin agent tools
- Voice Call plugin
- Zalo Personal plugin
- OpenProse (workflow format)
- Plugin distribution (npm)

### 09-nodes.md — Nodes & Devices (8 pages)
**Read this when the user asks about:**
- Audio and voice notes (transcription)
- Camera capture (iOS, Android, macOS)
- Talk mode (continuous voice conversation)
- Voice wake (wake words)
- Location command
- Media understanding (image/audio/video)
- Image and media support
- Node troubleshooting

### 10-platforms-macos.md — Platforms: macOS (20 pages)
**Read this when the user asks about:**
- macOS menu-bar app
- macOS app remote control
- Gateway on macOS (launchd)
- macOS skills, menu bar status
- Voice overlay, WebChat in macOS
- Gateway lifecycle (child process)
- macOS permissions (TCC)
- Code signing, Peekaboo Bridge
- Canvas (agent UI), IPC architecture (XPC)
- macOS dev setup, voice wake, release process
- macOS logging, health checks

### 11-platforms-mobile.md — Platforms: Mobile (2 pages)
**Read this when the user asks about:**
- iOS app (pairing, discovery, canvas, voice wake)
- Android app (support snapshot, system control, connection)

### 12-platforms-desktop.md — Platforms: Desktop (2 pages)
**Read this when the user asks about:**
- Linux (Gateway, systemd user unit)
- Windows / WSL2 (installation, portproxy, auto-start)

### 13-deploy.md — Deploy & Cloud Hosting (12 pages)
**Read this when the user asks about:**
- Hetzner VPS deployment
- GCP Compute Engine deployment
- Fly.io deployment
- Railway deployment
- Render deployment (Blueprint)
- Northflank deployment
- exe.dev VM deployment
- DigitalOcean droplet
- Oracle Cloud (Always Free tier)
- Raspberry Pi (always-on Gateway)
- macOS VMs (Lume)
- VPS hosting overview

### 14-cli.md — CLI Reference (47 pages)
**Read this when the user asks about:**
- Any `openclaw` CLI command
- CLI overview, global flags, command tree
- Commands: agent, agents, acp, approvals, backup
- Commands: browser, channels, config, configure, cron
- Commands: daemon, dashboard, devices, directory, dns, docs, doctor
- Commands: gateway, health, hooks, logs, memory, message, models
- Commands: nodes, onboard, pairing, plugins, qr, reset
- Commands: sandbox, secrets, security, sessions, setup, skills
- Commands: status, system, tui, uninstall, update, voicecall, webhooks
- Shell completion

### 15-web-uis.md — Web UIs (4 pages)
**Read this when the user asks about:**
- WebChat (Gateway WebSocket UI)
- Dashboard (Control UI)
- TUI (Terminal UI)

### 16-security.md — Security (2 pages)
**Read this when the user asks about:**
- Threat model (MITRE ATLAS framework)
- Contributing to OpenClaw security
- Security threat analysis

### 17-templates.md — Templates & Workspace Files (8 pages)
**Read this when the user asks about:**
- AGENTS.md template (workspace config)
- IDENTITY.md template (agent identity)
- SOUL.md template (agent personality)
- USER.md template (user info)
- TOOLS.md template (tool notes)
- HEARTBEAT.md template
- BOOT.md template (startup instructions)
- BOOTSTRAP.md template (first-run conversation)

### 18-reference.md — Reference (15 pages)
**Read this when the user asks about:**
- Default AGENTS.md configuration
- Onboarding wizard reference
- Token use and costs
- Prompt caching configuration
- Transcript hygiene (provider fixups)
- Session management deep dive
- SecretRef credential surface
- RPC adapters (signal-cli, imsg)
- Device model database
- API usage and costs
- Tests and CI pipeline
- Release checklist
- Pi development workflow

### 19-troubleshooting.md — Help & Troubleshooting (8 pages)
**Read this when the user asks about:**
- FAQ (comprehensive)
- General troubleshooting
- Testing (Vitest suites, Docker runners)
- Debugging
- Environment variables
- Diagnostics flags
- Helper scripts
- Node + tsx crash issues

### 20-experiments.md — Experiments & Design Docs (10 pages)
**Read this when the user asks about:**
- Internal plans and proposals
- PTY and process supervision plan
- Model config exploration
- Workspace memory research
- Session binding plan
- ACP thread-bound agents plan
- ACP unified streaming refactor
- Browser evaluate CDP refactor
- OpenResponses gateway plan
- Onboarding config protocol
- Kilo gateway integration design

## Important Rules

1. **NEVER paraphrase code blocks or configuration examples** — use them exactly as they appear in the docs
2. **NEVER invent configuration keys or CLI flags** — only reference what exists in the documentation
3. When showing config examples, include the full context (surrounding keys, comments) from the docs
4. If the docs mention a version requirement or caveat, always include it in your answer
5. If you cannot find the answer in the documentation files, say so explicitly — do not guess
6. Always mention which documentation section the answer comes from
7. For CLI commands, always show the exact syntax from the docs
8. Each `docs/` file has `<!-- SOURCE: url -->` comments indicating the original page URL — you can reference these for the user

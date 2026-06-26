---
name: openclaw-expert
description: "Complete OpenClaw reference: architecture, gateway, CLI (50+ commands), 25+ channels, 25+ providers, tools, plugins, automation, security, installation, platforms. Use when answering OpenClaw config/setup/behavior questions, debugging issues (gateway, channels, failover, sandboxing, heartbeat, cron), writing openclaw.json, setting up channels (WhatsApp/Telegram/Discord/Signal/Slack/iMessage/etc.), configuring providers (Anthropic/OpenAI/Gemini/xAI/Ollama/MiniMax/etc.), managing agents/sessions/memory/workspace, CLI commands, automation (cron/hooks/heartbeat/tasks), installing on any platform (macOS/Linux/Windows/Docker/VPS/RPi/iOS/Android), using tools (exec/browser/image/video/TTS/music/sub-agents/ACP), plugins, security hardening, troubleshooting, or gateway protocol. NOT for writing OpenClaw source code."
---

# OpenClaw Expert Skill

Complete OpenClaw reference compiled from 426+ official documentation pages.
12 reference files covering every aspect of the platform.

## Reference File Index

Load the relevant file based on the user's question. **Read only what's needed.**

| # | File | Topics | Lines |
|---|------|--------|-------|
| 01 | `references/01-core-concepts.md` | Architecture, agent runtime/loop, workspace, active memory, compaction, context engine, delegate architecture, dreaming, experimental features, markdown, memory (builtin/honcho/QMD/search), messages, model failover, model providers, models CLI, multi-agent routing, OAuth, presence, QA E2E automation, command queue, retry policy, sessions (management/pruning/tools), SOUL.md personality, streaming/chunking, system prompt, timezones, TypeBox schema, typing indicators, usage tracking, GPT-5.4/Codex agentic parity, Pi integration architecture, OpenProse | 2647 |
| 02 | `references/02-gateway.md` | Gateway runbook, authentication, background process, Bonjour/mDNS discovery, CLI backends, config (agents/channels/tools), configuration reference/examples, diagnostics export, doctor, gateway lock, health checks, heartbeat, local models, logging, multiple gateways, network model, OpenAI Chat Completions HTTP API, OpenResponses HTTP API, OpenShell, gateway-owned pairing, gateway protocol, remote access/setup, sandboxing (Docker/SSH/OpenShell), secrets management, security audit checks | 1538 |
| 03 | `references/03-cli.md` | All 50+ CLI subcommands: ACP, agent, agents, approvals/exec-policy, backup, browser, channels, completion, config, configure, cron, dashboard, devices, directory, DNS, docs, doctor, flows/tasks, gateway, health, hooks, infer/capability, logs, MCP, memory, message, models, node, nodes, onboard, pairing, plugins, proxy, QR, reset, sandbox, secrets, security, sessions, setup, skills, status, system, tasks, TUI/chat/terminal, uninstall, update, voicecall, webhooks, wiki + quick reference table | 3299 |
| 04 | `references/04-channels.md` | Channel overview/routing, groups, pairing, broadcast groups, location parsing, QA channel, BlueBubbles, Discord, Feishu/Lark, Google Chat, iMessage (legacy), IRC, LINE, Matrix (+ push rules), Mattermost, MS Teams, Nextcloud Talk, Nostr, QQ Bot, Signal, Slack, Synology Chat, Telegram, Tlon/Urbit, Twitch, WeChat, WhatsApp, Zalo (bot + personal), DM/group policy, multi-account, troubleshooting, feature comparison table | 2765 |
| 05 | `references/05-providers.md` | Anthropic, OpenAI, Gemini, OpenRouter, MiniMax, DeepSeek, Groq, Ollama, Together AI, Mistral, Fireworks, xAI, Perplexity, Amazon Bedrock, Cloudflare AI Gateway, Z.AI/GLM (Zhipu), 40+ additional providers (Arcee, Bedrock Mantle, Chutes, Claude Max Proxy, ComfyUI, GitHub Copilot, Gradium, Kilocode, LiteLLM, SGLang, Synthetic, Tencent, Vercel AI GW, vLLM, Volcengine, Vydra, Xiaomi, and more), model selection/failover config, env vars quick reference | 1689 |
| 06 | `references/06-tools.md` | Tool architecture, exec, code_execution, browser, message (agent send), image_generate, video_generate, music_generate, tts, web_fetch, sessions_spawn (sub-agents), web_search, tool configuration, gateway tool, memory_search/memory_get, session_status, plugin-provided tools | 1448 |
| 07 | `references/07-plugins.md` | Plugin system (install/develop/lifecycle), bundled plugins, voice-call, music-2.6, channel plugins, SDK conventions, registerCliBackend, registerAgentToolResultMiddleware, createOptionalChannelSetupSurface | 1190 |
| 08 | `references/08-automation.md` | Cron jobs (create/list/edit/delete/run/logs/doctor), background tasks (ledger), task flow, hooks (HTTP webhooks), standing orders, program examples (weekly status, content/social, financial, system monitoring), heartbeat, isolated sessions, failureDestination, model switch auth, Gmail PubSub, how they work together | 948 |
| 09 | `references/09-installation.md` | Getting started, updating, Docker (SSH/OpenShell sandbox, HEALTHCHECK, shared-network, VM runtime), Nix, Raspberry Pi, uninstall, onboarding wizard, VPS/Linux server deployment, migration guide, platform notes, Control UI custom build | 1019 |
| 10 | `references/10-security-and-misc.md` | Security model, exec approvals, sandbox modes, autoApproveCidrs, trusted-proxy, audit checks, FAQ, troubleshooting (gateway probe, doctor, channels --probe), debugging (watcher, PI_RAW_STREAM), env vars, scripts reference, nodes (remote exec, token rotation, SecretRef), diagnostics (export/recorder/privacy/flags), CI pipeline, RPC adapters | 1226 |
| 11 | `references/11-platforms.md` | macOS (app, discovery, --json), iOS (APNS relay, autoApproveCidrs, relay refresh), Android (autoApproveCidrs, foreground service, auto-reconnect, wide-area discover), Windows (companion, source dev loop, status), Linux (exe.dev, enable-linger), VPS hosting (shared agent, nodes, TimeoutStartSec), Web UI — Control UI (identity, auth gating, approval upgrade, base-hash guard, SecretRef preflight, abort, optimistic messages, compact button, Talk WebRTC, cron panel, schema.lookup, embedSandbox, chat.inject, config.apply) + WebChat (maxChars, abort metadata, tools panel) | 965 |
| 12 | `references/12-reference.md` | Configuration system overview, full config schema (gateway/agents/session/channels/cron/hooks/browser/UI/diagnostics/env), agent config reference, heartbeat reference (directPolicy/lightContext/isolatedSession/activeHours/ackMaxChars/multi-account/per-agent merge), workspace file map (BOOT.md hooks, bootstrap size limits, sandbox seed, Git backup), session management (threadBindings/maintenance/identityLinks), authentication (trusted-proxy fail-closed, HTTP API), gateway WS protocol (handshake/framing/roles/scopes/broadcast/RPC method families incl. diagnostics/secrets/sessions/approval/pairing), RPC adapters, CLI reference, onboarding wizard reference (providers table incl. MiniMax/StepFun/Synthetic/Moonshot/Kimi), file locations, env vars (OOM_SCORE_ADJ/PLUGIN_STAGE_DIR/ALLOW_INSECURE_PRIVATE_WS/PI_RAW_STREAM/DEBUG_TIMING/NODE_COMPILE_CACHE) | 1546 |

## Routing Guide

Match the user's question to the best starting file(s). Many topics span multiple files — follow cross-references.

| Question Pattern | Start With | Then Check |
|---|---|---|
| Configuration / openclaw.json schema | `12-reference.md` | `02-gateway.md` |
| How do I set up X channel? | `04-channels.md` | |
| How do I configure X provider? | `05-providers.md` | |
| CLI command help / "how do I run..." | `03-cli.md` | |
| Debugging / "not working" / errors | `10-security-and-misc.md` | `03-cli.md` (doctor/probe) |
| Heartbeat config / behavior | `12-reference.md` (heartbeat ref) | `08-automation.md`, `02-gateway.md` |
| Cron jobs / scheduled tasks | `08-automation.md` | `03-cli.md` (cron CLI) |
| Hooks / webhooks | `08-automation.md` | `03-cli.md` (hooks CLI) |
| Standing orders / task flow | `08-automation.md` | |
| Installation / getting started | `09-installation.md` | `11-platforms.md` |
| Docker setup | `09-installation.md` | `02-gateway.md` (sandboxing) |
| VPS / headless / PM2 / systemd | `09-installation.md` | `11-platforms.md` |
| Platform-specific apps (macOS/iOS/Android/Windows) | `11-platforms.md` | |
| Control UI / WebChat / Web UI | `11-platforms.md` | |
| Security / sandboxing / exec approvals | `10-security-and-misc.md` | `02-gateway.md`, `03-cli.md` |
| Tools (exec/browser/image/video/TTS/music) | `06-tools.md` | |
| Sub-agents / ACP / sessions_spawn | `06-tools.md` | `01-core-concepts.md` |
| Plugins (install/develop/voice-call/music) | `07-plugins.md` | |
| Architecture / how OpenClaw works | `01-core-concepts.md` | |
| Memory systems (builtin/honcho/QMD) | `01-core-concepts.md` | `03-cli.md` (memory CLI) |
| Agent workspace / bootstrap files | `01-core-concepts.md` | `12-reference.md` (workspace ref) |
| Sessions / multi-agent / routing | `01-core-concepts.md` | `12-reference.md` (session ref) |
| Model failover / retry / fallback chains | `01-core-concepts.md` | `05-providers.md` |
| System prompt / SOUL.md / personality | `01-core-concepts.md` | |
| Streaming / typing indicators / presence | `01-core-concepts.md` | |
| Usage tracking / token costs | `01-core-concepts.md` | |
| Gateway protocol / WebSocket RPC | `12-reference.md` | `02-gateway.md` |
| Nodes / remote exec / token rotation | `10-security-and-misc.md` | `12-reference.md` |
| Diagnostics / export / recorder | `10-security-and-misc.md` | |
| Environment variables | `10-security-and-misc.md` | `12-reference.md` |
| Migration / updating | `09-installation.md` | |
| Bonjour / mDNS / discovery | `02-gateway.md` | |
| OpenAI-compatible API / OpenResponses | `02-gateway.md` | |
| GPT-5.4 / Codex parity / strict-agentic | `01-core-concepts.md` | |
| Pi integration / createAgentSession | `01-core-concepts.md` | |
| OpenProse / .prose workflows | `01-core-concepts.md` | `07-plugins.md` |
| FAQ | `10-security-and-misc.md` | |

## Key Quick-Reference

### Config File Location
`~/.openclaw/openclaw.json` (JSON5 with comments/trailing commas)

### Essential CLI Commands
```bash
openclaw onboard          # Interactive setup
openclaw doctor           # Diagnose issues
openclaw doctor --fix     # Auto-repair
openclaw gateway start    # Start daemon
openclaw gateway status   # Check status
openclaw status --deep    # Full health probe
openclaw config get <path>    # Read config value
openclaw config set <path> <value>  # Write config value
openclaw cron list        # List cron jobs
openclaw models list      # List available models
openclaw models scan      # Probe all configured models
```

### Model Format
Always `provider/model` — e.g. `anthropic/claude-sonnet-4-6`, `openai/gpt-5.4`, `minimax/MiniMax-M2.7`

### DM Policy Options
`pairing` (default) → `allowlist` → `open` → `disabled`

### Sandbox Modes
`off` (default) | `non-main` | `all` — scope: `session` | `agent` | `shared`

### Heartbeat Defaults
- Interval: `30m` (or `1h` for Anthropic OAuth/token auth)
- Target: `none` (set `last` for delivery to last contact)
- Reply `HEARTBEAT_OK` when nothing needs attention

### Session Scoping
`main` | `per-peer` | `per-channel-peer` (recommended) | `per-account-channel-peer`

### File Precedence (workspace context)
Bootstrap files loaded every session: `AGENTS.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`, `TOOLS.md`, `HEARTBEAT.md`
Per-file limit: `bootstrapMaxChars` (default 12000), total: `bootstrapTotalMaxChars` (default 60000)

## Grep Patterns for Efficient Lookup

All reference files are large. Use targeted reads instead of loading entire files:

```bash
# Find a specific topic's section
grep -n '^## \|^### ' references/01-core-concepts.md   # List all headings
grep -n 'heartbeat' references/12-reference.md          # Find heartbeat mentions
grep -n '^## Telegram' references/04-channels.md         # Jump to Telegram section
grep -n '^## Anthropic' references/05-providers.md       # Jump to Anthropic section
```

**Strategy for large files:**
1. Read the first 40 lines (TOC or section overview) to locate the heading
2. `grep -n '^## TARGET'` to find the line number
3. Read only that section with offset/limit

## Common Multi-File Lookups

Some topics are spread across files. Read in this order:

| Topic | Primary | Secondary | Tertiary |
|-------|---------|-----------|----------|
| Heartbeat | `12-reference.md` §Heartbeat Reference | `08-automation.md` §Heartbeat | `02-gateway.md` §Heartbeat |
| Sandboxing | `02-gateway.md` §Sandboxing | `10-security-and-misc.md` §Security | `03-cli.md` §Sandbox |
| Memory | `01-core-concepts.md` §Memory | `03-cli.md` §Memory | `07-plugins.md` §Memory Plugins |
| Exec approvals | `10-security-and-misc.md` §Security | `03-cli.md` §Approvals | `11-platforms.md` §Control UI |
| Docker | `09-installation.md` §Docker | `02-gateway.md` §Sandboxing | |
| WebSocket | `12-reference.md` §Gateway Protocol | `02-gateway.md` §Gateway Protocol | `01-core-concepts.md` §TypeBox |

## Notes

- All 12 reference files have a Table of Contents at the top — read that first to locate the relevant section.
- Cross-reference between files is common. The routing guide and multi-file lookup table above cover the main overlaps.
- All content verified against live docs at docs.openclaw.ai as of April 2026.

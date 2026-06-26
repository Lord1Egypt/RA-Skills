# 🧠 OpenClaw Expert Skill

> The most comprehensive OpenClaw reference available — 20,000+ lines distilled from 426+ official documentation pages into 12 structured reference files.

[![Skill Valid](https://img.shields.io/badge/skill-valid-brightgreen)](https://clawhub.ai)
[![Lines of Reference](https://img.shields.io/badge/reference_lines-20%2C446-blue)]()
[![Docs Coverage](https://img.shields.io/badge/docs_coverage-426%2B_pages-orange)]()
[![Last Updated](https://img.shields.io/badge/updated-April_2026-yellow)]()

---

## What Is This?

An **AgentSkill** for [OpenClaw](https://github.com/openclaw/openclaw) that turns any AI agent into an OpenClaw expert. Once installed, your agent can answer detailed questions about OpenClaw's architecture, configuration, CLI, channels, providers, tools, plugins, security, installation, and more — without needing internet access or doc lookups.

Think of it as a **compressed, searchable brain** containing everything in [docs.openclaw.ai](https://docs.openclaw.ai), organized for fast agent retrieval.

---

## 📊 Coverage at a Glance

| Metric | Value |
|--------|-------|
| **Reference files** | 12 |
| **Total lines** | 20,446 |
| **H2 sections** | 297 |
| **H3 subsections** | 1,396 |
| **Official doc pages covered** | 426+ |
| **Providers documented** | 52+ |
| **Channels documented** | 25+ |
| **CLI commands documented** | 50+ |
| **Config schema entries** | Full `openclaw.json` schema |
| **Last verified against live docs** | April 25, 2026 |

---

## 📁 Reference File Map

Each file covers a focused domain. The agent loads **only the relevant file** based on the user's question — not all 20K lines at once.

| # | File | What It Covers | Lines |
|---|------|----------------|-------|
| 01 | [`01-core-concepts.md`](references/01-core-concepts.md) | Architecture, agent runtime/loop, workspace, active memory, compaction, context engine, delegate architecture, dreaming, experimental features, markdown rendering, memory engines (builtin/Honcho/QMD/search), messages, model failover, model providers, models CLI, multi-agent routing, OAuth, presence, QA E2E automation, command queue, retry policy, sessions (management/pruning/tools), SOUL.md personality, streaming/chunking, system prompt, timezones, TypeBox schema, typing indicators, usage tracking, GPT-5.4/Codex agentic parity, Pi integration architecture, OpenProse | 2,662 |
| 02 | [`02-gateway.md`](references/02-gateway.md) | Gateway runbook, authentication, background process, Bonjour/mDNS, CLI backends, config deep-dives, diagnostics export, doctor, gateway lock, health checks, heartbeat, local models, logging, multiple gateways, network model, OpenAI-compatible HTTP API, OpenResponses HTTP API, OpenShell, pairing, gateway protocol, remote access, sandboxing (Docker/SSH/OpenShell), secrets management, security audit checks | 1,579 |
| 03 | [`03-cli.md`](references/03-cli.md) | All 50+ CLI subcommands with full syntax, flags, examples, and edge cases. ACP, agent, agents, approvals, backup, browser, channels, completion, config, configure, cron, dashboard, devices, directory, DNS, docs, doctor, flows, gateway, health, hooks, infer, logs, MCP, memory, message, models, node, nodes, onboard, pairing, plugins, proxy, QR, reset, sandbox, secrets, security, sessions, setup, skills, status, system, tasks, TUI, uninstall, update, voicecall, webhooks, wiki | 3,299 |
| 04 | [`04-channels.md`](references/04-channels.md) | Channel architecture, routing, groups, pairing, broadcast. Per-channel guides: BlueBubbles, Discord, Feishu/Lark, Google Chat, iMessage, IRC, LINE, Matrix, Mattermost, MS Teams, Nextcloud Talk, Nostr, QQ Bot, Signal, Slack, Synology Chat, Telegram, Tlon/Urbit, Twitch, WeChat, WhatsApp, Zalo. DM/group policy, multi-account, troubleshooting, feature comparison table | 2,765 |
| 05 | [`05-providers.md`](references/05-providers.md) | In-depth: Anthropic, OpenAI, Gemini, OpenRouter, MiniMax, DeepSeek, Groq, Ollama, Together AI, Mistral, Fireworks, xAI, Perplexity, Amazon Bedrock, Cloudflare AI Gateway, Z.AI/GLM. Additional: 40+ more providers (Arcee, Chutes, Claude Max Proxy, ComfyUI, GitHub Copilot, LiteLLM, vLLM, Volcengine, and more). Model selection, failover config, env vars reference | 1,689 |
| 06 | [`06-tools.md`](references/06-tools.md) | Tool architecture, exec, code_execution, browser automation, message (agent→channel), image_generate, video_generate, music_generate, TTS, web_fetch, sessions_spawn (sub-agents/ACP), web_search, tool config, gateway tool, memory_search/memory_get, session_status, plugin-provided tools | 1,468 |
| 07 | [`07-plugins.md`](references/07-plugins.md) | Plugin system (install/develop/lifecycle), bundled plugins, voice-call plugin, music-2.6 plugin, channel plugins, SDK conventions, registerCliBackend, registerAgentToolResultMiddleware, createOptionalChannelSetupSurface | 1,215 |
| 08 | [`08-automation.md`](references/08-automation.md) | Cron jobs (full CRUD + logs + doctor), background tasks (ledger), task flow, hooks (HTTP webhooks), standing orders, program examples (weekly status, content/social, financial, system monitoring), heartbeat system, isolated sessions, failureDestination, model switch auth, Gmail PubSub | 962 |
| 09 | [`09-installation.md`](references/09-installation.md) | Getting started guide, updating, Docker (SSH/OpenShell sandbox, HEALTHCHECK, shared-network, VM runtime), Nix/NixOS, Raspberry Pi, uninstall, onboarding wizard, VPS/Linux server deployment, migration guide, platform notes, Control UI custom build | 1,032 |
| 10 | [`10-security-and-misc.md`](references/10-security-and-misc.md) | Security model, exec approvals, sandbox modes, autoApproveCidrs, trusted-proxy, audit checks, FAQ, troubleshooting (gateway probe, doctor, channels --probe), debugging (watcher, PI_RAW_STREAM), env vars, scripts reference, nodes (remote exec, token rotation, SecretRef), diagnostics (export/recorder/privacy), CI pipeline, RPC adapters | 1,239 |
| 11 | [`11-platforms.md`](references/11-platforms.md) | macOS (app, discovery, --json), iOS (APNS relay, autoApproveCidrs), Android (foreground service, auto-reconnect, wide-area discover), Windows (companion, dev loop), Linux (exe.dev, enable-linger), VPS hosting, Web UI — Control UI (identity, auth, approval upgrade, cron panel, WebRTC, embedSandbox, chat.inject) + WebChat (maxChars, abort, tools panel) | 975 |
| 12 | [`12-reference.md`](references/12-reference.md) | Complete config schema (gateway/agents/session/channels/cron/hooks/browser/UI/diagnostics/env), agent config reference, heartbeat reference (all options), workspace file map (BOOT.md hooks, bootstrap limits, sandbox seed), session management, authentication, gateway WS protocol (handshake/framing/roles/scopes/RPC methods), onboarding wizard reference, file locations, env vars | 1,561 |

---

## 🚀 Installation

### Via ClawHub (recommended)
```bash
clawhub install maxwellmelo/openclaw-expert-skill
```

### Manual
```bash
# Clone into your skills directory
cd ~/clawd/skills/  # or wherever your skills live
git clone https://github.com/maxwellmelo/openclaw-expert-skill.git

# Or copy the .skill package
clawhub install ./openclaw-expert-skill.skill
```

### Verify
```bash
# The skill should appear in your agent's available skills
openclaw skills list
```

---

## 🔍 How It Works

### For the Agent

When a user asks an OpenClaw-related question, the agent:

1. **Reads the SKILL.md** — contains a routing guide mapping question patterns → reference files
2. **Loads only the relevant file** — e.g., `04-channels.md` for "how do I set up Telegram?"
3. **Uses the TOC** at the top of each file to jump to the exact section
4. **Follows cross-references** when topics span multiple files

The agent never loads all 20K lines at once. Typical lookup reads 200-500 lines.

### Routing Examples

| User Question | File Loaded | Section Found |
|---------------|------------|---------------|
| "How do I set up WhatsApp?" | `04-channels.md` | `## WhatsApp` |
| "What's the cron syntax?" | `08-automation.md` | `## Cron Jobs` |
| "My gateway won't start" | `10-security-and-misc.md` | `## Troubleshooting` |
| "How do I add Ollama?" | `05-providers.md` | `## Ollama` |
| "What goes in openclaw.json?" | `12-reference.md` | `## Full Config Schema` |
| "How does memory work?" | `01-core-concepts.md` | `## Memory Overview` |
| "Docker sandbox setup" | `09-installation.md` | `## Docker` |
| "How do I use the browser tool?" | `06-tools.md` | `## Browser` |

---

## 📋 Topics Covered

### Architecture & Core
- Gateway architecture (single daemon, WS protocol, typed RPC)
- Agent runtime and loop lifecycle
- System prompt construction and caching
- Context engine (workspace files, bootstrap, skills, dynamic injection)
- Pi SDK integration (`createAgentSession`, embedded runner)
- TypeBox schema system for gateway protocol
- GPT-5.4/Codex agentic parity program

### Channels (25+)
BlueBubbles · Discord · Feishu/Lark · Google Chat · iMessage · IRC · LINE · Matrix · Mattermost · MS Teams · Nextcloud Talk · Nostr · QQ Bot · Signal · Slack · Synology Chat · Telegram · Tlon/Urbit · Twitch · WeChat · WhatsApp · Zalo (bot + personal)

### Providers (52+)
Anthropic · OpenAI · Gemini · OpenRouter · MiniMax · DeepSeek · Groq · Ollama · Together AI · Mistral · Fireworks · xAI · Perplexity · Amazon Bedrock · Cloudflare AI Gateway · Z.AI/GLM · Arcee · Bedrock Mantle · Cerebras · Chutes · Claude Max Proxy · ComfyUI · GitHub Copilot · Gradium · Hyperbolic · Inferrs · Kilocode · LiteLLM · Moonshot/Kimi · OpenCode Go · Qianfan · SambaNova · SGLang · StepFun · Synthetic · Tencent · Vercel AI GW · vLLM · Volcengine · Vydra · Xiaomi · and more

### CLI (50+ commands)
Every subcommand documented with full syntax, flags, examples, and edge cases.

### Tools
exec · code_execution · browser · message · image_generate · video_generate · music_generate · tts · web_fetch · web_search · sessions_spawn · memory_search · memory_get · session_status · gateway tool · plugin tools

### Automation
Cron jobs · Background tasks · Task flow · Hooks (webhooks) · Standing orders · Heartbeat system · Isolated sessions · Gmail PubSub

### Security
Exec approvals · Sandbox modes (off/non-main/all) · autoApproveCidrs · Trusted-proxy · Audit checks · Nodes (remote exec, token rotation) · SecretRef · Diagnostics privacy

### Memory Systems
Builtin engine · Honcho · QMD engine · Memory search · Active memory · Compaction · Dreaming

### Platforms
macOS · iOS · Android · Windows · Linux · VPS/headless · Docker · Nix · Raspberry Pi · Control UI · WebChat

### Workflows
OpenProse (.prose files, /prose CLI, multi-agent orchestration)

---

## 🏗️ How This Was Built

1. **Crawled** all 426+ pages from [docs.openclaw.ai](https://docs.openclaw.ai) via the `llms.txt` index
2. **Organized** content into 12 thematic reference files
3. **Cross-referenced** every section against the live documentation
4. **Audited** each file with specialized agents (4 parallel auditors)
5. **Verified** corrections against live pages (not guessed — fetched and confirmed)
6. **Validated** the final package against ClawHub's AgentSkill spec

Three audit passes were performed:
- **Audit 1:** Bulk correction of ~244 issues across all 12 files
- **Audit 2:** Per-file deep review against live docs (12 sequential reviews)
- **Audit 3:** Coverage gap analysis — added 20 missing providers, 3 missing architecture sections

---

## 📐 Skill Spec Compliance

| Constraint | Status |
|-----------|--------|
| SKILL.md body ≤ 500 lines | ✅ 149 lines |
| Description ≤ 1024 chars | ✅ 819 chars |
| No angle brackets in description | ✅ |
| Files >100 lines have TOC | ✅ All 12 files |
| No scripts/, assets/, symlinks | ✅ Clean structure |
| Validates via `quick_validate.py` | ✅ "Skill is valid!" |

---

## 📂 Repository Structure

```
openclaw-expert-skill/
├── SKILL.md                          # Skill manifest (routing guide + quick reference)
├── README.md                         # This file
└── references/
    ├── 01-core-concepts.md           # Architecture, memory, sessions, agents
    ├── 02-gateway.md                 # Gateway operations, sandboxing, health
    ├── 03-cli.md                     # All 50+ CLI commands
    ├── 04-channels.md                # 25+ messaging channels
    ├── 05-providers.md               # 52+ LLM providers
    ├── 06-tools.md                   # Agent tools (exec, browser, media, etc.)
    ├── 07-plugins.md                 # Plugin system and bundled plugins
    ├── 08-automation.md              # Cron, hooks, tasks, heartbeat
    ├── 09-installation.md            # Install on any platform
    ├── 10-security-and-misc.md       # Security, debugging, FAQ
    ├── 11-platforms.md               # Platform-specific guides + Web UI
    └── 12-reference.md               # Full config schema + protocol spec
```

---

## 🤝 Contributing

Found a gap or inaccuracy? Contributions welcome:

1. Fork the repo
2. Check the relevant section against [docs.openclaw.ai](https://docs.openclaw.ai)
3. Make your correction with a clear commit message
4. Open a PR describing what changed and why

**Guidelines:**
- Every claim should be verifiable against official docs
- Keep the existing structure (12 files, numbered, with TOCs)
- Files >100 lines must maintain their Table of Contents
- Run `quick_validate.py` before submitting

---

## 📄 License

MIT — use freely, attribute if you share.

---

## 🔗 Links

- **OpenClaw:** [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
- **OpenClaw Docs:** [docs.openclaw.ai](https://docs.openclaw.ai)
- **ClawHub (skill marketplace):** [clawhub.ai](https://clawhub.ai)
- **Community:** [Discord](https://discord.com/invite/clawd)

---

*Built with ⚡ by [MX3 Dev](https://github.com/maxwellmelo) — autonomous AI operations at scale.*

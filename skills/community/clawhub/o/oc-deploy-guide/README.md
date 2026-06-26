# openclaw-deploy

<p align="center">
  <strong>Interactive deployment guide for OpenClaw local capabilities</strong><br>
  Memory stack · Video processing · WeChat integration · Maintenance cron jobs
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">中文</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/clawhub-openclaw--deploy-brightgreen?style=for-the-badge" alt="ClawHub">
  <img src="https://img.shields.io/badge/OpenClaw-skill-orange?style=for-the-badge" alt="OpenClaw">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge" alt="License">
</p>

An [OpenClaw](https://github.com/openclaw/openclaw) skill that walks you through deploying a full local capability stack — step by step, with confirmation gates between each phase.

Tell your agent to run this skill and it will check prerequisites, install each component, verify success, and pause for your confirmation before moving on. You can deploy everything at once or pick individual components.

---

## What it deploys

| Phase | Component | What it does |
|-------|-----------|-------------|
| **A** | [Memory Stack](https://github.com/OttoPrua/openclaw-memory-manager) | qmd (semantic search) + LosslessClaw (context compression) |
| **B** | [Memory Manager Skill](https://clawhub.ai/OttoPrua/agent-memory-protocol) | Agent memory write/read protocol |
| **C** | [vid2md](https://github.com/OttoPrua/vid2md) | Video tutorial → structured Markdown |
| **D** | [WeChat Plugin](https://github.com/OttoPrua/openclaw-wechat-bot) | WeChat group chat integration (macOS) |
| **E** | Cron Jobs | Automated memory maintenance |

Each phase is independent — deploy all or just the ones you need.

---

## Usage

### Install the skill

```bash
clawhub install openclaw-deploy
```

Or clone:
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/OttoPrua/openclaw-deploy.git
```

### Run it

Just tell your OpenClaw agent:

```
Run the openclaw-deploy skill
```

or

```
Deploy all OpenClaw capabilities
```

The agent will:
1. Ask which components to deploy
2. Check prerequisites and report any missing tools
3. Walk through each selected phase with install + verify steps
4. Pause for your confirmation between phases
5. Show a final status table

---

## Phases in detail

### Phase A — Memory Stack

- Installs **qmd** (`@tobilu/qmd`) — local semantic + BM25 search over Markdown files
- Creates `memory-root` and `blackboard` collections pointing to your workspace
- Configures `openclaw.json` with the `qmd` memory backend
- Installs **LosslessClaw** (`@martian-engineering/lossless-claw`) — DAG-based context compression
- Restarts the gateway

→ Full docs: [openclaw-memory-manager](https://github.com/OttoPrua/openclaw-memory-manager)

### Phase B — Memory Manager Skill

- Installs the `agent-memory-protocol` skill from ClawHub
- Initializes the `memory/` directory structure if it doesn't exist

→ Full docs: [agent-memory-protocol on ClawHub](https://clawhub.ai/OttoPrua/agent-memory-protocol)

### Phase C — vid2md

- Clones the vid2md repository
- Installs Python dependencies (including platform-appropriate ASR models)
- Optionally downloads FunASR (Chinese), mlx-whisper (English/Apple Silicon)
- Optionally pulls a vision model for AI frame descriptions
- Runs a smoke test

→ Full docs: [vid2md](https://github.com/OttoPrua/vid2md)

### Phase D — WeChat Plugin

- Clones the WeChat plugin repository
- Configures `openclaw.json` with channel settings
- Guides you through WeChat notification and accessibility setup

> macOS only.

→ Full docs: [openclaw-wechat-bot](https://github.com/OttoPrua/openclaw-wechat-bot)

### Phase E — Cron Jobs

- Adds selected maintenance cron jobs:
  - **Dream Cycle** — weekly memory consolidation
  - **Daily Progress Sync** — project state sync to Blackboard
  - **Monthly Cleanup** — archive old session logs

→ Full docs: [cron reference configs](https://github.com/OttoPrua/openclaw-memory-manager/tree/main/cron)

---

## Prerequisites

The skill checks these automatically, but here's what you'll need:

| Tool | Required for | Install |
|------|-------------|---------|
| git | all | system package manager |
| python3 3.9+ | vid2md | system or pyenv |
| brew | macOS installs | https://brew.sh |
| ffmpeg | vid2md | `brew install ffmpeg` |
| ollama | vid2md (AI descriptions) | https://ollama.com |
| bun or node | qmd install | https://bun.sh |
| openclaw | all | `npm install -g openclaw` |

---

## Related

- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [ClawHub](https://clawhub.ai) — community skills
- [Discord](https://discord.gg/clawd)

## License

MIT

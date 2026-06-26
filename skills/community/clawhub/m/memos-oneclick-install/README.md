# MemOS for OpenClaw — One-Click Install

> Chinese version: [README_zh.md](./README_zh.md).

[![npm version](https://img.shields.io/npm/v/@memtensor/memos-local-openclaw-plugin)](https://www.npmjs.com/package/@memtensor/memos-local-openclaw-plugin)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/MemTensor/MemOS/blob/main/LICENSE)
[![Node.js >= 18](https://img.shields.io/badge/node-%3E%3D18-brightgreen)](https://nodejs.org/)
[![GitHub](https://img.shields.io/badge/GitHub-Source-181717?logo=github)](https://github.com/MemTensor/MemOS/tree/main/apps/memos-local-openclaw)

> [Homepage](https://memos-claw.openmem.net) · [Documentation](https://memos-claw.openmem.net/docs/) · [NPM](https://www.npmjs.com/package/@memtensor/memos-local-openclaw-plugin) · [Troubleshooting](https://memos-claw.openmem.net/docs/troubleshooting.html)

---

## What this folder contains

| File | Purpose |
| ---- | ------- |
| **`SKILL.md`** | The agent skill that drives one-click installation. Once loaded, OpenClaw reads this file and **autonomously** installs, configures, and verifies the MemOS plugin — you just answer one question. |
| **`README.md`** | This file — a human-readable overview of the installation experience and MemOS's features. |

---

## True one-click: let OpenClaw do the work

The **`SKILL.md`** in this folder is not a manual — it is a **machine-readable installation skill** designed for the OpenClaw agent. When you say *"install memos"* or *"install MemOS"*, here is what happens:

### Zero manual steps

Once triggered, OpenClaw executes a **6-step autonomous pipeline** — detecting your current state, installing the plugin, writing configuration, restarting the gateway, verifying the result, and delivering a final summary. **You do not need to run any command yourself.**

The only interaction during the entire process is a single question:

> *Choose your embedding model — local offline (A) or external API (B)?*

Reply `A` or `B`, and OpenClaw handles the rest. If you are upgrading an existing installation, even this question is skipped — the process is fully hands-free.

### Automatic OS detection — macOS, Linux, and Windows

You never need to tell the agent what system you are running. The skill uses **`process.platform`** (`darwin` / `linux` / `win32`) to detect your OS and adapts every command accordingly:

| Aspect | How it adapts |
| ------ | ------------- |
| **Path separators & home directory** | All paths are built with `require('path').join(...)` and `require('os').homedir()` — works identically on every OS. |
| **Shell commands** | The primary approach is `node -e "..."`, which runs the same way in bash, PowerShell, and cmd. Platform-specific fallbacks (e.g. `nohup` on macOS/Linux, `Start-Process` on Windows) are used only when inherently necessary. |
| **Install script fallback** | If the OpenClaw CLI is unavailable, the agent picks `install.sh` (macOS/Linux) or `install.ps1` (Windows) automatically — no user decision needed. |
| **Native module rebuild** | `better-sqlite3` is rebuilt to match your local Node.js version; build-tool guidance is platform-aware (`xcode-select` / `apt install build-essential` / Visual Studio Build Tools). |

**Bottom line:** whether you are on a Mac, a Linux server, or a Windows workstation, say *"install memos"* and walk away.

### Smart state detection

The skill does not blindly reinstall. Before touching anything it checks:

- **Not installed** — full install pipeline (Steps 0 – 6).
- **Installed but outdated** — automatic upgrade, preserving your existing config.
- **Already up to date** — quick verification only; no restart unless something is broken.
- **Config incomplete or broken** — auto-repair without re-downloading the plugin.

Every branch is chosen by the agent. You are never asked *"What would you like to do?"*.

---

## What MemOS gives you

Once installed, the MemOS plugin transforms OpenClaw into a **memory-powered agent** — 100% on-device, no cloud account required for the default local-embedding path.

### Core capabilities

| Capability | Description |
| ---------- | ----------- |
| **Persistent memory** | Every conversation turn is automatically captured, semantically chunked, embedded, and indexed into a local SQLite database (`~/.openclaw/memos-local/memos.db`). No manual "remember this" needed. |
| **Hybrid retrieval** | FTS5 keyword search + vector semantic search, fused with Reciprocal Rank Fusion (RRF) and Maximal Marginal Relevance (MMR) reranking. Configurable recency decay biases recent memories. |
| **Task summarization** | Conversations are auto-segmented into tasks. Completed tasks receive structured LLM summaries — goal, key steps, result, and preserved details (code, commands, URLs, errors). |
| **Skill evolution** | High-quality task executions are distilled into reusable skills (SKILL.md bundles) that can **auto-upgrade** when similar tasks appear later. Version history, quality scoring, and auto-install are built in. |
| **Team sharing** | Optional Hub–Client architecture: one Hub stores shared data, clients keep private data local. Scoped search (`local` / `group` / `all`), task sharing, skill publish/pull, admin approval flow, and real-time notifications. |
| **Memory Viewer** | A localhost web dashboard (default `http://127.0.0.1:18799`) with 7 pages: Memories, Tasks, Skills, Analytics, Logs, Import, Settings — full CRUD, i18n (Chinese/English), light/dark themes. |
| **Memory migration** | One-click import of OpenClaw's native built-in memories (SQLite + JSONL) into MemOS, with smart deduplication and resume support. |
| **Multi-provider embedding** | OpenAI-compatible, Gemini, Cohere, Voyage, Mistral, or fully offline local model (`Xenova/all-MiniLM-L6-v2`). |

### Automatic hooks — no manual "remember this"

| Hook | Trigger | What happens |
| ---- | ------- | ------------ |
| **`agent_end`** | After each turn | Messages are chunked, embedded, deduplicated (content-hash + LLM judge), and written. |
| **`before_agent_start`** | Before each turn | Relevant memories are injected into context. If recall is weak, the agent calls `memory_search` with a self-generated query. |

### Tools at your disposal

| Tool | Role |
| ---- | ---- |
| `memory_search` | Keyword + semantic search over memories (scoped). |
| `memory_get` / `memory_timeline` | Full chunk text / surrounding conversation context. |
| `memory_write_public` | Write memory visible to all local agents. |
| `task_summary` | Structured summary of a completed task. |
| `skill_get` / `skill_search` / `skill_install` | Discover and install evolved skills. |
| `memory_viewer` | Get the Memory Viewer URL. |

Plus Hub–Client networking tools (`task_share`, `skill_publish`, `network_skill_pull`, etc.). Full reference lives in the bundled **`memos-memory-guide`** skill, auto-installed during setup.

---

## Why MemOS — advantages over alternatives

| Problem | How MemOS solves it |
| ------- | ------------------- |
| **Agent forgets between sessions** | Durable, indexed memory — automatic capture after every turn. |
| **Shallow context, repeated mistakes** | Task summaries + skill evolution turn raw chat logs into structured, reusable knowledge. |
| **Multi-agent teams work in isolation** | Hub–Client sharing with scoped retrieval, task sharing, and skill publishing — while private data stays local. |
| **No visibility into what the agent remembers** | Memory Viewer: CRUD, analytics, tool-call logs, migration, and online configuration in one dashboard. |
| **Privacy and data residency concerns** | 100% local-first — SQLite on your machine. External APIs are optional and only used for embedding/summarization **you** configure. |
| **Platform compatibility** | Runs on macOS, Linux, and Windows. The install skill auto-detects your OS and adapts. |
| **Complex manual setup** | One phrase — *"install memos"* — triggers a fully autonomous pipeline. One embedding-choice question, zero shell commands from you. |

MemOS is part of the broader [MemOS Memory Operating System](../MemOS/README.md) project: a unified store/retrieve/manage platform for LLMs and AI agents, with multimodal memory, knowledge-base management, and enterprise-grade optimizations. This OpenClaw plugin is the **local, on-device** deployment path.

---

## Privacy and security

- **100% on-device** — all data in local SQLite, zero cloud uploads.
- **Anonymous telemetry** — opt-out via config; only sends tool names, latencies, and version info. Never sends memory content, queries, or personal data.
- **Viewer security** — binds to `127.0.0.1` only, password-protected with session cookies.

---

## Quick reference — manual install commands

In most cases you should just say *"install memos"* and let the skill handle it. If you prefer running the commands yourself:

**macOS / Linux:**

```bash
curl -fsSL https://cdn.memtensor.com.cn/memos-local-openclaw/install.sh | bash
```

**Windows (PowerShell):**

```powershell
powershell -c "irm https://cdn.memtensor.com.cn/memos-local-openclaw/install.ps1 | iex"
```

**Via OpenClaw CLI:**

```bash
openclaw plugins install @memtensor/memos-local-openclaw-plugin
```

Then configure `~/.openclaw/openclaw.json`, start the gateway, and open the Memory Viewer. See [full documentation](https://memos-claw.openmem.net/docs/) for embedding/summarizer tables, team sharing setup, and troubleshooting.

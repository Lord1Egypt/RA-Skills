---
name: openclaw-tally
description: Develop, test, or integrate the OpenClaw Tally Node.js library for task-level cost, complexity, and efficiency analytics. Use when working on Tally's detector, SQLite ledger, analytics engine, or an explicit plugin/hook integration; installing this skill alone does not register hooks or slash commands.
metadata:
  openclaw:
    version: "0.3.2"
    emoji: "📊"
    homepage: https://github.com/JonathanJing/openclaw-tally
    requires:
      bins: [node, npm]
---

# OpenClaw Tally

Reframes AI usage from token-counting to task-completion economics. Instead of "how many tokens?", answer "how much to get X done, and was it worth it?"

## 🛠️ Installation

### 1. Ask OpenClaw (Recommended)
Tell OpenClaw: *"Install the openclaw-tally skill."* The agent will handle the installation and configuration automatically.

### 2. Manual Installation (CLI)
If you prefer the terminal, run:
```bash
openclaw skills install @jonathanjing/openclaw-tally
```

## Security & Privacy Declaration

- **No automatic hook registration**: OpenClaw Skills are instruction bundles. This package must be integrated through an explicit plugin or operator-owned hook before it can process events.
- **Hook scope after integration**: A `message-post` integration would observe every message, so disclose that scope before enabling it.
- **Local only**: All processing is purely local. No data is sent to any external server.
- **Message content**: The task detector reads message text to identify task boundaries (start/complete/fail signals) using regex pattern matching. **No message text is stored** — only metadata (token count, model, session_id, complexity score) is persisted to the database.
- **Sandboxed storage**: SQLite database defaults to `~/.openclaw/tally/tally.db`. A custom path can be provided for testing.
- **Runtime**: Requires Node.js 22 or newer and `better-sqlite3` 13.x (native Node.js addon). Installation may download a signed prebuild or run a local native build.
- **Permissions**: No network access. No exec permissions. Filesystem limited to `~/.openclaw/tally/`.

## What It Does

- **Detects tasks** from message streams supplied by an explicit integration (Layer 1: Task Detector)
- **Attributes costs** across sessions, sub-agents, and cron triggers (Layer 2: Task Ledger)
- **Computes TES** (Task Efficiency Score) per task, model, and cron (Layer 3: Analytics Engine)

## Setup and verification

```bash
cd "{baseDir}"
npm install
npm test
```

The package currently exports library modules from `src/index.js`. Add slash commands and event hooks only through an OpenClaw plugin or another explicit runtime integration.

## Complexity Levels

- **L1 (Reflex)**: Single-turn, text-only, no tools
- **L2 (Routine)**: Multi-turn or 1–3 tool calls
- **L3 (Mission)**: Multiple tools + file I/O + external APIs
- **L4 (Campaign)**: Sub-agents + cron + cross-session

## TES (Task Efficiency Score)

```
TES = quality_score / (normalized_cost × complexity_weight)
```

- **> 2.0** 🟢 Excellent
- **1.0–2.0** 🟡 Good
- **0.5–1.0** 🟠 Below average
- **< 0.5** 🔴 Poor
- **0.0** ⚫ Failed

## Usage

When explicitly integrated, store analytics locally in `~/.openclaw/tally/tally.db` or a test-specific path.

See `{baseDir}/PRD.md` for the product specification.

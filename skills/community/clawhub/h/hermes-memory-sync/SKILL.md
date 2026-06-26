---
name: hermes-memory-sync
description: Extract daily conversation summaries from Hermes Agent session logs and persist them as readable memory files. Covers the Python extraction script, cron setup, and output format.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, macos, linux]
---

# Hermes Memory Sync

Automated daily memory extraction from Hermes Agent session logs. Reads session JSON/JSONL files, groups conversations by day, extracts key topics/decisions/tools used, and writes structured summaries to `workspace/memory/YYYY-MM-DD.md`.

## When to Use

- Setting up memory persistence for Hermes Agent (beyond built-in memory/session_search)
- Recovering or backfilling memory from earlier sessions
- Creating a human-readable daily log of what was discussed
- Auditing session history by topic or tool usage

## Installation

### 1. Place the script

Copy `hermes-memory-sync.py` to your workspace:

```bash
# Windows
copy hermes-memory-sync.py C:\path\to\workspace\

# Linux/macOS
cp hermes-memory-sync.py ~/workspace/
```

### 2. Verify

```bash
cd /path/to/workspace
python hermes-memory-sync.py stats
```

Expected output: shows active days, total messages, sessions, and existing memory files.

## Usage

```bash
# Show coverage gaps between sessions and existing memory files
python hermes-memory-sync.py compare

# Backfill today's memory
python hermes-memory-sync.py backfill today

# Backfill a specific date
python hermes-memory-sync.py backfill 2026-05-03

# Backfill all missing dates (first-time setup)
python hermes-memory-sync.py backfill all

# Show stats
python hermes-memory-sync.py stats
```

## Cron Setup (Hermes Native)

Use Hermes' built-in cron to run daily at 3 AM:

```
cronjob action=create name="memory-sync-daily"
  prompt="Run Hermes memory sync: cd /path/to/workspace && python hermes-memory-sync.py backfill today"
  schedule="0 3 * * *"
```

The cron job creates files at `workspace/memory/YYYY-MM-DD.md` each morning.

## Output Format

Each memory file contains:

```
# 📅 YYYY-MM-DD

**会话数:** N | **消息总数:** N
**用户提问:** N | **助手回复:** N | **工具调用:** N
**使用的模型:** model1, model2

## 🎯 讨论主题
- Topic 1
- Topic 2

## 💬 关键对话
**Q:** User question...
> **A:** Assistant response...

## ⚡ 决策/方案
- Decision item...

## 🛠️ 工具使用
- Tool call summary...

---
*自动生成于 YYYY-MM-DD HH:MM，来自 N 个会话*
```

## Supported Session Files

The script reads two types of Hermes session data:

### 1. `session_*.json` (full session records)
- Located at `%LOCALAPPDATA%/hermes/sessions/` (Windows)
- Complete conversation history with `messages` array
- Includes `session_id`, `model`, `platform`, `session_start`

### 2. `YYYYMMDD_HHMMSS_*.jsonl` (per-message logs)
- Same sessions directory
- One JSON object per line with `{role, content, timestamp}`
- Uses Hermes format (NOT OpenClaw format)

## Pitfalls

- **Memory usage** — periodically review and consolidate memory entries. Over-full memory causes truncation and lost context.
- **JSONL vs JSON confusion** — The sessions directory contains both `.jsonl` and `.json` files. The script handles both, but `request_dump_*.json` files (individual request/response dumps) are intentionally skipped to avoid duplication.
- **Don't confuse with ClawHub `memory-sync`** — That skill is designed for OpenClaw's JSONL format (`{type, message}` schema). This Hermes-native implementation directly parses Hermes format (`{role, content}` schema). See `clawhub-skills-install` skill for format differences.

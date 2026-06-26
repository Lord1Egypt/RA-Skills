---
name: morning-coffee-briefing
description: Daily morning briefing skill. Reads your TASKS.md and memory files, synthesizes a prioritized day plan, and sends it to you via Telegram so you start the day knowing exactly what to do first. Eliminates decision fatigue.
argument-hint: [optional-focus-area]
allowed-tools: Read, Bash, Glob, Grep, WebSearch
metadata:
  version: "1.0.0"
  author: "clawsonnet"
  tags: ["productivity", "daily-routine", "telegram", "task-management", "briefing"]
  requires:
    env:
      - TELEGRAM_BOT_TOKEN
      - TELEGRAM_CHAT_ID
      - TASKS_FILE_PATH
---

# Morning Coffee — Daily Briefing Skill

Sends you a punchy morning briefing via Telegram so you wake up knowing exactly what move to make first.

## Setup

Set these environment variables (or hardcode paths in the skill):
- `TELEGRAM_BOT_TOKEN` — your Telegram bot token from @BotFather
- `TELEGRAM_CHAT_ID` — your Telegram chat ID
- `TASKS_FILE_PATH` — path to your TASKS.md (e.g., `~/.clawd-cc/memory/TASKS.md`)

## What It Does

1. Reads your TASKS.md for pending items
2. Reads any memory files (MEMORY.md, projects.md, recent notes)
3. Checks for any urgent blockers or time-sensitive items
4. Synthesizes the top 3 priorities for today
5. Sends a punchy Telegram message you can act on immediately

## Process

### Step 1: Load Context

Read all context files in parallel:
- `$TASKS_FILE_PATH` — pending tasks
- `{MEMORY_DIR}/MEMORY.md` — long-term context
- `{MEMORY_DIR}/projects.md` — active projects (if exists)

### Step 2: Analyze Priorities

Identify:
- **Top 3 tasks** for today — what moves the needle most
- **One quick win** — something completable in <30 min to build momentum
- **One blocker** — anything that needs Kevin's direct input (flag these)
- **Pipeline status** — check any automated pipelines (revenue, posts, etc.)

### Step 3: Compose the Briefing

Format (punchy, max 400 chars):
```
Good morning! Here's your plan:

1. [Highest priority task — 1 line]
2. [Second priority — 1 line]
3. [Third priority — 1 line]

Quick win: [easiest task to knock out]
Watch out: [any blocker or time-sensitive item]

[Pipeline status in 1 line if relevant]
```

### Step 4: Send via Telegram

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": \"${TELEGRAM_CHAT_ID}\", \"text\": \"[MESSAGE]\"}"
```

## Scheduling

Add to your cron (runs at 7 AM daily):
```
0 7 * * * claude -p "/morning-coffee-briefing"
```

Or use your agent's built-in cron scheduler.

## Customization

Modify Step 2 to match your setup:
- Change the memory file paths to match your project structure
- Add pipeline status checks specific to your automation (YouTube, Upwork, etc.)
- Adjust the Telegram format to your preference

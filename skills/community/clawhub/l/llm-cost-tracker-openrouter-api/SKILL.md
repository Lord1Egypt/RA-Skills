---
name: llm-cost-tracker
version: 1.1.2
description: >
  Track OpenClaw LLM token usage and cost from OpenRouter API. Reports: last 24h, 7d, 30d, 90d, 365d with model breakdown. Skills that trigger this: - "llm cost", "token usage", "openrouter cost", "llm spend", "daily cost report" → runs run_tracker.py - "collect usage data" → runs collect_usage.py (populates DB silently) When "collect usage data" is received (e.g. from a cron job), run: python3 scripts/collect_usage.py and return "Done" — do NOT send any message to Telegram or any chat.
read_when: >
  - Running a cost/token usage report - Scheduling a daily/weekly cost report - Setting up on a new machine
---
# llm-cost-tracker

Track and report LLM token usage and cost for OpenClaw via OpenRouter.

## Quick Start

```bash
python3 scripts/collect_usage.py --init      # first-time: create DB + backfill
python3 scripts/run_tracker.py               # telegram report (default)
python3 scripts/run_tracker.py --output terminal  # full terminal report
python3 scripts/run_tracker.py --output debug     # per-request debug
```

## Core Design

- **Source of truth:** `usage.cost.total` from OpenRouter — never recomputed from token counts
- **Data source:** OpenClaw session JSONL files (including `.reset` files from context compaction)
- **Deduplication:** by `openrouter_request_id` — safe to re-run backfill anytime
- **Time windows:** 24h rolling (UTC); 7d/30d/90d/365d calendar days (configurable timezone)

## Schema: `request_facts`

| Column | Source |
|--------|--------|
| openrouter_request_id | responseId (unique key) |
| created_at_utc | entry timestamp |
| model | model ID |
| prompt_tokens | usage.input |
| completion_tokens | usage.output |
| cached_tokens | usage.cacheRead |
| cache_write_tokens | usage.cacheWrite |
| reasoning_tokens | usage.reasoning |
| total_tokens | usage.totalTokens |
| billed_cost | usage.cost.total (canonical) |

## Configuration

`config/env.json` (all fields optional):

```json
{
  "SESSIONS_DIR": "",
  "TIMEZONE": "Asia/Hong_Kong",
  "UTC_OFFSET_HOURS": 8
}
```

- `SESSIONS_DIR`: override session file location (empty = auto-detect)
- `TIMEZONE` / `UTC_OFFSET_HOURS`: for calendar-day window calculations
- API key: auto-detected from `~/.openclaw/agents/main/agent/auth-profiles.json` or `OPENROUTER_API_KEY` env var

## Scheduled Reports

```bash
openclaw cron add --name "llm-cost:collect" --message "collect usage data" \
  --cron "5 0 * * *" --tz "Asia/Hong_Kong" --session isolated --no-deliver

openclaw cron add --name "llm-cost:daily" --message "llm cost" \
  --cron "0 9 * * *" --tz "Asia/Hong_Kong" --session isolated
```

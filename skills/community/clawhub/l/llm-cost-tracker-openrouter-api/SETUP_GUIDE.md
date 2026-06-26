# llm-cost-tracker — Setup Guide

## First-Time Setup

```bash
cd <path-to-llm-cost-tracker>
python3 scripts/collect_usage.py --init
```

This creates the DB, backfills all session files (including reset files), and runs a health check.

## Scripts

| Script | Purpose |
|--------|---------|
| `collect_usage.py` | Scan session JSONL files → populate DB |
| `run_tracker.py` | Generate reports, health check, debug |
| `prune_usage.py` | Delete old rows with dry-run support |

### collect_usage.py

```bash
python3 scripts/collect_usage.py --init          # first-run wizard
python3 scripts/collect_usage.py --backfill      # re-scan all sessions
python3 scripts/collect_usage.py                  # collect today only
python3 scripts/collect_usage.py --date 2026-04-24
python3 scripts/collect_usage.py --verify         # DB health check
```

### run_tracker.py

```bash
python3 scripts/run_tracker.py                    # telegram (default)
python3 scripts/run_tracker.py --output terminal  # full terminal report
python3 scripts/run_tracker.py --output json      # JSON for scripting
python3 scripts/run_tracker.py --output debug     # per-request debug
python3 scripts/run_tracker.py --health           # quick health check
```

### prune_usage.py

```bash
python3 scripts/prune_usage.py 2024-04-25 --dry-run   # preview
python3 scripts/prune_usage.py 2024-04-25 --vacuum     # delete + reclaim
```

## Configuration

Edit `config/env.json` (all fields optional):

```json
{
  "SESSIONS_DIR": "",
  "TIMEZONE": "Asia/Hong_Kong",
  "UTC_OFFSET_HOURS": 8
}
```

- **SESSIONS_DIR**: Override if auto-detection fails. Leave empty for auto-detect.
- **TIMEZONE / UTC_OFFSET_HOURS**: For calendar-day windows (default: HKT +8).
- **API key**: Auto-detected from `~/.openclaw/agents/main/agent/auth-profiles.json` or `OPENROUTER_API_KEY` env var. Not stored in env.json.

### Auto-detected paths

Sessions directory search order:
1. `SESSIONS_DIR` from env.json
2. `~/.openclaw/agents/main/sessions`
3. `/data/.openclaw/agents/main/sessions`
4. `~/Library/Application Support/openclaw/agents/main/sessions`

## Cron Setup

```bash
# Midnight: collect data (silent)
openclaw cron add \
  --name "llm-cost:collect" \
  --message "collect usage data" \
  --cron "5 0 * * *" \
  --tz "Asia/Hong_Kong" \
  --session isolated \
  --no-deliver

# 9 AM: daily report to Telegram
openclaw cron add \
  --name "llm-cost:daily" \
  --message "llm cost" \
  --cron "0 9 * * *" \
  --tz "Asia/Hong_Kong" \
  --session isolated
```

Verify: `openclaw cron list`

## Troubleshooting

**Sessions directory not found** — Set `SESSIONS_DIR` in `config/env.json`.

**DB is empty** — Run `python3 scripts/collect_usage.py --init`.

**Cost seems wrong** — Run `--output debug` to inspect per-request costs. Compare with `--health` which shows API key total vs DB total.

**Migrating to a new machine** — Copy the whole folder, then run `--init` again. Cron jobs must be re-created.

## File Structure

```
llm-cost-tracker/
├── SKILL.md
├── SETUP_GUIDE.md
├── requirements.txt
├── config/
│   ├── env.json       (optional config)
│   └── usage.db       (created on first --init)
└── scripts/
    ├── collect_usage.py
    ├── run_tracker.py
    └── prune_usage.py
```

# Setup — llm-cost-tracker

## Requirements
- Python 3.7+
- `tabulate>=0.9.0`

## Install
```bash
pip install tabulate>=0.9.0
```

## First-time setup
```bash
cd skills/llm-cost-tracker
python3 scripts/collect_usage.py --init
```

## Configuration (optional)
Create `config/env.json` to override defaults:
```json
{
  "SESSIONS_DIR": "",
  "TIMEZONE": "Asia/Hong_Kong",
  "UTC_OFFSET_HOURS": 8
}
```

## Cron jobs
```bash
# Midnight: collect usage data (silent)
openclaw cron add --name "llm-cost:collect" --message "collect usage data" \
  --cron "5 0 * * *" --tz "Asia/Hong_Kong" --session isolated --no-deliver

# 9 AM: daily report to Telegram
openclaw cron add --name "llm-cost:daily" --message "llm cost" \
  --cron "0 9 * * *" --tz "Asia/Hong_Kong" --session isolated
```
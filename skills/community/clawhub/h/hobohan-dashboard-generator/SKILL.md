---
name: dashboard-generator
version: 1.0.0
description: "Generate self-contained HTML dashboards for memory logs, expense charts, and token usage. Run hourly via cron."
allowed-tools: [cron, exec, read, write]
---

# Dashboard Generator

Three dashboards served on port 8081 via `scripts/serve-dashboards.py`. Regenerated hourly with a 5-minute stagger.

## Dashboard types

| Dashboard | File | Content |
|-----------|------|---------|
| Memory | `memory/dashboard.html` | All daily logs embedded as cards, searchable |
| Expense | `dashboard/usage/expense-data.json` | All ledger entries as JSON (fed to chart) |
| Usage | `dashboard/usage/dashboard.json` | Token counts, costs, calls per source |

## Regeneration (hourly, `:00 + 5min stagger`)

Run in order:

```bash
/usr/bin/python3 /home/hobopi/.openclaw/workspace/scripts/gen-memory-dashboard.py
/usr/bin/python3 /home/hobopi/.openclaw/workspace/scripts/gen-expense-data.py
/usr/bin/python3 /home/hobopi/.openclaw/workspace/scripts/track-usage.py --dashboard
```

- Timeout: 180s for all three
- Cron: isolated agentTurn, delivery mode `none` (no Telegram notification)

## Dashboard server (8081)

- Script: `scripts/serve-dashboards.py`
- Serves files from `/home/hobopi/.openclaw/workspace/dashboard/` and `/home/hobopi/.openclaw/workspace/memory/`
- Watchdog cron (`every 300ms`): checks HTTP 200 on port 8081 every 5 minutes
- If down: kills old process, restarts script, rechecks
- Watchdog uses default model (not time-sensitive, no user delivery)

## Token usage tracker

- Script: `scripts/track-usage.py`
- Sources: OpenClaw trajectory files (~May 11+), Hermes state.db (~May 14+), Muthu
- Pricing: MiniMax models (M2.7, M2.5, M3) — rates in script
- `--update`: pull all sources, write daily/monthly JSON
- `--dashboard`: regenerate combined dashboard JSON
- `--today`/`--week`/`--month`/`--all`: summary views

### Dashboard JSON structure

```json
{
  "generated": "2026-06-03T12:00:00",
  "combined": [
    {"date": "2026-06-03", "source": "openclaw", "input": 123456, "output": 23456, "cost": 1.23},
    {"date": "2026-06-03", "source": "hermes", "input": 654321, "output": 12345, "cost": 3.45}
  ],
  "monthly": {"2026-06": {"totalCost": 45.67, ...}}
}
```

## Memory dashboard HTML

- Self-contained single HTML file (no external dependencies)
- All daily log content embedded in JS object
- Navigation by date, search, keyword filtering
- Dark theme matching Yoda Patch aesthetic

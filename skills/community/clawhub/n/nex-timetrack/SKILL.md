---
name: Nex Timetrack
description: Billable time logger for freelancers and agencies. Start/stop timers or log manually. Client and project management, rate cascading, 15-minute rounding, billing summaries, full-text search, CSV/JSON export. Python stdlib only, SQLite storage.
version: 1.0.0
metadata:
  author: Nex AI (Kevin Blancaflor)
  license: MIT-0
  website: https://nex-ai.be
  clawdbot:
    keywords:
      - time tracking
      - billable hours
      - timesheet
      - timer
      - stopwatch
      - freelancer
      - agency
      - invoicing
      - billing
      - hourly rate
      - project time
      - client hours
      - urenregistratie
      - tijdregistratie
      - facturatie
      - freelancer uren
    triggers:
      - track time
      - log hours
      - start timer
      - billable hours
      - time entry
      - how long did I work
      - client billing
      - project hours
      - timesheet
      - invoice summary
      - uren bijhouden
      - tijd loggen
      - factureerbare uren
---

# Nex Timetrack

Billable time logger built for freelancers and agencies. Track time with a live timer or log entries manually. Manage clients, projects, and rates. Generate billing summaries with optional 15-minute rounding.

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)
- SQLite (built into Python)

## Setup

```bash
bash setup.sh
```

## Commands

| Command | What it does |
|---------|-------------|
| `start` | Start a live timer |
| `stop` | Stop timer and save entry |
| `status` | Show running timer |
| `cancel` | Cancel timer without saving |
| `log` | Log time manually |
| `show` | Show entry details |
| `list` | List entries with filters |
| `edit` | Edit an entry |
| `delete` | Delete an entry |
| `search` | Full-text search entries |
| `client-add` | Add a client with rate |
| `clients` | List all clients |
| `project-add` | Add a project |
| `projects` | List all projects |
| `summary` | Billing summary with totals |
| `stats` | Usage statistics |
| `export` | Export to JSON or CSV |

## Rate Cascade

Rates resolve in this order: entry rate > project rate > client rate > default (85 EUR/h). Set rates at whatever level makes sense for your billing.

## Duration Format

When logging manually, use any of these:
- `2h` = 2 hours
- `90m` = 90 minutes
- `1h30m` = 1 hour 30 minutes
- `1.5` = 1.5 hours

## Tone Guide

This skill responds to natural language through ClawdBot. Example interactions:

**Starting a timer:**
> "Start tracking time for the Bakkerij Peeters redesign"
```bash
nex-timetrack start "Bakkerij Peeters redesign" --client "Bakkerij Peeters" --category development
```

**Logging time manually:**
> "Log 2 hours of design work for Lux Interiors yesterday"
```bash
nex-timetrack log "Homepage design" 2h --client "Lux Interiors" --category design --date 2026-04-05
```

**Stopping the timer:**
> "Stop the timer, I finished the API integration"
```bash
nex-timetrack stop --notes "Completed API integration for payment flow"
```

**Checking what's running:**
> "Is my timer running?"
```bash
nex-timetrack status
```

**Billing summary for a client:**
> "How many hours did I bill Bakkerij Peeters this month?"
```bash
nex-timetrack summary --client "Bakkerij Peeters" --date-from 2026-04-01 --round-up
```

**Weekly overview:**
> "Show me this week's time entries"
```bash
nex-timetrack list --date-from 2026-03-31 --date-to 2026-04-06
```

**Adding a client:**
> "Add Bakkerij Peeters as a client at 95 per hour"
```bash
nex-timetrack client-add "Bakkerij Peeters" --rate 95 --email "jan@bakkerijpeeters.be"
```

**Export for invoicing:**
> "Export all billable hours for Lux Interiors as CSV"
```bash
nex-timetrack export csv --client "Lux Interiors" --billable
```

## Storage

All data stored locally in `~/.nex-timetrack/timetrack.db` (SQLite). No cloud, no telemetry.

Override with: `export NEX_TIMETRACK_DIR=/custom/path`

## License

MIT-0 on ClawHub (free for any use).
AGPL-3.0 on GitHub (commercial licenses via info@nex-ai.be).

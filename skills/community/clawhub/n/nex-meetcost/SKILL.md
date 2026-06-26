---
name: Nex MeetCost
description: Meeting cost calculator. See what meetings actually cost in billable time. Per-attendee rates by role, recurring meeting projections (weekly/monthly/yearly), cost-per-type breakdowns. Python stdlib only, SQLite storage.
version: 1.0.0
metadata:
  author: Nex AI (Kevin Blancaflor)
  license: MIT-0
  website: https://nex-ai.be
  clawdbot:
    keywords:
      - meeting cost
      - meeting calculator
      - time wasted
      - meeting ROI
      - hourly rate
      - meeting expense
      - recurring meeting
      - standup cost
      - meeting budget
      - vergaderkosten
      - meeting tijd
      - vergadering kost
    triggers:
      - what does this meeting cost
      - calculate meeting cost
      - how expensive is this meeting
      - meeting cost calculator
      - recurring meeting projection
      - wat kost deze vergadering
      - vergaderkosten berekenen
---

# Nex MeetCost

Meeting cost calculator. See what your meetings actually cost based on who attends and their hourly rates. Track recurring meetings and project monthly/yearly costs.

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
| `calc` | Calculate cost (optional save) |
| `log` | Log a meeting with cost |
| `show` | Show meeting details |
| `list` | List logged meetings |
| `rates` | Show default hourly rates |
| `stats` | Cost statistics and breakdowns |
| `export` | Export to JSON or CSV |

## Attendee Format

`name:role:rate` separated by commas. Role and rate are optional.

- `Kevin:developer` uses the default developer rate
- `Kevin:developer:95` uses a custom rate
- `Kevin` uses the default "other" rate

## Tone Guide

**Quick calculation:**
> "What does a 1-hour meeting with 3 developers and a manager cost?"
```bash
nex-meetcost calc 60 -a "Kevin:developer,Sarah:developer,Thomas:developer,Lisa:manager"
```

**Log a meeting:**
> "Log today's 30-minute standup"
```bash
nex-meetcost log "Daily standup" 30 -a "Kevin:developer,Sarah:designer,Thomas:developer" --type standup --recurring 5
```

**See what recurring meetings cost per year:**
> "How much do our recurring meetings cost?"
```bash
nex-meetcost stats
```

## Storage

All data stored locally in `~/.nex-meetcost/meetcost.db` (SQLite). No cloud, no telemetry.

## License

MIT-0 on ClawHub (free for any use).
AGPL-3.0 on GitHub (commercial licenses via info@nex-ai.be).

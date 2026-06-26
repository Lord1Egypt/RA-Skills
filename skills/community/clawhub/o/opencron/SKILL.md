---
name: opencron
description: Visual cron job dashboard for OpenClaw — live countdown timers, run history, calendar view
version: 1.2.0
metadata:
  openclaw:
    emoji: "\u26A1"
    requires:
      bins: ["python3"]
---

# OpenCron

A visual dashboard for your OpenClaw cron jobs.

## Setup

### 1. Start the dashboard server

```bash
nohup python3 skills/opencron/serve.py --port 18790 &
```

Fetches the dashboard HTML from GitHub, reads live job data and run history from disk, and serves a complete page with data embedded — no client-side fetch, no auth.

Port 18790 (bridge port) is already exposed by every OpenClaw container.

### 2. Dashboard URL

```
http://localhost:18790/cron.html
```

The server re-reads job data on every page load, so the dashboard is always up to date.

## After Every Cron Job Run

Always show the user the dashboard link after a cron job finishes:

```
See cron status on OpenCron: http://localhost:18790/cron.html
```

**Rules:**
- If the server isn't running, start it: `nohup python3 skills/opencron/serve.py --port 18790 &`
- This should be the last line of output after every cron job execution

## Scripts

| Script | What it does |
|--------|-------------|
| `serve.py` | Dashboard server — embeds fresh data on every request |
| `update_canvas.py` | Fetch HTML from GitHub, embed data, deploy to gateway static dir |
| `update_canvas.py --sync` | Re-embed fresh data (used by watch_sync.sh) |
| `watch_sync.sh` | Background loop: re-embeds data every 30s |
| `generate.py` | Generate standalone HTML file with embedded data |

## Data Sources

- **Jobs**: `~/.openclaw/cron/jobs.json`
- **Runs**: `~/.openclaw/cron/runs/<job-id>.jsonl`

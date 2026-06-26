---
name: pm-dashboard
description: Real-time dashboard for visualizing AI agent project states including implementation progress, decision trees, and test results. Use when setting up project visualization, checking project status, or managing the dashboard lifecycle. Commands: install, start, stop, status, config, export, import.
metadata:
  clawdbot:
    emoji: "📊"
---

# PM Dashboard

Real-time visualization for AI agent project states.

## Installation

**Via npm:**
```bash
npm install -g @reghoul/pm-dashboard
pm-dashboard init
pm-dashboard start
```

**Via ClawHub:**
```bash
clawhub install pm-dashboard
pm-dashboard init
pm-dashboard start
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `pm-dashboard start` | Start the server |
| `pm-dashboard stop` | Stop the server |
| `pm-dashboard status` | Show status and config |
| `pm-dashboard config get <key>` | Get config value |
| `pm-dashboard config set <key> <value>` | Set config value |
| `pm-dashboard export -o <file>` | Export state |
| `pm-dashboard import <file>` | Import state |

## State Location

All user state is preserved in `~/.openclaw/pm-dashboard/`:
- `config.json` - User configuration
- `state.db` - SQLite database
- `logs/` - Server logs

## Updates

**Via npm:**
```bash
npm update -g @reghoul/pm-dashboard
```

**Via ClawHub:**
```bash
clawhub update pm-dashboard
```

Updates preserve all user state in `~/.openclaw/pm-dashboard/`.

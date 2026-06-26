# openclaw-daily-ops

**Daily cost reporting + zombie session killer for [OpenClaw](https://github.com/openclaw/openclaw) deployments.**

Two problems, one nightly cron:

1. **Know what you spent** — parses your OpenClaw session files, computes per-session API costs, posts a clean report to Discord with 7-day trend
2. **Kill what's dead** — wipes sessions older than 24h with >1MB context before they snowball into thousands of dollars

Zero AI credits spent running this. Pure Python + one Discord webhook.

---

## What the Report Looks Like

```
📊 Daily Cost Report — Mar 9, 2026

💰 Total: $4.21 · 8.3M tokens

By Session:
🔴 #general — $2.45 · 4.1M tok
🟡 #posting — $1.32 · 2.8M tok
🟢 heartbeat — $0.44 · 1.4M tok

7-day trend: $12 → $8 → $6 → $5 → $4 → $4 → $4

✅ UNDER BUDGET
🔄 Reset 2 stale sessions · 3.2MB freed
```

---

## Quick Start

```bash
git clone https://github.com/oh-ashen-one/openclaw-daily-ops
cd openclaw-daily-ops

# 1. Configure
cp config.example.json config.json
# Edit config.json with your webhook, user ID, and session paths

# 2. Test
python3 scripts/cost_report.py --config config.json --dry-run

# 3. Set up nightly cron (see SKILL.md for full options)
```

---

## Requirements

- Python 3.8+
- OpenClaw installed and running
- A Discord webhook URL (free, takes 30 seconds to create)

---

## Files

```
openclaw-daily-ops/
├── SKILL.md                 ← Full setup guide + OpenClaw cron integration
├── README.md                ← This file
├── config.example.json      ← Configuration template
└── scripts/
    ├── cost_report.py       ← Cost parser + Discord poster
    └── zombie_killer.py     ← Stale session wiper
```

---

## Configuration

See `config.example.json` for all options. The important ones:

| Key | Description |
|-----|-------------|
| `discord_webhook` | Where the daily report gets posted |
| `discord_user_id` | Who gets pinged when cost > threshold |
| `zombie_min_age_hours` | Session age threshold (default: 24h) |
| `zombie_min_size_mb` | Minimum file size to bother resetting (default: 1MB) |
| `alert_high_cost` | 🚨 URGENT flag threshold in USD (default: $50) |

---

## Why This Exists

Running multiple AI agents 24/7 across multiple machines is efficient — until you check your Anthropic bill and realize a zombie session has been burning $100/day in cached context for a week. 

This was built after a real incident. The zombie killer is the scar tissue.

---

## Part of the OpenClaw Skills ecosystem

Built to work alongside [openclaw-watchdog](https://github.com/oh-ashen-one/openclaw-watchdog) — the self-healing system monitor. Install both for full operational coverage.

---

MIT License

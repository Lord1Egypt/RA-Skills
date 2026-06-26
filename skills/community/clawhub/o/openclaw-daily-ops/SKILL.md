---
name: openclaw-daily-ops
description: Daily cost reporting + session hygiene for OpenClaw deployments. Tracks per-session API spend, shows 7-day trend, and wipes zombie sessions >24h old to prevent context snowball. Zero personal info — configure with your own paths and Discord channel. Runs nightly via cron.
---

# OpenClaw Daily Ops

Two tasks in one nightly cron: **know what you spent, kill what's dead.**

- Parses all OpenClaw session JSONL files → computes today's API cost per session
- Posts a clean cost report to Discord with 7-day trend
- Wipes sessions older than 24h with >1MB context (zombie killer)
- Logs everything to `state/cost-log.json` and `state/session-reset-log.json`

Zero AI credits spent — pure Python + one Discord message.

---

## Setup

### 1. Configure

Copy `config.example.json` to `config.json` and fill in your values:

```bash
cp config.example.json config.json
```

Edit `config.json`:

```json
{
  "sessions_dir": "~/.openclaw/agents/main/sessions",
  "workspace_dir": "~/.openclaw/workspace",
  "discord_webhook": "https://discord.com/api/webhooks/YOUR/WEBHOOK",
  "discord_user_id": "YOUR_DISCORD_USER_ID",
  "channel_names": {
    "channel:YOUR_CHANNEL_ID": "#your-channel-name"
  },
  "zombie_min_age_hours": 24,
  "zombie_min_size_mb": 1,
  "alert_high_cost": 50,
  "alert_low_cost": 10,
  "timezone_offset_hours": -6
}
```

**How to get a Discord webhook:**
1. Go to your Discord channel → Edit Channel → Integrations → Webhooks → New Webhook
2. Copy the webhook URL

**How to get your Discord user ID:**
1. Enable Developer Mode in Discord (Settings → Advanced → Developer Mode)
2. Right-click your username → Copy User ID

**Channel names** (optional): Map your OpenClaw channel session keys to human-readable names for the report. Find session keys in `~/.openclaw/agents/main/sessions/sessions.json`.

### 2. Test it

```bash
python3 scripts/cost_report.py --config config.json --dry-run
```

This prints the report without posting to Discord or writing logs.

### 3. Set up the cron

Add a nightly OpenClaw cron job. In your OpenClaw config or via CLI:

```
Schedule: 0 21 * * * (9 PM daily — adjust to your timezone)
Model: haiku (cost report is simple, no need for a heavy model)
Payload: Read /path/to/openclaw-daily-ops/SKILL.md and follow it exactly.
```

Or run it as a system cron:

```bash
# Add to crontab -e
0 21 * * * python3 /path/to/openclaw-daily-ops/scripts/cost_report.py --config /path/to/config.json >> /path/to/cost_report.log 2>&1
```

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
🔄 Reset 2 stale sessions (3.2MB freed)
```

Color coding:
- 🔴 session cost > $5
- 🟡 session cost $1–$5  
- 🟢 session cost < $1

---

## Skill Steps (for OpenClaw cron payload)

When running as an OpenClaw cron agentTurn, the agent should:

### Step 1 — Run cost parser
Execute `scripts/cost_report.py --config /path/to/config.json` and capture output.

### Step 2 — Run zombie killer
Execute `scripts/zombie_killer.py --config /path/to/config.json` and capture output.

### Step 3 — Format and post
Combine both outputs into the report format above and post to your Discord webhook.

---

## Configuration Reference

| Key | Type | Description |
|-----|------|-------------|
| `sessions_dir` | string | Path to OpenClaw sessions directory |
| `workspace_dir` | string | Path to OpenClaw workspace (for state logs) |
| `discord_webhook` | string | Discord webhook URL to post the report |
| `discord_user_id` | string | Your Discord ID — tagged on urgent alerts |
| `channel_names` | object | Map session keys → display names (optional) |
| `zombie_min_age_hours` | number | Sessions older than this get reset (default: 24) |
| `zombie_min_size_mb` | number | Minimum file size to reset (default: 1MB) |
| `alert_high_cost` | number | Daily cost threshold for 🚨 URGENT flag (default: $50) |
| `alert_low_cost` | number | Daily cost threshold for ✅ UNDER BUDGET flag (default: $10) |
| `timezone_offset_hours` | number | Your UTC offset for date filtering (default: -6 for CST) |

---

## Files

```
openclaw-daily-ops/
├── SKILL.md                 ← this file
├── config.example.json      ← template config (copy to config.json)
├── scripts/
│   ├── cost_report.py       ← parses sessions, computes costs, posts to Discord
│   └── zombie_killer.py     ← wipes stale sessions, logs what was cleared
└── state/                   ← created automatically
    ├── cost-log.json        ← rolling 90-day cost history
    └── session-reset-log.json ← log of all zombie kills
```

---

## FAQ

**Q: Will this break my active sessions?**
No. The zombie killer only resets sessions older than 24h AND larger than 1MB. Active sessions are never touched.

**Q: What does "reset" mean?**
It truncates the session JSONL file to empty. OpenClaw recreates it fresh on next use. All logs are saved to `session-reset-log.json` before wiping.

**Q: Can I adjust the thresholds?**
Yes — `zombie_min_age_hours` and `zombie_min_size_mb` in `config.json`.

**Q: Does this work on Andre/multi-machine setups?**
Yes. Run the setup on each machine with its own `config.json`. Both can post to the same Discord webhook.

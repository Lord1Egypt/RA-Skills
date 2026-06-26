# Cron Setup for Scribe

Run scribe automatically every night via OpenClaw's built-in cron system.

## Option A: OpenClaw Cron (Recommended)

Use an **isolated session** cron job with `agentTurn` payload. The agent will run scribe as a tool call.

### Add the cron job

Ask your agent:
> "Add a cron job that runs scribe every night at 23:30 Asia/Shanghai"

Or configure manually via the cron tool:

```json
{
  "name": "scribe-nightly",
  "schedule": {
    "kind": "cron",
    "expr": "30 23 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Run the scribe skill now. Scan today's session logs and write memory/YYYY-MM-DD.md. Use: python3 skills/public/scribe/scripts/scribe.py"
  },
  "sessionTarget": "isolated"
}
```

## Option B: System Cron (launchd / crontab)

For running outside OpenClaw:

```bash
# crontab -e
30 23 * * * cd ~/.openclaw/workspace && python3 skills/public/scribe/scripts/scribe.py >> /tmp/scribe.log 2>&1
```

## Environment Variables

Set in your shell profile or cron environment:

```bash
export SCRIBE_SESSION_DIR="$HOME/.openclaw/agents/main/sessions"
export SCRIBE_WORKSPACE="$HOME/.openclaw/workspace"
export SCRIBE_DAYS=1
export SCRIBE_APPEND_LONGTERM=false
export SCRIBE_MODEL=""   # leave empty to use oracle default
```

## Verifying It Works

```bash
python3 skills/public/scribe/scripts/scribe.py
cat memory/$(date +%Y-%m-%d).md
```

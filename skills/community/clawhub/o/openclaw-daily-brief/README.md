# Daily Brief Skill

This package provides a ClawHub-ready skill for a daily OpenClaw operations digest.

## What it does

- Collects last-24h gateway logs
- Reads latest capability-evolver log from `/tmp/evolver-*.log` (if present)
- Uses `secretary` agent to summarize into a structured daily report
- Pushes report to Telegram

## What lands in your Telegram

---
🗞️ Daily Brief — 2026-03-19 08:05

✅ System: openclaw-gateway running normally  
⚠️ Unresolved: ACP runtime plugin not configured  
📋 Today's priorities: [list]  
🧬 Evolution: No new report this week
---

## Who is this for

- Self-hosted OpenClaw users who want a daily ops snapshot
- Anyone running multiple agents who needs a single morning summary
- Users who want capability-evolver results surfaced automatically

## One-line pitch

Your OpenClaw runs 24/7. Now you'll actually know what it did overnight.

## Source references

- `/Users/lihaochen/openclaw/daily_brief.sh`
- `/Users/lihaochen/openclaw/config/workspace-secretary/SOUL.md`
- `/Users/lihaochen/openclaw/workspace/AGENTS.md`

## Publish command

```bash
~/.bun/bin/clawhub publish \
  /Users/lihaochen/openclaw/workspace/clawhub-submission/daily-brief \
  --slug daily-brief \
  --name "Daily Brief" \
  --version 1.0.0 \
  --tags latest \
  --changelog "Initial release: daily OpenClaw system status report via Telegram"
```

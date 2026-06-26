# Cronjob Model Selection Guide

When creating cronjobs in OpenClaw, always specify the cheapest appropriate model.

## General Rule

**90% of cronjobs should use Sonnet in current OpenClaw Sonnet/Opus setups** — they're routine operations that don't need complex reasoning. If your deployment adds a cheaper external provider, use that provider's cheapest reliable model for routine tasks.

## Model Selection by Task Type

### Routine Work: Sonnet, Never Opus

**Monitoring & Alerts:**
```bash
# Check server health
cron add --schedule "*/15 * * * *" \
  --payload '{"kind":"agentTurn","message":"Check server status","model":"anthropic/claude-sonnet-4-5"}' \
  --sessionTarget isolated

# Monitor disk space
cron add --schedule "0 */4 * * *" \
  --payload '{"kind":"agentTurn","message":"Check disk usage on all servers","model":"anthropic/claude-sonnet-4-5"}' \
  --sessionTarget isolated
```

**Data Processing:**
```bash
# Parse daily logs
cron add --schedule "0 2 * * *" \
  --payload '{"kind":"agentTurn","message":"Parse yesterday's error logs and summarize","model":"anthropic/claude-sonnet-4-5"}' \
  --sessionTarget isolated

# Process CSV reports
cron add --schedule "0 8 * * 1" \
  --payload '{"kind":"agentTurn","message":"Extract data from weekly_report.csv","model":"anthropic/claude-sonnet-4-5"}' \
  --sessionTarget isolated
```

**Reminders & Notifications:**
```bash
# Daily standup reminder
cron add --schedule "0 9 * * 1-5" \
  --payload '{"kind":"systemEvent","text":"Reminder: Daily standup in 30 minutes"}' \
  --sessionTarget main

# Weekly backup reminder
cron add --schedule "0 18 * * 5" \
  --payload '{"kind":"agentTurn","message":"Remind user to verify backups","model":"anthropic/claude-sonnet-4-5"}' \
  --sessionTarget isolated
```

**Document Extraction:**
```bash
# Extract invoices
cron add --schedule "0 10 * * *" \
  --payload '{"kind":"agentTurn","message":"Parse new invoices from inbox and extract totals","model":"anthropic/claude-sonnet-4-5"}' \
  --sessionTarget isolated
```

### Sonnet Is Also Fine for Quality-Sensitive Cronjobs

**Content Generation:**
```bash
# Daily blog summary (needs better quality)
cron add --schedule "0 7 * * *" \
  --payload '{"kind":"agentTurn","message":"Write a summary of yesterday's blog posts","model":"anthropic/claude-sonnet-4-5"}' \
  --sessionTarget isolated
```

**Analysis with Context:**
```bash
# Weekly performance analysis (needs reasoning)
cron add --schedule "0 9 * * 1" \
  --payload '{"kind":"agentTurn","message":"Analyze last week's metrics and provide insights","model":"anthropic/claude-sonnet-4-5"}' \
  --sessionTarget isolated
```

### NEVER Opus (Too Expensive for Scheduled Tasks)

Opus should NEVER be used for cronjobs. If a task needs Opus-level reasoning, it's probably too complex for automation — let the user trigger it manually.

## Configuration Pattern

### For agentTurn payload (isolated session):
```json
{
  "kind": "agentTurn",
  "message": "Your task description",
  "model": "anthropic/claude-sonnet-4-5",
  "timeoutSeconds": 300
}
```

### For systemEvent payload (main session):
```json
{
  "kind": "systemEvent",
  "text": "Reminder or alert text"
}
```
(systemEvent inherits the main session's model, which should be Sonnet by default)

## Cost Comparison

**Example: Daily log parsing cronjob**

| Model | Cost per run | Monthly cost (30 days) |
|-------|--------------|------------------------|
| Sonnet | $0.012 | $0.36 |
| Opus | $0.060 | $1.80 |

**10 cronjobs running daily:**
- Sonnet: $3.60/month
- Opus: $18/month

**Choose Sonnet instead of Opus for routine cronjobs.**

## Real-World Examples

### Good (Sonnet)
```bash
# Heartbeat-style health check
cron add --schedule "*/30 * * * *" \
  --payload '{"kind":"agentTurn","message":"Check if all services are running","model":"anthropic/claude-sonnet-4-5"}' \
  --sessionTarget isolated

# Parse structured data
cron add --schedule "0 1 * * *" \
  --payload '{"kind":"agentTurn","message":"Extract customer data from support_tickets.json","model":"anthropic/claude-sonnet-4-5"}' \
  --sessionTarget isolated

# Simple reminder
cron add --schedule "0 14 * * *" \
  --payload '{"kind":"systemEvent","text":"Reminder: Review pending PRs"}' \
  --sessionTarget main
```

### Bad (Wasteful)
```bash
# ❌ Using Opus for simple check
cron add --schedule "*/15 * * * *" \
  --payload '{"kind":"agentTurn","message":"Check email","model":"anthropic/claude-opus-4-5"}' \
  --sessionTarget isolated
# → Should be Sonnet. Opus adds cost without benefit here.
```

## Default Template

When creating a new cronjob, start with this template:

```bash
cron add \
  --schedule "CRON_EXPRESSION" \
  --payload '{
    "kind":"agentTurn",
    "message":"TASK_DESCRIPTION",
    "model":"anthropic/claude-sonnet-4-5",
    "timeoutSeconds":300
  }' \
  --sessionTarget isolated \
  --name "DESCRIPTIVE_NAME"
```

Then ask yourself:
1. Does this task require complex reasoning? If no, keep Sonnet.
2. Does this task generate user-facing content? Sonnet is fine.
3. Does this task need deep analysis? Consider whether it should be manual instead of cron.
4. Everything else: Sonnet, or a cheaper external provider if your deployment supports one.

## Monitoring Cronjob Costs

Track cronjob token usage:
```bash
# List all cronjobs
cron list

# Check runs for a specific job
cron runs --jobId <job-id>

# Use token_tracker.py to monitor spending
python3 scripts/token_tracker.py check
```

If daily costs are high, audit your cronjobs:
1. List all jobs: `cron list`
2. Check which model each uses
3. Switch expensive Opus jobs to Sonnet where possible

## Summary

**Default to Sonnet** for 90% of cronjobs in Sonnet/Opus installs.
**Specify model explicitly** in payload.
**Use isolated sessions** for background tasks.
**Monitor costs** regularly.

**Never use Opus** for routine scheduled tasks.
**Don't forget to specify model** because defaults can be expensive.

**Savings:** Using Sonnet instead of Opus for 10 daily cronjobs avoids unnecessary reasoning-model spend.

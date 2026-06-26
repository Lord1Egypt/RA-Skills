# Cron Recipes

Recommended cron jobs for new OpenClaw agents. Present these to the user and install only what they approve.

## Always Recommend

### Heartbeat
Periodic check-in that scans email, calendar, reminders, and surfaces anything needing attention.

```json
{
  "name": "Heartbeat",
  "schedule": {
    "kind": "every",
    "everyMs": 900000
  },
  "payload": {
    "kind": "systemEvent",
    "text": "Heartbeat prompt: Read HEARTBEAT.md if it exists. Follow it strictly. If nothing needs attention, reply HEARTBEAT_OK."
  },
  "sessionTarget": "current"
}
```

**Configure with the user:**
- Frequency: 15m (default), 30m, or 1h
- Active hours: match their timezone and schedule
- Model: use a cheap model (Haiku or equivalent) to save costs

### Workspace Backup
Daily backup of the workspace directory.

```json
{
  "name": "Daily Workspace Backup",
  "schedule": {
    "kind": "cron",
    "expr": "0 4 * * *",
    "tz": "USER_TIMEZONE"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Run a workspace backup. Commit all changes in the workspace to git with message 'daily backup YYYY-MM-DD'. Report any uncommitted changes or errors.",
    "timeoutSeconds": 300
  },
  "sessionTarget": "isolated"
}
```

## Recommend If Applicable

### Weekly Memory Consolidation
Review and consolidate memory files weekly.

```json
{
  "name": "Weekly Memory Consolidation",
  "schedule": {
    "kind": "cron",
    "expr": "0 3 * * 0",
    "tz": "USER_TIMEZONE"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Run weekly memory consolidation: review daily memory files from the past week, promote durable facts to MEMORY.md, prune stale entries, update ACTIVE.md. Log what was promoted and pruned.",
    "timeoutSeconds": 600
  },
  "sessionTarget": "isolated"
}
```

### Session Health Watchdog
Monitor for stuck sessions, bloated state, stale locks.

```json
{
  "name": "Session Health Watchdog",
  "schedule": {
    "kind": "every",
    "everyMs": 1800000
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Check session health: look for stale lock files, oversized session stores, stuck crons with consecutive errors. Report any issues found.",
    "timeoutSeconds": 120
  },
  "sessionTarget": "isolated"
}
```

### Security Scan
Daily lightweight security check.

```json
{
  "name": "Daily Security Scan",
  "schedule": {
    "kind": "cron",
    "expr": "0 6 * * *",
    "tz": "USER_TIMEZONE"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Run a lightweight security scan: check for exposed secrets in workspace files, verify channel access policies are set to allowlist, check for any suspicious patterns in recent logs. Report findings.",
    "timeoutSeconds": 300
  },
  "sessionTarget": "isolated"
}
```

## Installation Notes

- Always replace `USER_TIMEZONE` with the user's actual IANA timezone
- Always set explicit timeouts on every cron
- **CRITICAL:** Never route crons to `sessionTarget: "main"` (maps to `agent:main:main`) — this causes session deadlocks and blocks all channel responses. Use `"current"` for heartbeats (binds to the session where the cron is created) or `"isolated"` for background agent work.
- After installing, verify each cron has a valid `nextRunAtMs`
- Show the user what was installed and when it will first run

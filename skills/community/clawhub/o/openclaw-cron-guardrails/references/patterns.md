# OpenClaw Cron Safe Patterns

Use these patterns as the default building blocks.

## Pattern A — One-shot reminder in main session

Use for:
- remind me in 20 minutes
- tomorrow morning remind me to X
- next heartbeat do Y

Why:
- avoids isolated delivery routing entirely
- best for lightweight reminders

CLI:

```bash
openclaw cron add \
  --name "Reminder" \
  --at "20m" \
  --session main \
  --system-event "Reminder: check the calendar." \
  --wake now
```

JSON shape:

```json
{
  "name": "Reminder",
  "schedule": { "kind": "at", "at": "2026-03-12T14:00:00Z" },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": { "kind": "systemEvent", "text": "Reminder: check the calendar." }
}
```

## Pattern B — Recurring internal worker (recommended default for background chores)

Use for:
- periodic scans
- maintenance jobs
- research collection
- write files/state internally without user-facing delivery

Why:
- avoids the most common delivery-target failures
- keeps noisy work out of chat

CLI:

```bash
openclaw cron add \
  --name "Internal worker" \
  --cron "*/30 * * * *" \
  --tz "America/New_York" \
  --session isolated \
  --message "Run the periodic internal scan and update local state." \
  --timeout-seconds 300 \
  --no-deliver
```

JSON shape:

```json
{
  "name": "Internal worker",
  "schedule": { "kind": "cron", "expr": "*/30 * * * *", "tz": "America/New_York" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run the periodic internal scan and update local state.",
    "timeoutSeconds": 300
  },
  "delivery": { "mode": "none" }
}
```

## Pattern C — Isolated job with explicit Discord delivery

Use for:
- post a scheduled summary to a Discord channel/thread
- scheduled thread update
- visible bot message on a timer

Why:
- explicit route avoids `channel=last` ambiguity
- best pattern for multi-channel setups

CLI:

```bash
openclaw cron add \
  --name "Discord summary" \
  --cron "0 9 * * *" \
  --tz "America/New_York" \
  --session isolated \
  --message "Summarize overnight progress." \
  --timeout-seconds 300 \
  --announce \
  --channel discord \
  --to "channel:1480624517117247561"
```

Notes:
- Prefer explicit `channel:<id>` or `user:<id>` targets.
- If Discord uses multiple accounts, also set `--account <id>`.

## Pattern D — Isolated job with explicit webhook delivery

Use for:
- send finished event to an HTTP endpoint
- external automation hooks

CLI:

```bash
openclaw cron add \
  --name "Webhook callback" \
  --cron "0 * * * *" \
  --tz "UTC" \
  --session isolated \
  --message "Run the hourly job and publish the result." \
  --timeout-seconds 300
```

Then edit or create via JSON/tool payload with explicit webhook delivery:

```json
{
  "name": "Webhook callback",
  "schedule": { "kind": "cron", "expr": "0 * * * *", "tz": "UTC" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run the hourly job and publish the result.",
    "timeoutSeconds": 300
  },
  "delivery": {
    "mode": "webhook",
    "to": "https://example.com/openclaw/cron"
  }
}
```

## Pattern E — Heavier isolated analysis job

Use for:
- weekly analysis
- deep report generation
- multi-step research or codebase analysis

Why:
- most user-created cron failures are self-inflicted by too-short timeout

CLI:

```bash
openclaw cron add \
  --name "Weekly deep analysis" \
  --cron "0 9 * * 1" \
  --tz "America/New_York" \
  --session isolated \
  --message "Produce the weekly deep analysis report." \
  --model "opus" \
  --timeout-seconds 900 \
  --no-deliver
```

## Pattern F — Editing a broken job safely

Workflow:

1. inspect runs first

```bash
openclaw cron runs --id <jobId> --limit 10
```

2. fix only the broken dimension

Examples:

- switch broken isolated announce job to internal-only:

```bash
openclaw cron edit <jobId> --no-deliver
```

- make delivery explicit:

```bash
openclaw cron edit <jobId> --announce --channel discord --to "channel:1480624517117247561"
```

- increase timeout:

```bash
openclaw cron edit <jobId> --timeout-seconds 300
```

## Recommended defaults

If unsure, start from these defaults:

- reminder → `main + systemEvent`
- background worker → `isolated + no-deliver`
- visible scheduled post → `isolated + explicit channel + explicit to`
- recurring job → always set `tz`
- anything non-trivial → `timeoutSeconds >= 180`

## Verification after creation

Run:

```bash
openclaw cron list
openclaw cron runs --id <jobId> --limit 5
```

If safe to test immediately:

```bash
openclaw cron run <jobId>
```
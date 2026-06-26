# Cron Spec Examples

These examples are intended for the v0.2 helper scripts:

- `scripts/validate_cron_spec.py`
- `scripts/render_cron_command.py`

Use plain JSON.

## Example 1 — Safe one-shot reminder

```json
{
  "name": "Reminder",
  "schedule": { "kind": "at", "at": "2026-03-12T14:00:00Z" },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "Reminder: check the calendar."
  },
  "deleteAfterRun": true
}
```

## Example 2 — Safe internal isolated worker

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
  "delivery": { "mode": "none" },
  "multiChannelConfigured": true
}
```

## Example 3 — Safe explicit Discord delivery

```json
{
  "name": "Discord summary",
  "schedule": { "kind": "cron", "expr": "0 9 * * *", "tz": "America/New_York" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Summarize overnight progress.",
    "timeoutSeconds": 300
  },
  "delivery": {
    "mode": "announce",
    "channel": "discord",
    "to": "channel:1480624517117247561"
  },
  "multiChannelConfigured": true
}
```

## Example 4 — Session injection / push loop for current thread

```json
{
  "name": "Current thread push loop",
  "schedule": { "kind": "cron", "expr": "*/10 * * * *", "tz": "America/New_York" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Review the current project state and push the current session forward with one concrete next step.",
    "timeoutSeconds": 300
  },
  "delivery": { "mode": "none" },
  "multiChannelConfigured": true,
  "notes": {
    "intentType": "session-injection",
    "targetScope": "current-thread"
  }
}
```

## Example 5 — Intentionally bad spec (should fail validation)

```json
{
  "name": "Broken announce job",
  "schedule": { "kind": "cron", "expr": "*/10 * * * *" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Do the thing",
    "timeoutSeconds": 60
  },
  "delivery": {
    "mode": "announce",
    "channel": "last"
  },
  "multiChannelConfigured": true
}
```

Expected failure reason:
- isolated announce job in multi-channel setup requires explicit delivery.channel

## Usage

Validate:

```bash
python3 scripts/validate_cron_spec.py references/example.json
```

Render:

```bash
python3 scripts/render_cron_command.py references/example.json
```
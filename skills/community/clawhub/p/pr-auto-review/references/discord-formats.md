# Discord Notification Formats

## Standard PR Review Notification

```
🔍 **PR Auto-Review Complete**
PR: #123 — Fix auth flow
Author: @dev
CI/CD: ✅ All passing
Health: ✅ All services OK
[Link to full report]
```

## Alert Notification (CI failure or health issue)

```
🚨 **PR Auto-Review — Issues Found**
PR: #123 — Fix auth flow
CI/CD: ❌ 2 checks failing
Health: 🟡 nginx degraded
Action required before merge.
```

## Webhook Payload

```json
{
  "content": "message text (max 2000 chars)",
  "username": "PR Auto-Review Bot",
  "embeds": []
}
```

For richer formatting, use Discord embeds:
```json
{
  "embeds": [{
    "title": "PR #123 — Fix auth flow",
    "color": 5763719,
    "fields": [
      {"name": "CI/CD", "value": "✅ All passing", "inline": true},
      {"name": "Health", "value": "✅ All services OK", "inline": true}
    ],
    "footer": {"text": "pr-auto-review"}
  }]
}
```

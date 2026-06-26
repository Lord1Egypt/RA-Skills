---
name: notification-system
description: Manage outbound notifications across WhatsApp, Telegram, email. Handle templates, scheduling, delivery tracking, rate limiting.
---

# Notification System Agent

Centralized outbound notification management for all channels (WhatsApp, Telegram, email).

## Architecture

```
notification-system/
├── SKILL.md              # This file
├── templates/            # Message templates by channel & type
│   ├── whatsapp/         # WhatsApp templates
│   ├── telegram/         # Telegram templates
│   └── email/            # Email templates
├── queue/                # Pending notification queue
├── logs/                 # Delivery logs
├── rate-limiters.json    # Rate limit configuration
└── config/               # Channel configs
```

## Supported Channels

| Channel | Config | Rate Limits |
|---------|--------|-------------|
| WhatsApp | `channels.whatsapp` | 60 msg/min, 1000/day |
| Telegram | `channels.telegram` | 30 msg/sec, 20 msg/min |
| Email (Outlook) | `office365-connector` | 30 msg/hour, 300/day |

## Rate Limiting

Default limits per channel:
- **WhatsApp**: 1 message/second (safety), burst of 5
- **Telegram**: 30 messages/second hard limit from API
- **Email**: 60 emails/hour to prevent spam flags

Rate limit config: `notification-system/rate-limiters.json`

## Template Variables

All templates support:
```
{{recipient}}     - Target name/ID
{{date}}           - Current date
{{time}}           - Current time
{{subject}}        - Message subject
{{body}}           - Message body
{{cta_url}}        - Call-to-action link
{{sender_name}}    - Business/sender name
{{company}}        - Company name
```

## Sending a Notification

### WhatsApp
```bash
# Via message tool
message send --channel whatsapp --target "+18184389562" --message "Your appointment is confirmed for {{date}}"
```

### Telegram
```bash
# Via message tool
message send --channel telegram --target "655641853" --message "System alert: {{subject}}"
```

### Email
```bash
# Via outlook skill
outlook send --to "recipient@email.com" --subject "{{subject}}" --body "{{body}}"
```

## Queue System

Notifications are queued in `notification-system/queue/pending.json`:

```json
{
  "id": "uuid",
  "channel": "whatsapp|telegram|email",
  "target": "recipient-id",
  "template": "template-name",
  "variables": {},
  "scheduled_at": "ISO8601 or null",
  "created_at": "ISO8601",
  "priority": "high|normal|low",
  "status": "pending|sent|failed|delivered",
  "attempts": 0,
  "last_error": null
}
```

## Scheduling

Scheduled notifications stored in `notification-system/queue/scheduled.json` with cron-like scheduling.

Use cron jobs with `notification-system/process-queue.js` to process scheduled items.

## Delivery Tracking

Logs stored in `notification-system/logs/delivery-YYYY-MM-DD.json`:

```json
{
  "id": "notification-uuid",
  "timestamp": "ISO8601",
  "channel": "whatsapp",
  "target": "+1...",
  "template": "appointment-confirm",
  "status": "delivered|sent|failed",
  "latency_ms": 450,
  "error": null
}
```

## Template Management

Templates stored in `notification-system/templates/{channel}/{type}.md`:

```
templates/
├── whatsapp/
│   ├── appointment-confirm.md
│   ├── appointment-reminder.md
│   ├── payment-received.md
│   ├── status-update.md
│   ├── broadcast-promotion.md
│   └── support-acknowledged.md
├── telegram/
│   ├── system-alert.md
│   ├── status-report.md
│   ├── daily-brief.md
│   └── broadcast.md
└── email/
    ├── invoice.md
    ├── welcome.md
    └── notification.md
```

## Process Queue

To process pending notifications:

```bash
node notification-system/process-queue.js
```

## Status Commands

- List pending: `Get-Content queue/pending.json | ConvertFrom-Json`
- Check rate limits: `Get-Content rate-limiters.json`
- View recent logs: `Get-Content logs/delivery-$(Get-Date -Format 'yyyy-MM-dd').json`

## Best Practices

1. **Batch wisely**: Group similar notifications, respect quiet hours
2. **Fallback channels**: If WhatsApp fails, try Telegram, then email
3. **Deduplicate**: Don't send same notification twice within 24h
4. **Opt-out handling**: Honor STOP/opt-out requests immediately
5. **Personalize**: Use recipient name and relevant variables
6. **Monitor delivery**: Check logs for failures and retry

## Priority Handling

- `high`: System alerts, urgent items → Skip rate limit queue
- `normal`: Standard notifications → Normal rate limiting
- `low`: Marketing, non-urgent → Strictest rate limiting

# Notification System

Centralized outbound notification management for Edgar's AI operating system.

## Quick Start

### Send a notification immediately

```powershell
.\quick-notify.ps1 -Channel whatsapp -Target "+18184389562" -Template status-update -Variables @{recipient_name="Edgar"; status_text="System check complete"} -SendNow
```

### Schedule a notification

```powershell
.\quick-notify.ps1 -Channel telegram -Target "655641853" -Template system-alert -Variables @{subject="Reminder"; message="Check the system"} -ScheduledAt "2026-03-25 09:00"
```

### Process the queue

```powershell
.\process-queue.ps1 -DryRun  # Preview
.\process-queue.ps1          # Execute
```

### View stats

```powershell
.\get-stats.ps1
```

## Directory Structure

```
notification-system/
├── SKILL.md                    # This documentation
├── README.md                   # Quick reference
├── rate-limiters.json          # Rate limit configuration
├── quick-notify.ps1            # Quick notification sender
├── process-queue.ps1           # Queue processor
├── get-stats.ps1               # Statistics viewer
├── templates/
│   ├── whatsapp/              # WhatsApp templates
│   ├── telegram/               # Telegram templates
│   └── email/                  # Email templates
├── queue/
│   └── pending.json            # Pending & scheduled queue
└── logs/
    └── delivery-YYYY-MM-DD.json # Daily delivery logs
```

## Available Templates

### WhatsApp
- `appointment-confirm` - Appointment confirmation
- `appointment-reminder` - Appointment reminder
- `payment-received` - Payment confirmation
- `status-update` - Generic status update
- `broadcast-promotion` - Marketing broadcast
- `support-acknowledged` - Support ticket acknowledgment

### Telegram
- `system-alert` - System alerts (HTML/Markdown)
- `status-report` - Status reports
- `daily-brief` - Daily briefings
- `broadcast` - General broadcasts

### Email
- `invoice` - Invoice with table formatting
- `welcome` - Welcome email with next steps
- `notification` - Generic notification

## Variables

All templates support these variables:
- `{{recipient_name}}` - Recipient's name
- `{{date}}` / `{{time}}` - Current date/time
- `{{subject}}` - Message subject
- `{{message}}` - Message body
- `{{cta_url}}` - Call-to-action link
- `{{sender_name}}` - Sender name
- `{{company}}` - Company name
- Template-specific variables (see individual template files)

## Rate Limits

| Channel | Per Second | Per Minute | Per Hour | Per Day |
|---------|------------|------------|----------|---------|
| WhatsApp | 1 | 30 | 500 | 2000 |
| Telegram | 30 | 20 | 300 | 3000 |
| Email | - | 1 | 30 | 300 |

**Quiet Hours**: 10 PM - 8 AM (notifications queued, not sent)

## Delivery Tracking

Logs are stored in `logs/delivery-YYYY-MM-DD.json` with:
- Notification ID
- Timestamp
- Channel & target
- Template used
- Delivery status
- Latency (ms)
- Error details (if failed)

## Status Commands

```powershell
# Check queue depth and today's stats
Get-Content queue\pending.json | ConvertFrom-Json | Select-Object pending, scheduled

# View recent deliveries
Get-Content logs\delivery-$(Get-Date -Format 'yyyy-MM-dd').json | ConvertFrom-Json | Select-Object -Last 10

# Check rate limit status
Get-Content rate-limiters.json | ConvertFrom-Json | Select-Object -ExpandProperty channels
```

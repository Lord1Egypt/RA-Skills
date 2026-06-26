---
name: jpeng-email-sender
description: "Email sending skill via SMTP or API providers. Supports attachments, HTML templates, and batch sending."
version: "1.0.0"
author: "jpeng"
tags: ["email", "smtp", "notification", "communication"]
---

# Email Sender

Send emails via SMTP or API providers (SendGrid, Mailgun, Resend).

## When to Use

- User wants to send an email
- Automated notifications
- Batch email campaigns
- HTML email with attachments

## Configuration

Set environment variables:

```bash
# SMTP mode
export EMAIL_SMTP_HOST="smtp.gmail.com"
export EMAIL_SMTP_PORT="587"
export EMAIL_SMTP_USER="your@email.com"
export EMAIL_SMTP_PASS="your-app-password"

# Or API mode (SendGrid)
export EMAIL_SENDGRID_API_KEY="SG.xxx"

# Or API mode (Resend)
export EMAIL_RESEND_API_KEY="re_xxx"
```

## Usage

```bash
python3 scripts/send_email.py \
  --to "recipient@example.com" \
  --subject "Hello" \
  --body "This is the message body" \
  --html  # Optional: send as HTML
```

### With attachments

```bash
python3 scripts/send_email.py \
  --to "recipient@example.com" \
  --subject "Report Attached" \
  --body "Please find attached." \
  --attach "/path/to/report.pdf"
```

### Batch sending

```bash
python3 scripts/send_email.py \
  --batch recipients.csv \
  --template template.html \
  --subject "Newsletter"
```

## Output

Returns JSON with send status:

```json
{
  "success": true,
  "message_id": "msg_xxx",
  "to": "recipient@example.com"
}
```

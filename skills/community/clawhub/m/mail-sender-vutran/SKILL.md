---
name: mail-sender
description: Send emails via SMTP. Use when the user needs to send an email with a custom subject and body. This skill requires SMTP configuration (server, port, user, pass) to be set via environment variables or provided in the workflow.
---

# Mail Sender

This skill allows the agent to send emails using a standard SMTP server (like Gmail, Outlook, etc.).

## Setup

The skill uses the following environment variables for configuration:
- `SMTP_SERVER`: (e.g., smtp.gmail.com)
- `SMTP_PORT`: (e.g., 587)
- `SMTP_USER`: Your email address
- `SMTP_PASS`: Your app-specific password
- `FROM_EMAIL`: The sender's email (optional, defaults to SMTP_USER)

## Usage

To send an email, use the bundled script:

```bash
python3 skills/public/mail-sender/scripts/send.py \
  --to-email "recipient@example.com" \
  --subject "Hello from OpenClaw" \
  --body "This is a test email sent via the mail-sender skill."
```

## Security Note

For Gmail, use an **App Password** instead of your primary account password. Never hardcode credentials in the script or conversation history.

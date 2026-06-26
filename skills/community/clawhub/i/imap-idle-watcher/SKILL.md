---
name: imap-idle-watcher
description: >
  Real-time email monitoring using IMAP IDLE — no OAuth, no token expiration.
  Sets up a persistent connection to any IMAP server (Gmail, Outlook, Yahoo, etc.)
  and triggers a user-defined command instantly when new email arrives.
  Runs as a systemd service with auto-reconnect.
  Use when: (1) setting up email-triggered automation, (2) watching an inbox for
  new messages in real-time, (3) replacing OAuth-based email polling that keeps
  breaking due to token expiry, (4) building email-to-webhook or email-to-script
  pipelines. NOT for: sending email, reading/parsing email bodies, or
  non-Linux systems without systemd.
---

# IMAP IDLE Watcher

Real-time email watcher. Uses IMAP IDLE (server push) instead of polling.
App passwords instead of OAuth — no token expiry, no re-auth.

## Quick Start

### Interactive
```bash
bash scripts/setup_service.sh
```
Prompts for email, detects provider, gives app password link, tests connection, installs service.

### Non-interactive
```bash
bash scripts/setup_service.sh \
  --account "user@gmail.com" \
  --password "xxxx xxxx xxxx xxxx" \
  --command "python3 /path/to/handler.py" \
  --service-name my-watcher
```

### Test connection only
```bash
bash scripts/setup_service.sh --test --account "user@gmail.com" --password "xxxx"
```

## Configuration (env vars)

| Variable | Default | Description |
|----------|---------|-------------|
| `IMAP_ACCOUNT` | (required) | Email address |
| `IMAP_PASSWORD` | (required) | App password |
| `IMAP_HOST` | `imap.gmail.com` | IMAP server (auto-detected from email) |
| `IMAP_PORT` | `993` | IMAP port |
| `IMAP_FOLDER` | `INBOX` | Folder to watch |
| `ON_NEW_MAIL_CMD` | (optional) | Shell command to run on new mail |
| `FILTER_FROM` | (optional) | Only trigger for these senders (comma-separated, substring match) |
| `FILTER_SUBJECT` | (optional) | Only trigger for these subjects (comma-separated, substring match) |
| `IDLE_TIMEOUT` | `1200` | Seconds before IDLE renewal (max 1740) |
| `DEBOUNCE_SECONDS` | `10` | Min seconds between command runs |

## Filtering

Only process emails matching specific senders or subjects:

```bash
FILTER_FROM=paypal.com,stripe.com      # from contains either (OR)
FILTER_SUBJECT=payment,invoice         # subject contains either (OR)
```

- Case-insensitive substring match
- Both FROM and SUBJECT must match if both set (AND)
- Within each filter, any value matches (OR)
- No filter set = process all emails

## Writing a Handler

The agent should write a handler script based on the user's intent. The daemon passes email metadata as env vars:

| Variable | Example |
|----------|---------|
| `MAIL_FROM` | `John Doe <john@example.com>` |
| `MAIL_SUBJECT` | `Your order has shipped` |
| `MAIL_DATE` | `Mon, 17 Mar 2026 10:30:00 +0700` |
| `MAIL_UID` | `12345` |

### Workflow

1. User describes what they want (e.g. "watch my inbox, summarize new emails")
2. Agent writes a handler script (Python/Bash) that reads the env vars and does what the user asked
3. Agent saves it somewhere persistent (e.g. `~/email-handler.py`)
4. Agent runs `setup_service.sh` with `--command "python3 ~/email-handler.py"`

### Example: user says "notify me about new emails"

Agent writes `~/email-handler.py`:
```python
#!/usr/bin/env python3
import os
print(f"New mail from {os.environ.get('MAIL_FROM', '?')}: {os.environ.get('MAIL_SUBJECT', '?')}")
```

Then wires it up:
```bash
bash scripts/setup_service.sh --account "user@gmail.com" --password "xxxx" \
  --command "python3 ~/email-handler.py"
```

The handler is the agent's job — adapt it to whatever the user needs.

## How It Works

1. Connects to IMAP server with app password (SSL)
2. Enters IDLE mode — server holds connection open
3. Server pushes notification when new mail arrives (instant, no polling)
4. Daemon runs `ON_NEW_MAIL_CMD` with email metadata as env vars (`MAIL_FROM`, `MAIL_SUBJECT`, `MAIL_DATE`, `MAIL_UID`)
5. Returns to IDLE. Renews every 20 min per RFC 2177.
6. Auto-reconnects on disconnect (backoff: 5s → 10s → 30s → 60s → 120s)

## Service Management

```bash
systemctl status <service-name>
journalctl -u <service-name> -f
systemctl restart <service-name>
systemctl stop <service-name>
```

## Uninstall

```bash
bash scripts/setup_service.sh --uninstall --service-name <service-name>
```

## Provider Setup Guides

- Gmail: see [references/gmail.md](references/gmail.md)
- Outlook: see [references/outlook.md](references/outlook.md)
- Yahoo: see [references/yahoo.md](references/yahoo.md)

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md) for common errors and fixes.

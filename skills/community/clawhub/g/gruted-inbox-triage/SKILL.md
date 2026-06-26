---
name: gruted-inbox-triage
description: AI-powered email triage via IMAP (himalaya) or Google API. Fetches inbox, classifies messages by urgency, recommends actions, and generates daily markdown digests.
metadata:
  openclaw:
    requires:
      bins: [node, himalaya]
---

# inbox-triage-bot

AI email triage — fetch, classify, and report on your inbox.

## Quick start

```bash
cd ~/.openclaw/workspace/skills/inbox-triage-bot
npm install
EMAIL_BACKEND=himalaya npm run demo
```

## What it does

- Fetches recent emails via IMAP (himalaya) or Google API
- Classifies by urgency and category (AI or heuristic)
- Recommends actions per message
- Pulls upcoming calendar events
- Generates markdown daily digest reports

## Backends

### himalaya (recommended — no OAuth)

Requires himalaya CLI configured with a Gmail App Password:

```bash
himalaya envelope list -f INBOX -s 5  # test
EMAIL_BACKEND=himalaya npm run demo
```

### Google API (alternative)

Requires OAuth credentials:

```bash
cp .env.example .env  # edit with OAuth creds
npm run google:oauth:init
npm run demo
```

## Commands

```bash
npm run demo              # full triage report (markdown)
npm run email:fetch       # raw envelopes (JSON)
npm run email:triage      # classified envelopes (JSON)
npm run calendar:upcoming # upcoming events (JSON)
```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `EMAIL_BACKEND` | auto | `himalaya` or `google` |
| `HIMALAYA_ACCOUNT` | `gru_gmail` | himalaya account name |
| `OPENAI_API_KEY` | — | Optional AI classification |

## Cron

```bash
# Daily at 7 AM
0 7 * * * cd /path/to/inbox-triage-bot && EMAIL_BACKEND=himalaya npm run demo >> ~/inbox-triage.md 2>&1
```

## Links

- GitHub: https://github.com/gruted/inbox-triage-bot
- Landing page: https://gruted.github.io/inbox-triage-bot/

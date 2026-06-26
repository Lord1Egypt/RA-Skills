---
name: github-triage
description: "GitHub notification auto-triage via email channel. Classifies incoming GitHub notification emails into three tiers: (1) CI failures and security alerts → immediate forward with [紧急] tag, (2) PR reviews and merges → buffered for daily summary, (3) everything else → silent archive. Use when: an inbound email on the ghbot sub-mailbox is a GitHub notification. Requires: mail-cli, email channel plugin (@clawmail/email). NOT for: non-GitHub emails or manual email composition."
metadata:
  version: 1.0.0
---
# GitHub Triage

Automatically classify and route GitHub notification emails.

## Prerequisites

- `mail-cli` installed (`npm i -g @clawemail/mail-cli`) with API key configured
- Email channel plugin (`@clawmail/email`) enabled in OpenClaw
- A dedicated sub-mailbox for GitHub notifications (created via setup script)

## Setup

Run the setup script to create the sub-mailbox:

```bash
bash scripts/setup.sh [prefix]
```

- `prefix` — sub-mailbox prefix (default: `ghbot`)

Main email (for receiving urgent forwards and daily summaries) is automatically resolved at runtime via:

```bash
mail-cli clawemail master-user
```

After setup:
1. Add the new sub-mailbox as an email channel account in `openclaw.json` → `channels.email.accounts`
2. Go to GitHub → Settings → Notifications → Custom routing → set email to `<workspace>.ghbot@claw.163.com`
3. Restart OpenClaw gateway

## Triage Workflow

When an email arrives on the ghbot account:

1. **Identify priority** — read subject and body, match against rules in `references/triage-rules.md`
2. **Act on priority:**
   - **P0 (urgent):** Resolve main email via `mail-cli clawemail master-user`, then forward immediately via `mail-cli --profile ghbot compose send`; prepend `[紧急]` to subject
   - **P1 (buffer):** Append to today's buffer file at `memory/gh-triage-buffer-YYYY-MM-DD.json`; do NOT reply or forward
   - **P2 (archive):** Mark as read via `mail-cli --profile ghbot mail mark --ids <id> --fid 1 --read`; no reply

### Forwarding (P0)

First, resolve the main email:

```bash
MAIN_EMAIL=$(mail-cli clawemail master-user)
```

Then forward:

```bash
mail-cli --profile ghbot compose send \
  --to "$MAIN_EMAIL" \
  --subject "[紧急] <original-subject>" \
  --body "<original-body>" \
  --html
```

### Buffering (P1)

Append entry to workspace file `memory/gh-triage-buffer-YYYY-MM-DD.json`:

```json
[
  {
    "repo": "owner/repo",
    "type": "review_request",
    "title": "PR title",
    "number": 123,
    "url": "https://github.com/...",
    "author": "username",
    "receivedAt": "ISO-8601"
  }
]
```

Read existing file first (create `[]` if missing), append new entry, write back.

### Archiving (P2)

```bash
mail-cli --profile ghbot mail mark --ids "<message-id>" --fid 1 --read
```

No reply, no forward.

## Daily Summary

A cron job fires daily at the configured time (default `0 18 * * *`). The job:

1. Resolve main email: `MAIN_EMAIL=$(mail-cli clawemail master-user)`
2. Read `memory/gh-triage-buffer-YYYY-MM-DD.json` for today
3. If empty or missing → do nothing
4. Group entries by repo and type
5. Compose summary email following format in `references/triage-rules.md` → "Daily Summary Format"
6. Send via `mail-cli --profile ghbot compose send --to "$MAIN_EMAIL" --subject "[GitHub 日报] ..." --body "..." --html`
7. After successful send, rename buffer file to `memory/gh-triage-buffer-YYYY-MM-DD.sent.json`

### Cron Setup

Create the daily summary cron job in OpenClaw:

```
schedule: { kind: "cron", expr: "0 18 * * *", tz: "Asia/Shanghai" }
sessionTarget: "isolated"
payload: { kind: "agentTurn", message: "Run GitHub triage daily summary. Read today's buffer file, compose and send the summary email." }
```

## Configuration

- **main_email** — automatically resolved at runtime via `mail-cli clawemail master-user`; no manual configuration needed
- **summary_time** — cron expression for daily summary (default: `0 18 * * *`)

## Detailed Rules

See `references/triage-rules.md` for complete matching patterns and output formats.
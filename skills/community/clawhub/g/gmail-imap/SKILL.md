---
name: gmail-imap
description: "Read, search, send, trash, move, and label Gmail via IMAP. Requires GMAIL_IMAP_USER (Gmail address) and GMAIL_IMAP_PASSWORD (Google App Password) environment variables — no API key needed. Use when an agent needs Gmail access: reading inbox, searching messages, sending email, or deleting messages."
metadata:
  openclaw:
    requires:
      env:
        - GMAIL_IMAP_USER
        - GMAIL_IMAP_PASSWORD
    primaryEnv: GMAIL_IMAP_PASSWORD
    homepage: https://clawhub.ai/skills/gmail-imap
---

# Gmail IMAP Skill

All Gmail access uses IMAP. Credentials are read from environment variables — never printed.

## Requirements

Set these environment variables before use:

| Variable | Description |
|----------|-------------|
| `GMAIL_IMAP_USER` | Your Gmail address (e.g. user@gmail.com) |
| `GMAIL_IMAP_PASSWORD` | A Google App Password (not your account password) |

Generate an App Password at: https://myaccount.google.com/apppasswords (requires 2FA enabled)

## Quick Reference

```bash
# Locate the script (adjust SKILL_DIR to match your install location):
# Default: ~/.openclaw/skills/gmail-imap
# Custom:  <workspace>/skills/gmail-imap
SCRIPT="$SKILL_DIR/scripts/gmail_imap.py"

# List inbox (most recent 20)
"$SCRIPT" list

# List with custom limit
"$SCRIPT" list --limit 50

# List unread only (shorthand)
"$SCRIPT" list --unread

# List unread with limit
"$SCRIPT" list --unread --limit 10

# Search by sender (IMAP header search)
"$SCRIPT" list --search 'FROM "boss@example.com"'

# Full-text search (Gmail X-GM-RAW — searches body + headers)
"$SCRIPT" search "invoice"
"$SCRIPT" search "from:boss@example.com is:unread" --limit 5
"$SCRIPT" search "subject:meeting this week"

# Read a message (by UID shown in list output)
"$SCRIPT" read <uid>

# Read from a specific folder
"$SCRIPT" read <uid> --folder "[Gmail]/All Mail"

# Delete (moves to [Gmail]/Trash — correct Gmail deletion)
"$SCRIPT" trash <uid>

# Move to a label/folder
"$SCRIPT" move <uid> "Work"

# Send email
"$SCRIPT" send --to recipient@example.com --subject "Hello" --body "Message text"
```

## Deletion Rule (Critical)

Never use the standard IMAP `\Deleted` flag on Gmail — it only archives, it does not delete.
Always use `trash <uid>` which moves to `[Gmail]/Trash`. The script handles this correctly.

## Credentials

Set in env (never output raw password):
- `GMAIL_IMAP_USER` — Gmail address
- `GMAIL_IMAP_PASSWORD` — App password (generate at myaccount.google.com/apppasswords)

## Reference

For folder names, search syntax, direct Python IMAP usage, and connection details:
→ See [references/gmail-imap-reference.md](references/gmail-imap-reference.md)

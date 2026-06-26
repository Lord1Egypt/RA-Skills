---
name: msgraph
description: Read and manage Microsoft Outlook email (inbox, folders, move messages) and Outlook calendar (list events, create events) via Microsoft Graph API. Use when the user asks to check email, read messages, move emails to folders, see upcoming calendar events, or create calendar events in Outlook/Microsoft 365 personal accounts. Also use for anything involving the user's Outlook inbox or Microsoft calendar.
---

# Microsoft Graph Skill

Integrates with Microsoft Graph API for Outlook mail and calendar on personal Microsoft accounts (consumers tenant). Uses PKCE auth — no client secret needed.

**Skill root:** Skill directory containing `scripts/` and `references/`  
**Token file:** `~/.openclaw/msgraph-tokens.json`  
**First-time setup:** [Setup Guide](references/SETUP.md) — Walk through Azure app registration one time

For API details, scopes, and endpoint reference: see [API Reference](references/api.md).

## Auth

Always check auth status before making API calls.

```bash
python scripts/auth.py status    # Check if authenticated
python scripts/auth.py login     # Full PKCE login (opens browser — interactive, needs user)
python scripts/auth.py refresh   # Force token refresh
python scripts/auth.py token     # Print current access token
```

**First-time setup:** Run `auth.py login`. A browser window opens for Microsoft login. After login, tokens are stored and auto-refreshed on future calls.

**WSL2 note:** The script tries `cmd.exe /c start` to open the browser, then falls back to printing the URL. If the browser opens but the redirect fails, the user may need to paste the full redirect URL — ask them.

**On 401 errors:** Token auto-refreshes. If refresh fails, instruct the user to run `python auth.py login`.

## Mail

```bash
# List inbox (default 20 messages)
python scripts/mail.py inbox
python scripts/mail.py inbox --count 50
python scripts/mail.py inbox --folder sentitems

# Read a message (also marks it read)
python scripts/mail.py read <message_id>

# Move a message to a folder (by name or well-known name)
python scripts/mail.py move <message_id> archive
python scripts/mail.py move <message_id> "Newsletters"

# List all folders (shows IDs and unread counts)
python scripts/mail.py folders

# Search email
python scripts/mail.py search "project update"
```

**Folder names:** Well-known names (`inbox`, `drafts`, `sentitems`, `deleteditems`, `junk`, `archive`) work directly. Display names are resolved automatically by listing folders.

## Calendar

**Note:** The calendar script is named `cal.py` (not `calendar.py`) to avoid a Python stdlib conflict.

```bash
# List upcoming events (default 7 days)
python scripts/cal.py list
python scripts/cal.py list --days 14

# Get event detail
python scripts/cal.py get <event_id>

# Create an event
python scripts/cal.py create \
  --subject "Team Sync" \
  --start "2026-03-10T10:00" \
  --end "2026-03-10T11:00" \
  --tz "America/New_York" \
  --location "Zoom" \
  --body "Weekly sync call" \
  --attendees "alice@example.com,bob@example.com"

# Delete an event
python scripts/cal.py delete <event_id>

# List available calendars
python scripts/cal.py calendars
```

**Defaults:** `--tz` defaults to `America/New_York`. `--start`/`--end` accept `YYYY-MM-DDTHH:MM`.

## Workflow

1. Run `auth.py status` — if not authenticated, prompt user to run `auth.py login`
2. Call the appropriate script
3. Present results in a readable summary (don't dump raw IDs to the user; use subjects/senders)
4. For move operations, confirm which folder the email went to
5. For event creation, confirm back the created event's subject, time, and ID

## User Email Organization (example — update for your setup)

The user's inbox organization system:

- **Inbox** — open loops only (anything still needing action)
- **Events/** — travel plans, reservations (subfolders per trip/event)
- **eReceipts** — purchase receipts and confirmations

When processing email unprompted, apply this logic before moving anything.
When in doubt, leave in inbox and flag for the user.

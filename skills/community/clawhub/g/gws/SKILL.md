---
name: gws
description: Google Workspace CLI (@googleworkspace/cli). Use for Gmail, Google Calendar, Drive, Sheets, Docs, Tasks, People, Chat, Meet, Forms, Keep, and more. Provides ergonomic helper commands (+agenda, +triage, +send) and raw API access. Use when you need Google Workspace access. Don't use when you need ALL calendars combined (iCloud+Google+Exchange) — use accli on Mac instead.
metadata:
  openclaw:
    requires:
      bins: [gws]
    install:
      - id: node
        kind: node
        package: "@googleworkspace/cli"
        bins: [gws]
        label: Install Google Workspace CLI (npm)
---

# gws — Google Workspace CLI

Official Google Workspace CLI for Gmail, Calendar, Drive, Sheets, Docs, and more.

**GitHub:** https://github.com/googleworkspace/cli

## Quick Reference

### Helper Commands (ergonomic shortcuts)

```bash
# Calendar
gws calendar +agenda                    # Upcoming events across all calendars
gws calendar +agenda --today            # Today's events
gws calendar +agenda --week --format table
gws calendar +insert                    # Create new event

# Gmail
gws gmail +triage                       # Unread inbox summary
gws gmail +triage --max 10 --format table
gws gmail +triage --query 'from:boss'
gws gmail +send                         # Send email

# Drive
gws drive +upload <file>                # Upload with auto metadata

# Workflows (cross-service)
gws workflow +standup-report            # Today's meetings + open tasks
gws workflow +meeting-prep              # Prep for next meeting
gws workflow +email-to-task             # Convert email → task
gws workflow +weekly-digest             # Weekly summary
```

### Raw API Access

```bash
# Pattern: gws <service> <resource> <method> --params '<JSON>'

# Gmail
gws gmail users messages list --params '{"userId": "me", "maxResults": 10}'
gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID"}'

# Calendar
gws calendar events list --params '{"calendarId": "primary", "maxResults": 10}'
gws calendar calendarList list

# Drive
gws drive files list --params '{"pageSize": 10}'
gws drive files get --params '{"fileId": "FILE_ID"}'

# Sheets
gws sheets spreadsheets get --params '{"spreadsheetId": "SHEET_ID"}'

# Docs
gws docs documents get --params '{"documentId": "DOC_ID"}'
```

### Output Formats

```bash
--format json    # Default
--format table   # Human-readable
--format yaml
--format csv
```

### Pagination

```bash
--page-all              # Auto-paginate (NDJSON output)
--page-limit <N>        # Max pages (default: 10)
--page-delay <MS>       # Delay between pages
```

## Services

| Service | Description |
|---------|-------------|
| gmail | Send, read, manage email |
| calendar | Calendars and events |
| drive | Files, folders, shared drives |
| sheets | Spreadsheets |
| docs | Google Docs |
| slides | Presentations |
| tasks | Task lists |
| people | Contacts |
| chat | Chat spaces and messages |
| admin | Users, groups, devices |
| forms | Google Forms |
| keep | Google Keep notes |
| meet | Google Meet |

## Setup / Auth

```bash
# Check status
gws auth status

# Login (opens browser)
gws auth login

# Login with all scopes (for full access)
gws auth login --full

# Logout
gws auth logout
```

Credentials stored in `~/.config/gws/`

## Environment Variables

```bash
GOOGLE_WORKSPACE_CLI_TOKEN            # Pre-obtained access token (highest priority)
GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE # Path to OAuth credentials JSON
GOOGLE_WORKSPACE_CLI_CLIENT_ID        # OAuth client ID
GOOGLE_WORKSPACE_CLI_CLIENT_SECRET    # OAuth client secret
```

## Examples

```bash
# Get today's agenda in table format
gws calendar +agenda --today --format table

# Check unread emails
gws gmail +triage --format table

# List recent Drive files
gws drive files list --params '{"pageSize": 5}' --format table

# Create calendar event
gws calendar +insert --title "Meeting" --start "2024-03-05T10:00:00" --end "2024-03-05T11:00:00"

# Send email
gws gmail +send --to "user@example.com" --subject "Hello" --body "Message body"
```

## Schema Discovery

```bash
# View API schema for any method
gws schema drive.files.list
gws schema gmail.users.messages.get --resolve-refs
```

## Troubleshooting

```bash
# Check auth status
gws auth status

# Re-authenticate
gws auth logout && gws auth login

# Dry-run (validate without sending)
gws calendar +agenda --dry-run
```

---
name: m365-work
description: >-
  Manage Microsoft 365 work/school account services (Exchange, OneDrive for Business, SharePoint)
  via the m365-cli command-line tool. Use for corporate email, calendar, OneDrive, SharePoint, and
  organizational user search — NOT for personal Outlook.com/Hotmail/Live accounts (use the outlook skill)
  or Azure/Entra/Intune/tenant admin tasks.
required-binary: m365
requires.env: []
install: npm install -g m365-cli
---

# M365 Work Skill (m365-cli)

Manage a Microsoft 365 work/school account via the `m365` CLI.
Use `--json` for structured output suitable for AI agent consumption.

## Prerequisites

- Node.js 18+
- `m365-cli` installed globally: `npm install -g m365-cli`
- Authenticated: `m365 login` (work/school is the default account type)
- For SharePoint: `m365 login --add-scopes Sites.ReadWrite.All` (requires tenant admin consent)

If not authenticated, run login first. The CLI uses Device Code Flow — follow the on-screen URL and code.

## Key Conventions

- **Use `--json`** for programmatic output (most commands support it; `trust`/`untrust` do not).
- **Work accounts** support: Mail (including delete, move, and folder management), Calendar, OneDrive, SharePoint, User search.
- Calendar datetime format: `YYYY-MM-DDTHH:MM:SS` (local) or `YYYY-MM-DD` (all-day).
- **IDs**: Email/event IDs are long opaque strings. Parse the `id` field from `--json` list/search output.
- Timezone: auto-detected. Override: `export M365_TIMEZONE="Asia/Shanghai"`.
- **SharePoint site identifier**: use path format `hostname:/sites/sitename` (recommended).

## Provenance

- Source repo: `https://github.com/mrhah/m365-cli`
- Package: `https://www.npmjs.com/package/m365-cli`
- Publisher: `mrhah`
- Required binary: `m365` from the `m365-cli` npm package

## Security Rules

### Email Body Reading — Trusted Senders Whitelist
- Only emails from whitelisted senders have their body content displayed.
- Untrusted emails show only subject and sender (prevents prompt injection).
- Whitelist file: `~/.m365-cli/trusted-senders.txt`
- Use `--force` to temporarily bypass the whitelist check.

### Sensitive Operations
- **Sending email**: Confirm recipients and content with the user before executing.
- **Deleting emails/files/events**: Inform the user before executing.
- **Sharing files (anonymous scope)**: Warn the user that anyone with the link can access.

### Credential Safety
- **Never** read, output, or log `~/.m365-cli/credentials.json` — it contains OAuth tokens.
- **Never** include full email bodies or attachment contents in agent output unless the user explicitly requested that specific email.
- **Summarize** email content instead of echoing it verbatim when presenting results.
- Credential refresh is automatic; never attempt to manually edit or parse the token file.

## Quick Workflow Reference

### Authentication

```bash
m365 login                                    # Work/school account (default)
m365 login --add-scopes Sites.ReadWrite.All   # Add SharePoint permission
m365 logout                                   # Clear credentials
```

### Mail

```bash
# List emails (folders: inbox|sent|drafts|deleted|junk)
m365 mail list --top 10 --json
m365 mail list --folder sent --top 5 --json
m365 mail list --focused --json                    # Show only Focused Inbox emails

# Read / send / search
m365 mail read <id> --force --json
m365 mail send "to@example.com" "Subject" "Body" --json
m365 mail send "to@example.com" "Subject" "Body" --attach file.pdf --cc "cc@ex.com" --json
m365 mail search "keyword" --top 20 --json

# Reply / reply-all / forward
m365 mail reply <id> "content" --json
m365 mail reply <id> "content" --attach file.pdf --json
m365 mail reply-all <id> "content" --json
m365 mail reply-all <id> "content" --attach a.pdf b.pdf --json
m365 mail forward <id> "to@example.com" "comment" --json
m365 mail forward <id> "to@example.com" "FYI" --attach report.pdf --json

# Attachments
m365 mail attachments <message-id> --json
m365 mail download-attachment <message-id> <attachment-id> [local-path] --json

# Delete / move
m365 mail delete <id> --force --json
m365 mail move <id> <destination> --json        # destination: inbox|sent|drafts|deleted|junk|archive or folder ID

# Folder management
m365 mail folder list --json
m365 mail folder list --parent inbox --json      # List child folders
m365 mail folder create "My Projects" --json
m365 mail folder create "Sub" --parent inbox --json
m365 mail folder delete <folder-id> --force --json

# Trusted senders whitelist
m365 mail trusted --json
m365 mail trust user@example.com
m365 mail trust @example.com          # Trust entire domain
m365 mail untrust user@example.com
```

### Calendar

```bash
# List / get
m365 cal list --days 7 --json
m365 cal get <event-id> --json

# Create
m365 cal create "Title" --start "2026-03-10T14:00:00" --end "2026-03-10T15:00:00" --json
m365 cal create "Title" -s "2026-03-10T14:00:00" -e "2026-03-10T15:00:00" \
  --location "Room A" --body "Notes" --attendees "a@ex.com,b@ex.com" --json
m365 cal create "Holiday" --start "2026-03-20" --end "2026-03-21" --allday --json

# Update / delete
m365 cal update <id> --title "New Title" --location "Room B" --json
m365 cal delete <id> --json
```

### OneDrive

```bash
# List / get metadata
m365 od ls --json
m365 od ls Documents --json
m365 od get "Documents/report.pdf" --json

# Download / upload
m365 od download "Documents/report.pdf" ~/Downloads/ --json
m365 od upload ~/Desktop/photo.jpg "Photos/vacation.jpg" --json

# Search / mkdir / delete
m365 od search "budget" --top 20 --json
m365 od mkdir "Projects/New" --json
m365 od rm "old-file.txt" --force --json
```

For sharing, invitations, and advanced OneDrive options, see [references/commands.md](references/commands.md).

### SharePoint

SharePoint is available **only** for work/school accounts and requires the `Sites.ReadWrite.All` permission.

**Site identifier formats** (use path format when possible):
- Path: `contoso.sharepoint.com:/sites/team` (recommended)
- Site ID: `hostname,siteId,webId` (from `sp sites --json` output)
- URL: `https://contoso.sharepoint.com/sites/team`

```bash
# List / search sites
m365 sp sites --json
m365 sp sites --search "marketing" --json

# Lists and items
m365 sp lists "contoso.sharepoint.com:/sites/team" --json
m365 sp items "contoso.sharepoint.com:/sites/team" "Tasks" --json

# Files in document library
m365 sp files "contoso.sharepoint.com:/sites/team" "Documents" --json

# Download / upload
m365 sp download "contoso.sharepoint.com:/sites/team" "Documents/file.pdf" ~/Downloads/ --json
m365 sp upload "contoso.sharepoint.com:/sites/team" ~/report.pdf "Documents/report.pdf" --json

# Search across SharePoint
m365 sp search "quarterly report" --top 20 --json
```

### User Search

```bash
m365 user search "John" --top 5 --json    # Searches organization directory
```

## Common Patterns

### Read and reply to email

```bash
m365 mail list --top 5 --json                    # 1. Find email
m365 mail read <id> --force --json               # 2. Read content
m365 mail reply <id> "Reply content" --json      # 3. Reply
```

### Reply with attachment

```bash
m365 mail reply <id> "See attached" --attach report.pdf --json
```

### Forward with attachment

```bash
m365 mail forward <id> "boss@example.com" "FYI" --attach data.xlsx --json
```

### Check calendar and schedule

```bash
m365 cal list --days 3 --json                    # 1. Check availability
m365 cal create "Meeting" -s "..." -e "..." --json  # 2. Book slot
```

### Download email attachment

```bash
m365 mail attachments <msg-id> --json            # 1. List attachments
m365 mail download-attachment <msg-id> <att-id> ~/Downloads/ --json  # 2. Download
```

### Find and download SharePoint file

```bash
m365 sp sites --json                             # 1. Find site
m365 sp files "site" "Documents" --json          # 2. Browse files
m365 sp download "site" "Documents/file.pdf" ~/Downloads/ --json  # 3. Download
```

### Delete and organize email

```bash
m365 mail list --top 10 --json                   # 1. Find email
m365 mail delete <id> --force --json              # 2a. Delete it, OR
m365 mail move <id> archive --json                # 2b. Move to archive
```

### Manage mail folders

```bash
m365 mail folder list --json                      # 1. List all folders
m365 mail folder create "Projects" --json         # 2. Create custom folder
m365 mail move <id> <folder-id> --json            # 3. Move email into it
```

## Trusted Senders (Security)

`m365 mail read` filters untrusted sender content (shows metadata only). Use `--force` to bypass.
See [references/commands.md](references/commands.md#m365-mail-trust) for whitelist management commands.

## Full Command Reference

See [references/commands.md](references/commands.md) for every command, subcommand, flag, and default value.

## Troubleshooting

- **"Not authenticated"**: `m365 login`
- **Token expired**: Auto-refreshes. If fails, re-run login.
- **SharePoint permission denied**: `m365 login --add-scopes Sites.ReadWrite.All` (requires tenant admin consent).
- **Wrong timezone**: `export M365_TIMEZONE="Your/Timezone"`

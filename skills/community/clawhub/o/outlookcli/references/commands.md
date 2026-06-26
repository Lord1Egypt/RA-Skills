# m365-cli Complete Command Reference

Full reference for all `m365` CLI commands available to personal Microsoft accounts.

## Table of Contents

- [Authentication](#authentication)
- [Mail Commands](#mail-commands)
- [Calendar Commands](#calendar-commands)
- [OneDrive Commands](#onedrive-commands)
- [User Commands](#user-commands)
- [Configuration](#configuration)

---

## Authentication

### m365 login

Authenticate with Microsoft 365 using Device Code Flow.

```
m365 login [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--account-type <type>` | `work` or `personal` | `work` |
| `--scopes <scopes>` | Comma-separated scopes (overrides defaults) | — |
| `--add-scopes <scopes>` | Additional scopes to add to defaults | — |
| `--exclude <scopes>` | Scopes to exclude from defaults | — |

**Personal account default scopes**: `Mail.ReadWrite`, `Mail.Send`, `Calendars.ReadWrite`, `Files.ReadWrite`, `User.Read`, `Contacts.Read`, `offline_access`

### m365 logout

Clear stored credentials.

```
m365 logout
```

---

## Mail Commands

### m365 mail list

List emails from a folder.

```
m365 mail list [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--top <n>` / `-t <n>` | Number of emails | `10` |
| `--folder <name>` / `-f <name>` | Folder: `inbox`, `sent`, `drafts`, `deleted`, `junk`, or folder ID | `inbox` |
| `--json` | JSON output | — |
| `--focused` | Show only Focused Inbox emails | — |

### m365 mail read

Read a single email by ID.

```
m365 mail read <id> [options]
```

| Argument | Description |
|----------|-------------|
| `<id>` | Email ID (from list/search output) |

| Option | Description |
|--------|-------------|
| `--force` | Skip trusted-sender whitelist check, show full content |
| `--json` | JSON output |

**Note**: Untrusted sender content is filtered by default. Use `--force` to bypass.

### m365 mail send

Send an email.

```
m365 mail send <to> <subject> <body> [options]
```

| Argument | Description |
|----------|-------------|
| `<to>` | Recipient email(s), comma-separated |
| `<subject>` | Email subject |
| `<body>` | Email body (HTML supported) |

| Option | Description |
|--------|-------------|
| `--attach <files...>` / `-a <files...>` | Attach one or more files |
| `--cc <emails>` | CC recipients, comma-separated |
| `--bcc <emails>` | BCC recipients, comma-separated |
| `--json` | JSON output |

### m365 mail search

Search emails by keyword.

```
m365 mail search <query> [options]
```

| Argument | Description |
|----------|-------------|
| `<query>` | Search query string |

| Option | Description | Default |
|--------|-------------|---------|
| `--top <n>` / `-t <n>` | Max results | `10` |
| `--json` | JSON output | — |

### m365 mail attachments

List attachments for an email.

```
m365 mail attachments <id> [options]
```

| Argument | Description |
|----------|-------------|
| `<id>` | Email ID |

| Option | Description |
|--------|-------------|
| `--json` | JSON output |

### m365 mail download-attachment

Download a specific attachment.

```
m365 mail download-attachment <message-id> <attachment-id> [local-path] [options]
```

| Argument | Description |
|----------|-------------|
| `<message-id>` | Email ID |
| `<attachment-id>` | Attachment ID (from `attachments` command) |
| `[local-path]` | Download destination (default: original filename) |

| Option | Description |
|--------|-------------|
| `--json` | JSON output |

### m365 mail trust

Add email or domain to trusted senders whitelist.

```
m365 mail trust <email>
```

| Argument | Description |
|----------|-------------|
| `<email>` | Email address (`user@example.com`) or domain (`@example.com`) |

### m365 mail untrust

Remove email or domain from whitelist.

```
m365 mail untrust <email>
```

### m365 mail trusted

List all trusted senders.

```
m365 mail trusted [options]
```

| Option | Description |
|--------|-------------|
| `--json` | JSON output |

### m365 mail delete

Delete an email (moves to Deleted Items).

```
m365 mail delete <id> [options]
```

| Argument | Description |
|----------|-------------|
| `<id>` | Email ID |

| Option | Description |
|--------|-------------|
| `--force` | Skip confirmation prompt |
| `--json` | JSON output |

### m365 mail move

Move an email to another folder.

```
m365 mail move <id> <destination> [options]
```

| Argument | Description |
|----------|-------------|
| `<id>` | Email ID |
| `<destination>` | Folder name (`inbox`, `sent`, `drafts`, `deleted`, `junk`, `archive`) or folder ID |

| Option | Description |
|--------|-------------|
| `--json` | JSON output |

**Note**: Moving a message creates a new copy — the returned ID is the new message ID.

### m365 mail folder list

List mail folders.

```
m365 mail folder list [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--top <n>` / `-t <n>` | Max folders | `50` |
| `--parent <folder>` | List child folders of this folder (name or ID) | — |
| `--json` | JSON output | — |

### m365 mail folder create

Create a new mail folder.

```
m365 mail folder create <name> [options]
```

| Argument | Description |
|----------|-------------|
| `<name>` | Display name for the new folder |

| Option | Description |
|--------|-------------|
| `--parent <folder>` | Create as child of this folder (name or ID) |
| `--json` | JSON output |

### m365 mail folder delete

Delete a mail folder and all its contents.

```
m365 mail folder delete <id> [options]
```

| Argument | Description |
|----------|-------------|
| `<id>` | Folder ID |

| Option | Description |
|--------|-------------|
| `--force` | Skip confirmation prompt |
| `--json` | JSON output |

### m365 mail reply

Reply to an email. When attachments are provided, uses an internal draft-based flow.

```
m365 mail reply <id> <content> [options]
```

| Argument | Description |
|----------|-------------|
| `<id>` | Message ID to reply to |
| `<content>` | Reply message content |

| Option | Description |
|--------|-------------|
| `--html` | Treat content as HTML |
| `--attach <files...>` / `-a <files...>` | Attach one or more files |
| `--json` | JSON output |

### m365 mail reply-all

Reply to all recipients of an email. When attachments are provided, uses an internal draft-based flow.

```
m365 mail reply-all <id> <content> [options]
```

| Argument | Description |
|----------|-------------|
| `<id>` | Message ID to reply to |
| `<content>` | Reply-all message content |

| Option | Description |
|--------|-------------|
| `--html` | Treat content as HTML |
| `--attach <files...>` / `-a <files...>` | Attach one or more files |
| `--json` | JSON output |

### m365 mail forward

Forward an email to one or more recipients. When attachments are provided, uses an internal draft-based flow.

```
m365 mail forward <id> <to> [comment] [options]
```

| Argument | Description |
|----------|-------------|
| `<id>` | Message ID to forward |
| `<to>` | Recipient email(s), comma-separated |
| `[comment]` | Optional comment to include |

| Option | Description |
|--------|-------------|
| `--html` | Treat comment as HTML |
| `--attach <files...>` / `-a <files...>` | Attach one or more files |
| `--json` | JSON output |
---

## Calendar Commands

Alias: `m365 cal` = `m365 calendar`

### m365 cal list

List upcoming calendar events.

```
m365 cal list [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--days <n>` / `-d <n>` | Look-ahead days | `7` |
| `--top <n>` / `-t <n>` | Max events | `50` |
| `--json` | JSON output | — |

### m365 cal get

Get event details by ID.

```
m365 cal get <id> [options]
```

| Option | Description |
|--------|-------------|
| `--json` | JSON output |

### m365 cal create

Create a new calendar event.

```
m365 cal create <title> [options]
```

| Argument | Description |
|----------|-------------|
| `<title>` | Event title |

| Option | Description | Required |
|--------|-------------|----------|
| `--start <datetime>` / `-s` | Start time (`YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD`) | **Yes** |
| `--end <datetime>` / `-e` | End time | **Yes** |
| `--location <loc>` / `-l` | Location | No |
| `--body <text>` / `-b` | Description | No |
| `--attendees <emails>` / `-a` | Attendees, comma-separated | No |
| `--allday` | All-day event flag | No |
| `--json` | JSON output | No |

### m365 cal update

Update an existing event.

```
m365 cal update <id> [options]
```

| Option | Description |
|--------|-------------|
| `--title <title>` / `-t` | New title |
| `--start <datetime>` / `-s` | New start time |
| `--end <datetime>` / `-e` | New end time |
| `--location <loc>` / `-l` | New location |
| `--body <text>` / `-b` | New description |
| `--json` | JSON output |

### m365 cal delete

Delete a calendar event.

```
m365 cal delete <id> [options]
```

| Option | Description |
|--------|-------------|
| `--json` | JSON output |

---

## OneDrive Commands

Alias: `m365 od` = `m365 onedrive`

### m365 od ls

List files and folders.

```
m365 od ls [path] [options]
```

| Argument | Description | Default |
|----------|-------------|---------|
| `[path]` | Folder path | root |

| Option | Description | Default |
|--------|-------------|---------|
| `--top <n>` / `-t <n>` | Max items | `100` |
| `--json` | JSON output | — |

### m365 od get

Get file/folder metadata.

```
m365 od get <path> [options]
```

| Option | Description |
|--------|-------------|
| `--json` | JSON output |

### m365 od download

Download a file.

```
m365 od download <remote-path> [local-path] [options]
```

| Argument | Description |
|----------|-------------|
| `<remote-path>` | File path on OneDrive |
| `[local-path]` | Local destination (default: current directory) |

| Option | Description |
|--------|-------------|
| `--json` | JSON output |

### m365 od upload

Upload a file. Files ≥4MB use automatic chunked upload.

```
m365 od upload <local-path> [remote-path] [options]
```

| Argument | Description |
|----------|-------------|
| `<local-path>` | Local file to upload |
| `[remote-path]` | Remote destination (default: root, same name) |

| Option | Description |
|--------|-------------|
| `--json` | JSON output |

### m365 od search

Search files by name/content.

```
m365 od search <query> [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--top <n>` / `-t <n>` | Max results | `50` |
| `--json` | JSON output | — |

### m365 od share

Create a sharing link.

```
m365 od share <path> [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--type <view\|edit>` | Link type | `view` |
| `--scope <organization\|anonymous\|users>` | Sharing scope | `anonymous` |
| `--json` | JSON output | — |

### m365 od invite

Invite a user to access a file/folder.

```
m365 od invite <path> <email> [options]
```

| Argument | Description |
|----------|-------------|
| `<path>` | File/folder path |
| `<email>` | Email(s), comma-separated |

| Option | Description | Default |
|--------|-------------|---------|
| `--role <read\|write>` | Permission level | `read` |
| `--message <msg>` | Invitation message | — |
| `--no-notify` | Don't send email notification | — |
| `--json` | JSON output | — |

### m365 od mkdir

Create a folder.

```
m365 od mkdir <path> [options]
```

| Option | Description |
|--------|-------------|
| `--json` | JSON output |

### m365 od rm

Delete a file or folder.

```
m365 od rm <path> [options]
```

| Option | Description |
|--------|-------------|
| `--force` | Skip confirmation prompt |
| `--json` | JSON output |

---

## User Commands

### m365 user search

Search contacts and people by name.

```
m365 user search <name> [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--top <n>` / `-t <n>` | Max results per source | `10` |
| `--json` | JSON output | — |

---

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `M365_TENANT_ID` | Azure AD tenant ID (custom app) | `5b4c4b46-...` |
| `M365_CLIENT_ID` | Azure AD client ID (custom app) | `091b3d7b-...` |
| `M365_TIMEZONE` | Override timezone for calendar | `Asia/Shanghai` |

### Files

| Path | Description |
|------|-------------|
| `~/.m365-cli/credentials.json` | Stored OAuth tokens (mode 600) |
| `~/.m365-cli/trusted-senders.txt` | Trusted senders whitelist |

### Default Configuration

Located at `<install-dir>/config/default.json`:

```json
{
  "tenantId": "common",
  "clientId": "091b3d7b-e217-4410-868c-01c3ee6189b6",
  "graphApiUrl": "https://graph.microsoft.com/v1.0",
  "authUrl": "https://login.microsoftonline.com",
  "credsPath": "~/.m365-cli/credentials.json",
  "timezone": ""
}
```

Pre-configured shared Azure AD app works out of the box — no setup needed.

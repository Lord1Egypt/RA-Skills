---
name: officeclaw
description: Connect to personal Microsoft accounts via Microsoft Graph API to manage email, calendar events, and tasks. Use this skill when the user needs to read/write Outlook mail, manage calendar appointments, or handle Microsoft To Do tasks.
license: Apache-2.0
homepage: https://github.com/danielithomas/officeclaw
user-invocable: true
compatibility: Requires Python 3.10+, network access to graph.microsoft.com, and one-time OAuth setup
metadata:
  author: Daniel Thomas
  version: "1.1.1"
  openclaw:
    requires:
      anyBins: ["python", "python3", "officeclaw"]
      env: []
    os: ["darwin", "linux", "win32"]
---

# OfficeClaw: Microsoft Graph API Integration

Connect your OpenClaw agent to personal Microsoft accounts (Outlook.com, Hotmail, Live) to manage email, calendar, and tasks through the Microsoft Graph API.

## Installation

**This skill documents officeclaw 1.1.1.** Earlier versions lack the commands
below — `--list-name`, the due-date filters, `--repeat`, `tasks steps`,
`mail download-all`, `calendar --recurrence`, `auth refresh` and JSON error
output — and they do not check calendar attendees against the recipient
allowlist. Install or upgrade to at least 1.1.1:

```bash
pip install --upgrade "officeclaw>=1.1.1"
```

Or with uv:

```bash
uv pip install --upgrade "officeclaw>=1.1.1"
```

Verify the installed version:

```bash
officeclaw --version   # expect 1.1.1 or newer
```

Requires Python 3.10 or newer (3.9 reached end of life in October 2025, and the
patched releases of the dependencies need 3.10).

## Setup (One-Time)

> **Quick start:** OfficeClaw ships with a default app registration — just run `officeclaw auth login` and go. No Azure setup needed.
>
> **Advanced:** Want full control? Create your own Azure App Registration (free, ~5 minutes) and set `OFFICECLAW_CLIENT_ID` in your `.env`. See [Microsoft's guide](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app) or follow the steps below.

### 1. Create an Azure App Registration

1. Go to [entra.microsoft.com](https://entra.microsoft.com) → App registrations → New registration
2. Name: `officeclaw` (or anything you like)
3. Supported account types: **Personal Microsoft accounts only**
4. Redirect URI: leave blank (not needed for device code flow)
5. Click **Register**
6. Copy the **Application (client) ID** — this is your `OFFICECLAW_CLIENT_ID`
7. Go to **Authentication** → Advanced settings → **Allow public client flows** → **Yes** → Save
8. Go to **API permissions** → Add permission → Microsoft Graph → Delegated permissions. Choose based on your needs:

**Read-only (safest):**
- `Mail.Read`, `Calendars.Read`, `Tasks.ReadWrite`*

**Full access (all features including send/delete):**
- `Mail.Read`, `Mail.ReadWrite`, `Mail.Send`
- `Calendars.Read`, `Calendars.ReadWrite`
- `Tasks.ReadWrite`

*\*Tasks.ReadWrite is the minimum available scope for Microsoft To Do — there is no read-only option.*

> **Least privilege:** Only grant the permissions you actually need. If you only want to read emails and calendar, skip `Mail.ReadWrite`, `Mail.Send`, and `Calendars.ReadWrite`. OfficeClaw will gracefully error on commands that require missing permissions.

### 2. Configure Environment

Create a `.env` file in your skill directory:

```bash
OFFICECLAW_CLIENT_ID=your-client-id-here

# Capability gates (disabled by default for safety)
# OFFICECLAW_ENABLE_SEND=true    # Allow sending/replying/forwarding emails
# OFFICECLAW_ENABLE_DELETE=true   # Allow deleting emails, events, and tasks

# Recipient allowlist — STRONGLY RECOMMENDED when sending is enabled
# OFFICECLAW_ALLOWED_RECIPIENTS=user1@example.com,user2@example.com

# Attachment directories — restricts which files can be attached or downloaded to
# OFFICECLAW_ALLOWED_ATTACHMENT_DIRS=~/.openclaw/workspace/wip

# Where downloaded attachments are saved when --dest is omitted
# OFFICECLAW_DOWNLOADS_DIR=~/.openclaw/workspace/wip/downloads

# Default task list, so task commands need no --list-id / --list-name
# OFFICECLAW_DEFAULT_TASK_LIST_NAME=Tasks

# Timezone used to decide what "today" means for --overdue
# OFFICECLAW_TIMEZONE=Australia/Melbourne
```

No client secret needed for device code flow. Write operations (send, delete) are **disabled by default** — enable only what you need.

> ⚠️ **Recipient Allowlist (v1.0.4+):** If you enable sending, configure `OFFICECLAW_ALLOWED_RECIPIENTS` to restrict which addresses can receive email. This is especially critical for AI agent workflows — the allowlist provides a hard, code-level boundary that prevents sending to unauthorized addresses regardless of what the agent is instructed to do. Blocked attempts are logged for auditing. As of v1.1.0 it covers every send path, including reply, reply-all, forward and the Python API.

> ⚠️ **Attachment Directories (v1.1.0+):** `mail send --attachment` can read any file this process can read. Set `OFFICECLAW_ALLOWED_ATTACHMENT_DIRS` to a dedicated drop directory (for example `~/.openclaw/workspace/wip`) and copy files there when you want them sent, so an agent cannot attach credentials or keys straight off disk.

Optional: persistent preferences live in `~/.config/officeclaw/config.toml`.

```toml
default_task_list_name = "Tasks"
default_output = "json"
timezone = "Australia/Melbourne"
```

Precedence is command-line flag → environment variable → config file → default.
Security settings (`enable_send`, allowlists, credentials) are **ignored** if
placed in this file; they must come from the environment.

### 3. Authenticate

```bash
officeclaw auth login
```

This displays a URL and code. Open the URL in a browser, enter the code, and sign in with your Microsoft account. Tokens are stored securely in `~/.officeclaw/token_cache.json` (permissions 600).

## When to Use This Skill

Activate this skill when the user needs to:

### Email Operations
- **Read emails**: "Show me my latest emails", "Find emails from john@example.com"
- **Send emails**: "Send an email to...", "Reply to the last email from..."
- **Manage inbox**: "Mark emails as read", "Archive old emails", "Delete emails"

### Calendar Operations
- **View events**: "What's on my calendar today?", "Show meetings this week"
- **Create events**: "Schedule a meeting with...", "Add dentist appointment on Friday"
- **Update events**: "Move the 2pm meeting to 3pm", "Cancel tomorrow's standup"

### Task Management
- **List tasks**: "What's on my to-do list?", "Show incomplete tasks"
- **Create tasks**: "Add 'buy groceries' to my tasks", "Create a task to review report"
- **Complete tasks**: "Mark 'finish proposal' as done", "Complete all shopping tasks"

## Available Commands

### Authentication

```bash
officeclaw auth login       # Authenticate via device code flow
officeclaw auth status      # Check authentication status
officeclaw auth refresh     # Refresh the token without logging in again
officeclaw auth logout      # Clear stored tokens

# For scheduled jobs: exits 1 when an interactive login is required
officeclaw auth refresh --json
```

### Mail Commands

```bash
officeclaw mail list --limit 10                # List recent messages
officeclaw mail list --unread                   # List unread messages only
officeclaw mail get <message-id>               # Get specific message
officeclaw mail send --to user@example.com --subject "Hello" --body "Message text"
officeclaw mail send --to user@example.com --subject "Report" --body "Attached" --attachment report.pdf
officeclaw mail search "from:boss@example.com"   # QUERY is positional
officeclaw mail archive <message-id>           # Archive a message
officeclaw mail mark-read <message-id>         # Mark as read
officeclaw mail move <message-id> --folder Archive

# Replying and forwarding also need OFFICECLAW_ENABLE_SEND=true, and are
# subject to the recipient allowlist — reply-all is blocked if any address on
# the thread is unlisted.
officeclaw mail reply <message-id> --body "Thanks"
officeclaw mail reply <message-id> --body "Thanks" --reply-all
officeclaw mail forward <message-id> --to colleague@example.com --comment "FYI"

# Needs OFFICECLAW_ENABLE_DELETE=true
officeclaw mail delete <message-id>
officeclaw mail list --json                    # JSON output for parsing

# Attachments — all require OFFICECLAW_ENABLE_ATTACHMENT_DOWNLOAD=true
officeclaw mail attachments <message-id>                     # List them
officeclaw mail download <message-id> <attachment-name>      # One, by name
officeclaw mail download <message-id> <name> ./path/file.pdf # One, to a path
officeclaw mail download-all <message-id>                    # All of them
officeclaw mail download-all <message-id> --dest ./somewhere # All, to a directory
# Default location: OFFICECLAW_DOWNLOADS_DIR, else officeclaw_downloads/ inside
# the first allowed attachment directory, else the platform's Downloads folder.
# The JSON output reports the path each file was written to.
```

### When to Use Attachment Commands

Activate attachment commands when the user needs to:
- **List attachments**: "Show me the attachments for this email" or "What files are attached to the latest message?"
- **Download attachments**: "Download the attached PDF" (`mail download`) or "Save everything attached to that email" (`mail download-all`)

### Attachment Security for Agents

Every download path — `mail download` and `mail download-all` alike — applies
the same checks, in this order:

1. **Default-deny**: downloading is disabled unless `OFFICECLAW_ENABLE_ATTACHMENT_DOWNLOAD=true`
2. **Safe senders**: with `OFFICECLAW_SAFE_SENDERS_ONLY=true`, only senders matching `OFFICECLAW_SAFE_SENDERS_LIST` (exact address, or `@domain.com` wildcard) can be downloaded from
3. **Size and type**: `OFFICECLAW_ATTACHMENT_MAX_SIZE_MB` (default 25) and `OFFICECLAW_ATTACHMENT_ALLOWED_TYPES` (default `*`). In `download-all`, an attachment that fails either is reported as skipped and the rest continue
4. **Destination**: when `OFFICECLAW_ALLOWED_ATTACHMENT_DIRS` is set, files can only be written inside it — including the path argument to `mail download`, so naming a path does not escape the boundary
5. **Filenames**: names come from the sender, so they are reduced to a bare, portable filename before writing (`../../.ssh/authorized_keys` becomes `authorized_keys`), and an existing file is never overwritten — a collision becomes `report (1).pdf`

Also worth knowing:

- **Confirm before downloading** files from senders the user has not mentioned.
- **Item and reference attachments** (a forwarded email, a cloud link) have no bytes to save; their metadata is written as a `.json` file instead.
- **Blocked attempts are logged** to `~/.openclaw/workspace/automation/logs/email-blocked.log`, with an `email-alert.json` for monitoring. Successful downloads are not logged — the JSON output is the record, and it reports the path of every file written.
- `OFFICECLAW_ATTACHMENT_DOWNLOAD_PATH` was the v1.0.5 name for `OFFICECLAW_DOWNLOADS_DIR`. It still works, with a deprecation warning.

### Calendar Commands

```bash
officeclaw calendar list --start 2026-02-01 --end 2026-02-28
officeclaw calendar create \
  --subject "Team Meeting" \
  --start "2026-02-15T10:00:00" \
  --end "2026-02-15T11:00:00" \
  --location "Conference Room"
officeclaw calendar get <event-id>
officeclaw calendar update <event-id> --subject "Updated Meeting"
officeclaw calendar update <event-id> --attendee alice@example.com   # Replaces the attendee list
officeclaw calendar list-calendars

# Responding to an invitation
officeclaw calendar accept <event-id> --comment "See you there"
officeclaw calendar decline <event-id>

# Needs OFFICECLAW_ENABLE_DELETE=true
officeclaw calendar delete <event-id>
officeclaw calendar delete <event-id>
officeclaw calendar list --start 2026-02-01 --end 2026-02-28 --json

# Recurring events, attendees, Teams meetings, timezone
officeclaw calendar create \
  --subject "Weekly team sync" \
  --start "2026-09-08T10:00:00" --end "2026-09-08T11:00:00" \
  --timezone "AUS Eastern Standard Time" \
  --attendee alice@example.com --attendee bob@example.com \
  --online-meeting \
  --recurrence weekly --recurrence-count 12

# --recurrence and tasks --repeat share one syntax:
#   daily            daily:3          every day / every third day
#   weekly           weekly:MON,WED   the start weekday / named days
#   fortnightly      weekdays         every second week / Mon-Fri
#   monthly          monthly:15       the start day of month / the 15th
#   yearly                            annually on the start date
# End a calendar series with --recurrence-until YYYY-MM-DD or --recurrence-count N (not both)
```

### Task Commands

```bash
officeclaw tasks list-lists                     # List task lists

# Name a list instead of pasting an ID. With neither, the account's built-in
# Tasks list is used, or OFFICECLAW_DEFAULT_TASK_LIST_NAME / _ID if set.
officeclaw tasks list                           # Default list
officeclaw tasks list --list-name "Tasks"
officeclaw tasks list --list-name "🛒 Groceries"
officeclaw tasks list --list-id <list-id>       # Still works

officeclaw tasks list --status active           # Active tasks only
officeclaw tasks list --limit 20

# Due-date filters (see the note under Output Format — these are client-side)
officeclaw tasks list --overdue
officeclaw tasks list --due-on 2026-09-06
officeclaw tasks list --due-before 2026-09-10
officeclaw tasks list --due-after 2026-09-04

# Create with full metadata in one command
officeclaw tasks create \
  --list-name "Tasks" \
  --title "Call accountant" \
  --body "Ask about GST registration. Mention DGR1 timeline." \
  --due-date 2026-09-15 \
  --importance high \
  --reminder "2026-09-15T08:00:00" \
  --category "finance,admin"

officeclaw tasks update --task-id <task-id> --reminder "2026-09-16T08:00:00"
officeclaw tasks update --task-id <task-id> --no-reminder    # Clear the reminder

# Repeating tasks
officeclaw tasks create --title "Water plants" --repeat "weekly:MON,THU"
officeclaw tasks create --title "Rent" --due-date 2026-10-01 --repeat monthly
officeclaw tasks update --task-id <task-id> --no-repeat      # Stop repeating

# Steps (checklist items within a task)
officeclaw tasks steps list --task-id <task-id>
officeclaw tasks steps add --task-id <task-id> "Buy pots"
officeclaw tasks steps complete --task-id <task-id> --item-id <item-id>
officeclaw tasks steps complete --task-id <task-id> --item-id <item-id> --undo
officeclaw tasks steps delete --task-id <task-id> --item-id <item-id>
officeclaw tasks complete --task-id <task-id>
officeclaw tasks reopen --task-id <task-id>
officeclaw tasks get --task-id <task-id> --json

# Needs OFFICECLAW_ENABLE_DELETE=true
officeclaw tasks delete --task-id <task-id>
```

## Output Format

Use `--json` for structured output. The flag works **either before or after the
subcommand** — both of these are equivalent:

```bash
officeclaw mail list --json
officeclaw --json mail list
```

Every response is wrapped in the same envelope, and the objects inside `data`
are Microsoft Graph objects passed through unchanged — field names and values
are Graph's own (for example task status is `notStarted`, not `active`, and
`dueDateTime` is an object, not a string):
```json
{
  "status": "success",
  "data": [
    {
      "id": "AAMkADEzN...",
      "subject": "Meeting Notes",
      "from": {"emailAddress": {"address": "sender@example.com"}},
      "receivedDateTime": "2026-02-12T10:30:00Z",
      "isRead": false
    }
  ]
}
```

**Failures are JSON too**, so a script never has to parse prose. Exit status is
`0` on success and `1` on any failure:

```json
{
  "status": "error",
  "error": {
    "code": "AuthenticationError",
    "message": "No authentication tokens found. Run 'officeclaw auth login' to authenticate."
  }
}
```

Branch on `error.code`: `AuthenticationError` needs a human, `TooManyRequests`
is worth retrying, `CapabilityDisabled` means a gate is off by design.

**Due-date filters are applied client-side.** Microsoft To Do cannot filter on
due dates server-side, so `--overdue` and friends fetch the list and filter
locally. Fine for personal lists; not a cheap query on a very large one. Due
dates are compared by calendar date, because To Do drops the time portion.

**`--overdue` uses the user's timezone**, not UTC — a due date has no timezone
attached, and in Australia a morning briefing runs while UTC is still on
yesterday. Set `OFFICECLAW_TIMEZONE` to pin it (e.g. `Australia/Melbourne`);
otherwise the system timezone applies.

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `AuthenticationError` | Not logged in or token expired | Run `officeclaw auth login` |
| `AccessDenied` | Missing permissions | Re-authenticate with required scopes |
| `ResourceNotFound` | Invalid ID | Verify the ID exists |
| `RateLimitError` | Too many API calls | Wait 60 seconds and retry |
| `TaskListError` | `--list-name` matched no list, or several | Run `officeclaw tasks list-lists`, or pass `--list-id` |
| `CapabilityDisabled` | Write gate not enabled | Set `OFFICECLAW_ENABLE_SEND` / `_DELETE` in `.env` |
| `RecipientNotAllowedError` | Address not on the allowlist | Add it to `OFFICECLAW_ALLOWED_RECIPIENTS` |
| `AttachmentNotAllowedError` | File or destination outside the allowed directories | Use a directory in `OFFICECLAW_ALLOWED_ATTACHMENT_DIRS` |

## Guidelines for Agents

When using this skill:

1. **Confirm destructive actions**: Ask before deleting or sending
2. **Summarize results**: Don't show raw JSON, provide summaries
3. **Handle errors gracefully**: Guide user through re-authentication
4. **Respect privacy**: Don't log email content
5. **Use JSON mode**: For programmatic parsing, use `--json` — including for errors
6. **Batch operations**: Process multiple items efficiently
7. **Name lists, don't paste IDs**: `--list-name "Tasks"`, or rely on the default list
8. **Check auth before long jobs**: `officeclaw auth refresh --json` exits 1 if a login is needed. `auth status --json` always exits 0 — it returns `"data": null` when not authenticated, so test for that rather than for a non-zero exit

## Security & Privacy

- **Write operations disabled by default**: Send, reply, forward, and delete are all blocked unless explicitly enabled via `OFFICECLAW_ENABLE_SEND` and `OFFICECLAW_ENABLE_DELETE` environment variables. This prevents accidental or unauthorised write actions.
- **Recipient allowlist (v1.0.4+, extended in v1.1.0 and v1.1.1)**: When `OFFICECLAW_ALLOWED_RECIPIENTS` is set, outbound email is restricted to listed addresses only — on **every** path: send (including cc and bcc), reply, reply-all, forward, **calendar attendees** (an invitation is email), and the Python API. Blocked attempts are logged to `email-blocked.log` and an `email-alert.json` alert file is written for monitoring. If not set, a runtime warning is displayed on each send. **Strongly recommended for any AI agent deployment.**
- **Download location (v1.1.0+)**: with no `--dest`, files go to `OFFICECLAW_DOWNLOADS_DIR`, else `officeclaw_downloads/` inside the first allowed attachment directory, else inside the platform's Downloads folder. Saved names are made legal on Windows, macOS and Linux alike.
- **Attachment directories (v1.1.0+)**: `OFFICECLAW_ALLOWED_ATTACHMENT_DIRS` governs both directions — where files may be attached *from* and where downloads may be written *to*. Downloaded filenames are reduced to a bare name, so a message cannot steer a write with a name like `../../.ssh/authorized_keys`, and existing files are never overwritten.
- **`.env` cannot weaken injected settings (v1.1.0+)**: where a supervising process sets a security variable, `.env` composes with it to the stricter value — allowlists intersect, capability gates need both sources, restrictions apply if either asks. An entry that is dropped is reported with a warning, so nothing is ignored silently.
- **Config file cannot weaken security**: `~/.config/officeclaw/config.toml` sets conveniences only. Capability gates and both allowlists are read from the environment alone, so a process that can write the config file cannot grant itself the ability to send mail.
- **No client secret required**: Uses device code flow (public client) by default
- **Least-privilege permissions**: You choose which Graph API scopes to grant — read-only is sufficient for most use cases. See the setup guide above.
- **Tokens stored securely**: `~/.officeclaw/token_cache.json` with 600 file permissions
- **No data storage**: OfficeClaw passes data through, never stores email/calendar content
- **No telemetry**: No usage data collected
- **Your own Azure app**: Each user creates their own Azure app registration with their own client ID — no shared credentials

## Troubleshooting

If the skill isn't working:

1. **Check authentication**: Run `officeclaw auth status`
2. **Re-authenticate**: Run `officeclaw auth login`
3. **Verify network**: Ensure `graph.microsoft.com` is reachable
4. **Check environment**: Verify `OFFICECLAW_CLIENT_ID` is set in `.env`
5. **List name not found**: names are cached in `~/.officeclaw/list_cache.json`; renaming a list in To Do self-heals on the next lookup, but `officeclaw tasks list-lists` forces a refresh
6. **JSON output has warnings mixed in**: warnings go to stderr, never stdout — redirect with `2>/dev/null` if a parser is strict

## References

- [OfficeClaw on GitHub](https://github.com/danielithomas/officeclaw)
- [OfficeClaw on PyPI](https://pypi.org/project/officeclaw/)
- [Microsoft Graph API](https://docs.microsoft.com/graph/)
- [OpenClaw](https://docs.openclaw.ai)

# google-workspace

> OpenClaw skill for Google Workspace — one skill to rule Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, Tasks, Meet, and every other Workspace API.

## What is this?

An [OpenClaw](https://openclaw.ai) agent skill that wraps the official [`gws` CLI](https://github.com/googleworkspace/cli) (Google Workspace CLI). It gives your AI agent full access to Google Workspace through structured JSON commands — no custom API integrations needed.

## Install

```bash
clawhub install google-workspace
```

Or manually copy the `SKILL.md` into your OpenClaw skills directory.

### Dependency

The skill requires the `gws` CLI:

```bash
npm install -g @googleworkspace/cli
```

## What can it do?

Everything the Google Workspace APIs support, including:

| Service | Examples |
|---------|----------|
| **Drive** | List, upload, download, share files and folders |
| **Gmail** | Read, send, search, label, filter emails |
| **Calendar** | Create events, check availability, manage attendees |
| **Sheets** | Read/write cells, append rows, create spreadsheets |
| **Docs** | Create documents, insert/edit text |
| **Chat** | Send messages to spaces |
| **Tasks** | Create/list/manage task lists and tasks |
| **Admin** | User management, directory queries |
| **Meet** | Create meeting spaces, review participants |
| **Slides** | Create presentations |
| **Forms** | Collect and review responses |
| **Contacts** | Sync and manage contacts |

The `gws` CLI dynamically discovers all Workspace APIs from Google's Discovery Service — when Google adds new endpoints, they're available immediately without a CLI update.

## Auth Setup

### Desktop (with browser)

```bash
gws auth setup          # one-time GCP project setup
gws auth login -s drive,gmail,calendar,sheets
```

### Headless server

Export credentials from a desktop machine:

```bash
gws auth export --unmasked > credentials.json
```

Then on your server:

```bash
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/to/credentials.json
```

## Quick Examples

```bash
# List recent Drive files
gws drive files list --params '{"pageSize": 10}'

# Search Gmail
gws gmail users-messages list --params '{"userId": "me", "q": "is:unread from:boss"}'

# Create a calendar event
gws calendar events insert \
  --params '{"calendarId": "primary"}' \
  --json '{"summary": "Standup", "start": {"dateTime": "2026-03-07T09:00:00Z"}, "end": {"dateTime": "2026-03-07T09:30:00Z"}}'

# Read a spreadsheet
gws sheets spreadsheets-values get --params '{"spreadsheetId": "ID", "range": "Sheet1!A1:D10"}'
```

## Links

- **gws CLI**: https://github.com/googleworkspace/cli
- **OpenClaw**: https://openclaw.ai
- **ClawHub**: https://clawhub.com

## Disclaimer

The `gws` CLI is **not an officially supported Google product**. See the [upstream repository](https://github.com/googleworkspace/cli) for details.

## License

MIT

---
name: gmail-bridge
description: Google Workspace Bridge (Gmail, Drive, Sheets, Calendar) via local API at http://127.0.0.1:8787
homepage: local
metadata: {"clawdbot":{"emoji":"📧","requires":{"bins":["curl","jq"]}}}
---

# gmail-bridge

Use this skill whenever the user asks about:
- latest emails / unread emails / email search
- reading a specific email
- searching Google Drive files
- reading/writing Google Sheets ranges
- checking calendar events or creating events

## IMPORTANT BEHAVIOR RULES (for a good assistant experience)
- Do NOT return Gmail message IDs alone unless the user explicitly asks.
- For “check my latest email(s)”, return a short list of the latest 5–10 items with:
  **Subject, From, Date, Snippet**
- If the user asks “open email #3” or similar, call `get` on that message ID and summarize.
- For Sheets/Drive/Calendar, always show a concise summary and ask a follow-up only when an ID/range/time window is missing.

## How to use

### Gmail
1) Latest emails (returns summaries):
- `bash run.sh recent 10`

2) Unread emails:
- `bash run.sh unread 10`

3) Search emails (Gmail query syntax):
- `bash run.sh search "from:amazon subject:invoice" 10`

4) Forward an email to a specific address:
- `bash run.sh forward <messageId> <emailAddress>`
- For example: `bash run.sh forward 19c647bc33f89bdd christopher.tock@gmail.com`

5) Email details:
- `bash run.sh get <messageId> metadata`
- formats: `metadata` (default), `full`, `raw`

### Gmail
1) Latest emails (returns summaries):
- `bash run.sh recent 10`

2) Unread emails:
- `bash run.sh unread 10`

3) Search emails (Gmail query syntax):
- `bash run.sh search "from:amazon subject:invoice" 10`

4) Email details:
- `bash run.sh get <messageId> metadata`
- formats: `metadata` (default), `full`, `raw`

### Drive
1) Search files (Drive query language):
- `bash run.sh drive-search "name contains 'FutureReady'" 10`

2) Get file metadata:
- `bash run.sh drive-file <fileId>`

### Sheets
1) Read a range:
- `bash run.sh sheets-get <spreadsheetId> "Sheet1!A1:D20"`

2) Write values:
- `bash run.sh sheets-set <spreadsheetId> "Sheet1!A1:B2" '[[\"A1\",\"B1\"],[\"A2\",\"B2\"]]'`

### Calendar
1) List events:
- `bash run.sh cal-events 10 2026-02-01T00:00:00Z 2026-03-01T00:00:00Z primary`

2) Create an event:
- `bash run.sh cal-create "Workshop" 2026-02-20T02:00:00Z 2026-02-20T03:00:00Z primary "Bangi" "Prep session"`

## Auth / Security
- This skill calls a local bridge on 127.0.0.1. If the bridge enforces a secret header, set:
  `export BRIDGE_SECRET="..."` before running commands.
- The bridge uses OAuth tokens stored on the server.

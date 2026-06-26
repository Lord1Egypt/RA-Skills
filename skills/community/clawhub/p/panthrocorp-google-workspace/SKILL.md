---
name: Google Workspace
description: Gmail, Contacts, Calendar, Drive (with comments), Docs, and Sheets for OpenClaw agents
version: 0.5.2 # x-release-please-version
author: panthrocorp
license: MIT-0
metadata:
  openclaw:
    requires:
      env:
        - GOOGLE_WORKSPACE_TOKEN_KEY
        - GOOGLE_CLIENT_ID
        - GOOGLE_CLIENT_SECRET
      bins:
        - google-workspace
    emoji: "📧"
    homepage: https://github.com/PanthroCorp-Limited/openclaw-skills
    os: ["linux"]
---

# Google Workspace Skill

Access Gmail (read-only), Google Calendar (configurable), Google Contacts (read-only), Google Drive (configurable, with comments), Google Docs (configurable), and Google Sheets (configurable).

## Installation

Download the latest release binary for linux/arm64 and install to `~/.openclaw/bin/`:

```bash
TAG=$(curl -fsSL "https://api.github.com/repos/PanthroCorp-Limited/openclaw-skills/releases" \
  | grep -o '"tag_name":"google-workspace/v[^"]*"' | head -1 | cut -d'"' -f4)
VERSION=${TAG#google-workspace/v}
curl -fsSL "https://github.com/PanthroCorp-Limited/openclaw-skills/releases/download/${TAG}/google-workspace_${VERSION}_linux_arm64.tar.gz" \
  | tar -xz -C ~/.openclaw/bin/ google-workspace
chmod +x ~/.openclaw/bin/google-workspace
```

## Important

- Gmail is strictly read-only. You cannot send, modify, or delete emails.
- Contacts is strictly read-only. You cannot create, modify, or delete contacts.
- Drive, Calendar, Docs, and Sheets access depends on the configured mode. Check with `google-workspace config show`.
- Drive file creation/deletion is not supported. Drive write access is limited to comments.
- Docs and Sheets default to off. Enable them with `config set` before use.
- Setting `--drive=readwrite` requests the full `drive` OAuth scope, which grants broad access to all Drive files at the token level. Only enable this if the operator accepts that risk.

## Check configuration

Before using any commands, verify what is enabled:

```
google-workspace config show
```

## Gmail commands

Search messages:
```
google-workspace gmail search --query "from:someone@example.com" --max-results 10
```

Read a message by ID:
```
google-workspace gmail read --id MESSAGE_ID
```

List labels:
```
google-workspace gmail labels
```

Search or read threads:
```
google-workspace gmail threads --query "subject:meeting"
google-workspace gmail threads --id THREAD_ID
```

## Calendar commands

List available calendars:
```
google-workspace calendar list
```

List upcoming events:
```
google-workspace calendar events --from 2026-03-29T00:00:00Z --to 2026-04-05T23:59:59Z
```

Get a specific event:
```
google-workspace calendar event --id EVENT_ID
```

Create an event (only if calendar mode is readwrite):
```
google-workspace calendar create --summary "Team sync" --start "2026-04-01T10:00:00Z" --end "2026-04-01T11:00:00Z"
```

Update an event (only if calendar mode is readwrite):
```
google-workspace calendar update --id EVENT_ID --summary "Updated title"
```

Delete an event (only if calendar mode is readwrite):
```
google-workspace calendar delete --id EVENT_ID
```

## Contacts commands

List contacts:
```
google-workspace contacts list --max-results 50
```

Search contacts:
```
google-workspace contacts search --query "John"
```

Get a specific contact:
```
google-workspace contacts get --id "people/c1234567890"
```

## Drive commands

List files:
```
google-workspace drive list --max-results 20
```

Search files:
```
google-workspace drive list --query "name contains 'report'" --max-results 10
```

Get file metadata:
```
google-workspace drive get --id FILE_ID
```

Download file content (Google Docs export as plain text, Sheets as CSV):
```
google-workspace drive download --id FILE_ID
```

List comments on a file:
```
google-workspace drive comments list --file-id FILE_ID
```

Add a comment (requires readwrite mode):
```
google-workspace drive comment --file-id FILE_ID --content "Looks good, approved."
```

Reply to a comment (requires readwrite mode):
```
google-workspace drive comment reply --file-id FILE_ID --comment-id COMMENT_ID --content "Thanks!"
```

## Docs commands

Read a document:
```
google-workspace docs read --document-id DOC_ID
```

Insert text (requires readwrite mode):
```
google-workspace docs edit --document-id DOC_ID --insert-text "Hello" --index 1
```

Find and replace (requires readwrite mode):
```
google-workspace docs edit --document-id DOC_ID --find "old text" --replace-with "new text"
```

## Sheets commands

List sheets in a spreadsheet:
```
google-workspace sheets list --spreadsheet-id SPREADSHEET_ID
```

Read cell values:
```
google-workspace sheets read --spreadsheet-id SPREADSHEET_ID --range "Sheet1!A1:C10"
```

Write cell values (requires readwrite mode):
```
google-workspace sheets write --spreadsheet-id SPREADSHEET_ID --range "Sheet1!A1:B2" --values '[["Name","Score"],["Alice","95"]]'
```

## Authentication status

Check if the token is valid:
```
google-workspace auth status
```

If the token has expired, ask the operator to re-authenticate by running `google-workspace auth login` on the host.

If authentication fails with `Error 400: policy_enforced`, the operator's Google account likely has Advanced Protection enabled. They will need to temporarily unenroll, complete the OAuth flow, then re-enroll. The refresh token persists across sessions.

## Output format

All commands output JSON by default. Use `--output text` for plain text where supported.

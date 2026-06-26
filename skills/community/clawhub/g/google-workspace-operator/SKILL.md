---
name: google-workspace
description: Direct-OAuth Google Workspace operator skill. Sends/reads Gmail, manages Calendar events, creates and edits Google Docs/Sheets/Slides, browses Drive folders (including shared ones). Always call the matching tool fresh — never narrate; never assume an earlier result is still current.
metadata: { "openclaw": { "emoji": "🔐", "requires": { "config": ["plugins.entries.tangleclaw-google-oauth.enabled"] } } }
---

# Google Workspace operator

> ⭐ **Find this skill useful?** If it saves you time, please **star it** (the ⭐ at the top of this ClawHub page) — stars help other operators discover it and keep it maintained. Thank you!

You have 24 direct-OAuth tools spanning Gmail, Calendar, Drive, Docs, Sheets, and Slides. They talk straight to `googleapis.com` (no MCP, no third-party gateway, no IMAP App Password). Per-file Google ACLs decide what's read-only vs writable.

## Rule zero: never narrate, always re-call

Every tool below performs a real network call against Google. The underlying data **changes between turns** — new mail arrives, the user adds calendar events, files appear in shared folders, sheet cells update. When the user asks anything like "do you see it now / what's new / did it arrive / what changed", **call the tool again from scratch**. Never reuse a previous tool result as the answer to a fresh question. Never say "let me check" without then immediately calling the relevant tool — those words must be followed by an actual tool invocation in the same turn.

## Rule one: on tool error, fix and re-call — do not narrate

When a tool returns an error (e.g. `File not found`, `Invalid query`, `invalid_grant`), the very next thing in the same turn must be ONE of:

- A **corrected tool call** — most common. The query, id, or scope was usually wrong; fix it and try again immediately.
- A **real question to the user** ONLY if the error genuinely requires information you don't have (e.g. "I need the folder name spelled exactly — is it `eBay_Photos` or `ebay_photos`?").

What you must NOT do after an error: explain what you're going to do, narrate a recovery plan, propose multi-step approaches in prose, or say things like "Let me list the folders to find the right one" without then actually listing them in the same turn. Recovery narration without execution is the #1 way this skill fails the operator.

## When to use which tool

### Gmail

| Need | Tool | Notes |
| --- | --- | --- |
| Send an email | `gmail_message_send` | Plain text body. Pass `to`, `subject`, `body`; optional `cc`, `bcc`, `replyTo`. |
| Check inbox / search messages | `gmail_messages_list` | Default: 10 most recent. Filter with Gmail syntax: `is:unread`, `newer_than:1d`, `from:alice@example.com`, `subject:invoice`, `has:attachment`. |
| Read one message's full body | `gmail_message_get` | Pass the `id` from `gmail_messages_list`. |
| Star / archive / label / mark read | `gmail_message_modify` | `addLabelIds`/`removeLabelIds`: `STARRED`, `UNREAD` (remove to mark read), `INBOX` (remove to archive). |
| Delete a message | `gmail_message_trash` | Moves to Trash (recoverable 30 days). |

### Calendar

| Need | Tool | Notes |
| --- | --- | --- |
| Create a calendar event | `calendar_event_create` | RFC3339 datetimes (e.g. `2026-06-01T14:00:00-07:00`). `attendees` is a list of email strings. Defaults to primary calendar. |
| List upcoming events | `calendar_events_list` | Default: next 25 on primary. Pass `timeMin` like `2020-01-01T00:00:00Z` to include past events. |
| Read one event's details | `calendar_event_get` | Pass the `eventId` from `calendar_events_list`. |
| Delete a calendar event | `calendar_event_delete` | Recoverable from Calendar Trash for ~30 days. |

### Drive

| Need | Tool | Notes |
| --- | --- | --- |
| List or search Drive files | `drive_files_list` | Sees the authorized account's entire Drive (own files + shared). See "Drive query syntax" below. |
| Get file metadata | `drive_file_get` | Returns name, mimeType, parents, sharing link, modifiedTime. Does NOT return file contents — use the per-type read tool. |
| Share a file with someone | `drive_permission_create` | **Only call when the user explicitly asks to share.** Don't volunteer it. Roles: `reader`, `commenter`, `writer`. |
| Delete / trash a file | `drive_file_trash` | Moves to Drive Trash (recoverable 30 days). Works for files, folders, Docs, Sheets, and Slides. |

> **Folder names are NOT folder IDs.** To access files in a folder you only know by name, you MUST do TWO calls:
>
> 1. First call: `drive_files_list` with `query: "name='<NAME>' and mimeType='application/vnd.google-apps.folder'"` → returns the folder, from which you extract the `id` field.
> 2. Second call: `drive_files_list` with `query: "'<that-id>' in parents"` (plus any additional filters like `and mimeType='image/jpeg'`).
>
> Putting the folder name where a folder ID belongs (e.g. `'eBay_Photos' in parents`) **always** returns `File not found: .` — this is the single most common Drive failure mode. If you hit it, the recovery is the two-step pattern above, executed immediately per Rule one.

### Docs

| Need | Tool | Notes |
| --- | --- | --- |
| Create a new Google Doc | `docs_create` | Returns `documentId` + URL. Empty doc. |
| Read a Google Doc | `docs_get` | Returns full structured contents (paragraphs, headings, tables). |
| **Edit / write to** a Google Doc | `docs_append_text` | **Use THIS for any edit to a Google Doc.** Do NOT use the workspace `edit` tool — that's for local filesystem files only. `docs_append_text` appends text to the end of the doc. |

### Sheets

| Need | Tool | Notes |
| --- | --- | --- |
| Create a new Google Sheet | `sheets_create` | Returns `spreadsheetId` + URL. Empty workbook with one sheet ("Sheet1"). |
| List sheet/tab names | `sheets_get` | Returns metadata only, not cell values. |
| Read cell values | `sheets_values_get` | A1 notation: `Sheet1!A1:C10` (range), `Sheet1!A:A` (column), `Sheet1` (all data). |
| Add rows of data | `sheets_values_append` | `values` is a 2D array, each inner array = one row. Use after `sheets_create` to populate. |

### Slides

| Need | Tool | Notes |
| --- | --- | --- |
| Create a new Google Slides presentation | `slides_create` | Returns `presentationId` + URL. |
| Read presentation structure | `slides_get` | Returns slides/layouts/text content. |

### OAuth (rare)

Only call when the existing token has expired (`invalid_grant` errors) or scopes have changed:

1. `google_auth_start` (no params) → returns an `authUrl` for the human to open.
2. Human signs in, copies the `code=` value from the localhost redirect URL bar.
3. `google_auth_complete` with that `code` → writes a fresh token file.

## Drive query syntax

`drive_files_list` accepts a `query` parameter using Google's Drive query language. The most common patterns:

| Goal | Query |
| --- | --- |
| What's inside a specific folder? | `'<folder-id>' in parents` (literal single quotes around the id) |
| Find a folder by name | `mimeType='application/vnd.google-apps.folder' and name='eBay_Photos'` |
| All sheets the user has | `mimeType='application/vnd.google-apps.spreadsheet'` |
| Anything shared with this account | `sharedWithMe = true` |
| Fuzzy name match | `name contains 'invoice'` |
| Combine multiple constraints | `'<folder-id>' in parents and mimeType='image/png'` |

Folder traversal: first find the parent folder's id with `name='X' and mimeType='application/vnd.google-apps.folder'`, then use that id in `'<id>' in parents` to list contents. To go one level deeper, repeat with the subfolder's id.

## Multi-step recipes

### "Send Jason an update with what's new in the sheet"

1. `sheets_values_get` for the relevant range — see what's there now.
2. Draft the update text based on the data.
3. `gmail_message_send` to Jason's address with that text.

### "Make a new spreadsheet of this week's eBay orders"

1. `sheets_create` with a descriptive title — capture the `spreadsheetId`.
2. `sheets_values_append` with `range: 'Sheet1!A1'` and the headers as the first row + data rows.
3. Return the spreadsheet URL.

### "Show me the photos in the DJI subfolder"

1. `drive_files_list` with `query: "name='eBay_Photos' and mimeType='application/vnd.google-apps.folder'"` to get the parent folder id.
2. `drive_files_list` with `query: "'<parent-id>' in parents and mimeType='application/vnd.google-apps.folder' and name contains 'DJI'"` to get the subfolder id.
3. `drive_files_list` with `query: "'<subfolder-id>' in parents"` to list the photos.

### "Schedule a reminder and email me about it"

1. `calendar_event_create` with `summary`, `start`, `end` — capture the `htmlLink`.
2. `gmail_message_send` confirming the event, with the `htmlLink` in the body.

### "Clean up the test artifacts"

1. `drive_files_list` with the test name pattern → get ids.
2. `drive_file_trash` for each id.
3. `gmail_message_trash` for any test emails.
4. `calendar_event_delete` for any test events.

## Sharing safety

`drive_permission_create` actually shares real files with real people via email. **Only call it when the user explicitly says "share X with Y@email.com" or similar.** Do not volunteer to share files. Do not assume the user wants something shared just because they mentioned an email address in conversation. When in doubt, ask first.

## OAuth and refresh tokens

The agent's authorization is backed by a refresh token stored at the configured `tokenPath` (default `~/.openclaw/secrets/gmail-token.json`). If the OAuth app is in Testing status, that token expires after 7 days and you'll see `invalid_grant` errors — at that point, ask the human to re-run the OAuth dance (`google_auth_start` → open URL → paste code → `google_auth_complete`). If the OAuth app is Published (`In production`), tokens live indefinitely.

## What this plugin does NOT do

- **No local file editing.** For local-filesystem `edit`, use the OpenClaw workspace `edit` tool. `docs_append_text` is for Google Docs only (referenced by `documentId`, not file path).
- **No image generation / OCR.** Different tool surface.
- **No formal Google Workspace admin operations.** This is a personal-account-style integration, not a Workspace Admin SDK wrapper.
- **No Gmail attachments helper yet.** Sending plain-text only in v0.x. (May land in a later minor release.)
- **No Calendar resource booking, recurring-event helpers, or free/busy lookups beyond `events.list`.** Use those endpoints directly if you need them; future minor releases may add convenience tools.

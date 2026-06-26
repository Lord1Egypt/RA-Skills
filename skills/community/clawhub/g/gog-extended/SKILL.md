---
name: gog
description: "Extended Google Workspace CLI reference for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. Includes complete email body retrieval, attachments, and advanced query patterns. Use when working with Gmail to read full email content, extract attachments, search with advanced filters, or manage Google Workspace documents."
---

# gog-extended

Complete reference for the `gog` CLI with focus on advanced Gmail operations (full email bodies, attachments, complex searches).

## Setup (one-time)

```bash
gog auth credentials /path/to/client_secret.json
gog auth add you@gmail.com --services gmail,calendar,drive,contacts,docs,sheets
gog auth list
```

## Gmail Operations

### Search & Browse

- **Search threads** (one row per thread):
  ```bash
  gog gmail search 'newer_than:7d' --max 10
  gog gmail search 'from:sender@example.com' --max 20
  ```

- **Search individual messages** (ignores threading, returns all matches):
  ```bash
  gog gmail messages search "in:inbox from:ryanair.com" --max 20 --account you@example.com
  gog gmail messages search 'subject:invoice' --max 50
  ```

### Read Full Email Content (Critical for Automation)

**This is the key difference from basic search** — retrieve the complete email body, headers, and content:

```bash
# Full email with HTML body (recommended for parsing and automation)
gog gmail get <messageId> --format=full --account you@example.com

# Metadata only (faster, no body)
gog gmail get <messageId> --format=metadata --account you@example.com

# Raw RFC 2822 format (MIME encoded)
gog gmail get <messageId> --format=raw --account you@example.com
```

**Recommendation:** Use `--format=full` (default) which returns HTML-formatted email bodies. HTML preserves structure, links, and formatting better than raw RFC 2822, making it easier to parse and extract data programmatically.

**Example workflow** (extracting order details from email):
```bash
# 1. Find the message
gog gmail messages search 'from:order@example.com subject:confirmation' --max 1 --account you@example.com

# 2. Extract the message ID from results
# 3. Read full content (returns HTML body for easy parsing)
gog gmail get <messageId> --format=full --account you@example.com

# 4. Parse HTML for data (grep, sed, or HTML parser)
gog gmail get <messageId> --format=full --account you@example.com | grep -i "order\|price\|quantity"
```

The HTML format makes it easier to identify structure (tables, divs, links) and extract data without dealing with raw MIME encoding.

### Download Attachments

```bash
gog gmail attachment <messageId> <attachmentId>
```

Get attachment IDs from `gog gmail get <messageId> --format=full` output.

### Send Emails

- **Plain text**:
  ```bash
  gog gmail send --to a@b.com --subject "Hi" --body "Hello"
  ```

- **Multi-line (via file)**:
  ```bash
  gog gmail send --to a@b.com --subject "Hi" --body-file ./message.txt
  ```

- **Multi-line (via stdin)**:
  ```bash
  gog gmail send --to a@b.com --subject "Hi" --body-file - <<'EOF'
  Hi there,
  
  This is a test.
  
  Cheers
  EOF
  ```

- **HTML**:
  ```bash
  gog gmail send --to a@b.com --subject "Hi" --body-html "<p>Hello</p>"
  ```

### Drafts

```bash
gog gmail drafts create --to a@b.com --subject "Hi" --body-file ./message.txt
gog gmail drafts send <draftId>
```

### Reply to Messages

```bash
gog gmail send --to a@b.com --subject "Re: Hi" --body "Reply" --reply-to-message-id <msgId>
```

### Gmail History (Last Changes)

```bash
gog gmail history --max 100
```

### Gmail URL Links

```bash
gog gmail url <threadId> ...
```

Prints direct Gmail web URLs.

## Calendar Operations

### List Events

```bash
gog calendar events <calendarId> --from 2026-01-01T00:00:00Z --to 2026-12-31T23:59:59Z
```

### Create Event

```bash
gog calendar create <calendarId> --summary "Meeting" --from 2026-03-30T10:00:00Z --to 2026-03-30T11:00:00Z
```

With color (IDs 1–11):

```bash
gog calendar create <calendarId> --summary "Important" --from 2026-03-30T10:00:00Z --to 2026-03-30T11:00:00Z --event-color 4
```

### Update Event

```bash
gog calendar update <calendarId> <eventId> --summary "New Title" --event-color 7
```

### View Color Palette

```bash
gog calendar colors
```

**Color IDs:**
- 1: #a4bdfc (blue)
- 2: #7ae7bf (teal)
- 3: #dbadff (purple)
- 4: #ff887c (red)
- 5: #fbd75b (yellow)
- 6: #ffb878 (orange)
- 7: #46d6db (cyan)
- 8: #e1e1e1 (gray)
- 9: #5484ed (dark blue)
- 10: #51b749 (green)
- 11: #dc2127 (dark red)

## Drive Operations

```bash
gog drive search "filename:report.pdf" --max 10
gog drive search "in:starred" --max 20
```

## Contacts

```bash
gog contacts list --max 20
gog contacts list --max 50 --json
```

## Sheets

### Read Data

```bash
gog sheets get <sheetId> "Tab!A1:D10" --json
gog sheets metadata <sheetId> --json
```

### Update Data

```bash
gog sheets update <sheetId> "Tab!A1:B2" --values-json '[["A","B"],["1","2"]]' --input USER_ENTERED
```

### Append Data

```bash
gog sheets append <sheetId> "Tab!A:C" --values-json '[["x","y","z"]]' --insert INSERT_ROWS
```

### Clear Data

```bash
gog sheets clear <sheetId> "Tab!A2:Z"
```

## Docs

### Export

```bash
gog docs export <docId> --format txt --out /tmp/doc.txt
gog docs export <docId> --format pdf --out /tmp/doc.pdf
```

### Read (cat)

```bash
gog docs cat <docId>
```

## Advanced Flags

### Common Flags

- `--account you@gmail.com` — Target specific account (required when multiple accounts configured)
- `--json` — Output JSON (best for scripting)
- `--plain` — Stable TSV format (no colors)
- `--dry-run` — Preview changes without executing
- `--force` — Skip confirmations
- `--no-input` — Never prompt (useful for CI/automation)
- `--verbose` — Enable verbose logging

### Environment Variable

Avoid repeating `--account` by setting:

```bash
export GOG_ACCOUNT=you@gmail.com
```

Then:

```bash
gog gmail search 'newer_than:7d'  # Uses GOG_ACCOUNT automatically
```

## Gmail Query Syntax

Powerful search operators for `gog gmail search` and `gog gmail messages search`:

- `newer_than:7d` — Last 7 days
- `before:2026-03-30` — Before date
- `after:2026-03-20` — After date
- `from:sender@example.com` — From specific sender
- `to:recipient@example.com` — To specific recipient
- `subject:keywords` — Subject contains
- `in:inbox` — In inbox (also: `sent`, `draft`, `starred`, `important`)
- `is:unread` — Unread messages
- `has:attachment` — Has attachment
- `filename:document.pdf` — Attachment name
- `label:custom_label` — Custom labels

Complex queries:

```bash
gog gmail search 'from:billing@example.com subject:invoice after:2026-03-01'
gog gmail search 'in:inbox is:unread has:attachment'
```

## Notes

- **Search vs Messages**: `gog gmail search` returns one row per thread; use `gog gmail messages search` when you need every individual email.
- **Multi-account**: When multiple accounts are configured, always specify `--account email@domain.com`.
- **Token efficiency**: For scripting, use `--json` output and parse programmatically.
- **Email body extraction**: Use `gog gmail get <messageId> --format=full` to retrieve complete email content (critical for automation like order tracking, invoice extraction, etc.).
- **Docs are read-only in gog**: In-place edits require a separate Docs API client; gog supports export and read-only operations.

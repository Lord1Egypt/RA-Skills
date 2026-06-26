---
name: Mails for Agent
description: "Complete service registrations autonomously by receiving verification codes. Also: send and receive emails, monitor inbox, search by keyword, download attachments, view threads, filter by label, extract structured data, manage mailbox and webhooks."
version: 1.8.0
metadata:
  openclaw:
    requires:
      env:
        - MAILS_API_URL
        - MAILS_AUTH_TOKEN
        - MAILS_MAILBOX
      bins: []
      primaryEnv: MAILS_AUTH_TOKEN
---

# Email Skill — Agent Auth-Completion

You have the email address `$MAILS_MAILBOX`. Your primary superpower: **complete service registrations autonomously** by receiving verification codes via `GET /api/code?timeout=60`.

Make HTTP requests to `$MAILS_API_URL` with header `Authorization: Bearer $MAILS_AUTH_TOKEN`.

**Sign up for a service:** Fill form with `$MAILS_MAILBOX` → GET /api/code?timeout=60 → enter the code. Done.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/inbox | List/search emails. Params: `query`, `limit`, `offset`, `direction`, `label`, `mode` (keyword/semantic/hybrid) |
| GET | /api/email?id=ID | Full email with body, attachments, labels |
| GET | /api/code?timeout=60 | Wait for verification code (long-poll). Params: `timeout`, `since` |
| POST | /api/send | Send email. Body: `{ from, to[], cc[], bcc[], subject, text, html, reply_to, in_reply_to, headers, attachments }` |
| DELETE | /api/email?id=ID | Delete email and attachments |
| GET | /api/attachment?id=ID | Download attachment |
| GET | /api/threads | List conversation threads. Params: `limit`, `offset` |
| GET | /api/thread?id=ID | Get all emails in a thread |
| POST | /api/extract | Extract structured data. Body: `{ email_id, type }` type: order/shipping/calendar/receipt/code |
| GET | /api/stats | Mailbox statistics (total, inbound, outbound, this month) |
| GET | /api/events | SSE real-time event stream. Params: `types`, `since` |
| GET | /api/mailbox | Mailbox info (status, webhook_url) |
| PATCH | /api/mailbox | Update mailbox settings. Body: `{ webhook_url }` |
| PATCH | /api/mailbox/pause | Pause mailbox (blocks all operations) |
| PATCH | /api/mailbox/resume | Resume paused mailbox |
| GET | /api/mailbox/routes | List per-label webhook routes |
| PUT | /api/mailbox/routes | Upsert webhook route. Body: `{ label, webhook_url }` |
| DELETE | /api/mailbox/routes?label=X | Delete webhook route for label |
| GET | /api/me | Mailbox info and capabilities |
| GET | /health | Health check (no auth) |

## Request Format

All requests (except /health) require `Authorization: Bearer $MAILS_AUTH_TOKEN` header.

POST/PUT/PATCH requests require `Content-Type: application/json` header.

The `to` param is optional — the API auto-scopes to the token's mailbox.

## Response Shapes

**Inbox**: `{ "emails": [{ "id", "from_address", "from_name", "subject", "code", "direction", "status", "received_at", "has_attachments", "attachment_count" }], "search_mode": "keyword" }`

**Email detail**: Full email object with `body_text`, `body_html`, `headers`, `metadata`, `labels`, `thread_id`, `in_reply_to`, `references`, `attachments[]`

**Code**: `{ "id": "...", "code": "483920", "from": "...", "subject": "...", "received_at": "..." }` or `{ "code": null }`

**Send**: `{ "id": "...", "provider_id": "...", "thread_id": "..." }`

**Threads**: `{ "threads": [{ "thread_id", "latest_email_id", "subject", "from_address", "from_name", "received_at", "message_count", "has_attachments" }] }`

**Stats**: `{ "mailbox", "total_emails", "inbound", "outbound", "emails_this_month", "ingest": { "pending", "parsed", "failed" } }`

**Extract**: `{ "email_id": "...", "extraction": { "type": "order", "order_id": "...", ... } }`

**Events (SSE)**: `event: message.received\ndata: { "email_id", "mailbox", "from", "subject", ... }`

## Send Fields

| Field | Required | Description |
|-------|----------|-------------|
| from | Yes | Must be `$MAILS_MAILBOX` (enforced server-side) |
| to | Yes | Array of recipients (max 50) |
| subject | Yes | Max 998 characters |
| text | text or html | Plain text body |
| html | text or html | HTML body |
| cc | No | Array of CC recipients |
| bcc | No | Array of BCC recipients |
| reply_to | No | Reply-to address |
| in_reply_to | No | Message-ID of parent email (enables threading) |
| headers | No | Custom headers object |
| attachments | No | `[{ filename, content (base64), content_type?, content_id? }]` |

## Labels

Emails are auto-labeled on receive: `newsletter`, `notification`, `code`, `personal`. Filter with `?label=notification`.

## Common Flows

**Sign up for a service:** Fill form with `$MAILS_MAILBOX` → GET /api/code?timeout=60 → enter the code

**Process inbox:** GET /api/inbox → GET /api/email?id=ID → DELETE /api/email?id=ID

**Reply to an email:** GET /api/email?id=ID → POST /api/send with `in_reply_to` set to the email's `message_id`

**View threads:** GET /api/threads → GET /api/thread?id=THREAD_ID

**Monitor in real-time:** GET /api/events (SSE stream, reconnects automatically)

**Extract data:** POST /api/extract with `{"email_id":"ID","type":"order"}`

**Set up webhook routing:** PUT /api/mailbox/routes with `{"label":"code","webhook_url":"https://..."}`

## Constraints

- `from` must match `$MAILS_MAILBOX`
- Verification codes: 4-12 alphanumeric (EN/ZH/JA/KO)
- Code wait timeout max 55 seconds
- Send rate limit: 100 emails/day per mailbox
- Search uses FTS5 full-text search (keyword mode) or Vectorize (semantic mode)

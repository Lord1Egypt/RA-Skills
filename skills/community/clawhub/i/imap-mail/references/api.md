# API Reference

Base URL: `http://127.0.0.1:8025` (configurable via `IMAP_MAIL_PORT`)

## GET /health
Returns server status, IDLE watcher state, and VIP sender list.
```json
{
  "status": "ok",
  "inbox": "agent@example.com",
  "imap_host": "mail.example.com",
  "idle_active": true,
  "vip_senders": ["boss@company.com"]
}
```

---

## GET /idle/status
Returns IMAP IDLE watcher status.
```json
{
  "running": true,
  "last_event": "2026-03-07T10:30:00+00:00",
  "error": null,
  "webhook": "http://127.0.0.1:8080/mail-event",
  "folder": "INBOX",
  "vip_senders": ["boss@company.com"]
}
```

---

## Folders

### GET /inboxes/{inbox}/folders
List all IMAP folders.
```json
{"folders": [{"name": "INBOX", "flags": ["HasNoChildren"], "delimiter": "/"}]}
```

### POST /inboxes/{inbox}/folders
Create a folder. Body: `{"name": "Archive"}`

### DELETE /inboxes/{inbox}/folders/{folder_name}
Delete a folder.

---

## Messages

### GET /inboxes/{inbox}/messages
List messages, newest first.

**Query params:**
- `folder` (default: `INBOX`)
- `limit` (int, max 100, default 20)
- `unseen` (bool) — unread only

### GET /inboxes/{inbox}/messages/{uid}
Get a single message by IMAP UID.

**Query params:** `folder` (default: `INBOX`)

Messages include a `"vip": true/false` field based on `MAIL_VIP_SENDERS`.

### GET /inboxes/{inbox}/messages/{uid}/attachments/{index}
Download a specific attachment by zero-based index.

**Query params:** `folder` (default: `INBOX`)

```json
{
  "filename": "report.pdf",
  "content_type": "application/pdf",
  "data": "<base64-encoded content>",
  "size": 102400
}
```

### POST /inboxes/{inbox}/messages
Send an email.
```json
{
  "to": ["recipient@example.com"],
  "subject": "Hello",
  "text": "Plain text body",
  "html": "",
  "in_reply_to": "<original-msg-id>",
  "references": "<original-msg-id>"
}
```
Response (201): `{"message_id": "<new-msg-id>", "status": "sent"}`

### POST /inboxes/{inbox}/messages/{uid}/move
Move message to another folder.

**Query params:** `folder` (source folder, default: `INBOX`)

Body: `{"destination": "Archive"}`

### DELETE /inboxes/{inbox}/messages/{uid}
Delete (expunge) a message.

**Query params:** `folder` (default: `INBOX`)

---

## Scheduled Messages

### POST /inboxes/{inbox}/scheduled
Queue an email for future delivery. The scheduler checks every 60 seconds.

```json
{
  "to": ["recipient@example.com"],
  "subject": "Good morning",
  "text": "This was scheduled.",
  "send_at": "2026-03-10T09:00:00Z"
}
```
Response (201): `{"id": 1, "send_at": "2026-03-10T09:00:00Z", "status": "scheduled"}`

### GET /inboxes/{inbox}/scheduled
List all scheduled messages (pending, sent, and failed) for this inbox.

```json
{
  "scheduled": [
    {"id": 1, "to": ["user@example.com"], "subject": "Hello", "send_at": "...", "sent": false, "error": null}
  ],
  "total": 1
}
```

### DELETE /inboxes/{inbox}/scheduled/{id}
Cancel a pending scheduled message. Returns 409 if already sent.

---

## Search

### GET /inboxes/{inbox}/search
Search messages using IMAP SEARCH criteria.

**Query params:**
- `folder` (default: `INBOX`)
- `q` — search subject + body (convenience shorthand)
- `from` — filter by sender address
- `to` — filter by recipient address
- `subject` — filter by subject text
- `body` — filter by body text
- `since` — ISO date `2026-01-01` (messages after)
- `before` — ISO date `2026-12-31` (messages before)
- `unseen` — unread only (bool)
- `seen` — read only (bool)
- `has_attachments` — only messages with attachments (post-filter)
- `vip_only` — only messages from VIP senders (post-filter)
- `limit` (int, max 100, default 20)

```json
{
  "messages": [...],
  "total": 3,
  "folder": "INBOX",
  "criteria": "SUBJECT \"invoice\" SINCE 01-Jan-2026"
}
```

---

## Threads

### GET /inboxes/{inbox}/threads
Group messages into threads by `In-Reply-To` / `References`.

**Query params:** `folder`, `limit`

# OpenMail API Reference

Base URL: `https://api.openmail.sh/v1`

All requests require:
```
Authorization: Bearer $OPENMAIL_API_KEY
```

---

## Inboxes

### List inboxes
```
GET /inboxes
```

### Create inbox
```
POST /inboxes
```
```json
{
  "mailboxName": "support",
  "displayName": "Support Inbox"
}
```

Both fields are optional. `mailboxName` sets the local part of the address
(e.g. `support` → `support@yourdomain.sh`), 3–30 chars, defaults to random.
`displayName` sets the sender name in the From header, max 200 chars.

Returns 201 with `id`, `address`, `displayName`, `createdAt`. Live immediately.
Limit: 100 inbox creations per day.

### Get inbox
```
GET /inboxes/{id}
```

### Delete inbox
```
DELETE /inboxes/{id}
```

---

## Messages

### Send email
```
POST /inboxes/{id}/send
```

Required headers:
- `Content-Type: application/json`
- `Idempotency-Key: <uuid>` — required, prevents duplicate sends

Body:
```json
{
  "to": "recipient@example.com",
  "subject": "Subject line",
  "body": "Plain text body.",
  "bodyHtml": "<p>Optional HTML body.</p>",
  "threadId": "..."
}
```

`threadId` is optional. Include it to reply in an existing thread — `subject`
is ignored when replying.

Returns:
```json
{
  "messageId": "...",
  "threadId": "...",
  "providerMessageId": "...",
  "status": "pending"
}
```

Rate limits: 10 sends/min, 200 sends/day per inbox.

### List messages
```
GET /inboxes/{id}/messages
```

Query parameters:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `direction` | `inbound` \| `outbound` | — | Filter by direction |
| `limit` | integer | 50 | Max results (max 100) |
| `offset` | integer | 0 | Pagination offset |

No `since` parameter — filter by `createdAt` client-side after fetching.
Messages are returned newest first.

Response:
```json
{
  "data": [
    {
      "id": "...",
      "threadId": "...",
      "direction": "inbound",
      "fromAddr": "sender@example.com",
      "toAddr": "agent@yourdomain.sh",
      "subject": "Re: Your request",
      "bodyText": "Plain text body.",
      "bodyHtml": "<p>HTML body.</p>",
      "attachments": [
        {
          "filename": "document.pdf",
          "contentType": "application/pdf",
          "sizeBytes": 42819,
          "url": "https://..."
        }
      ],
      "status": "pending",
      "createdAt": "2026-03-20T14:32:00Z"
    }
  ],
  "total": 42
}
```

---

## Threads

### List threads
```
GET /inboxes/{id}/threads
```

Query parameters:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `is_read` | `true` \| `false` | — | Filter by read status. `false` = unread only. |
| `limit` | integer | 50 | Max results (max 100) |
| `offset` | integer | 0 | Pagination offset |

Response:
```json
{
  "data": [
    {
      "id": "...",
      "subject": "Re: Your request",
      "isRead": false,
      "lastMessageAt": "2026-03-20T14:32:00Z",
      "createdAt": "2026-03-20T12:00:00Z",
      "messageCount": 3
    }
  ],
  "total": 12
}
```

### Update thread
```
PATCH /threads/{id}
```

Body:
```json
{
  "is_read": true
}
```

Mark a thread as read or unread. New inbound threads start as unread
(`isRead: false`). Sending a reply auto-marks the thread as read.

Returns `{ "ok": true }`.

### Get thread messages
```
GET /threads/{id}/messages
```

Returns `threadId`, `subject`, `isRead`, and a `data` array of messages sorted
oldest-first. Same message schema as list messages.

---

## Attachments

```
GET /attachments/{messageId}/{filename}
```

Returns a 302 redirect to a signed URL. Use `-L` to follow the redirect:

```bash
curl -s -L \
  "https://api.openmail.sh/v1/attachments/$MESSAGE_ID/$FILENAME" \
  -H "Authorization: Bearer $OPENMAIL_API_KEY" \
  -o "$FILENAME"
```

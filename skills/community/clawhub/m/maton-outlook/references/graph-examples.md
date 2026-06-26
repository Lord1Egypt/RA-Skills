# Outlook Graph / Maton examples

## Base

Use:

https://gateway.maton.ai/outlook/v1.0/

All requests require:

Authorization: Bearer $MATON_API_KEY

---

## Read-only queries

### Profile

GET /me

### Recent messages

GET /me/messages?$top=5&$select=subject,receivedDateTime,from,isRead,webLink

### Inbox messages

GET /me/mailFolders/Inbox/messages?$top=10&$select=subject,receivedDateTime,from,isRead,webLink

### Unread messages

GET /me/messages?$top=10&$filter=isRead eq false&$select=subject,receivedDateTime,from,isRead,webLink

### One message with preview

GET /me/messages/{message-id}?$select=subject,from,toRecipients,receivedDateTime,bodyPreview,isRead,webLink

### One message with full body

GET /me/messages/{message-id}?$select=subject,from,toRecipients,ccRecipients,receivedDateTime,body,bodyPreview,isRead,webLink

### Search examples

Search by sender:

GET /me/messages?$search="from:github.com"

Search by subject keyword:

GET /me/messages?$search="subject:invoice"

Search by text keyword:

GET /me/messages?$search="password"

If `$search` is unsupported in a given route, fall back to a smaller recent-message pull and filter client-side.

---

## Write payload templates

Only use after explicit user confirmation.

### Draft a message

POST /me/messages

{
  "subject": "Subject here",
  "body": {
    "contentType": "Text",
    "content": "Body here"
  },
  "toRecipients": [
    {
      "emailAddress": {
        "address": "user@example.com"
      }
    }
  ]
}

### Send a message directly

POST /me/sendMail

{
  "message": {
    "subject": "Subject here",
    "body": {
      "contentType": "Text",
      "content": "Body here"
    },
    "toRecipients": [
      {
        "emailAddress": {
          "address": "user@example.com"
        }
      }
    ]
  },
  "saveToSentItems": true
}

### Mark read

PATCH /me/messages/{message-id}

{
  "isRead": true
}

### Mark unread

PATCH /me/messages/{message-id}

{
  "isRead": false
}

### Move message

POST /me/messages/{message-id}/move

{
  "destinationId": "Archive"
}

### Delete message

DELETE /me/messages/{message-id}

---

## Folder helpers

### List folders

GET /me/mailFolders?$top=50

### Archive folder messages

GET /me/mailFolders/Archive/messages?$top=10&$select=subject,receivedDateTime,from,isRead,webLink

### Sent items

GET /me/mailFolders/SentItems/messages?$top=10&$select=subject,receivedDateTime,toRecipients,webLink

---

## Practical patterns

### Quick inbox triage

1. GET recent or unread messages with small `$top`
2. Summarize sender + subject + time
3. Open only selected message ids
4. Ask before write actions

### Reply workflow

1. Read the target message first
2. Draft the reply body in chat
3. Confirm recipient + subject + body
4. Send only after confirmation

### Investigate one sender

1. Pull recent messages
2. Filter by sender address
3. Open only relevant message ids

---

## Notes

- Prefer `bodyPreview` before `body` when possible.
- Keep requests narrow with `$top` and `$select`.
- Use `webLink` when the user may want to open the message in Outlook Web.
- If a path without `/v1.0/` fails, use the explicit `/outlook/v1.0/...` form.

---
name: outlook
description: |
  Outlook / Microsoft mail integration via Maton managed OAuth and Microsoft Graph-compatible gateway. Use when users want to read, search, summarize, draft, send, label, move, or manage Outlook / Hotmail / Live / Microsoft 365 email through an existing Maton Outlook connection. Requires MATON_API_KEY and a Maton connection with app="outlook".
---

# Outlook

Access Outlook mail through Maton using an existing OAuth connection.

## Authentication

All requests require:

Authorization: Bearer $MATON_API_KEY

Environment variable required:

MATON_API_KEY

## Connection check

First verify that an active Outlook connection exists.

Control endpoint:

https://ctrl.maton.ai/connections

Look for a connection with:
- app: `outlook`
- status: `ACTIVE`

If multiple Outlook connections exist, prefer the ACTIVE one whose metadata mail/userPrincipalName matches the user’s target mailbox.

## Base path

Use the Maton Outlook gateway with Microsoft Graph v1.0 style paths:

https://gateway.maton.ai/outlook/v1.0/

Examples:
- `https://gateway.maton.ai/outlook/v1.0/me`
- `https://gateway.maton.ai/outlook/v1.0/me/messages?$top=5`
- `https://gateway.maton.ai/outlook/v1.0/me/mailFolders/Inbox/messages?$top=10`

## Preferred workflow

Prefer this order:
1. Verify Outlook connection is ACTIVE
2. Run a read-only probe on `/outlook/v1.0/me`
3. List recent or unread messages with a small `$top`
4. Read message body only when needed
5. Summarize before taking action when the inbox is noisy
6. Ask for confirmation before any write action

## Fast paths for common tasks

### Check recent mail

Use:

GET https://gateway.maton.ai/outlook/v1.0/me/messages?$top=5&$select=subject,receivedDateTime,from,isRead,webLink

### Check unread mail

Use:

GET https://gateway.maton.ai/outlook/v1.0/me/messages?$top=10&$filter=isRead eq false&$select=subject,receivedDateTime,from,isRead,webLink

### Check inbox folder specifically

Use:

GET https://gateway.maton.ai/outlook/v1.0/me/mailFolders/Inbox/messages?$top=10&$select=subject,receivedDateTime,from,isRead,webLink

### Search messages

Use Graph-style `$search` when supported, for example:

GET https://gateway.maton.ai/outlook/v1.0/me/messages?$search="from:github.com"

If `$search` is not supported by the gateway, fall back to a smaller recent messages pull and filter in the client.

### Read one message

Use:

GET https://gateway.maton.ai/outlook/v1.0/me/messages/{message-id}?$select=subject,from,toRecipients,ccRecipients,receivedDateTime,body,bodyPreview,isRead,webLink

Prefer `bodyPreview` first when the user only needs a quick triage.

## Read-only examples

### Profile

GET
https://gateway.maton.ai/outlook/v1.0/me

### Recent messages

GET
https://gateway.maton.ai/outlook/v1.0/me/messages?$top=5&$select=subject,receivedDateTime,from,isRead,webLink

### Unread messages

GET
https://gateway.maton.ai/outlook/v1.0/me/messages?$top=10&$filter=isRead eq false&$select=subject,receivedDateTime,from,isRead,webLink

## Drafting and sending

Treat drafting and sending as sensitive.

### Draft message

POST
https://gateway.maton.ai/outlook/v1.0/me/messages

Typical payload shape:

{
  "subject": "...",
  "body": {
    "contentType": "Text",
    "content": "..."
  },
  "toRecipients": [
    {
      "emailAddress": {
        "address": "user@example.com"
      }
    }
  ]
}

### Send mail directly

POST
https://gateway.maton.ai/outlook/v1.0/me/sendMail

Typical payload shape:

{
  "message": {
    "subject": "...",
    "body": {
      "contentType": "Text",
      "content": "..."
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

Prefer drafting or showing the final message preview before send unless the user explicitly asks for immediate sending.

## Common write operations

Only do these after explicit user confirmation.

### Patch a message

PATCH
https://gateway.maton.ai/outlook/v1.0/me/messages/{message-id}

### Move a message

POST
https://gateway.maton.ai/outlook/v1.0/me/messages/{message-id}/move

### Delete a message

DELETE
https://gateway.maton.ai/outlook/v1.0/me/messages/{message-id}

### Mark read / unread

PATCH
https://gateway.maton.ai/outlook/v1.0/me/messages/{message-id}

Use payloads like:

{ "isRead": true }

or

{ "isRead": false }

## Practical handling guidance

- For inbox triage, start with subject, sender, received time, isRead, and webLink.
- Avoid pulling full bodies for many messages at once unless the user explicitly wants a deep summary.
- For summaries, first list candidate emails, then read only the few that matter.
- When replying or sending, confirm recipients, subject, and final body before write actions.
- Keep read-only checks small and incremental to reduce noise and risk.

## Scripts

For repeated operations, prefer the bundled helper scripts:

- `scripts/outlook_mail.py` for read-only tasks
- `scripts/outlook_send.py` for drafting and sending

### `scripts/outlook_mail.py`

Use it for:
- mailbox profile
- recent messages
- unread messages
- inbox messages
- reading one message
- search

Examples:
- `python skills/outlook/scripts/outlook_mail.py profile`
- `python skills/outlook/scripts/outlook_mail.py recent --top 5`
- `python skills/outlook/scripts/outlook_mail.py unread --top 10`
- `python skills/outlook/scripts/outlook_mail.py get <message-id>`
- `python skills/outlook/scripts/outlook_mail.py get <message-id> --full`
- `python skills/outlook/scripts/outlook_mail.py search "from:github.com" --top 10`

### `scripts/outlook_send.py`

Use it for:
- creating drafts
- sending mail after explicit confirmation

Examples:
- `python skills/outlook/scripts/outlook_send.py draft --to user@example.com --subject "Hello" --body "Draft body"`
- `python skills/outlook/scripts/outlook_send.py send --to user@example.com --subject "Hello" --body "Mail body"`

Only use `send` after explicit user confirmation.

Prefer the scripts when the same request pattern would otherwise be rewritten in ad-hoc code.

## References

For more reusable query and payload examples, read:

- `references/graph-examples.md`

Use that file when you need ready-made Outlook Graph / Maton request patterns for inbox triage, message reads, folder access, drafting, sending, moving, or marking messages.

## Notes

- The gateway is Microsoft Graph-style, so fields and paths follow Graph conventions.
- Start with small read-only requests to verify access before doing broader queries.
- Treat send, delete, move, mark-read, and other state-changing actions as sensitive.
- If a request returns 401 or 403, re-check MATON_API_KEY and the Outlook connection status.
- If a request returns 400 on a path without `/v1.0/`, prefer the explicit `outlook/v1.0/...` path.

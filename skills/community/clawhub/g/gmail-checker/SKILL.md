---
name: gmail
description: "Send, read, search, and manage Gmail emails via the Gmail REST API. Use when asked to send an email, check inbox, read messages, search mail, reply to emails, draft emails, or manage labels. Triggers on phrases like 'send an email', 'check my email', 'reply to', 'draft a message', 'search my inbox', 'read my latest emails', 'send a gmail'."
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "requires": { "bins": ["curl", "jq"], "env": ["GMAIL_ACCESS_TOKEN"] },
      },
  }
---

# Gmail Skill

Send, read, search, reply, and manage Gmail directly from OpenClaw.

## Setup

### Option 1: OAuth2 Access Token (recommended)

1. Create OAuth2 credentials at https://console.cloud.google.com/apis/credentials
2. Enable the Gmail API at https://console.cloud.google.com/apis/library/gmail.googleapis.com
3. Obtain an access token via OAuth2 flow with scopes:
   - `https://www.googleapis.com/auth/gmail.send`
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/gmail.modify`
4. Set the environment variable:
   ```bash
   export GMAIL_ACCESS_TOKEN="your-access-token"
   ```

### Option 2: Refresh Token (long-lived)

If you have a refresh token, set these additional variables:

```bash
export GMAIL_CLIENT_ID="your-client-id"
export GMAIL_CLIENT_SECRET="your-client-secret"
export GMAIL_REFRESH_TOKEN="your-refresh-token"
```

All API calls use Bearer auth:

```bash
curl -s -H "Authorization: Bearer $GMAIL_ACCESS_TOKEN" \
  "https://gmail.googleapis.com/gmail/v1/users/me/..."
```

### Token Refresh

If `GMAIL_REFRESH_TOKEN` is set, refresh the access token before any API call:

```bash
GMAIL_ACCESS_TOKEN=$(curl -s -X POST "https://oauth2.googleapis.com/token" \
  -d "client_id=$GMAIL_CLIENT_ID" \
  -d "client_secret=$GMAIL_CLIENT_SECRET" \
  -d "refresh_token=$GMAIL_REFRESH_TOKEN" \
  -d "grant_type=refresh_token" | jq -r '.access_token')
```

---

## Commands

### Send an Email

Parse the user's request for:

| Field | Required | Description |
|-------|----------|-------------|
| to | yes | Recipient email address(es), comma-separated |
| subject | yes | Email subject line |
| body | yes | Email body (plain text or HTML) |
| cc | no | CC recipients |
| bcc | no | BCC recipients |
| attachments | no | File paths to attach |
| research | no | Topic to web-search for enriching the email body |

#### Web Research (if applicable)

If the user wants research-informed content:

1. Use `web_search` to find relevant information.
2. Fetch key pages with `xurl` or `curl` for details.
3. Incorporate findings into the email body naturally.

#### Compose and Send

Build a raw RFC 2822 message and base64url-encode it:

```bash
# Build raw message
RAW_MESSAGE=$(cat <<'MSGEOF'
From: me
To: recipient@example.com
Subject: Email subject
Content-Type: text/html; charset="UTF-8"
MIME-Version: 1.0

<html><body>
<p>Email body here.</p>
</body></html>
MSGEOF
)

# Base64url encode (no padding, URL-safe)
ENCODED=$(echo -n "$RAW_MESSAGE" | base64 -w 0 | tr '+/' '-_' | tr -d '=')

# Send
curl -s -X POST \
  -H "Authorization: Bearer $GMAIL_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://gmail.googleapis.com/gmail/v1/users/me/messages/send" \
  -d "{\"raw\": \"$ENCODED\"}"
```

Extract the message ID from the response and report success.

---

### Read / Check Inbox

List recent messages:

```bash
# List latest messages (default 10)
curl -s -H "Authorization: Bearer $GMAIL_ACCESS_TOKEN" \
  "https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=10&labelIds=INBOX"
```

For each message, fetch full details:

```bash
curl -s -H "Authorization: Bearer $GMAIL_ACCESS_TOKEN" \
  "https://gmail.googleapis.com/gmail/v1/users/me/messages/{MESSAGE_ID}?format=full"
```

Extract and display:
- **From**: sender
- **Subject**: subject line
- **Date**: when received
- **Snippet**: preview text
- **Body**: decoded from base64 (plain text part preferred)

Decode the body:

```bash
# Extract plain text body from payload parts
BODY=$(echo "$RESPONSE" | jq -r '
  .payload.parts[]? |
  select(.mimeType == "text/plain") |
  .body.data' | base64 -d 2>/dev/null)

# Fallback: single-part message
if [ -z "$BODY" ]; then
  BODY=$(echo "$RESPONSE" | jq -r '.payload.body.data' | base64 -d 2>/dev/null)
fi
```

---

### Search Emails

```bash
# Search with Gmail query syntax
curl -s -H "Authorization: Bearer $GMAIL_ACCESS_TOKEN" \
  "https://gmail.googleapis.com/gmail/v1/users/me/messages?q=QUERY&maxResults=10"
```

Gmail query examples:
- `from:user@example.com` — from a specific sender
- `subject:invoice` — subject contains "invoice"
- `is:unread` — unread messages
- `after:2026/01/01 before:2026/03/01` — date range
- `has:attachment filename:pdf` — PDFs attached
- `label:important` — labeled important

Fetch and display matching messages using the same read flow above.

---

### Reply to an Email

1. Fetch the original message to get `threadId`, `Message-ID` header, and sender.
2. Build the reply with proper headers:

```bash
RAW_REPLY=$(cat <<'MSGEOF'
From: me
To: original-sender@example.com
Subject: Re: Original subject
In-Reply-To: <original-message-id@mail.gmail.com>
References: <original-message-id@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"
MIME-Version: 1.0

Reply body here.
MSGEOF
)

ENCODED=$(echo -n "$RAW_REPLY" | base64 -w 0 | tr '+/' '-_' | tr -d '=')

curl -s -X POST \
  -H "Authorization: Bearer $GMAIL_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://gmail.googleapis.com/gmail/v1/users/me/messages/send" \
  -d "{\"raw\": \"$ENCODED\", \"threadId\": \"THREAD_ID\"}"
```

---

### Draft an Email

Create a draft without sending:

```bash
ENCODED=$(echo -n "$RAW_MESSAGE" | base64 -w 0 | tr '+/' '-_' | tr -d '=')

curl -s -X POST \
  -H "Authorization: Bearer $GMAIL_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://gmail.googleapis.com/gmail/v1/users/me/drafts" \
  -d "{\"message\": {\"raw\": \"$ENCODED\"}}"
```

Report the draft ID so the user can review it in Gmail before sending.

---

### Manage Labels

```bash
# List all labels
curl -s -H "Authorization: Bearer $GMAIL_ACCESS_TOKEN" \
  "https://gmail.googleapis.com/gmail/v1/users/me/labels" | jq '.labels[] | {name, id}'

# Add label to a message
curl -s -X POST \
  -H "Authorization: Bearer $GMAIL_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://gmail.googleapis.com/gmail/v1/users/me/messages/{MESSAGE_ID}/modify" \
  -d '{"addLabelIds": ["LABEL_ID"]}'

# Remove label
curl -s -X POST \
  -H "Authorization: Bearer $GMAIL_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://gmail.googleapis.com/gmail/v1/users/me/messages/{MESSAGE_ID}/modify" \
  -d '{"removeLabelIds": ["LABEL_ID"]}'

# Mark as read
curl -s -X POST \
  -H "Authorization: Bearer $GMAIL_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://gmail.googleapis.com/gmail/v1/users/me/messages/{MESSAGE_ID}/modify" \
  -d '{"removeLabelIds": ["UNREAD"]}'
```

---

## Network Policy

To use this skill inside NemoClaw's sandbox, add a Gmail network policy preset. Create or add to your sandbox policy:

```yaml
network_policies:
  google_gmail:
    name: google_gmail
    endpoints:
      - host: gmail.googleapis.com
        port: 443
        protocol: rest
        enforcement: enforce
        tls: terminate
        rules:
          - allow: { method: GET, path: "/**" }
          - allow: { method: POST, path: "/**" }
      - host: oauth2.googleapis.com
        port: 443
        protocol: rest
        enforcement: enforce
        tls: terminate
        rules:
          - allow: { method: POST, path: "/token" }
      - host: accounts.google.com
        port: 443
        protocol: rest
        enforcement: enforce
        tls: terminate
        rules:
          - allow: { method: GET, path: "/**" }
          - allow: { method: POST, path: "/**" }
```

---

## Notes

- Gmail API rate limit: 250 quota units per second per user.
- Sending has a daily limit of 2,000 messages for Google Workspace, 500 for free Gmail.
- Access tokens expire after ~1 hour. Use refresh token flow for long-running sessions.
- Attachments require multipart MIME encoding — for large files, use the resumable upload endpoint.

## Examples

```
# Send a simple email
/gmail send to:team@company.com subject:"Standup notes" body:"Here are today's updates..."

# Check inbox
/gmail inbox

# Search for unread emails from a specific sender
/gmail search "from:boss@company.com is:unread"

# Reply to the latest email
/gmail reply latest "Thanks, I'll look into this."

# Draft an email with web research
/gmail draft to:eng@company.com subject:"Redis 8 migration plan" --search "Redis 8 breaking changes"

# Mark all unread as read
/gmail read-all
```

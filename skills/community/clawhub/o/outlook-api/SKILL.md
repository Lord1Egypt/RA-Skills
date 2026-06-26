---
name: outlook
description: |
  Microsoft Outlook API integration with managed OAuth. Read, send, and manage emails, folders, calendar events, and contacts via Microsoft Graph. Use this skill when users want to interact with Outlook. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Outlook

Access the Microsoft Outlook API (via Microsoft Graph) with managed OAuth authentication. Read, send, and manage emails, folders, calendar events, and contacts.

## Quick Start

**CLI:**

```bash
maton outlook message list --folder Inbox --top 25
```

```bash
maton api '/outlook/v1.0/me/messages?$top=25'
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/outlook/v1.0/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/outlook/{native-api-path}
```

Maton proxies requests to `graph.microsoft.com` and automatically injects your OAuth token.

## Installation

**NPM:**
```bash
npm install -g @maton-ai/cli
```

**Homebrew:**
```bash
brew install maton-ai/cli/maton
```

## Authentication

**CLI:**

```bash
maton login                          # Opens browser for API key
maton login --interactive            # Skip browser, paste API key directly
maton whoami                         # Show current auth state
```

**Manual:**

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key
4. Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

## Connection Management

Manage your Microsoft OAuth connections at `https://api.maton.ai`.

### List Connections

**CLI:**

```bash
maton connection list outlook --status ACTIVE
```

```bash
maton api -X GET /connections -f app=outlook -f status=ACTIVE
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=outlook&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

**CLI:**

```bash
maton connection create outlook
```

```bash
maton api /connections -f app=outlook
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'outlook'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

**CLI:**

```bash
maton connection view {connection_id}
```

```bash
maton api /connections/{connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "outlook",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

**CLI:**

```bash
maton connection delete {connection_id}
```

```bash
maton api -X DELETE /connections/{connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Outlook connections, specify which one to use:

**CLI:**

```bash
maton outlook message list --folder Inbox --connection {connection_id}
```

```bash
maton api /outlook/v1.0/me/messages --connection {connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/outlook/v1.0/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always specify the connection to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to messages, mail folders, calendar events, and contacts within the connected Outlook account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.

## API Reference

### User Profile

```bash
GET /outlook/v1.0/me
```

Example:

```bash
maton outlook whoami
```

### Mail Folders

#### List Mail Folders

```bash
GET /outlook/v1.0/me/mailFolders
```

Example:

```bash
maton outlook folder list
```

#### Get Mail Folder

```bash
GET /outlook/v1.0/me/mailFolders/{folderId}
```

Well-known folder names: `Inbox`, `Drafts`, `SentItems`, `DeletedItems`, `Archive`, `JunkEmail`

Example:

```bash
maton outlook folder view {folderId}
```

#### Create Mail Folder

```bash
POST /outlook/v1.0/me/mailFolders
Content-Type: application/json

{
  "displayName": "My Folder"
}
```

Example:

```bash
maton outlook folder create --name "My Folder"
```

#### Delete Mail Folder

```bash
DELETE /outlook/v1.0/me/mailFolders/{folderId}
```

Example:

```bash
maton outlook folder delete {folderId}
```

#### List Child Folders

```bash
GET /outlook/v1.0/me/mailFolders/{folderId}/childFolders
```

Example:

```bash
maton outlook folder list --parent {folderId}
```

### Messages

#### List Messages

```bash
GET /outlook/v1.0/me/messages
```

Example:

```bash
maton outlook message list
```

From specific folder:

```bash
GET /outlook/v1.0/me/mailFolders/Inbox/messages
```

Example:

```bash
maton outlook message list --folder Inbox
```

With query filter:

```bash
GET /outlook/v1.0/me/messages?$filter=isRead eq false&$top=10
```

Example:

```bash
maton outlook message list --filter "isRead eq false" --top 10
```

#### Get Message

```bash
GET /outlook/v1.0/me/messages/{messageId}
```

Example:

```bash
maton outlook message view {messageId}
```

#### Create Draft

```bash
POST /outlook/v1.0/me/messages
Content-Type: application/json

{
  "subject": "Hello",
  "body": {
    "contentType": "Text",
    "content": "This is the email body."
  },
  "toRecipients": [
    {
      "emailAddress": {
        "address": "recipient@example.com"
      }
    }
  ]
}
```

Example:

```bash
maton outlook message draft --to recipient@example.com --subject "Hello" --body "This is the email body."
```

#### Send Message

```bash
POST /outlook/v1.0/me/sendMail
Content-Type: application/json

{
  "message": {
    "subject": "Hello",
    "body": {
      "contentType": "Text",
      "content": "This is the email body."
    },
    "toRecipients": [
      {
        "emailAddress": {
          "address": "recipient@example.com"
        }
      }
    ]
  },
  "saveToSentItems": true
}
```

Example:

```bash
maton outlook message send --to recipient@example.com --subject "Hello" --body "This is the email body."
```

#### Send Existing Draft

```bash
POST /outlook/v1.0/me/messages/{messageId}/send
```

Example:

```bash
maton outlook message send {messageId}
```

#### Update Message

```bash
PATCH /outlook/v1.0/me/messages/{messageId}
Content-Type: application/json

{
  "isRead": true
}
```

Example:

```bash
maton outlook message update {messageId} --read
```

#### Delete Message

```bash
DELETE /outlook/v1.0/me/messages/{messageId}
```

Example:

```bash
maton outlook message delete {messageId}
```

#### Move Message

```bash
POST /outlook/v1.0/me/messages/{messageId}/move
Content-Type: application/json

{
  "destinationId": "{folderId}"
}
```

Example:

```bash
maton outlook message move {messageId} --to {folderId}
```

#### Search Messages

Example:

```bash
maton outlook message search "quarterly report"
```

### Calendar

#### List Calendars

```bash
GET /outlook/v1.0/me/calendars
```

Example:

```bash
maton outlook calendar list
```

#### List Events

```bash
GET /outlook/v1.0/me/calendar/events
```

Example:

```bash
maton outlook event list
```

With date filter:

```bash
GET /outlook/v1.0/me/calendar/events?$filter=start/dateTime ge '2024-01-01'&$top=10
```

Example:

```bash
maton outlook event list --filter "start/dateTime ge '2024-01-01'" --top 10
```

#### Get Event

```bash
GET /outlook/v1.0/me/events/{eventId}
```

Example:

```bash
maton outlook event view {eventId}
```

#### Create Event

```bash
POST /outlook/v1.0/me/calendar/events
Content-Type: application/json

{
  "subject": "Meeting",
  "start": {
    "dateTime": "2024-01-15T10:00:00",
    "timeZone": "UTC"
  },
  "end": {
    "dateTime": "2024-01-15T11:00:00",
    "timeZone": "UTC"
  },
  "attendees": [
    {
      "emailAddress": {
        "address": "attendee@example.com"
      },
      "type": "required"
    }
  ]
}
```

Example:

```bash
maton outlook event create --subject "Meeting" --start 2024-01-15T10:00:00 --end 2024-01-15T11:00:00 --timezone UTC --attendees attendee@example.com
```

#### Delete Event

```bash
DELETE /outlook/v1.0/me/events/{eventId}
```

Example:

```bash
maton outlook event delete {eventId}
```

### Contacts

#### List Contacts

```bash
GET /outlook/v1.0/me/contacts
```

Example:

```bash
maton outlook contact list
```

#### Get Contact

```bash
GET /outlook/v1.0/me/contacts/{contactId}
```

Example:

```bash
maton outlook contact view {contactId}
```

#### Create Contact

```bash
POST /outlook/v1.0/me/contacts
Content-Type: application/json

{
  "givenName": "John",
  "surname": "Doe",
  "emailAddresses": [
    {
      "address": "john.doe@example.com"
    }
  ]
}
```

Example:

```bash
maton outlook contact create --given-name John --surname Doe --email john.doe@example.com
```

#### Delete Contact

```bash
DELETE /outlook/v1.0/me/contacts/{contactId}
```

Example:

```bash
maton outlook contact delete {contactId}
```

## Query Parameters

Use OData query parameters:

- `$top=10` - Limit results
- `$skip=20` - Skip results (pagination)
- `$select=subject,from` - Select specific fields
- `$filter=isRead eq false` - Filter results
- `$orderby=receivedDateTime desc` - Sort results
- `$search="keyword"` - Search content

## Pagination

Outlook uses cursor-based pagination. The CLI automatically paginates with '--paginate'.

Example:

```bash
maton outlook message list --folder Inbox --paginate
```

## Code Examples

### CLI

```bash
# List recent inbox messages
maton outlook message list --folder Inbox --top 25

# Send an email
maton outlook message send --to alice@example.com --subject hi --body "hello"

# Search for messages
maton outlook message search "quarterly report"
```

### JavaScript

```javascript
const response = await fetch(
  'https://api.maton.ai/outlook/v1.0/me/messages?$top=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://api.maton.ai/outlook/v1.0/me/messages',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'$top': 10, '$filter': 'isRead eq false'}
)
```

## Notes

- Use `me` as the user identifier for the authenticated user
- Message body content types: `Text` or `HTML`
- Well-known folder names work as folder IDs: `Inbox`, `Drafts`, `SentItems`, etc.
- Calendar events use ISO 8601 datetime format
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets (`fields[]`, `sort[]`, `records[]`) to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments. You may get "Invalid API key" errors when piping.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Outlook connection |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Microsoft Graph API |

### Troubleshooting: API Key Issues

**CLI:**

1. Check your auth state:

```bash
maton whoami
```

2. Verify the API key is valid by listing connections:

```bash
maton connection list
```

**Manual:**

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `outlook`. For example:

- Correct: `https://api.maton.ai/outlook/v1.0/me/messages`
- Incorrect: `https://api.maton.ai/v1.0/me/messages`

## Resources

- [Microsoft Graph API Overview](https://learn.microsoft.com/en-us/graph/api/overview)
- [Mail API](https://learn.microsoft.com/en-us/graph/api/resources/mail-api-overview)
- [Calendar API](https://learn.microsoft.com/en-us/graph/api/resources/calendar)
- [Contacts API](https://learn.microsoft.com/en-us/graph/api/resources/contact)
- [Query Parameters](https://learn.microsoft.com/en-us/graph/query-parameters)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)

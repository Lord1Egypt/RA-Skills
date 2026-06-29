---
name: google-calendar
description: |
  Google Calendar API integration with managed OAuth. Create events, list calendars, check availability, and manage schedules. Use this skill when users want to interact with Google Calendar. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Google Calendar

Access the Google Calendar API with managed OAuth authentication. Create and manage events, list calendars, and check availability.

## Quick Start

Show today's events on the primary calendar.

**CLI:**

```bash
# Show today's agenda (defaults to primary calendar when -c is omitted)
maton google-calendar agenda --today
```

```bash
maton api '/google-calendar/calendar/v3/calendars/primary/events?singleEvents=true&orderBy=startTime&timeMin=2026-05-05T00:00:00Z&timeMax=2026-05-06T00:00:00Z'
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/google-calendar/calendar/v3/calendars/primary/events?singleEvents=true&orderBy=startTime&timeMin=2026-05-05T00:00:00Z&timeMax=2026-05-06T00:00:00Z')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/google-calendar/{native-api-path}
```

Maton proxies requests to `www.googleapis.com` and automatically injects your OAuth token.

## Installation

**NPM:**
```bash
npm install -g @maton/cli
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

Manage your Google OAuth connections at `https://api.maton.ai`.

### List Connections

**CLI:**

```bash
maton connection list google-calendar --status ACTIVE
```

```bash
maton api -X GET /connections -f app=google-calendar -f status=ACTIVE
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=google-calendar&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

**CLI:**

```bash
maton connection create google-calendar
```

```bash
maton api /connections -f app=google-calendar
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-calendar'}).encode()
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
    "app": "google-calendar",
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

If you have multiple Google Calendar connections, specify which one to use:

**CLI:**

```bash
maton google-calendar event list -c primary --connection {connection_id}
```

```bash
maton api /google-calendar/calendar/v3/calendars/primary/events --connection {connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/google-calendar/calendar/v3/calendars/primary/events')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always specify the connection to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to calendars, events, and availability within the connected Google Calendar account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.

## API Reference

### List Calendars

```bash
GET /google-calendar/calendar/v3/users/me/calendarList
```

Example:

```bash
maton google-calendar calendar list
```

### Get Calendar

```bash
GET /google-calendar/calendar/v3/calendars/{calendarId}
```

Example:

```bash
maton google-calendar calendar view primary
```

### List Events

```bash
GET /google-calendar/calendar/v3/calendars/team@example.com/events?maxResults=10&orderBy=startTime&singleEvents=true
```

With time bounds:

```bash
GET /google-calendar/calendar/v3/calendars/team@example.com/events?timeMin=2024-01-01T00:00:00Z&timeMax=2024-12-31T23:59:59Z&singleEvents=true&orderBy=startTime
```

Example:

```bash
maton google-calendar event list -c team@example.com --time-min 2026-06-17T00:00:00Z --time-max 2026-06-18T00:00:00Z
```

### Get Event

```bash
GET /google-calendar/calendar/v3/calendars/primary/events/{eventId}
```

Example:

```bash
maton google-calendar event view EVENT_ID
```

### Create Event

```bash
POST /google-calendar/calendar/v3/calendars/primary/events
Content-Type: application/json

{
  "summary": "Team Meeting",
  "description": "Weekly sync",
  "start": {
    "dateTime": "2024-01-15T10:00:00",
    "timeZone": "America/Los_Angeles"
  },
  "end": {
    "dateTime": "2024-01-15T11:00:00",
    "timeZone": "America/Los_Angeles"
  },
  "attendees": [
    {"email": "attendee@example.com"}
  ]
}
```

Example:

```bash
maton google-calendar event create --summary 'Team Meeting' --description 'Weekly sync' --start 2024-01-15T10:00:00-08:00 --end 2024-01-15T11:00:00-08:00 --attendee attendee@example.com
```

### Create All-Day Event

```bash
POST /google-calendar/calendar/v3/calendars/primary/events
Content-Type: application/json

{
  "summary": "All Day Event",
  "start": {"date": "2024-01-15"},
  "end": {"date": "2024-01-16"}
}
```

### Update Event

```bash
PUT /google-calendar/calendar/v3/calendars/primary/events/{eventId}
Content-Type: application/json

{
  "summary": "Updated Meeting Title",
  "start": {"dateTime": "2024-01-15T10:00:00Z"},
  "end": {"dateTime": "2024-01-15T11:00:00Z"}
}
```

Example:

```bash
maton google-calendar event update EVENT_ID --summary 'Updated Meeting Title' --start 2024-01-15T10:00:00Z --end 2024-01-15T11:00:00Z
```

### Patch Event (partial update)

```bash
PATCH /google-calendar/calendar/v3/calendars/primary/events/{eventId}
Content-Type: application/json

{
  "summary": "New Title Only"
}
```

Example:

```bash
maton google-calendar event update EVENT_ID --summary 'New Title Only'
```

### Delete Event

```bash
DELETE /google-calendar/calendar/v3/calendars/primary/events/{eventId}
```

Example:

```bash
maton google-calendar event delete EVENT_ID
```

### Quick Add Event (natural language)

```bash
POST /google-calendar/calendar/v3/calendars/primary/events/quickAdd?text=Meeting+with+John+tomorrow+at+3pm
```

Example:

```bash
maton google-calendar event quick-add --text 'Meeting with John tomorrow at 3pm'
```

### Free/Busy Query

```bash
POST /google-calendar/calendar/v3/freeBusy
Content-Type: application/json

{
  "timeMin": "2024-01-15T00:00:00Z",
  "timeMax": "2024-01-16T00:00:00Z",
  "items": [{"id": "primary"}]
}
```

Example:

```bash
maton google-calendar freebusy query --time-min 2024-01-15T00:00:00Z --time-max 2024-01-16T00:00:00Z
```

## Pagination

Google Calendar uses token-based pagination. The CLI automatically paginates with '--paginate'.

Example:

```bash
maton google-calendar event list --paginate
```

## Code Examples

### CLI

```bash
# Show today's agenda (defaults to primary calendar when -c is omitted)
maton google-calendar agenda --today

# Filter with jq
maton google-calendar event list --json --jq '.items[] | {summary: .summary, start: .start.dateTime}'

# Extract specific fields
maton google-calendar calendar list --json --jq '.items[].summary'
```

### JavaScript

```javascript
// List events
const response = await fetch(
  'https://api.maton.ai/google-calendar/calendar/v3/calendars/primary/events?maxResults=10&singleEvents=true',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);

// Create event
await fetch(
  'https://api.maton.ai/google-calendar/calendar/v3/calendars/primary/events',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({
      summary: 'Meeting',
      start: { dateTime: '2024-01-15T10:00:00Z' },
      end: { dateTime: '2024-01-15T11:00:00Z' }
    })
  }
);
```

### Python

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}

# List events
events = requests.get(
    'https://api.maton.ai/google-calendar/calendar/v3/calendars/primary/events',
    headers=headers,
    params={'maxResults': 10, 'singleEvents': 'true'}
).json()

# Create event
response = requests.post(
    'https://api.maton.ai/google-calendar/calendar/v3/calendars/primary/events',
    headers=headers,
    json={
        'summary': 'Meeting',
        'start': {'dateTime': '2024-01-15T10:00:00Z'},
        'end': {'dateTime': '2024-01-15T11:00:00Z'}
    }
)
```

## Notes

- Times must be in RFC3339 format (e.g., `2024-01-15T10:00:00Z`)
- For recurring events, use `singleEvents=true` to expand instances
- `orderBy=startTime` requires `singleEvents=true`
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets (`fields[]`, `sort[]`, `records[]`) to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments. You may get "Invalid API key" errors when piping.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Google Calendar connection |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Google Calendar API |

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

1. Ensure your URL path starts with `google-calendar`. For example:

- Correct: `https://api.maton.ai/google-calendar/calendar/v3/calendars/primary/events`
- Incorrect: `https://api.maton.ai/calendar/v3/calendars/primary/events`

## Resources

- [Calendar API Overview](https://developers.google.com/calendar/api/v3/reference)
- [List Calendars](https://developers.google.com/workspace/calendar/api/v3/reference/calendarList/list)
- [List Events](https://developers.google.com/workspace/calendar/api/v3/reference/events/list)
- [Get Event](https://developers.google.com/workspace/calendar/api/v3/reference/events/get)
- [Insert Event](https://developers.google.com/workspace/calendar/api/v3/reference/events/insert)
- [Update Event](https://developers.google.com/workspace/calendar/api/v3/reference/events/update)
- [Delete Event](https://developers.google.com/workspace/calendar/api/v3/reference/events/delete)
- [Quick Add Event](https://developers.google.com/workspace/calendar/api/v3/reference/events/quickAdd)
- [Free/Busy Query](https://developers.google.com/workspace/calendar/api/v3/reference/freebusy/query)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)

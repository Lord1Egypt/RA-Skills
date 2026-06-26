---
name: limehouse-calendar
description: Read and write calendar events with granular per-calendar permissions. Users control which calendars an agent can access and whether it can read, create, update, or delete events.
metadata:
  openclaw:
    requires:
      env:
        - CAL_API_KEY
      bins:
        - curl
    primaryEnv: CAL_API_KEY
---
# Calendar API

Authenticate every request with your API key:

```
Authorization: Bearer cal_<your-api-key>
```

API keys are created from the **Agents** tab in the dashboard, or via the setup flow below. Each key
is scoped to specific calendars with granular permissions: `can_read`, `can_create`, `can_update`,
`can_delete`, `can_create_invitees`, and `can_update_invitees`.

---

## Setup (getting an API key)

If you don't have a `cal_` API key yet, use the setup flow to let the user authorize access:

1. Create a setup session (no auth required):
```
POST https://cal.limehouse.io/api/v1/setup/sessions
```
Response: `{ "token": "...", "setup_url": "https://...", "expires_at": "..." }`

2. Direct the user to open `setup_url` in their browser. They will sign in, choose calendars, and
   configure permissions.

3. Poll for completion (every 3 seconds):
```
GET https://cal.limehouse.io/api/v1/setup/sessions/{token}/poll
```
Response while pending: `{ "status": "pending" }`
Response when complete: `{ "status": "completed", "agent_token": "cal_..." }`

4. Store the `agent_token` value. This is your API key for all subsequent requests.

The setup session expires after 30 minutes. If the agent cannot make HTTP requests, direct the user
to `https://cal.limehouse.io/connect` where they can create a key and copy it manually.

---

## Get agent info

```
GET /api/v1/agent/me
```

Get metadata about the current agent, including its name, description, permitted calendars with per-calendar permissions, and calendars the user owns that the agent does not yet have access to (connected_calendars_without_access).

**Response**
```json
{
  "id": 1,
  "name": "My Agent",
  "description": "optional description",
  "created_at": "2024-01-01T00:00:00",
  "last_used": "2024-01-02T12:00:00",
  "permitted_calendars": [
    {
      "calendar_id": 3,
      "calendar_name": "Work",
      "can_read": true,
      "can_create": false,
      "can_update": false,
      "can_delete": false,
      "can_create_invitees": false,
      "can_update_invitees": false
    }
  ],
  "connected_calendars_without_access": [
    {
      "calendar_id": 5,
      "calendar_name": "Side Projects"
    }
  ]
}
```

Use `connected_calendars_without_access` to discover calendars the agent could
request access to via `POST /api/v1/agent/request-permission-change`.

---

## List accessible calendars

```
GET /api/v1/agent/calendars
```

List all calendars the agent has access to, along with read/write permissions.

**Response** — array of calendar objects:
```json
[
  { "id": 3, "name": "Work", "color": "#4285F4", "timezone": "America/New_York" }
]
```

---

## List events

```
GET /api/v1/agent/events
GET /api/v1/agent/calendars/{calendar_id}/events
```

List events on a calendar, optionally filtered by a time range. If no calendar_id is provided, returns events from all calendars the agent has read access to. start and end accept either a full ISO 8601 datetime (e.g. "2026-03-05T00:00:00-08:00") or a date-only string (e.g. "2026-03-05") which is expanded to the full day in the user's timezone. Requires `can_read`. Filter results with optional query parameters.

| Parameter     | Type              | Required | Description                                   |
|---------------|-------------------|----------|-----------------------------------------------|
| `calendar_id` | integer           | No       | Filter to a specific calendar. If omitted, returns events from all readable calendars. |
| `start`       | ISO 8601 datetime or date | No | ISO 8601 datetime for the event start. When a timezone parameter is provided, the datetime is interpreted as wall-clock time in that timezone (any UTC offset is ignored). Otherwise, include a UTC offset for non-UTC times, e.g. "2026-02-26T17:30:00-08:00". Naive datetimes (without offset) are treated as UTC. Also accepts a date-only string (e.g. "2026-03-05") which expands to start of day in the user's timezone. |
| `end`         | ISO 8601 datetime or date | No | ISO 8601 datetime for the event end. Same timezone rules as start_time. Also accepts a date-only string which expands to end of day in the user's timezone. |

**Response** — array of event objects:
```json
[
  {
    "id": 42,
    "uid": "abc123",
    "calendar_id": 3,
    "summary": "Team standup",
    "description": "Daily sync",
    "location": "Conference Room A",
    "start_time": "2024-01-15T09:00:00Z",
    "end_time": "2024-01-15T09:30:00Z",
    "all_day": false,
    "recurrence_rule": null,
    "invitees": [
      {"email": "alice@example.com", "name": "Alice", "rsvp": "ACCEPTED"},
      {"email": "bob@example.com", "name": null, "rsvp": "NEEDS-ACTION"}
    ],
    "etag": "v1",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

---

## Create an event

```
POST /api/v1/agent/calendars/{calendar_id}/events
```

Create a new event on a calendar. Requires `can_create`. Returns `201 Created` with the new event object. If `invitees` is non-empty, also requires `can_create_invitees`.

| Field            | Type              | Required | Description                              |
|------------------|-------------------|----------|------------------------------------------|
| `summary`        | string            | Yes      | Event title (1–255 chars)                |
| `description`    | string            | No       | Event description                        |
| `location`       | string            | No       | Physical address or virtual meeting link for the event.    |
| `start_time`     | ISO 8601 datetime | Yes      | ISO 8601 datetime for the event start. When a timezone parameter is provided, the datetime is interpreted as wall-clock time in that timezone (any UTC offset is ignored). Otherwise, include a UTC offset for non-UTC times, e.g. "2026-02-26T17:30:00-08:00". Naive datetimes (without offset) are treated as UTC. |
| `end_time`       | ISO 8601 datetime | Yes      | ISO 8601 datetime for the event end. Same timezone rules as start_time. |
| `all_day`        | boolean           | No       | Default: `false`                         |
| `timezone`       | string            | No       | IANA timezone name (e.g. "America/Los_Angeles"). When provided, start_time and end_time are interpreted as wall-clock times in this timezone, and DST is handled automatically. |
| `recurrence_rule`| string            | No       | RRULE string for recurring events (e.g. "FREQ=WEEKLY;BYDAY=MO").|
| `invitees`       | array             | No       | List of attendees. Each item: `{"email": "...", "name": "..."}`. For Google-connected calendars, Google will send invite emails (`sendUpdates=all`). |

**Example request body**
```json
{
  "summary": "Team standup",
  "description": "Daily sync",
  "location": "Conference Room A",
  "start_time": "2024-01-15T09:00:00",
  "end_time": "2024-01-15T09:30:00",
  "timezone": "America/Los_Angeles",
  "invitees": [
    {"email": "alice@example.com", "name": "Alice"},
    {"email": "bob@example.com"}
  ]
}
```

---

## Update an event

```
PUT /api/v1/agent/calendars/{calendar_id}/events/{event_id}
```

Update an existing event on a calendar. Only include the fields you want to change — omitted fields are left untouched. Never include start_time or end_time unless you are explicitly changing the time. Requires `can_update`. Returns `200 OK` with the updated event object. If `invitees` is included in the request body, also requires `can_update_invitees`.

Sending `invitees` replaces the full attendee list (pass `[]` to remove all invitees).

| Field            | Type              | Description                              |
|------------------|-------------------|------------------------------------------|
| `summary`        | string            | Event title (1–255 chars)                |
| `description`    | string            | Event description                        |
| `location`       | string            | Physical address or virtual meeting link for the event.    |
| `start_time`     | ISO 8601 datetime | ISO 8601 datetime for the event start. When a timezone parameter is provided, the datetime is interpreted as wall-clock time in that timezone (any UTC offset is ignored). Otherwise, include a UTC offset for non-UTC times, e.g. "2026-02-26T17:30:00-08:00". Naive datetimes (without offset) are treated as UTC.      |
| `end_time`       | ISO 8601 datetime | ISO 8601 datetime for the event end. Same timezone rules as start_time.        |
| `all_day`        | boolean           | Whether the event spans the full day     |
| `timezone`       | string            | IANA timezone name (e.g. "America/Los_Angeles"). When provided, start_time and end_time are interpreted as wall-clock times in this timezone, and DST is handled automatically. |
| `recurrence_rule`| string            | RRULE string for recurring events (e.g. "FREQ=WEEKLY;BYDAY=MO").|
| `invitees`       | array             | Replace full attendee list (pass `[]` to clear) |

**Example — rename an event (only send the field that changes):**
```json
{ "summary": "Coffee with Alice" }
```

**Example — reschedule (only when intentionally changing the time):**
```json
{
  "start_time": "2024-01-15T10:00:00",
  "end_time": "2024-01-15T10:30:00",
  "timezone": "America/Los_Angeles"
}
```

---

## Delete an event

```
DELETE /api/v1/agent/calendars/{calendar_id}/events/{event_id}
```

Delete an event from a calendar. Requires `can_delete`. Returns `204 No Content`.

---

## Add travel time

```
POST /api/v1/agent/calendars/{calendar_id}/events/{event_id}/travel-time
```

Add a travel time buffer event before an existing event using Google Maps directions. Creates a new event that ends when the target event starts, with duration based on the calculated travel time. Requires `can_read` + `can_create`.
The target event must have a `location` set.

| Field                  | Type   | Required | Description                                                |
|------------------------|--------|----------|------------------------------------------------------------|
| `mode`                 | string | Yes      | Travel mode — one of "walking", "driving", "biking", or "transit". For transit, the route is planned to arrive by the event's start time. |
| `start_location_type`  | string | No       | Where the user is traveling from — "home", "work", or "custom". If not specified, uses the location of the previous event on the same day, or falls back to the user's home address. |
| `start_location_address` | string | No     | Custom start address. Required when start_location_type is "custom".                              |

**Example request body**
```json
{
  "mode": "transit",
  "start_location_type": "home"
}
```

**Response** — `201 Created`:
```json
{
  "event_id": 42,
  "travel_event_id": 43,
  "duration_seconds": 1800,
  "duration_text": "30 mins",
  "distance_text": "5.2 km",
  "origin": "123 Home St, City",
  "destination": "456 Office Ave, City",
  "mode": "transit"
}
```

The user's home and work addresses are set via `PUT /api/v1/auth/me/preferences` with
`home_address` and/or `work_address` fields.

---

## Request a calendar connection

```
POST /api/v1/agent/request-calendar-connection
```

Request the user to connect a new calendar provider. Returns a confirmation URL that the user must visit to authorize the connection. The agent cannot connect the calendar directly — the user must click the link and approve.

| Field      | Type   | Required | Description                        |
|------------|--------|----------|------------------------------------|
| `provider` | string | Yes      | The calendar provider to connect — "google" or "microsoft".        |

**Response** — `201 Created`:
```json
{
  "confirmation_url": "https://cal.limehouse.io/confirm/abc123",
  "expires_at": "2026-03-09T15:10:00"
}
```

Surface the `confirmation_url` in chat so the user can click it.

---

## Request a permission change

```
POST /api/v1/agent/request-permission-change
```

Request the user to grant or change this agent's permissions on a calendar. Returns a confirmation URL that the user must visit to approve the change. The requested permissions are suggestions — the user can adjust them before confirming.

| Field                   | Type    | Required | Description                              |
|-------------------------|---------|----------|------------------------------------------|
| `calendar_id`           | integer | Yes      | The ID of the calendar.                       |
| `requested_permissions` | object  | Yes      | Permission flags (see below)             |

**`requested_permissions` fields** (all boolean, all optional — defaults to current value):

| Key                  | Description                        |
|----------------------|------------------------------------|
| `can_read`           | Request read access to events on this calendar.               |
| `can_create`         | Request permission to create events on this calendar.             |
| `can_update`         | Request permission to update events on this calendar.             |
| `can_delete`         | Request permission to delete events on this calendar.             |
| `can_create_invitees`| Add invitees when creating events  |
| `can_update_invitees`| Modify invitees when updating      |

**Response** — `201 Created`:
```json
{
  "confirmation_url": "https://cal.limehouse.io/confirm/def456",
  "expires_at": "2026-03-09T15:10:00"
}
```

If a matching pending request already exists, returns `409` with the existing URL.

**Tip:** Call `GET /api/v1/agent/me` first to see which calendars the agent already
has access to and which ones it doesn't (`connected_calendars_without_access`).

---

## Error responses

| Status             | Meaning                                                                 |
|--------------------|-------------------------------------------------------------------------|
| `401 Unauthorized` | Missing or invalid API key                                              |
| `403 Forbidden`    | Key exists but lacks permission — use `request-permission-change`       |
| `404 Not Found`    | Calendar or event does not exist                                        |
| `409 Conflict`     | A pending confirmation already exists (returns the existing URL)        |

---

## Quick-start (curl)

```bash
KEY="cal_your_api_key_here"
BASE="https://cal.limehouse.io/api/v1"

# Discover accessible calendars
curl -H "Authorization: Bearer $KEY" "$BASE/agent/calendars"

# List events for calendar 3 in January 2024
curl -H "Authorization: Bearer $KEY" \
  "$BASE/agent/calendars/3/events?start=2024-01-01T00:00:00&end=2024-01-31T23:59:59"

# Create an event
curl -X POST -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"summary":"My event","start_time":"2024-01-20T14:00:00","end_time":"2024-01-20T15:00:00"}' \
  "$BASE/agent/calendars/3/events"
```

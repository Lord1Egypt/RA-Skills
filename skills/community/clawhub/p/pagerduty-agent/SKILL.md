---
name: pagerduty-agent
description: "Manage PagerDuty incidents, on-call schedules, services, and maintenance windows directly from your agent."
version: 1.0.0
emoji: "🚨"
homepage: https://github.com/openclaw/skills
metadata:
  openclaw:
    requires:
      env:
        - PAGERDUTY_API_KEY
      bins:
        - node
      anyBins: []
    primaryEnv: PAGERDUTY_API_KEY
    always: false
    tags:
      - pagerduty
      - incidents
      - oncall
      - devops
      - observability
      - alerting
---

# PagerDuty Agent

> ⚠️ This is an unofficial community skill and is not affiliated with or endorsed by PagerDuty, Inc.

Trigger, acknowledge, and resolve PagerDuty incidents, check who's on-call,
manage maintenance windows, and inspect services — all without leaving your
agent workflow.

## Setup

1. Generate a PagerDuty API key: **PagerDuty → Integrations → API Access Keys → Create New API Key**
2. Export required environment variables:

```bash
export PAGERDUTY_API_KEY="your-v2-api-key"
export PAGERDUTY_FROM_EMAIL="you@yourcompany.com"   # required for write operations
```

> `PAGERDUTY_FROM_EMAIL` must be the email of a valid PagerDuty user in your
> account. It is required by PagerDuty's REST API for any POST/PUT request.

## Usage

All commands are invoked by piping a `{ command, params }` JSON object to
`node pagerduty.js`. The skill returns structured JSON on stdout.

```bash
echo '{"command":"list_incidents","params":{"status":"triggered"}}' | node pagerduty.js
```

---

## Commands

### Incidents

---

#### `trigger_incident`

Create a new incident on a service.

**Params**

| Field | Type | Required | Description |
|---|---|---|---|
| `service_id` | string | ✓ | PagerDuty service ID (e.g. `"P1ABCDE"`) |
| `title` | string | ✓ | Incident title / summary |
| `severity` | string | | `"critical"`, `"error"`, `"warning"`, `"info"` — maps to urgency |
| `body` | string | | Detailed description / runbook context |

**Example**

```json
{
  "command": "trigger_incident",
  "params": {
    "service_id": "P1ABCDE",
    "title": "Database replication lag > 60s",
    "severity": "critical",
    "body": "Replica db-02 is 90s behind primary. Check pg_stat_replication."
  }
}
```

**Response**

```json
{
  "id": "Q2W3E4R",
  "incident_number": 1042,
  "title": "Database replication lag > 60s",
  "status": "triggered",
  "urgency": "high",
  "html_url": "https://your-subdomain.pagerduty.com/incidents/Q2W3E4R",
  "created_at": "2026-03-04T12:00:00Z",
  "service": { "id": "P1ABCDE", "name": "Production Database" }
}
```

---

#### `acknowledge_incident`

Acknowledge an incident to signal it is being worked on.

**Params**

| Field | Type | Required | Description |
|---|---|---|---|
| `incident_id` | string | ✓ | PagerDuty incident ID |

**Example**

```json
{ "command": "acknowledge_incident", "params": { "incident_id": "Q2W3E4R" } }
```

**Response**

```json
{
  "id": "Q2W3E4R",
  "incident_number": 1042,
  "title": "Database replication lag > 60s",
  "status": "acknowledged",
  "acknowledged_at": "2026-03-04T12:03:00Z"
}
```

---

#### `resolve_incident`

Mark an incident as resolved.

**Params**

| Field | Type | Required | Description |
|---|---|---|---|
| `incident_id` | string | ✓ | PagerDuty incident ID |

**Example**

```json
{ "command": "resolve_incident", "params": { "incident_id": "Q2W3E4R" } }
```

**Response**

```json
{
  "id": "Q2W3E4R",
  "incident_number": 1042,
  "title": "Database replication lag > 60s",
  "status": "resolved",
  "resolved_at": "2026-03-04T12:45:00Z"
}
```

---

#### `list_incidents`

List incidents, optionally filtered by status.

**Params**

| Field | Type | Required | Description |
|---|---|---|---|
| `status` | string | | `"triggered"`, `"acknowledged"`, `"resolved"` |
| `limit` | number | | Max results (default 25) |

**Example**

```json
{
  "command": "list_incidents",
  "params": { "status": "triggered", "limit": 10 }
}
```

**Response**

```json
{
  "total": 3,
  "limit": 10,
  "incidents": [
    {
      "id": "Q2W3E4R",
      "incident_number": 1042,
      "title": "Database replication lag > 60s",
      "status": "triggered",
      "urgency": "high",
      "created_at": "2026-03-04T12:00:00Z",
      "service": { "id": "P1ABCDE", "name": "Production Database" },
      "assigned_to": ["Alice Smith"]
    }
  ]
}
```

---

#### `get_incident`

Fetch full details for a single incident.

**Params**

| Field | Type | Required | Description |
|---|---|---|---|
| `incident_id` | string | ✓ | PagerDuty incident ID |

**Example**

```json
{ "command": "get_incident", "params": { "incident_id": "Q2W3E4R" } }
```

**Response**

```json
{
  "id": "Q2W3E4R",
  "incident_number": 1042,
  "title": "Database replication lag > 60s",
  "status": "acknowledged",
  "urgency": "high",
  "html_url": "https://your-subdomain.pagerduty.com/incidents/Q2W3E4R",
  "created_at": "2026-03-04T12:00:00Z",
  "last_status_change_at": "2026-03-04T12:03:00Z",
  "service": { "id": "P1ABCDE", "name": "Production Database" },
  "assigned_to": ["Alice Smith"],
  "escalation_policy": { "id": "P9XYZ12", "name": "Eng On-Call" },
  "body": "Replica db-02 is 90s behind primary. Check pg_stat_replication."
}
```

---

#### `add_incident_note`

Append a timestamped note to an incident's timeline.

**Params**

| Field | Type | Required | Description |
|---|---|---|---|
| `incident_id` | string | ✓ | PagerDuty incident ID |
| `content` | string | ✓ | Note text (supports Markdown) |

**Example**

```json
{
  "command": "add_incident_note",
  "params": {
    "incident_id": "Q2W3E4R",
    "content": "Root cause identified: checkpoint completion time spiked to 95%. Increased max_wal_size and restarting standby."
  }
}
```

**Response**

```json
{
  "id": "NOTE123",
  "content": "Root cause identified...",
  "created_at": "2026-03-04T12:20:00Z",
  "user": "Alice Smith"
}
```

---

### On-Call & Schedules

---

#### `get_oncall`

List who is currently on-call, optionally scoped to a schedule.

**Params**

| Field | Type | Required | Description |
|---|---|---|---|
| `schedule_id` | string | | Filter to a specific schedule ID |

**Example**

```json
{ "command": "get_oncall", "params": { "schedule_id": "SCHED01" } }
```

**Response**

```json
{
  "oncalls": [
    {
      "user": { "id": "UABC123", "name": "Alice Smith" },
      "schedule": { "id": "SCHED01", "name": "Primary On-Call" },
      "escalation_policy": { "id": "P9XYZ12", "name": "Eng On-Call" },
      "escalation_level": 1,
      "start": "2026-03-04T08:00:00Z",
      "end": "2026-03-11T08:00:00Z"
    }
  ]
}
```

---

#### `list_schedules`

Return all on-call schedules in the account.

**Params** — none

**Example**

```json
{ "command": "list_schedules", "params": {} }
```

**Response**

```json
{
  "total": 2,
  "schedules": [
    {
      "id": "SCHED01",
      "name": "Primary On-Call",
      "description": "Weekly rotation — eng team",
      "time_zone": "America/New_York",
      "html_url": "https://your-subdomain.pagerduty.com/schedules/SCHED01",
      "users": [
        { "id": "UABC123", "name": "Alice Smith" },
        { "id": "UDEF456", "name": "Bob Jones" }
      ]
    }
  ]
}
```

---

### Services

---

#### `list_services`

Return all PagerDuty services.

**Params** — none

**Example**

```json
{ "command": "list_services", "params": {} }
```

**Response**

```json
{
  "total": 3,
  "services": [
    {
      "id": "P1ABCDE",
      "name": "Production Database",
      "description": "RDS Postgres cluster",
      "status": "active",
      "html_url": "https://your-subdomain.pagerduty.com/services/P1ABCDE",
      "escalation_policy": { "id": "P9XYZ12", "name": "Eng On-Call" }
    }
  ]
}
```

---

#### `get_service`

Fetch details for a single service including integrations.

**Params**

| Field | Type | Required | Description |
|---|---|---|---|
| `service_id` | string | ✓ | PagerDuty service ID |

**Example**

```json
{ "command": "get_service", "params": { "service_id": "P1ABCDE" } }
```

**Response**

```json
{
  "id": "P1ABCDE",
  "name": "Production Database",
  "description": "RDS Postgres cluster",
  "status": "active",
  "html_url": "https://your-subdomain.pagerduty.com/services/P1ABCDE",
  "created_at": "2024-01-15T09:00:00Z",
  "escalation_policy": { "id": "P9XYZ12", "name": "Eng On-Call" },
  "integrations": [
    { "id": "INT001", "name": "Datadog" }
  ],
  "alert_grouping": "intelligent",
  "alert_grouping_timeout": 300
}
```

---

### Maintenance

---

#### `create_maintenance_window`

Put one or more services into maintenance mode to suppress alerts.

**Params**

| Field | Type | Required | Description |
|---|---|---|---|
| `service_ids` | string[] | ✓ | Array of service IDs to put in maintenance |
| `start_time` | string | ✓ | ISO 8601 start time (e.g. `"2026-03-04T22:00:00Z"`) |
| `end_time` | string | ✓ | ISO 8601 end time |
| `description` | string | | Reason for maintenance |

**Example**

```json
{
  "command": "create_maintenance_window",
  "params": {
    "service_ids": ["P1ABCDE", "P2FGHIJ"],
    "start_time": "2026-03-04T22:00:00Z",
    "end_time": "2026-03-05T00:00:00Z",
    "description": "Scheduled DB migration — expect brief connectivity drops"
  }
}
```

**Response**

```json
{
  "id": "MW00123",
  "description": "Scheduled DB migration — expect brief connectivity drops",
  "start_time": "2026-03-04T22:00:00Z",
  "end_time": "2026-03-05T00:00:00Z",
  "html_url": "https://your-subdomain.pagerduty.com/maintenance_windows/MW00123",
  "services": [
    { "id": "P1ABCDE", "name": "Production Database" },
    { "id": "P2FGHIJ", "name": "API Gateway" }
  ]
}
```

---

#### `list_maintenance_windows`

Return all current and upcoming maintenance windows.

**Params** — none

**Example**

```json
{ "command": "list_maintenance_windows", "params": {} }
```

**Response**

```json
{
  "total": 1,
  "maintenance_windows": [
    {
      "id": "MW00123",
      "description": "Scheduled DB migration",
      "start_time": "2026-03-04T22:00:00Z",
      "end_time": "2026-03-05T00:00:00Z",
      "html_url": "https://your-subdomain.pagerduty.com/maintenance_windows/MW00123",
      "services": [
        { "id": "P1ABCDE", "name": "Production Database" }
      ]
    }
  ]
}
```

---

## Error Responses

All errors return a JSON object with a single `error` key:

```json
{ "error": "PAGERDUTY_API_KEY environment variable is not set" }
{ "error": "params.incident_id is required" }
{ "error": "Incident Not Found" }
```

## Tips

- Use `list_services` to discover service IDs before triggering incidents.
- Use `list_schedules` to find schedule IDs before calling `get_oncall`.
- `severity` values `"critical"` and `"error"` map to PagerDuty `urgency: high`; everything else maps to `urgency: low`.
- Times in `create_maintenance_window` must be ISO 8601 UTC strings.
- `PAGERDUTY_FROM_EMAIL` is required for all write operations (trigger, acknowledge, resolve, add note, create maintenance window).

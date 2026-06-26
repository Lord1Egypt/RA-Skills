# Komandr Agent API Reference

Base URL: `https://komandr.vercel.app` (configurable via `KOMANDR_URL`)

All requests require: `Authorization: Bearer km_...`

---

## Endpoints

### GET /api/v1/agent/me

Returns the authenticated agent profile.

**Response** `200 OK`
```json
{
  "id": "string",
  "org_id": "string",
  "name": "string",
  "agent_type": "string",
  "api_key_prefix": "string",
  "status": "online | offline | busy | error | suspended",
  "capabilities": ["string"],
  "metadata": {},
  "last_heartbeat": "ISO8601 | null",
  "created_at": "ISO8601"
}
```

---

### POST /api/v1/agent/heartbeat

Updates agent online status. Send every 30 seconds.

**Request Body** (all optional)
```json
{
  "status": "online | busy | error | offline",
  "current_task_id": "string",
  "metrics": {}
}
```

**Response** `200 OK`
```json
{
  "ok": true,
  "server_time": "ISO8601"
}
```

---

### GET /api/v1/agent/tasks/next

Returns the next queued task, or `null`.

**Query Parameters**
- `capabilities` (optional): Comma-separated list, e.g. `?capabilities=code,research`

**Response** `200 OK`
```json
{
  "task": {
    "id": "string",
    "project_id": "string",
    "convoy_id": "string | null",
    "title": "string",
    "description": "string | null",
    "status": "queued",
    "priority": 0,
    "position": 0,
    "task_type": "string",
    "context": {},
    "dependencies": ["string"],
    "assigned_agent": "string | null",
    "assigned_by": "string | null",
    "progress": 0,
    "created_at": "ISO8601",
    "updated_at": "ISO8601"
  }
}
```

When no task is available: `{ "task": null }`

---

### POST /api/v1/agent/tasks/:id/accept

Accepts a queued task. Sets status to `in_progress` and assigns it to you.

**Request Body**: None required.

**Response** `200 OK`
```json
{
  "task": { "...task object with status: in_progress..." }
}
```

**Error** `409 Conflict` — Task already accepted by another agent.

---

### POST /api/v1/agent/tasks/:id/progress

Reports progress on an accepted task.

**Request Body**
```json
{
  "progress": 50,
  "message": "Optional status message"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `progress` | integer | Yes | 0-100 |
| `message` | string | No | Human-readable status |

**Response** `200 OK`
```json
{
  "task": { "...task object with updated progress..." }
}
```

---

### POST /api/v1/agent/tasks/:id/submit

Submits completed work.

**Request Body**
```json
{
  "summary": "What was done",
  "result": { "files_changed": 3 },
  "artifacts": [
    {
      "filename": "output.diff",
      "content_type": "diff",
      "content": "file contents"
    }
  ]
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `summary` | string | Yes | Human-readable summary |
| `result` | object | Yes | Structured result data |
| `artifacts` | array | No | File artifacts |

Each artifact:

| Field | Type | Required | Description |
|---|---|---|---|
| `filename` | string | Yes | File name |
| `content_type` | string | Yes | MIME type or category |
| `content` | string | No | Inline content |
| `storage_path` | string | No | Remote storage path |

**Response** `200 OK`
```json
{
  "submission": { "summary": "...", "result": {} },
  "task": { "...task object with status: submitted..." }
}
```

---

### POST /api/v1/agent/tasks/:id/fail

Reports that a task could not be completed.

**Request Body**
```json
{
  "error_type": "compilation_error",
  "message": "Build failed on line 42",
  "recoverable": true
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `error_type` | string | Yes | Error category |
| `message` | string | Yes | What went wrong |
| `recoverable` | boolean | Yes | `true` = task returns to queue |

**Response** `200 OK`
```json
{
  "task": { "...task object with status: failed..." }
}
```

---

## Task Object

Full task shape returned in all task-related responses:

```json
{
  "id": "string",
  "project_id": "string",
  "convoy_id": "string | null",
  "title": "string",
  "description": "string | null",
  "status": "backlog | queued | in_progress | submitted | in_review | approved | rejected | failed | cancelled",
  "priority": 0,
  "position": 0,
  "task_type": "string",
  "context": {},
  "dependencies": ["string"],
  "assigned_agent": "string | null",
  "assigned_by": "string | null",
  "progress": 0,
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

---

## Error Responses

All errors return:

```json
{
  "error": "Human-readable message",
  "code": "ERROR_CODE",
  "details": null
}
```

| Status | Code | Meaning |
|---|---|---|
| 400 | `BAD_REQUEST` | Invalid request body |
| 401 | `UNAUTHORIZED` | Invalid or missing API key |
| 404 | `NOT_FOUND` | Resource does not exist |
| 409 | `CONFLICT` | Task already accepted |
| 429 | `RATE_LIMITED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Server error, retry later |

---

## Task Lifecycle

```
queued --> [accept] --> in_progress --> [submit] --> submitted --> in_review --> approved
                            |                                        |
                            +---> [fail] --> failed                   +---> rejected
```

---
name: komandr
description: Connect to Komandr Command Center to receive tasks, report progress, and submit work results. Komandr is a task orchestration platform where humans assign work to AI agents.
---

# Komandr Skill

This skill connects you to the **Komandr Command Center**, a task orchestration platform. Humans create tasks in Komandr and assign them to AI agents. Your job is to poll for tasks, accept them, do the work, and submit results.

## Installation

1. Copy this skill folder to `~/.openclaw/skills/komandr/`
2. Set environment variable `KOMANDR_API_KEY` to your agent API key (starts with `km_...`)
3. Set environment variable `KOMANDR_URL` to your Komandr instance (default: `https://komandr.vercel.app`)
4. Restart OpenClaw

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `KOMANDR_API_KEY` | Yes | -- | Your agent API key (`km_...`) |
| `KOMANDR_URL` | No | `https://komandr.vercel.app` | Komandr server URL |

## Quick Start

Once configured, use the bridge script to interact with Komandr:

```bash
# Check who you are
npx tsx scripts/komandr-bridge.ts me

# Send a heartbeat (tells Komandr you are online)
npx tsx scripts/komandr-bridge.ts heartbeat

# Poll for the next available task
npx tsx scripts/komandr-bridge.ts poll

# Accept a task
npx tsx scripts/komandr-bridge.ts accept <task-id>

# Report progress (0-100)
npx tsx scripts/komandr-bridge.ts progress <task-id> 50 "Halfway done"

# Submit completed work
npx tsx scripts/komandr-bridge.ts submit <task-id> "Summary of work" '{"files_changed": 3}'

# Report failure
npx tsx scripts/komandr-bridge.ts fail <task-id> "Error message"
```

## Workflow

Follow this exact sequence when working with Komandr tasks:

### Step 1 — Go Online

Send a heartbeat so Komandr knows you are available:

```bash
npx tsx scripts/komandr-bridge.ts heartbeat
```

### Step 2 — Poll for Tasks

Check if there is a task waiting for you:

```bash
npx tsx scripts/komandr-bridge.ts poll
```

If the response contains `"task": null`, there is nothing to do. Wait and poll again later.

If a task is returned, note its `id`, `title`, `description`, `context`, and `task_type`.

### Step 3 — Accept the Task

Lock the task so no other agent picks it up:

```bash
npx tsx scripts/komandr-bridge.ts accept <task-id>
```

### Step 4 — Do the Work

Read the task description and context carefully. Perform whatever the task asks — write code, research, generate content, etc.

While working, report progress periodically so the human can see what you are doing:

```bash
npx tsx scripts/komandr-bridge.ts progress <task-id> 25 "Analyzing requirements"
npx tsx scripts/komandr-bridge.ts progress <task-id> 50 "Implementing solution"
npx tsx scripts/komandr-bridge.ts progress <task-id> 75 "Running tests"
```

Progress is a number from 0 to 100. The message is optional but strongly recommended.

### Step 5 — Submit Results

When done, submit your work:

```bash
npx tsx scripts/komandr-bridge.ts submit <task-id> "Implemented the feature as requested" '{"files_changed": 3, "tests_passed": true}'
```

The first argument after the task ID is a human-readable summary. The second is a JSON object with structured result data.

### Step 6 — Handle Failures

If you cannot complete the task, report the failure honestly:

```bash
npx tsx scripts/komandr-bridge.ts fail <task-id> "Could not compile: missing dependency X"
```

Failed tasks may be returned to the queue for another agent or for human review.

### Step 7 — Keep Sending Heartbeats

While working on long tasks, send heartbeats every 30 seconds to stay online:

```bash
npx tsx scripts/komandr-bridge.ts heartbeat
```

If Komandr stops receiving heartbeats, it will mark you as offline.

## API Reference (curl)

All requests require the header:

```
Authorization: Bearer km_your_api_key_here
Content-Type: application/json
```

Base URL: `https://komandr.vercel.app` (or your `KOMANDR_URL`).

### GET /api/v1/agent/me

Returns the authenticated agent's profile.

```bash
curl -s -H "Authorization: Bearer $KOMANDR_API_KEY" \
  "$KOMANDR_URL/api/v1/agent/me"
```

Response:
```json
{
  "id": "agent_abc123",
  "org_id": "org_xyz",
  "name": "my-agent",
  "agent_type": "openclaw",
  "status": "online",
  "capabilities": ["code", "research"],
  "last_heartbeat": "2026-03-24T10:00:00Z",
  "created_at": "2026-03-01T00:00:00Z"
}
```

### POST /api/v1/agent/heartbeat

Updates your online status. Send every 30 seconds.

```bash
curl -s -X POST -H "Authorization: Bearer $KOMANDR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "online"}' \
  "$KOMANDR_URL/api/v1/agent/heartbeat"
```

Request body (all fields optional):
```json
{
  "status": "online",
  "current_task_id": "task_abc123",
  "metrics": { "cpu": 45, "memory": 72 }
}
```

Valid status values: `"online"`, `"busy"`, `"error"`, `"offline"`.

Response:
```json
{
  "ok": true,
  "server_time": "2026-03-24T10:00:00Z"
}
```

### GET /api/v1/agent/tasks/next

Returns the next queued task for you, or `null` if none available.

```bash
curl -s -H "Authorization: Bearer $KOMANDR_API_KEY" \
  "$KOMANDR_URL/api/v1/agent/tasks/next"
```

Optional query parameter: `?capabilities=code,research` to filter by capability.

Response (task available):
```json
{
  "task": {
    "id": "task_abc123",
    "project_id": "proj_xyz",
    "convoy_id": null,
    "title": "Implement user authentication",
    "description": "Add JWT-based auth to the API...",
    "status": "queued",
    "priority": 1,
    "position": 0,
    "task_type": "code",
    "context": { "repo": "github.com/org/repo", "branch": "main" },
    "dependencies": [],
    "assigned_agent": null,
    "assigned_by": "user_abc",
    "progress": 0,
    "created_at": "2026-03-24T09:00:00Z",
    "updated_at": "2026-03-24T09:00:00Z"
  }
}
```

Response (no task):
```json
{
  "task": null
}
```

### POST /api/v1/agent/tasks/:id/accept

Accept a queued task. This assigns it to you and changes status to `in_progress`.

```bash
curl -s -X POST -H "Authorization: Bearer $KOMANDR_API_KEY" \
  -H "Content-Type: application/json" \
  "$KOMANDR_URL/api/v1/agent/tasks/task_abc123/accept"
```

Response:
```json
{
  "task": {
    "id": "task_abc123",
    "status": "in_progress",
    "assigned_agent": "agent_xyz",
    "progress": 0
  }
}
```

### POST /api/v1/agent/tasks/:id/progress

Report progress on a task you are working on.

```bash
curl -s -X POST -H "Authorization: Bearer $KOMANDR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"progress": 50, "message": "Halfway done"}' \
  "$KOMANDR_URL/api/v1/agent/tasks/task_abc123/progress"
```

Request body:
```json
{
  "progress": 50,
  "message": "Halfway done"
}
```

- `progress` (required): Integer 0-100.
- `message` (optional): Human-readable status update.

Response:
```json
{
  "task": {
    "id": "task_abc123",
    "status": "in_progress",
    "progress": 50
  }
}
```

### POST /api/v1/agent/tasks/:id/submit

Submit completed work.

```bash
curl -s -X POST -H "Authorization: Bearer $KOMANDR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Implemented JWT auth with refresh tokens",
    "result": { "files_changed": 5, "tests_added": 12 },
    "artifacts": [
      {
        "filename": "changes.diff",
        "content_type": "diff",
        "content": "--- a/auth.ts\n+++ b/auth.ts\n..."
      }
    ]
  }' \
  "$KOMANDR_URL/api/v1/agent/tasks/task_abc123/submit"
```

Request body:
```json
{
  "summary": "Human-readable summary of work done",
  "result": { "any": "structured data" },
  "artifacts": [
    {
      "filename": "output.txt",
      "content_type": "text/plain",
      "content": "file contents as string"
    }
  ]
}
```

- `summary` (required): What you did.
- `result` (required): Structured result object.
- `artifacts` (optional): Array of file artifacts.

Response:
```json
{
  "submission": { "summary": "...", "result": { ... } },
  "task": {
    "id": "task_abc123",
    "status": "submitted",
    "progress": 100
  }
}
```

### POST /api/v1/agent/tasks/:id/fail

Report that you cannot complete the task.

```bash
curl -s -X POST -H "Authorization: Bearer $KOMANDR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "error_type": "compilation_error",
    "message": "Build failed: missing dependency lodash",
    "recoverable": true
  }' \
  "$KOMANDR_URL/api/v1/agent/tasks/task_abc123/fail"
```

Request body:
```json
{
  "error_type": "runtime_error",
  "message": "Human-readable error description",
  "recoverable": true
}
```

- `error_type` (required): Category of the error (e.g., `compilation_error`, `runtime_error`, `timeout`, `dependency_missing`).
- `message` (required): What went wrong.
- `recoverable` (required): If `true`, the task returns to the queue. If `false`, it is marked as permanently failed.

Response:
```json
{
  "task": {
    "id": "task_abc123",
    "status": "failed"
  }
}
```

## Error Handling

All error responses follow this format:

```json
{
  "error": "Human-readable error message",
  "code": "ERROR_CODE"
}
```

Common HTTP status codes:

| Status | Meaning | Action |
|---|---|---|
| 200 | Success | Proceed normally |
| 400 | Bad request | Check your request body |
| 401 | Unauthorized | Check your `KOMANDR_API_KEY` |
| 404 | Not found | Task ID may be wrong or task was cancelled |
| 409 | Conflict | Task was already accepted by another agent |
| 429 | Rate limited | Wait and retry after a delay |
| 500 | Server error | Retry with exponential backoff |

## Tips

- Always send heartbeats while working. If you go offline, Komandr may reassign your task.
- Report progress frequently. Humans watch the dashboard and appreciate seeing that work is happening.
- Read the task `context` field carefully. It often contains repository URLs, branch names, file paths, or other essential information.
- If a task has `dependencies`, those tasks must be completed first. Do not accept tasks with unmet dependencies.
- Submit structured `result` data. Include things like `files_changed`, `tests_passed`, `lines_added` so humans can quickly assess the work.
- When failing a task, set `recoverable: true` if the issue is temporary (network error, rate limit) and `recoverable: false` if the task itself is impossible.

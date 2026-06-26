---
name: manus-api
description: Interact with the Manus AI agent platform via its REST API. Use this skill whenever the user mentions Manus, manus.ai, Manus API, Manus tasks, Manus projects, or wants to delegate work to the Manus AI agent — including creating tasks, uploading files, managing projects, polling task status, continuing multi-turn conversations, or setting up webhooks. Also trigger when the user says "send to Manus", "ask Manus to", "have Manus do", "manus agent", or references task IDs, session IDs, or Manus file uploads. This skill handles session/task-ID tracking to prevent accidental task duplication — a critical concern since every POST to /v1/tasks without a taskId creates a NEW task and consumes credits. Trigger this skill even for simple Manus questions like "what's the status of my Manus task" or "list my Manus sessions."
metadata:
  openclaw:
    requires:
      env:
        - MANUS_API_KEY
    primaryEnv: MANUS_API_KEY
---

# Manus API Skill

Manage tasks, projects, files, and sessions on the Manus AI agent platform.

## Setup

```bash
export MANUS_API_KEY="your-api-key"
```

Get your key from: Manus dashboard → Settings → Integration → Build with Manus API.

The session manager writes `.manus_sessions.json` to the project root to track active and archived sessions. Add it to `.gitignore` — it contains prompts, task IDs, and task URLs that may be sensitive.

```bash
echo ".manus_sessions.json" >> .gitignore
```

## Authentication

Every request uses the `API_KEY` header (not Bearer token):
```bash
curl -H "API_KEY: $MANUS_API_KEY" https://api.manus.ai/v1/tasks
```

Base URL: `https://api.manus.ai` — all endpoints under `/v1/`.

---

## Session Management (CRITICAL — Read First)

**Every `POST /v1/tasks` without a `taskId` creates a brand-new task and consumes credits.** There is no undo. Session tracking prevents accidental duplication.

For the full registry format, search algorithm, archival rules, and edge cases, read `references/session-management.md`.

### How It Works

All sessions are tracked in `.manus_sessions.json` in the project root:

```json
{
  "active": {
    "security-audit": { "task_id": "...", "description": "...", "tags": [...], ... }
  },
  "archived": {
    "q2-report": { "task_id": "...", "description": "...", "archived_reason": "completed", ... }
  }
}
```

**Active** = running or pending tasks. **Archived** = completed or failed (still searchable, can be resumed).

### The 4 Rules

1. **Before creating any task**, search the registry for a matching session. If found, continue it with `taskId`. If not, create new.
2. **After every task creation**, save `task_id` + metadata to the registry immediately.
3. **When multiple sessions match**, present the top matches and ask the user to pick. Never guess.
4. **When a task completes or fails**, move it from `active` to `archived` automatically.

### Session Resolution Flow

When the user wants to work with a session:

```
1. Search active sessions (name, description, tags, prompts)
      |
   1 match  -> Use it
   0 matches -> Search archived
   >1 match  -> Present list, ask user
      |
2. Search archived
      |
   1 match  -> Ask: "Archived (completed). Resume or start fresh?"
   0 matches -> Create new session
   >1 match  -> Present list, ask user
```

### Registry Entry Fields

Each session stores: `task_id`, `task_title`, `task_url`, `description` (agent-generated summary), `tags` (keywords for search), `project_id`, `project_name`, `agent_profile`, `task_mode`, `created_at`, `last_used`, `last_status`, `turn_count`, `first_prompt`, `last_prompt`.

Archived entries additionally store `archived_at` and `archived_reason`.

### Using the Session Manager Script

The script at `scripts/manus_session.py` handles all session tracking, API calls, polling, archival, and search. Use it instead of calling the API directly.

**As a library** (when an agent imports it):
```python
from scripts.manus_session import ManusSession

s = ManusSession()  # reads .env automatically

# New session
s.send("Review auth module for vulnerabilities",
       session_name="security-audit",
       tags=["security", "auth", "code-review"])

# Continue (auto-passes taskId)
s.send("Now check the token refresh logic",
       session_name="security-audit")

# Search sessions
matches = s.search("auth")

# Poll until done (auto-archives on completion)
result = s.poll_until_done("security-audit")

# List sessions
s.list_sessions()                        # active only
s.list_sessions(include_archived=True)   # both

# Resume archived session
s.unarchive("q2-report")
s.send("Add December data", session_name="q2-report")

# Import orphaned task from Manus webapp
s.import_task("TeBim6FDQf9peS52xHtAyh", session_name="imported-task")
```

**As a CLI** (when an agent runs it from the shell):
```bash
# Send prompt (new or continue)
python scripts/manus_session.py send "Review this PR" -s pr-review --tags security,backend
python scripts/manus_session.py send "Focus on auth" -s pr-review  # continues

# Search
python scripts/manus_session.py search "auth"

# List sessions
python scripts/manus_session.py sessions
python scripts/manus_session.py sessions --archived

# Check status
python scripts/manus_session.py status -s pr-review

# Poll until done
python scripts/manus_session.py poll -s pr-review

# Resume archived
python scripts/manus_session.py unarchive -s old-session

# Import orphaned task
python scripts/manus_session.py import-task TASK_ID --name my-task

# Upload file
python scripts/manus_session.py upload report.pdf

# Projects
python scripts/manus_session.py create-project "Code Reviews" --instruction "Check for security issues"
python scripts/manus_session.py projects

# Cleanup old archived sessions (>7 days)
python scripts/manus_session.py cleanup
```

---

## Quick Reference — Endpoints

| Resource  | Method | Path                      | Purpose                                 |
|----------|--------|---------------------------|-----------------------------------------|
| Projects | POST   | /v1/projects              | Create project with default instruction |
| Projects | GET    | /v1/projects              | List all projects                       |
| Tasks    | POST   | /v1/tasks                 | Create new task OR continue existing    |
| Tasks    | GET    | /v1/tasks                 | List tasks (filter, paginate, search)   |
| Tasks    | GET    | /v1/tasks/{task_id}       | Get single task detail + output         |
| Tasks    | PUT    | /v1/tasks/{task_id}       | Update task (title, sharing, visibility)|
| Tasks    | DELETE | /v1/tasks/{task_id}       | Permanently delete task                 |
| Files    | POST   | /v1/files                 | Get presigned upload URL                |
| Files    | GET    | /v1/files                 | List uploaded files                     |
| Files    | GET    | /v1/files/{file_id}       | Get file details                        |
| Files    | DELETE | /v1/files/{file_id}       | Delete a file                           |
| Webhooks | POST   | /v1/webhooks              | Register webhook URL                    |
| Webhooks | DELETE | /v1/webhooks/{webhook_id} | Remove webhook                          |

For full request/response schemas, read `references/api-reference.md`.

---

## Core Workflows

### 1. Create a New Session

```bash
python scripts/manus_session.py send \
  "Analyze Q2 revenue trends and create a summary report" \
  -s q2-analysis --mode agent --tags revenue,q2,analysis
```

### 2. Continue an Existing Session

```bash
python scripts/manus_session.py send \
  "Now break it down by region" -s q2-analysis
```

### 3. Upload File and Attach

```bash
python scripts/manus_session.py upload report.pdf
# Returns file_id

python scripts/manus_session.py send \
  "Summarize this document" -s doc-review --file-id FILE_ID
```

Files expire after 48 hours.

### 4. Organize with Projects

```bash
python scripts/manus_session.py create-project "Research" \
  --instruction "Always cite sources and include confidence levels"

python scripts/manus_session.py send \
  "Research AI agent frameworks" -s agent-research --project proj_abc123
```

---

## Agent Profiles & Task Modes

| Profile           | Use Case                         | Cost     |
|------------------|-----------------------------------|----------|
| `manus-1.6`      | General — balanced quality/speed  | Standard |
| `manus-1.6-lite` | Simple/fast tasks                 | Lower    |
| `manus-1.6-max`  | Complex analysis                  | Higher   |

| Mode       | Behavior                                             |
|-----------|------------------------------------------------------|
| `chat`     | Conversational only                                  |
| `adaptive` | Agent decides when to use tools                      |
| `agent`    | Full agent — browses web, writes code, creates files |

## Connectors

Enable external service access by passing connector UUIDs:
- **Gmail**: `9444d960-ab7e-450f-9cb9-b9467fb0adda`
- **Notion** / **Google Calendar**: configured per account

## Cost Awareness

- ~150 credits per typical task. Use `manus-1.6-lite` + `chat` for simple queries.
- **Always reuse sessions** via `taskId`. Duplicate tasks = wasted credits.
- Check `credit_usage` in task responses to monitor spend.

## Reference Files

| File | When to Read |
|------|-------------|
| `references/session-management.md` | Full session registry design, JSON schema, search/scoring algorithm, archival rules, edge cases |
| `references/api-reference.md` | Exact field schemas for all endpoints, query params, webhook payloads, attachment formats, OpenAI SDK compat |
| `scripts/manus_session.py` | Session-aware Python client — use as library or CLI for all Manus interactions |
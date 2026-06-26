---
name: pa-ownership
version: "1.0.0"
description: "Autonomous task tracking with retry loops and proactive updates. Use when Heleni takes ownership of a task that needs to be tracked, retried on failure, and reported when complete or stuck. Integrates with heartbeat to surface stale tasks."
triggers:
  - "take ownership"
  - "track this"
  - "own this task"
  - "ownership"
  - "add to my tasks"
  - "remind me about"
---

## Load Local Context
```bash
CONTEXT_FILE="/opt/ocana/openclaw/workspace/skills/pa-ownership/.context"
[ -f "$CONTEXT_FILE" ] && source "$CONTEXT_FILE"
# Then use: $OWNER_PHONE, $TASKS_FILE, $WORKSPACE, etc.
```

# PA Ownership Skill

Heleni tracks tasks she owns — executing, retrying when blocked, and closing the loop when done.

---

## When to Use

Trigger phrases:
- "take ownership"
- "track this"
"own this"
- "add to my tasks"
- Any task Heleni explicitly commits to completing

---

## Data File

All tasks are persisted to:
```
/opt/ocana/openclaw/workspace/data/pa-tasks.json
```

### Schema

```json
{
  "tasks": [
    {
      "id": "task_<YYYYMMDD_HHMMSS>",
      "title": "Short task description",
      "description": "Full context / what needs to happen",
      "status": "NEW",
      "initiated_by": "Netanel | group:<jid> | self",
      "created_at": "2026-04-03T10:00:00Z",
      "updated_at": "2026-04-03T10:00:00Z",
      "due_at": null,
      "attempts": 0,
      "max_attempts": 3,
      "last_attempt_at": null,
      "blocked_reason": null,
      "result": null,
      "reported_done": false
    }
  ]
}
```

### Status Values

| Status | Meaning |
|---|---|
| `NEW` | Task received, not yet started |
| `IN_PROGRESS` | Currently executing |
| `DONE` | Completed successfully |
| `BLOCKED` | Cannot proceed — waiting on something |
| `FAILED` | Exhausted all retry attempts |

---

## Step-by-Step Process

### Step 1: Register the Task

When a task is received and Heleni commits to it:

1. **React 👍 immediately** to the owner's message (before starting work)
2. Read `data/pa-tasks.json` (create if missing: `{"tasks": []}`)
3. Generate a task ID: `task_<YYYYMMDD_HHMMSS>`
4. Determine `initiated_by`:
   - DM from Netanel → `"Netanel"`
   - Group message → `"group:<jid>"`
   - Heleni's own initiative → `"self"`
5. Set `status: "NEW"`, `attempts: 0`
6. Write updated JSON back to file
7. Write to WhatsApp memory: `memory/whatsapp/dms/<PHONE-sanitized>/context.md`

### Step 2: Execute

1. Set status to `IN_PROGRESS`, update `updated_at`
2. Execute the task using available tools
3. On success → go to **Step 4 (Done)**
4. On failure → go to **Step 3 (Retry)**

### Step 3: Retry (Blocked / Failed Attempt)

On failure or block:

1. Increment `attempts` counter
2. Record `blocked_reason`
3. Record `last_attempt_at`

**Backoff schedule:**
- Attempt 1 fail → retry after ~5 minutes
- Attempt 2 fail → retry after ~15 minutes
- Attempt 3 fail → mark as `FAILED`, notify Netanel immediately

```
If attempts >= max_attempts:
  → Set status: "FAILED"
  → Report to initiated_by: "❌ [task] failed after 3 attempts: [reason]"
  → Do NOT retry further
Else:
  → Set status: "BLOCKED"
  → Log blocked_reason
  → Schedule retry (via heartbeat or mental note)
```

### Step 4: Mark Done

1. Set `status: "DONE"`, `result: "<outcome summary>"`, `updated_at: now`
2. If `reported_done == false`:
   - **React ✅** to the original task message
   - Report to `initiated_by` with result
   - Set `reported_done: true`
3. Update the JSON file
4. Write outcome to WhatsApp memory file

**Close-the-loop rule:** ALWAYS report back to whoever initiated the task. No exceptions.
- Netanel initiated → send DM to Netanel
- Group initiated → reply in that group
- Self-initiated → log in daily memory

### Step 5: Write to File

After every state change, write the full updated `pa-tasks.json`.

```python
import json, datetime, os

TASKS_FILE = "/opt/ocana/openclaw/workspace/data/pa-tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return {"tasks": []}
    with open(TASKS_FILE) as f:
        return json.load(f)

def save_tasks(data):
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    with open(TASKS_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def update_task_status(task_id, status, **kwargs):
    data = load_tasks()
    for task in data["tasks"]:
        if task["id"] == task_id:
            task["status"] = status
            task["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
            for k, v in kwargs.items():
                task[k] = v
            break
    save_tasks(data)
```

---

## Heartbeat Integration

During every heartbeat, scan for stale tasks:

```
For each task in pa-tasks.json where status IN ["IN_PROGRESS", "BLOCKED"]:
  age = now - updated_at
  
  If age > 2 hours AND NOT reported_stuck:
    → Mark last_notified_at = now
  
  If status == "BLOCKED" AND attempts < max_attempts:
    → Attempt retry
```

Add this block to `HEARTBEAT.md`:
```
## PA Ownership Check
- Scan data/pa-tasks.json for IN_PROGRESS or BLOCKED tasks
- Alert if any task >2h without update
- Retry BLOCKED tasks with remaining attempts
```

---

## HEARTBEAT.md Snippet

When setting up this skill for the first time, add to HEARTBEAT.md:

```markdown
## Task Ownership Check
- Read /opt/ocana/openclaw/workspace/data/pa-tasks.json
- Flag any task with status IN_PROGRESS or BLOCKED updated >2h ago
- Retry BLOCKED tasks if attempts < max_attempts
- Report FAILED tasks to Netanel immediately
```

---

## Alert Format

### Task Stuck Alert (>2h)
```
📋 [task title]
[max_attempts]
```

### Task Complete
```
📝 [result summary]
```

### Task Failed (all retries exhausted)
```
```

---

## Rules

1. **Always close the loop** — when done, always report to whoever initiated it
2. **Never silently fail** — BLOCKED or FAILED always triggers a notification
3. **Max 3 retries** — after that, escalate to Netanel
4. **Persist everything** — every state change is written to pa-tasks.json
5. **Heartbeat integration** — stale tasks surface automatically, no manual polling

---

## Cost Notes

- File reads/writes: cheap — do on every state change
- Retry logic: don't call external APIs in tight loops; space out via heartbeat
- Alert: only send once per "stuck" detection (use `last_notified_at`)

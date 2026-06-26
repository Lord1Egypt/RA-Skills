# Task State Memory

> **Most valuable feature.** Persists across restarts — `hawk resume` continues from where you left off.

---

## Problem Solved

| Pain Point | Solution |
|------------|----------|
| Restarted and forgot where I was | Task state persisted, `hawk resume` recovers |
| Switched session and lost context | `hawk resume` works across any session |
| Keep repeating the same thing | `done_steps` records completed steps |
| Don't know what to do next | `next_steps` makes next action clear |
| No record of what was produced | `outputs` tracks all deliverables |

---

## Data Structure

```json
{
  "task_id": "task_20260329_001",
  "description": "Complete the API documentation",
  "status": "in_progress|pending|completed|blocked",
  "progress": 65,
  "priority": "high|medium|low",

  "steps": [
    {
      "id": 1,
      "description": "Write SKILL.md",
      "status": "completed",
      "done_at": "2026-03-29T00:15:00+08:00"
    },
    {
      "id": 2,
      "description": "Review architecture template",
      "status": "in_progress",
      "blocked_by": null
    },
    {
      "id": 3,
      "description": "Report to user",
      "status": "pending",
      "blocked_by": 2
    }
  ],

  "next_steps": [
    "Review architecture template",
    "Report to user"
  ],

  "outputs": [
    "SKILL.md completed",
    "constitution.md completed",
    "architect.md completed"
  ],

  "constraints": [
    "Coverage must reach 98%",
    "APIs must be versioned"
  ],

  "blockers": [],

  "created_at": "2026-03-29T00:00:00+08:00",
  "updated_at": "2026-03-29T00:20:00+08:00",
  "resumed_count": 3
}
```

---

## Lifecycle Commands

```bash
hawk task "description"        # Create new task (pending)
hawk task --start             # Start/in_progress
hawk task --step 1 done      # Mark step 1 complete
hawk task --next "next step" # Add next action
hawk task --output "file.md"  # Record output
hawk task --block "reason"    # Record blocker
hawk task --done              # Complete task
hawk task --abort             # Abandon task
hawk task --list             # List all tasks
hawk resume                   # Resume last task (most important!)
```

---

## hawk resume — Resume Task

This is the **most important command**. Even after full restart:

```
$ hawk resume

[Context-Hawk] Task Resume

  Task ID:   task_20260329_001
  Desc:      Complete the API documentation
  Progress:  65% (3/5 steps complete)
  Status:    🔄 in_progress

  Completed:
    ✅ 1. SKILL.md completed
    ✅ 2. constitution.md completed
    ✅ 3. architect.md completed

  Current:
    🔄 4. Review architecture template (in progress)

  Pending:
    ⬜ 5. Report to user

  Constraints:
    - Coverage must reach 98%
    - APIs must be versioned

  [Press Enter to continue step 4]
```

---

## Automatic Updates

Task state auto-updates on:

| Trigger | Auto-action |
|---------|------------|
| New file created | Append to `outputs` |
| Decision reached | Append to `outputs` |
| Test failure | Append to `blockers` |
| User provides new requirement | Update `next_steps` |
| User confirms completion | Set `progress = 100%` |

---

## Storage Location

```
memory/.hawk/
├── config.json          # Configuration
├── task_state.jsonl   # Task state (all tasks, JSONL)
├── memories.jsonl      # Structured memories
└── index.json         # Index
```

---

## Multi-Task Management

```bash
hawk task --list                   # List all tasks
hawk task --switch task_20260328_001  # Switch to another task
hawk task --archive                # Archive completed tasks
```

---

## Relationship with Other Features

```
Task State Memory
    │
    ├─── Self-Introspection → reads current task, checks task clarity
    │
    ├─── Compression → does NOT compress task_state.jsonl
    │
    ├─── Injection Strategy → current task always auto-injected (forced)
    │
    └─── Archive → tasks inactive >30 days auto-archived
```

# Taskboard CLI Setup

A lightweight, file-based task management system for multi-agent workflows.

## Task Schema

Tasks are stored in `taskboard.json`:

```json
{
  "tasks": [
    {
      "id": "PROJ-001",
      "title": "Implement user authentication",
      "description": "Add JWT-based auth with refresh tokens",
      "status": "backlog",
      "assignee": "code-engineer",
      "priority": "high",
      "dependencies": [],
      "tags": ["backend", "security"],
      "created": "2026-03-18T00:00:00Z",
      "updated": "2026-03-18T00:00:00Z",
      "adr": "ADR-003",
      "notes": []
    }
  ],
  "meta": {
    "project": "project-name",
    "prefix": "PROJ",
    "nextId": 2
  }
}
```

## CLI Commands

### Create a task
```bash
python3 scripts/taskboard.py create \
  --title "Implement user auth" \
  --assignee code-engineer \
  --priority high \
  --tags backend,security
```

### List tasks
```bash
# All tasks
python3 scripts/taskboard.py list

# Filter by status
python3 scripts/taskboard.py list --status in-progress

# Filter by assignee
python3 scripts/taskboard.py list --assignee tech-lead

# Filter by priority
python3 scripts/taskboard.py list --priority high
```

### Update task status
```bash
python3 scripts/taskboard.py update PROJ-001 --status in-progress
python3 scripts/taskboard.py update PROJ-001 --status review --note "Ready for Tech Lead review"
python3 scripts/taskboard.py update PROJ-001 --status done
```

### Assign task
```bash
python3 scripts/taskboard.py assign PROJ-001 --to code-engineer
```

### Add note to task
```bash
python3 scripts/taskboard.py note PROJ-001 "Found edge case with expired tokens, added test"
```

### View task detail
```bash
python3 scripts/taskboard.py show PROJ-001
```

### Board summary (for cron jobs / Discord posting)
```bash
python3 scripts/taskboard.py summary
```

Output:
```
📋 Project Board: project-name
━━━━━━━━━━━━━━━━━━━━━━━━━━━
📥 Backlog: 3 tasks
🔄 In Progress: 2 tasks (code-engineer: 1, tech-lead: 1)
👀 Review: 1 task
✅ Done (this week): 4 tasks
🚫 Blocked: 0 tasks

🔥 High Priority:
  PROJ-001 [in-progress] Implement user auth (code-engineer)
  PROJ-005 [backlog] Fix payment webhook (unassigned)
```

## Cross-Agent Handoff Protocol

### When Tech Lead completes architecture:
1. `taskboard.py update PROJ-001 --status review --note "ADR written, ready for implementation"`
2. `taskboard.py create --title "Implement: [feature]" --assignee code-engineer --deps PROJ-001`
3. Notify Code Engineer's Discord channel

### When Code Engineer completes implementation:
1. `taskboard.py update PROJ-002 --status review --note "PR #42 ready for review"`
2. Notify Tech Lead's Discord channel for code review

### When review passes:
1. `taskboard.py update PROJ-002 --status done`
2. Check if downstream tasks are unblocked
3. Notify relevant agents

## Cron Integration

### Daily board check (morning)
```
Check taskboard.json for:
1. Tasks in-progress for >3 days (flag as potentially stuck)
2. Blocked tasks (check if blockers are resolved)
3. High-priority unassigned tasks
4. Send summary to #traveler-home Discord channel
```

### Weekly board review (Sunday)
```
Generate weekly report:
1. Tasks completed this week
2. Tasks carried over
3. Velocity trend (tasks done per week)
4. Blocked items needing human decision
```

## Minimum Check Interval

Do not poll the taskboard more frequently than every **5 minutes**.

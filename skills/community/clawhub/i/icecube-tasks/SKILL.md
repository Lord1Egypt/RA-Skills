---
name: icecube-tasks
description: "🧊 IceCube Tasks — Task orchestration and tracking for AI agents. Manage tasks across sessions, track progress, handle blockers, and maintain execution continuity. When users mention 'task management', 'to-do list', 'task tracking', 'project management', 'blockers', 'pending tasks'."
metadata:
  openclaw:
    requires: {}
---

# 🧊 IceCube Tasks

**Tasks that survive session restarts.**

Chat-based task lists die when context compacts. IceCube Tasks lives in files, tracked across sessions.

## What This Skill Does

### 1. Task Persistence
- Tasks stored in `state/tasks/` directory
- Survives context compaction
- Survives session restarts
- Survives agent crashes

### 2. Task Lifecycle
```
inbox → spec → in_progress → blocked → done
                    ↓
                 cancelled
```

### 3. Task Orchestration
- Break down large tasks into subtasks
- Assign to worker agents
- Track completion
- Handle handoffs

### 4. Blocker Management
- Track blockers explicitly
- Link to dependencies
- Auto-escalate stale blockers
- Resume when unblocked

## File Structure

```
state/tasks/
├── current_dispatch.yaml    # What's being worked on NOW
├── current_schedule.yaml    # What's scheduled
├── unclosed_work.yaml       # All open items
├── task_ledger/
│   ├── TASK-001.yaml
│   ├── TASK-002.yaml
│   └── ...
└── completed/
    ├── TASK-000.yaml
    └── ...
```

## Task File Format

**state/tasks/task_ledger/TASK-001.yaml:**
```yaml
id: TASK-001
title: "Publish IceCube Skills to ClawHub"
status: in_progress  # inbox|spec|in_progress|blocked|done|cancelled
created_at: 2026-03-31 01:53 CST
updated_at: 2026-03-31 02:15 CST

# What
description: |
  Create and publish IceCube Skills series to ClawHub marketplace.
  
# Why
context: |
  Boss wants to explore creating tools and selling them.
  AI agent memory is an underserved market.
  
# How
steps:
  - id: STEP-1
    task: "Create icecube-memory skill"
    status: done
    completed_at: 2026-03-31 01:53 CST
  - id: STEP-2
    task: "Create icecube-heartbeat skill"
    status: done
    completed_at: 2026-03-31 01:53 CST
  - id: STEP-3
    task: "Create icecube-evolution skill"
    status: done
    completed_at: 2026-03-31 01:53 CST
  - id: STEP-4
    task: "Create icecube-reddit-scout skill"
    status: done
    completed_at: 2026-03-31 02:08 CST
  - id: STEP-5
    task: "Publish to ClawHub"
    status: blocked
    blocked_reason: "GitHub account needs 14 days age"
    blocked_until: 2026-04-10

# Dependencies
depends_on: []
blocks: []

# Assignment
assigned_to: main_agent  # main_agent|worker_1|user

# Priority
priority: high  # critical|high|medium|low
deadline: null

# Success Criteria
success_criteria:
  - All 4 skills published to ClawHub
  - Skills are installable by users
  - Documentation is complete

# Metadata
tags: [skills, clawhub, monetization]
estimated_effort: 2h
actual_effort: 1h

# History
history:
  - timestamp: 2026-03-31 01:53 CST
    event: created
  - timestamp: 2026-03-31 01:53 CST
    event: step_completed
    step: STEP-1
  - timestamp: 2026-03-31 02:10 CST
    event: blocked
    reason: "ClawHub requires 14-day-old GitHub account"
```

## Commands

### Create Task
```yaml
# Write to state/tasks/task_ledger/TASK-XXX.yaml
id: TASK-XXX
title: "Task title"
status: inbox
created_at: <now>
```

### Start Task
```yaml
# Update task file
status: in_progress
updated_at: <now>
assigned_to: <agent>

# Update current_dispatch.yaml
focused_task: TASK-XXX
```

### Block Task
```yaml
# Update task file
status: blocked
blocked_reason: "Why blocked"
blocked_until: "When it might be resolved"
updated_at: <now>

# Update unclosed_work.yaml
- Add blocker note
```

### Complete Task
```yaml
# Update task file
status: done
completed_at: <now>

# Move to completed/
# Update current_dispatch.yaml
focused_task: null
```

## Orchestration Patterns

### Pattern 1: Sequential
```
TASK-001 → TASK-002 → TASK-003
```
Each task blocks the next.

### Pattern 2: Parallel
```
TASK-001 ─┬→ TASK-003
TASK-002 ─┘
```
TASK-003 depends on both.

### Pattern 3: Delegated
```
main_agent → worker_agent (TASK-001)
          → worker_agent (TASK-002)
```
Subagents execute parallel tasks.

### Pattern 4: User-Blocked
```
TASK-001 → [waiting for user] → TASK-001 continues
```
Agent can't proceed without user input.

## Anti-Patterns

❌ **Don't:**
- Create tasks without writing to files
- Update status in chat only
- Forget about blocked tasks
- Leave tasks in limbo

✅ **Do:**
- Write every task to a file
- Update status immediately
- Check blockers regularly
- Close tasks explicitly

## Integration with IceCube Suite

**icecube-heartbeat:** Checks for stale tasks during heartbeat
**icecube-evolution:** Failed tasks feed improvement queue
**icecube-memory:** Task context loaded on startup

## Task Recovery

If agent crashes or restarts:

1. Read `state/tasks/current_dispatch.yaml`
2. Find `focused_task`
3. Read task file from `task_ledger/`
4. Resume from last completed step

## Metrics

**Track in state/tasks/metrics.yaml:**
```yaml
total_created: 47
total_completed: 42
total_cancelled: 3
currently_open: 5
avg_completion_time: 2.3h
blocker_rate: 15%
```

## License

MIT — Use freely.

---

*Tasks in files survive. Tasks in chat die.*
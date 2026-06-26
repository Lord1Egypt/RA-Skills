---
name: multi-topic-board
description: "Multi-Topic Board: AI Agent active topic tracking and task closed-loop management. Tracks unresolved discussions, auto-updates aging days, sends timeout alerts after 3 days with no task, and generates execution tasks in tasks/. Triggered when: (1) user discusses a topic without conclusion; (2) user asks where things left off; (3) user wants to track pending decisions."
license: MIT-0
version: "1.0"
stage: "beta"
---

# Multi-Topic Board v1.0

## What This Skill Does

**Not a notepad — an execution accelerator.**

Multi-Topic Board solves the "discussed then forgotten" problem. Discussions generate unresolved topics that never reach the execution layer. The board chains two Cron systems with tasks/ into a closed loop: track → remind → create task → complete.

---

## When to Use This Skill

- User discusses a topic without reaching a conclusion
- User asks "where did we leave off?" or "what's pending?"
- User wants to track pending decisions across sessions
- A topic has been active for 3+ days without an execution task

---

## Architecture

```
🔥 Pending ──[3+ days, no task]──→ Cron notifies main
    │                                    ↓
    │                          main decides: create task?
    ↓                                    ↓
🔄 Parked                          tasks/ file created
    │                                    ↓
    ↓                                    ↓
✅ Done ←─────────────────────── task done, board updated
```

**Two trigger Cron systems**:
- **Heartbeat Cron** (every 4 hours): state sync + timeout reminder
- **System Maintenance Cron** (daily): update aging days + timeout stats
- **Main Agent**: decides whether to create task, manually links task path to board

---

## Entry Format

Each entry in the board:
```markdown
- [ ] [Topic] Description | YYYY-MM-DD | source | X days | task: filename.md or none
```

| Field | Description | Who fills |
|-------|-------------|-----------|
| YYYY-MM-DD | Discovery date, auto-recorded | Agent |
| days | Days since discovery, auto-updated | System (Cron) |
| task | File path when task exists | Manual |

---

## Status Flow

| Status | Meaning | Trigger |
|--------|---------|---------|
| 🔥 Pending | Topic open, no conclusion | User raises new topic |
| 🔄 Parked | Temporarily on hold | User says "暂缓" / "hold" |
| ✅ Done | Concluded or closed | Has conclusion + write result |

---

## Bootstrap Setup

When this skill is first loaded, set up the closed-loop infrastructure:

### Step 1: Create tasks/ Directory

```bash
mkdir -p tasks/
```

Tasks directory stores execution task files. When main decides to act on a pending topic, create a task file here and manually link it back to the board entry.

### Step 2: Setup Multi-Topic Board

Check if `HEARTBEAT.md` exists in workspace:
- **IF exists**: Write new task items into the existing file (do not overwrite existing content)
- **IF not exists**: Create `HEARTBEAT.md` as a new cron job

**Create Multi-Topic Board File** (`memory/multi-topic.md`):
```markdown
# Multi-Topic Board

> Track active topics and unresolved pending items.
> Both agent and user can update; Heartbeat syncs automatically.

**State Flow**:
🔥 Pending → 🔄 Parked → ✅ Done

**Closed-Loop Mechanism**:
- Heartbeat Cron syncs state changes
- System Maintenance Cron updates aging days
- 3+ days with no task → notifies main to create task in tasks/
- After task created → manually link file path to entry

**Usage**:
- User starts a topic → append to 🔥 Pending
- User says "hold" → move topic to 🔄 Parked
- Has conclusion → move to ✅ Done + write conclusion
- User asks "where did we leave off?" → read this file

**Format**:
- Aging days: updated daily by System Maintenance Cron
- Task link: fill in after creating task file

---
## 🔥 Pending

## 🔄 Parked

## ✅ Done
```

### Step 3: Setup or Update Heartbeat Cron

**IF HEARTBEAT.md already exists**:
- Read the existing file
- Add this task to the existing Heartbeat workflow (do not overwrite):
  > Multi-Topic Board Sync
  > - Read `memory/multi-topic.md`
  > - Inject active topics into context
  > - Sync state changes
  > - Identify topics 3+ days with no task; report in main notification

**IF HEARTBEAT.md does not exist**, create a new cron job:

```json
{
  "schedule": { "kind": "every", "everyMs": 14400000 },
  "payload": {
    "kind": "agentTurn",
    "message": "【Multi-Topic Board Sync】\n\nStep 1: Read sessions_list (filter noise sessions)\n\nStep 2: Read memory/multi-topic.md\n- Inject active topics into context\n- Sync state changes\n\nStep 3: Identify timed-out topics\n- Find topics 3+ days with task = none\n- IF > 0 → sessions_send to main: list timed-out topics, suggest creating tasks in tasks/\n"
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "none" }
}
```

Every 4 hours (14400000ms).

### Step 4: Setup System Maintenance Cron

```json
{
  "schedule": { "kind": "every", "everyMs": 86400000 },
  "payload": {
    "kind": "agentTurn",
    "message": "【Daily Multi-Topic Board Maintenance】\n\nStep 1: Update aging days\n- Read memory/multi-topic.md\n- For each 🔥 Pending entry: today - discovered_at = days\n- IF no days field → append to entry\n- IF days changed → update in place\n- Write back to multi-topic.md (only touch the days field)\n\nStep 2: Timeout stats and alert\n- Count entries: days >= 3 AND task = none\n- IF > 0 → sessions_send to main: N topics 3+ days with no task: [topic names]\n- IF = 0 → silent end\n"
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "none" }
}
```

Daily.

### Step 5: Link Task to Board

After creating any task file, update the corresponding board entry in `memory/multi-topic.md`:
- Change `task: none` to `task: tasks/your-task-file.md`

---

## File Locations

| File | Purpose |
|------|---------|
| `memory/multi-topic.md` | Multi-Topic Board main file |
| `HEARTBEAT.md` | Heartbeat cron payload (if skill creates it) |
| `tasks/*.md` | Execution task files |

---

## Design Principles

1. **Minimal intervention**: No separate hook needed; embedded in existing cron workflows
2. **Auto flow**: Aging days and state sync maintained by cron
3. **Proactive alerts**: Only alert after 3+ days with no task; no spam
4. **One-way feedback**: Task done → board updated; board updated → does NOT auto-create task (main decides)
5. **Manual bridge**: Task path is a manual bridge — the human's judgment must not be stolen by the system

---

## Usage Scenarios

### Scenario 1: Auto-append New Topic
User discussion produces unresolved topic → Agent appends to 🔥 Pending

### Scenario 2: Timeout Auto-alert
days >= 3 AND task = none → Cron notifies main → Suggest creating task in tasks/

### Scenario 3: Task Completion Closed-loop
tasks/ file completed → Agent manually links path to board → Moves to ✅ Done

### Scenario 4: Progress Query
User asks "where did we leave off?" → Read board to user

---

## Usage Boundaries

**Suitable for**:
- Unresolved topics from user discussions
- Decisions needing tracking but not immediate execution
- Multi-session coordinated long-cycle tasks

**Not suitable for**:
- Tasks with clear execution plans (go directly to tasks/)
- One-time information queries (no tracking needed)
- Topics user explicitly says "不需要管"

---

*Multi-Topic Board v1.0 — Every unresolved topic gets a landing place*
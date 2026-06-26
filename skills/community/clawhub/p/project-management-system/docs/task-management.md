# Task Management Mechanism

> Task state machine, claim anti-duplication, dependency management, pre-write conflict detection.

---

## Task State Machine

_Source: A2A Protocol Task Lifecycle + Practice Precipitation_

Each task has and only has the following states, state transitions have strict guard conditions:

```
Pending Dispatch → In Progress → Pending Review → Accepted
                      ↓
                    Rework → Pending Review (Loop)
                      ↓ (Exceeds 3 rounds)
                   Abandoned → Replacement Task (New)

Special States:
Pending Dispatch → Cancelled (When project cancelled)
In Progress → Paused (When project paused)
Paused → In Progress (When project resumes, may change executor)
In Progress → Blocked (Waiting for input/dependency/Decision Maker confirmation)
Blocked → In Progress (After block resolved)
```

### Status Transition Guard Conditions

| Transition | Guard Condition (Must be met to transition) | Who Triggers |
|------|---------------------------|--------|
| Pending Dispatch → In Progress | Prerequisite dependencies ready + Project check-in sheet no conflict + Executor assigned | Dispatcher |
| In Progress → Blocked | Executor reports blocking reason | Executor feedback |
| Blocked → In Progress | Blocking reason resolved | Dispatcher confirmation |
| In Progress → Pending Review | Output file exists at specified location | Executor delivery |
| Pending Review → Accepted | review-record exists and conclusion is "pass" | Dispatcher |
| Pending Review → Rework | review-record exists and conclusion is "fail" | Dispatcher |
| Rework → Pending Review | Modification complete + Output file updated | Executor re-delivery |
| Rework (3rd round) → Abandoned | Provide 3 rounds of records + stuck reason + alternative plan | Dispatcher escalation |

**Violating guard condition = Invalid status transition.** For example: Output file doesn't exist cannot be marked as "Pending Review".

## Task Dependency Management

- Each task-spec has "Dependency" field, marking prerequisite and subsequent dependencies
- Dispatch according to dependency order: Prerequisite not complete → Subsequent not dispatched
- Tasks without dependencies can be dispatched in parallel
- After prerequisite completes, immediately check and dispatch subsequent tasks

**Dependency Status:**
- Ready — Prerequisite accepted, output available
- Not Ready — Prerequisite not complete, waiting

## Circular Dependency Detection

- After breaking down all tasks, draw dependency graph to check for cycles
- Starting from each task, walk along dependency chain, returning to self means cycle
- Find cycle → Re-break down, break the cycle
- Before dispatch confirm again: All "Pending Dispatch" tasks' prerequisites are either ready or have no dependency

## Task Nesting (Subtask Breakdown)

- Large tasks can be broken down into subtasks
- Naming: `TASK-003a`, `TASK-003b` (letter after parent number)
- Subtasks each have independent task-spec
- Parent task status depends on subtasks: All accepted → Parent accepted
- Maximum two levels of nesting, more than that means breakdown granularity has problems

## Prevent Duplicate Dispatch

- **Must check task status before dispatch** — Already "In Progress" or later status, don't dispatch again
- When dispatching, immediately update status to "In Progress", write communication record with communication identifier
- After restart recover context:
  1. Run dashboard.py to view all task statuses
  2. "In Progress" → Check communication identifier in communication record, try to contact to confirm progress
  3. Cannot contact → Handle according to exception handling process (see `scheduling.md`)

## Task Claim Mechanism

**Background:** From real incident — Two agents' subagents simultaneously transcribed the same video, producing duplicate files.

**Mechanism:** Each project directory has its own `task-registry.md` (project-level check-in sheet), recording tasks currently executing in this project. Check-in sheet is a project-internal anti-duplication mechanism, not a cross-project global lock. Cross-project anti-duplication relies on Dispatcher's scheduling responsibility.

**Rules:**
- Each task assigned unique ID (TASK-001, TASK-002...)
- Before starting, check project check-in sheet — Same task already claimed and not expired → Don't execute duplicate
- When claiming, write: Task ID, Claimer, Status, Start Time, Expiration Time, Output Location
- Status flow: `Claiming → In Progress → Completed / Released`
- Expiration mechanism: Default 2 hours, customizable. After expiration others can take over (mark as "taking over")
- Completed records can be cleaned up after 24 hours

**Dispatcher Responsibility:** Register during dispatch, update when complete, periodically clean up.

**Check-in Sheet Format (task-registry.md under project directory):**

```markdown
# Task Check-in Sheet

> Project data file — Normal read/write, no approval needed

| Task ID | Claimer | Status | Start Time | Expiration Time | Output Location | Notes |
|--------|--------|------|----------|----------|----------|------|
| TASK-001 | Forge | In Progress | 03-21 10:00 | 03-21 12:00 | tasks/ | |
```

Status values: `Claiming` / `In Progress` / `Paused` / `Completed` / `Released`

## Pre-Write Conflict Detection

Before writing files to project directory, must do three-step check:

1. **File Existence** — Already exists → Compare content, same skip, different rename and save
2. **Check-in Sheet Check** — Check project check-in sheet, someone is doing same task → Don't start, feedback to Dispatcher
3. **Content Similarity** — Highly similar file in target directory → Pause, feedback to confirm

**Principle: Better to ask once more than produce duplicate files.**

## Parallel Task Limit

- Same executor maximum **2** in-progress tasks (hard limit)
- Same project maximum **5** parallel in-progress tasks
- Exceed → Queue wait, status stays "Pending Dispatch"
- Urgent tasks not limited by this, but will pause low-priority tasks
- Queue strategy: High priority dequeues first, same priority first-in-first-out

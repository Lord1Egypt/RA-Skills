# Task Autonomy & Self-Expansion

> **Enable true autonomous operation with self-expanding task lists**
> Priority: CRITICAL | Category: Operations

## Overview

A common failure mode: agent completes one task, then sits idle waiting for instructions. This skill enables true autonomy through self-expanding task lists that grow organically as work progresses.

## The Problem

```yaml
typical_failure:
  scenario: "User assigns multi-step task at midnight"
  expectation: "Agent completes all steps overnight"
  reality: "Agent completes step 1, then stops"
  result: "User wakes to 20% completion, agent idle for hours"
```

## The Solution: Living Task Systems

### Task Autonomy Principles

1. **Tasks Beget Tasks**: Completing a task reveals subtasks
2. **Continuous Discovery**: Work uncovers new work
3. **Self-Selection**: Agent picks next task without prompting
4. **Organic Growth**: Todo list expands and contracts naturally

### The Autonomous Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS CYCLE                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   1. SELECT → Pick highest-priority incomplete task         │
│   2. EXECUTE → Apply execution-discipline cycle             │
│   3. DISCOVER → Identify new tasks from work                │
│   4. ADD → Append discovered tasks to Todo.md                │
│   5. UPDATE → Mark current task status                      │
│   6. REPEAT → Return to step 1                              │
│                                                              │
│   Exit conditions:                                           │
│   - All tasks complete                                       │
│   - Blocked (escalate)                                       │
│   - Cron job ends session                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Todo.md Structure

### Required Sections

```markdown
# Todo.md

## Last Updated
**Timestamp**: [ISO 8601]
**Agent**: [Agent Name]
**Session**: [Session ID]

## Task Statistics
- Total: [N]
- Pending: [N]
- In Progress: [N]
- Completed: [N]
- Blocked: [N]

## Active Tasks [PRIORITY: HIGH]

### [T-001] [Task Title]
**Status**: pending | in_progress | completed | blocked
**Priority**: critical | high | medium | low
**Assigned**: [Agent Name]
**Created**: [Timestamp]
**Updated**: [Timestamp]

**Description**: [Clear, actionable description]

**Definition of Done**:
- [ ] [Specific criteria 1]
- [ ] [Specific criteria 2]
- [ ] [Specific criteria 3]

**Dependencies**: [T-000] (or 'none')
**Blocks**: [T-002, T-003] (or 'none')

**Subtasks**: [T-001A, T-001B] (or 'none')

**Progress Notes**:
- [YYYY-MM-DD HH:MM] [Note]
- [YYYY-MM-DD HH:MM] [Note]

## Pending Tasks [PRIORITY: MEDIUM]
[Same structure as above]

## Backlog [PRIORITY: LOW]
[Same structure as above]

## Completed Today
### [T-XXX] [Task Title] - Completed at [HH:MM]
[Brief summary of what was done]

## Blocked Tasks
### [T-XXX] [Task Title] - Blocked since [HH:MM]
**Blocker**: [Description]
**Action Required**: [What needs to happen]
```

## Task Selection Algorithm

### Priority Matrix

```python
def select_next_task(todo_list):
    """
    Select the next task to work on based on priority,
    dependencies, and agent capacity.
    """
    candidates = []

    for task in todo_list.pending_tasks:
        # Skip blocked tasks
        if task.status == 'blocked':
            continue

        # Skip tasks with incomplete dependencies
        if not all(dep.status == 'completed' for dep in task.dependencies):
            continue

        # Score each task
        score = calculate_task_score(task)
        candidates.append((score, task))

    # Return highest scored task
    if candidates:
        return sorted(candidates, reverse=True)[0][1]
    return None

def calculate_task_score(task):
    """
    Higher score = higher priority
    """
    score = 0

    # Priority base score
    priority_scores = {
        'critical': 1000,
        'high': 500,
        'medium': 100,
        'low': 10
    }
    score += priority_scores.get(task.priority, 0)

    # Age bonus (older tasks get slight boost)
    age_hours = (now - task.created).hours
    score += min(age_hours * 0.5, 50)  # Max +50 for age

    # Subtask penalty (prefer parent tasks first)
    if task.is_subtask:
        score -= 25

    # Completion momentum bonus (if related tasks completed)
    completed_siblings = sum(1 for t in task.siblings if t.status == 'completed')
    if completed_siblings > 0:
        score += completed_siblings * 10

    return score
```

## Task Discovery Patterns

### Pattern 1: Decomposition

When receiving a complex task:

```yaml
trigger: "Task estimate > 2 hours OR > 3 logical steps"
action: "Break into subtasks"

example:
  original: "Implement user authentication system"

  decomposed:
    - T-001A: "Research authentication options"
    - T-001B: "Design authentication architecture"
    - T-001C: "Implement login endpoint"
    - T-001D: "Implement token validation"
    - T-001E: "Write authentication tests"
    - T-001F: "Update documentation"

  rule: "Each subtask should be independently completable"
```

### Pattern 2: Discovery During Execution

When working reveals new requirements:

```yaml
trigger: "Work uncovers prerequisite or follow-up work"
action: "Add new task immediately"

example:
  working_on: "T-005: Add user profile endpoint"
  discovery: "Need email validation library"
  action: "Add T-005A: Install and configure email validator"
  relationship: "T-005A blocks T-005"
```

### Pattern 3: Error-Driven Discovery

When errors reveal systemic issues:

```yaml
trigger: "Error indicates missing foundational work"
action: "Create task for root cause, block current task"

example:
  working_on: "T-010: Add feature X"
  error: "Database schema doesn't support required query"
  action:
    - Create T-010A: "Update database schema for feature X"
    - Mark T-010 blocked by T-010A
    - Switch to T-010A
```

### Pattern 4: Testing Discovery

When tests reveal missing work:

```yaml
trigger: "Test failure reveals unimplemented edge case"
action: "Add task for edge case"

example:
  testing: "T-020: Input validation"
  discovery: "Null input not handled"
  action: "Add T-020A: Handle null edge case in validation"
```

### Pattern 5: Documentation Discovery

When documentation reveals missing features:

```yaml
trigger: "Docs describe feature not implemented"
action: "Add task for missing feature"

example:
  reading: "API documentation"
  discovery: "Docs mention rate limiting, not implemented"
  action: "Add T-030: Implement rate limiting"
```

## Task Lifecycle States

```yaml
task_states:
  pending:
    description: "Ready to start, no blockers"
    next_action: "Select and execute"

  in_progress:
    description: "Currently being worked on"
    next_action: "Continue execution cycle"
    rule: "Only one task in this state at a time"

  completed:
    description: "All definition of done items met"
    next_action: "Select next task"
    rule: "Move to 'Completed Today' section"

  blocked:
    description: "Cannot proceed due to dependency"
    next_action: "Work on unblocking task"
    rule: "Must specify blocker and required action"

  cancelled:
    description: "No longer needed"
    next_action: "Remove from active tracking"
    rule: "Document cancellation reason"
```

## Autonomous Session Flow

### Overnight Work Example

```yaml
22:00 - User assigns: "Add user authentication"
22:01 - Agent receives task
22:02 - Agent decomposes into 6 subtasks
22:03 - T-001A: Research authentication options
23:45 - T-001A: Complete, discovers need for security review
23:46 - T-001A1: Security assessment of options [ADDED]
23:50 - T-001A1: Complete
23:51 - T-001B: Design architecture

02:00 - CRON: Wake up, check Todo.md
02:01 - Resume T-001B (in progress)
02:45 - T-001B: Complete
02:46 - T-001C: Implement login endpoint
04:00 - CRON: Wake up, check Todo.md
04:01 - Resume T-001C (in progress)
04:30 - T-001C: Complete, discovers missing test library
04:31 - T-001C1: Install test library [ADDED]
04:35 - T-001C1: Complete
04:36 - T-001D: Implement token validation
06:00 - CRON: Wake up, check Todo.md
06:01 - Resume T-001D (in progress)
06:45 - T-001D: Complete
06:46 - T-001E: Write tests
07:30 - All tasks complete
07:31 - Generate completion summary
07:32 - Return to idle state

08:00 - User wakes to complete authentication system
```

## Quality Checks

### Before Marking Task Complete

```yaml
completion_checklist:
  definition_of_done:
    - "All criteria in task description met"
    - "Tests passing (if applicable)"
    - "Documentation updated (if applicable)"
    - "No regressions introduced"

  cleanup:
    - "No temporary/debug code left"
    - "No commented-out code"
    - "Git commit made (if applicable)"
    - "Task status updated"

  follow_through:
    - "Discovered tasks added to Todo.md"
    - "Dependencies marked as resolved"
    - "Blocking tasks notified"
    - "Progress logged in progress-log.md"
```

### Before Starting Task

```yaml
readiness_checklist:
  prerequisites:
    - "All dependencies complete"
    - "No blockers active"
    - "Required resources available"
    - "Context understood"

  scope:
    - "Definition of done clear"
    - "Time estimate reasonable"
    - "No ambiguity in requirements"

  capacity:
    - "Agent has required permissions"
    - "Required tools available"
    - "Model appropriate for task"
```

## Anti-Patterns

### ❌ Task Explosion
```yaml
pattern: "Creating hundreds of tiny tasks"
problem: "Overhead exceeds work value"
solution: "Group related work into meaningful units"
threshold: "No task < 5 minutes estimated"
```

### ❌ Orphan Tasks
```yaml
pattern: "Creating subtasks without linking to parent"
problem: "Lost context, unclear priority"
solution: "Always specify parent/child relationships"
rule: "Every subtask has 'Parent: T-XXX'"
```

### ❌ Zombie Tasks
```yaml
pattern: "Tasks stuck in 'in_progress' for days"
problem: "Agent moved on, task never closed"
solution: "Auto-stale after 4 hours, require review"
rule: "Mark stale, don't leave in progress"
```

### ❌ Priority Inversion
```yaml
pattern: "Working on low-priority while high-priority waits"
problem: "Wrong task selection algorithm"
solution: "Always score by priority first"
rule: "Critical tasks always before low priority"
```

## Cron Integration

```bash
# Overnight work cycles
openclaw cron add --name "overnight-2am" \
  --cron "0 2 * * *" \
  --message "Check Todo.md. Pick up incomplete or in-progress tasks. Continue work. Log progress."

openclaw cron add --name "overnight-4am" \
  --cron "0 4 * * *" \
  --message "Check Todo.md. Update progress-log. Continue highest priority task."

openclaw cron add --name "overnight-6am" \
  --cron "0 6 * * *" \
  --message "Final check. Summarize all overnight work. Mark complete tasks."
```

## Verification

After implementing this skill:

```bash
# Check task autonomy
openclaw test autonomy --scenario "multi-step-task"

# Verify task discovery
openclaw logs last --check "discovered.*task"

# Check overnight progress
diff Todo.md.22:00 Todo.md.06:00
```

## Key Takeaway

**A task list is a living organism, not a static document.** The agent should discover, create, and complete tasks autonomously while you sleep.

---

**Related Skills**: `execution-discipline.md`, `progress-logging.md`, `cron-orchestration.md`

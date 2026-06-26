# Task Layer Guide

## What is a Task?

A task is a unit of work with a clear owner and a clear state.

Not everything is a task. Meeting notes, decisions, reference material — these are not tasks.

## Task Properties

**Must have:**
- Title (what)
- Status (open/in-progress/done/waiting)
- Owner (whose job is this)

**Nice to have:**
- Created date
- Follow-up actions
- Waiting on (what's blocking)
- Done date

## Status Conventions

| Status | Meaning | Trigger |
|--------|---------|---------|
| `[ ]` Open | Not started, not being worked | Task created |
| `[p]` In Progress | Being worked on | Work started |
| `[w]` Waiting | Blocked by something | Dependency not met |
| `[d]` Done | Completed | Work finished |

## Task Examples

### Simple Task
```markdown
- [ ] Review API documentation
```

### Detailed Task
```markdown
- [p] Write unit tests for auth module
  - Created: 2026-03-25
  - Waiting on: auth module PR #42
  - Follow-up: Update API docs after tests pass
```

## Task vs Not Task

| Not a Task | Is a Task |
|-------------|-----------|
| Reference material | Single action item |
| Meeting notes | Something you can mark done |
| Decision | Something with a clear next action |
| Idea | Something with a deadline |
| Project | Single step in a project |

## Task Ownership

If it's your task, it's in your TODO.

If it's someone else's task, it shouldn't be in your TODO — track it as a waiting-on, not a task.

## Task Aging

Open tasks that haven't been touched in 7 days should be:
- Reviewed for relevance
- Updated if still valid
- Removed if no longer needed

Started tasks that have been "in progress" for more than 3 days without updates are stale. Surface them in review.

## Task Patterns

### Stale Open Task
```
- [ ] Old task that hasn't been touched
  → Surface in review, decide: still valid or prune?
```

### Waiting Task
```
- [w] Waiting on legal review
  → Who owns the legal review?
  → Is there a deadline?
```

### Blocked Task
```
- [w] Blocked by: API not ready
  → Can I work around it?
  → Should I downgrade the priority?
```

## Task Review Questions

During review:
1. Which open tasks are stale?
2. Which in-progress tasks have been stuck?
3. Which waiting tasks can be unblocked?
4. Which tasks should be pruned?

## Task System Integration

Tasks connect to other modules:
- **Decision follow-ups** → Tasks
- **Review findings** → Tasks
- **Routing triage** → Tasks
- **Execution records** → Task updates

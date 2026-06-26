---
name: orchestrator
description: Routes work to the correct specialist skill. Enforces gates: one ticket at a time, artifact-first, stop when done. Delegates instead of executing.
---

# orchestrator

## When to use
- New session start: unclear next action
- Multiple tasks exist; need exactly one next step
- After a run: choose the next handoff
- Blocker occurred: route to escalation

## Reads
- workspace/CONTEXT.md
- workspace/TASKS.md
- workspace/NEXT_TICKET.md (optional)
- workspace/BLOCKED_STATE.json (optional)
- workspace/worklog.md (optional)

## Writes
- workspace/NEXT_AGENT.md
- workspace/NEXT_TICKET.md (if missing)
- workspace/worklog.md (append)

See: `instructions.md`

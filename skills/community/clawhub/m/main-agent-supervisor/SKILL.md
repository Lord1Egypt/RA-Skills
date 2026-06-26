---
name: main-agent-supervisor
description: Supervise a main agent so it defaults to execution, suppresses obvious permission loops, and escalates to the user only for true approvals or critical ambiguity. Use when designing, running, or auditing a reviewer/gatekeeper/coaching layer for agent replies, approval policy, escalation logic, anti-stuck behavior, or supervisor-style chat/output filtering.
---

# Main Agent Supervisor

This skill is for a **supervisor layer over a main agent**, not a generic task tracker.

## Goal

Prevent the main agent from getting stuck on obvious decisions while still preserving real human control for risky or ambiguous actions.

## Core design

Use a four-part model:

1. **Classifier**
   - Decide whether a pending ask/action is:
     - `AUTO`
     - `CONFIRM`
     - `ESCALATE`

2. **Pre-send gate**
   - Before the main agent sends a user-visible reply, ask:
     - Is this asking for an obvious decision?
     - Is there a safe default?
     - Is the agent permission-looping?
   - If yes, suppress the question and continue execution.

3. **Triage / watchdog**
   - Borrowing from `claude-code-supervisor`, classify agent state into:
     - `FINE`
     - `NEEDS_NUDGE`
     - `STUCK`
     - `DONE`
     - `ESCALATE`
   - Use a lightweight pre-filter for obvious cases before invoking heavier review.

4. **Task-state tracking for large tasks**
   - Borrowing from `task-supervisor`, keep simple checkpoint files for long tasks.
   - Track:
     - started time
     - status
     - completed steps
     - last updated
     - current blocker / next step

## Use this policy

### AUTO
Proceed without bothering the user when all are true:
- internal / local action
- reversible or low-risk
- no external send/publish
- no payment / secret / production change
- user intent is already clear
- there is one reasonable default

### CONFIRM
Ask the user when any are true:
- external send/publish
- destructive / irreversible action
- money / orders / account changes
- production/live-system changes
- privacy / compliance / legal sensitivity

### ESCALATE
Ask only when blocked after reasonable retries or when multiple materially different paths exist.

## Reply-shaping rules

When the main agent drafts a question, rewrite it if:
- it is merely asking permission for an AUTO action
- it asks for a trivial preference that has a safe default
- it proposes extra scope that is obviously worth trying and reversible

Preferred rewrite:
- state the chosen default
- continue execution
- mention assumptions briefly if needed

For larger tasks, pair this with a task-state file instead of ad-hoc check-in messages. That preserves progress visibility without interrupting the user for obvious decisions.

## Best current pattern

For this workspace, the best practical setup is:
- **escalation classifier** as the core policy
- **pre-send gate** as enforcement
- **triage/watchdog** for stuck detection
- **task-state files** for large tasks
- **passive reviewer/audit log** for tuning

## References

Read these when needed:
- `references/design.md` — recommended architecture and message flow
- `references/comparison.md` — what existing public skills cover vs what they miss
- `references/implementation.md` — workspace-specific OpenClaw implementation plan

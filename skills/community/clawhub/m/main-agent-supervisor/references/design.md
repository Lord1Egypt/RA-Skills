# Supervisor Design

## Problem statement
Main agents often ask the user for decisions that are already obvious, especially around safe internal actions. This creates permission loops and makes the agent feel timid or stuck.

## Desired behavior
- default to execution for low-risk internal work
- reserve user attention for genuine approvals
- coach the main agent when hesitation is unnecessary
- keep a lightweight audit trail for tuning

## Recommended architecture

### Layer 1: Action classifier
Input:
- current task
- pending action
- draft reply
- risk/context flags

Output:
- `AUTO`
- `CONFIRM`
- `ESCALATE`

### Layer 2: Pre-send gate
Before any user-visible reply, determine whether the draft is:
- a valid escalation
- a true approval request
- a lazy/obvious proceed-question

If it is a lazy proceed-question, convert it into:
- default assumption(s)
- recommended next action
- continue execution

### Layer 3: Triage / watchdog
Borrow the useful pattern from `claude-code-supervisor`:
- use a cheap pre-filter for obvious cases
- classify the agent state into:
  - `FINE`
  - `NEEDS_NUDGE`
  - `STUCK`
  - `DONE`
  - `ESCALATE`

This gives the supervisor a second job beyond reply gating: detect when the main agent is spinning, prematurely stopping, or silently failing.

### Layer 4: Task-state tracking
Borrow the useful pattern from `task-supervisor` for larger tasks:
- keep a lightweight task file
- update status after each meaningful step
- preserve current step, blockers, and last update time

This reduces pressure to ask the human for progress-confirmation and makes pause/resume much easier.

### Layer 5: Coach output
When the main agent stalls, emit:
- `defaults_used`
- `assumptions`
- `recommended_next_action`
- `one_question_if_needed`

## Suggested emitted fields
- `decision_class`: `AUTO | CONFIRM | ESCALATE`
- `triage_class`: `FINE | NEEDS_NUDGE | STUCK | DONE | ESCALATE`
- `worth_trying`: `true | false`
- `assumptions`: []
- `defaults_used`: []
- `recommended_next_action`: string
- `one_question_if_needed`: string | null
- `reasoning_summary`: short string
- `task_state_path`: string | null

## Worth-trying heuristic
Treat a next step as AUTO if all are true:
- low cost (roughly <= 30 minutes or <= 5 concrete steps)
- reversible
- no external send/publish
- no secret write
- no production/live risk
- no destructive large batch action

## Anti-stuck triggers
Intervene when the main agent:
- asks “should I proceed?” for an AUTO action
- repeats a question in different wording
- stops after one trivial step
- escalates before trying reasonable alternatives
- over-focuses on low-impact ambiguity

## Good escalation format
If escalation is truly needed, keep it to:
1. situation
2. what was tried
3. recommended default
4. one compact question

# Workspace Implementation Plan

Use this skill in the current OpenClaw workspace with a phased design.

## Verified platform pieces

Observed on this machine:
- `openclaw hooks` exists and can list/install/manage hook packs
- `openclaw cron` exists for exact scheduled jobs
- `openclaw sessions` exists
- current bundled hooks include:
  - `boot-md`
  - `bootstrap-extra-files`
  - `command-logger`
  - `session-memory`

## Important current limitation

A built-in hook that directly intercepts every outgoing main-agent user reply before send is **not yet verified**.

So the implementation should be phased:
- **Phase 1:** prompt/skill policy + task files + watchdog/reporting
- **Phase 2:** optional custom hook pack for stronger enforcement if needed

## Phase 1 — Practical MVP

### 1. Policy layer
Use `main-agent-supervisor` as the standing policy for:
- `AUTO`
- `CONFIRM`
- `ESCALATE`
- anti-permission-loop rules
- triage states (`FINE`, `NEEDS_NUDGE`, `STUCK`, `DONE`, `ESCALATE`)

### 2. Task-state files for larger tasks
Create lightweight files under:
- `.tasks/<task-slug>.md`

Track:
- title
- status
- started
- last updated
- completed steps
- current blocker
- recommended next action

### 3. Audit/review files
For tasks where the agent may ask unnecessary questions, keep optional review artifacts:
- `artifacts/supervisor/<task-slug>/candidate.md`
- `artifacts/supervisor/<task-slug>/decision.json`
- `artifacts/supervisor/<task-slug>/last.md`

### 4. Cron-based watchdog for long tasks
For long tasks, add a periodic cron job that checks the task-state file and emits only useful nudges.

Suggested behaviors:
- if task file not updated for N minutes and not done -> mark as `STUCK`
- if status is `done` -> stop reporting
- if status is `paused` -> surface blocker summary
- if task is progressing -> send concise progress update or stay quiet

## Phase 2 — Stronger enforcement

If Phase 1 is not enough, build a custom hook pack that sits closer to the agent loop.

### Goal of the hook pack
Before a user-visible reply is emitted:
1. inspect draft reply + task context
2. classify AUTO / CONFIRM / ESCALATE
3. suppress obvious proceed-questions
4. rewrite into default-and-continue when safe
5. log the decision

## Recommended first implementation
1. Keep the skill as the policy brain
2. For long tasks, always create `.tasks/<slug>.md`
3. Add a cron-based stall checker for large tasks only
4. Add review artifacts only when the task has meaningful ambiguity
5. If the main agent still permission-loops too much, build a custom hook pack

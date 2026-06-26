---
name: project-loop
description: Run approved long-running project work from file-backed state, continue through self-clearable tasks, pause cleanly at real gates, and recover across sessions.
---

# Project Loop

Use for approved multi-step work that must survive resets, compaction, interruption, approval gates, and stalled execution.

Do not use for trivial one-turn work, open-ended autonomy, or projects without a clear owner.

## Core Rules

- Project files, not chat, are the source of truth
- Trust this order: `state.json` > `manifest.md` > `validation.md` > `handoff.md` > memory > chat
- Only the `owner_agent` in `state.json` executes project tasks
- Other agents may improve the skill, but do not run the loop
- Do not wait for human confirmation between self-clearable tasks
- Keep executing until an approval gate, blocker, or stop condition is reached
- After completing a chunk and successfully updating state, immediately begin the next eligible self-clearable chunk in the same turn
- Do not wait for a human response between self-clearable tasks after a successful state update
- Stop only for a real blocker, approval gate, failed state update, or explicit stop condition
- Before starting any task, check whether the output already exists
- If the work already landed, mark it done and advance
- On every resume, verify `state.json` against actual reality before executing
- During active execution, send a status update at least every 5 minutes
- A 5-minute update must include one of: artifact created, task completed, blocker, or exact next action in progress
- Do not send empty “still working” updates

## Required Project Files

Project path:

```text
agents/<agent-id>/projects/<project-slug>/
```

Required:

```text
README.md
manifest.md
state.json
validation.md
```

Optional:

```text
handoff.md
notes.md
artifacts/
logs/
```

## `state.json` Minimum Fields

- `project_id`
- `owner_agent`
- `status`
- `phase`
- `current_task_id`
- `last_checkpoint`
- `next_action`
- `blocked_reason`
- `awaiting_approval`
- `approval_items`
- `retry_count`
- `max_retries`
- `last_session_note`
- `resume_instructions`
- `interrupted`
- `active_loop`

Recommended additions:
- `approved_objective`
- `scope_guardrails`
- `task_queue_snapshot`
- `completed_tasks`
- `blocked_tasks`
- `deferred_tasks`
- `artifacts`
- `validation_status`
- `last_error`
- `last_error_at`
- `budget_hints`
- `resume_history`
- `watchdog`

## Session Start and Resume

Read in this order:
1. `state.json`
2. `manifest.md`
3. `validation.md`
4. `handoff.md` if present
5. only then memory or chat if still needed

Never start by asking “what were we doing?” if project files exist.

On resume:
- read `status`, `phase`, `current_task_id`, `next_action`, `resume_instructions`
- verify state against actual reality before doing anything
- continue from recorded state, not guesswork

## State Machine

States:
- `Draft`
- `Ready`
- `Running`
- `Validating`
- `AwaitingApproval`
- `Blocked`
- `Paused`
- `Done`
- `Abandoned`

Allowed transitions:

```text
Draft -> Ready
Ready -> Running
Running -> Validating
Validating -> Running
Validating -> Done
Running -> AwaitingApproval
Validating -> AwaitingApproval
Running -> Blocked
Validating -> Blocked
Running -> Paused
AwaitingApproval -> Running
Blocked -> Running
Paused -> Running
Any state -> Abandoned
```

Rules:
- `Draft -> Ready` only when objective, scope, manifest, and validation exist
- `Ready -> Running` only when the next chunk is sized and eligible
- `Running -> Validating` only after outputs are recorded
- `Validating -> Running` only after pass and a next task is eligible
- `Validating -> Done` only when required tasks are complete and final checks pass
- `Running/Validating -> AwaitingApproval` for true human-cleared boundaries
- `Running/Validating -> Blocked` when a blocker cannot be self-cleared within retry rules
- `Running -> Paused` only for interruption, manual pause, or no eligible task

## Execution Rules

- One chunk = one objective + one validation target
- If a task has more than one verb, split it
- Split at boundary changes: local prep -> remote write, remote write -> validation, planning -> execution, authenticated action -> read-back
- Never bundle multiple operations into one command if they can be independent
- If any command or execution step is denied for obfuscation or size, split it into smaller independent steps and retry
- This applies to file writes, API calls, shell commands, browser actions, and any other execution path

A chunk is too large if it:
- has more than one primary deliverable
- crosses multiple boundaries
- mixes planning, execution, and validation
- touches too many pages, endpoints, or files at once
- cannot be described with one clear done condition

## Progress Rules

- Updating `state.json`, `manifest.md`, `validation.md`, or `handoff.md` alone does not count as execution progress unless the current task is explicitly documentation-only
- Do not claim forward execution unless the external world changed or a required artifact for the current task was created
- When marking a task complete, record concrete evidence in state and in your reply when relevant: artifact path, file changed, page changed, validation evidence, or blocker artifact
- If you cannot point to the output, the task is not done
- Do not spend more than 2 consecutive project turns on planning, loop setup, or state reshaping without either executing, validating, or escalating
- If the user questions silence or progress, stop meta narration and report only: what changed, what artifact exists, what blocker exists, and what exact action is next
- Do not report system status theatrically. Report concrete project facts only

## Validation Rules

No task is complete until validation passes and the result is recorded.

Validation may include:
- artifact existence/content check
- file diff or file review
- browser verification of rendered state
- API read-back
- log/command review
- human review for customer-facing release steps

Validation records should capture:
- task ID
- method
- pass/fail
- timestamp
- evidence location
- next step

If validation fails:
- do not advance
- record exact failure
- retry only with a bounded corrective chunk or move to `Blocked`

## Approval and Pause Rules

Self-clearable work may continue if it stays in scope.

Human-cleared work includes:
- credential handling
- auth construction
- authenticated remote writes
- WordPress REST writes
- installs or config changes
- third-party sends
- publish/live-release steps unless already pre-approved
- actions requiring manual login or privileged access

When a true approval gate is reached:
- set `status` to `AwaitingApproval`
- record the exact pending action in `approval_items`
- record what prep is already done
- continue only if another independent task is eligible
- otherwise pause cleanly

Do not pause at routine internal chunk boundaries.
Pause only for:
- real blocker
- missing access or credentials
- meaningful human decision
- explicit stop/pause
- genuine risk or scope boundary

## Interruption and Recovery

If interrupted by unrelated work:
- finish any atomic write already in progress if safe
- update `state.json` immediately
- set `interrupted=true`
- set `active_loop=false`
- set `status=Paused` unless already `AwaitingApproval` or `Blocked`

When updating `state.json`, use a full-file write by default, not a partial edit. `state.json` changes frequently and exact-match edit operations are brittle on high-churn files. Use partial edit only if you have just read the current file and the change is truly small, stable, and low-risk.

If `state.json` cannot be updated:
- stop execution immediately
- this is a hard stop, not a soft warning
- do not continue the loop, do not start another chunk, and do not claim progress until state is repaired or successfully rewritten
- report the exact failure and recovery step

If a task may have partially executed:
- verify actual reality first
- do not blindly rerun
- choose next action from observed state, not assumptions

If state is missing or inconsistent:
- reconstruct from manifest, validation, artifacts, and handoff
- rewrite state before resuming

## Watchdog Rules

Cron is a watchdog only, never the main workflow engine.

- When creating a new project, automatically create a watchdog cron for that project
- When a project moves to `Done` or `Abandoned`, remove the watchdog
- The watchdog only reports when it takes an action or finds something worth surfacing
- If there is nothing to resume, retry, or escalate, stay silent

Watchdog may:
- detect stale `Running`
- detect resumable `Paused`
- detect approval-cleared states ready to continue
- trigger one bounded resume pass

Watchdog must not:
- invent new work
- rewrite scope
- cross approval gates without clearance
- spam retries
- chain arbitrary timer-based work

Recommended cap:
- one automatic resume attempt per cycle
- no more than two automatic recovery attempts without new evidence

## Operating Sequence

1. Read `state.json`
2. Read `manifest.md`
3. Read `validation.md`
4. Read `handoff.md` if present
5. Verify current state against actual reality
6. Check whether the target output already exists
7. Pick one eligible chunk
8. Apply chunk sizing rules
9. Execute
10. Validate
11. Update `state.json`
12. Continue if self-clearable, otherwise pause or escalate cleanly

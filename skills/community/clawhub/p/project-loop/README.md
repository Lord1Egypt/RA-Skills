# Project Loop

Lean orchestration skill for approved long-running work that must survive resets, interruption, approval gates, and stale sessions.

## Use It When
- a project will outlast one session
- chat history is not enough
- work should continue through self-clearable tasks
- approvals, validation, pause/resume, and recovery matter

Do not use it for trivial one-turn tasks or open-ended autonomy.

## Core Model
- project files are the source of truth
- trust: `state.json` > `manifest.md` > `validation.md` > `handoff.md` > memory > chat
- only the `owner_agent` in `state.json` runs project tasks
- do not wait between self-clearable tasks
- after completing a chunk and successfully updating state, immediately begin the next eligible self-clearable chunk in the same turn
- stop only for a real blocker, approval gate, failed state update, or explicit stop condition
- on resume, verify `state.json` against reality before executing
- check whether output already exists before redoing work

## Required Files

```text
agents/<agent-id>/projects/<project-slug>/
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

Typical flow:

```text
Draft -> Ready -> Running -> Validating -> Running -> Done
```

## Key Rules
- one chunk = one objective + one validation target
- if a task has more than one verb, split it
- split at boundary changes
- if a command or step is denied for obfuscation or size, split and retry smaller
- never bundle unrelated operations into one command
- docs/state updates alone do not count as execution progress unless the task is documentation-only
- do not claim completion without concrete evidence
- when updating `state.json`, use a full-file write by default, not a partial edit. Partial edits are brittle on a high-churn state file
- if `state.json` update fails, stop immediately. This is a hard stop. Do not continue, do not start another chunk, and do not claim progress until state is repaired
- do not spend more than 2 consecutive turns in meta/planning without executing, validating, or escalating

## Progress Updates
During active execution, send a status update at least every 5 minutes.

A valid update must include one of:
- artifact created
- task completed
- blocker found
- exact next action in progress

## Approval and Pause
Pause only for real gates:
- missing access or credentials
- human decision
- real blocker
- explicit stop/pause
- meaningful risk boundary

Do not pause at routine internal chunk boundaries.

## Validation
No task is done until validation passes and evidence is recorded.

Validation can include:
- artifact checks
- file review
- browser verification
- API read-back
- rendered output checks
- human review for customer-facing release steps

## Watchdog
The watchdog is for project-loop recovery only.

- auto-create when a new project is created
- remove when project reaches `Done` or `Abandoned`
- stay silent if there is nothing to resume, retry, or escalate
- only report when it acts or finds something worth surfacing
- never invent work or bypass approval gates

## Operating Flow
1. read `state.json`
2. read `manifest.md`
3. read `validation.md`
4. verify reality
5. check whether output already exists
6. pick one chunk
7. execute
8. validate
9. update `state.json`
10. continue or pause cleanly

## Note
Project Loop is the orchestration layer. Project-specific truth should live in each project folder, not in chat.

# Task lifecycle and state machine

This document defines the minimum lifecycle model for `local-coding-orchestrator` tasks.

## Purpose

A local worker exiting is not enough to call a task done.

The supervisor owns lifecycle transitions. Workers only produce artifacts and execution outcomes.

## Canonical states

- `draft`
- `queued`
- `running`
- `awaiting-review`
- `changes-requested`
- `retrying`
- `blocked`
- `completed`
- `failed`
- `cancelled`

## State meanings

### `draft`
Task exists but has not been accepted for execution.

### `queued`
Task is ready to run but waiting for resources, prerequisites, or scheduling.

### `running`
At least one assigned worker is actively executing the current attempt.

### `awaiting-review`
Implementation attempt produced a candidate result and the supervisor is now waiting for review or objective checks.

### `changes-requested`
Review or checks found issues that need another implementation pass.

### `retrying`
The supervisor has decided to relaunch the task after preparing a revised attempt.

### `blocked`
Task cannot proceed without outside help, missing context, environmental repair, or explicit operator decision.

### `completed`
All required objective checks passed and the supervisor has explicitly marked the task done.

### `failed`
The task reached a terminal unsuccessful state, such as max attempts exhausted or a fatal constraint.

### `cancelled`
The task was intentionally stopped by the operator.

## Allowed transitions

```text
draft -> queued | cancelled
queued -> running | blocked | cancelled
running -> awaiting-review | blocked | failed | cancelled
awaiting-review -> completed | changes-requested | blocked | failed | cancelled
changes-requested -> retrying | blocked | failed | cancelled
retrying -> running | blocked | failed | cancelled
blocked -> queued | cancelled | failed
failed -> queued | cancelled
completed -> (terminal)
cancelled -> (terminal)
```

## Transition rules

### Who may change state

The supervisor is the only authority that should commit lifecycle transitions.

Workers may emit signals such as:
- process exited
- patch written
- tests passed
- review artifact created

But workers should not write `completed` directly into the task state without supervisor confirmation.

### Required metadata on transition

Every lifecycle transition should record:
- previous state
- next state
- timestamp
- reason
- actor (`supervisor`, `worker`, `operator`, `system`)
- attempt number

Recommended event record:

```json
{
  "from": "running",
  "to": "awaiting-review",
  "at": 1772959300000,
  "reason": "worker exited and produced candidate patch",
  "actor": "supervisor",
  "attempt": 1
}
```

### Blocked vs failed

Use `blocked` when progress may resume after intervention.
Use `failed` only for terminal outcomes.

Examples of `blocked`:
- missing repository access
- environment not prepared
- ambiguous requirement
- unavailable dependency

Examples of `failed`:
- max attempts exhausted
- repository intentionally rejected task direction
- required tool unavailable and no substitute allowed

## Minimum state transition checks

Before allowing a transition, validate:
- transition pair is allowed
- task id exists
- attempt number is present
- timestamp is written
- reason is non-empty

## Suggested helper API

A future helper script or module can expose functions like:

- `New-OrchestratorTask`
- `Get-OrchestratorTask`
- `Set-OrchestratorTaskState`
- `Add-OrchestratorTaskEvent`
- `Get-OrchestratorTaskHistory`

The helper should reject illegal state jumps unless an operator explicitly forces them.

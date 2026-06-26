# Script interface overview

This file lists the main scripts and their current role in the v2 scaffold.

## Task state

### `task-state.ps1`
Purpose:
- initialize tasks
- fetch task records
- perform validated state transitions

## Evaluation

### `evaluate-done.ps1`
Purpose:
- inspect objective checks
- determine whether task completion is currently allowed

## Retry

### `generate-retry-brief.ps1`
Purpose:
- create mechanical or semantic retry briefs
- optionally write the next prompt artifact

## Pipeline

### `start-pipeline.ps1`
Purpose:
- resolve role-based worker presets for the configured pipeline

## Worker launch

### `launch-worker.ps1`
Purpose:
- select the worker role
- generate either a default brief or a probe-mode brief
- allocate prompt/log/result artifacts
- optionally launch sync or background worker execution

## Worker reconcile

### `reconcile-worker.ps1`
Purpose:
- inspect worker runtime state
- classify worker outcome
- write summary/result artifacts
- backfill some objective checks
- interpret probe-mode results for supervisor follow-up

## Supervisor

### `supervise-task.ps1`
Purpose:
- reconcile running background workers
- evaluate current task status
- recommend or apply next orchestration steps
- optionally auto-launch or auto-block in safe cases

## Tool wrappers

### `run-codex.ps1`
### `run-claude-code.ps1`
### `run-opencode.ps1`
Purpose:
- adapt local coding CLIs to the orchestrator
- accept either `Task` or `TaskFile`

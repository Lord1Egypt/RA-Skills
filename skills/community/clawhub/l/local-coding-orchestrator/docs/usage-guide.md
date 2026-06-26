# local-coding-orchestrator usage guide

This guide describes the current v2 shape of `local-coding-orchestrator`.

## What it is now

The skill is no longer just a router for local coding CLIs.
It is now a lightweight supervisor skeleton with:
- persistent task records
- lifecycle transitions
- done policy evaluation
- retry brief generation
- pipeline presets
- worker launch adapters
- background worker reconcile
- environment failure classification

## Core scripts

### Task and lifecycle
- `assets/scripts/task-state.ps1`
- `assets/scripts/evaluate-done.ps1`

### Orchestration
- `assets/scripts/start-pipeline.ps1`
- `assets/scripts/generate-retry-brief.ps1`
- `assets/scripts/supervise-task.ps1`

### Worker execution
- `assets/scripts/launch-worker.ps1`
- `assets/scripts/reconcile-worker.ps1`
- `assets/scripts/run-codex.ps1`
- `assets/scripts/run-claude-code.ps1`
- `assets/scripts/run-opencode.ps1`

## Recommended happy path

1. create/init a task record
2. move it to `queued`
3. let supervisor auto-launch a background worker
4. reconcile worker state periodically
5. let supervisor recommend `awaiting-review`, `blocked`, or `completed`
6. use retry briefs only when the failure is semantic rather than environmental

## Example flow

### 1. initialize a task
```powershell
powershell -ExecutionPolicy Bypass -File assets/scripts/task-state.ps1 \
  -Action init -TaskId feat-demo -Repo D:/data/code/my-repo -TaskType feature \
  -Pipeline implement_and_review -Role implementer -Agent codex
```

Prefer a concrete repo path. Internally the scaffold now standardizes toward `repoPath` while remaining backward-compatible with the `repo` field.

### 2. queue the task
```powershell
powershell -ExecutionPolicy Bypass -File assets/scripts/task-state.ps1 \
  -Action transition -TaskId feat-demo -ToState queued -Reason "ready" -Actor supervisor
```

### 3. let supervisor auto-launch
```powershell
powershell -ExecutionPolicy Bypass -File assets/scripts/supervise-task.ps1 \
  -TaskId feat-demo -AutoLaunch -ApplyTransition -Json
```

### 3b. use auto-probe for constrained environments
```powershell
powershell -ExecutionPolicy Bypass -File assets/scripts/supervise-task.ps1 \
  -TaskId feat-demo -AutoLaunch -AutoProbe -ApplyTransition -Json
```

### 4. reconcile background worker later
```powershell
powershell -ExecutionPolicy Bypass -File assets/scripts/reconcile-worker.ps1 \
  -TaskId feat-demo -Json
```

### 5. ask supervisor what to do next
```powershell
powershell -ExecutionPolicy Bypass -File assets/scripts/supervise-task.ps1 \
  -TaskId feat-demo -Json
```

## Current known limits

- background worker completion is still heuristic
- worker output cleaning is basic
- environment failures are classified, but not all types are normalized yet
- task objective checks still need deeper automatic population from actual builds/tests/reviews

## Best use right now

Use this skill as a local orchestration scaffold and supervisor layer.
Do not treat it as a fully autonomous production runtime yet.

# Operator playbook

This is the practical guide for using `local-coding-orchestrator` as of the current stage-based scaffold.

## Recommended flow

### 1. Start with repo path, not just repo name
Use a concrete repo path whenever possible.

### 2. Run a probe first in constrained environments
Use probe mode when:
- the repo is new to the orchestrator
- the runtime may be read-only or policy-limited
- you are unsure whether build/test can run

Recommended supervisor call:
```powershell
powershell -ExecutionPolicy Bypass -File assets/scripts/supervise-task.ps1 \
  -TaskId feat-demo -AutoLaunch -AutoProbe -ApplyTransition -Json
```

### 3. Reconcile after background execution
After the worker runs, reconcile the result:
```powershell
powershell -ExecutionPolicy Bypass -File assets/scripts/reconcile-worker.ps1 \
  -TaskId feat-demo -Json
```

### 4. Let supervisor decide the next phase
Then ask the supervisor what phase comes next:
```powershell
powershell -ExecutionPolicy Bypass -File assets/scripts/supervise-task.ps1 \
  -TaskId feat-demo -Json
```

## Phase intent

### Probe
Find out whether the repo and runtime are viable.

### Implement
Make changes when the runtime is good enough.

### Review
Classify blockers and decide whether to advance, block, or request changes.

### Harden
Do final cleanup or follow-up fixes before considering the task complete.

## Practical advice

- if probe says the runtime is blocked, trust it and stop forcing implementation
- if review says `blocked-by-environment`, do not generate semantic retry briefs
- if review says `approved-for-next-step`, then move to implementation or hardening
- use retry generation for misunderstanding or wrong-scope work, not for policy or sandbox limits

## What this skill is best at right now

- structuring local coding work
- supervising local agent runs
- distinguishing environment blockers from implementation blockers
- guiding next-step decisions with lightweight orchestration state

## What still needs caution

- background execution still inherits local CLI quirks
- build/test feasibility can be runtime-limited even when repo access works
- some conclusions still depend on summary parsing rather than deterministic artifact analysis

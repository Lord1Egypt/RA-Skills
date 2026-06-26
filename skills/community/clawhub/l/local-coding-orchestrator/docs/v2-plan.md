# local-coding-orchestrator v2 plan

## Goal

Upgrade the skill from a prompt router into a lightweight local coding supervisor.

## Priority roadmap

### P1 - foundation
- add persistent task records
- define lifecycle states
- define done policies by task type
- define supervisor vs worker responsibilities

### P2 - orchestration quality
- add mechanical vs semantic retry model ✅
- add role-based pipelines ✅
- add objective progress reporting shape

### P3 - operational safety
- add resource scheduling guidance
- add worktree / artifact isolation rules ✅
- add operator controls for steer / cancel / reassign

### P4 - automation expansion
- add task queue ingestion from files/issues
- add stuck-task detection
- add optional proactive task discovery

## Recommended artifacts

```text
local-orchestrator/
  tasks/
  logs/
  prompts/
  reviews/
  state/
```

## Recommended first implementation targets

1. task JSON schema
2. task state transition helper
3. done policy evaluator
4. retry brief generator
5. pipeline presets

## Notes

Do not add proactive discovery until the system is reliable at:
- persisting tasks
- supervising running workers
- distinguishing worker exit from task completion
- retrying semantically when task interpretation is wrong

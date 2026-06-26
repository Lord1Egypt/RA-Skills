# Agent Permission Matrix

Use least privilege. The plugin should enforce this matrix where possible.

| Actor | Read task | Start attempt | Record checkpoint | Record artifact | Append review | Request/resolve approval | Transition phase | Open circuit | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| Orchestrator | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Only phase owner |
| Executor (local) | Yes | No | Yes | Yes | No | No | No | No | Produces evidence only |
| Executor (ACP/Codex) | Yes | No | Yes | Yes | No | No | No | No | External session refs are advisory only |
| Spec Reviewer | Yes | No | Optional | Optional | Yes, `spec` only | No | No | No | Cannot close task |
| Quality Reviewer | Yes | No | Optional | Optional | Yes, `quality` only | No | No | No | Cannot close task |
| Lobster | Yes | No | Yes | Optional | No | Yes | No | No | Approval/recovery only |
| Human Approver | Limited | No | No | No | No | Via Lobster/UI only | No | No | Decision only |

## Mandatory Guardrails

- reject `task_transition` unless `actor_role=orchestrator`
- reject `task_append_review` if `review_type` does not match reviewer capability
- reject approval resolution from arbitrary executor identities
- reject `task_open_circuit` from reviewers/executors

## Why This Matrix Exists

v1 failed by mixing evidence production and state authority:

- reviewer output implicitly closed work
- blackboard writes became de facto truth
- prompt wording acted like state

v2 fixes that by making permissions explicit and tool-enforced.

# Migration From v1 To OpenClaw-native v2

## Migration Steps

1. Freeze the old protocol entrypoints.
   Stop teaching agents to use `shared/blackboard.json`, `bd`, or fixed role `sessionKey`.

2. Install and enable the `task-store` plugin.
   Create the SQLite DB and verify typed tools are available before any workflow cutover.

3. Port the protocol contract into `SKILL.md`.
   Keep spec-first, review gates, retry/circuit breaker. Remove storage and coordination assumptions from prompts.

4. Replace prompt-only control flow with OpenProse.
   Put only orchestration branches in `.prose`. Put canonical phase and attempts in SQLite.

5. Introduce Lobster only for approval/recovery.
   Any side-effecting step should route through the Lobster template instead of ad hoc chat confirmation.

6. Rewire executor paths.
   Use local workers for local tasks and ACP for external harnesses such as Codex. Pass `task_id`, `attempt_id`, `workspace`, and allowed capabilities explicitly.

7. Rewire reviewers.
   Reviewers write `task_append_review` only. The orchestrator reads those verdicts and decides the next phase.

8. Replace old retry bookkeeping.
   Move retry count, failure summaries, and circuit state into `attempts/events/tasks.circuit_status`.

9. Decommission old files and assumptions.
   Remove or archive blackboard, beads-specific notes, and fixed session conventions.

10. Cut over AGENTS/global guidance.
    Any top-level operator instructions should now point to `multi-agent-protocol` v2 and the `task-store` tools.

## Delete / Replace Checklist

| Old v1 element | Action | v2 replacement |
|---|---|---|
| Fixed role `sessionKey` contract | Delete as protocol requirement | `attempt_id` + optional `external_session_ref` in `task-store` |
| `shared/blackboard.json` | Delete | SQLite tables + append-only event log |
| `shared/artifacts/{role}` as truth | Replace | `artifacts` records with explicit `uri` |
| `beads` dependency graph | Delete as required dependency | `task_*` typed tools and orchestrator branching |
| `bd ready / bd close / bd sync` flows | Replace | `task_get`, `task_transition`, `task_open_circuit` |
| Reviewer verdict implicitly closes task | Delete | Reviewer writes evidence; orchestrator moves phase |
| Prompt text carries retry count | Delete | `attempts` + `events` |
| `git worktree` as default parallelism story | Replace | ACP/local runtime selection; git optional per task |
| LangGraph DAG assumption | Delete | OpenProse orchestration + SQLite state |
| "Orchestrator reads blackboard to determine next phase" | Replace | Orchestrator reads `task_get` snapshot |

## Old Content To Remove From Existing OpenClaw Workspace

From the current local setup, remove or rewrite any guidance that says:

- same role must reuse the same `sessionKey`
- agents communicate through `shared/blackboard.json`
- `beads` is the task bus
- `bd sync` is required to flush state
- reviewer may directly determine task completion
- prompt history is enough to recover after interruption

## Old Content Worth Keeping

Keep these ideas, but re-home them:

- spec-first
- separate spec review and quality review
- bounded retry
- circuit breaker
- serial implementation when file conflict risk is high

## Cutover Outcome

After migration, the state ownership should be:

- protocol rules: `SKILL.md`
- orchestration graph: `OpenProse`
- approval/recovery: `Lobster`
- canonical task state: `task-store`
- external coding harness bridge: `ACP`

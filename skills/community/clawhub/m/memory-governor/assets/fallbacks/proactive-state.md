+++
target_class = "proactive_state"
schema_version = "0.1"
updated_at = "2026-03-31T00:00:00Z"
state_mode = "combined"
current_objective = ""
current_blocker = ""
next_move = ""
+++

# proactive-state.md

Fallback template for the `proactive_state` target class.

Use this when no preferred adapter is available.

## Current Task State

- current objective
- current blocker
- next move

## Durable Boundaries

- durable proactive boundaries that matter for the current line of work

## Rules

- treat this as the current truth, not a running transcript
- replace stale fields when the task state changes
- extract durable lessons before promoting elsewhere
- clear or refresh when the task is done

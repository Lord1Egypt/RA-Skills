+++
target_class = "proactive_state"
schema_version = "0.1"
updated_at = "2026-03-31T00:00:00Z"
state_mode = "combined"
current_objective = ""
current_blocker = ""
next_move = ""
+++

# Proactive State

This file is the local fallback for `proactive_state`.

Use it when the host does not install a dedicated proactivity adapter.

## Current Task State

- current objective
- current blocker
- next move

## Durable Boundaries

- activation preferences that still matter for this line of work
- proactive boundaries worth preserving across interruptions

## Rules

- keep current task state easy to scan
- replace stale task fields instead of appending forever
- keep durable boundaries separate from transient breadcrumbs
- clear or refresh task-specific fields when the task is complete

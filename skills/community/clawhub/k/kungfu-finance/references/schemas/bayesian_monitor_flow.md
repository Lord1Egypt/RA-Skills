# Bayesian Monitor Flow Contract

This file documents the first-stage bayesian monitor flow for `kungfu_finance`.
It is an internal contract for implementation and maintenance.
It is not the primary user-facing routing surface.

Use [SKILL.md](../../SKILL.md) for high-level intent routing first.

## Purpose

The bayesian monitor flow currently supports two actions only:

- list the current user's existing bayesian monitor tasks
- inspect one existing task's initial report and latest monitor records

It does not cover task creation, task deletion, manual task execution, schedule management, or cross-user task access.

## Router Entry

Use the router command:

```bash
node scripts/router/run_router.mjs bayesian-monitor ...
```

## Actions

### `list`

Required input:

- `--bayesian-action list`

Behavior:

- fetch `/api/bayesian-monitor/tasks`
- return task summaries only
- do not expose full `original_report` in the list response

### `reports`

Required input:

- `--bayesian-action reports`
- exactly one of:
  - `--bayesian-task-id`
  - `--bayesian-topic`

Optional input:

- `--bayesian-record-limit`

Behavior:

- fetch `/api/bayesian-monitor/tasks`
- resolve the task selector in flow first
- then fetch `/api/bayesian-monitor/tasks/records`
- return:
  - selected task summary
  - `initial_report` from the selected task's `original_report`
  - simplified monitor records

## Resolution Rules

- Bayesian monitor flow must require OpenKey before local validation branches.
- `reports` must resolve the selected task against the current user's task list before calling the records endpoint.
- If both `bayesian-task-id` and `bayesian-topic` are given, return `needs_input`.
- If selector is missing, return `needs_input`.
- If topic matches multiple tasks, return `needs_input` and require `bayesian-task-id`.
- If no task matches, return `needs_input`.
- If the current user has no tasks and asks for `reports`, return `blocked`.

## Error Handling Rules

- Do not treat `/api/bayesian-monitor/tasks/records` empty array as proof that the task exists.
- If upstream returns `401` or `403`, surface the auth or permission error directly.
- Keep the first-stage scope read-only. Do not fallback to create/run task behaviors.

## Output Shape

### `needs_input`

- `action`
- `status: "needs_input"`
- `prompt`
- `missing`
- optional `reason`
- optional `options`
- optional `attempted`

### `blocked`

- `action`
- `status: "blocked"`
- `reason`
- `message`

### `completed`

List returns:

- `action`
- `status: "completed"`
- `tasks`
- `total`

Reports returns:

- `action`
- `status: "completed"`
- `task`
- `initial_report`
- `records`
- `record_limit`

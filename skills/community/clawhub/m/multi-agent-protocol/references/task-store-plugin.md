# task-store Plugin Design

This plugin is the authoritative state layer for Multi-Agent Protocol v2.

## Responsibilities

- persist canonical task state in SQLite
- expose typed tools for orchestration, reviews, approvals, and recovery
- emit an append-only event log
- provide resumable state for Lobster and ACP-connected executors

## Non-Responsibilities

- no orchestration graph logic
- no review judgment
- no prompt memory emulation
- no dependency on `git`, `beads`, or shared JSON files

## Storage Model

SQLite is the source of truth. The event log is append-only and queryable from SQLite.

Recommended tables:

### `tasks`

| column | type | notes |
|---|---|---|
| `id` | text pk | `tsk_...` |
| `title` | text | |
| `workspace` | text | absolute path or logical workspace |
| `phase` | text | canonical phase enum |
| `goal` | text | extracted from spec |
| `scope_in_json` | text | JSON array |
| `scope_out_json` | text | JSON array |
| `inputs_json` | text | JSON array/object |
| `outputs_json` | text | JSON array/object |
| `acceptance_json` | text | JSON array |
| `risks_json` | text | JSON array |
| `created_at` | text | ISO-8601 |
| `updated_at` | text | ISO-8601 |
| `circuit_status` | text | `closed|open` |
| `current_attempt_id` | text null | |

### `attempts`

| column | type | notes |
|---|---|---|
| `id` | text pk | `att_...` |
| `task_id` | text fk | |
| `ordinal` | integer | starts at 1 |
| `phase` | text | usually `executing` |
| `runtime` | text | `local|acp|other` |
| `executor_kind` | text | `builder|research|external_coder` |
| `worker_ref` | text | logical worker ID |
| `external_session_ref` | text null | ACP/Codex session ref |
| `status` | text | `running|succeeded|failed|aborted` |
| `error_summary` | text null | |
| `started_at` | text | ISO-8601 |
| `finished_at` | text null | ISO-8601 |

### `reviews`

| column | type | notes |
|---|---|---|
| `id` | text pk | `rev_...` |
| `task_id` | text fk | |
| `attempt_id` | text fk | |
| `review_type` | text | `spec|quality` |
| `reviewer_ref` | text | |
| `verdict` | text | `approved|changes_requested|blocked` |
| `summary` | text | |
| `findings_json` | text | JSON array |
| `created_at` | text | ISO-8601 |

### `artifacts`

| column | type | notes |
|---|---|---|
| `id` | text pk | `art_...` |
| `task_id` | text fk | |
| `attempt_id` | text fk | |
| `kind` | text | `primary_output|test_report|diff|review_report|other` |
| `uri` | text | file path or external URI |
| `summary` | text | |
| `produced_by` | text | |
| `created_at` | text | ISO-8601 |

### `approvals`

| column | type | notes |
|---|---|---|
| `id` | text pk | `apr_...` |
| `task_id` | text fk | |
| `attempt_id` | text fk | |
| `requested_action` | text | |
| `side_effect_kind` | text | |
| `idempotency_key` | text | |
| `status` | text | `pending|approved|rejected|request_changes` |
| `requested_by` | text | |
| `resolved_by` | text null | |
| `note` | text null | |
| `created_at` | text | ISO-8601 |
| `resolved_at` | text null | ISO-8601 |

### `events`

Append-only audit log.

| column | type | notes |
|---|---|---|
| `id` | integer pk | autoincrement |
| `task_id` | text fk | |
| `attempt_id` | text null | |
| `event_type` | text | |
| `actor` | text | |
| `payload_json` | text | |
| `created_at` | text | ISO-8601 |

## Phase Ownership

Only the orchestrator may mutate `tasks.phase`.

Enforce this in plugin logic:

- `task_transition` requires `actor_role=orchestrator`
- reviewer tools reject phase writes
- approval tools reject phase writes
- ACP executor tools reject phase writes

This is the hard stop that keeps reviewers from becoming the source of truth.

## Tool Set

Below is a minimal schema set. Names can be adjusted to your plugin SDK, but preserve the
separation of authority.

### `task_create`

Creates a canonical task record.

```json
{
  "name": "task_create",
  "description": "Create a task and persist its initial spec.",
  "input_schema": {
    "type": "object",
    "required": ["title", "spec_markdown", "workspace", "initial_phase"],
    "properties": {
      "title": { "type": "string" },
      "spec_markdown": { "type": "string" },
      "workspace": { "type": "string" },
      "initial_phase": {
        "type": "string",
        "enum": ["spec_draft", "spec_review"]
      },
      "labels": {
        "type": "array",
        "items": { "type": "string" }
      }
    }
  }
}
```

### `task_get`

Returns the canonical snapshot plus denormalized latest review/approval info.

```json
{
  "name": "task_get",
  "description": "Fetch a task snapshot with current phase, reviews, attempts, artifacts, and approvals.",
  "input_schema": {
    "type": "object",
    "required": ["task_id"],
    "properties": {
      "task_id": { "type": "string" },
      "include_events_limit": { "type": "integer", "minimum": 0, "maximum": 200 }
    }
  }
}
```

### `task_transition`

Only orchestrator may call this successfully.

```json
{
  "name": "task_transition",
  "description": "Atomically move a task from one phase to another and append an event.",
  "input_schema": {
    "type": "object",
    "required": ["task_id", "from_phase", "to_phase", "actor", "actor_role", "reason"],
    "properties": {
      "task_id": { "type": "string" },
      "from_phase": { "type": "string" },
      "to_phase": { "type": "string" },
      "actor": { "type": "string" },
      "actor_role": { "type": "string", "enum": ["orchestrator"] },
      "reason": { "type": "string" },
      "attempt_id": { "type": "string" }
    }
  }
}
```

### `task_start_attempt`

```json
{
  "name": "task_start_attempt",
  "description": "Create a new execution attempt and increment retry counters.",
  "input_schema": {
    "type": "object",
    "required": ["task_id", "phase", "actor", "runtime", "executor_kind"],
    "properties": {
      "task_id": { "type": "string" },
      "phase": { "type": "string", "enum": ["executing"] },
      "actor": { "type": "string" },
      "runtime": { "type": "string", "enum": ["local", "acp", "other"] },
      "executor_kind": {
        "type": "string",
        "enum": ["builder", "research", "external_coder"]
      },
      "worker_ref": { "type": "string" },
      "external_session_ref": { "type": "string" }
    }
  }
}
```

### `task_record_checkpoint`

For heartbeats, execution summaries, retry scheduling, and recovery markers.

```json
{
  "name": "task_record_checkpoint",
  "description": "Append a structured checkpoint event without mutating task phase.",
  "input_schema": {
    "type": "object",
    "required": ["task_id", "attempt_id", "checkpoint_type", "payload"],
    "properties": {
      "task_id": { "type": "string" },
      "attempt_id": { "type": "string" },
      "checkpoint_type": { "type": "string" },
      "payload": { "type": "object" }
    }
  }
}
```

### `task_record_artifact`

```json
{
  "name": "task_record_artifact",
  "description": "Register an artifact produced by an executor or reviewer.",
  "input_schema": {
    "type": "object",
    "required": ["task_id", "attempt_id", "kind", "uri", "produced_by"],
    "properties": {
      "task_id": { "type": "string" },
      "attempt_id": { "type": "string" },
      "kind": { "type": "string" },
      "uri": { "type": "string" },
      "summary": { "type": "string" },
      "produced_by": { "type": "string" }
    }
  }
}
```

### `task_append_review`

Reviewers only add evidence.

```json
{
  "name": "task_append_review",
  "description": "Append a spec or quality review record. Does not move phase.",
  "input_schema": {
    "type": "object",
    "required": ["task_id", "attempt_id", "review_type", "reviewer_ref", "verdict", "findings"],
    "properties": {
      "task_id": { "type": "string" },
      "attempt_id": { "type": "string" },
      "review_type": { "type": "string", "enum": ["spec", "quality"] },
      "reviewer_ref": { "type": "string" },
      "verdict": {
        "type": "string",
        "enum": ["approved", "changes_requested", "blocked"]
      },
      "summary": { "type": "string" },
      "findings": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["severity", "message"],
          "properties": {
            "severity": { "type": "string", "enum": ["critical", "major", "minor"] },
            "message": { "type": "string" },
            "file": { "type": "string" },
            "line": { "type": "integer" },
            "artifact_uri": { "type": "string" }
          }
        }
      }
    }
  }
}
```

### `task_request_approval`

```json
{
  "name": "task_request_approval",
  "description": "Create a pending approval record for a side-effecting action.",
  "input_schema": {
    "type": "object",
    "required": ["task_id", "attempt_id", "requested_action", "side_effect_kind", "idempotency_key", "status"],
    "properties": {
      "task_id": { "type": "string" },
      "attempt_id": { "type": "string" },
      "requested_action": { "type": "string" },
      "side_effect_kind": { "type": "string" },
      "idempotency_key": { "type": "string" },
      "requested_by": { "type": "string" },
      "status": { "type": "string", "enum": ["pending"] }
    }
  }
}
```

### `task_resolve_approval`

```json
{
  "name": "task_resolve_approval",
  "description": "Resolve an approval request. Does not move workflow phase.",
  "input_schema": {
    "type": "object",
    "required": ["task_id", "approval_id", "resolution", "resolved_by"],
    "properties": {
      "task_id": { "type": "string" },
      "approval_id": { "type": "string" },
      "resolution": {
        "type": "string",
        "enum": ["approved", "rejected", "request_changes"]
      },
      "resolved_by": { "type": "string" },
      "note": { "type": "string" }
    }
  }
}
```

### `task_open_circuit`

```json
{
  "name": "task_open_circuit",
  "description": "Mark a task as circuit_open and append the failure summary.",
  "input_schema": {
    "type": "object",
    "required": ["task_id", "actor", "reason"],
    "properties": {
      "task_id": { "type": "string" },
      "actor": { "type": "string" },
      "reason": { "type": "string" },
      "latest_attempt_id": { "type": "string" }
    }
  }
}
```

### Optional helper: `task_list_ready`

Useful for dashboards or cron-driven orchestration, but not required for the minimal workflow.

## Event Taxonomy

Recommended event types:

- `task.created`
- `task.transitioned`
- `attempt.started`
- `attempt.checkpoint`
- `attempt.finished`
- `artifact.recorded`
- `review.appended`
- `approval.requested`
- `approval.resolved`
- `circuit.opened`

## Recovery Contract

Lobster and the orchestrator should be able to resume from:

- latest phase
- latest attempt
- latest approval state
- latest checkpoint
- latest artifact

No recovery flow should depend on replaying hidden prompt history.

## ACP Integration Notes

Store ACP metadata as references, not truth:

- `external_session_ref`
- `worker_ref`
- `runtime`

These help debugging and resume, but canonical state still lives in `tasks/attempts/events`.

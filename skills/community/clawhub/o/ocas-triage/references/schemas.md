# Triage Schemas

Extends `spec-ocas-shared-schemas.md` (DecisionRecord, LogEvent, ConfigBase).

---

## Task

Primary record. State transitions are new appended records with the same `task_id` — never mutations.

```json
{
  "task_id": "string — hash(origin_message + created_at)",
  "origin": "string — user_message | dispatch | mentor | cron | heartbeat",
  "origin_message": "string",
  "created_at": "ISO8601",
  "deadline": "ISO8601 | null",
  "estimated_completion_seconds": "number | null",
  "priority_score": "number — integer, clamped 0–100",
  "state": "string — queued | active | completed | cancelled | blocked | waiting_external",
  "checkpoint": {
    "last_execution_time": "ISO8601 | null",
    "partial_result": "string | null",
    "progress_marker": "string | null"
  },
  "routing_hint": "string — mentor | dispatch | direct | null",
  "blocking_reason": "string | null",
  "completed_at": "ISO8601 | null",
  "retry_count": "number — default 0"
}
```

### State semantics

| State | Meaning | Queue aging |
|---|---|---|
| `queued` | Waiting for execution | Yes |
| `active` | Currently executing (max one at a time) | Yes |
| `completed` | Finished; moved to history | — |
| `cancelled` | Explicitly cancelled or TTL expired | — |
| `blocked` | Retry limit exceeded; awaiting human | No |
| `waiting_external` | Awaiting external service or human response | No |

### routing_hint semantics

| Value | Consumer |
|---|---|
| `mentor` | Mentor picks up on heartbeat; project-level orchestration |
| `dispatch` | Dispatch picks up; communication action |
| `direct` | Base agent handles without skill invocation |
| `null` | Consumer to be determined at pickup time |

`routing_hint` is advisory. Consumer makes final routing decision.

---

## Signals

Written to `.triage/signals.jsonl`. Consumers poll this file.

### task_ready (standard)

Emitted when a task transitions to `active` with `routing_hint != mentor`.

```json
{
  "signal": "task_ready",
  "task_id": "string",
  "routing_hint": "string | null",
  "priority_score": "number",
  "emitted_at": "ISO8601"
}
```

### task_ready (Mentor handoff — required extension)

Emitted when `routing_hint = mentor`. The `heartbeat_interval_seconds` field is **required**. Signals without it are malformed and must not be picked up by Mentor.

```json
{
  "signal": "task_ready",
  "task_id": "string",
  "routing_hint": "mentor",
  "priority_score": "number",
  "heartbeat_interval_seconds": "number — 60 | 600 | 3600",
  "heartbeat_rationale": "string — human-readable explanation",
  "emitted_at": "ISO8601"
}
```

**Heartbeat interval assignment:**

| Priority score | heartbeat_interval_seconds |
|---|---|
| 70–100 | 60 |
| 40–69 | 600 |
| 0–39 | 3600 (default for low; may extend to 21600 for explicit non-urgent background) |

### task_completed

```json
{
  "signal": "task_completed",
  "task_id": "string",
  "state": "completed | cancelled",
  "completed_at": "ISO8601"
}
```

### task_acknowledged

Written by the consuming system to prevent double-pickup.

```json
{
  "signal": "task_acknowledged",
  "task_id": "string",
  "acknowledged_by": "string — mentor | dispatch | agent",
  "acknowledged_at": "ISO8601"
}
```

A `task_ready` signal without a corresponding `task_acknowledged` within the same heartbeat window is eligible for re-emission.

---

## DecisionRecord (Triage extension)

```json
{
  "decision_id": "string — dec_<hash>",
  "timestamp": "ISO8601",
  "skill_id": "ocas-triage",
  "skill_version": "string",
  "decision_type": "string — preemption | task_expired | stall_detected | queue_rebuild | overflow_drop | heartbeat_assigned",
  "description": "string",
  "evidence_refs": ["string — task_ids involved"],
  "outcome": "string",
  "confidence": "high",
  "side_effects": "string | null",
  "triage_payload": {
    "active_task_id": "string | null",
    "new_task_id": "string | null",
    "score_delta": "number | null",
    "queue_depth_before": "number | null",
    "queue_depth_after": "number | null",
    "heartbeat_interval_seconds": "number | null"
  }
}
```

Note: `heartbeat_assigned` is a new `decision_type`. Emit a DecisionRecord for every Mentor handoff that includes heartbeat injection, logging the priority score and assigned interval.

---

## config.json

```json
{
  "skill_id": "ocas-triage",
  "skill_version": "1.2.0",
  "config_version": "string",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "max_queue_size": 50,
  "history_limit": 100,
  "default_task_ttl_days": 7,
  "stall_threshold_seconds": 120,
  "retry_limit": 3,
  "preemption_threshold": 25,
  "priority_update_interval_seconds": 60,
  "debounce_window_seconds": 1,
  "duplicate_similarity_threshold": 0.90,
  "duplicate_window_minutes": 5,
  "default_estimated_completion_seconds": 1800,
  "heartbeat_high_priority_seconds": 60,
  "heartbeat_medium_priority_seconds": 600,
  "heartbeat_low_priority_seconds": 3600
}
```

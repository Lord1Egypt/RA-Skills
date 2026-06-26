---
name: ocas-triage
description: System scheduler and priority queue manager. Determines what gets attention next across all pending work. Use when prioritizing competing tasks, checking queue state, preempting active work, auditing execution order, or passing a complex long-running task to Mentor. Assigns heartbeat cadence based on task priority before handoff.
metadata: {"openclaw":{"emoji":"🔀","version":"1.2.0"}}
---

# Triage

Triage is the system scheduler. Its only job is to determine what gets attention next. It maintains a durable priority queue, scores work deterministically, emits pickup signals, injects heartbeat cadence into Mentor handoffs, and handles interrupts.

## When to use

- Prioritize competing tasks
- Check queue state: "what are you working on", "what's pending"
- Interrupt active work: "stop and do this first"
- Add work to the queue
- Any complex multi-step task that requires Mentor

## When not to use

- Project orchestration internals — Mentor owns that
- Message drafting or inbox triage — use Dispatch
- Skill execution requests — route directly to the target skill
- Pattern analysis — use Corvus

## Core promise

One active task at a time. Deterministic scoring. Durable queue. Priority-linked heartbeat on every Mentor handoff. Every task logged.

---

## Meta commands (bypass queue, execute immediately)

```
status / what are you working on
stop / cancel that
pause / resume
```

Meta commands never appear in `queue.jsonl`.

---

## Task model

A task is created for every actionable input. Not created for: thanks, casual conversation, clarification, meta queries.

**States:** `queued` → `active` → `completed` or `cancelled`
Lateral: `blocked` (retries exceeded), `waiting_external` (awaiting response)

Read `references/schemas.md` for full schema and signal formats.

---

## Priority scoring

```
priority_score = urgency + deadline_proximity + consequence_weight +
                 interruption_intent + quick_completion_bonus + queue_aging
Clamp: 0–100
```

Read `references/scoring_model.md` for signal definitions, points, and examples.

---

## Mentor handoff with heartbeat injection

When Triage scores a task and determines it requires Mentor (`routing_hint: mentor`), it **must** inject a `heartbeat_interval` into the `task_ready` signal before emission. This is not optional.

### Heartbeat assignment rules

| Priority score | Heartbeat interval | Rationale |
|---|---|---|
| 70–100 (high) | 60 seconds | High-stakes work must surface stalls within 1 minute |
| 40–69 (medium) | 10 minutes | Sustained work; surface stalls before significant time is lost |
| 0–39 (low) | 1–6 hours | Background work; check-in at natural rest points |

For low-priority tasks, use 1 hour as the default. Scale toward 6 hours only if the task is explicitly flagged as non-urgent background work with no deadline.

### Extended task_ready signal (Mentor handoff)

```json
{
  "signal": "task_ready",
  "task_id": "string",
  "routing_hint": "mentor",
  "priority_score": 75,
  "heartbeat_interval_seconds": 60,
  "heartbeat_rationale": "high priority — stall detection required within 60s",
  "emitted_at": "ISO8601"
}
```

Mentor reads `heartbeat_interval_seconds` from the signal and configures its internal heartbeat loop before beginning work. If this field is absent from a Mentor-routed signal, Mentor defaults to 600 seconds (10 min) and logs a missing-heartbeat warning.

---

## Task selection and preemption

**Selection formula:** `task_score = priority_score / max(estimated_completion_seconds / 60, 1)`

**Preemption:** if new task priority exceeds active task by > 25 points, checkpoint active task and run higher-priority task first.

Read `references/scoring_model.md` for full preemption and tie-breaking rules.

---

## Stall detection

Stall threshold: 120 seconds of no progress on a non-Mentor task.
Retry limit: 3, exponential backoff.
On limit exceeded: `state → blocked`, `blocking_reason` logged.

For Mentor tasks, stall detection is delegated to Mentor's heartbeat loop (interval set at handoff). Triage does not independently poll Mentor-owned tasks.

---

## Queue pickup

Triage writes to `.triage/signals.jsonl`. Consumers poll this file.

`task_ready` — emitted when a task becomes active
`task_completed` — emitted on completion or cancellation
`task_acknowledged` — written by consumer to prevent double-pickup

Read `references/boundary_contracts.md` for consumer pickup protocol.

---

## Storage layout

```
.triage/
  config.json
  queue.jsonl        append-only; state transitions are new records per task_id
  signals.jsonl      task_ready, task_completed, task_acknowledged
  decisions.jsonl    DecisionRecord entries for preemption and scoring
  history.jsonl      completed/cancelled tasks, last 100
  journals/
  reports/
```

---

## Validation rules

- No two tasks simultaneously in `active` state
- Every Mentor-routed `task_ready` signal must include `heartbeat_interval_seconds`
- Meta commands never appear in `queue.jsonl`
- Preemption always produces a journal entry and DecisionRecord
- `waiting_external` tasks have non-null `blocking_reason`
- `history.jsonl` does not exceed 100 records
- Queue does not exceed 50 tasks

---

## Reference files

| File | When to read |
|---|---|
| `references/schemas.md` | Task, signal, DecisionRecord schemas; heartbeat signal extension |
| `references/scoring_model.md` | Full scoring formula, preemption rules, estimation heuristics |
| `references/boundary_contracts.md` | Consumer pickup protocol; Mentor, Dispatch, base agent boundaries |

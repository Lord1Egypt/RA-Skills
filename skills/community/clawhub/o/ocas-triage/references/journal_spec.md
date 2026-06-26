# Triage Journal Specification

Journal type: **Action Journal**
Journal spec version: 1.2 (spec-ocas-journal.md)

Triage scheduling decisions are actions — tasks are selected, emitted,
checkpointed, and completed. Every scheduling event is an action with an
auditable side effect.

---

## Events That Produce Journal Entries

One journal entry per event:

| Event | decision_type |
|---|---|
| Task created | `task_created` |
| Task scored (initial or recalculated) | `task_scored` |
| Task selected as active | `task_selected` |
| Preemption | `preemption` |
| Task completed | `task_completed` |
| Task cancelled | `task_cancelled` |
| Meta command executed | `meta_command` |
| Stall detected | `stall_detected` |
| Retry attempt | `retry_attempt` |
| Queue integrity rebuild | `queue_rebuild` |
| Queue overflow drop | `overflow_drop` |

---

## Journal Entry Structure

```json
{
  "run_identity": {
    "comparison_group_id": "string — generated before execution",
    "run_id": "string — r_<hash>",
    "role": "champion",
    "skill_name": "ocas-triage",
    "skill_version": "1.1.0",
    "timestamp_start": "ISO8601",
    "timestamp_end": "ISO8601",
    "normalized_input_hash": "sha256"
  },
  "runtime": {
    "model": "string | null",
    "provider": "string | null",
    "node": "string | null",
    "oc_version": "string | null"
  },
  "input": {
    "normalized_input_hash": "sha256",
    "input_schema_version": "1.0",
    "context_tokens": "number"
  },
  "decision": {
    "decision_type": "string — see event table above",
    "payload": {
      "task_id": "string",
      "priority_score": "number | null",
      "routing_hint": "string | null",
      "score_delta": "number | null",
      "preempted_task_id": "string | null",
      "queue_depth": "number"
    },
    "confidence": "high",
    "reasoning_summary": "string — brief human-readable explanation"
  },
  "action": {
    "side_effect_intent": "string — emit_task_ready | emit_task_completed | checkpoint_task | drop_task | rebuild_queue",
    "side_effect_executed": "boolean"
  },
  "artifacts": [],
  "metrics": {
    "latency_ms": "number",
    "queue_depth": "number",
    "retry_count": "number",
    "validation_failures": "number",
    "context_tokens_used": "number"
  },
  "okr_evaluation": {
    "success_rate": "number",
    "retry_rate": "number",
    "validation_failure_rate": "number",
    "repair_events": "number",
    "context_utilization": "number",
    "journal_completeness": 1.0,
    "tasks_completed_today": "number",
    "preemptions_today": "number",
    "tasks_waiting_gt_4hr": "number",
    "meta_command_latency_ms": "number | null",
    "scoring_consistency": "number",
    "duplicates_correctly_merged": "number",
    "estimation_within_bucket": "number"
  },
  "journal_type": "Action",
  "journal_spec_version": "1.2"
}
```

---

## Universal OKRs

Required by spec-ocas-journal.md §13. Evaluated on every run.

| OKR | Metric | Target |
|---|---|---|
| Reliability | `success_rate` | ≥ 0.95 |
| Reliability | `retry_rate` | ≤ 0.10 |
| Validation integrity | `validation_failure_rate` | ≤ 0.05 |
| Efficiency | `latency_ms` | trending downward |
| Efficiency | `repair_events` | ≤ 0.05 |
| Context stability | `context_utilization` | ≤ 0.70 |
| Observability | `journal_completeness` | = 1.0 |

---

## Triage-Specific OKRs

Evaluated over rolling windows. Defined per spec-ocas-journal.md §14.

```yaml
skill_okrs:
  - name: throughput
    metric: tasks_completed_per_day
    direction: maximize
    target: trending_upward
    evaluation_window: 30_days

  - name: preemption_rate
    metric: preemptions_per_day
    direction: minimize
    target: 3
    evaluation_window: 30_days

  - name: starvation_rate
    metric: tasks_waiting_gt_4hr_ratio
    direction: minimize
    target: 0.05
    evaluation_window: 30_runs

  - name: meta_command_latency
    metric: meta_command_latency_ms
    direction: minimize
    target: 500
    evaluation_window: 30_runs

  - name: scoring_consistency
    metric: identical_input_identical_score_rate
    direction: maximize
    target: 1.0
    evaluation_window: 30_runs

  - name: duplicate_detection_accuracy
    metric: correctly_merged_duplicates_ratio
    direction: maximize
    target: 0.90
    evaluation_window: 30_runs

  - name: estimation_accuracy
    metric: actual_completion_within_bucket_rate
    direction: maximize
    target: 0.75
    evaluation_window: 30_runs
```

---

## Journal Storage

Journal entries are written to `.triage/journals/` as individual files:

```
.triage/journals/
  <date>/
    <run_id>.json
```

Example: `.triage/journals/2026-03-14/r_91d28e1.json`

Journal files are immutable after write (spec-ocas-journal.md §17).

---

## Champion / Challenger Pairing

Triage generates a `comparison_group_id` before each scheduling run. This
enables Mentor to pair champion and challenger runs for evaluation.

The `comparison_group_id` is written to the journal entry before execution
begins — not after.

Challenger variants of Triage must set `side_effect_executed: false` in the
action block. They must not emit signals to `.triage/signals.jsonl`.

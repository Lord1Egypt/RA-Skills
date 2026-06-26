# Event Schema

Events are append-only JSONL records stored per run.

Core event types:

- `message_received`
- `run_started`
- `skill_invoked`
- `skill_completed`
- `tool_called`
- `artifact_created`
- `state_changed`
- `summary_refreshed`
- `blocker_detected`
- `human_decision_requested`
- `human_decision_resolved`
- `external_trigger_bound`
- `session_shared`
- `session_archived`
- `checkpoint_restored`
- `spool_appended`
- `attention_escalated`
- `capability_fact_derived`

The event log is the fact base for:

- recovery
- observability
- attention scoring
- run evidence snapshots
- closure metrics
- capability distillation

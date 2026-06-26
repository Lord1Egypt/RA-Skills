# Journal

Corvus produces journals per spec-ocas-journal.md v1.3. Write a journal at the end of every run. Runs missing journals are invalid.

Journal path: `~/openclaw/journals/ocas-corvus/YYYY-MM-DD/{run_id}.json`

Written atomically (write to `.tmp`, then rename). Never edit after writing.

## Journal type

All Corvus journals are Observation Journals. Corvus analyzes patterns and discovers signals -- no external side effects.

## Journal structure

```json
{
  "run_identity": {
    "comparison_group_id": "cg_xxxxxxx",
    "run_id": "r_xxxxxxx",
    "role": "champion",
    "skill_name": "ocas-corvus",
    "skill_version": "2.0.0",
    "timestamp_start": "2026-03-17T10:00:00-07:00",
    "timestamp_end": "2026-03-17T10:00:05-07:00",
    "normalized_input_hash": "sha256:...",
    "journal_spec_version": "1.3",
    "journal_type": "observation"
  },
  "runtime": {
    "model": "claude-sonnet-4-6",
    "provider": "anthropic",
    "temperature": null,
    "context_window": "200k",
    "node": "macstudio-01",
    "oc_version": "2026.1.30"
  },
  "input": {
    "normalized_input_hash": "sha256:...",
    "input_schema_version": "1.0",
    "context_tokens": 0,
    "command": ""
  },
  "decision": {
    "decision_type": "",
    "payload": {},
    "confidence": 1.0,
    "reasoning_summary": ""
  },
  "action": {
    "side_effect_intent": null,
    "side_effect_executed": false,
    "reason": "observation_run"
  },
  "artifacts": [],
  "metrics": {
    "latency_ms": 0,
    "retry_count": 0,
    "validation_failures": 0,
    "context_tokens_used": 0,
    "records_written": 0,
    "records_skipped": 0,
    "records_failed": 0
  },
  "okr_evaluation": {
    "success_rate": 1.0,
    "latency_score": null,
    "reliability_score": 1.0,
    "proposal_precision": null,
    "pattern_validation_rate": null,
    "graph_coverage": null,
    "false_anomaly_rate": null
  }
}
```

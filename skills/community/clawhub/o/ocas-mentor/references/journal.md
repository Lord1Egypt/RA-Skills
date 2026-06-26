# Journal

Mentor produces Action Journals per spec-ocas-journal.md v1.3. Write a journal at the end of every run. Runs missing journals are invalid.

Journal path: `~/openclaw/journals/ocas-mentor/YYYY-MM-DD/{run_id}.json`

Written atomically (write to `.tmp`, then rename). Never edit after writing.

## Journal type

All Mentor journals are Action Journals. Mentor orchestrates tasks and evaluates variants -- these are consequential decisions.

## Journal structure

```json
{
  "run_identity": {
    "comparison_group_id": "cg_xxxxxxx",
    "run_id": "r_xxxxxxx",
    "role": "champion",
    "skill_name": "ocas-mentor",
    "skill_version": "2.0.0",
    "timestamp_start": "2026-03-17T10:00:00-07:00",
    "timestamp_end": "2026-03-17T10:05:00-07:00",
    "normalized_input_hash": "sha256:...",
    "journal_spec_version": "1.3",
    "journal_type": "action"
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
    "command": "mentor.heartbeat.deep"
  },
  "decision": {
    "decision_type": "heartbeat_evaluation",
    "payload": {},
    "confidence": 0.90,
    "reasoning_summary": ""
  },
  "action": {
    "side_effect_intent": "variant_proposal",
    "side_effect_executed": true,
    "external_reference": null
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
    "orchestration_success_rate": null,
    "evaluation_coverage": null,
    "variant_decision_quality": null,
    "repair_escalation_rate": null
  }
}
```

## Decision payload by command

mentor.heartbeat.light / .deep:
- `journals_scanned`, `journals_ingested`, `skills_evaluated`, `anomalies_detected`, `proposals_generated`

mentor.project.create:
- `project_id`, `goal`, `task_count`, `estimated_duration`

mentor.variants.decide:
- `variant_id`, `target_skill`, `decision`, `rationale`, `aggregate_scores`

mentor.proposals.create:
- `proposal_id`, `target_skill`, `observed_problem`, `expected_improvement`

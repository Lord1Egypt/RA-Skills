# Journal

Forge produces Action Journals per spec-ocas-journal.md v1.3. Write a journal at the end of every run. Runs missing journals are invalid.

Journal path: `~/openclaw/journals/ocas-forge/YYYY-MM-DD/{run_id}.json`

Written atomically (write to `.tmp`, then rename). Never edit after writing.

## Journal type

All Forge journals are Action Journals. Forge builds skill packages — these are consequential outputs.

## Journal structure

```json
{
  "run_identity": {
    "comparison_group_id": "cg_xxxxxxx",
    "run_id": "r_xxxxxxx",
    "role": "champion",
    "skill_name": "ocas-forge",
    "skill_version": "2.0.0",
    "timestamp_start": "2026-03-17T10:00:00-07:00",
    "timestamp_end": "2026-03-17T10:02:00-07:00",
    "normalized_input_hash": "sha256:...",
    "journal_spec_version": "1.3",
    "journal_type": "action"
  },
  "runtime": {
    "model": "claude-sonnet-4-6",
    "provider": "anthropic"
  },
  "input": {
    "normalized_input_hash": "sha256:...",
    "input_schema_version": "1.0",
    "context_tokens": 0,
    "command": "forge.build"
  },
  "decision": {
    "decision_type": "skill_build",
    "payload": {
      "target_skill": "ocas-example",
      "skill_type": "workflow",
      "files_created": 3,
      "validation_passed": true
    },
    "confidence": 0.95,
    "reasoning_summary": ""
  },
  "action": {
    "side_effect_intent": "package_creation",
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
    "reliability_score": 1.0,
    "build_completion_rate": null,
    "validation_pass_rate": null,
    "variant_build_success": null
  }
}
```

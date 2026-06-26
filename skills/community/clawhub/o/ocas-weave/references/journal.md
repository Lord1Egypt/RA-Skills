# Journal

Weave produces journals per spec-ocas-journal.md v1.3. Write a journal at the end of every run that modifies data or produces a query result. Runs missing journals are invalid.

Journal path: `~/openclaw/journals/ocas-weave/YYYY-MM-DD/{run_id}.json`

Journals are written atomically (write to `.tmp`, then rename). Never edit after writing.

## Journal type selection

Observation Journal -- query runs, upsert runs, import runs (no external side effects)
Action Journal -- sync runs, writeback runs (external side effects executed)

## Journal structure

```json
{
  "run_identity": {
    "comparison_group_id": "cg_xxxxxxx",
    "run_id": "r_xxxxxxx",
    "role": "champion",
    "skill_name": "ocas-weave",
    "skill_version": "2.0.0",
    "timestamp_start": "2026-03-17T10:00:00-07:00",
    "timestamp_end": "2026-03-17T10:00:04-07:00",
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
    "command": "weave.upsert.person"
  },
  "decision": {
    "decision_type": "observation",
    "payload": {
      "entities_observed": [],
      "relationships_observed": [],
      "preferences_observed": []
    },
    "confidence": 1.0,
    "reasoning_summary": "Upserted 1 Person record."
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
    "records_written": 1,
    "records_skipped": 0,
    "records_failed": 0
  },
  "okr_evaluation": {
    "success_rate": 1.0,
    "latency_score": null,
    "reliability_score": 1.0,
    "person_record_completeness": null,
    "sync_success_rate": null,
    "import_skip_rate": null,
    "query_provenance_coverage": null
  }
}
```

For sync/writeback runs, change journal_type to `"action"` and set `action.side_effect_executed: true`.

## Python helper

```python
import json, uuid
from datetime import datetime, timezone
from pathlib import Path

JOURNALS = Path("~/openclaw/journals/ocas-weave").expanduser()

def start_run():
    return {
        "run_id": "r_" + uuid.uuid4().hex[:7],
        "comparison_group_id": "cg_" + uuid.uuid4().hex[:7],
        "timestamp_start": datetime.now(timezone.utc).isoformat()
    }

def write_journal(run_ctx: dict, command: str, decision_payload: dict,
                  metrics: dict, journal_type: str = "observation"):
    ended = datetime.now(timezone.utc).isoformat()
    date_str = ended[:10]
    journal_dir = JOURNALS / date_str
    journal_dir.mkdir(parents=True, exist_ok=True)
    journal_path = journal_dir / f"{run_ctx['run_id']}.json"

    entry = {
        "run_identity": {
            "comparison_group_id": run_ctx["comparison_group_id"],
            "run_id": run_ctx["run_id"],
            "role": "champion",
            "skill_name": "ocas-weave",
            "skill_version": "2.0.0",
            "timestamp_start": run_ctx["timestamp_start"],
            "timestamp_end": ended,
            "normalized_input_hash": run_ctx.get("input_hash", ""),
            "journal_spec_version": "1.3",
            "journal_type": journal_type
        },
        "input": {
            "normalized_input_hash": run_ctx.get("input_hash", ""),
            "input_schema_version": "1.0",
            "context_tokens": 0,
            "command": command
        },
        "decision": {
            "decision_type": "observation" if journal_type != "action" else "action",
            "payload": decision_payload,
            "confidence": metrics.get("confidence", 1.0),
            "reasoning_summary": metrics.get("reasoning_summary", "")
        },
        "action": {
            "side_effect_intent": metrics.get("side_effect_intent"),
            "side_effect_executed": journal_type == "action",
            "reason": None if journal_type == "action" else "observation_run"
        },
        "artifacts": metrics.get("artifacts", []),
        "metrics": {
            "latency_ms": metrics.get("latency_ms", 0),
            "retry_count": metrics.get("retry_count", 0),
            "validation_failures": metrics.get("validation_failures", 0),
            "context_tokens_used": 0,
            "records_written": metrics.get("records_written", 0),
            "records_skipped": metrics.get("records_skipped", 0),
            "records_failed": metrics.get("records_failed", 0)
        },
        "okr_evaluation": metrics.get("okr_evaluation", {
            "success_rate": 1.0 if metrics.get("records_failed", 0) == 0 else 0.0,
            "reliability_score": 1.0
        })
    }

    tmp = journal_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(entry, indent=2))
    tmp.rename(journal_path)
    return str(journal_path)
```

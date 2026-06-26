# Journal

Elephas produces Action Journals per spec-ocas-journal.md v1.3. Write a journal at the end of every run that makes a decision — consolidation, promotion, merge, rejection, ingestion. Runs missing journals are invalid.

Journal path: `~/openclaw/journals/ocas-elephas/YYYY-MM-DD/{run_id}.json`

Written atomically (write to `.tmp`, then rename). Never edit after writing.

## Journal type

All Elephas journals are Action Journals. Elephas writes to Chronicle — those are consequential side effects that Praxis and Mentor evaluate to improve consolidation quality over time.

Exception: `elephas.ingest.journals` runs that only scan and create Signals (no promotions or merges) may use Observation Journal type.

## Journal structure

```json
{
  "run_identity": {
    "comparison_group_id": "cg_xxxxxxx",
    "run_id": "r_xxxxxxx",
    "role": "champion",
    "skill_name": "ocas-elephas",
    "skill_version": "2.0.0",
    "timestamp_start": "2026-03-17T10:00:00-07:00",
    "timestamp_end": "2026-03-17T10:00:09-07:00",
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
    "command": "elephas.consolidate.immediate",
    "journals_scanned": 14,
    "signals_found": 6
  },
  "decision": {
    "decision_type": "consolidation",
    "payload": {
      "candidates_evaluated": 8,
      "candidates_promoted": 3,
      "candidates_rejected": 1,
      "candidates_flagged": 2,
      "identities_merged": 0,
      "identities_flagged": 1,
      "inferences_generated": 0,
      "promotions": [
        {"candidate_id": "cand_abc", "entity_name": "Jane Doe", "confidence": "high",
         "reason": "email identifier match across 2 skills"}
      ],
      "rejections": [
        {"candidate_id": "cand_xyz", "reason": "contradicted by higher-confidence signal from Scout"}
      ]
    },
    "confidence": 0.92,
    "reasoning_summary": "Immediate consolidation: 3 high-confidence candidates promoted, 1 rejected."
  },
  "action": {
    "side_effect_intent": "chronicle_write",
    "side_effect_executed": true,
    "external_reference": null
  },
  "artifacts": [],
  "metrics": {
    "latency_ms": 1840,
    "retry_count": 0,
    "validation_failures": 0,
    "context_tokens_used": 0,
    "records_written": 3,
    "records_skipped": 2,
    "records_failed": 0
  },
  "okr_evaluation": {
    "success_rate": 1.0,
    "latency_score": null,
    "reliability_score": 1.0,
    "promotion_precision": null,
    "identity_merge_accuracy": null,
    "candidate_queue_age": null,
    "ingestion_coverage": null
  }
}
```

## Decision payload by command

elephas.consolidate.immediate / .deep:
- `candidates_evaluated`, `candidates_promoted`, `candidates_rejected`, `candidates_flagged`
- `identities_merged`, `identities_flagged`, `inferences_generated`
- `promotions[]` — list of {candidate_id, entity_name, confidence, reason}
- `rejections[]` — list of {candidate_id, reason}

elephas.identity.merge:
- `merged_entity_a`, `merged_entity_b`, `surviving_entity`, `reason`

elephas.candidates.promote (manual):
- `candidate_id`, `entity_name`, `promoted_by: "manual"`

elephas.candidates.reject (manual):
- `candidate_id`, `reason`, `rejected_by: "manual"`

elephas.ingest.journals:
- `journals_scanned`, `journals_ingested`, `signals_created`, `candidates_created`
- Use `journal_type: "observation"` for scan-only runs with no Chronicle writes

## Python helper

```python
import json, uuid
from datetime import datetime, timezone
from pathlib import Path

JOURNALS = Path("~/openclaw/journals/ocas-elephas").expanduser()

def start_run():
    return {
        "run_id": "r_" + uuid.uuid4().hex[:7],
        "comparison_group_id": "cg_" + uuid.uuid4().hex[:7],
        "timestamp_start": datetime.now(timezone.utc).isoformat()
    }

def write_journal(run_ctx: dict, command: str, decision_payload: dict,
                  metrics: dict, journal_type: str = "action"):
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
            "skill_name": "ocas-elephas",
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
            "decision_type": "consolidation",
            "payload": decision_payload,
            "confidence": metrics.get("confidence", 1.0),
            "reasoning_summary": metrics.get("reasoning_summary", "")
        },
        "action": {
            "side_effect_intent": "chronicle_write",
            "side_effect_executed": journal_type == "action",
            "external_reference": None
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

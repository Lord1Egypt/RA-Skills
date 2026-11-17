# OCAS Shared Schemas

Spec Version: 1.1.4
Author: Indigo Karasu

Changes from 1.2: added PortfolioOutcomeRecord schema (Rally domain extension); added ConsumptionSignal and ItemRecord schemas (Taste domain extensions); added EvaluationResult schema (Mentor domain extension).

Changes from 1.0: updated JournalEntry minimum fields to match journal spec v1.3 (added journal_type, journal_spec_version); updated ConfigBase to reference central storage path; added InsightProposal schema (Corvus output); added BehavioralSignal schema (Corvus→Praxis); added VariantProposal and VariantDecision schemas (Mentor→Forge); clarified extension rules.

---

## Purpose

This document defines canonical schemas for data objects that appear across multiple OCAS skills. Skills reference these definitions rather than redefining them independently.

Skills may extend these schemas with domain-specific fields. Base fields defined here must be present and semantically consistent.

---

## DecisionRecord

Used by: all skills that make consequential decisions.

Every decision that changes behavior, triggers an external action, or produces an interpretive output should be recorded as a DecisionRecord.

```json
{
  "decision_id": "string — unique identifier (dec_{hash})",
  "timestamp": "string — ISO 8601",
  "skill_id": "string — which skill made the decision",
  "skill_version": "string",
  "decision_type": "string — skill-defined category (e.g., route, execute, promote, ingest, safety)",
  "description": "string — brief human-readable summary",
  "evidence_refs": ["string — references to signals, sources, or artifacts that informed the decision"],
  "outcome": "string — what was decided",
  "confidence": "string — high|med|low",
  "side_effects": "string|null — description of any external effects"
}
```

---

## Signal

Used by: skills that emit observations to be ingested by Elephas.

See `spec-ocas-ontology.md` for the full evidence model and signal delivery mechanism.

```json
{
  "signal_id": "string — unique identifier (sig_{hash})",
  "timestamp": "string — ISO 8601",
  "source_skill": "string — skill that emitted the signal",
  "source_journal_type": "string — Observation|Action|Research",
  "payload": {
    "type": "string — entity type or signal category",
    "data": "object — the observed information"
  },
  "confidence": "string — high|med|low",
  "status": "string — active|consumed"
}
```

---

## Candidate

Used by: skills that propose new facts for Chronicle.

```json
{
  "candidate_id": "string — unique identifier",
  "timestamp": "string — ISO 8601",
  "source_skill": "string",
  "proposed_node": {
    "type": "string — Entity|Place|Concept|Thing or subclass",
    "data": "object — the proposed record"
  },
  "supporting_signals": ["string — signal_ids"],
  "confidence": "string — high|med|low",
  "status": "string — pending|confirmed|rejected|merged"
}
```

---

## InsightProposal

Used by: Corvus (output), Vesper (input), Praxis (input for behavioral signals).

```json
{
  "proposal_id": "string — unique identifier",
  "proposal_type": "string — routine_prediction|thread_continuation|opportunity_discovery|anomaly_alert|behavioral_signal",
  "description": "string — human-readable description of the insight",
  "confidence_score": "number — 0.0 to 1.0",
  "supporting_entities": ["string — entity or node IDs from Chronicle or Weave"],
  "supporting_relationships": ["string — relationship IDs"],
  "predicted_outcome": "string|null",
  "suggested_follow_up": "string|null",
  "target_skill": "string|null — for behavioral_signal type, the skill this proposal is directed to",
  "created_at": "string — ISO 8601"
}
```

Proposal type `behavioral_signal` is used when Corvus detects an anomaly or pattern that should be reviewed by Praxis for potential behavior shift extraction.

---

## BehavioralSignal

Used by: Corvus (writes to Praxis intake), Praxis (reads from intake).

Written to: `{agent_root}/commons/data/ocas-praxis/intake/{signal_id}.json`

```json
{
  "signal_id": "string — unique identifier",
  "source_skill": "ocas-corvus",
  "timestamp": "string — ISO 8601",
  "signal_type": "string — anomaly_detected|pattern_validated|regression_flagged",
  "target_skill": "string — skill the behavior concerns",
  "description": "string — what was observed",
  "evidence_refs": ["string — journal run_ids or pattern_ids that support this"],
  "confidence": "string — high|med|low",
  "suggested_event_type": "string|null — suggested Praxis event_type for lesson extraction"
}
```

---

## VariantProposal

Used by: Mentor (writes to Forge intake), Forge (reads from intake).

Written to: `{agent_root}/commons/data/ocas-forge/intake/{proposal_id}.json`

```json
{
  "proposal_id": "string — unique identifier",
  "source_skill": "ocas-mentor",
  "timestamp": "string — ISO 8601",
  "target_skill": "string — skill to improve",
  "base_version": "string — current champion version",
  "observed_problem": "string — what is underperforming",
  "supporting_evidence": ["string — journal run_ids, OKR scores, or evaluation IDs"],
  "proposed_changes": "string — description of what should change",
  "expected_improvement": "string — which OKR metric and by how much",
  "evaluation_plan": "string — how the variant will be tested",
  "minimum_runs": "number — minimum runs before promotion decision",
  "critical_non_regression_conditions": ["string — OKRs that must not regress"]
}
```

---

## VariantDecision

Used by: Mentor (writes), Forge (reads and acts on).

Written to: `{agent_root}/commons/data/ocas-forge/intake/{decision_id}.json`

```json
{
  "decision_id": "string — unique identifier",
  "variant_id": "string",
  "target_skill": "string",
  "decision": "string — promote|continue_testing|archive|reject|emergency_rollback",
  "rationale": "string",
  "aggregate_scores": "object — OKR scores across evaluation window",
  "confidence": "string — high|med|low",
  "non_regression_check": "boolean",
  "evaluation_window_runs": "number",
  "timestamp": "string — ISO 8601"
}
```

---

## LogEvent

Used by: skills that maintain append-only event logs.

```json
{
  "event_id": "string — unique identifier (evt_{hash})",
  "timestamp": "string — ISO 8601",
  "skill_id": "string",
  "event_type": "string — skill-defined category",
  "summary": "string — brief human-readable description",
  "data": "object|null — event-specific payload",
  "related_ids": ["string — references to related records"]
}
```

---

## SkillStatus

Used by: all skills via their `.status` command.

```json
{
  "skill_id": "string",
  "skill_version": "string",
  "timestamp": "string — ISO 8601",
  "state": "string — healthy|degraded|error",
  "summary": "string — brief human-readable status",
  "metrics": "object — skill-specific status metrics"
}
```

---

## JournalEntry

Used by: all skills that write journal entries.

See `spec-ocas-journal.md` for the full specification including champion/challenger pairing, OKR evaluation, and runtime telemetry.

Minimum required fields:

```json
{
  "run_id": "string — unique run identifier (r_{hash})",
  "comparison_group_id": "string — (cg_{hash})",
  "role": "string — champion|challenger",
  "skill_name": "string",
  "skill_version": "string",
  "journal_spec_version": "1.3",
  "journal_type": "string — observation|action|research",
  "timestamp_start": "string — ISO 8601",
  "timestamp_end": "string — ISO 8601",
  "normalized_input_hash": "string — sha256:...",
  "decision": "object — what was decided or produced",
  "metrics": "object — run metrics",
  "okr_evaluation": "object — universal and skill-specific OKR scores"
}
```

---

## ConfigBase

Used by: all skills that maintain a config file.

Every skill's `config.json` at `{agent_root}/commons/data/{skill-name}/config.json` includes these base fields plus skill-specific configuration:

```json
{
  "skill_id": "string",
  "skill_version": "string",
  "config_version": "string — incremented on config changes",
  "created_at": "string — ISO 8601",
  "updated_at": "string — ISO 8601"
}
```

---

## ExperimentRequest

Used by: Mentor (writes to Fellow intake), Fellow (reads from intake).

Written to: `{agent_root}/commons/data/ocas-fellow/intake/{experiment_id}.json`

```json
{
  "experiment_id": "string — unique identifier (exp_{hash})",
  "source_skill": "ocas-mentor",
  "timestamp": "string — ISO 8601",
  "target": "string — component identifier (skill name, heuristic id, or workflow path)",
  "program_id": "string — experiment program identifier",
  "objective": "string — primary metric to optimize",
  "benchmark": "string — benchmark identifier",
  "budget": {
    "type": "string — wall_clock | task_count | token_budget | simulation_window",
    "value": "number"
  },
  "constraints": {
    "max_variants": "number",
    "max_cycles": "number",
    "mutation_surface": ["string — paths or fields eligible for mutation"],
    "protected_surface": ["string — paths or fields that must not change"]
  },
  "promotion": {
    "threshold": "number — minimum improvement required (e.g., 0.03)",
    "automatic": "boolean — promote without manual approval if threshold met",
    "rollback_on_regression": true
  },
  "runner": {
    "type": "string — command | function | workflow",
    "entrypoint": "string",
    "timeout_seconds": "number"
  },
  "metric_extractor": {
    "type": "string — json | regex | function | structured_output",
    "source": "string — artifact path or journal field",
    "selector": "string — field path or regex pattern"
  }
}
```

---

## CycleResult

Used by: Fellow (writes to Mentor intake), Mentor (reads from intake).

Written to: `{agent_root}/commons/data/ocas-mentor/intake/{cycle_id}.json`

```json
{
  "cycle_id": "string — unique identifier (cyc_{hash})",
  "experiment_id": "string — references the ExperimentRequest that triggered this cycle",
  "source_skill": "ocas-fellow",
  "timestamp": "string — ISO 8601",
  "target": "string — component that was evaluated",
  "baseline_score": "number",
  "best_variant_id": "string | null — null if no variant beat the baseline",
  "best_variant_score": "number | null",
  "improvement": "number | null — best_variant_score minus baseline_score",
  "decision": "string — promote | no_change | abort",
  "artifacts_ref": "string | null — path to variant artifacts",
  "rollback_ref": "string | null — path to rollback snapshot",
  "abort_reason": "string | null — populated when decision is abort"
}
```

---

## Domain Extension Schemas

The schemas below are skill-specific extensions of shared base schemas. They are documented here for cross-skill discoverability. Each extension follows the rules in the Extension Rules section — base fields are preserved.

---

### PortfolioOutcomeRecord

**Extends:** JournalEntry (decision field)
**Used by:** Rally (writes), Vesper (reads via cooperative interface)
**Written to:** `{agent_root}/commons/data/ocas-rally/reports/YYYY-MM-DD-daily.json`

```json
{
  "report_date": "string — ISO 8601 date",
  "portfolio_value": "number — total portfolio value in USD",
  "daily_return": "number — daily return as decimal (e.g., 0.012 = 1.2%)",
  "ytd_return": "number — year-to-date return",
  "drawdown": "number — current drawdown from peak as decimal",
  "regime_score": "number — 0.0 to 1.0, market regime assessment",
  "top_movers": [
    {
      "ticker": "string",
      "pct_change": "number",
      "direction": "string — up|down"
    }
  ],
  "allocation_changes": [
    {
      "ticker": "string",
      "from_weight": "number",
      "to_weight": "number",
      "reason": "string"
    }
  ],
  "risk_flags": ["string — active risk constraint violations or warnings"],
  "factor_ic": "object | null — information coefficient by factor, if computed",
  "generated_at": "string — ISO 8601"
}
```

Vesper reads `top_movers`, `risk_flags`, `daily_return`, and `allocation_changes` for briefing inclusion.

---

### ConsumptionSignal

**Extends:** Signal (payload.data)
**Used by:** Taste (writes internally)
**Written to:** `{agent_root}/commons/data/ocas-taste/signals.jsonl`

This schema is Taste-internal. It is not emitted to Elephas. It represents a single observed consumption event.

```json
{
  "signal_id": "string — sig_{hash}",
  "timestamp": "string — ISO 8601",
  "source_skill": "ocas-taste",
  "source_journal_type": "Observation",
  "payload": {
    "type": "string — item|venue|media|product|concept",
    "item_id": "string — reference to ItemRecord",
    "action": "string — consumed|saved|skipped|dismissed|rated",
    "rating": "number | null — 1–5 if rated",
    "context": "string | null — situational context if available"
  },
  "confidence": "string — high|med|low",
  "status": "string — active|consumed"
}
```

---

### ItemRecord

**Used by:** Taste (writes internally)
**Written to:** `{agent_root}/commons/data/ocas-taste/items.jsonl`

```json
{
  "item_id": "string — item_{hash}",
  "item_type": "string — venue|media|product|concept",
  "name": "string",
  "attributes": "object — type-specific attributes (e.g., cuisine, genre, category)",
  "first_seen": "string — ISO 8601",
  "last_seen": "string — ISO 8601",
  "signal_count": "number",
  "aggregate_strength": "number — 0.0 to 1.0"
}
```

---

### EvaluationResult

**Used by:** Mentor (writes internally)
**Written to:** `{agent_root}/commons/data/ocas-mentor/evaluations/{evaluation_id}.json`

```json
{
  "evaluation_id": "string — eval_{hash}",
  "target_skill": "string",
  "evaluated_at": "string — ISO 8601",
  "evaluation_window_runs": "number",
  "okr_scores": "object — universal and domain OKR scores",
  "trend": "string — improving|stable|degrading",
  "regression_flags": ["string — OKRs below threshold"],
  "recommendation": "string — continue|investigate|propose_variant",
  "notes": "string | null"
}
```

---

## Extension Rules

Skills may extend any shared schema by adding fields. They must not:
- Remove or rename base fields
- Change the semantic meaning of base fields
- Change the type of base fields

Extended schemas document which base schema they extend and what fields they add.
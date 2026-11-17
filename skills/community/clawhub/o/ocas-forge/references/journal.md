# OCAS Journals & Evaluation Specification

Spec Version: 1.2.3
Versioning Policy: Minor version increments only. Major versions avoided to maintain compatibility.

Changes from 1.2: canonicalized this file's own name to spec-ocas-journal.md (was inconsistently referenced as spec-ocas-Journals.md in some skill specs -- use spec-ocas-journal.md everywhere); added journal directory path (`~/openclaw/journals/{skill-name}/YYYY-MM-DD/{run_id}.json`); added Thread to Observation Journal consumers; added Elephas and Weave to journal emitters; added journal path to section 3; clarified champion/challenger directory structure.

---

## 1. Naming Convention

Skill identifiers must use hyphenated names to avoid namespace conflicts.

Examples:
- `ocas-scout`
- `ocas-rally`
- `ocas-taste`
- `ocas-mentor`
- `ocas-forge`

Variant naming: `ocas-rally-variant-20260307`

Dots must not be used because some runtimes interpret them as hierarchy separators.

---

## 2. Journal System Overview

The journal system provides three capabilities:

1. **Traceability** — every run can be reconstructed
2. **Comparability** — champion and challenger runs can be paired
3. **Optimization** — Mentor can evaluate runs against OKRs

Journals are append-only structured telemetry bundles produced by every skill run. Journals are immutable and never edited after completion.

Conceptual model per journal entry:
- run_identity
- runtime
- input
- decision
- action
- artifacts
- metrics
- okr_evaluation

---

## 2.1 Journal Types

Three formal artifact classes:

### Observation Journal

Purpose: Record signals discovered by the system. No external side effects.

Used by: Corvus, Sift, Scout, Look, Weave (read/query runs), Taste, Rally (research phase), Thread, Relay

Example:
```yaml
observation_journal:
  source: sift
  entities_detected:
    - LadybugDB
    - graph database
  confidence: medium
```

### Action Journal

Purpose: Record actions executed by the system. External side effects occurred.

Used by: Praxis, Dispatch, Voyage, Rally (execution phase), Mentor, Vesper, Forge, Elephas, Weave (sync/writeback runs), Fellow

Example:
```yaml
action_journal:
  action: reservation_booked
  place: natuRe Waikiki
  time: 7:30pm
```

### Research Journal

Purpose: Record research sessions and sources.

Used by: Sift, Scout

Example:
```yaml
research_journal:
  query: embedded graph database
  sources:
    - ladybugdb.com
    - neo4j.com
  entities:
    - LadybugDB
    - Neo4j
```

Elephas ingests all journal types into Chronicle. Mentor reads all journal types for evaluation.

---

## 3. Journal Directory Structure

All journals are written to the central journal root. Skills do not store journals inside their data directories or skill packages.

```
~/openclaw/journals/{skill-name}/YYYY-MM-DD/{run_id}.json
```

Example standard run:
```
~/openclaw/journals/ocas-scout/
  2026-03-17/
    r_91d28e1.json
    r_a7f2c1.json
```

Example champion/challenger pair:
```
~/openclaw/journals/ocas-rally/
  2026-03-07/
    cg_5cfa2c1/
      champion.json
      challenger.json
```

---

## 4. Pairing Champion and Challenger Runs

Champion and challenger runs are paired through a shared `comparison_group_id` generated before execution begins.

```
comparison_group_id
  champion run_id
  challenger run_id
```

Neither run needs awareness of the other. Each writes its own journal using the same group identifier. Both files land in the same date directory.

---

## 5. Run Identity Block

Every journal entry begins with run identity.

```yaml
run_identity:
  comparison_group_id: cg_5cfa2c1
  run_id: r_91d28e1
  role: champion        # champion | challenger
  skill_name: ocas-rally
  skill_version: 1.3.2
  variant_parent: 1.3.2
  timestamp_start: 2026-03-07T22:13:01Z
  timestamp_end: 2026-03-07T22:13:05Z
  normalized_input_hash: sha256:...
  journal_spec_version: "1.3"
  journal_type: observation   # observation | action | research
```

Required fields: `comparison_group_id`, `run_id`, `role`, `skill_name`, `skill_version`, `timestamp_start`, `timestamp_end`, `normalized_input_hash`, `journal_spec_version`, `journal_type`.

---

## 6. Runtime Telemetry

```yaml
runtime:
  model: claude-sonnet-4-6
  provider: anthropic
  temperature: 0.2
  context_window: 200k
  node: macstudio-01
  oc_version: 2026.1.30
```

Capturing model information enables skill-to-model pairing analysis over time.

---

## 7. Input Record

Inputs must be normalized so champion and challenger runs use identical data.

```yaml
input:
  normalized_input_hash: sha256:...
  input_schema_version: "1.0"
  context_tokens: 4820
  command: scout.research.start
```

---

## 8. Decision Record

All runs record decisions. Variants record decisions but must never execute side effects.

```yaml
decision:
  decision_type: research_completed
  payload:
    subject: Jane Doe
    tiers_used: [1, 2]
    findings_count: 12
  confidence: 0.85
  reasoning_summary: Sufficient Tier 1 and 2 coverage for stated goal.
```

---

## 9. Action Record

Champion runs may execute actions. Variants must not.

Champion:
```yaml
action:
  side_effect_intent: execute_trade
  side_effect_executed: true
  external_reference: broker_order_id_abc123
```

Variant (challenger):
```yaml
action:
  side_effect_intent: execute_trade
  side_effect_executed: false
  reason: shadow_run
```

---

## 10. Artifact Manifest

```yaml
artifacts:
  - research.md
  - analysis.json
```

---

## 11. Metrics Snapshot

```yaml
metrics:
  latency_ms: 412
  retry_count: 0
  validation_failures: 0
  context_tokens_used: 5300
  records_written: 3
  records_skipped: 0
  records_failed: 0
```

---

## 12. OKR Evaluation Block

```yaml
okr_evaluation:
  success_rate: 1.0
  latency_score: 0.74
  reliability_score: 0.92
  # skill-specific OKRs below, null if not applicable
  verified_claim_ratio: 0.83
  entity_resolution_accuracy: 0.95
```

---

## 13. Universal OKRs (Required for All Skills)

All skills implement these operational OKRs.

**Reliability**
- `success_rate` ≥ 0.95
- `retry_rate` ≤ 0.10

**Validation Integrity**
- `validation_failure_rate` ≤ 0.05

**Efficiency**
- `latency` trending downward
- `repair_events` ≤ 0.05

**Context Stability**
- `context_utilization` ≤ 0.70

**Observability**
- `journal_completeness` = 1.0

Runs missing journals are invalid.

---

## 14. Skill-Specific OKRs

```yaml
skill_okrs:
  - name: decision_accuracy
    metric: decision_accuracy
    direction: maximize
    target: 0.60
    evaluation_window: 30_runs
```

---

## 15. Example Skill OKRs

**ocas-rally**
- `decision_accuracy` ≥ 0.60
- `risk_adjusted_return` ≥ benchmark
- `max_drawdown` ≤ 0.10

**ocas-scout**
- `verified_claim_ratio` ≥ 0.70
- `entity_resolution_accuracy` ≥ 0.90
- `source_diversity` ≥ 6

**ocas-elephas**
- `promotion_precision` ≥ 0.90
- `identity_merge_accuracy` ≥ 0.95
- `candidate_queue_age` ≤ 24 hours
- `ingestion_coverage` ≥ 0.99

**ocas-weave**
- `person_record_completeness` ≥ 0.80
- `sync_success_rate` ≥ 0.90
- `import_skip_rate` ≤ 0.05

---

## 16. Good OKR Design Principles

**Observable** — measurable automatically from journal data.
**Stable** — evaluated over rolling windows (e.g., 30 runs).
**Outcome-Oriented** — reflects real-world task success, not process steps.

Bad: `number_of_steps`
Good: `decision_accuracy`

---

## 17. Engineering Safeguards

- `comparison_group_id` must be generated before execution begins
- `normalized_input_hash` must match for both champion and challenger runs
- Journal files must be written atomically (write to `.tmp`, then rename)
- Journal files are append-only and never edited after write
- Malformed journals are quarantined by Mentor, not trusted

---

## 18. JSON Schema Validation

All journals conform to a shared JSON schema so Mentor and Forge can reliably parse them.

Validation workflow:
1. Skill finishes execution
2. Journal entry generated
3. Schema validator runs
4. If validation fails, run is marked invalid

Minimum required schema:
```json
{
  "type": "object",
  "required": ["run_identity", "runtime", "input", "decision", "metrics"],
  "properties": {
    "run_identity": {"type": "object"},
    "runtime": {"type": "object"},
    "input": {"type": "object"},
    "decision": {"type": "object"},
    "action": {"type": "object"},
    "metrics": {"type": "object"},
    "okr_evaluation": {"type": "object"}
  }
}
```

Forge enforces schema compliance when building new skills. Mentor quarantines journal entries that fail schema validation.

---

## 19. Spec Versioning Rules

Minor version increments only. Backward compatibility preserved between minor versions.

Skills include the spec version they implement:
```yaml
journal_spec_version: "1.3"
```

The canonical filename for this spec is `spec-ocas-journal.md`. All skill packages and build specs must reference this exact filename.

---

## 20. System Invariant

Every champion run must:
- generate a `comparison_group_id`
- write a journal entry to `~/openclaw/journals/{skill-name}/YYYY-MM-DD/{run_id}.json`
- spawn a variant run if one exists
- ensure variants never execute side effects

---

## 21. System Model

```
skills execute tasks
journals capture telemetry → ~/openclaw/journals/
mentor reads journals for evaluation
elephas reads journals for knowledge ingestion
forge builds variants from mentor proposals
```

Journals are the evaluation and knowledge substrate for the OCAS ecosystem.
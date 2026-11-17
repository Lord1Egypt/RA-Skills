# OCAS Inter-Skill Interfaces

Spec Version: 1.3.4
Author: Indigo Karasu

Changes from 1.3: added Sands → Vesper Schedule Brief Intake interface; added Sands to polling cadence table.
Changes from 1.2: added Rally → Vesper Portfolio Outcome cooperative read interface; added Vesper → Dispatch Briefing Delivery session-scoped interface; added Cooperative Query Interfaces section documenting five informal read-only cross-skill queries (Sift↔Thread, Sift↔Weave, Scout↔Weave, Taste↔Sift, Voyage↔Sift); added Rally and Vesper to polling cadence table.

---

## Purpose

This document defines the contracts for all inter-skill communication in the OCAS ecosystem. Skills communicate through shared filesystem paths under `{agent_root}/commons/`, not through direct calls or shared memory.

All interface paths, file formats, and handoff contracts are defined here. Skills reference this document when they need to send or receive data from another skill.

---

## General Rules

- Skills communicate by writing files to another skill's intake directory.
- The consuming skill polls its intake directory during its normal execution cycle.
- Files are immutable after writing. The producer must not modify a file after placing it in the intake directory.
- After the consumer processes a file, it moves it to `intake/processed/`. The producer must not delete or read from `processed/`.
- Intake directories are created by the consuming skill on initialization. Producers must create the directory if it does not exist before writing.
- All interface files are JSON. Filenames use the record's primary ID as the name: `{id}.json`.
- See `spec-ocas-shared-schemas.md` for the schemas referenced here.

---

## Elephas Signal Intake

### Purpose
Skills emit Signal observations to Elephas for Chronicle ingestion.

### Path
```
{agent_root}/commons/db/ocas-elephas/intake/{signal_id}.signal.json
```

### Producers
Any skill that observes entities, relationships, or events worth promoting to Chronicle: Sift, Scout, Look, Thread, Corvus, Weave (optional), Triage (optional).

### Format
Signal schema from `spec-ocas-shared-schemas.md`. The `.signal.json` extension distinguishes signal files from other intake files.

### Consumption
Elephas scans this directory during every `elephas.ingest.journals` run. Processed files move to `intake/processed/`.

### Notes
Signal emission is optional for standalone skills (Weave, Triage). Chronicle is a downstream consumer, not an upstream dependency.

---

## Mentor Journal Feed

### Purpose
Mentor reads journals from all skills during heartbeat evaluation passes.

### Path
```
{agent_root}/commons/journals/{skill-name}/YYYY-MM-DD/{run_id}.json
```

### Producers
All skills (every run writes a journal).

### Consumption
Mentor scans `{agent_root}/commons/journals/` recursively during `mentor.heartbeat.light` and `mentor.heartbeat.deep`. It tracks which `run_id`s have already been ingested via its own ingestion log at `{agent_root}/commons/data/ocas-mentor/ingestion_log.jsonl`.

### Notes
Mentor and Elephas are independent consumers of the same journal files. Neither blocks the other. Mentor reads for performance evaluation; Elephas reads to extract Chronicle candidates.

---

## Corvus → Praxis Behavioral Signal

### Purpose
Corvus notifies Praxis when it detects a behavioral anomaly or opportunity in skill output patterns that may warrant lesson extraction or a behavior shift.

### Path
```
{agent_root}/commons/data/ocas-praxis/intake/{signal_id}.json
```

### Producer
Corvus only. Written during `corvus.analyze.light` or `corvus.analyze.deep` when a validated pattern has `proposal_type: behavioral_signal`.

### Format
BehavioralSignal schema from `spec-ocas-shared-schemas.md`.

```json
{
  "signal_id": "sig_a7f2c1",
  "source_skill": "ocas-corvus",
  "timestamp": "2026-03-17T10:00:00-07:00",
  "signal_type": "anomaly_detected",
  "target_skill": "ocas-scout",
  "description": "Scout retry_rate exceeded 0.20 threshold across last 8 runs",
  "evidence_refs": ["r_b3e8d2", "r_c91f4a", "r_d2f1e3"],
  "confidence": "high",
  "suggested_event_type": "failure"
}
```

### Consumption
Praxis checks its intake directory during `praxis.event.record` and during any heartbeat or scheduled pass. Praxis decides whether to record this as an event and extract a lesson. It is not obligated to act on every signal.

---

## Mentor → Forge Variant Proposal

### Purpose
Mentor proposes skill improvements to Forge after detecting OKR regressions or patterns warranting a skill rebuild.

### Path
```
{agent_root}/commons/data/ocas-forge/intake/{proposal_id}.json
```

### Producer
Mentor. Written during `mentor.heartbeat.deep` or when `mentor.proposals.create` is invoked.

### Format
VariantProposal schema from `spec-ocas-shared-schemas.md`.

```json
{
  "proposal_id": "prop_5cfa2c1",
  "source_skill": "ocas-mentor",
  "timestamp": "2026-03-17T10:00:00-07:00",
  "target_skill": "ocas-scout",
  "base_version": "1.1.0",
  "observed_problem": "verified_claim_ratio below 0.70 target over last 30 runs",
  "supporting_evidence": ["eval_a7f2c1", "r_b3e8d2", "r_c91f4a"],
  "proposed_changes": "Strengthen source corroboration requirement before marking a claim as verified",
  "expected_improvement": "verified_claim_ratio from 0.62 to >= 0.72",
  "evaluation_plan": "Run challenger against benchmark-scout-v1 with 20 standard research requests",
  "minimum_runs": 20,
  "critical_non_regression_conditions": ["entity_resolution_accuracy >= 0.90", "source_diversity >= 6"]
}
```

### Consumption
Forge checks its intake directory when `forge.build` is invoked or during a Forge heartbeat cycle. Forge builds the variant package and places it for challenger testing. Processed proposals move to `intake/processed/`.

---

## Mentor → Forge Variant Decision

### Purpose
Mentor emits a promotion decision after evaluating champion vs. challenger runs over a sufficient window.

### Path
```
{agent_root}/commons/data/ocas-forge/intake/{decision_id}.json
```

### Producer
Mentor. Written when `mentor.variants.decide` is invoked.

### Format
VariantDecision schema from `spec-ocas-shared-schemas.md`.

### Consumption
Forge reads the decision and acts: promotes the challenger to champion if decision is `promote`, continues testing if `continue_testing`, or archives if `archive` or `reject`. Emergency rollback is handled immediately regardless of polling cycle.

---

## Sands → Vesper Schedule Brief Intake

### Purpose
Sands delivers structured schedule briefs to Vesper for inclusion in morning and evening briefings.

### Path
```
{agent_root}/commons/data/ocas-vesper/intake/{proposal_id}.json
```

### Producer
Sands. Written during `sands.brief` (both morning and evening modes).

### Format
InsightProposal schema from `spec-ocas-shared-schemas.md` with the following field values:
- `proposal_type`: `routine_prediction`
- `description`: `"[SANDS BRIEF: EVENING | MORNING] YYYY-MM-DD"`
- `confidence_score`: `1.0`
- `suggested_follow_up`: full schedule payload JSON-encoded as a string (see `references/vesper_emit_format.md` in the sands package for the payload structure)

Vesper must JSON-parse `suggested_follow_up` to obtain the structured schedule data.

### Consumption
Vesper checks its intake during `vesper.briefing.morning`, `vesper.briefing.evening`, or `vesper.briefing.manual`. Processed files move to `intake/processed/`.

### Notes
Sands writes directly to Vesper intake — it does not route through Corvus. Schedule briefs are deterministic, user-invoked outputs, not pattern-detected insights.

---

## Corvus → Vesper Opportunity Signal

### Purpose
Corvus delivers validated insight proposals to Vesper for inclusion in daily briefings.

### Path
```
{agent_root}/commons/data/ocas-vesper/intake/{proposal_id}.json
```

### Producer
Corvus. Written when a validated InsightProposal reaches sufficient confidence and `proposal_type` is `opportunity_discovery`, `routine_prediction`, `anomaly_alert`, or `thread_continuation`.

### Format
InsightProposal schema from `spec-ocas-shared-schemas.md`. Exclude `behavioral_signal` type (those go to Praxis).

```json
{
  "proposal_id": "prop_b3e8d2",
  "proposal_type": "opportunity_discovery",
  "description": "Rally portfolio has no allocation to the energy sector despite 6 months of rising energy search activity",
  "confidence_score": 0.78,
  "supporting_entities": ["entity_energy_sector", "entity_nvda"],
  "supporting_relationships": [],
  "predicted_outcome": "Adding energy allocation may improve risk-adjusted return",
  "suggested_follow_up": "Review Rally allocation plan for energy sector exposure",
  "target_skill": null,
  "created_at": "2026-03-17T10:00:00-07:00"
}
```

### Consumption
Vesper checks its intake during `vesper.briefing.morning`, `vesper.briefing.evening`, or `vesper.briefing.manual`. Vesper applies signal filtering rules (see `spec-ocas-signal-filtering.md` if defined, or Vesper's own `references/signal_filtering.md`). Processed files move to `intake/processed/`.

---

## Thread → Corvus Research Signal

### Purpose
Thread delivers reconstructed research threads to Corvus for pattern analysis.

### Path
```
{agent_root}/commons/data/ocas-corvus/intake/{thread_id}.json
```

### Producer
Thread. Written when a research thread reaches sufficient depth to be an interest candidate.

### Format
A normalized research thread record including: `thread_id`, `topic_label`, `first_seen`, `last_seen`, `sessions`, `entities`, `concepts`, `sources`, `engagement_summary`, `thread_strength`, `novelty_score`, `interest_candidate`.

### Consumption
Corvus reads Thread's research threads during analysis cycles as additional signal context for the Interest Engine and Novelty drive.

---

## Thread → Elephas Chronicle Candidate

### Purpose
Thread proposes stable research topics, interests, and source affinities as Chronicle candidates.

### Path
```
{agent_root}/commons/db/ocas-elephas/intake/{candidate_id}.signal.json
```

### Producer
Thread. Written only for high-quality candidates (interest candidates with session count ≥ 3, long_click count ≥ 3).

### Format
Candidate schema from `spec-ocas-shared-schemas.md`. Bad candidates (raw visit records, low-engagement URLs) must not be written.

---

## Rally → Vesper Portfolio Outcome

### Purpose
Vesper reads Rally's latest daily report during briefing generation to include portfolio outcomes and allocation changes.

### Path
This is a cooperative read interface — no intake directory is used. Vesper reads directly from Rally's data directory:

```
{agent_root}/commons/data/ocas-rally/reports/{YYYY-MM-DD}-daily.json
```

Vesper reads the most recent file matching `*-daily.json` in that directory.

### Format
PortfolioOutcomeRecord schema from `spec-ocas-shared-schemas.md`. If no file exists or the most recent file is more than 48 hours old, Vesper skips Rally data for that briefing without error.

### Consumption
Vesper checks this path during `vesper.briefing.morning` and `vesper.briefing.evening`. No file is written back; Rally's data is read-only from Vesper's perspective.

### Notes
Rally writes its daily report during `rally.report.daily`. The filename format is `YYYY-MM-DD-daily.json`. Rally does not write to Vesper's intake directory — Vesper pulls when it needs the data.

---

## Vesper → Dispatch Briefing Delivery

### Purpose
Vesper requests Dispatch to deliver a completed briefing via a user-preferred channel (e.g., iMessage, email).

### Path
None. This is a session-scoped handoff — no intake directory is used.

### Producer
Vesper. Occurs when `vesper.briefing.morning`, `vesper.briefing.evening`, or `vesper.briefing.manual` is invoked with a delivery channel configured in `config.json`.

### Consumption
Dispatch receives the briefing content directly in-session from Vesper. Dispatch drafts the delivery message and awaits explicit user confirmation before sending.

### Notes
Vesper never sends directly. Dispatch is always the sending agent. If Dispatch is not present, Vesper presents the briefing inline without delivery. This interface uses no file drop for the same reason as Praxis → Dispatch: Dispatch never operates autonomously on queued sends.

---

## Mentor → Fellow Experiment Request

### Purpose
Mentor invokes Fellow to run a controlled benchmark experiment against a target skill, heuristic, or workflow.

### Path
```
{agent_root}/commons/data/ocas-fellow/intake/{experiment_id}.json
```

### Producer
Mentor. Written when `mentor.variants.decide` determines empirical evaluation is needed, or when `mentor.heartbeat.deep` detects an OKR regression requiring a benchmark experiment.

### Format
ExperimentRequest schema from `spec-ocas-shared-schemas.md`.

### Consumption
Fellow checks its intake directory when `fellow.experiment.run` is invoked. Mentor writes the ExperimentRequest file first, then invokes `fellow.experiment.run`. Fellow processes the request, runs the experiment cycle, and writes a CycleResult to Mentor's intake. Processed experiment files move to `intake/processed/`.

### Notes
Fellow is purely reactive — it has no cron or heartbeat registration. Mentor is responsible for invoking `fellow.experiment.run` after dropping the request file.

---

## Fellow → Mentor Cycle Result

### Purpose
Fellow returns the outcome of a completed experiment cycle to Mentor for promotion decision.

### Path
```
{agent_root}/commons/data/ocas-mentor/intake/{cycle_id}.json
```

### Producer
Fellow. Written at the end of every `fellow.experiment.run` cycle, regardless of outcome (promote, no_change, or abort).

### Format
CycleResult schema from `spec-ocas-shared-schemas.md`.

### Consumption
Mentor reads CycleResult files from its intake directory during `mentor.heartbeat.light` and `mentor.heartbeat.deep`. On receiving a result with `decision: promote`, Mentor may emit a VariantDecision to Forge. On `abort`, Mentor logs the failure and may re-queue. Processed files move to `intake/processed/`.

---

## Praxis → Dispatch Action Handoff

### Purpose
Praxis passes communication action decisions to Dispatch for drafting and delivery. This is a session-scoped handoff — no intake directory is used.

### Path
None. Communication is in-session: Praxis proposes a communication action and Dispatch executes within the same session context.

### Producer
Praxis. Occurs when a behavior decision or outcome requires external communication (e.g., a follow-up message, a commitment confirmation).

### Consumption
Dispatch receives the action description directly in-session from Praxis. Dispatch drafts accordingly and awaits explicit user approval before any send operation.

### Notes
This interface uses no file drop because Dispatch never operates autonomously on queued actions — all sends require user confirmation in the active session. A file-drop pattern would imply autonomous send capability that Dispatch does not have.

---

## Cooperative Query Interfaces

Cooperative query interfaces are read-only cross-skill data accesses that do not use intake directories. They are optional — the requesting skill must degrade gracefully if the cooperating skill's data is absent or unavailable.

Cooperative reads are permitted for any skill to any other skill's data directory. The rules:
- The reading skill opens data as read-only. It must not write, move, or delete files.
- The reading skill must not block on missing data. If the target file or directory does not exist, it proceeds without that data.
- The reading skill documents its cooperative reads in its SKILL.md `## Optional skill cooperation` section.

The following cooperative reads are documented here because they are load-bearing for at least one skill's normal operation:

### Sift ↔ Thread: Query Rewriting

Sift may read Thread's active research context to improve query specificity. Thread's current context is available at:
```
{agent_root}/commons/data/ocas-thread/active_context.json
```
If absent, Sift proceeds with the unmodified query. Thread never reads from Sift.

### Sift ↔ Weave: Entity Disambiguation

Sift may query Weave's social graph database to disambiguate entity references (e.g., resolving "John" to a specific person when multiple matches exist). Weave's LadybugDB is at:
```
{agent_root}/commons/db/ocas-weave/
```
Sift opens this database as read-only. If absent, Sift proceeds with unresolved references.

### Scout ↔ Weave: Identity Context

Scout may read Weave's social graph to pre-populate identity context before starting a research request (known aliases, emails, relationships). Same database path as above. Scout never writes to Weave.

### Taste ↔ Sift: Item Enrichment

Taste may invoke Sift to enrich an extracted item (e.g., a restaurant, product, or media title) with additional structured data. This is a direct skill invocation in-session, not a file read. If Sift is absent, Taste records the item with available data only.

### Voyage ↔ Sift: Venue and Route Enrichment

Voyage may invoke Sift to enrich venue details, check transport options, or validate hours and pricing. Direct skill invocation in-session. If Sift is absent, Voyage proceeds with available data.

---

## Polling and Timing

Skills poll their intake directories on their own schedule. There are no push notifications or event queues.

Recommended polling cadences:

| Consumer | Intake | Recommended Cadence |
|---|---|---|
| Elephas | Signal intake | Every `elephas.ingest.journals` run (e.g., every 15 min) |
| Mentor | Journals directory + Fellow CycleResults | Every `mentor.heartbeat.light` (e.g., every 15 min) |
| Praxis | Behavioral signals from Corvus | Every Praxis scheduled pass or on-demand |
| Forge | Variant proposals and decisions from Mentor | Every Forge cycle or on-demand |
| Vesper | Opportunity signals from Corvus + Schedule briefs from Sands + Rally daily report (cooperative read) | At briefing generation time |
| Sands | n/a — Sands writes to Vesper intake, does not poll its own intake | On `sands.brief` invocation |
| Corvus | Research threads from Thread | During analysis cycles |
| Fellow | ExperimentRequest from Mentor | On `fellow.experiment.run` invocation |

---

## Error Handling

If a producer cannot write to an intake directory (directory missing, permission issue):
1. Create the directory and retry once.
2. If still failing, log the error to the producer's own decisions.jsonl and continue.
3. Do not halt the producing skill's normal operation.

If a consumer finds a malformed file in its intake directory:
1. Move it to `intake/errors/` with a `.error` suffix.
2. Log the error.
3. Continue processing remaining files.

---

## Adding New Interfaces

When a new inter-skill interface is needed:
1. Add an entry to this spec with producer, consumer, path, format, and consumption cadence.
2. Update the relevant skill SKILL.md files to reference this spec for the interface.
3. Bump this spec's minor version.

Do not create undocumented inter-skill interfaces.
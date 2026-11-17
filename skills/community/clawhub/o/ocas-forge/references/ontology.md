# OCAS Shared Ontology

Spec Version: 2.0.1
Author: Indigo Karasu

Changes from 2.0.0: architecture coherence audit 2026-04-12 found only 1 active OCAS skill repository (ocas-forge); ocas-triage has no GitHub repository instantiation; updated Skill Entity Extraction Ownership and Signal Emission Responsibilities tables to reflect only ocas-forge as active; moved ocas-triage to historical reference section; patch version bump due to scope refinement within existing active skills count.

Changes from 1.5.4: architecture coherence audit 2026-04-11 found only 2 active OCAS skill repositories (ocas-forge, ocas-triage); updated Skill Entity Extraction Ownership and Signal Emission Responsibilities tables to reflect current state; marked 22 previously-documented skills as historical reference; major version bump due to scope reduction from 24 to 2 active implementations.

Changes from 1.5.3: removed duplicate ocas-fellow entry from Signal Emission Responsibilities table; all 24 OCAS skills verified and listed without duplicates.

Changes from 1.5.2: removed ocas-relay from Skill Entity Extraction Ownership and Signal Emission Responsibilities tables; skill does not exist as OCAS architecture component; verified 24/24 actual OCAS skills listed and current.

Changes from 1.5.1: verified all 24 OCAS skills have complete ontology type definitions and Signal emission declarations; all skills audited for Ontology types section compliance on 2026-04-05.

Changes from 1.5: added ocas-multipass and ocas-vibes to Skill Entity Extraction Ownership and Signal Emission Responsibilities tables; updated to reflect all 24 active OCAS skills as of 2026-04-04.

Changes from 1.3 (v1.4): added ocas-sands to Skill Entity Extraction Ownership and Signal Emission tables; added ocas-elephas, ocas-mentor, ocas-praxis, ocas-forge, ocas-fellow, and ocas-custodian to Skill Entity Extraction Ownership and Signal Emission Responsibilities tables for complete skill inventory coverage. Changes from 1.1: added source_skill and record_time to Entity required fields; added possible_matches and merge_history to Entity fields; defined identifier type vocabulary and JSON serialization format; defined confidence derivation rules (numeric → label); decomposed valid_time into valid_from / valid_until for unambiguous range encoding; defined journal type semantics for source_journal_type; added signal delivery mechanism; added skill write permissions as a formal rule; added Chronicle-to-skill reference model (Chronicle stores skill-namespaced identifiers, not copies); added acquaintance_of to Entity-Entity relationship types; added storage layout convention reference. Changes from 1.1 (v1.2): added Skill Entity Extraction Ownership table; added Signal Emission Responsibilities table; updated Usage by Skills section with explicit per-skill entity type assignments. Changes from 1.2 (v1.3): added ocas-spot, ocas-haiku, ocas-bower, ocas-triage, ocas-relay to Skill Entity Extraction Ownership and Signal Emission tables.

---

## Purpose

This document defines the shared entity type hierarchy, relationship model, evidence model, time model, and identity resolution rules used across the OCAS ecosystem.

Chronicle (Elephas) is the authoritative store for ontology instances. Skills that extract, reference, or query entities must use the types defined here.

---

## Core Node Types

### Entity

Represents a real-world actor.

Subclasses:
- **Person** — a human individual
- **AI** — a synthetic individual or agent (e.g., the agent)

Required fields:
- `id` — unique identifier (UUID)
- `name` — canonical name
- `aliases` — list of known alternate names or handles
- `identifiers` — list of typed identifiers. See Identifier Vocabulary below.
- `type` — `Person` or `AI`
- `source_skill` — which skill created or last updated this record
- `record_time` — ISO 8601 timestamp when this record was written to Chronicle

Optional identity resolution fields:
- `possible_matches` — list of Entity ids flagged as possible duplicates
- `merge_history` — list of merge event records. Format: `[{"merged_id": "...", "merged_at": "...", "merged_by": "ocas-elephas", "reason": "..."}]`
- `identity_state` — `distinct` (default) / `possible_match` / `confirmed_same`

### Identifier Vocabulary

The `identifiers` field is a JSON array of typed identifier objects:

```json
[
  {"type": "email", "value": "user@example.com"},
  {"type": "phone", "value": "+14155551234"},
  {"type": "handle", "value": "@username"},
  {"type": "url", "value": "https://linkedin.com/in/username"},
  {"type": "domain", "value": "example.com"}
]
```

Allowed `type` values: `email`, `phone`, `handle`, `url`, `domain`, `employee_id`, `external_id`.

Skills may add skill-namespaced identifier types to cross-reference their own records. These are treated as reference pointers, not identity signals:

```json
{"type": "weave:person_id", "value": "uuid-from-weave-db"}
{"type": "scout:subject_id", "value": "req_20260305_001"}
```

### Place

Represents a physical location.

Required fields:
- `id` — unique identifier
- `name` — canonical name
- `place_type` — e.g., restaurant, office, city, venue
- `source_skill` — originating skill
- `record_time` — ISO 8601 timestamp

Optional fields:
- `coordinates` — `{"lat": 0.0, "lng": 0.0}`
- `address` — street address

### Concept

Represents an abstract idea or occurrence.

Subclasses:
- **Event** — a dated occurrence (meeting, trip, concert, purchase)
- **Action** — a discrete executed action
- **Idea** — a topic, theme, or abstract concept

Required fields:
- `id` — unique identifier
- `name` — label or title
- `description` — brief description
- `concept_type` — `Event`, `Action`, or `Idea`
- `source_skill` — originating skill
- `record_time` — ISO 8601 timestamp

### Thing

Represents a concrete or digital object.

Subclasses:
- **DigitalArtifact** — a document, file, email, or digital record
- **PhysicalArtifact** — a physical object
- **Signal** — a raw observation from a skill (see Evidence Model)
- **Candidate** — a proposed fact awaiting confirmation (see Evidence Model)

Required fields:
- `id` — unique identifier
- `name` — label or identifier
- `thing_type` — subclass name
- `metadata` — type-specific fields

---

## Relationship Model

Relationships are typed, directed edges between nodes.

Required fields:
- `source_id` — origin node
- `target_id` — destination node
- `relationship_type` — see Standard Relationship Types below
- `evidence_refs` — list of signal_ids or source references supporting this relationship
- `confidence` — `high`, `med`, or `low`
- `record_time` — ISO 8601 timestamp

Optional time fields (see Time Model).

### Confidence Derivation

When a skill produces a numeric confidence score (0.0–1.0), derive the label as follows:

- `>= 0.8` → `high`
- `>= 0.5` → `med`
- `< 0.5` → `low`

Skills may store numeric scores internally. The label form is required for Chronicle-facing fields.

### Standard Relationship Types

Between Entity and Entity:
- `knows`, `friend_of`, `colleague_of`, `family_of`, `introduced_by`, `spouse_of`, `reports_to`, `acquaintance_of`

Between Entity and Event:
- `participated_in`, `organized`, `attended`

Between Entity and Place:
- `lives_in`, `works_at`, `visited`, `associated_with`

Between Entity and Thing:
- `created`, `owns`, `uses`

Between Event and Place:
- `occurred_at`, `located_in`

Between Concept and Concept:
- `related_to`, `derived_from`, `part_of`

Skills may define additional relationship types in `snake_case` within their domains. Standard types above must be used when applicable.

---

## Evidence Model

Every fact in Chronicle traces to its source.

```
Skill Journal → Signal → supports → Candidate → becomes → Chronicle Fact
                                                         → Inference (separate, never overwrites facts)
```

### Signal

A raw observation produced by a skill. Signals are immutable after creation.

Required fields:
- `signal_id` — UUID
- `source_skill` — which skill emitted it
- `source_journal_type` — see Journal Types below
- `payload` — the observed data (structured JSON)
- `timestamp` — ISO 8601 when the signal was created
- `status` — `active` or `consumed`

### Journal Types for source_journal_type

- `Observation` — passive observation. No external side effects. Examples: Scout finding a public profile, Sift analyzing a document.
- `Action` — a skill executed an external action. Examples: Dispatch sending a message, Voyage booking a reservation.
- `Research` — structured multi-source research workflow. Examples: Scout running a full research pipeline.

### Candidate

A proposed addition to Chronicle requiring validation before becoming a confirmed fact.

Required fields:
- `candidate_id` — UUID
- `proposed_node` — full object being proposed
- `supporting_signals` — list of signal_ids
- `confidence` — `high`, `med`, or `low`
- `status` — `pending`, `confirmed`, `rejected`, or `merged`

### Promotion Rules

A candidate becomes a confirmed Chronicle fact when:
- It has at least one supporting signal
- Confidence meets the configured promotion threshold
- No contradicting evidence of higher confidence exists

Signals remain permanently attached as evidence after promotion.

### Signal Delivery

Skills emit Signals by writing a JSON file to the Elephas intake directory:

```
{agent_root}/commons/db/ocas-elephas/intake/{signal_id}.signal.json
```

Elephas watches this directory and processes new files. After processing, files move to `intake/processed/`. Skills must not delete or modify files in either directory.

Not all skills emit Signals. Skills that maintain standalone domain databases (Weave, Triage) operate independently. They may optionally emit Signals for Chronicle promotion, but this is not required for normal operation.

---

## Time Model

Three distinct temporal fields:

- `event_time` — when the real-world event occurred
- `record_time` — when the system recorded the observation
- `valid_from` / `valid_until` — the time range during which the fact is considered true. `valid_until` is null for currently-valid facts.

All timestamps use ISO 8601 format with timezone offset (e.g., `2026-03-17T10:00:00-07:00`).

---

## Identity Resolution

### Identity States

- `distinct` — confirmed to be a separate entity (default)
- `possible_match` — may refer to the same entity; flagged for review
- `confirmed_same` — confirmed to be the same entity; eligible for merge

### Merge Rules

- Merges must be reversible. Merge history is preserved in `merge_history` on the surviving node.
- Automatic merges require confidence above the configured `auto_merge_threshold`.
- Below that threshold, matches are flagged as `possible_match` for human review.

### Resolution Precedence

1. Exact identifier match (email, phone, URL)
2. Name + location match with corroborating signals
3. Behavioral pattern match (activity overlap, relationship overlap)

Ambiguous cases must preserve separation rather than silently collapsing records.

---

## Skill Write Permissions

**Only Elephas writes confirmed facts to Chronicle.** All other skills are read-only consumers.

Skills that maintain their own domain databases (Weave, Triage) own and write exclusively to their own database files. No skill may open another skill's database as `READ_WRITE`.

Cross-skill reads are permitted. A skill may open any other skill's database as `READ_ONLY`.

Skills do not read from Chronicle as part of normal operation. Chronicle is a downstream consolidation layer, not an upstream dependency. Skills that optionally query Chronicle for enrichment must degrade gracefully when Chronicle is unavailable.

---

## Chronicle-to-Skill Reference Model

Chronicle does not copy data from skill-local databases. When a person, task, or entity exists in both a skill database and Chronicle, Chronicle stores a reference pointer using a skill-namespaced identifier:

```json
{"type": "weave:person_id", "value": "uuid-from-weave-db"}
{"type": "triage:task_id", "value": "uuid-from-triage-db"}
```

The authoritative record lives in the skill's database. Chronicle holds a pointer. Skills are responsible for the integrity of their own data.

---

## Skill Entity Extraction Ownership

Every skill that extracts, manages, or emits entities must map its outputs to the types defined in this spec. The table below documents which entity types each skill is responsible for extracting or emitting as Signals.

**Currently active OCAS skills (as of 2026-04-12):**

| Skill | Entity Types | Place Types | Concept Types | Thing Types | Notes |
|---|---|---|---|---|---|
| ocas-forge | — | — | — | — | Skill architect; does not extract entities or emit Signals |

**Historical skill mappings (reference; skills not currently released):**

Skills not in this list do not extract entities and do not emit Signals to Elephas. Historical reference: ocas-scout, ocas-sift, ocas-look, ocas-thread, ocas-corvus, ocas-weave, ocas-taste, ocas-voyage, ocas-rally, ocas-sands, ocas-dispatch, ocas-vesper, ocas-custodian, ocas-spot, ocas-haiku, ocas-bower, ocas-elephas, ocas-mentor, ocas-praxis, ocas-fellow, ocas-multipass, ocas-vibes, ocas-triage

**Rules:**
- A skill's extracted entity types must be present in its emitted Signals' `payload.type` field.
- Skills that query Chronicle or Weave for entity context (read-only consumers) are not listed here — this table covers extraction and emission only.
- Skills not listed above (Elephas, Praxis, Mentor, Forge, Fellow) do not extract entities from user data. Elephas is the Chronicle writer; others operate on skill-internal data.

---

## Signal Emission Responsibilities

Skills that extract entities must emit Signals to Elephas for Chronicle ingestion. This table documents the expected emission pattern for each extracting skill.

**Currently active OCAS skills (as of 2026-04-12):**

| Skill | Emit Signals to Elephas? | Condition |
|---|---|---|
| ocas-forge | No | Skill architect; no entity signals |

**Historical skill patterns (reference; skills not currently released):**

Historical reference: ocas-scout, ocas-sift, ocas-look, ocas-thread, ocas-corvus, ocas-weave, ocas-taste, ocas-voyage, ocas-rally, ocas-sands, ocas-dispatch, ocas-spot, ocas-haiku, ocas-bower, ocas-custodian, ocas-elephas, ocas-mentor, ocas-praxis, ocas-fellow, ocas-multipass, ocas-vibes, ocas-triage

---

## Expected Scale

Nodes: 100k–500k
Edges: 5M–20M
Target hardware: Mac Studio, 512GB–1TB RAM, embedded LadybugDB.

---

## Usage by Skills

Skills that extract entities (Sift, Scout, Look, Corvus, Thread, Weave, Taste, Voyage, Spot, Sands) must map their extracted data to the types defined here. See the Skill Entity Extraction Ownership table above for the full mapping.

Skills that query entities (Weave, Vesper, Dispatch, Taste, Voyage, Haiku) expect the types defined here when reading from Chronicle or Weave's social graph.

Skills that emit Signals to Elephas must set `payload.type` to the ontology type of the primary entity in the signal (e.g., `Person`, `Place`, `Idea`).

Elephas is the only skill that writes confirmed facts to Chronicle.
# Chronicle Ontology

Chronicle implements the OCAS Shared Ontology (spec-ocas-ontology.md v1.1). This file documents Chronicle-specific implementation details.

## Node type hierarchy

Entity (entity_type: Person | AI)
Place (place_type: restaurant | office | city | venue | ...)
Concept (concept_type: Event | Action | Idea)
  Event subtypes: TravelEvent, MeetingEvent, PurchaseEvent, AppointmentEvent, CommunicationEvent
Thing (thing_type: DigitalArtifact | PhysicalArtifact | Signal | Candidate)

Chronicle does not store full documents. Artifacts remain in external systems. Chronicle stores references via Thing nodes with metadata pointing to the external location.

## Identifier vocabulary

The `identifiers` field on Entity nodes is a JSON array of typed identifier objects. Stored as a STRING in LadybugDB — serialize/deserialize as JSON.

Standard types: `email`, `phone`, `handle`, `url`, `domain`, `employee_id`, `external_id`

Skill-namespaced cross-references (reference pointers, not identity signals):
```json
{"type": "weave:person_id", "value": "uuid-from-weave-db"}
{"type": "scout:subject_id", "value": "req_20260305_001"}
```

## Standard relationship types

Used in `Relates.relationship_type`:

Entity-Entity: knows, friend_of, colleague_of, family_of, introduced_by, spouse_of, reports_to, acquaintance_of
Entity-Concept: participated_in, organized, attended
Entity-Place: lives_in, works_at, visited, associated_with
Entity-Thing: created, owns, uses
Concept-Place: occurred_at, located_in
Concept-Concept: related_to, derived_from, part_of

## Confidence

Relationship and Candidate confidence uses label form: `high` / `med` / `low`.

Derivation from numeric score (0.0–1.0):
- >= 0.8 → high
- >= 0.5 → med
- < 0.5 → low

## Time model

event_time — when the real-world event occurred
record_time — when Elephas wrote this to Chronicle
valid_from / valid_until — validity window. valid_until null = currently valid.

All timestamps: ISO 8601 with timezone offset.

## Identity model

States: distinct (default), possible_match, confirmed_same.
Resolution precedence: exact identifier match → name+location with corroboration → behavioral pattern match.
Merges are reversible. merge_history preserved on surviving node.

## Evidence model

```
Skill Journal → Signal → Supports → Candidate → Promotes → Chronicle Fact
                                                           → Inference (via Infers, never overwrites facts)
```

Every Chronicle fact traces back to at least one Signal. Signals are immutable after creation.

## Chronicle-to-skill reference model

Chronicle stores reference pointers for entities that exist in both Chronicle and skill-local databases:

```json
{"type": "weave:person_id", "value": "uuid-from-weave"}
{"type": "triage:task_id", "value": "uuid-from-triage"}
```

The authoritative record lives in the skill's database. Chronicle holds a pointer. Skills are responsible for their own data integrity.

## Expected scale

Nodes: 100k–500k
Edges: 5M–20M
Hardware: Mac Studio, 512GB–1TB RAM
LadybugDB indexes primary keys automatically. At this scale, filtering by `entity_type`, `identity_state`, `status`, and `confidence` should use indexed primary key lookups where possible to avoid full scans.

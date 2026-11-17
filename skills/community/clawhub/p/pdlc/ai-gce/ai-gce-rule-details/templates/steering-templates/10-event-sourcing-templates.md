<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Event Sourcing Steering Templates

> **Purpose:** Used by the project-init-agent to generate event sourcing and CQRS steering files
> in the target project's `rules/` folder. These templates encode event store patterns,
> CQRS boundaries, projection strategies, and event versioning rules derived from `event-sourcing.md`
> (conditional — only if Event Sourcing extension is active).

---

## event-sourcing-core.md (Always — within event sourcing scope)

**Generates**: `rules/event-sourcing-core.md`
**Condition**: Generated only IF `event-sourcing.md` exists in workspace steering
**Derived From**: event-sourcing.md + domain-context.md + architecture-principles.md

```markdown
---
inclusion: always
---

# Event Sourcing Standards

## Event Store
- {event_store_technology}: {event_store_description}
- Events are IMMUTABLE — NEVER modify or delete stored events
- Event streams are per-aggregate: {stream_naming_pattern}
- {event_serialization_format}
- {event_metadata_requirements}

## Event Design
- Events MUST be named in past tense: {event_naming_pattern}
- Events MUST be self-contained (include all data needed to reconstruct state)
- Events MUST NOT reference external entities by navigation (only by ID)
- Event payload MUST be backward-compatible (new fields optional, old fields never removed)
- {event_size_constraints}

## Aggregate Reconstitution
- Aggregates are rebuilt from event stream (no snapshot by default)
- {snapshot_strategy} (IF stream length > {snapshot_threshold} events)
- Loading: fetch events → apply in order → current state
- NEVER query aggregate state directly from event store

## CQRS Boundaries
- Command side: validates → produces events → stores in event stream
- Query side: reads from projections (NEVER from event store directly)
- {command_query_separation_enforcement}
- Write model and read model are SEPARATE (different schemas/stores)
```

---

## event-sourcing-projections.md (FileMatch `{projection_layer_pattern}`)

**Generates**: `rules/event-sourcing-projections.md`
**Derived From**: event-sourcing.md + database-rules.md

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{projection_layer_pattern}"
---

# Projection Standards

## Projection Design
- Projections are DISPOSABLE — can be rebuilt from events at any time
- {projection_rebuild_strategy}
- Projections MUST be idempotent (processing same event twice = same result)
- {projection_error_handling}

## Read Models
- One read model per query use case (not one-to-one with aggregates)
- Read models are denormalized for query performance
- {read_model_storage_strategy}
- Read models MAY be eventually consistent (document acceptable lag: {acceptable_lag})

## Projection Lifecycle
- {projection_deployment_strategy}
- Version projections: {projection_versioning_approach}
- {projection_monitoring_strategy}
```

---

## event-sourcing-versioning.md (FileMatch `{event_definition_pattern}`)

**Generates**: `rules/event-sourcing-versioning.md`
**Derived From**: event-sourcing.md

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{event_definition_pattern}"
---

# Event Versioning Standards

## Schema Evolution
- Adding optional fields: non-breaking (old events deserialize with default)
- Removing fields: BREAKING — use {event_upcasting_strategy} instead
- Renaming fields: BREAKING — map old name in {deserialization_strategy}
- Changing field type: BREAKING — create new event version

## Upcasting
- {upcasting_mechanism}: transforms old event shapes to current shape
- Upcasters run at read time (stored events are never modified)
- {upcaster_registration_pattern}
- ALL upcasters MUST be tested with real historical event samples

## Event Versioning Pattern
- Event type includes version: {event_type_versioning_pattern}
- New versions: {event_version_creation_strategy}
- {event_deprecation_strategy}
```

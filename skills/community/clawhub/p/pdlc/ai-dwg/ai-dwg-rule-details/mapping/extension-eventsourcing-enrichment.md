<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Event Sourcing/CQRS Extension Enrichment

## Purpose

When the **Event Sourcing/CQRS** extension was active in AI-ADLC, this mapping enriches existing steering files AND forces generation of a new conditional file.

**Trigger:** `adlc-state.md` → Enabled Extensions includes `event-sourcing-cqrs`

---

## MANDATORY: Stage Sub-Role — Event-Driven Architect

During THIS activity, ALSO adopt the mindset of an **Event-Driven Architect**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Events are immutable facts — "happened in the past" semantics drive naming (past tense) and storage (append-only, never modify)
- CQRS means complete separation — write side produces events, read side consumes projections; never mix the two models
- Projections are disposable — any read model can be rebuilt from the event stream; this is the safety net for schema evolution
- Design for eventual consistency as the default — the UI and API layer must handle projection lag gracefully
- Event versioning is the hardest problem — upcasters transform old formats on READ; never rewrite stored events

### Anti-Patterns for This Activity
- Do NOT allow projections to have side effects (sending emails, calling APIs) — projections are pure data transforms
- Do NOT let the write side query the event store for read operations — use projections
- Do NOT generate Event Sourcing enrichment unless the `event-sourcing-cqrs` extension is confirmed active

### Quality Check
A good output from this activity sounds like:
- "ES-01: Event store is APPEND-ONLY — NEVER modify or delete events. ES-06: Event payload includes ALL data needed to reconstruct state — no external lookups."
- "CQRS-05: Read models are disposable — can be rebuilt from events at any time. PROJ-02: Projections are idempotent — replaying same event produces same result."

---

## Files Enriched

| File | Enrichment |
|------|-----------|
| `database-rules.md` | DB-ES rules activated (event store schema, projections, snapshots) |
| `coding-standards.md` | CQRS command/query separation patterns, event handler conventions |
| `testing-strategy.md` | Event replay testing, projection verification |

---

## Forced Conditional Generation

| File | Normal Trigger | With Event Sourcing Extension |
|------|---------------|:-----------------------------:|
| `event-sourcing.md` | — (no normal trigger) | ✅ GENERATED — full event sourcing steering file |

---

## New File: event-sourcing.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Data Architecture + Event Sourcing/CQRS extension | date: {generation-date} -->

# Event Sourcing & CQRS

## Model

**Pattern:** {from AP — e.g., Event Sourcing with CQRS separation}
**Event Store:** {from AP — e.g., custom on PostgreSQL / EventStoreDB / Marten}
**Read Models:** {from AP — e.g., PostgreSQL projections / Elasticsearch}

---

## Event Store Rules

| Rule | Standard |
|------|----------|
| ES-01 | Event store is APPEND-ONLY — NEVER modify or delete events |
| ES-02 | Events are facts — named in past tense: `IncidentCreated`, `PriorityChanged` |
| ES-03 | Event schema: `{id, stream_id, event_type, version, payload, metadata, timestamp}` |
| ES-04 | Stream per aggregate: `{aggregate_type}-{aggregate_id}` |
| ES-05 | Optimistic concurrency: check expected version on append — reject if conflict |
| ES-06 | Event payload: include ALL data needed to reconstruct state — no external lookups |

---

## CQRS Rules

| Rule | Standard |
|------|----------|
| CQRS-01 | Write side: commands → validate → produce events → store events |
| CQRS-02 | Read side: events → projection → read model (separate database/table) |
| CQRS-03 | Queries NEVER read from event store directly — always from read models |
| CQRS-04 | Commands and queries use SEPARATE models — never shared DTOs |
| CQRS-05 | Read models are disposable — can be rebuilt from events at any time |

---

## Projection Rules

| Rule | Standard |
|------|----------|
| PROJ-01 | One projection per read model — clear mapping from events → state |
| PROJ-02 | Projections are idempotent — replaying same event produces same result |
| PROJ-03 | Projection lag is acceptable — UI must handle eventual consistency |
| PROJ-04 | Rebuild capability: every projection can be rebuilt from scratch (zero-state + all events) |
| PROJ-05 | Projection versioning: when schema changes, rebuild with new version |

---

## Snapshot Rules

| Rule | Standard |
|------|----------|
| SNAP-01 | Snapshot after every {from AP — e.g., 100} events per stream |
| SNAP-02 | Load: snapshot + events after snapshot = current state |
| SNAP-03 | Snapshots are optimization — system MUST work without them (just slower) |
| SNAP-04 | Snapshot invalidation: rebuild when aggregate logic changes |

---

## Event Versioning

| Rule | Standard |
|------|----------|
| EVER-01 | Events are immutable — never change published event schema |
| EVER-02 | New fields: add as optional (backward compatible) |
| EVER-03 | Breaking changes: new event type + upcaster from old → new |
| EVER-04 | Upcasters: transform old event format to new on read — never on write |

---

## Anti-Patterns

1. **NEVER** delete or modify events — they are historical facts
2. **NEVER** query the event store for read operations — use projections
3. **NEVER** put side effects in projections (sending emails, calling APIs) — projections are pure data transforms
4. **NEVER** share event schemas between bounded contexts without explicit mapping
5. **NEVER** make projections synchronous with writes — accept eventual consistency
```

---

## Enrichment to database-rules.md

Activate the DB-ES section (already templated). Ensure event store table schema is documented.

## Enrichment to coding-standards.md

```markdown
## CQRS Patterns

| Rule | Standard |
|------|----------|
| CQRS-CODE-01 | Command handlers: validate, execute aggregate method, return void (or event list) |
| CQRS-CODE-02 | Query handlers: read from projection/read-model only — never touch write side |
| CQRS-CODE-03 | Event handlers: update projections, trigger side effects (notifications, integrations) — idempotent |
| CQRS-CODE-04 | Aggregate methods: accept command data, enforce invariants, return domain events |
```

## Enrichment to testing-strategy.md

```markdown
## Event Sourcing Testing

| Rule | Standard |
|------|----------|
| ES-TEST-01 | Given-When-Then: given(past events).when(command).then(expected new events) |
| ES-TEST-02 | Projection tests: given(event stream) → verify(read model state) |
| ES-TEST-03 | Rebuild tests: verify projection rebuilds produce same state as incremental |
| ES-TEST-04 | Upcaster tests: old format events correctly transformed to new format |
```

---

## Key Rule

Event Sourcing enrichment fundamentally changes how data-to-steering.md and coding-standards.md work — it introduces the concept of "events as source of truth" which overrides traditional CRUD patterns for affected aggregates.

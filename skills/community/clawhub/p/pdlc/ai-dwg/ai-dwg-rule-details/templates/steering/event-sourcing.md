<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: event-sourcing.md (CONDITIONAL — ADLC Extension)

**Generate IF:** Event Sourcing/CQRS extension was active in AI-ADLC.

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Data Architecture + Event Sourcing extension | date: {generation-date} -->

# Event Sourcing & CQRS

## Model
**Pattern:** {Event Sourcing + CQRS}  |  **Store:** {tool}  |  **Read Models:** {tool}

## Event Store Rules
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| ES-01 | Append-only — NEVER modify/delete |
| ES-02 | Past tense naming: `IncidentCreated` |
| ES-03 | Schema: id, stream_id, type, version, payload, metadata, timestamp |
| ES-04 | Stream per aggregate: `{type}-{id}` |
| ES-05 | Optimistic concurrency: expected version check |
| ES-06 | Payload: ALL data needed to reconstruct |
<!-- end: AP-sourced -->

## CQRS Rules
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| CQRS-01 | Write: command → validate → events → store |
| CQRS-02 | Read: events → projection → read model |
| CQRS-03 | Queries from read models ONLY |
| CQRS-04 | Separate command/query models |
| CQRS-05 | Read models disposable — rebuildable |
<!-- end: AP-sourced -->

## Projections
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| PROJ-01 | One projection per read model |
| PROJ-02 | Idempotent |
| PROJ-03 | Eventual consistency acceptable |
| PROJ-04 | Rebuildable from scratch |
<!-- end: AP-sourced -->

## Snapshots
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| SNAP-01 | Every {n} events |
| SNAP-02 | Load = snapshot + subsequent events |
| SNAP-03 | Optional optimization |
<!-- end: AP-sourced -->

## Event Versioning
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| EVER-01 | Events immutable once published |
| EVER-02 | New optional fields = backward compatible |
| EVER-03 | Breaking = new event type + upcaster |
<!-- end: AP-sourced -->
```

## Filling: Refer to `mapping/extension-eventsourcing-enrichment.md`.

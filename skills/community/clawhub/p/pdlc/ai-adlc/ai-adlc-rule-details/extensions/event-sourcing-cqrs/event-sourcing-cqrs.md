<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Rules: Event Sourcing + CQRS

**Extension ID:** event-sourcing-cqrs
**Version:** 1.1.0
**Rule Prefix:** ES
**Status:** Active

---

## Activation Point

- **Primary Stage:** Stage 9 (Data Architecture)
- **Secondary Stages:** Stage 12 (Component Design), Stage 11 (Integration Architecture)

These rules fundamentally change the data model approach — state is derived from an append-only event log rather than mutated in place.

---

## MANDATORY: Extension Sub-Role — Event-Driven Architect

When this extension is active, ALSO adopt the mindset of an **Event-Driven Architect**. This does NOT replace your primary role (CTO / Chief Architect) — it ADDS a thinking dimension for the duration of event sourcing rule enforcement.

### Behavioral Shifts
- Think in events, not state — "what happened?" (immutable facts) rather than "what is?" (derived current state)
- Plan for schema evolution from day one — events will change shape; define versioning and upcasting strategy upfront
- Separate write model (command, enforces business rules) from read model (projection, serves queries) — they're different things
- Accept eventual consistency for projections — define what "eventually" means (ms? seconds?)

### Anti-Patterns for This Extension
- Do NOT maintain a "real" mutable database alongside the event store as dual source of truth — one must be authoritative
- Do NOT design events around technical implementation ("RowUpdated") — model around business meaning ("OrderShipped")

### Quality Check
A good output with this extension sounds like:
- "Events: OrderPlaced, PaymentAuthorized, ShipmentDispatched — immutable, versioned; read model: OrderSummaryProjection, lag target <500ms; snapshot every 100 events..."

---

## Rules

### Rule ES-01: Event Store as Source of Truth

**Statement:** The event store is the single source of truth for all state. Current state is derived by replaying events, never stored independently as the authoritative record. All writes append events; no updates or deletes occur in the event store.

**Verification:**
- [ ] Event store is append-only (no update, no delete operations)
- [ ] Current state can be reconstructed entirely from the event stream
- [ ] No separate "source of truth" database exists alongside the event store
- [ ] Event store guarantees ordering within a stream (per aggregate/entity)
- [ ] Event store provides a global ordering mechanism for cross-stream projections

**Anti-Pattern:** Maintaining both an event store and a "real" mutable database as dual sources of truth, leading to divergence and confusion about which is authoritative.

**ADR Trigger:** Yes — When deciding to adopt event sourcing (this is a fundamental, hard-to-reverse architectural decision).

---

### Rule ES-02: Event Immutability

**Statement:** Once an event is stored, it must never be modified or deleted. Corrections are expressed as new compensating events, not mutations to existing events.

**Verification:**
- [ ] Events are immutable after persistence (no field updates, no deletion)
- [ ] Corrections use compensating events (e.g., `OrderCorrected`, not update to `OrderPlaced`)
- [ ] Event store infrastructure enforces immutability (no update/delete API exposed)
- [ ] Regulatory "right to erasure" is handled via crypto-shredding or redaction events, not deletion
- [ ] Historical audit trail is never broken

**Anti-Pattern:** Deleting or modifying historical events to "fix" data, destroying the audit trail and potentially corrupting downstream projections that already processed the original event.

**ADR Trigger:** Yes — When handling data erasure requirements (GDPR/privacy) in an event-sourced system.

---

### Rule ES-03: Event Schema Versioning

**Statement:** Every event type must have an explicit version. Schema evolution must be handled through upcasting (transforming old event versions to new format on read) without modifying stored events.

**Verification:**
- [ ] Each event type has a version identifier (e.g., `v1`, `v2`)
- [ ] Upcasters exist to transform old event formats to current format on read
- [ ] New fields added as optional with default values (backward compatible)
- [ ] Removing or renaming fields requires a new event version + upcaster
- [ ] Event version history is documented
- [ ] Upcasting is tested (old events can be read by current code)

**Anti-Pattern:** Changing event schemas in place without versioning, breaking replay and projection rebuild capabilities for historical events.

**ADR Trigger:** Yes — When defining the event versioning and upcasting strategy.

---

### Rule ES-04: Stream-per-Aggregate Design

**Statement:** Each aggregate instance must have its own event stream. Stream identity corresponds to aggregate identity. Cross-aggregate queries use projections, not cross-stream reads.

**Verification:**
- [ ] One event stream per aggregate instance (identified by aggregate type + ID)
- [ ] Aggregate state is rebuilt by replaying only its own stream
- [ ] No aggregate reads from another aggregate's stream directly
- [ ] Stream naming convention is documented and consistent
- [ ] Cross-aggregate reads are served by projections (read models), not stream queries

**Anti-Pattern:** Single global event stream for all aggregates, making it impossible to efficiently load a single aggregate without scanning the entire event history.

**ADR Trigger:** No

---

### Rule ES-05: Snapshot Strategy

**Statement:** Aggregates with long event histories must define a snapshot strategy to avoid prohibitive replay times. Snapshots are optimization caches, not sources of truth — the full event stream remains authoritative.

**Verification:**
- [ ] Snapshot threshold is defined (e.g., snapshot every N events or every T time)
- [ ] Snapshots are stored alongside (not replacing) the event stream
- [ ] Aggregate can be rebuilt from events alone (snapshot is optional optimization)
- [ ] Snapshot invalidation/rebuild process exists
- [ ] Snapshot format is versioned (snapshots may need migration too)
- [ ] Performance targets for aggregate load time are defined

**Anti-Pattern:** Never snapshotting long-lived aggregates, leading to unacceptable load times as event count grows to thousands per aggregate.

**ADR Trigger:** Yes — When defining snapshot frequency, storage approach, and versioning strategy.

---

### Rule ES-06: CQRS Separation

**Statement:** The command side (write model) and query side (read model) must be explicitly separated. Commands modify state by appending events. Queries read from purpose-built projections. No query logic in the command path; no command logic in the query path.

**Verification:**
- [ ] Command handlers produce events (append to event store)
- [ ] Query handlers read from projections/read models (not from event store directly)
- [ ] Read models are optimized for specific query patterns (denormalized, pre-computed)
- [ ] No query logic in command handlers; no write logic in query handlers
- [ ] Eventual consistency between write and read side is explicitly acknowledged and documented

**Anti-Pattern:** Querying by replaying events on every read request (extremely expensive), or mixing read model queries into write-side transaction logic.

**ADR Trigger:** No

---

### Rule ES-07: Projection Design

**Statement:** Each distinct query need must have a dedicated projection (read model) built from the event stream. Projections are disposable and rebuildable — they can be destroyed and recreated from the event store at any time.

**Verification:**
- [ ] At least one projection is defined per distinct query pattern
- [ ] Projections are fully rebuildable from the event store
- [ ] Projection rebuild time is measured and acceptable
- [ ] Each projection documents which events it consumes
- [ ] Projection lag (eventual consistency delay) is measured and within SLA
- [ ] Projections are independently deployable and can be added without changing the write side

**Anti-Pattern:** A single "do everything" read model that tries to serve all query needs, becoming complex and slow to rebuild.

**ADR Trigger:** No

---

### Rule ES-08: Eventual Consistency Contract

**Statement:** The system must define explicit consistency guarantees between write side and read side. Acceptable propagation delay (lag) must be documented, monitored, and communicated to consumers.

**Verification:**
- [ ] Maximum acceptable lag between event write and projection update is defined (SLA)
- [ ] Lag is monitored in production (alerting if exceeded)
- [ ] UI/client design accounts for eventual consistency (optimistic updates, loading states)
- [ ] Commands that need read-after-write consistency have a defined strategy (e.g., read from write model)
- [ ] Consistency boundary per projection is documented

**Anti-Pattern:** Promising "real-time" consistency to users while the architecture is eventually consistent, leading to confused users seeing stale data without explanation.

**ADR Trigger:** No

---

### Rule ES-09: Event Replay and Projection Rebuild

**Statement:** The system must support full event replay to rebuild any or all projections from scratch. Replay must be an operational capability, not an emergency procedure.

**Verification:**
- [ ] Replay procedure is documented and tested
- [ ] Replay can be performed per-projection (not all-or-nothing)
- [ ] Replay time is measured for each projection (acceptable for operational use)
- [ ] Replay does not affect write-side availability
- [ ] New projections can be built from historical events (retroactive analytics)
- [ ] Replay handles event versioning (upcasting during replay)

**Anti-Pattern:** Designing event sourcing without ever testing replay, then discovering it takes days to rebuild a projection or fails on old event versions.

**ADR Trigger:** No

---

### Rule ES-10: Idempotent Projection Handlers

**Statement:** All projection handlers must be idempotent. Receiving the same event multiple times must produce the same result as receiving it once. Event position or ID must be tracked per projection.

**Verification:**
- [ ] Each projection tracks the last processed event position
- [ ] Duplicate event delivery produces no change (idempotent handling)
- [ ] Projection handlers use event ID or position for deduplication
- [ ] Projection can resume from its last checkpoint after restart
- [ ] At-least-once delivery is the assumed guarantee (not exactly-once)

**Anti-Pattern:** Projection handlers that increment counters or append without checking for duplicates, causing incorrect state after any redelivery or replay.

**ADR Trigger:** No

---

### Rule ES-11: Process Manager / Saga for Cross-Aggregate Workflows

**Statement:** Workflows spanning multiple aggregates must use a process manager (saga) that reacts to events and issues commands. Process managers maintain their own state and are themselves event-sourced when long-lived.

**Verification:**
- [ ] Cross-aggregate workflows are identified and modeled as process managers
- [ ] Process manager state is persisted (survives restarts)
- [ ] Process managers react to events and issue commands (not direct mutations)
- [ ] Timeout handling is defined for long-running process managers
- [ ] Compensation logic is explicit for each process manager step
- [ ] Process manager completion criteria are defined

**Anti-Pattern:** Embedding cross-aggregate coordination inside a single aggregate, violating aggregate boundaries and creating a "God aggregate" that knows about unrelated domains.

**ADR Trigger:** Yes — When deciding on process manager vs. choreography for a specific cross-aggregate workflow.

---

### Rule ES-12: Temporal Query Capability

**Statement:** The event-sourced system must support temporal queries — reconstructing the state of any aggregate or projection as it was at any point in time. This is a core benefit of event sourcing and must be architecturally preserved.

**Verification:**
- [ ] State at any historical point in time can be reconstructed (replay up to timestamp)
- [ ] Temporal queries are possible without full event replay (snapshot + partial replay)
- [ ] Bitemporal support is documented if needed (when known vs. when it happened)
- [ ] Projection rebuild to a specific point in time is supported
- [ ] Temporal query performance is acceptable for operational use

**Anti-Pattern:** Compacting or archiving old events, destroying the ability to perform temporal queries — which negates a primary reason for choosing event sourcing.

**ADR Trigger:** No

---

## Verification Checklist (Stage Completion)

Before completing a stage with Event Sourcing + CQRS rules active, verify:

- [ ] Event store is defined as the single source of truth (append-only)
- [ ] Event immutability is enforced at the infrastructure level
- [ ] Event versioning and upcasting strategy is documented
- [ ] Stream-per-aggregate design is applied consistently
- [ ] Snapshot strategy is defined for long-lived aggregates
- [ ] Command side and query side are explicitly separated
- [ ] Projections are defined per query pattern and are rebuildable
- [ ] Eventual consistency SLAs are documented and monitorable
- [ ] Event replay is tested and operational (not just theoretical)
- [ ] Projection handlers are idempotent
- [ ] Cross-aggregate workflows use process managers
- [ ] Temporal query capability is preserved

---

## ADR Triggers Summary

| Rule | ADR Required When |
|------|-------------------|
| ES-01 | Deciding to adopt event sourcing (foundational decision) |
| ES-02 | Handling data erasure requirements in an event-sourced system |
| ES-03 | Defining event versioning and upcasting strategy |
| ES-05 | Defining snapshot frequency and storage approach |
| ES-11 | Choosing process manager vs. choreography for cross-aggregate flows |

---

## Templates

### Event Catalog Entry

```
## Event: {EventName} (v{N})

**Stream:** {Aggregate type + instance identifier}
**Produced By:** {Aggregate / Command handler}
**Payload:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| {field} | {type} | {yes/no} | {description} |

**Consumers (Projections):** {List of projections that process this event}
**Consumers (Process Managers):** {List of process managers that react}
**Schema History:** v1 → v2 (added {field}, upcaster adds default)
```

### Projection Design Card

```
## Projection: {Name}

**Purpose:** {What query pattern it serves}
**Events Consumed:** {List of event types}
**Storage:** {Data store type for the read model}
**Rebuild Time:** {Estimated time to rebuild from scratch}
**Consistency SLA:** {Max acceptable lag from write to read}
**Query Patterns Supported:**
1. {Query 1 — description}
2. {Query 2 — description}
**Checkpoint Strategy:** {How position is tracked}
```

### Eventual Consistency Contract

```
## Consistency Contract: {Read Model / Projection Name}

**Write-to-Read Lag SLA:** {e.g., < 500ms under normal load}
**Monitoring:** {How lag is measured}
**Alerting Threshold:** {When to alert}
**Client Handling:** {How UI handles stale data — optimistic update, loading indicator, etc.}
**Read-after-Write Strategy:** {For operations needing immediate consistency}
```

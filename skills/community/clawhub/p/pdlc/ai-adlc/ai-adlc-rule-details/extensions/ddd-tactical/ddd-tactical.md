<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Rules: DDD Tactical Patterns

**Extension ID:** ddd-tactical
**Version:** 1.1.0
**Rule Prefix:** DDD
**Status:** Active

---

## Activation Point

- **Primary Stage:** Stage 12 (Component Design)
- **Secondary Stages:** Stage 9 (Data Architecture), Stage 11 (Integration Architecture)

These rules apply to internal module/component structure, domain modeling, and cross-context communication.

---

## MANDATORY: Extension Sub-Role — Domain Modeller (DDD Specialist)

When this extension is active, ALSO adopt the mindset of a **Domain Modeller**. This does NOT replace your primary role (CTO / Chief Architect) — it ADDS a thinking dimension for the duration of DDD rule enforcement.

### Behavioral Shifts
- Think in business language first — name aggregates, events, commands using the domain's ubiquitous language, not technical jargon
- Protect invariants explicitly — every aggregate exists to guard specific business rules; if you can't name them, the boundary is wrong
- Keep aggregates small — prefer eventual consistency between aggregates over large transactional scopes
- Model behaviour (commands, events), not just data (entities) — domains are defined by what they DO

### Anti-Patterns for This Extension
- Do NOT model aggregates as database tables — they're consistency boundaries, not persistence units
- Do NOT allow cross-aggregate transactions — if you need atomicity across two, they might be one aggregate

### Quality Check
A good output with this extension sounds like:
- "Order aggregate protects 3 invariants; cross-context via events (OrderPlaced → ShipmentRequested through ACL); ubiquitous language glossary defined..."

---

## Rules

### Rule DDD-01: Aggregate Boundary Definition

**Statement:** Every aggregate must define an explicit consistency boundary — the set of entities and value objects that change together within a single transaction.

**Verification:**
- [ ] Each aggregate has a documented boundary (which entities/value objects it contains)
- [ ] No transaction spans more than one aggregate
- [ ] The aggregate root is clearly identified for every aggregate
- [ ] Invariants protected by the aggregate are listed explicitly

**Anti-Pattern:** "God aggregate" — a single aggregate containing most of the domain model, leading to contention and large transaction scopes.

**ADR Trigger:** Yes — When an aggregate boundary decision is non-obvious or contested (e.g., choosing between one large aggregate vs. splitting into two with eventual consistency).

---

### Rule DDD-02: Aggregate Root as Single Entry Point

**Statement:** External consumers must access an aggregate only through its root entity. No direct access to child entities or value objects from outside the aggregate boundary.

**Verification:**
- [ ] All public operations are exposed through the aggregate root
- [ ] Child entities have no public entry points accessible from outside the aggregate
- [ ] Repository interfaces return aggregate roots (never child entities)
- [ ] Commands target aggregate roots, not internal members

**Anti-Pattern:** Allowing external code to hold references to inner entities and mutate them directly, bypassing invariant checks in the root.

**ADR Trigger:** No

---

### Rule DDD-03: Aggregate Size Optimization

**Statement:** Aggregates must be designed as small as possible while still protecting their invariants. Prefer smaller aggregates with eventual consistency between them over large aggregates with immediate consistency.

**Verification:**
- [ ] Each aggregate protects at most 2–5 invariants (if more, evaluate splitting)
- [ ] No aggregate contains more entities than needed to enforce its invariants
- [ ] Eventual consistency is explicitly accepted for cross-aggregate relationships
- [ ] Performance implications of aggregate size are considered (load time, contention)

**Anti-Pattern:** Including entities in an aggregate "just in case" without a specific invariant that requires them to be consistent in the same transaction.

**ADR Trigger:** Yes — When choosing eventual consistency over immediate consistency for a business rule.

---

### Rule DDD-04: Domain Event Definition

**Statement:** Every significant state change in an aggregate must emit a domain event. Events are named in past tense, represent facts that have occurred, and carry sufficient data for consumers to react without querying back.

**Verification:**
- [ ] Domain events are named in past tense (e.g., `OrderPlaced`, `TicketEscalated`)
- [ ] Event payload is self-contained (consumers do not need to call back to the source)
- [ ] Events are immutable once published
- [ ] A domain event catalog exists listing all events, their source aggregate, and payload schema
- [ ] Events represent business facts, not technical mutations

**Anti-Pattern:** Events that are just "entity changed" notifications without meaningful business semantics or that require consumers to fetch additional data to be useful.

**ADR Trigger:** No

---

### Rule DDD-05: Domain Event Ordering and Idempotency

**Statement:** Event consumers must handle out-of-order delivery and duplicate events gracefully. Event producers must include ordering metadata (sequence number or timestamp) per aggregate stream.

**Verification:**
- [ ] Each event carries a sequence number or logical timestamp relative to its aggregate
- [ ] Consumers implement idempotency checks (deduplication by event ID or idempotency key)
- [ ] Ordering guarantees are documented per event channel (ordered vs. unordered)
- [ ] Handling of duplicate delivery is designed explicitly (not assumed away)

**Anti-Pattern:** Assuming events will always arrive exactly once and in order, leading to inconsistent state when infrastructure delivers duplicates or reorders.

**ADR Trigger:** No

---

### Rule DDD-06: Value Object Identification

**Statement:** Concepts without identity that are defined entirely by their attributes must be modeled as value objects. Value objects are immutable and replaceable.

**Verification:**
- [ ] Entities vs. value objects are explicitly classified in the domain model
- [ ] Value objects have no identity field (no surrogate key)
- [ ] Value objects are immutable — changing a property produces a new instance
- [ ] Equality is based on attribute comparison, not reference/identity
- [ ] Common value objects are identified (money, address, date range, email, etc.)

**Anti-Pattern:** Giving identity (primary key) to every concept in the model, even those that should be value objects, leading to unnecessary complexity and lifecycle management.

**ADR Trigger:** No

---

### Rule DDD-07: Anti-Corruption Layer (ACL) at Context Boundaries

**Statement:** Every integration point between bounded contexts (or with external systems) must have an Anti-Corruption Layer that translates external models into the local domain model. No foreign model concepts leak into the core domain.

**Verification:**
- [ ] ACL is defined at every bounded context boundary
- [ ] External models are translated to internal ubiquitous language at the boundary
- [ ] No external system's data structures appear in the core domain layer
- [ ] ACL failures are handled gracefully (circuit breaker, fallback)
- [ ] Translation logic is co-located with the boundary, not scattered

**Anti-Pattern:** Importing external system DTOs directly into the domain layer, coupling the domain model to external contracts and breaking it when external systems change.

**ADR Trigger:** Yes — When deciding on the relationship type between contexts (conformist, ACL, shared kernel, open host).

---

### Rule DDD-08: Bounded Context Relationship Map

**Statement:** All bounded context relationships must be documented with their integration pattern: Shared Kernel, Customer-Supplier, Conformist, Anti-Corruption Layer, Open Host Service, or Published Language.

**Verification:**
- [ ] A context map exists showing all bounded contexts and their relationships
- [ ] Each relationship has a named pattern (from DDD strategic patterns)
- [ ] Data flow direction is documented (upstream/downstream)
- [ ] Team ownership per context is identified
- [ ] Integration contracts (APIs, events) are documented per relationship

**Anti-Pattern:** Treating all context relationships the same way, or having undocumented implicit coupling between contexts that surfaces only at runtime.

**ADR Trigger:** Yes — When the relationship type between two specific contexts is decided (especially Shared Kernel, which couples release cycles).

---

### Rule DDD-09: Domain Service Scoping

**Statement:** Domain services encapsulate business logic that does not naturally belong to a single entity or value object. They must be stateless and operate within a single bounded context.

**Verification:**
- [ ] Domain services contain only logic that spans multiple entities or doesn't fit a single entity
- [ ] Domain services are stateless (no instance-level state between invocations)
- [ ] Domain services operate within one bounded context (not cross-context orchestrators)
- [ ] Logic is first considered for placement in an entity/aggregate before escalating to a service
- [ ] Domain services are named with verbs (e.g., `TransferFundsService`, `RouteTicketService`)

**Anti-Pattern:** Using domain services as a dumping ground for all business logic, resulting in an anemic domain model where entities are just data holders.

**ADR Trigger:** No

---

### Rule DDD-10: Repository per Aggregate

**Statement:** Each aggregate has exactly one repository. Repositories abstract persistence and return fully reconstituted aggregate instances. No repository returns partial aggregates or individual child entities.

**Verification:**
- [ ] One repository interface per aggregate root
- [ ] Repositories return complete aggregates (not projections or partial loads)
- [ ] Repositories encapsulate all persistence logic (query construction, mapping)
- [ ] No business logic resides in repositories
- [ ] Repositories operate within a single bounded context

**Anti-Pattern:** Generic repositories that expose query builders, allowing consumers to load arbitrary subsets or join across aggregates, bypassing the aggregate boundary.

**ADR Trigger:** No

---

### Rule DDD-11: Ubiquitous Language Enforcement

**Statement:** All code artifacts (classes, methods, events, commands) within a bounded context must use the ubiquitous language of that context. No technical jargon or external system terminology in the domain layer.

**Verification:**
- [ ] A glossary/ubiquitous language dictionary exists per bounded context
- [ ] Class names, method names, and event names match the language of domain experts
- [ ] No database terminology (rows, tables) or infrastructure terminology in domain code
- [ ] Language is consistent across code, documentation, and conversation
- [ ] Ambiguous terms are disambiguated per context (same word may differ between contexts)

**Anti-Pattern:** Naming domain concepts after database tables, API endpoints, or framework terminology instead of using the language of the business domain.

**ADR Trigger:** No

---

### Rule DDD-12: Domain Event vs. Integration Event Separation

**Statement:** Internal domain events (within a bounded context) must be separated from integration events (published across context boundaries). Integration events have a stable public contract; domain events can evolve freely.

**Verification:**
- [ ] Domain events and integration events are distinct types (not shared classes)
- [ ] Integration events have a versioning and compatibility strategy
- [ ] Domain events can change without breaking external consumers
- [ ] An explicit translation step converts domain events to integration events at the boundary
- [ ] Integration event schemas are documented as public contracts

**Anti-Pattern:** Publishing internal domain events directly to external consumers, coupling the internal model evolution to all downstream systems.

**ADR Trigger:** Yes — When deciding whether to separate domain and integration events or use a unified event model.

---

## Verification Checklist (Stage Completion)

Before completing a stage with DDD rules active, verify:

- [ ] All aggregates have defined boundaries and documented invariants
- [ ] Domain event catalog is complete and follows naming conventions
- [ ] Value objects vs. entities are explicitly classified
- [ ] Anti-Corruption Layers exist at all context boundaries
- [ ] Context map with relationship patterns is documented
- [ ] Ubiquitous language glossary is current
- [ ] Domain events vs. integration events are separated
- [ ] Repository interfaces align with aggregate boundaries

---

## ADR Triggers Summary

| Rule | ADR Required When |
|------|-------------------|
| DDD-01 | Aggregate boundary is non-obvious or contested |
| DDD-03 | Choosing eventual consistency over immediate consistency |
| DDD-07 | Deciding relationship type between bounded contexts |
| DDD-08 | Selecting context relationship pattern (especially Shared Kernel) |
| DDD-12 | Deciding on domain vs. integration event separation model |

---

## Templates

### Domain Event Catalog Entry

```
| Event Name | Source Aggregate | Payload Fields | Published To | Consumers |
|------------|-----------------|----------------|--------------|-----------|
| {PastTenseEvent} | {Aggregate} | {field1, field2, ...} | {Channel} | {Context/Service} |
```

### Aggregate Design Card

```
## Aggregate: {Name}

**Root Entity:** {Root}
**Contained Entities:** {List}
**Value Objects:** {List}
**Invariants Protected:**
1. {Invariant description}
2. {Invariant description}

**Commands Handled:** {List}
**Events Emitted:** {List}
**Estimated Size:** {Small / Medium / Large}
**Concurrency Strategy:** {Optimistic / Pessimistic / Event-sourced}
```

### Context Map Entry

```
## {Context A} ←→ {Context B}

**Relationship Type:** {ACL / Shared Kernel / Customer-Supplier / Conformist / Open Host / Published Language}
**Upstream:** {Context}
**Downstream:** {Context}
**Integration Mechanism:** {Sync API / Async Events / Shared DB}
**Translation Required:** {Yes/No — describe if yes}
```

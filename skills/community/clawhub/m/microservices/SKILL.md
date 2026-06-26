---
name: microservices
description: Deep microservices workflow—service boundaries, data ownership, synchronous vs async integration, contracts, deployment independence, and operational complexity. Use when splitting a monolith, reviewing service boundaries, or debugging distributed failures.
---

# Microservices (Deep Workflow)

Microservices trade **code simplicity** for **operational and contract complexity**. Justify each boundary with **ownership** and **data isolation**—not fashion.

## When to Offer This Workflow

**Trigger conditions:**

- Splitting the monolith; coupling blocks independent deploys
- Latency cascades, partial failures, contract breaks
- Conway’s law alignment between teams and services

**Initial offer:**

Use **six stages**: (1) goals & constraints, (2) boundaries & data ownership, (3) integration patterns, (4) contracts & versioning, (5) reliability patterns, (6) ops & governance). Confirm org maturity and platform capabilities.

---

## Stage 1: Goals & Constraints

**Goal:** Why not a modular monolith first?

### Valid drivers

- Independent deploy cadence per team
- Different scaling profiles or stacks
- Clear domain ownership and blast-radius isolation

### Costs

- Distributed transactions, harder debugging, broader test matrix

**Exit condition:** Explicit assumption that modular monolith was considered.

---

## Stage 2: Boundaries & Data Ownership

**Goal:** One service owns each aggregate’s write path; no shared writable tables across services.

### Practices

- Bounded contexts from DDD when helpful

**Exit condition:** Entity → owning service map.

---

## Stage 3: Integration Patterns

**Goal:** Sync HTTP/gRPC vs async events—match consistency needs.

### Patterns

- Sagas or outbox for multi-step business processes

**Exit condition:** Sequence diagrams for top three flows.

---

## Stage 4: Contracts & Versioning

**Goal:** Backward-compatible evolution; consumer-driven contracts optional.

### Practices

- Deprecation policy published

---

## Stage 5: Reliability Patterns

**Goal:** Timeouts, retries with backoff, circuit breakers, bulkheads; idempotent handlers for retries.

---

## Stage 6: Ops & Governance

**Goal:** Service catalog, SLIs on dependency edges, golden paths for new services.

---

## Final Review Checklist

- [ ] Boundary and data ownership clear
- [ ] Integration style matches consistency needs
- [ ] Contract versioning policy exists
- [ ] Reliability patterns applied at boundaries
- [ ] Ops ownership and catalog in place

## Tips for Effective Guidance

- Microservices without delivery maturity often fail—say so explicitly.
- Shared databases are hidden coupling—flag them.
- The network is not reliable—design for partial failure.

## Handling Deviations

- Small teams: strong bias toward modular monolith or few services.

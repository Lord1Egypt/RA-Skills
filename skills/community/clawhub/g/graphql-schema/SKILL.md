---
name: graphql-schema
description: Deep GraphQL schema workflow—modeling types, queries and mutations, N+1 and complexity limits, errors and pagination, federation risks, and evolution. Use when designing or reviewing GraphQL APIs.
---

# GraphQL Schema (Deep Workflow)

GraphQL concentrates complexity on the server: **resolver graphs**, **N+1** fetches, **schema evolution**, and **field-level authorization**.

## When to Offer This Workflow

**Trigger conditions:**

- Designing a new GraphQL API or federated subgraph
- Latency or complexity incidents from client queries
- Need for safe schema deprecation and versioning

**Initial offer:**

Use **six stages**: (1) domain modeling, (2) operations surface, (3) performance patterns, (4) errors & partial results, (5) security & authz, (6) versioning & evolution). Confirm client patterns (Apollo, Relay) and gateway (if any).

---

## Stage 1: Domain Modeling

**Goal:** Types reflect domain concepts; avoid dumping everything on `Query`; use input objects for mutations with validation.

---

## Stage 2: Operations Surface

**Goal:** Queries for reads; mutations for writes; subscriptions only when justified (scaling and operational cost).

### Pagination

- Prefer cursor-based connections for large lists (Relay-style edges/nodes)

---

## Stage 3: Performance Patterns

**Goal:** DataLoader or batching for N+1; query complexity/depth/cost limits; optional persisted queries for public APIs.

---

## Stage 4: Errors & Partial Results

**Goal:** Document semantics of `errors` alongside partial `data`; map domain failures to structured extensions.

---

## Stage 5: Security & Authz

**Goal:** Enforce authorization at field/object level—not only at the top resolver.

---

## Stage 6: Versioning & Evolution

**Goal:** Prefer additive changes; `@deprecated` with migration window; in federation, clear ownership of types and entities.

---

## Final Review Checklist

- [ ] Schema reflects domain and operations
- [ ] Pagination and mutations idiomatic
- [ ] Batching and complexity limits in place
- [ ] Error behavior documented for clients
- [ ] Field-level authz enforced
- [ ] Deprecation policy defined

## Tips for Effective Guidance

- N+1 is the default failure mode—plan batching early.
- Pair with **rest-best-practices** when REST and GraphQL coexist at the edge.

## Handling Deviations

- Public APIs: consider persisted queries or allowlists to limit abusive queries.

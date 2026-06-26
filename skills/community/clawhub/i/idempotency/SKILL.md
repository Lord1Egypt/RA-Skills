---
name: idempotency
description: Deep idempotency workflow—identifying retry surfaces, idempotency keys, storage and TTL, exactly-once pitfalls, and testing duplicate delivery. Use when designing safe APIs, workers, and payment flows under at-least-once delivery.
---

# Idempotency (Deep Workflow)

Most distributed systems deliver work **at least once**. Idempotency makes **duplicate processing safe**—critical for payments, inventory, and message consumers.

## When to Offer This Workflow

**Trigger conditions:**

- Retries on HTTP, queues, or background jobs
- Double charges, duplicate records, or “at-least-once” confusion
- Product asks for “exactly-once” semantics

**Initial offer:**

Use **six stages**: (1) identify side effects, (2) choose keys, (3) storage & scope, (4) API patterns, (5) worker patterns, (6) testing). Confirm storage (Redis, SQL) and retention window.

---

## Stage 1: Identify Side Effects

**Goal:** Classify operations: reads vs creates vs monetary transfers vs state transitions.

**Exit condition:** List of mutations that must be idempotent under retries.

---

## Stage 2: Choose Keys

**Goal:** Client-supplied `Idempotency-Key` header (Stripe-style) vs deterministic hash of normalized payload—trade UX vs collision risk.

---

## Stage 3: Storage & Scope

**Goal:** Store key → outcome or result reference with TTL covering retry window; scope keys per tenant/user when needed.

---

## Stage 4: API Patterns

**Goal:** Same key + same body → same outcome; reject or conflict if same key with different body.

---

## Stage 5: Worker Patterns

**Goal:** Natural unique constraints in DB; dedupe table keyed by `event_id` or business idempotency key for consumers.

---

## Stage 6: Testing

**Goal:** Chaos or integration tests that deliver duplicate messages; property tests for key behavior.

---

## Final Review Checklist

- [ ] Mutating paths classified
- [ ] Key strategy and scope documented
- [ ] Storage, TTL, conflict rules defined
- [ ] HTTP and async consumers aligned
- [ ] Duplicate delivery tests

## Tips for Effective Guidance

- True exactly-once end-to-end is rare—design for at-least-once + idempotent effects.
- Pair with **message-queues** and **rest-best-practices** for HTTP idempotency keys.

## Handling Deviations

- Financial flows: require stronger audit and longer key retention.

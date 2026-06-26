---
name: message-queues
description: Deep message queue workflow—queue vs topic, ordering and partitions, retries and DLQ, idempotency, backpressure, observability, and failure design. Use when integrating workers, event buses, or debugging poison messages and lag.
---

# Message Queues (Deep Workflow)

Queues decouple producers and consumers—and introduce **duplicates**, **ordering surprises**, **poison messages**, and **lag**. Make **delivery semantics** and **failure handling** explicit.

## When to Offer This Workflow

**Trigger conditions:**

- Choosing Kafka vs RabbitMQ vs SQS vs Pub/Sub
- Consumer lag, DLQ growth, reprocessing needs
- “Exactly-once” expectations—need alignment on reality

**Initial offer:**

Use **six stages**: (1) delivery semantics, (2) topology & partitions, (3) message contract, (4) consumers & retries, (5) ops & scaling, (6) failure drills). Confirm cloud and ordering requirements.

---

## Stage 1: Delivery Semantics

**Goal:** Choose at-most-once, at-least-once, or effective-once via idempotency.

### Questions

1. Can duplicate processing break invariants?
2. Is ordering global, per-entity, or unnecessary?
3. Latency vs durability trade-offs

**Exit condition:** One paragraph per pipeline stating semantics.

---

## Stage 2: Topology & Partitions

**Goal:** Throughput and ordering align—ordering only within partition when using Kafka-style partitions.

### Practices

- Partition key often equals business key (e.g., user id)
- Watch hot partitions

---

## Stage 3: Message Contract

**Goal:** Versioned events or commands with schema registry.

### Practices

- Envelope: id, type, version, timestamp
- Payload size limits; reference blobs by id

---

## Stage 4: Consumers & Retries

**Goal:** Exponential backoff + jitter; DLQ with reason; replay tooling owned.

### Pitfalls

- Retries can reorder unless single-threaded per partition

---

## Stage 5: Ops & Scaling

**Goal:** Lag metrics, consumer offset health, rebalance awareness (Kafka).

---

## Stage 6: Failure Drills

**Goal:** Kill consumer mid-batch; duplicate publish intentionally; validate idempotency.

---

## Final Review Checklist

- [ ] Delivery semantics and idempotency explicit
- [ ] Partitioning/ordering strategy documented
- [ ] Versioned message contract
- [ ] Retry, DLQ, replay documented
- [ ] Lag metrics and alerts; capacity plan

## Tips for Effective Guidance

- **Exactly-once** end-to-end is rare—design for at-least-once + idempotent handlers.
- Challenge global ordering requirements—they cost scale.
- Visibility timeouts (SQS) differ by product—read the vendor docs.

## Handling Deviations

- **Transactional outbox** when you need DB + queue consistency without dual writes.

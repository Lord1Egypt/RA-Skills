---
name: performance-tuning
description: Deep performance tuning workflow—goals and measurement, profiling, hotspots, caching and concurrency trade-offs, system-specific tuning (DB, GC, network), and verification. Use when fixing latency, throughput, or resource saturation.
---

# Performance Tuning (Deep Workflow)

Performance work is **measurement-driven**. **Profile** before optimizing; **verify** after changes; **guard** against regressions with benchmarks or production metrics.

## When to Offer This Workflow

**Trigger conditions:**

- High **CPU**, **memory**, **p99** latency, **GC** pauses
- **Cost** reduction via efficiency
- **Premature** optimization requests—need **evidence** first

**Initial offer:**

Use **six stages**: (1) frame goals & SLOs, (2) measure baseline, (3) profile & hypothesize, (4) implement changes, (5) verify & compare, (6) prevent regression). Confirm **language/runtime** and **environment** (prod-like data volume).

---

## Stage 1: Frame Goals & SLOs

**Goal:** **Numeric** targets: p95 latency, throughput, max memory—**not** “faster.”

### Questions

1. Which **workloads** matter most (batch vs interactive)?
2. **Correctness** constraints (approximation allowed or not)?
3. **Cost** budget for hardware vs engineering time?

**Exit condition:** One-page success criteria and out-of-scope areas.

---

## Stage 2: Measure Baseline

**Goal:** **Reproducible** benchmark or **RUM** segment—same inputs, same conditions.

### Practices

- **Warm** caches when prod is always warm
- **Statistical** repeat (multiple runs, discard outliers methodology)

**Exit condition:** Baseline numbers + environment fingerprint (versions, flags).

---

## Stage 3: Profile & Hypothesize

**Goal:** Find **dominant cost**: CPU bound, I/O bound, lock contention, allocation rate.

### Tools (examples)

- **CPU** flame graphs; **async** wait profiling
- **Alloc** profiling for GC pressure
- **DB** query plans and lock waits

**Exit condition:** Hypothesis tied to evidence (e.g., “40% time in JSON parse”).

---

## Stage 4: Implement Changes

**Goal:** **Smallest** change that addresses the hotspot; **avoid** **clever** without proof.

### Levers

- **Algorithm** / data structure
- **Caching** with **invalidation** discipline
- **Batching** I/O; **connection** pooling
- **Parallelism** where safe—watch **locks**

---

## Stage 5: Verify & Compare

**Goal:** **A/B** or before/after with **same** workload; **watch** **tail** latency **not** only mean.

### Production

- **Canary** with **error** rate and **latency** gates

---

## Stage 6: Prevent Regression

**Goal:** **Micro-benchmarks** in CI (optional), **budgets**, or **synthetic** checks.

---

## Final Review Checklist

- [ ] Goals and baseline documented
- [ ] Root cause supported by profiler/trace evidence
- [ ] Change scoped; trade-offs explicit
- [ ] Verification on realistic load
- [ ] Regression guard where feasible

## Tips for Effective Guidance

- **Little’s Law** intuition: queues blow **latency**—often **fix** **concurrency** **before** **micro-opts**.
- **Avoid** optimizing **cold** paths **first**.
- **GC** languages: **allocation** **rate** often **is** the **enemy**.

## Handling Deviations

- **Embedded** / **mobile**: **battery** and **thermal** **constraints** **matter** **too**.
- **Distributed** systems: **local** **opt** **may** **hurt** **system** **(see** **load-testing**).

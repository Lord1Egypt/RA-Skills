---
name: load-testing
description: Deep load testing workflow—goals and SLOs, workload modeling, scenario design, environment fidelity, execution, metrics interpretation, and bottlenecks to fixes. Use when validating capacity, before launches, or reproducing latency under stress.
---

# Load Testing (Deep Workflow)

Load tests answer **whether the system meets behavior under target load**—not “how many RPS the tool prints.” Tie every run to **SLOs**, **workload realism**, and **analysis** that engineers can act on.

## When to Offer This Workflow

**Trigger conditions:**

- Major launch, traffic spike season, infra resize
- Latency/timeout under peak; need **evidence** for capacity decisions
- Comparing architectures or **debottlenecking**

**Initial offer:**

Use **seven stages**: (1) goals & SLOs, (2) workload model, (3) scenarios & scripts, (4) environment & data, (5) run & observe, (6) analyze bottlenecks, (7) fixes & retest. Confirm **tool** (k6, Locust, Gatling, JMeter) and **environment** policy (prod-like staging vs synthetic).

---

## Stage 1: Goals & SLOs

**Goal:** Define **success** in measurable terms.

### Questions

1. **Peak** RPS/users, **growth** assumption, **duration** of peak
2. **SLOs**: p95/p99 latency, error rate, throughput **per** critical endpoint
3. **Scope**: read-heavy vs write-heavy; **background** jobs interaction

**Exit condition:** Numeric **targets** + **out of scope** (e.g., “third-party API mocked”).

---

## Stage 2: Workload Model

**Goal:** **Representative** mix—not one URL forever.

### Practices

- **Transaction mix** from analytics or access logs (proportions)
- **Think time** between steps for user journeys
- **Payload** size distribution; **auth** token behavior
- **Spike** vs **soak** vs **step** ramp—match **real** failure modes

**Exit condition:** **Workload profile** documented (table or script comments).

---

## Stage 3: Scenarios & Scripts

**Goal:** **Deterministic**, **idempotent** load scripts where possible.

### Practices

- **Correlate** virtual user with **trace/request id** for debugging
- **Parameterize** data to avoid **cache** **fantasy** (every request hits same key)
- **Order** operations to match **real** **causality** (login → browse → checkout)

### Pitfalls

- **Client-side** bottleneck (single generator machine)—**distribute** load generators

**Exit condition:** **Smoke** run at small k validates script **correctness**.

---

## Stage 4: Environment & Data

**Goal:** **Fidelity** without **destroying** prod.

### Rules

- **Staging** scale proportional; **feature flags** aligned
- **Data volume** similar order-of-magnitude for **DB** **plans**
- **External** deps: mock, **sandbox**, or **throttle** **awareness**

**Exit condition:** **Safety** checklist: no prod writes unless explicitly planned and isolated.

---

## Stage 5: Run & Observe

**Goal:** **System-wide** visibility during test.

### Instrumentation

- **App**: latency histograms, error codes, **queue** depth
- **Infra**: CPU, memory, **connections**, **GC**, **disk** IOPS
- **DB**: slow queries, **locks**, **replication** lag
- **Tracing** sample during test for **hot spans**

**Exit condition:** **Dashboard** or **runbook** link for the test window.

---

## Stage 6: Analyze Bottlenecks

**Goal:** Identify **dominant** constraint: **app**, **DB**, **network**, **dependency**.

### Process

- **Utilization** vs **saturation** (e.g., CPU high but wait on locks—different fix)
- **Compare** p95 vs **max**—**tail** often **separate** issue
- **Reproduce** bottleneck with **smaller** experiment when unclear

**Exit condition:** **Written** hypothesis with **evidence** (graphs, trace ids).

---

## Stage 7: Fixes & Retest

**Goal:** **Controlled** changes with **retest** protocol.

### Practices

- **One** major change per retest when debugging
- **Document** **baseline** vs **after** for regression to **capacity** planning

---

## Final Review Checklist

- [ ] SLO-aligned goals and workload mix
- [ ] Realistic scenarios; distributed load if needed
- [ ] Environment safe and representative enough
- [ ] Full-stack observability during runs
- [ ] Bottleneck analysis leads to actionable tickets

## Tips for Effective Guidance

- **Warm** caches explicitly if prod is always warm—otherwise **misleading** **good** numbers.
- **Throughput** without **latency** SLO is meaningless.
- Call out **coordination** **overhead** (locks, **hot** **keys**) vs **raw** CPU.

## Handling Deviations

- **Cannot** match prod data: **state** **assumptions** and test **directional** only.
- **Serverless**: account for **cold** **start** and **account** **concurrency** limits in interpretation.

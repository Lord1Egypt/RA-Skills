---
name: observability-slos
description: Deep SLO/SLI workflow—user-centric SLIs, SLO targets and windows, error budgets, multi-window burn alerts, and policy when budget is exhausted. Use when defining reliability targets or aligning eng and product on trade-offs.
---

# Observability & SLOs (Deep Workflow)

SLOs connect **engineering work** to **user-perceived reliability**. SLIs must be **measurable from systems** but **grounded in user journeys**.

## When to Offer This Workflow

**Trigger conditions:**

- Defining **99.9%** without defining **for what**
- Too many pages or none; need **error budget** discipline
- **Product** wants features while **stability** degrades

**Initial offer:**

Use **six stages**: (1) pick user journeys, (2) define SLIs, (3) set SLO targets & windows, (4) error budget policy, (5) alerting on budget burn, (6) review & iterate). Confirm **metric** stack and **dependency** SLOs from vendors.

---

## Stage 1: User Journeys

**Goal:** **Critical paths** that matter if broken—checkout, login, API sync, not “CPU low”.

### Output

3–10 journeys ranked by **business impact** and **frequency**.

**Exit condition:** One paragraph per journey: user intent + failure symptom.

---

## Stage 2: Define SLIs

**Goal:** **Ratio** of good events over total over a window—**implementation** explicit.

### Examples

- **Availability**: successful requests / valid requests (define “valid”)
- **Latency**: proportion of requests faster than **T** ms

### Good SLIs

- **Objective**, **low-cardinality** enough to measure reliably

**Exit condition:** SLI formula + data source (metrics, logs, probes).

---

## Stage 3: SLO Targets & Windows

**Goal:** **Target** (e.g., 99.9% monthly) implies **allowed** bad minutes—make it explicit.

### Practices

- **Rolling** 30d common; align with **release** cadence
- **Tier** services: not everything needs same SLO

**Exit condition:** Published table: journey → SLI → target → window.

---

## Stage 4: Error Budget Policy

**Goal:** **What we do** when budget is healthy vs exhausted.

### Policy ideas

- Budget healthy → ship features; low → freeze risky changes, focus on reliability
- **Escalation** when budget burns fast (multi-window alerts)

**Exit condition:** Written policy with product sign-off.

---

## Stage 5: Alerting on Burn

**Goal:** Page on **budget burn rate**, not every blip—**multi-window** **multi-burn-rate** pattern when using Google-style SLO alerting.

### Practices

- **Fast burn** = page soon; **slow burn** = ticket/track

**Exit condition:** Alert rules linked to runbooks.

---

## Stage 6: Review & Iterate

**Goal:** SLOs **drift** with architecture—**quarterly** review; adjust targets with data.

---

## Final Review Checklist

- [ ] Journeys and SLIs tied to real user pain
- [ ] Targets realistic vs dependencies and cost
- [ ] Error budget policy agreed with product
- [ ] Alerts on burn, not noisy symptom spam
- [ ] Review cadence scheduled

## Tips for Effective Guidance

- Translate **99.9%** to **minutes/month** of allowed badness.
- **SLA** (contract) vs **SLO** (internal)—don’t confuse.
- Dependency SLO caps what you can promise—surface that early.

## Handling Deviations

- **No metrics yet**: start with **proxy SLI** (synthetic probes) and improve instrumentation.
- **Batch systems**: event processing lag as SLI instead of HTTP.

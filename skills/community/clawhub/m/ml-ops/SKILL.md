---
name: ml-ops
description: Deep MLOps workflow—reproducible training, experiment tracking, packaging, deployment, monitoring (drift, performance), governance, and rollback for ML. Use when shipping models to production or hardening ML pipelines.
---

# MLOps (Deep Workflow)

MLOps connects **research velocity** to **production reliability**: version **data**, **code**, and **artifacts** together; monitor **behavior** after deploy.

## When to Offer This Workflow

**Trigger conditions:**

- First production model; batch or online serving
- Drift, bias, or latency SLO misses
- Compliance needs for lineage and explainability

**Initial offer:**

Use **six stages**: (1) problem & risk class, (2) data & reproducibility, (3) training & evaluation, (4) packaging & deployment, (5) monitoring & feedback, (6) governance & rollback). Confirm batch vs real-time and regulatory tier.

---

## Stage 1: Problem & Risk Class

**Goal:** Align ML to decision risk (credit, health vs recommendation).

**Exit condition:** Offline and online success metrics defined.

---

## Stage 2: Data & Reproducibility

**Goal:** Snapshot training data; deterministic pipelines; PII handling.

### Practices

- Feature stores optional but valuable for consistency
- Secrets not in notebooks; orchestrated jobs

**Exit condition:** Run id reproduces artifact hash within agreed bounds.

---

## Stage 3: Training & Evaluation

**Goal:** Train/val/test without leakage; time-series splits careful.

### Practices

- Model card with limits and metrics
- Fairness slices where policy requires

---

## Stage 4: Packaging & Deployment

**Goal:** Immutable artifacts; canary or shadow before full cutover.

### Practices

- Model + preprocessing code version pinned together

**Exit condition:** Rollback to previous artifact id documented.

---

## Stage 5: Monitoring & Feedback

**Goal:** Data drift, concept drift, latency; business KPIs tied to model decisions.

### Practices

- Human review queue for low-confidence predictions when needed

---

## Stage 6: Governance & Rollback

**Goal:** Approvals for retrain/deploy; audit trail; A/B for big changes.

---

## Final Review Checklist

- [ ] Offline metrics aligned with business risk
- [ ] Data and code reproducibility
- [ ] Packaged artifacts with versioning and rollback
- [ ] Online monitoring and drift strategy
- [ ] Governance and approval path

## Tips for Effective Guidance

- Training-serving skew is a top bug—feature parity tests help.
- Offline accuracy ≠ online business outcome.
- Fairness needs explicit slices—not one headline number.

## Handling Deviations

- LLM-heavy products: lean on eval harnesses and prompt versioning (see **llm-evaluation**).
- Tiny teams: start with artifact registry + dashboards before a full feature store.

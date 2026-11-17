<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Product Backlog Package (AI-POLC) → value-metrics.md (POLC CLUSTER)

## Purpose

Transforms the value/KPI tracking model produced by AI-POLC (`operations/value-metrics.md`) into a **value-metrics tracking scaffold** in the destination workspace. This gives AI-DLC v1 a measurable definition of "success" beyond functional completion, and gives the observability layer the product KPIs it must instrument. Without it, the workspace can build features but cannot prove they delivered value.

**Output:** `{workspace-root}/value-metrics.md`
**Secondary effect:** Relay the instrument-able subset of KPIs to `observability-logging.md` (IF ADLC present) so the metrics have a technical home.

**Condition:** Generate IF `polc-state.md` is present AND the PBP contains a value/metrics artefact.

**Cluster:** Product — belongs to the POLC input cluster (with an observability relay when ADLC is also present).

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS activity, ALSO adopt the mindset of a **Business Analyst**. This ADDS a thinking dimension — it does NOT replace your primary role.

### Behavioral Shifts
- Think outcomes, not outputs — a shipped feature is not the metric; the behaviour change it causes is
- Every KPI needs a baseline, a target, and a measurement method — a metric without these is a slogan
- Distinguish leading indicators (early signal) from lagging indicators (confirmed result)
- Tie each metric back to a product goal — a KPI with no parent goal is noise

### Anti-Patterns for This Activity
- Do NOT invent targets POLC did not set — leave `{target: TBD — confirm with PO}` if absent
- Do NOT convert qualitative goals into fake precision ("improve satisfaction" ≠ "95% satisfaction") unless POLC stated it
- Do NOT list vanity metrics POLC flagged as non-decision-driving

---

## Source Inputs

**Primary source:** AI-POLC → PBP, via `polc-state.md` marker.

| PBP Document | What to Extract | Maps to Section |
|---|---|---|
| `operations/value-metrics.md` | KPI definitions, baselines, targets, cadence | KPI Register (all rows) |
| `foundation/product-vision.md` | Success metrics + parent goals | Goal→Metric linkage |
| `strategy/value-prioritization.md` | Value hypotheses behind prioritized items | Value Hypotheses section |
| `operations/acceptance-feedback.md` | Benefit-realization checkpoints | Measurement Cadence |

---

## Target Structure: value-metrics.md

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-POLC — operations/value-metrics.md + product-vision success metrics"
generatedOn: "{generation-date}"
ownership: hybrid
projectId: "{project-id}"
---

<!-- AI-DWG generated | source: AI-POLC Value & Metrics | date: {generation-date} -->

# Value & Success Metrics

> Defines how this product proves it delivered value. AI-DLC v1 instruments these;
> the observability layer reports them; AI-GCE may gate releases against them.

## KPI Register
<!-- begin: PBP-sourced -->
| KPI ID | Metric | Parent Goal | Type (leading/lagging) | Baseline | Target | Measurement Method | Cadence |
|--------|--------|-------------|------------------------|----------|--------|--------------------|---------|
| {KPI-01} | {metric} | {goal-id} | {leading} | {baseline} | {target} | {how-measured} | {weekly} |
| ... | ... | ... | ... | ... | ... | ... | ... |
<!-- end: PBP-sourced -->

## Value Hypotheses
<!-- begin: PBP-sourced -->
- We believe **{feature/epic}** will achieve **{outcome}**, measured by **{KPI-id}** moving from **{baseline}** to **{target}**.
- ...
<!-- end: PBP-sourced -->

## Measurement Cadence
- Review checkpoint: {cadence}
- Owner: {role from POLC, else "Product Owner"}

## Instrumentation Relay (IF ADLC present)
<!-- These KPIs require technical instrumentation. Wired into observability-logging.md. -->
| KPI ID | Signal to Capture | Suggested Telemetry |
|--------|-------------------|---------------------|
| {KPI-01} | {event/metric} | {counter/gauge/log field} |
```

---

## Transformation Rules

### Rule 1: Every KPI Has Baseline + Target + Method
If any is missing in the PBP, emit `{TBD — confirm with PO}` rather than fabricating a number.

### Rule 2: Each KPI Links to a Parent Goal
Use POLC goal IDs. A KPI with no parent goal is flagged, not dropped.

### Rule 3: Instrumentation Relay Only When ADLC Present
The `Instrumentation Relay` section is generated ONLY if `adlc-state.md` is also present (there is a technical layer to instrument). If ADLC absent, omit the section and note: `<!-- No ADLC peer — instrumentation deferred -->`.

### Rule 4: Leading vs Lagging Preserved
Carry POLC's classification verbatim; if unclassified, infer and mark `(inferred)`.

---

## Interaction with Other Mappings

| Related Mapping | Relationship |
|---|---|
| `infra-to-observability.md` | Receives the Instrumentation Relay subset — the product KPIs become technical telemetry requirements in `observability-logging.md`. |
| `polc-to-traceability.md` | KPIs link to the same goal IDs the traceability matrix threads — keep IDs consistent. |
| `quality-to-dod.md` | If a KPI is a release gate, it should also appear as a Definition-of-Done criterion. |

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| POLC present, no value-metrics artefact | Seed KPI Register from `product-vision.md` success metrics only; flag thinness |
| Metrics are purely qualitative | Keep qualitative, add `Measurement Method = qualitative review`; do not fake numbers |
| ADLC absent | Omit Instrumentation Relay; note deferral |
| Conflicting targets across POLC docs | Cross-input conflict within the product cluster — surface to user, do not pick one |

---

## Output Validation

- [ ] Every KPI has baseline/target/method (or explicit TBD)
- [ ] Every KPI links to a POLC goal ID
- [ ] Instrumentation Relay present IFF ADLC present
- [ ] Leading/lagging classification preserved
- [ ] Provenance front-matter + projectId present

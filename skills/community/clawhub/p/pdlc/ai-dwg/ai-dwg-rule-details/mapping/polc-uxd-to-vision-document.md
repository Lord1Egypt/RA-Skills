<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Product Backlog Package + UXP → vision.md (POLC CLUSTER)

## Purpose

Assembles the **Vision Document** that AI-DLC v1 expects as one of its two primary human-authored inputs. The Vision Document answers "What are we building, for whom, and why?" — combining product strategy from AI-POLC with user-research artefacts from AI-UXD.

**Output:** `{workspace-root}/vision.md`

**Condition:** Generate IF `polc-state.md` is present (POLC peer input detected).

**Enrichment:** If `uxd-state.md` is ALSO present, the Target Users and MVP User Journeys sections are enriched with UXD personas and journey maps.

**Cluster:** Product (primary) + UX (enrichment)

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS activity, ALSO adopt the mindset of a **Business Analyst**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think product-first — the Vision Document serves the product owner and the AI-DLC v1, not the architect
- Preserve the PO's voice — vision statements, success metrics, and scope decisions are quoted verbatim
- Personas and journeys ADD user empathy to the product strategy — they don't replace it
- Structure matters for AI-DLC v1 — follow the expected section format precisely

### Anti-Patterns for This Activity
- Do NOT inject technical architecture into the Vision Document (that's `technical-environment.md`)
- Do NOT paraphrase the product vision statement — quote it exactly as AI-POLC produced it
- Do NOT invent personas if UXD is absent — leave the Target Users section with POLC user segments only
- Do NOT include implementation details (tech stack, API patterns) — vision is WHAT and WHY, not HOW

---

## Source Inputs

### Primary: AI-POLC → Product Backlog Package (PBP)

| PBP Document | What to Extract | Maps to Vision Section |
|---|---|---|
| `product-vision.md` | Vision statement, problem statement, success metrics | Executive Summary, Problem Statement, Success Metrics |
| `roadmap.md` or `release-plan.md` | Full-scope vision, MVP scope (IN/OUT) | Full-Scope Vision, MVP Definition (IN/OUT) |
| `product-risk-register.md` | Key product risks, assumptions | Risks & Open Questions |
| `assumption-log.md` | Validated/unvalidated assumptions | Risks & Open Questions |
| User segments / target audience | User types, market segments | Target Users (baseline) |

### Enrichment: AI-UXD → UX Design Package (UXP) — IF PRESENT

| UXP Document | What to Extract | Maps to Vision Section |
|---|---|---|
| `personas.md` (1-N) | Persona profiles (name, role, goals, frustrations) | Target Users / Personas |
| `journey-maps.md` (1-N) | User journey maps (steps, touchpoints, pain points) | MVP User Journeys |
| `user-flows.md` | Key task flows | MVP User Journeys (supporting detail) |
| JTBD (Jobs to Be Done) | Job statements | Problem Statement (enrichment) |

---

## Target Structure: vision.md

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-POLC (primary) + AI-UXD (personas/journeys enrichment)"
generatedOn: "{generation-date}"
ownership: hybrid
---

<!-- AI-DWG generated | source: AI-POLC Product Vision + AI-UXD Personas/Journeys | date: {generation-date} -->

# Vision Document

## Executive Summary
<!-- begin: PBP-sourced -->
{product-vision-statement — VERBATIM from AI-POLC product-vision.md}
<!-- end: PBP-sourced -->

## Problem Statement
<!-- begin: PBP-sourced -->
{problem-description — from AI-POLC product-vision.md}

**Jobs to Be Done:**
{JTBD statements — from UXP if present, else from POLC user needs}
<!-- end: PBP-sourced -->

## Success Metrics
<!-- begin: PBP-sourced -->
| Metric | Target | Measurement |
|--------|--------|-------------|
| {metric-1} | {target-value} | {how-measured} |
| {metric-2} | {target-value} | {how-measured} |
| ... | ... | ... |
<!-- end: PBP-sourced -->

## Target Users / Personas
<!-- begin: UXP-sourced (if UXD present) / PBP-sourced (if UXD absent) -->

### IF UXD PRESENT — Full Personas:
| Persona | Role | Goals | Frustrations | Key Scenario |
|---------|------|-------|--------------|--------------|
| {persona-name-1} | {role} | {goals} | {frustrations} | {primary-scenario} |
| {persona-name-2} | {role} | {goals} | {frustrations} | {primary-scenario} |
| ... | ... | ... | ... | ... |

### IF UXD ABSENT — User Segments Only:
| Segment | Description | Primary Need |
|---------|-------------|--------------|
| {segment-1} | {description} | {need} |
| {segment-2} | {description} | {need} |
<!-- end: UXP-sourced / PBP-sourced -->

## Full-Scope Vision
<!-- begin: PBP-sourced -->
{full-scope description — what the product looks like at maturity}
<!-- end: PBP-sourced -->

## MVP Definition
<!-- begin: PBP-sourced -->
### IN Scope (MVP)
- {feature/capability 1}
- {feature/capability 2}
- ...

### OUT of Scope (Post-MVP)
- {deferred feature 1}
- {deferred feature 2}
- ...
<!-- end: PBP-sourced -->

## MVP User Journeys
<!-- begin: UXP-sourced (if UXD present) / PBP-sourced (if UXD absent) -->

### IF UXD PRESENT — Journey Maps:
#### Journey: {journey-name-1}
| Step | Action | Touchpoint | Pain Point | Opportunity |
|------|--------|-----------|-----------|-------------|
| 1 | {action} | {touchpoint} | {pain} | {opportunity} |
| ... | ... | ... | ... | ... |

#### Journey: {journey-name-2}
| Step | Action | Touchpoint | Pain Point | Opportunity |
| ... | ... | ... | ... | ... |

### IF UXD ABSENT — User Stories Summary:
- As a {user-type}, I want to {action} so that {benefit}
- ...
<!-- end: UXP-sourced / PBP-sourced -->

## Risks & Open Questions
<!-- begin: PBP-sourced -->
| # | Risk/Question | Impact | Status |
|---|---------------|--------|--------|
| 1 | {risk-or-question} | {impact} | {open/mitigated} |
| ... | ... | ... | ... |
<!-- end: PBP-sourced -->
```

---

## Transformation Rules

### Rule 1: Product Vision Is VERBATIM

The product vision statement from AI-POLC is quoted exactly. Do not paraphrase, shorten, or "improve."

### Rule 2: Personas Replace Segments (When UXD Present)

If UXD provides persona profiles, they REPLACE the basic user segments from POLC. Personas are richer — they include goals, frustrations, and scenarios that AI-DLC v1 uses for empathy-driven development.

### Rule 3: Journey Maps Replace User Stories (When UXD Present)

If UXD provides journey maps, they REPLACE basic user story summaries in the MVP User Journeys section. Journey maps give AI-DLC v1 the full context of user flows.

### Rule 4: Success Metrics Are Measurable

Every success metric MUST have a target value and measurement method. If POLC provides vague metrics ("improve user satisfaction"), flag for clarification.

### Rule 5: IN/OUT Scope Is Binary

MVP scope items are either IN or OUT. No "maybe" or "stretch goal" items in the Vision Document — those belong in the backlog.

### Rule 6: JTBD Enrichment

If UXD provides Jobs to Be Done statements, add them to the Problem Statement section. They complement (not replace) the product problem description.

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| POLC present, UXD absent | Generate with user segments only (no personas). Note in provenance: "Enrichment from UXD not available" |
| POLC product-vision.md missing vision statement | BLOCK within product cluster — ask user. Vision Document without a vision is invalid |
| UXD personas but no journey maps | Include personas; use POLC user stories for journeys section |
| POLC and UXD describe different user populations | Cross-input conflict — surface via conflict gate. Do NOT merge conflicting user models |
| No success metrics in POLC | Flag to user: "No success metrics found in PBP. Vision Document will lack measurable targets." Proceed if approved |

---

## Output Validation

- [ ] Vision statement is verbatim from POLC (not paraphrased)
- [ ] All success metrics have target + measurement
- [ ] MVP IN/OUT is binary (no ambiguity)
- [ ] If UXD present: personas replace segments; journeys replace stories
- [ ] If UXD absent: user segments used; no invented personas
- [ ] Risks section populated from POLC risk register
- [ ] Provenance markers present throughout
- [ ] No technical/architecture content (that's technical-environment.md)

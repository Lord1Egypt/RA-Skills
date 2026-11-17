<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: UX Design Package (AI-UXD) → design-qa.md (UXD CLUSTER)

## Purpose

Transforms the **Design QA framework** produced by AI-UXD (`validate/design-qa-framework.md` — design-to-code drift rules, severity model, report format) into a prescriptive `design-qa.md` steering file, and relays its enforceable rules to AI-GCE. This makes design-to-code fidelity a checkable discipline in the build workspace: AI-DLC v1 builds against it, and AI-GCE derives drift-detection hooks from it.

**Output:** `rules/design-qa.md`
**Secondary effect:** Relay the rule set to AI-GCE (a `design-fidelity` / `design-qa` governance rule) via the downstream signal — enforcement is AI-GCE's responsibility, not DWG's.

**Condition:** Generate IF `uxd-state.md` is present AND the UXP contains a Design QA framework artefact.

**Cluster:** UX — belongs exclusively to the UXD input cluster.

---

## MANDATORY: Stage Sub-Role — Audit Specialist

During THIS activity, ALSO adopt the mindset of an **Audit Specialist** (with a UX-designer lens for what "drift" means). ADDS a thinking dimension — does NOT replace your primary role.

### Behavioral Shifts
- Design QA is a control, not a style opinion — each rule must be objectively checkable
- The severity model classifies findings — preserve its thresholds verbatim (they drive gate/no-gate)
- Drift = measurable deviation from a token/component/spec — name the exact source of truth per rule
- A report format is a contract with reviewers — keep its fields stable

### Anti-Patterns for This Activity
- Do NOT soften severity thresholds — a "blocker" stays a blocker
- Do NOT convert objective drift checks into subjective "looks off" guidance
- Do NOT duplicate token values here — reference `design-system.md` as the source of truth

---

## Source Inputs

**Primary source:** AI-UXD → UXP, via `uxd-state.md` marker.

| UXP Document | What to Extract | Maps to Section |
|---|---|---|
| Design QA Framework (`validate/design-qa-framework.md`) | Drift rules, check categories, source-of-truth refs | QA Check Rules |
| Severity model | Severity levels + thresholds + gate behavior | Severity & Gating |
| Report format | Finding fields, report layout | Report Format |
| Accessibility baseline | A11y checks that belong to design QA | A11y QA subset (cross-ref) |

---

## Target Structure: design-qa.md

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-UXD — validate/design-qa-framework.md"
generatedOn: "{generation-date}"
ownership: generated
projectId: "{project-id}"
---

<!-- AI-DWG generated | source: AI-UXD Design QA Framework | date: {generation-date} -->

# Design QA & Fidelity Rules

> Source of truth for visual/interaction values = `design-system.md`. This file
> defines how implementation is CHECKED against it. AI-GCE derives drift hooks here.

## QA Check Rules
<!-- begin: UXP-sourced -->
| Rule ID | Check | Source of Truth | Pass Condition | Severity |
|---------|-------|-----------------|----------------|----------|
| DQA-01 | {e.g. spacing uses tokens} | `design-system.md` DS-SPC-* | No hardcoded px in layout | {blocker} |
| DQA-02 | {component state coverage} | `design-system.md` DS-CMP-* | All defined states implemented | {major} |
| ... | ... | ... | ... | ... |
<!-- end: UXP-sourced -->

## Severity & Gating
| Severity | Definition | Gate Behavior |
|----------|------------|---------------|
| Blocker | {def} | MUST block merge/release |
| Major | {def} | MUST be triaged before release |
| Minor | {def} | SHOULD be logged; non-gating |

## Report Format
{verbatim finding fields/layout from UXP — e.g. ID, rule, location, expected, actual, severity}

## Accessibility QA (cross-reference)
- WCAG-related drift checks live with `design-system.md` DS-A11Y-* and the GCE `accessibility-compliance` rule.
```

---

## Transformation Rules

### Rule 1: Severity Thresholds Are VERBATIM
Copy the UXP severity model exactly — gate behavior depends on it.

### Rule 2: Every Check Names a Source of Truth
Each DQA rule references the exact `design-system.md` rule ID (or other artefact) it checks against. No floating checks.

### Rule 3: No Token Duplication
Values are NOT restated here; reference `design-system.md`. This file is checks-only.

### Rule 4: Relay to AI-GCE
After generation, include the DQA rule set in the downstream signal so AI-GCE can derive enforcement hooks. DWG defines the rules; AI-GCE enforces them.

---

## Interaction with Other Mappings

| Related Mapping | Relationship |
|---|---|
| `uxd-to-design-system.md` | `design-system.md` is the source of truth; `design-qa.md` checks against it. |
| `governance-derivation.md` | Feeds the GCE relay — design-QA rules become candidate compliance hooks. |
| `uxd-to-information-architecture.md` | Nav/route fidelity checks may reference `navigation-structure.md`. |

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| UXP present, no Design QA framework | Skip the dedicated file; emit a minimal default set (token usage, state coverage, a11y) derived from `design-system.md`; flag thinness |
| Severity model absent | Use default 3-tier (Blocker/Major/Minor); mark `(default — UXP did not specify)` |
| No frontend in project | Skip entirely |

---

## Output Validation

- [ ] Severity thresholds copied verbatim
- [ ] Every check references a concrete source-of-truth rule ID
- [ ] No design-token values duplicated (references only)
- [ ] Report format preserved
- [ ] GCE relay included in downstream signal
- [ ] Provenance front-matter + projectId present

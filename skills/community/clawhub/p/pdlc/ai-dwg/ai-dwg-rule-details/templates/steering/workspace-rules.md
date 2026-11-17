<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: workspace-rules.md

## Template Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Architecture Vision / Product Vision / (deferred) | date: {generation-date} -->

# Workspace Rules

## Identity Assembly (Peer-Input Dependent)

<!-- IDENTITY IS ASSEMBLED BASED ON WHICH PEER INPUTS ARE PRESENT -->
<!-- DWG selects ONE of the following identity formats: -->

### IF ADLC PRESENT → "Architecture Identity"

## Architecture Identity

{architecture-vision-statement — VERBATIM from AP Architecture Vision. NEVER paraphrase.}

**System:** {system-name}
**Architecture style:** {monolith | modular-monolith | microservices | hybrid}
**Primary technology:** {language + framework}
**Deployment model:** {on-premises | cloud | hybrid}
**Project ID:** {project-id from adlc-state.md — immutable family correlation key}

### ELSE IF POLC PRESENT (no ADLC) → "Product Identity"

## Product Identity

{product-vision-statement — VERBATIM from POLC product-vision.md. NEVER paraphrase.}

**Product:** {product-name}
**Target users:** {primary user segments}
**Success metric:** {primary KPI}
**Project ID:** {project-id from polc-state.md or user-provided}

<!-- NOTE: Architecture not yet defined. Tech steering not available. -->
<!-- Quality-impact disclosure informed user that tech decisions are deferred. -->

### ELSE (UXD-only) → No Identity Header

<!-- Identity deferred — no architecture or product vision provided. -->
<!-- UXD does not produce a discrete vision statement. -->
<!-- Quality-impact disclosure informed user of this limitation. -->
**Project:** {project-name from user config}

<!-- END IDENTITY ASSEMBLY -->

## Guiding Principles

<!-- begin: AP-sourced -->

| # | Principle | Statement | Implication for Development |
|---|-----------|-----------|---------------------------|
| P1 | {principle-name} | {principle-statement} | {development-implication} |
| P2 | {principle-name} | {principle-statement} | {development-implication} |
| ... | ... | ... | ... |

<!-- end: AP-sourced -->

## Constraints (Non-Negotiable)

<!-- begin: AP-sourced -->

These constraints are ABSOLUTE. They cannot be violated regardless of convenience or preference.

| Constraint | Rule | Source |
|-----------|------|--------|
| {constraint-name} | {MUST NOT / NEVER / DO NOT statement} | {source} |
| ... | ... | ... |

<!-- end: AP-sourced -->

## Quality Priorities

Development decisions MUST prioritize quality attributes in this order:

<!-- begin: AP-sourced -->

1. **{critical-attribute}** — {practical-meaning}
2. **{critical-attribute}** — {practical-meaning}
3. **{high-attribute}** — {practical-meaning}
4. ...

<!-- end: AP-sourced -->

When two quality attributes conflict, the higher-priority attribute wins.

## Golden Rules

<!-- begin: AP-sourced -->

1. {rule-derived-from-principle — prescriptive, actionable}
2. {rule-derived-from-principle}
3. {rule-derived-from-constraint}
4. ...
(8-12 total)

<!-- end: AP-sourced -->

## Scope Awareness

This system includes: {module-list-brief}
This system does NOT include: {out-of-scope-items}

## References

- Architecture Principles (full detail): `rules/architecture-principles.md`
- Technology Stack: `rules/tech-stack.md`
- Module Structure: `rules/module-structure.md`
```

## Filling Instructions

Refer to `mapping/vision-to-workspace-rules.md` for complete transformation rules.

### Identity Assembly Logic

| Inputs Present | Identity Format | Vision Source | Fields |
|---|---|---|---|
| **ADLC** (with or without others) | "Architecture Identity" | AP Architecture Vision (verbatim) | system, arch style, tech, deployment, project ID |
| **POLC only** (no ADLC) | "Product Identity" | POLC Product Vision (verbatim) | product name, target users, success metric, project ID |
| **UXD only** (no ADLC, no POLC) | No identity header (deferred) | None — UXD has no quotable vision | project name only |

**Rules:**
- Vision statement is ALWAYS verbatim — NEVER paraphrase the architect's/product owner's vision
- ADLC takes precedence for identity because it provides the fullest technical context
- POLC-only identity honestly states "architecture not yet defined"
- UXD-only defers identity entirely — this was disclosed in quality-impact gate
- "Design Identity" was considered and DROPPED — UXD's closest equivalents (design principles, WCAG target, persona goals) are not a single quotable identity statement

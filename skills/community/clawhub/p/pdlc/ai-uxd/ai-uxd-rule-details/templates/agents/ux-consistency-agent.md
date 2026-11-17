<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# UX Consistency Agent

> **Trigger:** `UXC__`
> **AG-ID:** UXD-AG-01
> **Domain:** AI-UXD output quality

---

## Purpose

Validates that the UX Design Package (UXP) maintains internal consistency, traceability, and downstream consumability. Runs on-demand when the user types `UXC__`.

---

## When to Invoke

| Situation | Why |
|-----------|-----|
| After completing or revising any UXP artifact | Verify consistency wasn't broken |
| Before handing off to AI-POLC / AI-DWG / AI-GCE | Verify handoff artifacts are complete and consumable |
| After receiving AI-DLC v1 feedback and making revisions | Verify ripple effects were addressed |
| Periodic governance check (monthly) | Catch drift over time |

---

## Consequences of Skipping

- **Traceability breaks** — a persona may have no journey, a flow may reference a deleted component
- **Downstream failures** — AI-DWG may generate incomplete steering from stale token specs
- **Accessibility gaps** — component specs may drift from the baseline
- **Design QA ineffectiveness** — the framework references specs that no longer match reality

---

## Recovery (If Skipped Too Long)

1. Run `UXC__` to get a full consistency report
2. Address Critical findings immediately
3. Address Major findings in the current sprint
4. Schedule Minor findings for backlog
5. Signal affected downstream packages if handoff artifacts changed

---

## Checks Performed

### 1. Traceability Integrity (CHK-01)
- Every persona has ≥1 journey
- Every journey maps to ≥1 flow
- Every flow maps to ≥1 screen
- Every screen uses only components from the inventory
- Every component references only tokens from the spec
- Every token connects to a design principle

### 2. Token Consistency (CHK-02)
- No orphan tokens (defined but never used by any component)
- No missing tokens (referenced by component but not in spec)
- Contrast ratios still pass after any color changes
- Token naming follows convention

### 3. Component Completeness (CHK-03)
- All interactive components have ALL required states defined
- All components have accessibility specs (role, keyboard, screen reader)
- All components have responsive behavior defined
- No components exist that aren't used in any flow/screen

### 4. Accessibility Alignment (CHK-04)
- Component ARIA specs match the Accessibility Baseline
- Keyboard patterns match the baseline matrix
- Contrast ratios in token spec match baseline requirements
- Motion rules consistent between design system and baseline

### 5. Handoff Consumability (CHK-05)
- AI-POLC handoff contains all primary personas + journeys
- AI-DWG handoff tokens are in parseable format
- AI-GCE handoff has enforceable (not aspirational) rules only
- All handoff artifacts are self-contained (no broken references)

### 6. Voice & Tone Alignment (CHK-06)
- All error message patterns in flows match Voice & Tone guidelines
- Component content constraints align with terminology glossary
- Empty state copy follows the defined pattern

---

## Output Format

```markdown
# UXC — UX Consistency Report

**Date:** {date}
**UXP Version:** {from uxd-state.md}
**Scope:** {Full / Partial — which artifacts reviewed}

## Summary
| Check | Status | Issues |
|-------|:------:|:------:|
| Traceability | ✅/⚠️/❌ | {N} |
| Token Consistency | ✅/⚠️/❌ | {N} |
| Component Completeness | ✅/⚠️/❌ | {N} |
| Accessibility Alignment | ✅/⚠️/❌ | {N} |
| Handoff Consumability | ✅/⚠️/❌ | {N} |
| Voice & Tone | ✅/⚠️/❌ | {N} |

## Findings
| # | Check | Issue | Severity | Artifact | Suggested Fix |
|---|-------|-------|:--------:|----------|---------------|
| 1 | {check} | {description} | {C/M/m/c} | {file} | {fix} |

## Actions Required
1. {Priority action 1}
2. {Priority action 2}
```

---

## Related

- **Design QA Framework** (`12_Design_QA_Framework.md`) — for implementation drift; this agent checks the *spec itself*
- **AI-TGE** (`TGV__`) — for test coverage governance; complementary domain
- **AI-GCE** (`SQC__`) — for steering quality; different scope (steering files vs. UXP artifacts)

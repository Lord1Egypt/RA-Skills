<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-UXD
generatedVersion: "{version}"
source: "{upstream-doc-path}"
generatedOn: "{ISO-date}"
ownership: hybrid
---

# Design QA Framework

## Purpose

Governs how design-to-code drift is detected, classified, and resolved. Use this framework whenever implementation begins, and run it periodically throughout development.

---

## Comparison Dimensions

| # | Dimension | What's Compared | Source of Truth | Automatable? |
|---|-----------|----------------|----------------|:------------:|
| 1 | Spacing | Margins, padding, gaps | Spacing tokens | Partial |
| 2 | Color | Backgrounds, text, borders, icons | Color tokens | Yes |
| 3 | Typography | Font, size, weight, line-height | Typography tokens | Yes |
| 4 | Component structure | Correct component used, correct variant | Component Library | Manual |
| 5 | States | All states implemented correctly | State matrix | Partial |
| 6 | Responsiveness | Correct adaptation per breakpoint | Responsive spec | Manual |
| 7 | Accessibility | ARIA, keyboard, focus, screen reader | Accessibility Baseline | Partial |
| 8 | Iconography | Correct icon, size, color | Icon system | Manual |
| 9 | Voice & copy | Microcopy follows patterns + terminology | Voice & Tone | Manual |
| 10 | Layout | Grid alignment, zone structure | Wireframe specs | Manual |

---

## Severity Model

| Severity | Definition | Response | Timeline | Example |
|----------|-----------|----------|----------|---------|
| **Critical** | Breaks accessibility, blocks task, causes harm | Must fix before release | Immediate | Keyboard trap, contrast fails, missing error path |
| **Major** | Noticeably degrades UX quality or violates principle | Fix in current sprint | Days | Wrong component used, missing states, broken responsive |
| **Minor** | Visible but doesn't impact task completion | Add to backlog | Sprint+ | Spacing 4px off, slight color mismatch |
| **Cosmetic** | Present but imperceptible to users | Fix opportunistically | When adjacent | 1px off, animation timing slightly different |

### Quick Classification

| Dimension | Critical | Major | Minor | Cosmetic |
|-----------|----------|-------|-------|----------|
| Spacing | Overlapping / hidden content | >8px deviation | 2-4px off | 1px off |
| Color | Contrast fails WCAG | Wrong semantic role applied | Shade slightly off | Imperceptible |
| Typography | Wrong heading level (breaks a11y) | Wrong size/weight | Line-height off | Letter-spacing off |
| States | Missing state blocks interaction | Missing hover/focus visual | Transition differs | Timing slightly off |
| Accessibility | Keyboard trap / no AT access | Missing ARIA or role | Suboptimal but works | Verbose announcement |
| Responsiveness | Layout broken at breakpoint | Wrong adaptation type | Slightly off grid | Sub-pixel alignment |

---

## Process

### Per-Component Review

1. **Identify** — select component instance in implementation
2. **Overlay** — compare against component spec on all 10 dimensions
3. **Document** — log each drift with: dimension, severity, evidence (screenshot)
4. **Recommend** — reference specific token/spec section for the fix
5. **Verify** — after fix, confirm drift resolved

### Per-Screen Review

1. Layout matches wireframe zones? ✅/❌
2. Content hierarchy correct (visual priority matches spec)? ✅/❌
3. Correct components used (no custom one-offs without approval)? ✅/❌
4. All screen states implemented (empty, loading, error)? ✅/❌
5. Responsive behavior matches spec at each breakpoint? ✅/❌

### Per-Flow Review

1. Full happy path completable as designed? ✅/❌
2. Error paths match flow spec? ✅/❌
3. Edge cases handled per spec? ✅/❌
4. Transitions between steps correct? ✅/❌

---

## Report Template

### Summary

| Metric | Value |
|--------|:-----:|
| Components reviewed | {N} |
| Screens reviewed | {N} |
| Flows reviewed | {N} |
| Total drifts found | {N} |
| Critical | {N} |
| Major | {N} |
| Minor | {N} |
| Cosmetic | {N} |
| **Quality Score** | **{(Total - Critical×4 - Major×2 - Minor×1) / Total × 100}%** |

### Findings

| # | Location | Dimension | Description | Severity | Spec Ref | Fix |
|---|----------|-----------|-------------|:--------:|----------|-----|
| 1 | {component/screen} | {dimension} | {what drifted} | {sev} | {section} | {suggested fix} |

### Trends

- {Systemic observation 1}
- {Systemic observation 2}

### Priority Actions

1. {Most impactful fix — addresses multiple drifts}
2. {Critical fix}
3. {Systemic correction}

---

## Integration Points

### UXC__ Agent (Manual Trigger)
- Triggered by: `UXC__` shortcut
- Runs this framework against the current implementation state
- Produces a drift report as output
- Focuses on: token compliance, component states, accessibility spec match

### AI-GCE (Automated Enforcement)
- AI-GCE can derive hooks from this framework:
  - `design-token-check`: No hardcoded color/spacing values in UI files
  - `accessibility-check`: ARIA present on interactive components
  - `component-state-check`: New components define all required states

### AI-TGE (Test Governance)
- Design QA maps to AI-TGE test register entries
- Visual regression testing validates no unintended drift between releases
- Periodic audit (userTriggered) runs the full framework

---

## Cadence

| Checkpoint | When | Scope |
|------------|------|-------|
| Component release | Per new/updated component | Single component, all dimensions |
| Sprint review | End of each sprint | All changed screens |
| Pre-release | Before deployment | Full per-flow review |
| Periodic audit | Monthly / quarterly | Full framework (all dimensions, all flows) |

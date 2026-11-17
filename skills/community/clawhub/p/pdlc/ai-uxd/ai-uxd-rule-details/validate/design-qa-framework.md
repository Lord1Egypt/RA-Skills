<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 13: Design QA Framework

## Purpose

Define the governance framework for detecting and managing design-to-code drift — the gap between what was designed and what was built. This produces the rules, severity model, and comparison process that the UXC__ agent and development teams use during implementation.

---

## Depth Adaptation

| Depth | QA Framework Output |
|-------|---------------------|
| **Minimal** | Comparison dimensions + severity model + checklist |
| **Standard** | Full framework: dimensions, severity, process, report format, integration points |
| **Comprehensive** | Full framework + per-component QA spec + automated check suggestions + regression tracking |

---

## Steps

### Step 1: Define What "Design Drift" Means

```markdown
## Design Drift Definition

Design drift occurs when the implemented UI deviates from the governed
design specification in ways that affect:
- Visual consistency (spacing, color, typography don't match tokens)
- Interaction fidelity (states, transitions, behaviors differ from spec)
- Accessibility conformance (ARIA, keyboard, focus don't match baseline)
- Responsive behavior (breakpoint adaptations differ from spec)
- Content/voice (copy doesn't follow voice & tone guidelines)
```

### Step 2: Define Comparison Dimensions

```markdown
## Comparison Dimensions

| # | Dimension | What's Compared | Source of Truth |
|---|-----------|----------------|----------------|
| 1 | **Spacing** | Margins, padding, gaps between elements | Spatial System tokens |
| 2 | **Color** | Background, text, border, icon colors | Color System tokens |
| 3 | **Typography** | Font, size, weight, line-height, letter-spacing | Typography tokens |
| 4 | **Component structure** | Correct component used, correct variant | Component Library spec |
| 5 | **States** | All states implemented, correct visual per state | Component state matrix |
| 6 | **Responsiveness** | Correct adaptation at each breakpoint | Responsive behavior spec |
| 7 | **Accessibility** | ARIA roles, keyboard, focus, screen reader | Accessibility Baseline |
| 8 | **Iconography** | Correct icon, correct size, correct color | Icon system spec |
| 9 | **Voice & copy** | Microcopy follows tone, patterns, terminology | Voice & Tone guidelines |
| 10 | **Layout** | Grid alignment, zone structure, content hierarchy | Wireframe specs |
```

### Step 3: Define Severity Model

```markdown
## Drift Severity Model

| Severity | Definition | Response | Timeline |
|----------|-----------|----------|----------|
| **Critical** | Drift that breaks accessibility, creates user harm, or blocks core task completion | Must fix before release | Immediate |
| **Major** | Drift that noticeably degrades UX quality or violates a design principle | Fix in current sprint | Days |
| **Minor** | Drift that's visible but doesn't impact task completion or accessibility | Add to backlog | Sprint+ |
| **Cosmetic** | Drift that's technically present but imperceptible to users | Track, fix when adjacent work happens | Opportunistic |

### Severity Classification Guide

| Dimension | Critical | Major | Minor | Cosmetic |
|-----------|----------|-------|-------|----------|
| Spacing | Overlapping elements | >8px off spec | 2-4px off | 1px off |
| Color | Contrast fails WCAG | Wrong semantic role | Shade off | Imperceptible |
| Typography | Wrong hierarchy level | Wrong size/weight | Line-height off | Letter-spacing off |
| States | Missing states that block interaction | Missing hover/focus | Transition differs | Timing slightly off |
| Accessibility | Keyboard trap / no screen reader access | Missing ARIA | Suboptimal but functional | Verbose announcements |
| Responsiveness | Layout broken at breakpoint | Wrong adaptation behavior | Slightly off grid | 1px alignment |
```

### Step 4: Define Comparison Process

```markdown
## Design QA Process

### Per-Component Review
1. **Identify** — select component instance in implementation
2. **Compare** — check against component spec (Stage 9) on all 10 dimensions
3. **Document** — log each drift with dimension, severity, screenshot/evidence
4. **Recommend** — suggest the fix (reference specific token or spec section)

### Per-Screen Review
1. **Layout check** — does the screen match the wireframe zones?
2. **Content hierarchy** — is visual priority correct?
3. **Component usage** — are correct components used (no custom one-offs)?
4. **State coverage** — are all screen states implemented (empty, loading, error)?
5. **Responsive check** — test at each breakpoint, verify adaptation

### Per-Flow Review
1. **Path completeness** — can the user follow the entire flow as designed?
2. **Error handling** — do error paths match flow spec?
3. **Transitions** — are step-to-step transitions correct?
4. **Edge cases** — are documented edge cases handled?
```

### Step 5: Define Drift Report Format

```markdown
## Design QA Report Template

### Summary
| Metric | Value |
|--------|-------|
| Components reviewed | {N} |
| Screens reviewed | {N} |
| Total drifts found | {N} |
| Critical | {N} |
| Major | {N} |
| Minor | {N} |
| Cosmetic | {N} |

### Findings

| # | Component/Screen | Dimension | Drift Description | Severity | Spec Reference | Suggested Fix |
|---|-----------------|-----------|-------------------|----------|---------------|---------------|
| 1 | Button (primary) | Color | Background uses #2563EB instead of token `color.primary.default` (resolves to #2563EB in light, wrong in dark mode) | Major | Component_Button.md §Color | Reference token, not hardcoded value |
| 2 | ... | ... | ... | ... | ... | ... |

### Trends
- {Pattern observed — e.g., "spacing consistently 4px off across all cards"}
- {Systemic issue — e.g., "dark mode not tested; 0 components pass dark contrast"}

### Recommendations
1. {Priority fix 1}
2. {Priority fix 2}
3. {Systemic change if applicable}
```

### Step 6: Define Integration Points

```markdown
## Integration with AI-* Family

### AI-GCE (Governance)
- Design QA rules can feed AI-GCE's compliance engine
- GCE can enforce: "frontend component must reference design token" (not hardcode value)
- GCE hook: `design-drift-check.json` — fires on UI file changes

### AI-TGE (Testing)
- Visual regression testing validates no unintended drift between releases
- AI-TGE test register includes design QA as a test category
- TGE hook: periodic design QA audit (userTriggered)

### UXC__ Agent
- The UX Consistency agent (`UXC__`) runs this framework on demand
- Checks: token usage, component compliance, state coverage, accessibility spec match
- Produces the drift report as output
```

### Step 7: Present for Approval

Present:
- Comparison dimensions (are all 10 correct?)
- Severity model (are thresholds reasonable?)
- Process overview (per-component, per-screen, per-flow)
- Report format (clear enough to action?)
- Integration points (with GCE, TGE, UXC__ agent)

---

## Gate

**Approval required before proceeding to Stage 14.**

User must confirm:
- Dimensions cover all relevant comparison areas
- Severity thresholds are realistic for the team
- Process is clear and executable
- Report format is actionable
- Integration points are correct

---

## Log

Update `uxd-state.md`:
- Completed Stages: add Stage 13 with date and artifact (`12_Design_QA_Framework.md`)
- Current Stage: 14

---

## Transition

After gate approval:
```
Stage 13 complete. Design QA framework defined.

Moving to Phase 5: Assembly. Stage 14: AI-POLC Handoff.
I'll now package personas and journeys for AI-POLC consumption.
```

Load `assemble/polc-handoff.md`.

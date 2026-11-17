<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 11: Accessibility Baseline

## Purpose

Consolidate all accessibility requirements into a governed baseline document. This is not where accessibility begins (it's been embedded since Stage 3) — it's where everything is formalized into a single, enforceable standard that AI-GCE can derive compliance rules from.

---

## MANDATORY: Stage Sub-Role — Audit Specialist

During this stage, layer the Audit Specialist lens on top of the UX Designer primary:

**Behavioral Shifts:**
- Think in terms of standards compliance, not just user experience
- Be precise about conformance levels (AA vs. AAA) and success criteria numbers
- Document exceptions with justification (never silently skip a requirement)
- Produce checkable, testable requirements (not aspirational statements)

**Anti-Patterns for This Stage:**
- DO NOT produce vague accessibility goals ("we'll be accessible") — specify exactly what level and what criteria
- DO NOT defer accessibility to development ("they'll figure out the ARIA") — specify it here
- DO NOT conflate "looks good to me" with conformance — use measurable criteria
- DO NOT apply AAA everywhere — it's aspirational; be realistic about what's AA vs. what warrants AAA

**Quality Check:**
- [ ] Every requirement maps to a WCAG success criterion by number
- [ ] Keyboard interaction patterns are fully specified for all interactive components
- [ ] Screen reader behavior is documented (not just "add aria-label")
- [ ] Conformance target is explicit and scoped

---

## Steps

### Step 1: Declare Conformance Target

```markdown
## Accessibility Conformance Target

| Scope | Target Level | Justification |
|-------|-------------|---------------|
| Full product | WCAG 2.2 Level AA | {rationale — legal, ethical, market} |
| {specific area} | WCAG 2.2 Level AAA | {if certain areas warrant higher standard} |

### Exclusions (if any)
| Criterion | Exclusion Reason | Mitigation |
|-----------|-----------------|-----------|
| {SC number} | {why it doesn't apply} | {alternative provided} |
```

### Step 2: Organize by POUR Principles

Produce the baseline organized by the four WCAG principles:

```markdown
## Perceivable

### Text Alternatives (SC 1.1.1)
| Requirement | Implementation | Component |
|-------------|---------------|-----------|
| All images have alt text | `alt` attribute on all `<img>` | Image, Avatar, Icon |
| Decorative images hidden | `aria-hidden="true"` or empty alt | Icon (decorative) |
| Complex images have long description | `aria-describedby` or adjacent text | Charts, Diagrams |

### Color & Contrast (SC 1.4.3, 1.4.6, 1.4.11)
| Requirement | Standard | Verification |
|-------------|----------|-------------|
| Text contrast ≥4.5:1 (normal) | AA | Verified in Stage 8 color system |
| Text contrast ≥3:1 (large, ≥18px) | AA | Verified in Stage 8 |
| UI component contrast ≥3:1 | AA (SC 1.4.11) | Borders, icons, focus indicators |
| Color not sole indicator | AA (SC 1.4.1) | Errors use icon + text, not just red |

### Adaptable Content (SC 1.3.1-1.3.5)
| Requirement | Implementation |
|-------------|---------------|
| Logical reading order | DOM order matches visual order |
| Meaningful sequence | Heading hierarchy (h1 → h2 → h3, no skips) |
| Orientation support | Content works in portrait AND landscape |
| Input purpose identifiable | `autocomplete` attributes on form fields |

## Operable

### Keyboard (SC 2.1.1-2.1.4)
| Requirement | Implementation |
|-------------|---------------|
| All functionality keyboard-accessible | Tab, Enter, Space, Escape, Arrow keys |
| No keyboard traps | Escape always closes/exits |
| Focus order logical | Matches visual layout order |
| Focus visible | Minimum 2px outline, 3:1 contrast ratio |

### Keyboard Interaction Patterns
| Component | Tab | Enter/Space | Escape | Arrows |
|-----------|-----|-------------|--------|--------|
| Button | Focus | Activate | — | — |
| Link | Focus | Navigate | — | — |
| Input | Focus | — | — | — |
| Dropdown | Focus trigger | Open/select | Close | Navigate options |
| Modal | Focus first element | — | Close modal | — |
| Tabs | Focus tab list | Activate tab | — | Switch tabs |
| Menu | Focus menu | Select item | Close menu | Navigate items |
| Checkbox | Focus | Toggle | — | — |
| Radio | Focus group | Select | — | Move within group |

### Timing (SC 2.2.1-2.2.2)
| Requirement | Implementation |
|-------------|---------------|
| No time limits on interaction | Or: warn + extend option |
| Pause/stop/hide for auto-updating | User control for live regions |
| No content flashes >3/second | Motion/animation constraint |

### Motion (SC 2.3.1, 2.3.3)
| Requirement | Implementation |
|-------------|---------------|
| Respect `prefers-reduced-motion` | Disable/reduce all non-essential motion |
| Essential motion only | Loading spinners OK; decorative parallax off |
| Motion duration ≤400ms for transitions | Keep transitions quick |

## Understandable

### Language & Readability (SC 3.1.1-3.1.2)
| Requirement | Implementation |
|-------------|---------------|
| Page language declared | `lang` attribute on root element |
| Section language changes marked | `lang` on the changed section |

### Predictable Behavior (SC 3.2.1-3.2.4)
| Requirement | Implementation |
|-------------|---------------|
| No context change on focus | Focus never triggers navigation/submit |
| No context change on input | Typing never triggers navigation (except search) |
| Consistent navigation | Same nav structure across pages |
| Consistent identification | Same action = same label everywhere |

### Error Handling (SC 3.3.1-3.3.4)
| Requirement | Implementation |
|-------------|---------------|
| Errors identified | Field highlighted + error message text |
| Error described in text | Not just red border — include what's wrong |
| Suggestions provided | "Try format: name@company.com" |
| Reversible for important actions | Confirm destructive actions |

## Robust

### Compatibility (SC 4.1.1-4.1.3)
| Requirement | Implementation |
|-------------|---------------|
| Valid markup | No duplicate IDs, proper nesting |
| Name/role/value exposed | All components have accessible names |
| Status messages announced | Live regions for toast/alert |
```

### Step 3: Component-Level Accessibility Matrix

Map accessibility requirements to specific components:

| Component | Role | Keyboard | Focus | Announces | Touch Target |
|-----------|------|----------|-------|-----------|-------------|
| Button | `button` | Enter/Space | 2px ring | Label text | 44x44 min |
| Link | `link` | Enter | 2px ring | Link text + "link" | 44x44 min |
| Input | `textbox` | Tab in/out | Ring + label | Label + value | — |
| Checkbox | `checkbox` | Space toggle | Ring | Label + state | 44x44 min |
| Modal | `dialog` | Escape close | Trap inside | Title on open | — |
| ... | ... | ... | ... | ... | ... |

### Step 4: Assistive Technology Testing Plan

Define what to test with which AT:

| AT | Priority | What to Verify |
|----|----------|---------------|
| Screen reader (NVDA/JAWS/VoiceOver) | High | Reading order, announcements, landmarks |
| Keyboard only | High | All functionality accessible, no traps |
| Screen magnification (ZoomText) | Medium | Layout at 200% zoom, no clipping |
| Voice control (Dragon) | Medium | All targets reachable by voice |
| Switch access | Low | Sequential navigation works |

### Step 5: Present for Approval

Present:
- Conformance target and scope
- POUR-organized requirements (summary count per principle)
- Component accessibility matrix
- Keyboard interaction patterns
- Any areas where AA is not achievable + mitigation
- Testing plan

---

## Gate

**Approval required before proceeding to Stage 12.**

User must confirm:
- Conformance target is correct
- Requirements are complete for the product's scope
- Keyboard patterns are specified for all interactive components
- Any exclusions are justified and mitigated
- Testing approach is viable

---

## Log

Update `uxd-state.md`:
- Completed Stages: add Stage 11 with date and artifact (`10_Accessibility_Baseline.md`)
- Current Stage: 12

---

## Transition

After gate approval:
```
Stage 11 complete. Accessibility baseline defined targeting WCAG 2.2 Level {AA/AAA}.

Moving to Stage 12: Usability Validation Plan. I'll now define how
we'll validate that the design actually works for real users.
```

Load `validate/usability-validation.md`.

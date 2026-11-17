<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-UXD → Wireframes + Component Inventory + User Flows + Design System"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: ui-implementation-spec.md (UXD CLUSTER)

**Generate IF:** `uxd-state.md` is present (UXD peer input detected).
**Cluster:** UX
**Purpose:** Provides AI-DLC v1 with a detailed, page-by-page UI specification for code generation. This is the governed alternative to "paste Figma screenshots" — structured, versioned, and traceable.

## Template

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-UXD Wireframes + Components + User Flows"
generatedOn: "{generation-date}"
ownership: hybrid
---

<!-- AI-DWG generated | source: AI-UXD Wireframe Spec + Component Inventory + User Flows | date: {generation-date} -->

# UI Implementation Specification

## Overview

This document provides AI-DLC v1 with the detailed UI specification for code generation. Each page/screen is defined with its layout, components, states, interactions, and data bindings. Use alongside `design-system.md` (token/component rules) and `frontend-standards.md` (code patterns).

**Design System:** {design-system-name} v{version}
**WCAG Target:** {wcag-level}
**Responsive Strategy:** {strategy — e.g., mobile-first / desktop-first / adaptive}
**Breakpoints:** {breakpoint-list — e.g., sm:640px, md:768px, lg:1024px, xl:1280px}

---

## Page Inventory

<!-- begin: UXP-sourced -->
| # | Page/Screen | Route | Layout | Priority | Status |
|---|------------|-------|--------|----------|--------|
| 1 | {page-name} | {route-path} | {layout-pattern from DS-PAT} | {MVP/Post-MVP} | {spec'd/pending} |
| 2 | {page-name} | {route-path} | {layout-pattern} | {priority} | {status} |
| ... | ... | ... | ... | ... | ... |
<!-- end: UXP-sourced -->

---

## Page Specifications

### {Page Name 1}
<!-- begin: UXP-sourced -->

**Route:** `{route-path}`
**Layout:** {layout-pattern — references DS-PAT-NN}
**Auth Required:** {yes/no}
**Priority:** {MVP/Post-MVP}

#### Component Composition

| Zone | Component | Variant | Data Source | Interactions |
|------|-----------|---------|-------------|-------------|
| {header} | {DS-CMP-NN — e.g., Navigation} | {variant} | {data binding} | {click/hover/etc.} |
| {main} | {DS-CMP-NN} | {variant} | {API endpoint / state} | {interactions} |
| {sidebar} | {DS-CMP-NN} | {variant} | {data binding} | {interactions} |
| ... | ... | ... | ... | ... |

#### States

| State | Trigger | Display | Transition |
|-------|---------|---------|-----------|
| Loading | Initial fetch | {skeleton/spinner per DS-INT-01} | → Loaded / Error |
| Loaded | Data received | Full content | — |
| Empty | No data | {empty state per DS-INT-02} | — |
| Error | Fetch failure | {error state per DS-INT-03} | Retry → Loading |

#### Responsive Behavior

| Breakpoint | Layout Change |
|-----------|--------------|
| < sm | {stack components / hide sidebar / etc.} |
| sm–md | {adjust grid / collapse nav / etc.} |
| ≥ lg | {full layout as designed} |

#### Accessibility Notes

- Focus order: {tab sequence}
- Screen reader: {announcements for dynamic content}
- Keyboard shortcuts: {if any}
<!-- end: UXP-sourced -->

---

### {Page Name 2}
<!-- Repeat structure above for each page -->

---

## Shared Flows

### {Flow Name — e.g., Authentication Flow}
<!-- begin: UXP-sourced -->

| Step | Screen | User Action | System Response | Next Step |
|------|--------|------------|-----------------|-----------|
| 1 | {screen} | {action} | {response} | → Step 2 |
| 2 | {screen} | {action} | {response} | → Step 3 / Error |
| ... | ... | ... | ... | ... |

**Error paths:**
- {error-condition} → {error-screen/toast} → {recovery-action}
<!-- end: UXP-sourced -->

---

## Data Binding Reference

<!-- begin: UXP-sourced -->
| Component Instance | Data Field | Source | Update Frequency |
|-------------------|-----------|--------|-----------------|
| {page.component} | {field-name} | {API endpoint / store path} | {real-time / on-action / static} |
| ... | ... | ... | ... |
<!-- end: UXP-sourced -->

---

## Implementation Notes

- All components reference `design-system.md` by DS-CMP-NN ID
- All tokens reference `design-system.md` by DS-* ID
- Responsive breakpoints are from design tokens (`--breakpoint-*`)
- Loading/empty/error patterns follow `design-system.md` DS-INT-* rules
- This spec is the SOURCE OF TRUTH for UI implementation — takes precedence over verbal descriptions
```

---

## Filling Instructions

### Source Artifacts (from UXP)

| UXP Document | Fills Section |
|---|---|
| Wireframe Specifications | Page Specifications (layout, component zones, responsive) |
| Component Inventory | Component Composition tables (DS-CMP references) |
| User Flows | Shared Flows (step-by-step interaction sequences) |
| Information Architecture | Page Inventory (route structure, hierarchy) |
| Design System Document | Overview header (system name, breakpoints) |
| Accessibility Baseline | Accessibility Notes per page |

### Key Filling Rules

1. **Every component references its DS-CMP-NN ID.** No "a button" — always "DS-CMP-01 (Button, primary variant)."
2. **Every page has all four state definitions** (loading, loaded, empty, error). Even if UXP doesn't explicitly define them, use the DS-INT pattern rules as defaults.
3. **Responsive behavior is mandatory.** Every page MUST define behavior at minimum 2 breakpoints. If UXP doesn't specify, derive from layout pattern.
4. **Data bindings connect UI to backend.** If ADLC is present, reference API endpoints from the API Architecture. If ADLC absent, use `{API-TBD}` placeholders.
5. **Shared Flows capture multi-page interactions.** Authentication, checkout, onboarding — any flow spanning >1 page gets a Shared Flow section.
6. **Priority = MVP scope alignment.** Cross-reference with `info/vision.md` MVP IN/OUT (if POLC present) to mark pages as MVP or Post-MVP.

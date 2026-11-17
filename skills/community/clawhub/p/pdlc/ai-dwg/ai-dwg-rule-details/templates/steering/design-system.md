<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-UXD → UX Design Package (design system + tokens + component inventory)"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: design-system.md (UXD CLUSTER — CONDITIONAL)

**Generate IF:** `uxd-state.md` is present (UXD peer input detected).
**Cluster:** UX
**Source Input:** AI-UXD → Design System Document + Design Tokens Specification + Component Inventory

## Purpose

This steering file governs all UI implementation to ensure consistency with the design system produced by AI-UXD. It is the single source of truth for design tokens, component usage rules, and pattern compliance. AI-GCE derives enforcement hooks from this file. AI-DLC v1 uses it to produce UI code that respects the design system without deviation.

## Template

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: AI-UXD Design System + Tokens + Component Inventory | date: {generation-date} -->

# Design System

## Design Identity
**System Name:** {design-system-name}  |  **Version:** {version}
**WCAG Target:** {wcag-level}  |  **Brand Voice:** {voice-tone-summary}
**Token Format:** {format — e.g., W3C Design Tokens, Style Dictionary JSON}

---

## Design Tokens

### Color Palette
<!-- begin: UXP-sourced -->
| Token | Value | Usage | Rule |
|-------|-------|-------|------|
| DS-COL-01 | `--color-primary` = {value} | Primary actions, brand identity | MUST use for all primary CTAs |
| DS-COL-02 | `--color-secondary` = {value} | Secondary actions, supporting UI | MUST use for secondary buttons |
| DS-COL-03 | `--color-surface` = {value} | Card/panel backgrounds | MUST NOT use raw hex — always reference token |
| DS-COL-04 | `--color-error` = {value} | Error states, destructive actions | MUST use for all error indicators |
| DS-COL-05 | `--color-success` = {value} | Success states, confirmations | MUST use for positive feedback |
| DS-COL-06 | `--color-warning` = {value} | Warning states, caution indicators | MUST use for non-blocking alerts |
| DS-COL-07 | `--color-text-primary` = {value} | Body text, headings | MUST meet AA contrast on surface |
| DS-COL-08 | `--color-text-secondary` = {value} | Labels, captions, placeholders | MUST meet AA contrast minimum |
<!-- end: UXP-sourced -->

### Typography Scale
<!-- begin: UXP-sourced -->
| Token | Value | Usage | Rule |
|-------|-------|-------|------|
| DS-TYP-01 | `--font-family-primary` = {value} | Body text, UI labels | MUST NOT introduce additional typefaces |
| DS-TYP-02 | `--font-family-heading` = {value} | Headings H1-H4 | MUST use for all heading elements |
| DS-TYP-03 | `--font-size-base` = {value} | Body text baseline | MUST use rem units — NEVER px for font |
| DS-TYP-04 | `--font-size-sm` = {value} | Captions, helper text | Minimum readable size |
| DS-TYP-05 | `--font-size-lg` = {value} | Subheadings, emphasis | MUST scale proportionally |
| DS-TYP-06 | `--line-height-body` = {value} | Body text line spacing | MUST use for readability (min 1.5) |
| DS-TYP-07 | `--font-weight-regular` = {value} | Body, labels | Default weight |
| DS-TYP-08 | `--font-weight-bold` = {value} | Headings, emphasis, CTAs | MUST NOT use for entire paragraphs |
<!-- end: UXP-sourced -->

### Spacing System
<!-- begin: UXP-sourced -->
| Token | Value | Usage | Rule |
|-------|-------|-------|------|
| DS-SPC-01 | `--space-unit` = {value} | Base spacing unit | All spacing MUST be multiples of this unit |
| DS-SPC-02 | `--space-xs` = {value} | Inline padding, icon gaps | MUST NOT use arbitrary values |
| DS-SPC-03 | `--space-sm` = {value} | Input padding, tight groups | Use between related elements |
| DS-SPC-04 | `--space-md` = {value} | Card padding, section gaps | Default component spacing |
| DS-SPC-05 | `--space-lg` = {value} | Section separators | Use between distinct sections |
| DS-SPC-06 | `--space-xl` = {value} | Page-level margins | Top-level layout only |
<!-- end: UXP-sourced -->

### Motion & Animation
<!-- begin: UXP-sourced -->
| Token | Value | Usage | Rule |
|-------|-------|-------|------|
| DS-MOT-01 | `--duration-fast` = {value} | Micro-interactions (hover, focus) | MUST respect prefers-reduced-motion |
| DS-MOT-02 | `--duration-normal` = {value} | Transitions (expand, slide) | MUST respect prefers-reduced-motion |
| DS-MOT-03 | `--duration-slow` = {value} | Page transitions, modals | MUST respect prefers-reduced-motion |
| DS-MOT-04 | `--easing-default` = {value} | Standard easing curve | MUST use for all transitions |
<!-- end: UXP-sourced -->

### Elevation & Shadows
<!-- begin: UXP-sourced -->
| Token | Value | Usage | Rule |
|-------|-------|-------|------|
| DS-ELEV-01 | `--shadow-sm` = {value} | Cards, dropdowns | MUST use token — NEVER hardcode shadow |
| DS-ELEV-02 | `--shadow-md` = {value} | Modals, popovers | Floating elements only |
| DS-ELEV-03 | `--shadow-lg` = {value} | Drawers, overlays | Highest elevation |
<!-- end: UXP-sourced -->

---

## Component Rules

### Component Inventory
<!-- begin: UXP-sourced -->
| ID | Component | States | Variants | Rule |
|----|-----------|--------|----------|------|
| DS-CMP-01 | {Button} | default, hover, active, disabled, loading | primary, secondary, ghost, destructive | MUST use — NEVER create custom button styles |
| DS-CMP-02 | {Input} | default, focus, error, disabled, readonly | text, number, password, search | MUST show error state with DS-COL-04 |
| DS-CMP-03 | {Card} | default, interactive, selected | standard, compact, media | MUST use DS-ELEV-01 for elevation |
| DS-CMP-04 | {Modal} | open, closing | dialog, confirmation, full-screen | MUST trap focus; MUST use DS-ELEV-02 |
| DS-CMP-05 | {Navigation} | default, active, collapsed | top-bar, sidebar, breadcrumb | MUST support keyboard navigation |
| DS-CMP-06 | {Table} | default, loading, empty, error | standard, compact, selectable | MUST support sorting + pagination |
| DS-CMP-07 | {Toast/Alert} | info, success, warning, error | dismissible, persistent | MUST use role="alert" or aria-live |
| DS-CMP-08 | {Form Group} | default, error, success | inline, stacked, horizontal | MUST associate label + input + error |
<!-- end: UXP-sourced -->

### Component Usage Rules
<!-- begin: UXP-sourced -->
| Rule | Standard |
|------|----------|
| DS-USE-01 | MUST use design system components — NEVER create one-off UI elements that duplicate existing components |
| DS-USE-02 | MUST NOT modify component tokens inline — override via theme layer only |
| DS-USE-03 | MUST use the documented states — NEVER invent additional visual states |
| DS-USE-04 | MUST follow the variant hierarchy — primary for main action, secondary for supporting, ghost for tertiary |
| DS-USE-05 | MUST NOT nest interactive components (no buttons inside buttons, no links inside buttons) |
| DS-USE-06 | New component proposals MUST include: use case, states, variants, accessibility spec, token usage |
<!-- end: UXP-sourced -->

---

## Pattern Library

### Layout Patterns
<!-- begin: UXP-sourced -->
| Pattern | When to Use | Rule |
|---------|------------|------|
| DS-PAT-01 | {Page layout — e.g., sidebar + content} | MUST use for all authenticated pages |
| DS-PAT-02 | {Form layout — stacked fields} | MUST use for all data-entry flows |
| DS-PAT-03 | {List/Table layout — data display} | MUST use for >5 items; cards for ≤5 |
| DS-PAT-04 | {Dashboard layout — grid/masonry} | MUST use for overview/analytics pages |
<!-- end: UXP-sourced -->

### Interaction Patterns
<!-- begin: UXP-sourced -->
| Pattern | Standard |
|---------|----------|
| DS-INT-01 | Loading: skeleton screens for content areas; spinner for actions. MUST NOT use both simultaneously |
| DS-INT-02 | Empty states: illustration + message + CTA. MUST NOT show blank areas |
| DS-INT-03 | Error states: inline for field-level; toast for action-level; page for system-level |
| DS-INT-04 | Confirmation: destructive actions MUST require explicit confirmation (modal or undo) |
| DS-INT-05 | Progressive disclosure: complex forms MUST use stepped/wizard pattern |
<!-- end: UXP-sourced -->

---

## Accessibility Governance
<!-- begin: UXP-sourced -->
| Rule | Standard |
|------|----------|
| DS-A11Y-01 | WCAG {wcag-level} compliance is MANDATORY — not aspirational |
| DS-A11Y-02 | Color MUST NOT be the only means of conveying information (use icons, text, patterns) |
| DS-A11Y-03 | All interactive elements MUST have visible focus indicators (min 3:1 contrast) |
| DS-A11Y-04 | All images MUST have alt text (decorative = alt="") |
| DS-A11Y-05 | Form inputs MUST have associated labels (visible or aria-label) |
| DS-A11Y-06 | Dynamic content changes MUST use aria-live regions |
| DS-A11Y-07 | Touch targets MUST be ≥44×44px |
| DS-A11Y-08 | Motion MUST respect `prefers-reduced-motion` — reduce or remove animations |
| DS-A11Y-09 | Text MUST meet minimum contrast: {AA-ratio} normal text, {AA-ratio-large} large text |
| DS-A11Y-10 | Keyboard navigation MUST follow logical tab order; no focus traps (except modals) |
<!-- end: UXP-sourced -->

---

## Theme & Customization
<!-- begin: UXP-sourced -->
| Rule | Standard |
|------|----------|
| DS-THM-01 | Theming MUST use CSS custom properties (tokens) — NEVER override component internals |
| DS-THM-02 | Dark mode (if supported): MUST define a complete token set — NEVER invert colors programmatically |
| DS-THM-03 | Multi-brand (if applicable): MUST use token aliasing — component code MUST NOT reference brand directly |
| DS-THM-04 | User preference MUST be respected: system theme → explicit choice → persist in storage |
<!-- end: UXP-sourced -->

---

## Governance & Extension
<!-- begin: UXP-sourced -->
| Rule | Standard |
|------|----------|
| DS-GOV-01 | Design system changes MUST go through design review (not just code review) |
| DS-GOV-02 | New tokens MUST follow the naming convention: `--{category}-{property}-{variant}` |
| DS-GOV-03 | Deprecated tokens/components MUST have migration path documented before removal |
| DS-GOV-04 | Token updates MUST be versioned — breaking changes require major version bump |
| DS-GOV-05 | Component additions MUST include: visual spec, accessibility spec, interaction spec, code example |
<!-- end: UXP-sourced -->
```

---

## Filling Instructions

Refer to `mapping/uxd-to-design-system.md` for the complete extraction and transformation rules.

### Source Artifacts (from UXP)

| UXP Document | Fills Section |
|---|---|
| Design System Document | Design Identity, Color Palette, Typography, Spacing, Motion, Elevation |
| Design Tokens Specification | All token values (copy verbatim — NEVER paraphrase token names/values) |
| Component Inventory (with states) | Component Rules table |
| Interaction Patterns | Pattern Library |
| Accessibility Baseline | Accessibility Governance |
| Voice & Tone Guidelines | Design Identity (brand voice summary) |

### Key Filling Rules

1. **Token values are VERBATIM.** Copy token names and values exactly as AI-UXD produced them. Do not rename, reformat, or abbreviate.
2. **Component states are exhaustive.** Every state from the UXP component inventory MUST appear in the component table. Do not omit states.
3. **WCAG level is non-negotiable.** Whatever AI-UXD's accessibility baseline specifies, this file enforces. It's not a suggestion.
4. **Rule IDs are sequential per section.** DS-COL-01, DS-COL-02, etc. If UXP has more tokens than the template shows, extend the table.
5. **Prescriptive language only.** Every rule uses MUST/MUST NOT/NEVER. No "should" or "consider."
6. **Provenance markers preserved.** All `<!-- begin: UXP-sourced -->` sections are subject to reconciliation. Team additions go BELOW the `<!-- end: UXP-sourced -->` marker.

### Interaction with Other Files

| Relationship | Description |
|---|---|
| `frontend-standards.md` | References this file for token usage. If both exist, `frontend-standards` handles code patterns; `design-system` handles visual/interaction governance. No overlap. |
| AI-GCE | Derives accessibility enforcement hooks from the DS-A11Y-* rules |
| `ui-implementation-spec.md` | Detailed per-page spec references components defined here |
| `technical-environment.md` | Frontend Patterns section references this file's token format |

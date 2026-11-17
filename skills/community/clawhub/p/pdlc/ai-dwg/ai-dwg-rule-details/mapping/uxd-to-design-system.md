<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: UX Design Package (AI-UXD) → design-system.md (UXD CLUSTER)

## Purpose

Transforms the design system, design tokens, component inventory, and accessibility baseline produced by AI-UXD into a prescriptive steering file that governs all UI implementation in the destination workspace. This is the core UXD-cluster mapping — the design system steering file is the single source of truth for visual and interaction governance.

**Output:** `rules/design-system.md`

**Condition:** Generate IF `uxd-state.md` is present (UXD peer input detected).

**Cluster:** UX — this output belongs exclusively to the UXD input cluster.

---

## MANDATORY: Stage Sub-Role — UX Designer

During THIS activity, ALSO adopt the mindset of a **UX Designer**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in systems, not screens — a design system is a living vocabulary of constraints, not a style guide
- Tokens are API contracts between design and code — treat names/values with the same precision as API fields
- Components are behavioral specifications, not just visual — states and interactions matter as much as appearance
- Accessibility is structural, not cosmetic — if WCAG compliance fails at the steering level, no amount of code review fixes it
- Respect the designer's intent — extract verbatim; do NOT reinterpret, simplify, or "improve" the token values

### Anti-Patterns for This Activity
- Do NOT rename tokens — use the exact names AI-UXD produced (they may reference a token format standard like W3C Design Tokens)
- Do NOT merge or collapse tokens that look similar — if AI-UXD defined both `--color-info` and `--color-primary`, they serve different purposes
- Do NOT paraphrase component state descriptions — copy the state names and their behavioral definitions exactly
- Do NOT omit "obvious" accessibility rules — explicit is better than assumed (AI-GCE derives enforcement from what's written)
- Do NOT skip motion/animation tokens — reduced-motion governance is a first-class concern

### Quality Check
A good output from this activity sounds like:
- "DS-COL-01: `--color-primary` = #2563EB. MUST use for all primary CTAs. MUST NOT use raw hex — always reference token."
- "DS-CMP-04: Modal. States: open, closing. Variants: dialog, confirmation, full-screen. MUST trap focus; MUST use DS-ELEV-02."
- "DS-A11Y-03: All interactive elements MUST have visible focus indicators (min 3:1 contrast ratio against adjacent colors)."

---

## Source Inputs

**Primary source:** AI-UXD → UX Design Package (UXP), accessed via `uxd-state.md` marker.

### UXP Documents to Read

| UXP Document | What to Extract | Maps to Template Section |
|---|---|---|
| **Design System Document** | Color palette, typography scale, spacing system, elevation/shadows, motion tokens, brand voice summary | Design Identity + Design Tokens (all subsections) |
| **Design Tokens Specification** | Exact token names, values, and categories in their specified format | Design Tokens (all values — VERBATIM) |
| **Component Inventory** | Component list with all states, variants, and interaction behaviors | Component Rules (inventory table + usage rules) |
| **Interaction Patterns** | Layout patterns, loading/empty/error state conventions, progressive disclosure | Pattern Library |
| **Accessibility Baseline** | WCAG level, specific requirements, contrast ratios, touch targets, motion policy | Accessibility Governance |
| **Voice & Tone Guidelines** | Brand voice summary (1-2 sentences for the identity header) | Design Identity (`Brand Voice` field) |

### How to Locate UXP Documents

From `uxd-state.md`, look for the following relative to its directory:

```
UXP document detection patterns:
  Design System:      *Design_System* | *design-system* | design/design-system*
  Design Tokens:      *Design_Tokens* | *tokens* | design/tokens*
  Component Inventory: *Component_Inventory* | *components* | design/components*
  Interaction Patterns: *Interaction_Patterns* | *patterns* | design/patterns*
  Accessibility:      *Accessibility_Baseline* | *accessibility* | validate/accessibility*
  Voice & Tone:       *Voice_Tone* | *voice-tone* | design/voice*
```

### `uxd-state.md` Fields Used

| Field | Used For |
|-------|----------|
| `Completed Stages` | Confirms UXP completeness — expect Stages 7-10 (Design phase) complete minimum |
| `WCAG Target` | Quick reference for accessibility level (also in Accessibility Baseline doc) |
| `Token Format` | Determines token output format (W3C Design Tokens / Style Dictionary / custom) |
| `Design Depth` | Minimal/Standard/Comprehensive — affects how many tokens/components to expect |

---

## Transformation Contract

### Rule 1: Token Values Are VERBATIM

```
INPUT  (from UXP Design Tokens):
  color:
    primary: "#2563EB"
    secondary: "#7C3AED"

OUTPUT (in design-system.md):
  | DS-COL-01 | `--color-primary` = #2563EB | Primary actions, brand identity | MUST use for all primary CTAs |
  | DS-COL-02 | `--color-secondary` = #7C3AED | Secondary actions | MUST use for secondary buttons |
```

**NEVER** rename, reformat, abbreviate, or "improve" token names or values. If AI-UXD used `--space-unit`, the output uses `--space-unit` — not `--spacing-base` or `--sp-1`.

### Rule 2: Component States Are Exhaustive

Every state listed in the UXP Component Inventory MUST appear in the component table. If UXP defines a button with states `[default, hover, active, focus, disabled, loading, error]`, ALL seven appear.

```
INPUT  (from UXP Component Inventory):
  Button:
    states: [default, hover, active, focus, disabled, loading]
    variants: [primary, secondary, ghost, destructive, icon-only]

OUTPUT (in design-system.md):
  | DS-CMP-01 | Button | default, hover, active, focus, disabled, loading | primary, secondary, ghost, destructive, icon-only | MUST use — NEVER create custom button styles |
```

### Rule 3: Accessibility Level Is Non-Negotiable

Whatever AI-UXD's accessibility baseline specifies, this file enforces at the steering level. It is not a suggestion — it is a hard constraint that AI-GCE derives hooks from.

```
INPUT  (from UXP Accessibility Baseline):
  Target: WCAG 2.1 Level AA
  Contrast: 4.5:1 normal text, 3:1 large text
  Touch targets: ≥44×44px

OUTPUT (in design-system.md):
  | DS-A11Y-01 | WCAG 2.1 Level AA compliance is MANDATORY — not aspirational |
  | DS-A11Y-09 | Text MUST meet minimum contrast: 4.5:1 normal text, 3:1 large text |
  | DS-A11Y-07 | Touch targets MUST be ≥44×44px |
```

### Rule 4: Pattern Library Maps Behavioral Conventions

Interaction patterns from UXP define HOW the UI behaves in standard situations. These become enforceable steering rules, not just suggestions.

```
INPUT  (from UXP Interaction Patterns):
  Loading convention: skeleton screens for content, spinner for actions
  Empty state: illustration + message + CTA
  Error: inline for fields, toast for actions, page for system

OUTPUT (in design-system.md):
  | DS-INT-01 | Loading: skeleton screens for content areas; spinner for actions. MUST NOT use both simultaneously |
  | DS-INT-02 | Empty states: illustration + message + CTA. MUST NOT show blank areas |
  | DS-INT-03 | Error states: inline for field-level; toast for action-level; page for system-level |
```

### Rule 5: Motion Tokens Include prefers-reduced-motion Governance

Every motion/animation token MUST include the reduced-motion rule. This is structural accessibility — not optional.

```
INPUT  (from UXP Design Tokens — motion section):
  duration:
    fast: 100ms
    normal: 250ms
    slow: 400ms

OUTPUT (in design-system.md):
  | DS-MOT-01 | `--duration-fast` = 100ms | Micro-interactions (hover, focus) | MUST respect prefers-reduced-motion |
  | DS-MOT-02 | `--duration-normal` = 250ms | Transitions (expand, slide) | MUST respect prefers-reduced-motion |
  | DS-MOT-03 | `--duration-slow` = 400ms | Page transitions, modals | MUST respect prefers-reduced-motion |
```

### Rule 6: Theming Rules Derive from Token Architecture

If UXP defines dark mode tokens, multi-brand token sets, or theme switching behavior, map to the Theme & Customization section. If UXP only defines a single theme, include only DS-THM-01 and DS-THM-04 (base theming rules).

### Rule 7: Governance Rules Map from UXP Design QA Framework

If AI-UXD produced a Design QA framework or extension governance rules, they map to the Governance & Extension section. These define how the design system evolves (review process, deprecation, versioning).

---

## Section-by-Section Mapping

### Design Identity

| Field | Source |
|-------|--------|
| System Name | UXP Design System document title or `uxd-state.md` project name |
| Version | `uxd-state.md` version field or "1.0.0" if not specified |
| WCAG Target | UXP Accessibility Baseline → target level |
| Brand Voice | UXP Voice & Tone Guidelines → 1-sentence summary |
| Token Format | `uxd-state.md` Token Format field |

### Design Tokens — Color Palette

| UXP Source | Extraction |
|---|---|
| Design Tokens → `color` category | Extract ALL color tokens. Map each to a DS-COL-NN rule |
| For each token: name, value, semantic usage | Name → Token column; Value → Value column; Usage from UXP spec or inferred from name |
| Rule column | "MUST use for {usage purpose}" or "MUST NOT use raw hex — always reference token" |

**Minimum expected tokens:** primary, secondary, surface, error, success, warning, text-primary, text-secondary. If UXP provides more (info, disabled, brand-accent, etc.), extend the table.

### Design Tokens — Typography Scale

| UXP Source | Extraction |
|---|---|
| Design Tokens → `typography` or `font` category | Extract ALL typography tokens |
| Families, sizes, weights, line-heights | Each becomes a DS-TYP-NN rule |
| Size unit governance | Add "MUST use rem — NEVER px for font-size" if UXP specifies rem-based scale |

### Design Tokens — Spacing System

| UXP Source | Extraction |
|---|---|
| Design Tokens → `spacing` or `space` category | Extract ALL spacing tokens |
| Base unit + scale | DS-SPC-01 = base unit; remaining tokens = the scale |
| Rule | "All spacing MUST be multiples of base unit" + "MUST NOT use arbitrary values" |

### Design Tokens — Motion & Animation

| UXP Source | Extraction |
|---|---|
| Design Tokens → `motion` or `duration` or `animation` category | Extract ALL motion tokens |
| Duration values + easing curves | Each becomes DS-MOT-NN |
| **Mandatory addition** | EVERY motion token MUST include "MUST respect prefers-reduced-motion" |

### Design Tokens — Elevation & Shadows

| UXP Source | Extraction |
|---|---|
| Design Tokens → `elevation` or `shadow` category | Extract ALL shadow tokens |
| Shadow values | Each becomes DS-ELEV-NN |
| Rule | "MUST use token — NEVER hardcode shadow values" |

### Component Rules — Inventory

| UXP Source | Extraction |
|---|---|
| Component Inventory document | Extract component name, ALL states, ALL variants |
| Behavioral notes (from UXP) | Map to rule column |
| Accessibility notes per component | Include in rule (e.g., "MUST trap focus" for modals) |

**For each component, produce one DS-CMP-NN row.** If UXP defines 15 components, produce 15 rows. Do not truncate.

### Component Rules — Usage Rules

| UXP Source | Extraction |
|---|---|
| Component governance section (if in UXP) | Direct mapping to DS-USE rules |
| Implied from component architecture | "MUST use design system components — NEVER one-off elements" etc. |

**Minimum rules (always include):** use DS components, don't modify tokens inline, use documented states, follow variant hierarchy, no nested interactives, new proposals need spec.

### Pattern Library — Layout Patterns

| UXP Source | Extraction |
|---|---|
| Interaction Patterns → layout section | Map each layout convention to DS-PAT-NN |
| Wireframe specifications | Infer layout patterns from page templates (sidebar+content, form, list, dashboard) |

### Pattern Library — Interaction Patterns

| UXP Source | Extraction |
|---|---|
| Interaction Patterns → behavioral conventions | Map loading, empty, error, confirmation, progressive disclosure |
| Each convention becomes DS-INT-NN | Prescriptive: "MUST use skeleton" not "consider using skeleton" |

### Accessibility Governance

| UXP Source | Extraction |
|---|---|
| Accessibility Baseline document | Direct mapping — every requirement becomes DS-A11Y-NN |
| WCAG level → DS-A11Y-01 | Non-negotiable framing |
| Specific criteria (contrast, focus, targets, motion, ARIA) | One rule per concrete requirement |

**Minimum rules (always include):** WCAG level, color-not-only-means, focus indicators, alt text, form labels, aria-live, touch targets, reduced motion, contrast ratios, tab order.

### Theme & Customization

| UXP Source | Extraction |
|---|---|
| Design System → theming section (if present) | Map to DS-THM rules |
| Dark mode token set (if defined) | DS-THM-02 with specific guidance |
| Multi-brand tokens (if defined) | DS-THM-03 with aliasing rules |
| If no theming section in UXP | Include only DS-THM-01 (tokens-only override) + DS-THM-04 (user preference) |

### Governance & Extension

| UXP Source | Extraction |
|---|---|
| Design QA Framework (if produced by AI-UXD) | Map review process, deprecation, versioning to DS-GOV rules |
| Token naming convention (from token spec) | DS-GOV-02 with the specific convention |
| If no governance section in UXP | Include minimum set: review required, naming convention, deprecation path, versioning, addition spec |

---

## Interaction with Other Mappings

| Related Mapping | Relationship |
|---|---|
| `containers-to-frontend.md` | `frontend-standards.md` handles code patterns (state mgmt, API calls, testing). `design-system.md` handles visual + interaction governance. If ADLC AND UXD both present, both files generate — no overlap. UXD tokens are referenced FROM frontend-standards, not duplicated. |
| `vision-to-workspace-rules.md` | If UXD-only (no ADLC), `workspace-rules.md` gets a minimal identity header (no Architecture Identity — deferred). See identity-assembly fix (Action 11). |
| `ap-uxp-to-tech-environment.md` (Action 7) | `technical-environment.md` Frontend Patterns section references the design system token format and component architecture defined here. |

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| UXP has fewer tokens than template expects | Generate only what UXP provides. Do NOT invent tokens. Mark missing categories with `<!-- UXP did not define: {category} -->` |
| UXP has MORE tokens than template shows | Extend the table. The template is a minimum — add rows for every token in UXP |
| Token names use a non-CSS format (e.g., Figma slugs) | Use the token name as-is. Add a note: `<!-- Token format: {format}. Transform to CSS custom properties during build. -->` |
| Component has no explicit states in UXP | Use minimum: `default, disabled`. Flag: `<!-- States not fully specified in UXP — verify with designer -->` |
| UXP accessibility baseline is less strict than ADLC constraint | This is a **cross-input conflict** — surface via the conflict-surfacing gate (core-generator Phase B). Do NOT resolve here. |
| UXP defines tokens that conflict with ADLC technology choices | Cross-input conflict — same handling as above. |
| No UXP accessibility baseline document | Use `uxd-state.md` WCAG Target field as minimum. Include standard DS-A11Y rules with that level. |

---

## Output Validation

After generating `design-system.md`, verify:

- [ ] ALL token names match UXP exactly (verbatim — no renames)
- [ ] ALL component states from UXP inventory are present (exhaustive)
- [ ] WCAG level matches UXP accessibility baseline
- [ ] Every rule uses MUST/MUST NOT/NEVER (prescriptive)
- [ ] Provenance markers (`<!-- begin: UXP-sourced -->`) wrap all UXP-derived content
- [ ] Rule IDs are sequential per section (DS-COL-01, DS-COL-02, ...)
- [ ] No duplicate rule IDs across sections
- [ ] Motion tokens all include prefers-reduced-motion governance
- [ ] Template placeholder `{...}` syntax used for ALL values that come from UXP at generation time
- [ ] Filling instructions reference this mapping file

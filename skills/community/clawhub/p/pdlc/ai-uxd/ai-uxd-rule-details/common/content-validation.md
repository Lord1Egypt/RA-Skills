<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-UXD — Content Validation Rules

**Purpose:** Quality rules that every AI-UXD artifact must pass before stage gate approval. Use this as a checklist for artifact review.

---

## Universal Rules (Apply to ALL Artifacts)

### Formatting
- [ ] Markdown format with proper heading hierarchy (H1 = document title, H2 = sections)
- [ ] Tables use consistent column widths and alignment
- [ ] Code blocks use proper language identifiers where applicable
- [ ] No orphaned links (every link resolves to an existing artifact or external resource)
- [ ] Consistent date format: ISO 8601 (`YYYY-MM-DD`)

### Content Quality
- [ ] Zero project-specific hardcoded content — all project values use `{placeholder}` syntax
- [ ] No lorem ipsum or filler text — every content slot has either real content or `{placeholder}`
- [ ] Professional language — no casual tone, no hedging ("maybe", "perhaps", "could be")
- [ ] Actionable — every section tells the reader what to DO, not just what to know
- [ ] Concise — no redundant explanations; say it once, clearly

### Traceability
- [ ] Every artifact references its source (which stage produced it, what input informed it)
- [ ] Personas referenced by name (not "User Type 1")
- [ ] Journeys reference their owning persona
- [ ] Flows reference their owning journey stage
- [ ] Components reference the flows/screens where they appear
- [ ] Tokens reference the design principles they serve

### Provenance (NAMING_AND_OWNERSHIP.md §5.2)
- [ ] Front-matter present on all generated artifacts:
```yaml
---
generatedBy: AI-UXD
generatedVersion: 1.0.0
source: {upstream-doc-path}
generatedOn: {ISO-date}
ownership: generated | hybrid | user
---
```

---

## Per-Artifact-Type Rules

### Personas
- [ ] Each persona has: Name, Role/Context, Goals (≥2), Pain Points (≥2), Behaviors, Quoted Need
- [ ] Goals are outcome-oriented ("Complete X in Y time") not feature-oriented ("Use button Z")
- [ ] No demographic-only personas — must include behavioral data
- [ ] At Comprehensive depth: includes empathy map (Think/Feel/Say/Do)
- [ ] JTBD framing present: "When {situation}, I want to {motivation}, so I can {expected outcome}"

### Journey Maps
- [ ] Structured as: Stages → Actions → Touchpoints → Emotions → Opportunities
- [ ] Each journey has: owning persona, starting trigger, end state
- [ ] Emotions mapped per stage (positive/neutral/negative with intensity)
- [ ] Opportunities linked to design decisions downstream
- [ ] Error/edge-case paths explicitly shown (not just the happy path)
- [ ] Onboarding represented as an explicit journey where relevant

### Information Architecture
- [ ] Contains all four IA systems: Organization, Labeling, Navigation, Search
- [ ] Site map present with clear hierarchy (max 3 levels deep for navigation)
- [ ] Navigation model specified (global + local + contextual + utility)
- [ ] Labeling system defined (terminology glossary for the product)
- [ ] Validated against personas: "Can {persona} complete {goal} via this structure?"

### User Flows
- [ ] Each flow has: entry point, exit point(s), decision diamonds, error branches
- [ ] Flow type declared: Task Flow (single path) / User Flow (multi-path) / Wireflow (with UI)
- [ ] All decision points have both Yes/No (or equivalent) paths drawn
- [ ] Error paths lead to recovery (never dead-end)
- [ ] Mapped back to journey stage (traceability)
- [ ] States identified: what data is the system in at each step?

### Design System
- [ ] Design principles: 4-6 principles, each with a "This means..." concrete implication
- [ ] Color system: palette + semantic roles + contrast ratios documented
- [ ] Typography: complete type ramp with sizes, weights, line heights, use cases
- [ ] Spatial system: grid definition + breakpoints + responsive behavior rules
- [ ] Iconography: style guide + sizing scale + usage rules
- [ ] Voice & tone: principles + patterns per context (error, success, empty, onboarding, CTA)
- [ ] All values expressed as tokens (Global → Semantic → Component tiers)

### Design Tokens
- [ ] Follows W3C Design Tokens Format Module structure
- [ ] Token naming convention defined and consistent (e.g., `color.primary.500`)
- [ ] Three tiers present: Global (raw), Alias/Semantic (purpose), Component (scoped)
- [ ] Every token has: name, value, type, description
- [ ] No magic numbers — every dimension traces to a token

### Component Library
- [ ] Each component has: visual spec, ALL states, interactions, responsive behavior, accessibility
- [ ] States covered: default, hover, focus, active, disabled, loading, error, empty, skeleton
- [ ] Keyboard interaction defined for every interactive component
- [ ] ARIA roles/properties specified
- [ ] Atomic Design level declared (atom/molecule/organism)
- [ ] Content constraints defined (character limits, truncation, overflow behavior)

### Accessibility Baseline
- [ ] WCAG conformance target stated (Level AA minimum)
- [ ] Organized by POUR principles
- [ ] Per-component accessibility requirements defined
- [ ] Keyboard interaction patterns documented
- [ ] Screen reader expectations per component
- [ ] Color contrast ratios verified against token values
- [ ] Motion accessibility addressed (prefers-reduced-motion)

### Wireframes
- [ ] Screen inventory complete (every unique state from flows)
- [ ] Layout zones defined (header, nav, content, sidebar, footer patterns)
- [ ] Content hierarchy visible (what's primary, secondary, tertiary)
- [ ] Interaction points marked (what's clickable/tappable)
- [ ] Responsive behavior annotated per breakpoint

---

## Cross-Reference Validation

After all stages complete, verify the following cross-references are intact:

| From | To | Check |
|------|----|-------|
| Persona | Journey | Every persona has ≥1 journey |
| Journey | Flow | Every journey stage maps to ≥1 flow |
| Flow | Screen | Every flow step maps to a screen in the inventory |
| Screen | Component | Every screen uses only components from the library |
| Component | Token | Every component value traces to a token |
| Token | Principle | Every semantic token connects to a design principle |
| Component | Accessibility | Every interactive component has accessibility spec |

---

## File Naming Convention

| Artifact Type | Pattern | Example |
|---------------|---------|---------|
| Persona | `Persona_{NN}_{Name}.md` | `Persona_01_Healthcare_Admin.md` |
| Journey | `Journey_{NN}_{Persona}_{Goal}.md` | `Journey_01_Admin_Onboarding.md` |
| Flow | `Flow_{NN}_{Task}.md` | `Flow_01_Create_Patient_Record.md` |
| Component | `Component_{Name}.md` | `Component_Button.md` |
| Wireframe | `Wireframe_{Screen}.md` | `Wireframe_Dashboard_Home.md` |

---

*Part of AI-UXD v1.0.0 | Reference: core-workflow.md § Key Principles*

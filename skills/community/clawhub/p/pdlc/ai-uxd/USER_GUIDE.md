# AI-UXD — User Guide

**Package:** AI-UXD (AI-Driven UX Design Life Cycle)
**Version:** 1.0.0
**Audience:** UX Designers, Product Designers, Frontend Developers, Product Managers, Design System Leads

---

## What is AI-UXD?

AI-UXD is an injectable UX design lifecycle that guides you from user research to a governed design system — producing artifacts that downstream development tools can consume directly. It reasons and writes as a senior UX designer, producing professional-grade deliverables (personas, journeys, information architecture, user flows, design tokens, component library, accessibility baseline) without requiring prior UX expertise.

**In one sentence:** AI-UXD turns business intent and user research into a governed UX Design Package (UXP) — the missing design foundation that downstream packages assume but nothing else produces.

---

## When to Use AI-UXD

| Scenario | AI-UXD helps you... |
|----------|---------------------|
| New product needs UX foundations | Build personas, journeys, IA, and design system from scratch |
| Development needs design tokens | Produce W3C-aligned token architecture (global → semantic → component) |
| Need component specifications | Define every component with all states, accessibility, responsive behavior |
| Accessibility must be embedded | WCAG 2.2 baseline baked into every stage, not bolted on |
| Existing product needs design system governance | Brownfield mode — audit, baseline, and govern incrementally |

---

## How It Works (5 Minutes)

1. **Install** — Copy package files into your IDE's steering folder (see `setup/INSTALL.md`)
2. **Start a session** — Say: *"Using AI-UXD, design the UX for this product"*
3. **Provide context** — A PIP, Architecture Package, or verbal description of the product
4. **Approve at gates** — Every stage produces deliverables requiring your sign-off
5. **Get your UXP** — A complete UX Design Package ready for AI-DWG, AI-POLC, or manual development

---

## Input Modes

AI-UXD detects what you already have and adapts:

| What You Have | Mode | Behavior |
|---------------|------|----------|
| PIP + Architecture Package | Mode A — Full chain | Richest context: reads scope, constraints, users, tech stack. Minimal questions. |
| PIP only | Mode B — Initiation-enriched | Reads project scope, stakeholders, goals. Asks architecture questions. |
| Standalone (no upstream) | Mode C — Independent | Full questionnaire. You provide product vision, users, and constraints conversationally. |
| Existing design artifacts | Mode D — Brownfield | Audits current state, identifies gaps, applies progressive governance. |

You do NOT need any predecessor. AI-UXD works standalone — upstream enriches, absence doesn't block.

---

## The Workflow (5 Phases, 16 Stages)

### Phase 1: Discover (Stages 1–3)

Research users, synthesize findings, build understanding.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 1 — Research Synthesis | Compiles user research, market context, business goals | Confirm research inputs are complete |
| 2 — Persona Development | Creates evidence-backed personas with JTBD and accessibility considerations | Approve personas |
| 3 — Journey Mapping | Maps end-to-end journeys with emotional tracking and error paths | Approve journey maps |

### Phase 2: Define (Stages 4–6)

Structure the information space and user paths.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 4 — Information Architecture | Organization, labeling, navigation, and search systems | Approve IA structure |
| 5 — User Flows | Task flows, user flows, wireflows with error/edge-case paths | Approve flow designs |
| 6 — Wireframe Specifications | Low-fidelity structural specifications per key screen | Approve wireframe specs |

### Phase 3: Design (Stages 7–10)

Build the design system — tokens, components, theming.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 7 — Design System Foundations | Colors, typography, spatial grid, iconography, voice & tone | Approve design foundations |
| 8 — Design Tokens | W3C-aligned three-tier architecture (global → semantic → component) | Approve token structure |
| 9 — Component Library | Every component with ALL states, interactions, accessibility, responsive behavior | Approve component specs |
| 10 — Multi-Brand Theming | Dark mode, brand variants, token inheritance (conditional — only if needed) | Approve theming approach |

### Phase 4: Validate (Stages 11–13)

Verify accessibility, usability, and implementation fidelity.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 11 — Accessibility Baseline | WCAG 2.2 compliance verification across all artifacts | Approve accessibility report |
| 12 — Usability Validation | Heuristic evaluation + test plan + feedback intake framework | Approve validation approach |
| 13 — Design QA Framework | Governed drift detection for implementation fidelity | Approve QA framework |

### Phase 5: Assemble (Stages 14–16)

Package everything and establish governance.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 14 — Package Assembly | Consolidates all artifacts; cross-references traceability | Confirm package completeness |
| 15 — Governance Setup | Establishes design change governance + UXC__ agent rules | Approve governance model |
| 16 — Handoff Preparation | Prepares UXP for downstream consumption (AI-DWG, AI-POLC) | Final approval — UXP ready |

---

## The Relationship with Connected Packages

AI-UXD has bidirectional relationships:

```
AI-UXD ──(personas/journeys)──► AI-POLC (value-based prioritization)
AI-UXD ──(tokens/components/accessibility)──► AI-DWG (workspace generation)
AI-DLC v1 ──(runtime feedback)──► AI-UXD (design iteration)
```

| Direction | What Flows | When |
|-----------|-----------|------|
| UXD → POLC | Personas and journeys | For value-based backlog prioritization |
| UXD → DWG | Design tokens, component specs, accessibility baseline | For workspace generation |
| POLC → UXD | Value goals | Focus UX research on highest-value outcomes |
| DLC → UXD | Implementation feedback | Design iteration based on development reality |

**Strategy-stage exchange with AI-POLC:** AI-POLC's value goals focus UX research priorities, and AI-UXD's personas/journeys inform POLC's prioritization. They enrich each other.

---

## Adaptive Depth

AI-UXD auto-calibrates based on product complexity:

| Depth | When Applied | What Changes |
|-------|-------------|--------------|
| **Minimal** | Simple product, few user types, clear scope | Streamlined UXP — core personas + key flows + basic design system |
| **Standard** | Typical complexity, multiple user types | Full UXP with all stages and complete component library |
| **Comprehensive** | Enterprise, multi-brand, heavy accessibility, many user types | Multi-brand theming, full i18n/RTL, extended component states |

Override anytime: *"Change depth to Comprehensive"*

---

## Brownfield Mode (Mode D)

Already have design artifacts? AI-UXD doesn't force a restart:

1. **Audit** — Scans existing design system, personas, tokens for completeness
2. **Gap Analysis** — Identifies what's missing (no accessibility baseline? inconsistent tokens?)
3. **Progressive Governance** — Brings existing design under discipline incrementally
4. **Preserve & Enrich** — Builds on what exists; never discards working design decisions

Say: *"I have an existing design system that needs governance"* to activate brownfield mode.

---

## Session Continuity

AI-UXD saves progress in `uxd-state.md`. You can:
- Close your session at any time
- Resume later — AI-UXD reads state and picks up where you left off
- Switch depth mid-workflow
- Skip conditional stages (e.g., multi-brand theming if single-brand)

---

## What You Get (Output Artifacts)

| Artifact | Purpose |
|----------|---------|
| `uxd-state.md` | State tracking + chain marker |
| `01_Research_Synthesis.md` | User research compilation |
| `02_Personas/` | Evidence-backed persona files |
| `03_Journey_Maps/` | End-to-end journey documents |
| `04_Information_Architecture.md` | IA structure + navigation |
| `05_User_Flows/` | Task/user/wireflow documents |
| `06_Wireframe_Specifications/` | Low-fidelity structural specs |
| `07_Design_System/` | Foundations (color, type, grid, icons, voice) |
| `08_Component_Library/` | Full component specs with all states |
| `09_Multi_Brand_Theming.md` | (Conditional) Brand variants + dark mode |
| `10_Accessibility_Baseline.md` | WCAG 2.2 compliance report |
| `11_Usability_Test_Plan.md` | Validation framework |
| `12_Design_QA_Framework.md` | Drift detection rules |
| `UXP_README.md` | Package index + completeness report |

---

## Quick Start Examples

**Full chain (richest context):**
```
Using AI-UXD, design the UX for this product.
I have a PIP from AI-PILC and an Architecture Package from AI-ADLC.
```

**Standalone (no upstream):**
```
Using AI-UXD, I need to design the UX for a project management dashboard.
I'll describe the users and product vision.
```

**Brownfield (existing design):**
```
Using AI-UXD, I have an existing design system with inconsistent tokens
and no accessibility baseline. Help me bring governance.
```

**Component library focus:**
```
Using AI-UXD, I need a complete component library specification
for a healthcare application with strict accessibility requirements.
```

---

## Tips for Best Results

1. **Start with real user understanding** — Even brief persona work dramatically improves downstream design.
2. **Don't skip accessibility** — It's embedded throughout, not a bolt-on. Skipping creates expensive rework.
3. **Approve personas before proceeding** — Everything downstream references them; changes cascade.
4. **Use tokens, not raw values** — Three-tier token architecture prevents design drift in implementation.
5. **Specify ALL component states** — Default, hover, active, disabled, error, loading, empty. Incomplete states cause developer guesswork.
6. **Feed personas to AI-POLC** — Value-based prioritization improves when persona needs are explicit.

---

## What AI-UXD Is NOT

- NOT a design tool replacement (doesn't replace Figma, Sketch, or XD)
- NOT code generation (that's AI-DLC v1)
- NOT product backlog management (that's AI-POLC)
- NOT architecture design (that's AI-ADLC)
- NOT visual mockup creation — it produces specifications, not pixel-perfect visuals

AI-UXD is the **Design System Producer** — it answers *"What should the user experience look like, and how do we govern it?"*

---

## Platform Support

AI-UXD works on: Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, and GitHub Copilot — plus any AI-assisted IDE that supports steering/rules files via the Universal Setup.

See `setup/INSTALL.md` for detailed platform instructions.

---

*AI-UXD v1.0.0 | Part of [AIFLC](../README.md) — the AI-* PDLC Family*

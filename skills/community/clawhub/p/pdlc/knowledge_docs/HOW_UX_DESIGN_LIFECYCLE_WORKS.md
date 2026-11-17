# How the UX Design Lifecycle Works

**Purpose:** Explains how AI-UXD transforms business intent and user research into a governed UX Design Package (UXP) — covering the 5-phase / 16-stage lifecycle, the traceability spine that links persona to token, adaptive depth, conditional generation, and the handoffs that feed AI-POLC, AI-DWG, and AI-GCE.

---

## What AI-UXD Does

AI-UXD is the single producer of the design foundation downstream packages assume but nothing else creates. It turns user research and business context into personas, journeys, information architecture, user flows, a complete design system with tokens, a component library, and an accessibility baseline — all governed, versioned, and consumable without interpretation.

```
PIP (from AI-PILC) + AP (from AI-ADLC) + strategy exchange with AI-POLC
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  AI-UXD LIFECYCLE                                                    │
│                                                                      │
│  DISCOVER → DEFINE → DESIGN → VALIDATE → ASSEMBLE                    │
│  (5 phases, 16 stages)                                               │
│                                                                      │
│  Produces: UX Design Package (UXP)                                   │
│  Feeds: AI-POLC (personas/journeys) + AI-DWG (design system+tokens)  │
│         + AI-GCE (accessibility baseline)                            │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
UX DESIGN PACKAGE (UXP)
├── Research Synthesis
├── Personas (evidence-backed, JTBD-framed)
├── Journey Maps (touchpoints, emotions, error paths)
├── Information Architecture (site map, navigation, taxonomy, search)
├── User Flows (task flows, user flows, wireflows)
├── Wireframe Specifications
├── Design System (color, type, spatial, icons, voice & tone)
├── Design Tokens (W3C-aligned: global → semantic → component)
├── Component Library (every state, interaction, ARIA)
├── Accessibility Baseline (WCAG 2.2 mapped to POUR)
├── Usability Validation Plan
├── Design QA Framework
├── UXP_README.md
└── uxd-state.md (marker)
```

**Hard boundary:** AI-UXD produces governed structure, specifications, and references — it does NOT produce pixel-level comps, design-tool files, or working prototypes. It governs what those tools implement.

---

## Identity and Scope

**Identity spine:** AI-UXD answers *how it looks, how it feels, how it behaves, and whether everyone can use it*. If a concern is about look/feel/behavior + inclusive access → AI-UXD owns it.

**Inclusion rule:** If it answers "what/why/order" → AI-POLC. If it answers "how it's built" → AI-DLC v1. If it answers "is it compliant at runtime" → AI-GCE. If it answers "what's the system architecture" → AI-ADLC. AI-UXD owns the experience layer between them.

---

## The Traceability Spine

The defining mechanism of AI-UXD. Every artifact links to the one before it, so nothing exists without a rationale:

```
persona → journey → flow → screen → component → token → principle
```

| Link | Means |
|------|-------|
| persona → journey | Every journey belongs to a real user with goals and pain points |
| journey → flow | Every flow realizes a stage of a mapped journey |
| flow → screen | Every screen appears in a defined flow (including error/edge paths) |
| screen → component | Every screen is assembled from inventoried components |
| component → token | Every component's visual values reference design tokens, not raw values |
| token → principle | Every token traces to a design principle that justifies it |

Break any link and the system loses its rationale. This spine is what makes the UXP consumable by downstream packages without interpretation — every decision is auditable back to a user need.

---

## The Four Input Modes

AI-UXD detects what the user already has and adapts. It works standalone — upstream enriches, absence never blocks.

| Mode | Input Available | Behavior |
|------|----------------|----------|
| **A — Full Chain** | PIP + Architecture Package | Richest context: reads scope, constraints, users, tech stack. Minimal questions. |
| **B — Initiation-Enriched** | PIP only | Reads project scope, stakeholders, goals. Asks architecture-relevant questions. |
| **C — Independent** | Standalone brief | Full questionnaire — user supplies product vision, users, brand conversationally. |
| **D — Brownfield** | Existing design artifacts | Audits current state, finds gaps, applies progressive governance without restart. |

Mode is detected at Stage 1 and confirmed with the user at the gate.

---

## The Five Phases (Double Diamond)

AI-UXD is structured on the Double Diamond — divergent then convergent thinking, twice over.

```
Discover → Define → Design → Validate → Assemble
    │         │        │         │           │
    │         │        │         │           └── Package & hand off (POLC, DWG, GCE)
    │         │        │         └── Prove it works (accessibility, usability, QA)
    │         │        └── Build the system (wireframes, tokens, components)
    │         └── Structure it (journeys, IA, flows)
    └── Understand the users (research, personas)
```

### Phase 1: Discover (Stages 1–3)

| Stage | What Happens | Deliverable |
|-------|-------------|-------------|
| 1. Workspace Detection & Input Ingestion | Detect mode (A/B/C/D), read predecessor markers, set depth, detect conditional triggers, create state | `uxd-state.md` |
| 2. Research Planning & Synthesis | Define research questions, plan methods, synthesize existing data into themes | Research synthesis |
| 3. Persona Definition | Build evidence-backed personas with goals, pain points, context, JTBD framing | Personas (2–8 by depth) |

**Gate exit:** personas approved → journey work begins. Personas flow to AI-POLC at Stage 14.

### Phase 2: Define (Stages 4–6)

| Stage | What Happens | Deliverable |
|-------|-------------|-------------|
| 4. Journey Mapping | Map end-to-end journeys per persona — touchpoints, emotions, onboarding, error paths | Journey maps |
| 5. Information Architecture | Organization, labeling, navigation model, search strategy (Rosenfeld/Morville 4 systems) | IA document |
| 6. User Flow Design | Task flows, user flows, wireflows with edge cases; map flows to journey stages | User flows |

### Phase 3: Design (Stages 7–10)

| Stage | What Happens | Deliverable |
|-------|-------------|-------------|
| 7. Wireframe & Screen Inventory | Inventory every unique screen/state; low-fidelity wireframe specs (Atomic Design) | Screen inventory + wireframes |
| 8. Design System Foundation | Principles, color, typography, spatial grid, iconography, voice & tone — all as tokens | Design system + tokens |
| 9. Component Library | Every component with full state set, interactions, responsive behavior, ARIA | Component inventory |
| 10. Multi-Brand Theming **(conditional)** | Token inheritance (base → brand → mode), color modes, theme switching | Multi-brand token spec |

### Phase 4: Validate (Stages 11–13)

| Stage | What Happens | Deliverable |
|-------|-------------|-------------|
| 11. Accessibility Baseline | Declare WCAG 2.2 target, map to POUR, link to design decisions, define keyboard + SR behavior | Accessibility baseline |
| 12. Usability Validation Plan | Heuristic checklist, test plan, feedback intake (AI-DLC v1 runtime signals route back here) | Validation plan |
| 13. Design QA Framework | Define design-to-code drift tolerance, comparison dimensions, severity model, report format | Design QA framework |

### Phase 5: Assemble (Stages 14–16)

| Stage | What Happens | Deliverable |
|-------|-------------|-------------|
| 14. AI-POLC Handoff | Package personas + journeys to match AI-POLC's consumer contract | Prioritization-ready bundle |
| 15. AI-DWG / AI-GCE Handoff | Package design system + tokens + component inventory (DWG); accessibility baseline (GCE) | Workspace-ready bundle |
| 16. Package Assembly & UXP README | Assemble UXP, generate `UXP_README.md`, install governance agent, mark complete | Assembled UXP |

---

## Adaptive Depth

AI-UXD scales its output to product complexity. Depth is detected at Stage 1 and can be raised mid-workflow if complexity emerges.

| Depth | When Applied | Effect |
|-------|-------------|--------|
| **Minimal** | Simple app, ≤2 user types, clear scope | 2–3 personas, 1–2 journeys, essential tokens only, fewer questions |
| **Standard** | Typical product, 3–5 user types | Full persona set, journeys per persona, complete design system |
| **Comprehensive** | Complex multi-user platform, accessibility-critical, enterprise | Extended research, empathy maps, service blueprints, multi-brand tokens |

---

## Conditional Generation

Four outputs are generated only when their trigger condition is met — the workflow never produces them speculatively:

| Output | Trigger |
|--------|---------|
| Multi-brand theming + dark mode | IF >1 brand OR color modes required |
| i18n/RTL/localization tokens | IF >1 locale OR multi-language mentioned |
| Service blueprints | IF Comprehensive depth + service-oriented product |
| Empathy maps | IF Comprehensive depth |

Stage 10 (Multi-Brand Theming) is the only stage that may be skipped — all others always execute.

---

## Accessibility by Design

Accessibility is not a phase — it is a constraint embedded at every stage:

| Stage | Accessibility Contribution |
|-------|---------------------------|
| Persona Definition | Include users with disabilities as first-class personas |
| Design System | Contrast ratios baked into color tokens; focus indicators in component states |
| Component Library | ARIA role, keyboard interaction, screen-reader behavior per component |
| Accessibility Baseline (Stage 11) | Consolidates the WCAG 2.2 target against POUR — never starts from zero |

By the time Stage 11 runs, the accessibility work is already done across prior stages. Stage 11 consolidates and declares the conformance target (Level AA minimum), it does not retrofit.

---

## State and Continuity

`uxd-state.md` is the marker file and session-continuity record. It carries the `projectId` front-matter key (camelCase) — extracted from `pilc-state.md` when a PIP is present, otherwise generated. This key correlates the UXP with sibling Project-layer outputs (`adlc-state.md`, `polc-state.md`) that all feed AI-DWG.

The state file tracks:
- Mode (A/B/C/D) and depth (Minimal/Standard/Comprehensive)
- Current phase and stage (1–16)
- Completed stages with artifacts and dates
- Conditional features active (multi-brand, i18n, service blueprints, empathy maps)
- Downstream signals (AI-POLC / AI-DWG / AI-GCE — Pending or Handed Off)

When `uxd-state.md` exists, AI-UXD resumes: it reads the current stage, announces where it is, and offers Resume / Back / Show status.

---

## The Gate Model

Every stage ends with a gate. The workflow does not advance on its own:

1. Present the deliverable summary
2. Ask for explicit approval — "Approve and proceed to Stage {N+1}? [Y/N/Revise]"
3. On revise → iterate the current stage, do not advance
4. On approve → update `uxd-state.md`, log the decision, transition
5. No stage is skippable except Stage 10 (conditional)

---

## Key Interactions

### AI-UXD → AI-POLC (Producer → Consumer, with exchange)

AI-UXD produces personas and journeys; AI-POLC consumes them to ground epics in real user needs and validate prioritization against journey pain points. The exchange is bidirectional: AI-POLC's value goals focus AI-UXD's research priorities. They enrich each other during the strategy stage.

### AI-UXD → AI-DWG (Producer → Consumer)

The design system and tokens seed AI-DWG's `design-system.md` and enrich its `frontend-standards.md` steering. The component inventory feeds AI-DWG's structure generation. Tokens are handed off in W3C-aligned consumable form.

### AI-UXD → AI-GCE (Producer → Consumer)

The accessibility baseline seeds AI-GCE's `accessibility-compliance` rule — the WCAG 2.2 target declared at Stage 11 becomes an enforceable governance rule in the development workspace.

### AI-DLC v1 → AI-UXD (Runtime Feedback)

During delivery, AI-DLC v1 runtime usability and accessibility signals flow back into the UXP through the feedback intake defined at Stage 12 — closing the loop between design intent and implementation reality.

---

## The Governance Agent

At Stage 16, AI-UXD installs the `ux-consistency-agent` (shortcut `UXC__`, AG-ID `UXD-AG-01`) into the workspace `.kiro/agents/`. It validates the UXP on demand:
- Internal consistency across artifacts
- Traceability spine integrity (persona → journey → flow → screen → component → token)
- Token alignment (no raw values where tokens should be used)
- Accessibility spec match (component states vs. baseline)
- Handoff consumability (does the bundle match each consumer's contract?)

It is an on-demand validator — it does not run automatically and does not block the workflow.

---

## Output: The UX Design Package (UXP)

```
{your-project}/ux-design/
├── uxd-state.md                        ← Marker file (chain handoff + session resume)
├── 01_Research_Synthesis.md
├── 02_Personas/                        ← Evidence-backed persona files
├── 03_Journey_Maps/                    ← End-to-end journeys + error paths
├── 04_Information_Architecture.md      ← IA structure + navigation + search
├── 05_User_Flows/                      ← Task / user / wireflow documents
├── 06_Wireframe_Specifications/        ← Low-fidelity structural specs
├── 07_Design_System/                   ← Color, type, grid, icons, voice & tone, tokens
├── 08_Component_Library/               ← Full component specs with all states
├── [09_Multi_Brand_Theming.md]         ← Conditional (>1 brand or color modes)
├── 10_Accessibility_Baseline.md        ← WCAG 2.2 mapped to POUR
├── 11_Usability_Test_Plan.md           ← Validation framework + feedback intake
├── 12_Design_QA_Framework.md           ← Drift detection rules + severity model
└── UXP_README.md                       ← Reading guide, artifact index, traceability map
```

---

## Related Documents

| Document | Location |
|----------|----------|
| How to Design User Experience | `knowledge_docs/HOW_TO_DESIGN_USER_EXPERIENCE.md` |
| How to Design Architecture | `knowledge_docs/HOW_TO_DESIGN_ARCHITECTURE.md` |
| How to Manage Product Backlog | `knowledge_docs/HOW_TO_MANAGE_PRODUCT_BACKLOG.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How Depth Levels Work | `knowledge_docs/HOW_DEPTH_LEVELS_WORK.md` |
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |

*Knowledge Document | Created: 2026-06-13 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

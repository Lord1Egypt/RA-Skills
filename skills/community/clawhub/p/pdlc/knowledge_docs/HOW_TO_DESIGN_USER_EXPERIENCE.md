# How to Design User Experience

**Purpose:** Practical guide for using AI-UXD to transform business intent and user research into a governed UX Design Package (UXP) — personas, journeys, information architecture, user flows, a complete design system with tokens, and an accessibility baseline that AI-DWG, AI-POLC, and AI-GCE consume directly.

---

## Who This Is For

UX designers, product designers, frontend developers, product managers, or design system leads who need to design the experience for a product before implementation begins. You want evidence-backed personas, a real information architecture, W3C-aligned design tokens, a fully-specified component library, and accessibility built in from the start — produced through guided conversation rather than blank-page struggle. You do not need prior UX expertise; AI-UXD reasons and writes as a senior UX designer.

---

## Before You Start

**You need:**
- AI-UXD installed in your AI workspace (see `ai-uxd/setup/INSTALL.md`)
- Input — ANY of the following:
  - A PIP from AI-PILC + an Architecture Package from AI-ADLC (ideal — richest context)
  - A PIP only (scope, stakeholders, goals — no architecture yet)
  - A product or brand brief (standalone)
  - An existing design system you want to bring under governance (brownfield)

**You do NOT need:**
- Prior UX research already done (AI-UXD helps you plan and synthesize it)
- Design tokens or a component library (that's the output, not the input)
- A predecessor package — AI-UXD works standalone; upstream enriches, absence doesn't block

---

## Starting: Standalone vs. Chain

When you activate AI-UXD (type `_UXD_` or say *"Using AI-UXD, design the UX for this product"*), it asks which mode fits your situation:

| You Pick | Mode | What AI-UXD Does |
|----------|------|------------------|
| **[A]** I have a PIP + Architecture Package | Full chain | Reads scope, constraints, users, tech stack from markers. Asks the fewest questions. |
| **[B]** I have a PIP only | Initiation-enriched | Reads project scope, stakeholders, goals. Asks architecture-relevant questions. |
| **[C]** I have a product/brand brief | Standalone | Full questionnaire — you supply vision, users, and brand conversationally. |
| **[D]** I have an existing design system | Brownfield | Audits what exists, finds gaps, governs incrementally — never forces a restart. |

In **chain mode**, AI-UXD detects predecessor markers automatically — `pilc-state.md` for project context and `adlc-state.md` for technical constraints. You don't point it at files; it finds them. In **standalone mode**, you describe the product and users in conversation. Either way, you reach the same UXP.

---

## The Process (16 Stages, 5 Phases)

### Phase 1: Discover — "Who are the users?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 1. Workspace Detection | Detect mode + depth, read predecessor markers, detect conditional triggers, create workspace | Confirm mode and depth level |
| 2. Research Planning & Synthesis | Define research questions, plan methods, synthesize existing data into themes | Confirm research inputs are complete |
| 3. Persona Definition | Build evidence-backed personas with goals, pain points, context, JTBD framing | Approve personas |

**Gate:** Personas approved → journey work begins. (These personas later flow to AI-POLC.)

### Phase 2: Define — "How is it structured?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 4. Journey Mapping | Map end-to-end journeys per persona — touchpoints, emotions, onboarding, error paths | Approve journey maps |
| 5. Information Architecture | Define organization, labeling, navigation model, and search strategy | Approve IA structure |
| 6. User Flow Design | Produce task flows, user flows, wireflows with edge cases | Approve flow designs |

**Gate:** Flows approved → wireframing begins.

### Phase 3: Design — "What's the system?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 7. Wireframe & Screen Inventory | Inventory every screen/state; low-fidelity wireframe specs (Atomic Design) | Approve screen inventory + approach |
| 8. Design System Foundation | Principles, color, typography, spatial grid, iconography, voice & tone — all as tokens | Approve design foundations |
| 9. Component Library | Every component with ALL states, interactions, responsive behavior, ARIA | Approve component specs |
| 10. Multi-Brand Theming | Token inheritance, color modes, theme switching (conditional — only if needed) | Approve theming approach |

**Gate:** Component library approved → validation begins.

### Phase 4: Validate — "Does it work for everyone?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 11. Accessibility Baseline | Declare WCAG 2.2 target, map to POUR, define keyboard + screen-reader behavior | Confirm conformance target |
| 12. Usability Validation Plan | Heuristic checklist + test plan + feedback intake framework | Approve validation approach |
| 13. Design QA Framework | Define design-to-code drift tolerance, severity model, report format | Approve QA framework |

**Gate:** QA framework approved → assembly begins.

### Phase 5: Assemble — "Package it for handoff."

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 14. AI-POLC Handoff | Package personas + journeys to match AI-POLC's consumer contract | Confirm handoff is complete |
| 15. AI-DWG / AI-GCE Handoff | Package design system + tokens + components (DWG); accessibility baseline (GCE) | Confirm handoff packages complete |
| 16. Package Assembly & UXP README | Assemble UXP, generate `UXP_README.md`, install governance agent | Final approval — UXP ready |

---

## What You Decide at Each Gate

Every stage ends with a gate, and the workflow never advances without you. At each gate you can:
- **Approve** — accept the deliverable and move to the next stage
- **Revise** — send it back for iteration; the stage re-runs, nothing advances
- **Skip** — only available at Stage 10 (Multi-Brand Theming), and only when it doesn't apply

The gates exist so you stay in control. Read the deliverable, correct anything the AI misread, add context it missed. Approvals are logged in `uxd-state.md` so the decision trail is auditable.

---

## How Personas and Journeys Flow to the Backlog

Personas (Stage 3) and journey maps (Stage 4) are not just design artifacts — they are the input AI-POLC uses for value-based prioritization. At Stage 14, AI-UXD packages them to match AI-POLC's consumer contract:

- **Personas** ground epics in real user needs instead of abstract requirements
- **Journey pain points** become the evidence for ranking what gets built first
- **JTBD framing** gives AI-POLC the "why this matters" behind each backlog item

The exchange runs both ways: AI-POLC's value goals can focus your UX research priorities back in Phase 1. If you're running the full chain, feed your personas to AI-POLC — prioritization gets sharper when persona needs are explicit.

---

## How the Design System and Tokens Reach the Dev Workspace

At Stage 15, AI-UXD packages the design output for AI-DWG, the workspace generator:

- **Design system + tokens** seed AI-DWG's `design-system.md` and enrich its `frontend-standards.md` steering
- **Component inventory** (with all states and ARIA) feeds AI-DWG's structure generation
- **Tokens** hand off in W3C-aligned form (global → semantic → component) so developers reference tokens, not raw values

This is why the three-tier token architecture matters: it prevents design drift once code starts. A developer who pulls `color.semantic.action.primary` instead of a hex value inherits your design decisions automatically.

The handoff is automatic — AI-DWG detects `uxd-state.md` alongside `adlc-state.md` and `polc-state.md` (all correlated by the same `projectId`) and reads what it needs.

---

## Accessibility from Day One

Accessibility is not Stage 11 — it runs through every stage. By the time you reach the baseline, the work is already done:

- **Stage 3** — users with disabilities are first-class personas, not an afterthought
- **Stage 8** — contrast ratios are baked into color tokens; focus indicators into component states
- **Stage 9** — every component carries its ARIA role, keyboard interaction, and screen-reader behavior
- **Stage 11** — consolidates all of it, declares the WCAG 2.2 conformance target (Level AA minimum), and maps it to POUR

That baseline then seeds AI-GCE's `accessibility-compliance` rule, so the target you declare in design becomes enforceable in the development workspace. Skipping accessibility early creates expensive rework later — embedding it costs almost nothing.

---

## Choosing Your Depth Level

AI-UXD calibrates to product complexity at Stage 1. You can raise it mid-workflow if complexity emerges.

| Depth | Best For | What You Get |
|-------|----------|-------------|
| **Minimal** | Simple product, ≤2 user types, clear scope | 2–3 personas, 1–2 journeys, essential tokens only |
| **Standard** | Typical product, 3–5 user types — recommended | Full persona set, journeys per persona, complete design system |
| **Comprehensive** | Enterprise, multi-brand, accessibility-critical | Extended research, empathy maps, service blueprints, multi-brand tokens |

Override anytime: *"Change depth to Comprehensive."*

---

## Conditional Stages and Outputs

AI-UXD only generates what your product needs:

| Output | Generated When |
|--------|---------------|
| Multi-brand theming + dark mode | More than one brand OR color modes required |
| i18n/RTL/localization tokens | More than one locale OR multi-language mentioned |
| Service blueprints | Comprehensive depth + service-oriented product |
| Empathy maps | Comprehensive depth |

If your product is single-brand and single-locale, AI-UXD skips Stage 10 and the i18n token work entirely — you don't carry artifacts you don't need.

---

## What You Get (The UX Design Package)

```
{your-project}/ux-design/
├── uxd-state.md                        ← Marker file (chain handoff + session resume)
├── 01_Research_Synthesis.md            ← User research compilation
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

## Tips for Better UX Sessions

1. **Start with real user understanding.** Even brief persona work dramatically improves everything downstream. Demographic-only personas (age, job title, nothing else) are useless — push for goals, pain points, and context.

2. **Approve personas carefully.** Everything downstream references them — journeys, flows, prioritization. A change to a persona cascades, so get them right before proceeding.

3. **Don't let polish override structure.** Information architecture and flows come before colors and typography. A beautiful screen with broken flows is a failure. AI-UXD enforces structure-before-surface — work with it.

4. **Use tokens, never raw values.** The three-tier architecture (global → semantic → component) is what prevents drift in implementation. Resist the urge to hardcode a hex value.

5. **Specify ALL component states.** Default, hover, focus, active, disabled, loading, error, empty. A button without its states is half-specified and forces developers to guess.

6. **Don't skip accessibility.** It's embedded, not optional. Engaging with it at each stage costs little; bolting it on after implementation is expensive rework.

7. **Brownfield is different.** If you have an existing design system, say so at Stage 1. AI-UXD audits and governs incrementally — it builds on what works rather than discarding it.

---

## What Happens Next

Your UXP feeds the next packages in the chain:

| Next Package | What It Reads from the UXP |
|-------------|----------------------------|
| **AI-POLC** | Personas + journeys → value-based backlog prioritization |
| **AI-DWG** | Design system, tokens, component inventory → workspace generation (`design-system.md`, `frontend-standards.md`) |
| **AI-GCE** | Accessibility baseline → derives `accessibility-compliance` enforcement rule |
| **AI-DLC v1** | (runtime) sends usability/accessibility feedback back to AI-UXD for design iteration |

The handoff is automatic — successor packages detect `uxd-state.md` and read what they need. The `ux-consistency-agent` (`UXC__`) installed at Stage 16 lets you re-validate the UXP's traceability and consistency on demand at any time.

---

## Related Documents

| Document | Location |
|----------|----------|
| How the UX Design Lifecycle Works | `knowledge_docs/HOW_UX_DESIGN_LIFECYCLE_WORKS.md` |
| How to Design Architecture | `knowledge_docs/HOW_TO_DESIGN_ARCHITECTURE.md` |
| How to Manage Product Backlog | `knowledge_docs/HOW_TO_MANAGE_PRODUCT_BACKLOG.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |
| How Depth Levels Work | `knowledge_docs/HOW_DEPTH_LEVELS_WORK.md` |

*Knowledge Document | Created: 2026-06-13 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

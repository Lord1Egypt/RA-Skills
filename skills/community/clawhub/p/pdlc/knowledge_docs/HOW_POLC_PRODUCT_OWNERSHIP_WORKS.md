# How AI-POLC Product Ownership Works

**Purpose:** Explains how AI-POLC transforms business intent into a governed, prioritized Product Backlog Package (PBP) — covering vision, epic decomposition, value-based prioritization, and the continuous backlog/acceptance exchange with AI-DLC v1 during delivery.

---

## What AI-POLC Does

AI-POLC is the single source of truth for WHAT gets built, in WHAT order, and WHY. It sits between strategic planning (AI-PILC) and implementation (AI-DLC v1), turning business goals into a structured, prioritized backlog that developers consume.

```
PIP (from AI-PILC) + AP (from AI-ADLC)
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  AI-POLC LIFECYCLE                                                    │
│                                                                      │
│  VISION → DISCOVERY → DECOMPOSITION → PRIORITIZATION → RELEASE      │
│                                                                      │
│  Produces: Product Backlog Package (PBP)                             │
│  Feeds: AI-DWG (workspace enrichment) + AI-DLC v1 (implementation)      │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
PRODUCT BACKLOG PACKAGE (PBP)
├── Product Vision & Goals
├── PO Charter & Authority (RACI)
├── Epic Map (goal → epic → story)
├── Prioritized Backlog (value-ranked)
├── Release Plan (MVP/MMP slicing)
├── Definition of Ready / Done
├── Product Risk Register
└── polc-state.md (marker)
```

---

## Identity and Scope

**Identity spine:** AI-POLC turns business intent into a prioritized, value-justified product backlog, and is the single source of truth for *what gets built, in what order, and why*.

**Inclusion rule:** If it answers "what/why/order" → AI-POLC owns it. If it answers "how/when-built/is-it-compliant" → it belongs to a sibling package (AI-ADLC, AI-DLC v1, AI-GCE).

---

## The Two-Tier Activation Model

### Tier 1 — Always Active (the gap-filling delta)

Active regardless of chain context. Covers what AI-DLC v1's Inception phase does NOT:

| Capability | What It Produces |
|-----------|-----------------|
| Product Vision & Goals | Measurable business objectives the backlog serves |
| PO Charter & Authority | Decision boundaries, RACI, escalation paths |
| Product Discovery & Roadmap | Now/Next/Later strategic planning |
| Epic Decomposition | Goal → Epic mapping with acceptance criteria |
| Value-Based Prioritization | WSJF, MoSCoW, or value-effort scoring with rationale |
| Release & Increment Slicing | MVP/MMP scope definition + delivery groupings |
| Definition of Ready / Done | Quality gates flowing to AI-DWG and AI-GCE |
| Product Risk & Assumptions | Product-level risk register (not project-level — that's AI-PILC) |
| Traceability | Intent → Epic → Story → Release linkage |

### Tier 2 — User-Activated (full PO discipline)

For standalone use or teams wanting comprehensive product ownership:

| Capability | What It Adds |
|-----------|-------------|
| Stakeholder value mapping | Deep stakeholder-to-feature alignment |
| Outcome metrics & OKR tracking | Measure whether features deliver intended outcomes |
| Feedback loop governance | Structure for incorporating AI-DLC v1 runtime feedback |
| Sprint-level refinement governance | Backlog grooming standards and ceremonies |
| Technical debt as backlog items | Surfaces architecture debt as prioritized work |

---

## Key Interactions

### AI-UXD → AI-POLC (Producer → Consumer)

AI-UXD produces personas and user journeys. AI-POLC consumes them to:
- Ground epics in real user needs (not abstract requirements)
- Validate prioritization against user journey pain points
- Ensure backlog covers all persona needs

### AI-POLC → AI-DWG (Enrichment)

AI-DWG reads the PBP to enrich workspace generation:
- `DEFINITION_OF_DONE.md` derives from AI-POLC's DoD
- Story structure informs project instructions
- Release structure informs milestone tracking

### AI-POLC ⇄ AI-DLC v1 (Continuous Exchange)

During delivery, AI-POLC and AI-DLC v1 exchange continuously:
- **POLC → DLC:** Stories with acceptance criteria, priority order, DoR compliance
- **DLC → POLC:** Implementation feedback (stories that need splitting, discovered complexity, technical debt)

This is the only bidirectional flow in the family — both packages read from and write to each other throughout delivery.

---

## Prioritization Framework

AI-POLC supports multiple prioritization methods (PO chooses):

| Method | Best For | Scoring |
|--------|----------|---------|
| **WSJF** (Weighted Shortest Job First) | Lean/SAFe environments | (Business Value + Time Criticality + Risk Reduction) / Job Size |
| **MoSCoW** | Fixed-scope projects | Must / Should / Could / Won't categorization |
| **Value-Effort Matrix** | Simple, visual prioritization | Value (1-5) vs. Effort (1-5) quadrant placement |
| **Custom** | Organization-specific framework | Configurable criteria and weights |

**Key rule:** Every prioritization decision includes recorded rationale. "Why is this #1 and that #5?" is always answerable.

---

## The Backlog Quality Gate: Definition of Ready

Before a story enters the "ready for development" state:

| Criterion | What's Checked |
|-----------|---------------|
| Acceptance criteria defined | Clear, testable conditions for "done" |
| Dependencies identified | What else must exist/be available |
| Value articulated | WHY this story matters (traced to goal/epic) |
| Size estimated | Story points or T-shirt size |
| Priority assigned | Position in the backlog with rationale |
| Risks noted | Known risks or assumptions |

Stories that don't pass DoR are sent back to refinement — they don't enter AI-DLC v1 consumption.

---

## State and Continuity

`polc-state.md` tracks:
- Product Vision status (defined/draft)
- Epic map coverage (how many goals have decomposed epics)
- Backlog depth (stories elaborated vs. placeholder)
- Current release slice
- Active tier (1 or 2)
- Prioritization method in use
- Last refinement date

---

## Output: The Product Backlog Package (PBP)

```
{output-folder}/
├── polc-state.md                      ← Marker file
├── product-vision.md                  ← Vision, goals, success metrics
├── po-charter.md                      ← Authority, RACI, decision rights
├── product-roadmap.md                 ← Now/Next/Later strategic view
├── epic-map.md                        ← Goal → Epic decomposition
├── prioritized-backlog.md             ← Ranked stories with rationale
├── release-plan.md                    ← MVP/MMP slicing + increments
├── definition-of-ready.md             ← Quality gate for stories
├── definition-of-done.md              ← Quality gate for completion
├── product-risks.md                   ← Product-level risk register
└── management_framework/
    ├── Decision_Register.md
    └── Assumptions_Log.md
```

---

## Related Documents

| Document | Location |
|----------|----------|
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |
| How Depth Levels Work | `knowledge_docs/HOW_DEPTH_LEVELS_WORK.md` |
| How to Initiate a Project | `knowledge_docs/HOW_TO_INITIATE_A_PROJECT.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

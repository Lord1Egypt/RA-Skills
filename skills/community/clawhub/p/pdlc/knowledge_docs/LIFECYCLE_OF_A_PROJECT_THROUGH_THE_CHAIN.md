# Lifecycle of a Project Through the Chain

**Purpose:** Traces how a single project flows through the entire AI-* Family chain over time — from raw idea to governed production system — showing what exists at each stage, what decisions accumulate, and how the project's governance posture matures.

---

## The Complete Project Lifecycle

```
WEEK 0        WEEK 1-2       WEEK 2-4        WEEK 4-5       WEEK 5+         ONGOING
──────        ────────       ────────        ────────       ──────         ────────
AI-ILC        AI-PILC        AI-POLC →       AI-DWG         AI-GCE         AI-DLC v1
(optional)    (initiate)     AI-UXD →        (generate)     + AI-TGE       (build)
                             AI-ADLC                        (govern)

Output:       Output:        Output:         Output:        Output:        Output:
Idea Brief    PIP            PBP + UXP + AP  Workspace      Governance     Working
                                                            Layer          Software
```

---

## Phase 1: Idea Evaluation (Week 0 — Optional)

**Package:** AI-ILC
**Project state:** An unvalidated idea.

| What Exists | What's Decided |
|------------|---------------|
| Raw idea in any format | Nothing yet — evaluation pending |

**What happens:**
- 6-stage evaluation (Capture → Shape → Evaluate → Scope → Approve → Route)
- Go/no-go decision made
- If approved: Idea Brief produced, routed to AI-PILC

**Project after this phase:**
- Has a validated problem statement
- Has evaluation scores (value, feasibility, risk)
- Has scope boundaries and routing decision
- State: `ilc-state.md` with decision record

---

## Phase 2: Project Initiation (Weeks 1-2)

**Package:** AI-PILC
**Project state:** An approved idea or raw requirement.

| What Exists | What's Decided |
|------------|---------------|
| Idea Brief (or raw requirements) | Problem is real, worth investing in |

**What happens:**
- 13-stage structured initiation (Inception → Assessment → Planning → Definition)
- Requirements captured and structured
- Feasibility assessed (5 dimensions)
- Stakeholders identified, risks registered
- Charter produced and approved

**Project after this phase:**
- Has: structured requirements, feasibility study, stakeholder register, risk register, scope statement, project charter, management framework (6 governance registers)
- Depth selected (cascades to all downstream)
- Project ID minted (family-wide correlation key)
- State: `pilc-state.md` (complete)
- **Governance posture:** Project-level governance initialized (registers exist, no code-level enforcement yet)

---

## Phase 3: Product, UX & Architecture Design (Weeks 2-4)

**Packages:** AI-POLC → AI-UXD → AI-ADLC (sequential)
**Project state:** A fully initiated project with requirements.

| What Exists | What's Decided |
|------------|---------------|
| Full PIP (requirements, charter, risks, constraints) | What to build, why, for whom, at what cost |

The Project layer runs sequentially — each package completes its primary output before the next starts, so each discipline builds on firm upstream decisions. Feedback loops (ADLC→POLC cost/risk, ADLC→UXD constraints, UXD→POLC persona refinement) allow iterative refinement without changing the forward sequence.

**What happens (AI-POLC — first):**
- Product vision and goals formalized
- Epics decomposed from goals
- Backlog prioritized with rationale
- Release plan defined (MVP/MMP)

**What happens (AI-UXD — second, reads PBP):**
- Personas and user journeys produced
- Information architecture designed
- Design system and tokens defined
- Accessibility baseline established

**What happens (AI-ADLC — third, reads PBP + UXP):**
- 13-stage progressive decomposition (Foundation → Decomposition → Decisions → Design → Assembly)
- System context (L1), containers (L2), components (L3) defined
- Technology decisions made (ADRs produced)
- API contracts, security model, data architecture designed
- Extensions activated if needed (DDD, Microservices, etc.)

**Project after this phase:**
- Has: Product Backlog Package (PBP), UX Design Package (UXP), Architecture Package (AP) with ADRs
- Major technical decisions locked (ADRs)
- States: `polc-state.md`, `uxd-state.md`, `adlc-state.md` (all complete)
- **Governance posture:** Architectural decisions exist, but no runtime enforcement yet

---

## Phase 4: Workspace Generation (Week 4-5)

**Package:** AI-DWG
**Project state:** Full architecture, UX, and backlog ready.

| What Exists | What's Decided |
|------------|---------------|
| AP + UXP + PBP | What the system is, how it's structured, what gets built first |

**What happens:**
- AI-DWG reads AP (+ optionally UXP, PBP)
- Generates full development workspace:
  - `.kiro/steering/` (19+ files from architecture decisions)
  - Folder structure matching container/component architecture
  - `PROJECT_INSTRUCTIONS.md`, `DEFINITION_OF_DONE.md`, `TEAM_AGREEMENTS.md`
  - CI/CD templates, `docker-compose.yml`, `CODEOWNERS`
  - Management framework

**Project after this phase:**
- Has: A ready-to-code workspace with steering, structure, and operational docs
- Architecture decisions are now STEERING (machine-readable constraints)
- Marker: `.kiro/steering/workspace-rules.md` exists
- **Governance posture:** Advisory governance (steering files guide AI sessions) but no automated enforcement yet

---

## Phase 5: Governance Activation (Week 5)

**Packages:** AI-GCE + AI-TGE
**Project state:** Workspace generated, team ready to build.

| What Exists | What's Decided |
|------------|---------------|
| Full workspace with steering | How to code, what patterns to follow |

**What happens (AI-GCE):**
- Reads all steering files + built-in baseline
- Derives governance rules (numbered, binary)
- Generates hooks (automated enforcement on IDE events)
- Generates agents (process governance)
- Sets initial tier (Tier 1 recommended)
- Produces compliance state tracking

**What happens (AI-TGE):**
- Reads AP + workspace
- Derives test requirements from architecture commitments
- Builds test register (what MUST be tested)
- Establishes test strategy (pyramid, coverage thresholds)

**Project after this phase:**
- Has: Active governance enforcement (hooks fire, rules checked)
- Has: Test register (accountability for what needs testing)
- Compliance score established (baseline for brownfield, 100% target for greenfield)
- **Governance posture:** Full automated enforcement at chosen tier

---

## Phase 6: Development (Ongoing)

**Package:** AI-DLC v1 (Amazon's AI-DLC v1, not ours)
**Project state:** Everything in place — build with full support.

| What Exists | What's Decided |
|------------|---------------|
| Steering + hooks + rules + test register + backlog | Everything — now execute |

**What happens:**
- AI-DLC v1 uses steering files (architecture constraints in every session)
- Hooks fire on code changes (naming, security, boundaries enforced)
- Stories from AI-POLC's PBP are consumed
- Tests written against AI-TGE's register (accountability tracked)
- AI-POLC ⇄ AI-DLC v1 exchange backlog/acceptance
- AI-TGE observes: tracks coverage, scores gaps
- AI-GCE audits periodically: compliance score trending

**Project over time:**
- Tier 1 → Tier 2 graduation (2-4 weeks of stable Tier 1)
- Tier 2 → Tier 3 graduation (production approaching)
- Test coverage increases (TGE gaps closed as stories implement)
- Compliance score trends upward

---

## The Maturity Curve

```
Governance    │
Maturity      │                                    ┌────── Production
              │                               ┌────┘       (Tier 3, full governance)
              │                          ┌────┘
              │                     ┌────┘   Tier 2 activated
              │                ┌────┘
              │           ┌────┘   Tier 1 activated
              │      ┌────┘
              │ ┌────┘   Workspace generated (steering active)
              │─┘
              │  Architecture designed (ADRs exist, no enforcement)
              │
              │  Initiated (project-level governance only)
              │
              └──────────────────────────────────────────── Time
              W0   W2      W4     W6      W8     W12    W16+
```

---

## Related Documents

| Document | Location |
|----------|----------|
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| Pattern: Graceful Standalone | `knowledge_docs/PATTERN_GRACEFUL_STANDALONE.md` |
| Pattern: Progressive Activation | `knowledge_docs/PATTERN_PROGRESSIVE_ACTIVATION.md` |
| When to Use Standalone vs Chain | `knowledge_docs/WHEN_TO_USE_STANDALONE_VS_CHAIN.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

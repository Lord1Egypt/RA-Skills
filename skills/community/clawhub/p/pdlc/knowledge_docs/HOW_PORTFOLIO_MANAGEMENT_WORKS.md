# How AI-PPM Portfolio Management Works

**Purpose:** Explains how AI-PPM's adaptive Portfolio-layer engine governs MANY projects at once — registering them from upstream initiation packages, scoring strategic alignment, ranking them against each other, making admit/pause/retire decisions, dispatching authorizations down to the Project layer via AI-FLO, and aggregating roll-up telemetry into portfolio-level health views.

---

## What AI-PPM Does

AI-PPM is a continuous portfolio governance engine. It does not run a single project — it governs the SET of projects as one investment portfolio. It answers the questions no single-project package can: "Which projects should we run? In what order? Is the portfolio healthy across the board? Should anything stop?"

```
MULTIPLE PIPs (from AI-PILC) + APPROVED IDEA BRIEFS (from AI-ILC)
        │  (same-layer, direct marker read)
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  AI-PPM PORTFOLIO ENGINE — 5 phases / 10 stages                      │
│                                                                      │
│  INTAKE → PRIORITIZATION → AUTHORIZATION → MONITORING → OPTIMIZATION │
│                                                                      │
│  Governs the SET of projects — comparative, aggregate, continuous   │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
PORTFOLIO REGISTER + CROSS-PROJECT PRIORITIZATION
+ GOVERNANCE DECISIONS + DISPATCH AUTHORIZATIONS
        │
        ▼ (cross-layer, ONLY via AI-FLO)
┌─────────────────────────────────────────────────────────────────────┐
│  PROJECT LAYER (AI-ADLC / AI-UXD / AI-POLC / AI-DWG / AI-DLC v1 / ...)  │
│                                                                      │
│  FLO carries dispatch DOWN · FLO carries roll-up telemetry UP        │
└─────────────────────────────────────────────────────────────────────┘
```

**Hard boundary:** AI-PPM governs the portfolio — it never executes a project. It aggregates downstream data; it never recomputes it. And it never talks to Project-layer packages directly — everything crossing the layer boundary goes through AI-FLO.

---

## Identity and Scope

**Identity spine:** AI-PPM governs the SET of projects — registering, ranking, authorizing, monitoring, and rebalancing the portfolio as a single governed entity. It answers: "Which projects should we run, in what order, and is the portfolio healthy?"

**Inclusion rule:** If a concern is about *one project's internals* (scope, architecture, backlog, compliance) → out of scope (it belongs to a sibling: AI-PILC / AI-ADLC / AI-POLC / AI-GCE / AI-TGE). If a concern is about *the portfolio as a whole* (which projects, what priority, overall health, capacity across projects) → AI-PPM owns it.

**Layer position:** AI-PPM sits at the top of the **Portfolio layer** (scope = MANY projects), alongside AI-ILC and AI-PILC. The Project layer (scope = ONE project) lives below it, on the far side of the AI-FLO routing edge.

---

## Two Sources In, Four Things Out

### Input (same-layer, read directly)

| Source | What It Provides | How It's Read |
|--------|------------------|---------------|
| **PIPs from AI-PILC** | Project Initiation Packages — one per initiated project | Direct marker read of `pilc-state.md` (same Portfolio layer) |
| **Approved Idea Briefs from AI-ILC** | Potential projects still in the funnel | Direct marker read of `ilc-state.md` (same Portfolio layer) |

Because AI-ILC, AI-PILC, and AI-PPM all live in the Portfolio layer, AI-PPM reads their output markers directly — no router needed.

### Output

| Artifact | What It Is |
|----------|------------|
| **Portfolio Register** | The single source of truth for "what are we running" — every project, its identity, and its state |
| **Cross-Project Prioritization** | Project-vs-project ranking via an explicit, auditable scoring model |
| **Governance Decisions** | Admit / Pause / Resume / Retire / Hold records, rationale-first |
| **Dispatch Authorizations** | Authorization signals AI-FLO carries down to activate Project-layer packages |

---

## The Five Phases / Ten Stages

AI-PPM organizes ten stages across five phases. Unlike lifecycle packages that run once and complete, the engine is event-driven — a session enters at whichever stage the trigger requires.

### Phase 1 — INTAKE (Stages 1–2)

| Stage | Name | What Happens |
|:-----:|------|--------------|
| 1 | Portfolio Detection & Initialization | Scan for an existing `ppm-state.md` (resume) or `portfolio-register.md`; detect upstream markers; set depth level; initialize state |
| 2 | Project Registration | Admit a new project from a PIP, Approved Idea Brief, or manual entry; create a Project Intake Card; add a Portfolio Register entry in state `Registered` |

### Phase 2 — PRIORITIZATION & ALIGNMENT (Stages 3–4)

| Stage | Name | What Happens |
|:-----:|------|--------------|
| 3 | Strategic Alignment | Map 3–7 organizational objectives × projects; score each project's alignment (1–5); surface low-alignment retirement candidates |
| 4 | Cross-Project Prioritization | Rank all active projects against each other (Value vs. Effort, Weighted Scoring, Pairwise, or Cost of Delay / WSJF); record rationale for any governance override; surface resource contention |

### Phase 3 — AUTHORIZATION & DISPATCH (Stages 5–6)

| Stage | Name | What Happens |
|:-----:|------|--------------|
| 5 | Portfolio Governance Gate | Make explicit Admit / Pause / Resume / Retire / Hold decisions, each with rationale, conditions, and a review date; produce a Governance Decision Record |
| 6 | Dispatch Authorization | For "Admit"/"Resume" projects, produce a Dispatch Authorization (project ID, scope, priority rank, constraints, required packages) for AI-FLO to carry across the layer boundary |

### Phase 4 — MONITORING & DASHBOARDS (Stages 7–8)

| Stage | Name | What Happens |
|:-----:|------|--------------|
| 7 | Roll-Up Ingestion | Read FLO-carried roll-up snapshots (by project ID); refresh Register entries with health signals; flag deteriorating projects; compute portfolio aggregates |
| 8 | Portfolio Health & Dashboards | Render aggregate views — RAG distribution, financial summary, resource heatmap, risk heat map, progress tracker, quality posture; identify governance triggers |

### Phase 5 — OPTIMIZATION (Stages 9–10)

| Stage | Name | What Happens |
|:-----:|------|--------------|
| 9 | Portfolio Rebalancing | When reality changes (new data, new project, crisis, breach), re-rank and produce a Rebalancing Proposal; route back to Stage 5 for any formal decisions |
| 10 | Project Retirement & Closure | Formally remove a project (Completed / Cancelled / Superseded / Merged); capture actual-vs-planned, benefits status, and portfolio lessons; release capacity |

---

## The Continuous Engine Model

AI-PPM does not "finish." Projects enter, move through governance, and exit over time. There is no "workflow complete" — only episodes. A session enters at the stage its trigger demands:

| Trigger Event | Enters At | Session Pattern |
|---------------|:---------:|-----------------|
| New PIP available (AI-PILC completes) | Stage 2 | Registration session → Stages 1–6 |
| New Idea Brief approved (AI-ILC completes) | Stage 2 | Registration session |
| FLO delivers a roll-up refresh | Stage 7 | Review session → Stages 7–8 |
| Scheduled portfolio review | Stage 7→8 | Review session |
| Health threshold breached | Stage 9 | Rebalancing session |
| Project completion signal | Stage 10 | Retirement session |
| User requests a portfolio action | Varies | Direct entry to the relevant stage |

The engine also adapts its **depth** to portfolio size: Minimal (≤3 projects), Standard (4–10), Comprehensive (10+, enterprise, heavy cross-project dependencies — full extensions).

---

## Layered Communication — Never Talk Down Directly

This is the rule that keeps the portfolio decoupled from project execution:

> **Cross-layer communication MUST go through AI-FLO. Same-layer communication is direct (marker read).**

| Communication | Mechanism | Why |
|---------------|-----------|-----|
| PPM reads PILC output | **Direct** | Both in the Portfolio layer — marker read of `pilc-state.md` |
| PPM reads ILC output | **Direct** | Both in the Portfolio layer — marker read of `ilc-state.md` |
| PPM dispatches to ADLC / POLC / UXD | **Via FLO** | Portfolio → Project boundary — FLO carries the authorization down |
| Project packages report to PPM | **Via FLO** | Project → Portfolio boundary — FLO carries roll-up telemetry up |

AI-PPM never reads a Project-layer state file (like `flo-state.md` or a downstream package marker) directly, and Project-layer packages never read `ppm-state.md` directly. The router is the only conduit across the boundary.

**Fallback (no AI-FLO installed):**
- Same-layer reads always work, unchanged.
- Cross-layer down: the Dispatch Authorization becomes a manual reference — the user starts the Project-layer packages themselves, pointing at the PIP.
- Cross-layer up: AI-PPM prompts the user for manual status updates (progress %, RAG, top blocker, budget) — minimal viable monitoring.

---

## Addressable Roll-Up by `projectId`

Every project carries a correlation key — a camelCase `projectId` (for example `PRJ-ACME-2026-001`) — that threads through the entire chain from AI-PILC onward. AI-PPM uses it as the addressable key for roll-up:

- FLO roll-up payloads arrive keyed by `projectId`.
- AI-PPM matches each payload to its Portfolio Register entry by that key.
- Health signals (progress, RAG, risks, budget, velocity, compliance) update the right row without ambiguity.

This is what makes aggregation reliable across a large portfolio — there is exactly one canonical key per project, and it is the same key the project was initiated under.

---

## Aggregate, Never Recompute

AI-PPM is deliberately thin on per-project analysis. It **aggregates** downstream data into portfolio views; it does not redo work a sibling package already did:

| Per-Project Concern | Owned By | AI-PPM's Role |
|---------------------|----------|---------------|
| Per-project value scoring | AI-POLC | Reads it; rolls it up |
| Per-project resource planning | AI-PILC | Reads it; aggregates demand |
| Per-project risk assessment | AI-PILC / AI-POLC | Reads it; surfaces concentration |
| Per-project compliance / test posture | AI-GCE / AI-TGE | Reads it; rolls into quality posture |

The portfolio scorecard ranks projects *against each other*; it never re-derives a single project's internal numbers. "We'll redo the analysis" is an anti-pattern — read the output, don't repeat it.

---

## Portfolio Scope — Off the Per-Project Governance Spine

AI-PPM is **portfolio-scope**, which has a concrete structural consequence: it does NOT write to any per-project `management_framework`. The per-project governance spine (Decision Register, Assumptions Log, etc.) belongs to project-touching packages. AI-PPM is explicitly excluded — it maintains its own portfolio-scope registers instead:

- Portfolio Register (the master list)
- Strategic Alignment Map
- Prioritization Scorecard
- Governance Decision Records
- Portfolio Health Dashboard

A project's internal records stay with that project; the portfolio's records stay with the portfolio. The two never bleed into each other.

---

## Seven Opt-In Extensions

The core ten stages cover most portfolios. Seven extensions add depth, activated by user request, portfolio size, or context detection — each is additive (it adds sub-steps to an existing stage, never replacing core behavior):

| ID | Extension | Typical Trigger |
|:--:|-----------|-----------------|
| E1 | Portfolio Balancing & Visualization | "balance" / portfolio mix / >10 projects |
| E2 | What-If Scenario Modeling | "what-if" / capacity constraints |
| E3 | Cross-Project Dependency Mapping | >5 projects / shared components |
| E4 | Portfolio-Level Capacity & Demand | shared teams / resource contention |
| E5 | Investment Themes / Strategic Buckets | formal investment categories |
| E6 | Financial Governance | budget / funding / enterprise context |
| E7 | Benefits Realization Aggregation | projects completing / ROI tracking |

Active extensions are recorded in `ppm-state.md` so they persist across sessions.

---

## State and Continuity

`ppm-state.md` is the marker that makes the portfolio resumable across sessions. It tracks:
- Portfolio register location and project count
- Depth level (Minimal / Standard / Comprehensive)
- Dispatched project IDs (what FLO has been asked to route)
- Last roll-up ingestion timestamp
- Active extensions
- Where the engine left off (so the next session resumes cleanly)

Because the engine is continuous, the marker never reaches a terminal "complete" — it reflects the living state of the portfolio.

---

## The Portfolio Governance Agent (`PGA__`)

AI-PPM ships a dedicated agent — the **portfolio-governance-agent**, triggered by `PGA__`. It runs a governance pass over the portfolio: refreshing roll-up data, recomputing aggregate health, surfacing threshold breaches, and recommending governance actions (rebalance, pause, retire) for the user to confirm. It operates within the layered-communication and human-in-the-loop rules — every consequential decision still requires explicit confirmation.

---

## Output Artifacts

| Artifact | Purpose | Produced In |
|----------|---------|-------------|
| `portfolio-register.md` | Master list of all projects + states | Stages 1–2 (continuously updated) |
| `strategic-alignment-map.md` | Objectives × projects scoring | Stage 3 |
| `prioritization-scorecard.md` | Comparative project ranking | Stage 4 |
| `governance-decision-record.md` | Admit/pause/retire decisions + rationale | Stage 5 |
| `dispatch-authorization.md` | FLO-carried authorization to the Project layer | Stage 6 |
| `portfolio-health-dashboard.md` | Aggregate health views | Stages 7–8 |
| `rebalancing-proposal.md` | Change proposal + impact | Stage 9 |
| `retirement-record.md` | Formal project closure + lessons | Stage 10 |
| `ppm-state.md` | Portfolio continuity marker | After every stage |

---

## Related Documents

| Document | Location |
|----------|----------|
| How Flow Orchestrator Works | `knowledge_docs/HOW_FLOW_ORCHESTRATOR_WORKS.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |
| How POLC Product Ownership Works | `knowledge_docs/HOW_POLC_PRODUCT_OWNERSHIP_WORKS.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |

*Knowledge Document | Created: 2026-06-13 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

# How to Manage a Portfolio of Projects

**Purpose:** Practical guide for using AI-PPM to govern MANY projects as one investment portfolio — registering projects, scoring strategic alignment, ranking them against each other, making admit/pause/retire decisions, dispatching authorizations down to execution, ingesting roll-up status, and keeping the whole portfolio healthy over time. This is the operational companion to the mechanics doc: it answers "I need to run a portfolio, how do I actually use this?"

---

## Who This Is For

Portfolio managers, PMO leads, and delivery directors who own *which projects run, in what order, and whether the set is healthy*. You're not executing any single project — you're governing the investment portfolio above them. You want a register that's the single source of truth, prioritization that's defensible instead of loudest-voice, and aggregate health views that tell you when to intervene. You're comfortable saying "no" and "not yet"; you want AI-PPM to structure the governance, enforce the discipline, and keep the portfolio current.

---

## When to Use AI-PPM vs. a Single-Project Package

AI-PPM governs the SET. If your concern is one project's internals, a sibling package owns it.

| Your Concern | Package That Owns It |
|--------------|----------------------|
| Which projects should we run, in what order? | **AI-PPM** |
| Is the portfolio healthy across the board? | **AI-PPM** |
| Should we pause or retire something? | **AI-PPM** |
| How is capacity split across all projects? | **AI-PPM** |
| One project's charter, budget, feasibility | AI-PILC |
| One project's architecture | AI-ADLC |
| One project's backlog and priorities | AI-POLC |
| One project's compliance / test posture | AI-GCE / AI-TGE |

The rule of thumb: *one project's internals* → a sibling package. *The portfolio as a whole* → AI-PPM. AI-PPM never executes a project and never re-derives a single project's internal numbers — it reads downstream output and rolls it up.

---

## Before You Start

**You need:**
- AI-PPM installed in your AI workspace (see `ai-ppm/setup/INSTALL.md`)
- Input — ANY of the following works:
  - PIPs from AI-PILC (ideal — one Project Initiation Package per initiated project, richest context)
  - Approved Idea Briefs from AI-ILC (potential projects still in the funnel)
  - A manual project list (name, objective, rough budget, timeline, sponsor — you can start from zero)

**You do NOT need:**
- AI-FLO installed — without it, dispatch and roll-up use a manual fallback (covered below)
- Strategic objectives already written (AI-PPM elicits them at Stage 3)
- A chosen prioritization model (you pick one at Stage 4)
- Every project initiated — you can register potential projects from Idea Briefs and govern the pipeline

Because AI-ILC, AI-PILC, and AI-PPM all live in the **Portfolio layer**, AI-PPM reads their output markers directly — no router needed. Only the boundary down to the Project layer requires AI-FLO.

---

## Starting Out: Standalone vs. Chain

AI-PPM adapts to what you already have. You tell it your situation at Stage 1 and it sets mode and depth accordingly.

| Start Mode | What You Say | What Happens |
|-----------|-------------|--------------|
| **Chain (PIPs present)** | "Govern my portfolio; I have PIPs from AI-PILC" | Reads `pilc-state.md` markers directly, extracts project ID, objective, budget, timeline, sponsor, risk — minimal questions |
| **Chain (Idea Briefs present)** | "Register the approved ideas into the portfolio" | Reads `ilc-state.md` markers, seeds potential-project entries from the briefs |
| **Standalone** | "Help me set up a portfolio for 6 projects" | Guided intake — you provide each project's basics conversationally |
| **Resume** | (auto-detected) | Finds existing `ppm-state.md` and `portfolio-register.md`, picks up where the last session left off |

**Marker file:** AI-PPM tracks the living portfolio in `ppm-state.md`, and every project carries a camelCase `projectId` as its correlation key — the same key it was initiated under in AI-PILC, threading through the entire chain. Example: `projectId: PRJ-ACME-2026-001`. The marker never reaches a terminal "complete" — the portfolio is a continuous, resumable entity. Close and resume any time.

---

## The Process (10 Stages, 5 Phases) — From the Operator's Seat

AI-PPM is a continuous, event-driven engine, not a once-through lifecycle. A session enters at whichever stage your trigger demands — you rarely run all ten in one sitting. Here's the full flow and what you do at each stage.

### Phase 1: INTAKE — "What are we running?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 1. Portfolio Detection & Initialization | Scans for existing `ppm-state.md`/`portfolio-register.md` (resume) or sets up a new portfolio; detects upstream markers; sets depth | Confirm new vs. resume, and the depth level |
| 2. Project Registration | Admits a project from a PIP, Approved Idea Brief, or manual entry; creates a Project Intake Card; adds a Register entry in state `Registered` | Confirm each registration is correct |

**Gate:** You confirm registration before prioritization begins.

### Phase 2: PRIORITIZATION & ALIGNMENT — "Which matter most?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 3. Strategic Alignment | Maps 3–7 organizational objectives × projects; scores each project's alignment (1–5); surfaces low-alignment retirement candidates | Provide/confirm objectives; sanity-check scores |
| 4. Cross-Project Prioritization | Ranks all active projects against each other using your chosen model; records rationale for any governance override; surfaces resource contention | Approve the ranking or override with recorded reason |

**Gate:** You approve the prioritized ranking before any authorization decisions.

### Phase 3: AUTHORIZATION & DISPATCH — "What proceeds, what waits, what stops?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 5. Portfolio Governance Gate | Makes explicit Admit / Pause / Resume / Retire / Hold decisions, each with rationale, conditions, and a review date; produces a Governance Decision Record | Confirm each decision — these are consequential |
| 6. Dispatch Authorization | For Admit/Resume projects, produces a Dispatch Authorization (project ID, scope, priority rank, constraints, required packages) for AI-FLO to carry across the layer boundary | Confirm scope and constraints |

**Gate:** Every governance decision requires your explicit confirmation. A portfolio with no rejections has no governance.

### Phase 4: MONITORING & DASHBOARDS — "Are we healthy?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 7. Roll-Up Ingestion | Reads FLO-carried roll-up snapshots (keyed by `projectId`); refreshes Register entries with health signals; flags deteriorating projects; computes aggregates | Review flagged anomalies |
| 8. Portfolio Health & Dashboards | Renders aggregate views — RAG distribution, financial summary, resource heatmap, risk heat map, progress tracker, quality posture; identifies governance triggers | Read the dashboards; decide whether to rebalance |

**No terminal gate** — this is the rhythm you re-enter on cadence.

### Phase 5: OPTIMIZATION — "What changes?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 9. Portfolio Rebalancing | When reality changes (new data, new project, crisis, breach), re-ranks and produces a Rebalancing Proposal; routes back to Stage 5 for any formal decisions | Approve rebalancing changes before they take effect |
| 10. Project Retirement & Closure | Formally removes a project (Completed / Cancelled / Superseded / Merged); captures actual-vs-planned, benefits status, and portfolio lessons; releases capacity | Confirm retirement is appropriate |

**The engine doesn't "finish."** Projects enter, move through governance, and exit over time. Each session ends by persisting `ppm-state.md`.

---

## Which Session Am I Running?

You don't march through all ten stages. You enter at the stage your trigger demands:

| Trigger | Enters At | Session Pattern |
|---------|:---------:|-----------------|
| New PIP available (AI-PILC completes) | Stage 2 | Registration → Stages 1–6 |
| New Idea Brief approved (AI-ILC completes) | Stage 2 | Registration |
| FLO delivers a roll-up refresh | Stage 7 | Review → Stages 7–8 |
| Scheduled portfolio review | Stage 7→8 | Review |
| Health threshold breached | Stage 9 | Rebalancing |
| Project completion signal | Stage 10 | Retirement |
| You request a portfolio action | Varies | Direct entry to the relevant stage |

---

## How Dispatch Reaches the Project Layer (via AI-FLO)

The portfolio sits in the Portfolio layer; execution happens in the Project layer below. The two are deliberately decoupled — **everything crossing that boundary goes through AI-FLO.** AI-PPM never starts AI-ADLC, AI-POLC, or AI-UXD directly.

```
AI-PPM  ──(Dispatch Authorization, keyed by projectId)──►  AI-FLO  ──►  Project layer
                                                                          (AI-ADLC / AI-UXD /
                                                                           AI-POLC / AI-DWG / ...)
```

When you Admit a project at Stage 5 and authorize it at Stage 6, AI-PPM writes a Dispatch Authorization — project ID, authorization scope, priority rank, constraints (budget ceiling, deadline, team allocation), and which Project-layer packages to activate. AI-FLO reads that authorization and carries it across the boundary to start execution. You authorize *what* runs; FLO handles *routing it there*.

---

## How Roll-Up Status Comes Back

Status flows the same path in reverse — up through AI-FLO, keyed by `projectId`:

```
Project layer  ──(roll-up telemetry: progress, RAG, risks, budget, velocity, compliance)──►  AI-FLO  ──►  AI-PPM
```

At Stage 7, AI-PPM ingests each FLO roll-up payload, matches it to the right Portfolio Register row by `projectId` (there is exactly one canonical key per project, so there's no ambiguity), and refreshes the health signals. Stage 8 then aggregates those signals into the portfolio dashboards. AI-PPM **aggregates, never recomputes** — it reads the per-project numbers downstream packages already produced and rolls them up; it never redoes a single project's internal analysis.

---

## The No-FLO Manual Fallback

AI-FLO is optional. Without it, the portfolio still works — the cross-layer edge just becomes manual:

| Communication | With AI-FLO | Without AI-FLO (Fallback) |
|---------------|-------------|---------------------------|
| Same-layer reads (PIPs, Idea Briefs) | Direct marker read | **Direct marker read — unchanged** |
| Dispatch down to Project layer | FLO carries the authorization | The Dispatch Authorization becomes a manual reference — **you start the Project-layer packages yourself, pointing them at the PIP** |
| Roll-up up from Project layer | FLO carries telemetry | AI-PPM **prompts you for manual status updates** per project — progress %, RAG, top blocker, budget — minimal viable monitoring |

Same-layer reads always work because AI-ILC, AI-PILC, and AI-PPM share the Portfolio layer. Only the Project-layer boundary needs FLO, and the fallback keeps you governing even without it.

---

## Choosing Your Prioritization Model

At Stage 4 you pick a model and AI-PPM applies it consistently — never improvising the order. This is project-vs-project ranking at portfolio scope (not the per-project epic ranking AI-POLC does).

| Model | Pick It When | How It Scores |
|-------|-------------|---------------|
| **Value vs. Effort** | Small portfolio, want a fast visual call | Two-axis quadrant placement |
| **Weighted Scoring** | Multiple criteria matter (strategic fit, urgency, risk, capacity) | Weighted composite across dimensions |
| **Pairwise Comparison** | Small portfolio, want forced ranking | Compare projects in pairs to force a rank |
| **Cost of Delay / WSJF** | Time-sensitivity dominates | Value of delay ÷ job size |

**The rule that matters:** any rank that differs from the pure score carries a recorded rationale as a governance override. Months later, "why is Project A above Project B?" is always answerable — that's what protects the portfolio from loudest-voice prioritization.

---

## Choosing Your Depth Level

AI-PPM auto-calibrates to portfolio size, but you can override anytime with "Change depth to X."

| Depth | Best For | What You Get |
|-------|----------|--------------|
| **Minimal** | ≤3 projects, simple priorities, low contention | Streamlined register + basic ranking; Health Summary + Progress Tracker |
| **Standard** | 4–10 projects, some contention, clear strategy | Full prioritization with governance gates + all core dashboards |
| **Comprehensive** | 10+ projects, enterprise, heavy cross-project dependencies | Full extensions, detailed financial governance, scenario modeling, extension dashboards |

---

## The Seven Opt-In Extensions — When to Turn Them On

The core ten stages cover most portfolios. Seven extensions add depth, each additive (it adds sub-steps to an existing stage, never replacing core behavior). AI-PPM scans for triggers at engine start and offers an opt-in; you confirm before it loads. Active extensions are recorded in `ppm-state.md` so they persist across sessions.

| ID | Extension | Turn It On When |
|:--:|-----------|-----------------|
| E1 | Portfolio Balancing & Visualization | You want a visual portfolio mix, or you're past ~10 projects |
| E2 | What-If Scenario Modeling | You're capacity-constrained and want to compare scenarios before deciding |
| E3 | Cross-Project Dependency Mapping | More than ~5 projects share components or sequencing dependencies |
| E4 | Portfolio-Level Capacity & Demand | Shared teams create resource contention across projects |
| E5 | Investment Themes / Strategic Buckets | You allocate budget by formal investment categories |
| E6 | Financial Governance | Budget/funding tracking matters, or you're in an enterprise context |
| E7 | Benefits Realization Aggregation | Projects are completing and you're tracking ROI / value realized |

The guiding principle mirrors depth: don't activate an extension because it might be nice. Activate when the portfolio's reality calls for it.

---

## The Portfolio Governance Agent (`PGA__`)

AI-PPM ships a dedicated agent — the **portfolio-governance-agent**, triggered by typing `PGA__`. It runs a governance pass over the whole portfolio in one shot: refreshing roll-up data, recomputing aggregate health, surfacing threshold breaches, and recommending governance actions (rebalance, pause, retire) for you to confirm. It's the fast path to "where does my portfolio stand right now?" without manually walking Stages 7–9.

It operates inside the same rules as the engine: layered communication (cross-layer still via FLO) and human-in-the-loop — every consequential decision still requires your explicit confirmation. The agent recommends; you decide. Install happens automatically during your first AI-PPM session (see `ai-ppm/setup/INSTALL.md` for the manual steps).

---

## What You Get (Portfolio-Scope Artifacts)

```
{your-output-folder}/
├── ppm-state.md                       ← Marker file (continuity; carries dispatched projectIds, depth, active extensions)
├── portfolio-register.md              ← Master list of every project + its state (single source of truth)
├── strategic-alignment-map.md         ← Objectives × projects scoring
├── prioritization-scorecard.md        ← Comparative project-vs-project ranking + rationale
├── governance-decision-record.md      ← Admit/pause/resume/retire/hold + rationale
├── dispatch-authorizations/           ← FLO-carried authorizations to the Project layer
│   └── {projectId}.md                 ← e.g. PRJ-ACME-2026-001.md
├── portfolio-health-dashboard.md      ← Aggregate views (RAG, financial, risk, resource, progress, quality)
├── rebalancing-proposal.md            ← Change proposal + impact (when reality shifts)
├── retirement-record.md               ← Formal project closure + portfolio lessons
└── project-intake-cards/              ← One registration card per project
    └── {projectId}.md
```

**Important:** AI-PPM is portfolio-scope. It does NOT write to any per-project `management_framework` — a project's internal records stay with that project, and the portfolio's records stay with the portfolio. The two never bleed into each other.

---

## Tips for Running a Healthy Portfolio

1. **The Register is the truth.** Treat `portfolio-register.md` as the single answer to "what are we running." If a project isn't on it with a state, it isn't governed. Keep it current — a stale register is worse than none.

2. **A portfolio with no rejections has no governance.** Admitting everything isn't a portfolio decision — it's an absence of one. Use Pause and Hold liberally; finite capacity means choosing *not* to do things.

3. **Always rank comparatively, never in isolation.** Every project competes for the same finite capacity. "Project A scores 78 vs. Project B at 62" is a portfolio decision; "Project A looks good" is not.

4. **Record the override, not just the rank.** When you put a project above its raw score, log why. That rationale is what makes reprioritization defensible when a sponsor challenges the order.

5. **Don't redo downstream analysis.** AI-PPM reads per-project value, risk, and resource numbers from the packages that own them and rolls them up. "We'll redo the analysis" is an anti-pattern — read the output, don't repeat it.

6. **Run it on a cadence, not ad-hoc.** Portfolio management is rhythmic. A light biweekly sync (Stages 7–8) plus a monthly health review keeps small problems from compounding. Use `PGA__` for the quick pass.

7. **Surface contention before it's a crisis.** When two top-ranked projects need the same team, say so at Stage 4 — "admitting X means Y slips three months." Naming the trade-off early beats discovering it mid-delivery.

---

## What Happens Next

Once you authorize projects, the portfolio's decisions reach execution and status flows back:

| Direction | What Flows | How |
|-----------|-----------|-----|
| **Down to Project layer** | Dispatch Authorizations (scope, priority, constraints, required packages) | Via AI-FLO (or manual fallback — you start the packages) |
| **Up from Project layer** | Roll-up telemetry (progress, RAG, risks, budget, velocity, compliance) | Via AI-FLO (or manual status prompts), keyed by `projectId` |

From there the engine keeps cycling — register new projects, review health on cadence, rebalance when reality shifts, retire what's done. The portfolio is never "finished"; it's a living investment you keep healthy.

---

## Related Documents

| Document | Location |
|----------|----------|
| How AI-PPM Portfolio Management Works | `knowledge_docs/HOW_PORTFOLIO_MANAGEMENT_WORKS.md` |
| How Flow Orchestrator Works | `knowledge_docs/HOW_FLOW_ORCHESTRATOR_WORKS.md` |
| How to Initiate a Project | `knowledge_docs/HOW_TO_INITIATE_A_PROJECT.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |

*Knowledge Document | Created: 2026-06-13 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

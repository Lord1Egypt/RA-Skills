# AI-PPM — User Guide

**Package:** AI-PPM (AI-Driven Project Portfolio Management)
**Version:** 1.0.0
**Audience:** Portfolio Managers, PMO Directors, CIOs, Program Managers, Investment Decision-Makers

---

## What is AI-PPM?

AI-PPM is an injectable portfolio governance engine that manages multiple projects as a single governed portfolio. It registers, prioritizes, authorizes, monitors, and rebalances projects — answering the questions no single-project package can: *"Which projects should we run? In what order? Is the portfolio healthy? Should anything stop?"*

**In one sentence:** AI-PPM governs the SET of projects — not individual execution — ensuring the right work gets funded, prioritized, and monitored across your entire portfolio.

---

## When to Use AI-PPM

| Scenario | AI-PPM helps you... |
|----------|---------------------|
| Managing 3+ concurrent projects | Register, prioritize, and track them as a portfolio |
| Need to decide which projects to fund | Score and rank across consistent criteria |
| Portfolio becoming unhealthy (delays, conflicts) | Monitor health and propose rebalancing |
| New project request arrives | Evaluate fit against existing portfolio constraints |
| Projects completing or failing | Formally retire with lessons captured |

---

## How It Works (5 Minutes)

1. **Install** — Copy package files into your IDE's steering folder (see `setup/INSTALL.md`)
2. **Start a session** — Say: *"I want to manage my project portfolio using AI-PPM"*
3. **Register projects** — Provide PIPs, Idea Briefs, or describe your projects
4. **Authorize and dispatch** — AI-PPM scores, ranks, and helps you make go/no-go decisions
5. **Monitor continuously** — Re-enter for health checks, rebalancing, and retirement

---

## Input Sources

AI-PPM consumes outputs from other AI-* packages:

| Input | Source | What It Provides |
|-------|--------|-----------------|
| Project Initiation Packages (PIPs) | AI-PILC | Project scope, resources, risks, business case |
| Approved Idea Briefs | AI-ILC | New project candidates with evaluation scores |
| Project status telemetry | AI-FLO (roll-up) | Health signals from project-layer packages |

AI-PPM also works standalone — you can register projects manually by describing them conversationally.

---

## The Workflow (5 Phases, 10 Stages)

### Phase 1: Intake (Stages 1–2)

Register projects into the portfolio.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 1 — Portfolio Configuration | Sets up governance model, scoring criteria, capacity constraints | Confirm portfolio parameters |
| 2 — Project Registration | Registers each project with identity, state, and key data | Confirm project entries are correct |

### Phase 2: Prioritization (Stages 3–4)

Align to strategy and rank projects against each other.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 3 — Strategic Alignment | Maps objectives × projects; scores alignment | Confirm alignment scores |
| 4 — Cross-Project Prioritization | Ranks projects using scoring model (project-vs-project) | Approve priority order |

### Phase 3: Authorization (Stages 5–6)

Decide which projects proceed and dispatch them.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 5 — Governance Decisions | Produces admit/pause/retire decisions with rationale | Make go/no-go/pause decisions |
| 6 — Dispatch Authorization | Authorizes execution; FLO carries dispatch to Project layer | Confirm dispatch |

### Phase 4: Monitoring (Stages 7–8)

Track portfolio health on cadence.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 7 — Health Monitoring | Aggregates project status into portfolio-level views | Review health dashboard |
| 8 — Exception Management | Flags projects in trouble; proposes interventions | Approve/reject interventions |

### Phase 5: Optimization (Stages 9–10)

Rebalance and retire as reality changes.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 9 — Rebalancing | Proposes priority/resource changes when conditions shift | Approve rebalancing proposals |
| 10 — Retirement | Formally closes completed/cancelled projects with lessons | Confirm retirement decisions |

---

## Key Design Principle: Continuous Engine

Unlike lifecycle packages that complete (PILC, ADLC), AI-PPM operates **continuously**:
- Projects enter and exit over time
- Health is monitored on cadence
- Priorities shift as reality changes
- There is no "workflow complete" — only episodes (register, review, rebalance, retire)

---

## Extensions (Opt-In)

Extensions add specialized portfolio capabilities. They activate via trigger phrases:

| Say... | Extension | What It Adds |
|--------|-----------|--------------|
| "balance" / >10 projects | Portfolio Balancing & Visualization | Visual balance maps, bubble charts |
| "what-if" / capacity constraints | What-If Scenario Modeling | Simulate priority/resource changes |
| "dependencies" / >5 projects | Cross-Project Dependency Mapping | Dependency graphs, conflict detection |
| "capacity" / shared teams | Portfolio-Level Capacity & Demand | Resource demand vs. supply views |
| "strategic buckets" | Investment Themes | Category-based allocation governance |
| "budget" / "funding" | Financial Governance | Budget tracking, funding gates |
| "benefits" | Benefits Realization Aggregation | Portfolio-level value tracking |

---

## Layered Communication Rule

AI-PPM follows strict communication boundaries:

| Communication | Method |
|---------------|--------|
| PPM → Project-layer packages | **Through AI-FLO only** (dispatch authorization) |
| PPM ← Project-layer packages | **Through AI-FLO only** (roll-up telemetry) |
| PPM → AI-PILC / AI-ILC | **Direct** (same Portfolio layer — marker read) |

AI-PPM never directly commands project-layer packages. FLO carries decisions down and status up.

---

## The Relationship with AI-FLO

```
AI-PPM ──(dispatch authorization)──► AI-FLO ──► Project Layer
AI-PPM ◄──(roll-up telemetry)─────── AI-FLO ◄── Project Layer
```

| Direction | What Flows | When |
|-----------|-----------|------|
| PPM → FLO | Dispatch authorizations, pause/resume commands | After governance decisions |
| FLO → PPM | Project health signals, milestone completions, blockers | On cadence or exception |

**Without FLO:** AI-PPM still works — but cross-layer communication becomes manual. You report project status into PPM yourself.

---

## Adaptive Depth

AI-PPM auto-calibrates based on portfolio complexity:

| Depth | When Applied | What Changes |
|-------|-------------|--------------|
| **Minimal** | 2-5 projects, single team, clear priorities | Lightweight register + simple scoring |
| **Standard** | 5-15 projects, multiple teams, competing resources | Full scoring model + health monitoring |
| **Comprehensive** | 15+ projects, enterprise, formal investment governance | All extensions suggested, formal financial governance |

Override anytime: *"Change depth to Comprehensive"*

---

## Session Continuity

AI-PPM saves progress in `ppm-state.md`. You can:
- Close your session at any time
- Resume later — AI-PPM reads state and picks up where you left off
- Re-enter for any episode (register new project, health check, rebalance)
- Portfolio state persists across all sessions

---

## What You Get (Output Artifacts)

| Artifact | Purpose |
|----------|---------|
| `ppm-state.md` | State tracking + portfolio marker |
| `portfolio-register.md` | All projects with identity, state, priority |
| `strategic-alignment-map.md` | Objectives × projects scoring |
| `prioritization-scorecard.md` | Project-vs-project ranking |
| `governance-decision-records/` | Admit/pause/retire decisions with rationale |
| `dispatch-authorizations/` | Execution authorizations (for FLO) |
| `portfolio-health-dashboard.md` | Aggregate health views |
| `rebalancing-proposals/` | Change proposals when conditions shift |
| `retirement-records/` | Formal closure with lessons |

---

## Quick Start Examples

**New portfolio setup:**
```
Using AI-PPM, I want to manage my project portfolio.
I have 8 active projects — let me register them.
```

**Adding a new project to existing portfolio:**
```
Using AI-PPM, register a new project from this PIP.
Evaluate its fit against the current portfolio.
```

**Health check:**
```
Using AI-PPM, run a portfolio health check.
Two projects are reporting delays.
```

**Rebalancing:**
```
Using AI-PPM, we lost a key team member.
Rebalance the portfolio given reduced capacity.
```

---

## Tips for Best Results

1. **Think portfolio, not project** — Every PPM decision is about the SET. Never optimize one project at the expense of the portfolio.
2. **Feed PIPs when possible** — Richer project data produces better prioritization and alignment scores.
3. **Monitor on cadence** — Don't wait for crises. Regular health checks catch problems early.
4. **Use FLO for cross-layer communication** — Don't bypass the communication model; it exists for auditability.
5. **Retire formally** — Every project that ends (success or failure) deserves a formal closure with lessons.
6. **Let extensions activate naturally** — As your portfolio grows, AI-PPM suggests relevant extensions.

---

## What AI-PPM Is NOT

- NOT single-project management (that's AI-PILC for initiation, AI-DLC v1 for execution)
- NOT architecture design (that's AI-ADLC)
- NOT product backlog management (that's AI-POLC)
- NOT routing/orchestration (that's AI-FLO — PPM decides, FLO carries)
- NOT compliance enforcement (that's AI-GCE)

AI-PPM is the **Portfolio Governor** — it answers *"Which projects should we run, in what order, and is the portfolio healthy?"*

---

## Platform Support

AI-PPM works on: Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, and GitHub Copilot — plus any AI-assisted IDE that supports steering/rules files via the Universal Setup.

See `setup/INSTALL.md` for detailed platform instructions.

---

*AI-PPM v1.0.0 | Part of [AIFLC](../README.md) — the AI-* PDLC Family*

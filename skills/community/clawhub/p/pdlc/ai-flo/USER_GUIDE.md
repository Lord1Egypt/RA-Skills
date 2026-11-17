# AI-FLO — User Guide

**Package:** AI-FLO (AI-Driven Flow Orchestrator)
**Version:** 1.0.0
**Audience:** Portfolio Managers, Program Managers, PMOs, Tech Leads managing multi-package workflows

---

## What is AI-FLO?

AI-FLO is the nervous system of the AI-* Family. It routes decisions down from the Portfolio layer, relays status up from the Project layer, and maintains awareness of where every project is in the chain at all times. It turns the AI-* Family from a collection of independent packages into a coordinated pipeline.

**In one sentence:** AI-FLO routes work between packages and layers — tracking positions, dispatching projects, detecting conflicts, and ensuring nothing falls between the cracks.

---

## When to Use AI-FLO

| Scenario | AI-FLO helps you... |
|----------|---------------------|
| Multiple packages active for a project | Track which package each project is in and what comes next |
| AI-PPM approved a project for dispatch | Carry authorization down to the right Project-layer packages |
| Need portfolio-level status | Roll up project telemetry from Project layer to PPM |
| Sequential packages running (POLC → UXD → ADLC) | Track position, handoff each completion to the next package |
| Routing conflicts between packages | Detect and surface conflicts — never silently resolve |

---

## How It Works (5 Minutes)

1. **Install** — Copy package files into your IDE's steering folder (see `setup/INSTALL.md`)
2. **Configure** — Say: *"Using AI-FLO, configure routing for my project"*
3. **AI-FLO reads markers** — Detects state files from other packages (`pilc-state.md`, `adlc-state.md`, etc.)
4. **Routes automatically** — When a package completes, FLO determines the next destination
5. **Monitor** — FLO tracks position, detects conflicts, and relays status

---

## Understanding AI-FLO's Nature

AI-FLO is NOT a lifecycle — it's a **routing engine**. Key differences:

| Lifecycle Packages | AI-FLO |
|-------------------|--------|
| Have phases and stages you walk through | Has configuration, then activates on state changes |
| Complete when all stages done | Never "completes" — runs as long as projects flow |
| You interact with them directly | Operates in the background, surfaces when routing decisions are needed |
| Produce documents | Produces routing decisions, dispatch records, conflict alerts |

---

## The Three Phases

### Phase 1: Configure (Stages 1–3)

Set up the routing topology and rules.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 1 — Workspace Topology | Detects workspace layout (co-located, hub-and-spoke, distributed) | Confirm topology mode |
| 2 — Routing Table Setup | Loads canonical default routes + any project-specific profiles | Confirm/customize route profiles |
| 3 — Signal Registration | Registers which state markers to watch and their transitions | Confirm signal sources |

### Phase 2: Route (Stages 4–7)

The active routing engine — dispatches, coordinates, resolves.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 4 — Downward Dispatch | Carries PPM authorization to Project-layer packages | Confirm dispatch targets |
| 5 — Sequential Routing | Routes each handoff through the POLC→UXD→ADLC sequence; validates readiness at DWG convergence | Monitor progress |
| 6 — Convergence Readiness | Detects when AI-ADLC completes (confirming AP+PBP+UXP all present); signals DWG can proceed | Approve readiness |
| 7 — Conflict Resolution | Flags bidirectional signal collisions; holds for human decision | Resolve conflicts |

### Phase 3: Monitor (Stages 8–10)

Ongoing awareness and reporting.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 8 — Position Tracking | Maintains real-time awareness of every project's chain position | Review positions |
| 9 — Upward Roll-Up | Compiles project status for portfolio-level consumption (PPM) | Confirm telemetry accuracy |
| 10 — Exception Handling | Manages blocks, cancellations, rework, skips, escalations | Decide on exceptions |

---

## Routing Logic

### Canonical Default Chain

```
AI-ILC (optional) → AI-PILC → AI-PPM (authorize)
                                    │
                              AI-FLO (dispatch)
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
                 AI-ADLC         AI-UXD          AI-POLC
                    │               │               │
                    └───────────────┼───────────────┘
                                    ▼
                                 AI-DWG → AI-GCE → AI-DLC v1
```

### Sequential Routing & Convergence

FLO coordinates the sequential Project-layer flow:
- **Sequential chain:** PILC → POLC → UXD → ADLC → DWG (each package completes before the next starts)
- **Convergence at DWG:** When AI-ADLC completes, all three outputs (AP + PBP + UXP) are present and DWG can proceed

FLO tracks position by monitoring state markers at each handoff point in the sequence.

---

## Conflict Detection

AI-FLO detects 6 types of conflicts and **always surfaces them** — never silently resolves:

| Conflict Type | What It Means | Resolution |
|---------------|---------------|------------|
| Signal Collision | Two packages emit conflicting signals simultaneously | Human picks which takes priority |
| Contention | Multiple projects competing for same resource/slot | Portfolio manager decides |
| Profile Contradiction | Route profile says X but runtime condition says Y | Operator resolves |
| Stale Signal | A marker hasn't updated in expected timeframe | Investigate or force-through |
| Deadlock | Circular dependency between packages | Timeout + deterministic fallback |
| Authority Conflict | PPM says X but operator override says Y | Explicit authority resolution |

**Anti-deadlock guarantee:** Every hold has a timeout with deterministic fallback. Operator can always force-through.

---

## Workspace Topology Modes

AI-FLO adapts to how your packages are deployed:

| Topology | Layout | How FLO Communicates |
|----------|--------|---------------------|
| **Co-located** | All packages in one workspace (1:1) | Direct marker file reading |
| **Hub-and-spoke** | Central workspace + satellite project workspaces (1:N) | Marker detection across linked folders |
| **Fully distributed** | Each package in its own workspace (1:N remote) | State file synchronization |

---

## Interaction Model

AI-FLO uses a hybrid interaction model:

| Mode | Purpose | When Active |
|------|---------|-------------|
| **Dashboard** | Read flow state, positions, routes | Anytime — query the current state |
| **Command** | Execute routing actions (dispatch, override, force-through) | When operator needs to act |
| **Alert** | Proactive notification of conflicts, readiness, stale signals | When FLO detects exceptions |

---

## Flow Exceptions

When routing doesn't follow the happy path:

| Exception | What Happens | Your Options |
|-----------|-------------|--------------|
| **Block** | Package can't proceed — dependency unmet | Wait, resolve blocker, or skip |
| **Cancel** | Project removed from flow mid-route | Formal cancellation with audit record |
| **Rework** | Package output rejected — needs revision | Route back to prior package |
| **Skip** | Package not needed for this project | Skip with logged rationale |
| **Escalate** | Decision beyond operator authority | Surface to portfolio governance |

---

## The Relationship with AI-PPM

```
AI-PPM ──(dispatch authorization)──► AI-FLO ──► Project Layer
AI-PPM ◄──(roll-up telemetry)─────── AI-FLO ◄── Project Layer
```

**Rule:** AI-PPM decides. AI-FLO carries. FLO does not make portfolio decisions — it executes routing that PPM (or the operator) has authorized.

**Without AI-PPM:** FLO still works — it routes based on canonical defaults and operator decisions. PPM adds portfolio-level authorization and priority.

---

## Session Continuity

AI-FLO saves state in `flo-state.md`:
- Current position of every tracked project
- Active routing profiles
- Pending conflicts (flag-and-hold)
- Routing history (append-only log)
- Topology configuration

FLO state persists indefinitely — it's a continuous engine, not a session-based workflow.

---

## What You Get (Output Artifacts)

| Artifact | Purpose |
|----------|---------|
| `flo-state.md` | Flow state + chain marker |
| `routing-table.md` | Active routes + project profiles + toggles |
| `routing-log.md` | Append-only audit trail of all routing events |
| `dispatch-records/` | One record per dispatched project |
| `readiness-checks/` | Convergence evaluations (are all predecessor outputs present before DWG?) |
| `conflict-alerts/` | Flag-and-hold reports for human resolution |
| `roll-up-reports/` | Periodic status summaries for PPM |

---

## Quick Start Examples

**Configure for a new project:**
```
Using AI-FLO, configure routing for my project.
It has a PIP ready and needs to run through POLC, UXD, and ADLC sequentially.
```

**Check project position:**
```
Using AI-FLO, where is {project-name} in the chain right now?
```

**Dispatch after PPM approval:**
```
Using AI-FLO, dispatch {project-name} to the Project layer.
PPM authorized it — route to POLC (first in Project-layer sequence).
```

**Resolve a conflict:**
```
Using AI-FLO, I see a conflict alert. Show me the details and let me resolve it.
```

---

## Tips for Best Results

1. **Let FLO read markers** — Don't manually update routing; let packages emit their state and FLO detect it.
2. **Resolve conflicts promptly** — Flag-and-hold means FLO is waiting for your decision. Don't let it stale.
3. **Use route overrides sparingly** — Canonical defaults exist for a reason. Overrides are logged and auditable.
4. **Check readiness before convergence** — DWG needs AP + PBP + UXP. In the sequential flow, AI-ADLC completing guarantees all three are present.
5. **Review the routing log** — It's your audit trail. Every routing decision is recorded with rationale.
6. **FLO is advisory** — It records decisions for human action; it does not auto-execute package sessions.

---

## What AI-FLO Is NOT

- NOT a lifecycle (no "stages" you walk through — it's an engine)
- NOT a portfolio manager (that's AI-PPM — FLO carries, PPM decides)
- NOT a project manager (that's AI-PILC)
- NOT a requirement for the family to work (packages work standalone; FLO adds coordination)
- NOT autonomous — it advises and records; humans decide and act

AI-FLO is the **Router** — it answers *"Where should this work go next, and is everything flowing correctly?"*

---

## Platform Support

AI-FLO works on: Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, and GitHub Copilot — plus any AI-assisted IDE that supports steering/rules files via the Universal Setup.

See `setup/INSTALL.md` for detailed platform instructions.

---

*AI-FLO v1.0.0 | Part of [AIFLC](../README.md) — the AI-* PDLC Family*

# AI-FLO — AI-Driven Flow Orchestrator

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)

**Version:** 1.0.0
**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**License:** Apache 2.0 with Attribution

---

## What Is AI-FLO?

AI-FLO is the nervous system of the AI-* PDLC Family. It routes decisions down from the Portfolio layer, relays status up from the Project layer, and maintains awareness of where every project is in the chain at all times.

**In one sentence:** AI-FLO turns the AI-* PDLC Family from a collection of independent packages into a coordinated pipeline — tracking positions, dispatching projects, detecting conflicts, and ensuring nothing falls between the cracks.

---

## Family Position

AI-FLO is part of **AIFLC** (AI Full Life Cycle). It sits on the **edge** between the Portfolio layer and Project layer in the AI-* PDLC Family:

```
╔════════════════ PORTFOLIO LAYER · scope = MANY projects ════════════════╗

   (optional)
    AI-ILC  ⇢  AI-PILC  ⇢  AI-PPM
    Decide it   Initiate it   Govern it (portfolio of N projects)

╚═════════════════════════════════╤═══════════════════════════════════════╝
                                   │
                                AI-FLO   Route it — package-to-package
                                   │     flow on the edge between layers
╔════════════════ PROJECT LAYER · scope = ONE project ════════════════════╗

    AI-POLC ──► AI-UXD ──► AI-ADLC ──► AI-DWG ──► AI-DLC v1 (build) ¹
    Own it      Design UX   Design it   Prepare it       ▲
                                                         │
                        AI-POLC ⇄ AI-DLC v1 (back-and-forth)┘
                AI-DLC v1 ⇢ AI-UXD+AI-POLC (feedback)

    AI-GCE  +  AI-TGE  ──── alongside AI-DLC v1 (continuous quality) ────►
    Guard it   Test it

╚═════════════════════════════════════════════════════════════════════════╝
  ¹ AI-DLC v1 = Amazon's open-source build lifecycle (not ours; we feed it).
```

| Layer | Package | Type | Input | Output |
|-------|---------|------|-------|--------|
| Portfolio | **AI-ILC** ² | Interactive workflow (lifecycle) | Raw idea | Approved Idea Brief / Feature Brief |
| Portfolio | **AI-PILC** | Interactive workflow (lifecycle) | Raw requirement | Project Initiation Package (PIP) |
| Portfolio | **AI-PPM** ³ | Adaptive portfolio engine | Multiple PIPs + Approved Idea Briefs | Portfolio register + cross-project prioritization & governance |
| Edge | **AI-FLO** ³ | Router / orchestration engine | Any package output marker | Routing decision + handoff to next package/layer |
| Project | **AI-POLC** ³ | Interactive workflow (lifecycle) | PIP | Product Backlog Package (PBP) |
| Project | **AI-UXD** ³ | Interactive workflow (lifecycle) | PIP + PBP | UX Design Package (UXP): personas/journeys, IA, user flows, design system + tokens, accessibility baseline |
| Project | **AI-ADLC** | Interactive workflow (lifecycle) | PIP + PBP + UXP | Architecture Package (AP) |
| Project | **AI-DWG** | One-time generator | AP + PBP + UXP | Ready-to-code development workspace (DW) |
| Project | **AI-GCE** | Adaptive governance engine | DW (AI-DWG output) | Compliance enforcement layer |
| Project | **AI-TGE** | Test governance engine | DW / build artifacts | Test governance & quality layer |
| Project | **AI-DLC v1** ¹ | Interactive workflow (lifecycle) | DW + GCE + User Stories (from AI-POLC) | Working Software |

> ¹ **AI-DLC v1** ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) is NOT our product. Our chain produces the workspace AI-DLC v1 consumes.
> ² **AI-ILC** is an **optional pre-stage** (the funnel before the funnel). The chain still works without it for users who start at AI-PILC. `⇢` denotes the optional link.
> ³ All packages in this table are **built**. AI-PPM (portfolio engine), AI-FLO (router), AI-POLC (product ownership lifecycle), and AI-UXD (UX design lifecycle) were the last four — completed June 2026. Within the Project layer, **AI-POLC, AI-UXD, and AI-ADLC run sequentially** (POLC→UXD→ADLC) — each feeds the next, culminating at AI-DWG which receives all three outputs (AP + PBP + UXP). **AI-GCE and AI-TGE run alongside AI-DLC v1** as continuous quality engines; **AI-POLC ⇄ AI-DLC v1** exchange backlog/acceptance throughout delivery; and **AI-DLC v1 runtime feedback flows back to both AI-UXD and AI-POLC**. Feedback loops (ADLC→POLC cost/risk, ADLC→UXD constraints) provide iterative refinement without changing the forward sequence.

> **AI-DFE** ([Data Fabric Engine](../ai-dfe/)) is a family-scoped **companion** — it gathers data from all packages and distributes structured JSON for dashboards and status roll-ups. It runs alongside the chain rather than as a linear step, so it is not shown as a chain row above.

---

## Features

- **3 phases, 10 stages** — Configure → Route → Monitor
- **Cross-layer dispatch** — carry AI-PPM's authorization down to Project-layer packages
- **Upward roll-up relay** — compile project status and surface to portfolio level
- **Sequential routing** — carry routing decisions through the Project-layer sequence (POLC → UXD → ADLC → DWG) and validate readiness at convergence (AP+PBP+UXP → DWG)
- **Flow state tracking** — know where every project is at all times (`flo-state.md`)
- **Routing table** — static canonical default + per-project profiles + runtime toggles
- **Conflict detection (flag-and-hold)** — detect bidirectional signal collisions; never silently resolve
- **6 conflict types** — signal collision, contention, profile contradiction, stale signal, deadlock, authority conflict
- **Anti-deadlock guarantee** — every hold has a timeout with deterministic fallback; operator can always force-through
- **Flow exceptions** — block, cancel, rework, skip, escalate with full audit trail
- **Route override + toggle** — operator can deviate from canonical chain at any time (logged)
- **3 workspace topology modes** — co-located (1:1), hub-and-spoke (1:N), fully distributed (1:N remote)
- **Hybrid interaction model** — Dashboard (read state) + Command (execute actions) + Alert (proactive notifications)
- **Routing log** — append-only audit trail of every routing event
- **Governance spine contribution** — FLO-D- decisions, FLO-I- issues (routine hops stay in log only)
- **FIA__ governance agent** — on-demand integrity validation (17 checks across 5 categories)
- **Graceful degradation** — without FLO, same-layer packages still work via direct marker detection
- **Advisory model** — records decisions for human action; does not auto-execute package sessions (v1.0)

---

## Activation

**Explicit key:** type `_FLO_` in any prompt to activate AI-FLO unambiguously — even when other AI-* packages share the workspace. The status key `_ACTIVE_` reports which package is currently active. A package switch never happens without your explicit key or confirmation, and any switch is announced on the first line of the response (`Active package: AI-FLO`). See [`../TRIGGER_KEYS_REFERENCE.md`](../TRIGGER_KEYS_REFERENCE.md) for the full family key table.

---

## Installation

See `setup/INSTALL.md` for full multi-platform installation instructions.

**Quick start (Kiro):**
1. Copy `ai-flo-rules/` and `ai-flo-rule-details/` into the uniform home `.aiflc/pdlc/`
2. Copy `session-orchestrator.md` into `.kiro/steering/` (the only always-loaded file; it `Read`s the core on demand)
3. Start a session — AI-FLO activates when you request routing operations

---

## Usage

1. Open a workspace where AI-* packages are installed
2. Start a chat and say:
   ```
   Using AI-FLO, what should I do next?
   ```
3. AI-FLO reads the current workflow state markers and tells you which package to activate next (and flags pending handoffs or conflicts)
4. It routes decisions and relays status between packages — it never produces package artifacts itself

## File Structure

```
ai-flo/
├── README.md                          ← This file
├── LICENSE                            ← Apache 2.0 + Attribution
├── PLAN.md                            ← Design rationale + decisions
├── ai-flo-rules/
│   └── core-engine.md                 ← Master orchestration (THE spec)
├── ai-flo-rule-details/
│   ├── common/                        ← Cross-cutting (5 files)
│   ├── configure/                     ← Phase 1 stages (3 files)
│   ├── route/                         ← Phase 2 stages (4 files)
│   ├── monitor/                       ← Phase 3 stages (3 files)
│   └── templates/                     ← Output templates (9 files)
│       └── agents/                    ← Governance agent (2 files)
└── setup/
    └── INSTALL.md                     ← Platform setup guide
```

---

## Tenets

1. **Advisory, not autonomous** — records decisions for human action; never auto-executes
2. **Carry, don't decide** — PPM decides; operator overrides; FLO routes
3. **Log everything** — every hop, override, toggle, conflict is recorded
4. **Flag, never suppress** — conflicts always surface; FLO never silently picks a winner
5. **Canonical default, governed deviation** — family chain is default; deviations are explicit and auditable
6. **Topology-aware** — adapts to co-located, hub-and-spoke, or fully-distributed workspaces
7. **Additive, not blocking** — without FLO, the family still works; FLO adds coordination, never becomes a single point of failure

---

## Output (What You Get)

When AI-FLO is active:

```
{workspace}/flow-orchestration/
├── flo-state.md                    (marker + flow state)
├── routing-table.md                (active routes + profiles)
├── routing-log.md                  (append-only audit trail)
├── dispatch-records/               (one per dispatched project)
├── readiness-checks/               (fan-in evaluations)
├── conflict-alerts/                (flag-and-hold reports)
└── roll-up-reports/                (periodic status for PPM)
```

---

## Author

**Mohammad Maheri** — Process designer specializing in injectable AI workflow packages.

AI-FLO was designed to complete the AI-* Family's architecture: turning a collection of independent packages into a coordinated system where work flows between layers as naturally as data flows through a pipeline.

---

*v1.0.0 | 2026-06-12*

---

## License

**Apache License 2.0 with Attribution Addendum**

- **Free to use:** Personal, commercial, educational, and organizational use — all permitted
- **Modify and distribute:** Create derivative works, redistribute, sublicense — all permitted
- **Attribution required:** Any distributed product substantially based on this work must include:

> *"Built on AIFLC by Mohammad Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)"*

- **No warranty:** Provided "AS IS" without warranties of any kind

See `LICENSE` and `NOTICE` in this directory for full terms.

**Copyright:** © 2026 Mohammad Maheri

---

*Part of [AIFLC](../README.md) — the AI-* PDLC Family*

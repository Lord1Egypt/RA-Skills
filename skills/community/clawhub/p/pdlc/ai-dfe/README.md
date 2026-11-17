# AI-DFE — AI-Driven Data Fabric

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)

**Version:** 1.0.0
**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**License:** Apache 2.0 with Attribution

---

## What Is AI-DFE?

AI-DFE is the data layer of the AI-* PDLC Family. It gathers the scattered markdown outputs every package produces, shapes them into structured JSON per consumer needs, and distributes them to one read-point — so dashboards, extensions, and reports get clean, machine-readable data without ever knowing where the raw files live.

**In one sentence:** AI-DFE turns the family's scattered, human-readable outputs into a single governed, machine-readable data surface — gather, shape, distribute.

**Tagline:** *Fabric it.*

---

## Family Position

AI-DFE is part of **AIFLC** (AI Full Life Cycle) and the **AI-* PDLC Family**. Like AI-FLO, it lives in **every family** as a continuous adaptive engine — but where FLO routes decisions, DFE fabrics data. It owns one folder, `pdlc-ws/data/`, and is its sole writer.

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

> **Note on AI-DFE's table row:** AI-DFE is a continuous data-fabric engine that operates *alongside* the whole family (like AI-FLO, it is not a chain link). Its formal row is added to the canonical family table during family-governance integration; the diagram and table above are reproduced verbatim from the family canonical (`FAMILY_TABLE_MAP.md`) and are never improvised.

---

## Features

- **3 phases** — Configure (discover) → Operate (gather, shape, distribute, monitor) → Govern (validate, freshness, history, cleanup)
- **Two-layer pipeline** — sources → per-package JSON (Layer 1) → demand-shaped consumer output (Layer 2)
- **Single-writer territory** — DFE is the sole owner and sole writer of `pdlc-ws/data/`
- **Discover-once, monitor-continuously** — reads each package's interface once, then only checks timestamps
- **Consumer decoupling** — consumers declare a DEMAND; they never touch raw source files
- **REGISTRY.json discovery** — every consumer reads ONE fixed path to find all its data
- **Schema-first** — every data file validates against a JSON Schema (per-package + DFE-owned aggregations)
- **Historical snapshots** — millisecond-timestamped history with retention + cleanup
- **Graceful degradation** — a missing source becomes a `null` field, never an error
- **Multi-family ready** — single-active master mode for operating several families' data from one seat (deferred until a 2nd family exists)
- **`DAT__` operations trigger** — gather/shape/distribute/discover/aggregate/cleanup/master
- **`DHC__` data-fabric health check** — bootstrap readiness check ("can DFE operate in this workspace?"); the data-layer analogue of AI-FLO's `FHC__`. Run it first. Read-only.
- **`DFA__` data-fabric integrity agent** — standalone integrity pass, 18 checks across 5 categories (schema / registry / manifest / freshness / territory); the data-layer analogue of AI-FLO's `FIA__`. Reports, never writes.
- **Hook-free governance** — convention + sole-writer ownership + agent, no IDE hooks

---

## Activation

**Explicit key:** type `_DFE_` in any prompt to activate AI-DFE unambiguously — even when other AI-* packages share the workspace. The status key `_ACTIVE_` reports which package is currently active. A package switch never happens without your explicit key or confirmation, and any switch is announced on the first line of the response (`Active package: AI-DFE`). See [`../TRIGGER_KEYS_REFERENCE.md`](../TRIGGER_KEYS_REFERENCE.md) for the full family key table.

**Operations:** `DAT__` runs data operations (e.g. `DAT__ all`, `DAT__ pdlc/pilc`, `DAT__ status`). **Quality:** `DFA__` runs the data-fabric quality agent (report-only).

---

## Installation

See `setup/INSTALL.md` for full multi-platform installation instructions.

**Quick start (Kiro):**
1. Copy `ai-dfe-rules/` and `ai-dfe-rule-details/` into the uniform home `.aiflc/pdlc/`
2. Copy `session-orchestrator.md` into `.kiro/steering/` (the only always-loaded file; it `Read`s the core on demand)
3. The installer bootstraps an empty `pdlc-ws/data/`; run `DAT__ all` to populate it.

---

## Usage

1. Open a workspace where AI-* packages have produced output
2. Start a chat and run the data trigger:
   ```
   DAT__ all
   ```
3. AI-DFE gathers data from every installed package, shapes it per consumer demands, and distributes structured JSON to `{family}-ws/data/`
4. Use `DAT__ full` for a complete-set pass with a readiness report, `DAT__ status` for a staleness check, or `DFA__` for a report-only quality assessment
5. Consumers (e.g. the dashboard) read the data via `REGISTRY.json`

## File Structure

```
ai-dfe/
├── README.md                          ← This file
├── LICENSE  ·  NOTICE                 ← Apache 2.0 + Attribution
├── PLAN.md  ·  CONCEPTUAL_MAP.md      ← rationale + navigation
├── USER_GUIDE.md  ·  WHITEPAPER.md    ← walkthrough + design narrative
├── ai-dfe-rules/
│   └── core-engine.md                 ← Master orchestration (THE spec) + § Gate Contract
├── ai-dfe-rule-details/
│   ├── common/                        ← process-overview, session-continuity
│   ├── configure/                     ← Phase 1: family / package / demand discovery
│   ├── operate/                       ← Phase 2: gather, shape, distribute, monitor, cross-project, cross-family
│   ├── govern/                        ← Phase 3: validation, freshness, history, cleanup
│   ├── data-schema/                   ← DFE's own data interface (reports on itself)
│   └── templates/                     ← dfe-state, DATA_INTERFACES, SOURCE_MAP, demand, data-samples/, agents/
└── setup/
    └── INSTALL.md                     ← multi-platform install
```

---

## Tenets

1. **Generated, not hand-edited** — everything in `data/` is tool-produced.
2. **Single-writer** — only DFE writes to `data/`; any consumer may read.
3. **Schema-first** — no data file without a schema.
4. **Consumers are decoupled** — they declare a DEMAND and read the registry; they never reach into source files.
5. **Family-scoped** — each family owns its own `data/`; cross-family exchange reads the neighbour's data, never mixes.
6. **Graceful degradation** — incomplete is allowed; broken is not.

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

> **Note:** AI-DLC v1 (Development Life Cycle) is NOT part of the AI-* Family — it is a separate AWS product ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) licensed under MIT-0.

---

## Author

**Maheri** — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)

AI-DFE is part of **AIFLC** (AI Full Life Cycle), a family of injectable AI workflow packages. Built on AIFLC by Mohammad Maheri.

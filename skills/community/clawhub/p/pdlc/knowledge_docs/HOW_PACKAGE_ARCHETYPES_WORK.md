# How Package Archetypes Work

**Purpose:** Explains the three structural archetypes that every AI-* Family package belongs to — interactive workflow, one-time generator, and adaptive engine — and the rules that decide which archetype a package is. Answers the recurring question: "Why is this package an *engine* and not a *workflow*?"

---

## The Three Archetypes

Every package in the family is exactly one of three archetypes. The archetype determines the package's core file, its execution shape, and how long it stays relevant.

```
   INTERACTIVE WORKFLOW          ONE-TIME GENERATOR            ADAPTIVE ENGINE
   ┌──────────────────┐          ┌──────────────────┐         ┌──────────────────┐
   │ one input        │          │ inputs           │         │ N inputs (grows) │
   │   │              │          │   │              │         │   │              │
   │   ▼ ordered      │          │   ▼ one shot     │         │   ▼ observe +    │
   │  stages + gates  │          │  artifact        │         │     adapt        │
   │   │              │          │   │              │         │   │   ▲          │
   │   ▼              │          │   ▼              │         │   ▼   │ (loops as │
   │ one deliverable  │          │ generated output │         │ standing layer   │
   │ (then DONE)      │          │ (then DONE)      │         │  state changes)  │
   └──────────────────┘          └──────────────────┘         └──────────────────┘
   core-workflow.md              core-generator.md            core-engine.md
```

| Archetype | Core file | Execution shape | Lifespan |
|-----------|-----------|-----------------|----------|
| Interactive workflow (lifecycle) | `core-workflow.md` | Multi-stage interactive interview with gates | Runs once → produces one deliverable → done |
| One-time generator | `core-generator.md` | One-shot generation with modes | Runs once → emits artifacts → done |
| Adaptive engine | `core-engine.md` | Hybrid strategy + continuous observation | Standing layer → re-runs as state changes |

---

## How to Classify a Package

Ask these questions in order. The first "yes" wins.

1. **Does it watch a workspace or portfolio state and re-act whenever that state changes?**
   → **Adaptive engine.** (AI-PPM, AI-GCE, AI-TGE)

2. **Does it produce a build artifact in a single pass, with no ongoing relationship after?**
   → **One-time generator.** (AI-DWG)

3. **Does it take one input and march it through ordered, interactive stages to a single defined deliverable?**
   → **Interactive workflow.** (AI-ILC, AI-PILC, AI-ADLC, AI-UXD, AI-POLC)

The discriminator is **time and input cardinality**, not subject matter. A package is an engine because of *how* it runs (continuously, over a changing set of inputs), not because of *what domain* it covers.

---

## Family Classification

| Layer | Package | Archetype | Why |
|-------|---------|-----------|-----|
| Portfolio | AI-ILC | Interactive workflow | One raw idea → ordered evaluation → one Idea Brief |
| Portfolio | AI-PILC | Interactive workflow | One raw requirement → ordered intake → one PIP |
| Portfolio | **AI-PPM** | **Adaptive engine** | Watches N PIPs/briefs; re-prioritises as the portfolio changes |
| Edge | AI-FLO | Router / orchestration engine | Observes package output markers; routes continuously |
| Project | AI-ADLC | Interactive workflow | Requirements → ordered design stages → one AP |
| Project | AI-UXD | Interactive workflow | PIP/AP → ordered design stages → one UXP |
| Project | AI-POLC | Interactive workflow | PIP/AP → ordered stages → one PBP |
| Project | AI-DWG | One-time generator | AP + PBP + UXP → workspace in one pass |
| Project | AI-GCE | Adaptive engine | Watches the workspace; enforces and re-derives rules |
| Project | AI-TGE | Adaptive engine | Watches build artifacts; maintains test governance |

> The canonical Type values live in `FAMILY_TABLE_MAP.md`. This table summarises the archetype reasoning; it does not redefine the official Type strings.

---

## Worked Example: Why AI-PPM Is an Engine, Not a Workflow

AI-PPM (portfolio management) is the classic "why isn't this a workflow?" case. Three reasons:

**1. No linear lifecycle to walk through.** Workflow packages take a single input and move it through ordered, interactive stages to one deliverable — raw requirement → PIP, requirements → AP. There is a start, a sequence of question/answer gates, and a defined end. AI-PPM has none of that. It does not take one thing and finish it.

**2. Continuous operation over a changing input set.** AI-PPM's input is *multiple* PIPs plus approved Idea Briefs — N projects that arrive, change, and grow over time. It scans for `pilc-state.md` markers with `Status: Complete`, aggregates them, and re-prioritises. That is the *observation* half of the engine model: it watches portfolio state and reacts, rather than running a one-time interview. A workflow ends; an engine keeps running as the portfolio evolves.

**3. Output is standing governance logic, not a one-shot deliverable.** AI-PPM produces a portfolio register plus cross-project prioritisation and governance — decisions that must be recomputed whenever a new PIP lands or priorities shift. That is the *adaptive strategy* half. The same reasoning makes AI-GCE (compliance enforcement) and AI-TGE (test governance) engines: standing, reactive layers, not start-to-finish interviews.

So portfolio management is an ongoing, cross-project, state-driven governance function. There is no "finished" portfolio the way there is a finished PIP — which is exactly why AI-PPM is an engine.

---

## Why the Distinction Matters

| Consequence | Workflow | Generator | Engine |
|-------------|----------|-----------|--------|
| Core file | `core-workflow.md` | `core-generator.md` | `core-engine.md` |
| Runs per project | Once to completion | Once | Repeatedly, on demand or on change |
| Session model | One session, resumable via state file | One session | Re-invoked whenever inputs change |
| User interaction | Heavy (staged interview) | Moderate (mode selection) | Light (strategy setup, then observation) |
| "Done" state | Yes — deliverable produced | Yes — artifact emitted | No — standing layer |

Getting the archetype right keeps the core file shape consistent across the family: a builder opening any `core-engine.md` expects strategy + observation, and any `core-workflow.md` expects ordered stages with gates.

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong |
|--------------|----------------|
| Labelling AI-PPM a "workflow" because it's in the Portfolio layer | Layer ≠ archetype. Layer is *where* in the chain; archetype is *how* it runs. |
| Giving an engine a `core-workflow.md` | Engines observe and adapt — they have no single ordered run to completion. |
| Treating AI-DWG as an engine because it's complex | Complexity ≠ archetype. AI-DWG runs once and is done — that's a generator. |
| Adding staged gates to an engine | Engines react to state changes; forcing a linear gate sequence breaks the observation model. |

---

## Related Documents

| Document | Location |
|----------|----------|
| How Package Installation Works (core-file types) | `knowledge_docs/HOW_PACKAGE_INSTALLATION_WORKS.md` |
| How Portfolio Management Works | `knowledge_docs/HOW_PORTFOLIO_MANAGEMENT_WORKS.md` |
| How the Flow Orchestrator Works | `knowledge_docs/HOW_FLOW_ORCHESTRATOR_WORKS.md` |
| How the Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| Family Structure | `FAMILY_STRUCTURE.md` |
| Family Table Map (canonical Type values) | `FAMILY_TABLE_MAP.md` |

*Knowledge Document | Created: 2026-06-15 | Updated: 2026-06-15 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

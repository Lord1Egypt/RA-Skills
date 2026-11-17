# Why the Lifecycle Sequence Matters

**Purpose:** Explains why AIFLC's AI-* PDLC Family runs its packages in a specific order — *decide → initiate → own → design experience → design structure → generate workspace* — and what breaks when that order is rearranged. The sequence is not arbitrary: each package consumes the package before it, so the order is a dependency chain, not a preference.

---

## The Practice

The AI-* PDLC Family executes as a forward sequence:

```
Portfolio layer:   AI-ILC  →  AI-PILC        (decide it → initiate it)
                                  │
                          (portfolio admission + routing)
                                  │
Project layer:     AI-POLC → AI-UXD → AI-ADLC → AI-DWG → build
                   own it    design UX  design it  prepare it
```

Each arrow is a real handoff: the producer's **output package** becomes the consumer's **input**. AI-POLC produces the Product Backlog Package; AI-UXD consumes it and produces the UX Design Package; AI-ADLC consumes both and produces the Architecture Package; AI-DWG consumes all three to generate the development workspace. The order encodes the dependency: you cannot design an experience for features you have not yet scoped, and you cannot architect a system whose experience you have not yet defined.

This document focuses on the *single-project golden path*. Two family packages sit outside this line by design and are covered separately: **AI-PPM** is a continuous portfolio engine that reasons across many projects (it is not a station on one project's track), and **AI-FLO** is the router that *performs* each handoff (it is the mechanism, not a step). The companions **AI-GCE** and **AI-TGE** run alongside delivery rather than in the forward line.

---

## What Happens When You Reorder It

1. **Designing before scoping (UX before product ownership).** If experience design runs before the backlog is built and prioritized, designers produce flows, screens, and a design system for features that may never be funded or may be cut. The result is polished UX for the wrong scope — expensive rework once priorities land, and a design system shaped around features that don't survive triage.

2. **Architecting before experience (architecture before UX).** If the architecture is locked before interaction needs are understood, technical choices get made blind to real-time, offline, accessibility, or interaction-density requirements. The experience is then boxed into whatever the architecture already allows. Teams discover late that the chosen pattern can't support the journey the product needs — and the journey gets degraded to fit the architecture, rather than the architecture serving the journey.

3. **Generating the workspace before the inputs exist.** AI-DWG composes a development workspace from the architecture, backlog, and UX packages. Run it early and it has nothing concrete to compose from — it either stalls or fabricates structure that the later real packages then contradict.

4. **Skipping initiation (jumping straight to product ownership).** Without a Project Initiation Package, the backlog has no charter, no business case, no scope boundary, and no success criteria to prioritize against. Prioritization becomes opinion rather than alignment, and the project carries an unowned set of assumptions into delivery.

5. **Running everything in parallel with no contracts.** Concurrency feels faster, but without each package's output existing as a stable input for the next, the handoffs are not real — packages feed each other artifacts that don't exist yet. Integration becomes reconciliation, traceability breaks, and the "fast" parallel path spends its savings on rework.

---

## Real-World Impact

| Dimension | Impact of a wrong sequence |
|-----------|----------------------------|
| Traceability | Out-of-order work breaks the line from product intent → journey → screen → component → architecture. You lose the ability to answer "why does this exist?" for any given artifact. |
| Rework | Each skipped dependency surfaces later as contradiction. Reworking a design system or architecture mid-delivery costs multiples of doing it in order. |
| Handoff quality | The sequence guarantees each package's input is a finished, reviewed package. Reordering replaces clean handoffs with partial, in-flight assumptions. |
| Determinism | An AI-executable chain needs each step's input to already exist. Reordering forces packages to guess at missing inputs, making outputs non-repeatable. |
| Cost & timeline | Wrong-order discovery is late discovery. The further downstream a missing dependency is found, the larger the blast radius and the schedule hit. |

---

## How the AI-* PDLC Family Enforces the Order

| Mechanism | How it holds the sequence |
|-----------|---------------------------|
| **Input/output contracts** | Each package declares what it consumes and produces. AI-UXD consumes PIP + PBP; AI-ADLC consumes PIP + PBP + UXP; AI-DWG consumes AP + PBP + UXP. A package can only start when its declared inputs exist. |
| **Marker/state files** | Each package writes a state marker its successor detects. The successor knows its predecessor finished — and refuses to assume an absent input silently. |
| **Gates before transition** | Each lifecycle package closes with a gate. The next package starts from a reviewed, approved package, not a half-finished draft. |
| **AI-FLO routing** | The router performs handoffs in dependency order and flags conflicts rather than dispatching a package whose inputs aren't ready. |
| **Peer-input composition (AI-DWG)** | Where a project legitimately lacks one input (brownfield, partial scope), AI-DWG accepts any non-empty subset and discloses the quality impact of the missing cluster — reordering is surfaced and approved, never silent. |

---

## Comparing the Realistic Orderings

Most of the chain is fixed by contracts — you cannot generate a workspace before there is something to put in it. The one place reasonable practitioners debate is the project-layer trio: product ownership, UX design, and architecture. Here is how the candidate orderings compare.

| Ordering | Logic | Quality read |
|----------|-------|--------------|
| **POLC → UXD → ADLC** (default) | Value & scope → experience → structure. Each output is the next input. | Strongest for product-led work. Clean contracts, full traceability, lowest rework. |
| UXD → POLC → ADLC | Design-discovery first, backlog second. | Risk of designing flows for unscoped features. User insight belongs upstream (in idea + initiation), so UX can safely follow scope. |
| POLC → ADLC → UXD | Architecture before experience. | Locks tech choices before interaction needs are known. Acceptable for backend/platform/API products with thin UI; weak for UX-heavy products. |
| All three in parallel → DWG | Run concurrently, converge at workspace generation. | Fastest on paper, but no clean handoff contract; integration/rework risk and non-deterministic feedback ordering. |

### Quality scorecard

| Dimension | POLC→UXD→ADLC (default) | Architecture-first | Fully parallel |
|-----------|:----------------------:|:------------------:|:--------------:|
| Traceability | High | Medium | Low |
| Rework risk (low is better) | Low | Medium | High |
| Handoff/contract cleanliness | High | Medium | Low |
| Determinism (AI-executable) | High | High | Low |
| Raw speed | Medium | Medium | High |
| Fit: UX-heavy product | High | Low | Medium |
| Fit: backend/platform product | Medium | High | Medium |

---

## The Counter-Argument (and Why It Mostly Fails)

**"Real teams work in parallel — the product manager, designer, and architect collaborate at the same time, so the chain should too."**

Human teams *do* collaborate concurrently, and the family supports that: the forward sequence carries **feedback loops** (architecture feeds cost/risk back to product ownership; architecture feeds constraints back to UX; runtime feedback flows back to both UX and product ownership). Iteration flows backward freely. What the sequence fixes is the *forward dependency* — the order in which each package's output becomes the next package's committed input. Collaboration is continuous; the contract order is not negotiable, because a package cannot consume a package that doesn't exist yet.

**"Our product is backend-heavy — architecture should come first."** Legitimate. The default is product-led; for a platform/API product with thin UI, `POLC → ADLC → UXD` is a defensible variant. The family doesn't forbid context-sensitive reordering — it optimizes for the common case and asks you to make the trade-off explicitly.

---

## Severity: High

Sequence errors are dependency errors, and dependency errors compound. A backlog built without initiation, a design built without a backlog, or an architecture built without a design each carries a missing-input debt that surfaces downstream as contradiction and rework. The order is cheap to honor and expensive to violate — which is exactly why the family enforces it through contracts, markers, gates, and routing rather than leaving it to discipline.

---

## Related Documents

| Document | Location |
|----------|----------|
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How Project Layer Collaboration Works | `knowledge_docs/HOW_PROJECT_LAYER_COLLABORATION_WORKS.md` |
| How the Flow Orchestrator Works | `knowledge_docs/HOW_FLOW_ORCHESTRATOR_WORKS.md` |
| Lifecycle of a Project Through the Chain | `knowledge_docs/LIFECYCLE_OF_A_PROJECT_THROUGH_THE_CHAIN.md` |
| Why Architecture Before Code Matters | `knowledge_docs/WHY_ARCHITECTURE_BEFORE_CODE_MATTERS.md` |
| Why Project Initiation Matters | `knowledge_docs/WHY_PROJECT_INITIATION_MATTERS.md` |
| When to Use Standalone vs Chain | `knowledge_docs/WHEN_TO_USE_STANDALONE_VS_CHAIN.md` |

*Knowledge Document | Created: 2026-06-22 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

# How AI-ILC Idea Lifecycle Works

**Purpose:** Explains how AI-ILC's 6-stage pipeline takes a raw idea through structured evaluation to a defensible go/no-go decision, then routes the approved output to the correct next package with zero context loss.

---

## What AI-ILC Does

AI-ILC is the optional entry point to the AI-* Family — the "funnel before the funnel." It takes raw ideas (from anyone, in any format) and applies structured evaluation before the organization commits resources to full project initiation.

```
RAW IDEA (any format)
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  AI-ILC PIPELINE (6 Stages)                                          │
│                                                                      │
│  CAPTURE → SHAPE → EVALUATE → SCOPE → APPROVE → ROUTE               │
│                                                                      │
│  Gate at every stage — human decides, AI advises                     │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼ (one of three outputs)
┌──────────────┐  ┌────────────────────┐  ┌─────────────────┐
│ Idea Brief   │  │ Change Request     │  │ Feature Brief   │
│ → AI-PILC    │  │ Brief → AI-PILC    │  │ → AI-DLC v1        │
│ (new project)│  │ (change to existing)│  │ (small feature) │
└──────────────┘  └────────────────────┘  └─────────────────┘
```

---

## The 6 Stages

### Stage 1: Capture

**What happens:** The raw idea is received and recorded in whatever form it arrives.

**Input acceptance:** Verbal description, one-liner, meeting notes, feature request, competitive observation, technical improvement proposal — any format, any length.

**Output:** Structured Idea Record with: source, raw statement, initial category, date captured.

**Gate:** "Is this idea captured accurately?" (validation, not evaluation)

### Stage 2: Shape

**What happens:** The raw idea is transformed into a structured format suitable for evaluation.

**AI produces:**
- Problem statement (what's wrong / what opportunity exists)
- Proposed solution (high-level, not detailed)
- Hypothesis ("We believe {action} will result in {outcome} for {audience}")
- Assumption inventory (what must be true for this to work)
- Initial categorization (new product / feature / improvement / technical debt)

**Gate:** "Does this shaped version accurately represent the idea?"

### Stage 3: Evaluate

**What happens:** The shaped idea is scored against 7 evaluation criteria using a consistent rubric.

**7 Evaluation Criteria:**
| # | Criterion | What It Measures |
|---|-----------|-----------------|
| 1 | Problem Severity | How painful is the problem being solved? |
| 2 | Market/User Demand | Is there evidence people want this? |
| 3 | Strategic Alignment | Does this fit organizational goals? |
| 4 | Technical Feasibility | Can we build this with available technology? |
| 5 | Effort Estimate | How much work (T-shirt: S/M/L/XL)? |
| 6 | Risk Profile | What could go wrong and how badly? |
| 7 | Competitive Position | Does this differentiate us? |

**Two-source scoring:**
- **Rubric-derived** (from evaluation criteria — project-specific weights)
- **Baseline minimums** (universal: e.g., "technical feasibility < 2/5 = automatic defer")

**Output:** Evaluation scorecard with per-criterion scores and composite rating.

**Gate:** "Do these scores reflect reality? Any criterion to revisit?"

### Stage 4: Scope

**What happens:** For ideas that pass evaluation, define the boundaries of what "implementing this" means.

**AI produces:**
- Scope boundaries (in/out)
- Dependency identification (what else must exist/change)
- Portfolio context check (conflicts with existing initiatives?)
- Value articulation (WHY this matters — stakeholder-ready language)
- Effort refinement (from T-shirt to rough timeline range)

**Gate:** "Is the scope realistic and well-bounded?"

### Stage 5: Approve (Decision Gate)

**What happens:** Final go/no-go decision with full evaluation context.

**Decision options:**
| Decision | Criteria | Output |
|----------|----------|--------|
| **Approve** | Scores pass thresholds, scope is feasible, resources available | Proceed to routing |
| **Defer** | Good idea but bad timing (resources, dependencies, market) | Logged with re-evaluation trigger |
| **Pivot** | Problem valid, solution needs rethinking | Return to Stage 2 with new direction |
| **Reject** | Scores below threshold or fundamental blocker identified | Documented with rationale |

**Output:** Decision Record with rationale, scores, and any conditions.

**Gate:** Human approval — this is THE decision point.

### Stage 6: Route & Handoff

**What happens:** Approved idea is packaged in the correct format and routed to the right next package.

**Routing logic (impact-driven):**
| Impact Level | Brief Type | Destination |
|-------------|-----------|-------------|
| **New project** (large, cross-cutting) | Approved Idea Brief | → AI-PILC (full initiation) |
| **Major change** (to existing project) | Change Request Brief | → AI-PILC (change management) |
| **Small feature** (within existing backlog) | Feature Brief | → AI-POLC / AI-DLC v1 (direct backlog) |

**Handoff mechanism:** `ilc-state.md` (marker file) + the appropriate brief document. Successor packages auto-detect and read.

---

## Adaptive Depth

| Depth | Stages Active | Time | Best For |
|-------|:-------------:|------|----------|
| **Minimal** | 1, 3, 5, 6 (skip shaping/scoping) | 20-30 min | Quick screening of obvious ideas |
| **Standard** | All 6 | 45-90 min | Most ideas — recommended |
| **Comprehensive** | All 6 + deep analysis | 2-3 hours | Strategic bets, large investments |

---

## The Evaluation Rubric (Two-Source Model)

### Source 1: Configurable Rubric (project-specific)

Organizations can weight criteria differently:
- A startup might weight "Market Demand" and "Competitive Position" heavily
- An enterprise might weight "Strategic Alignment" and "Risk Profile" heavily
- A technical team might weight "Technical Feasibility" and "Effort" heavily

### Source 2: Built-In Baseline (universal)

Regardless of rubric weights, certain thresholds are universal:
- Technical Feasibility < 2/5 → automatic defer (can't build it)
- Risk Profile = 5/5 (extreme) → requires explicit risk acceptance before approval
- Effort = XL + Strategic Alignment < 3/5 → high-cost low-alignment warning

---

## State and Session Continuity

`ilc-state.md` tracks:
- Current stage
- Evaluation scores (if past Stage 3)
- Decision (if past Stage 5)
- Output brief type and location
- Depth level
- Session timestamps

Any session can resume exactly where the last one left off — cold resume guarantee applies.

---

## Portfolio Integration

When multiple ideas are evaluated:
- Each gets its own evaluation and Idea Brief
- AI-PPM (portfolio engine) can ingest multiple approved briefs for cross-project prioritization
- Deferred ideas stay in the register with re-evaluation dates
- Rejected ideas remain documented (prevents re-evaluation of the same bad idea)

---

## Related Documents

| Document | Location |
|----------|----------|
| How to Evaluate an Idea Before Building | `knowledge_docs/HOW_TO_EVALUATE_AN_IDEA_BEFORE_BUILDING.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |
| How Depth Levels Work | `knowledge_docs/HOW_DEPTH_LEVELS_WORK.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

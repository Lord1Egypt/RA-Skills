# How the AI-PILC Workflow Engine Works

**Purpose:** Explains how AI-PILC guides a user from a raw requirement to a complete, professional Project Initiation Package (PIP) — the internal mechanics of its phase-gate workflow, state management, adaptive depth, and governance output.

---

## What AI-PILC Does

AI-PILC is an interactive workflow lifecycle package. It transforms any form of raw project requirement — a document, a verbal description, an existing brief, or a brownfield extension need — into a complete, governance-ready Project Initiation Package that a Steering Committee would sign off on.

```
RAW REQUIREMENT (any format)
        │
        ▼
┌───────────────────────────────────────────────────────────────────────┐
│  AI-PILC ENGINE                                                        │
│                                                                        │
│  🔵 INCEPTION ─▶ 🟠 ASSESSMENT ─▶ 🟡 JUSTIFICATION ─▶               │
│  (WHAT is it?)    (SHOULD we?)     (WHY invest?)                      │
│                                                                        │
│  ─▶ 🟣 AUTHORIZATION ─▶ 🟢 PLANNING ─▶ 🚀 MOBILIZATION              │
│     (WHO empowers it?)   (HOW organize?)  (READY to start)            │
│                                                                        │
└───────────────────────────────────────────────────────────────────────┘
        │
        ▼
PROJECT INITIATION PACKAGE (PIP)
   • 12+ governance artifacts
   • 6 management registers
   • State file for chain handoff to AI-ADLC
```

---

## The Six-Phase Architecture

AI-PILC organizes 16 stages into 6 sequential phases. Each phase answers a fundamental project governance question:

| Phase | Question Answered | Stages | Gate |
|-------|------------------|:------:|------|
| 🔵 Inception | WHAT are we working with? | 1-3 | User confirms structured requirements |
| 🟠 Assessment | SHOULD we proceed? | 4-7 | User confirms feasibility + priority |
| 🟡 Justification | WHY invest? | 8 | User approves business case |
| 🟣 Authorization | WHO empowers it? | 9 | User approves project charter |
| 🟢 Planning | HOW will we organize? | 10-14 | User confirms all planning artifacts |
| 🚀 Mobilization | IS IT ready to start? | 15-16 | User confirms kickoff readiness |

---

## How the Engine Runs — Core Mechanics

### 1. State Management

Every session maintains persistent state in `pilc-state.md`:

```
Project ID: PRJ-ACME-2026-001    ← Immutable family-wide correlation key
Current Phase: PLANNING
Current Stage: 11 (Scope Definition)
Completed Stages: 1-10 (with timestamps)
Workflow Depth: Standard
Output Structure: numbered
Pending Decisions: [D-007 awaiting stakeholder input]
Register Counts: Decisions=6, Changes=1, Issues=2, Actions=4, Assumptions=8, Lessons=2
```

State is updated immediately after EVERY stage completion. This enables cold-resume — any AI session can load `pilc-state.md` and continue exactly where the previous session left off.

### 2. Adaptive Depth (Three-Tier)

The engine assesses project complexity at Stage 2 (Source Ingestion) and calibrates all subsequent stages:

| Level | Trigger | Effect |
|-------|---------|--------|
| **Minimal** | Source is clear, scope is small, low risk | Fewer questions, shorter documents, fewer iterations |
| **Standard** | Normal complexity, some gaps to resolve | Full deliverable set, standard interaction depth |
| **Comprehensive** | High complexity, many unknowns, multiple stakeholders | Extended analysis, multiple iteration cycles, deeper detail |

Depth affects every stage: document length, questions asked, iteration cycles, options analysis depth, diagram inclusion, and cross-reference traceability.

### 3. Gate Mechanism (Human-in-the-Loop)

Every stage ends with a gate — a structured approval point:

```
✅ Stage N complete.

[Summary of what was produced]
[Key decisions made]
[Items logged to registers]

Options:
(a) Approve — proceed to Stage N+1
(b) Revise — provide feedback for iteration
(c) Reject — return to a previous stage with new direction
```

The engine NEVER auto-progresses past a gate. This is non-negotiable — it ensures human authority over every governance decision.

### 4. Multiple Input Modes (Adaptive Intake)

AI-PILC accepts input in five formats, adapting its behavior per mode:

| Mode | Input | Engine Behavior |
|------|-------|----------------|
| A | Structured document (PRD, RFP, spec) | Parse and extract requirements systematically |
| B | Raw document (email, brief, notes) | Interpret, structure, and clarify |
| C | Verbal description | Interview mode — ask structured questions to build requirements |
| D | Brownfield extension | "What exists? What's changing? Extend-vs-replace decision?" |
| E | AI-ILC brief (from predecessor) | Load approved idea as pre-structured input |

### 5. Structured Question Format

When decisions are needed, the engine uses a consistent format:

```
### Q-{nn}: {Question Title}

**Context:** {Why this question matters}

**Options:**
- (a) {Option A description}
- (b) {Option B description}
- (c) {Option C description}

**Recommended:** Option {x}
**Rationale:** {Why this is recommended}
```

Every decision is immediately logged in the Decision Register.

### 6. Management Registers (Real-Time Governance)

Six registers are created at Stage 1 and maintained throughout:

| Register | Captures |
|----------|----------|
| Decision Log | Every significant decision with rationale + accountability |
| Change Log | Scope, approach, or timeline changes during initiation |
| Issue Log | Blockers encountered |
| Action Items | Tasks arising from interactions |
| Assumptions & Dependencies | Captured and tracked for validation |
| Lessons Learned | Insights captured at each phase gate |

Entries are added in real-time as they arise — never batched. Each entry is sequentially numbered with phase-prefixed IDs (`PILC-D-001`, `PILC-C-001`).

---

## Output Structure

AI-PILC produces 12+ artifacts organized by user preference (numbered or flat):

| # | Artifact | Produced At |
|---|----------|-------------|
| 1 | Requirement Intake Form | Stage 3 |
| 2 | Requirements Analysis Report | Stage 4 (if depth ≥ Standard) |
| 3 | Clarification Questionnaire | Stage 5 (conditional — if gaps found) |
| 4 | Feasibility Assessment | Stage 6 |
| 5 | Business Case | Stage 8 |
| 6 | Project Charter | Stage 9 |
| 7 | Stakeholder Register | Stage 10 |
| 8 | Scope Statement + WBS | Stage 11 |
| 9 | Resource Plan | Stage 12 |
| 10 | Risk Register | Stage 13 |
| 11 | RACI Matrix | Stage 14 |
| 12 | Kickoff Agenda | Stage 15 |
| — | PIP README (summary + reading guide) | Stage 16 |

---

## Chain Position

AI-PILC is the **first required package** in the AI-* Family chain:

- **Predecessor:** AI-ILC (optional — idea lifecycle pre-stage)
- **Successor:** AI-ADLC (architecture design lifecycle)
- **Marker file:** `pilc-state.md`
- **What AI-ADLC reads:** Project ID, status, depth, output structure, project name

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Phase-gate (not stage-gate) for simple projects | Reduces friction — simple projects don't need 16 approval points |
| PMO Professional persona (15-year veteran) | Output must read as if a senior PMO advisor wrote it |
| PMBOK 7th Edition + PRINCE2 alignment | Recognized frameworks ensure terminology consistency |
| Real-time register entries (not batched) | Governance discipline — nothing falls through cracks |
| No downstream signaling | PIP is a one-time handoff; AI-PILC doesn't reconcile |

---

## Related Documents

| Document | Location |
|----------|----------|
| Core workflow | `ai-pilc/ai-pilc-rules/core-workflow.md` |
| Process overview | `ai-pilc/ai-pilc-rule-details/common/process-overview.md` |
| Session continuity | `ai-pilc/ai-pilc-rule-details/common/session-continuity.md` |
| Family Structure | `FAMILY_STRUCTURE.md` |

*Knowledge Document | Created: 2026-06-11 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

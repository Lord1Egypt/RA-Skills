# AI-PILC — User Guide

**Package:** AI-PILC (AI-Driven Project Initiation Life Cycle)
**Version:** 1.0.0
**Audience:** Project Managers, PMOs, Business Analysts, Sponsors, Delivery Leads

---

## What is AI-PILC?

AI-PILC is an injectable workflow that guides you through the complete process of initiating a project — from receiving a raw requirement to delivering a professional, execution-ready Project Initiation Package (PIP). It reasons and writes as a senior PMO professional, producing PMBOK/PRINCE2-aligned deliverables at every step.

**In one sentence:** AI-PILC turns a raw requirement into a governed, execution-ready Project Initiation Package — the foundation everything else builds on.

---

## When to Use AI-PILC

| Scenario | AI-PILC helps you... |
|----------|---------------------|
| Starting a new project from a requirement | Structure, assess, justify, and plan from scratch |
| Received an approved idea from AI-ILC | Convert Idea Brief into full project initiation |
| Need a business case for investment approval | Build evidence-based justification with cost-benefit |
| Inheriting a project with no initiation docs | Reconstruct initiation artifacts from existing knowledge |
| Preparing for project kickoff | Assemble all governance docs, stakeholders, and plans |

---

## How It Works (5 Minutes)

1. **Install** — Copy package files into your IDE's steering folder (see `setup/INSTALL.md`)
2. **Start a session** — Say: *"Using AI-PILC, initiate a project from this requirement"*
3. **Provide your source** — A requirement doc, idea brief, verbal description, or existing materials
4. **Approve at gates** — Every stage requires your approval before moving forward
5. **Get your PIP** — A complete Project Initiation Package ready for architecture or execution

---

## Input Modes

AI-PILC detects what you already have and adapts:

| What You Have | Mode | Behavior |
|---------------|------|----------|
| AI-ILC output (Idea Brief) | Chain — idea-enriched | Reads ilc-state.md; extracts problem, value, scope, routing decision. Minimal re-questioning. |
| Raw requirement document | Standard | Full 16-stage pipeline with structured ingestion |
| Verbal description | Conversational | Extended questioning to build structured requirement |
| Existing partial initiation | Brownfield | Audits what exists, fills gaps, applies governance |
| Nothing (exploratory) | Discovery | Guides you to articulate the requirement from scratch |

You do NOT need AI-ILC first. AI-PILC works standalone — upstream enriches, absence doesn't block.

---

## The Workflow (6 Phases, 16 Stages)

### Phase 1: Inception (Stages 1–3)

Receive, validate, and structure the requirement.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 1 — Workspace Detection | Detects upstream state files, determines mode + depth | Confirm mode and starting context |
| 2 — Source Ingestion | Receives and validates your input requirement | Confirm the requirement is captured correctly |
| 3 — Requirement Structuring | Structures raw input into a formal Intake Form | Approve the structured requirement |

### Phase 2: Assessment (Stages 4–7)

Analyze feasibility, resolve gaps, prioritize.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 4 — Requirements Analysis | Gap/ambiguity analysis; identifies what's missing or unclear | Confirm findings are valid |
| 5 — Clarification Cycle | Structured Q&A to resolve gaps | Provide answers; confirm resolution |
| 6 — Feasibility Assessment | 4-dimension scoring (technical, financial, operational, schedule) | Approve feasibility verdict |
| 7 — Prioritization | Strategic alignment + MoSCoW prioritization | Confirm priority assignment |

### Phase 3: Justification (Stage 8)

Build the investment case.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 8 — Business Case | Costs, benefits, ROI, options analysis, recommendation | Approve or refine the business case |

### Phase 4: Authorization (Stage 9)

Formalize authority and boundaries.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 9 — Project Charter | Defines authority, objectives, constraints, success criteria | Sign off on the charter |

### Phase 5: Planning (Stages 10–14)

Plan scope, resources, risks, governance.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 10 — Stakeholder Management | Builds stakeholder register with influence/interest | Approve stakeholder map |
| 11 — Scope Definition | WBS + scope boundaries + exclusions | Confirm scope is correct |
| 12 — Resource & Budget | Team structure + cost breakdown | Approve resource plan |
| 13 — Risk Management | Risk register with probability/impact scoring | Validate risk assessment |
| 14 — Governance & Communication | RACI matrix + communication plan | Confirm governance model |

### Phase 6: Mobilization (Stages 15–16)

Prepare kickoff and assemble the final package.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 15 — Kickoff Preparation | Kickoff agenda, materials, presentation outline | Approve kickoff plan |
| 16 — Package Assembly | Consolidates all artifacts into the PIP; finalizes state | Final approval — PIP ready for downstream |

---

## The Relationship with the Project Layer (AI-POLC next)

AI-PILC's output (PIP) is the foundation the entire Project layer reads. In the chain it hands off first to **AI-POLC**, which starts the sequential Project layer (AI-POLC → AI-UXD → AI-ADLC → AI-DWG):

```
AI-PILC ──(PIP)──► AI-POLC ──► AI-UXD ──► AI-ADLC ──► AI-DWG
                    Own the product, then design UX, then architecture
```

| What Flows | Purpose |
|-----------|---------|
| Project Charter | Authority, objectives, constraints |
| Scope Statement + WBS | What's being built |
| Stakeholder Register | Who's involved |
| Risk Register | Known risks downstream design must address |
| Feasibility Assessment | Technology/team constraints |

Every Project-layer package reads the PIP as the source of truth — AI-POLC for backlog scope, AI-UXD for users and goals, AI-ADLC for constraints. The richer the PIP, the less each needs to ask.

---

## Adaptive Depth

AI-PILC auto-calibrates based on project complexity:

| Depth | When Applied | What Changes |
|-------|-------------|--------------|
| **Minimal** | Small scope, clear requirements, low risk | Streamlined PIP — fewer interaction cycles, lighter deliverables |
| **Standard** | Normal complexity, some gaps to resolve | Full deliverable set with standard gates |
| **Comprehensive** | High complexity, many unknowns, large investment | Detailed analysis, multiple iterations, formal governance |

Override anytime: *"Change depth to Comprehensive"*

---

## Session Continuity

AI-PILC saves progress in `pilc-state.md`. You can:
- Close your session at any time
- Resume later — AI-PILC reads state and picks up where you left off
- Switch depth mid-workflow
- Skip or combine stages (with logged rationale)

---

## What You Get (Output Artifacts)

| Artifact | Purpose |
|----------|---------|
| `pilc-state.md` | State tracking + chain marker |
| `requirement-intake-form.md` | Structured requirement |
| `requirements-analysis.md` | Gap/ambiguity findings |
| `feasibility-assessment.md` | 4-dimension scoring |
| `business-case.md` | Investment justification |
| `project-charter.md` | Formal authority + objectives |
| `stakeholder-register.md` | Influence/interest map |
| `scope-statement.md` | WBS + boundaries |
| `resource-plan.md` | Team + budget |
| `risk-register.md` | Risks with scoring |
| `raci-matrix.md` | Governance assignments |
| `kickoff-agenda.md` | Kickoff materials |
| `decision-log.md` | All decisions with rationale |
| Management Registers (5) | Change, Issue, Action, Assumptions, Lessons |
| `PIP_README.md` | Package index + handoff guide |

---

## Quick Start Examples

**From a requirement document:**
```
Using AI-PILC, initiate a project from this requirement:
[paste or reference your requirement document]
```

**From an AI-ILC approved idea:**
```
Using AI-PILC, initiate a project. I have an Approved Idea Brief from AI-ILC.
```

**Verbal / exploratory:**
```
Using AI-PILC, I need to initiate a project for building a customer portal.
I'll describe the requirements conversationally.
```

---

## Tips for Best Results

1. **Provide the richest source you have** — The more context in your initial requirement, the less AI-PILC needs to ask.
2. **Be honest about complexity** — Don't over-process a simple project; don't under-process a complex one.
3. **Approve actively at gates** — AI-PILC won't auto-progress. Your "approved" moves things forward.
4. **Use the clarification cycle** — Stage 5 exists to resolve ambiguity. Don't rush past it.
5. **The business case matters** — Even internal projects benefit from articulated justification.
6. **Hand off the PIP, not fragments** — The assembled package (Stage 16) is what downstream consumes.

---

## What AI-PILC Is NOT

- NOT idea evaluation (that's AI-ILC)
- NOT architecture design (that's AI-ADLC)
- NOT product backlog management (that's AI-POLC)
- NOT code generation or testing
- NOT portfolio management (that's AI-PPM)

AI-PILC is the **Project Initiation companion** — it answers *"Is this project viable, and how should it be set up?"*

---

## Platform Support

AI-PILC works on: Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, and GitHub Copilot — plus any AI-assisted IDE that supports steering/rules files via the Universal Setup.

See `setup/INSTALL.md` for detailed platform instructions.

---

*AI-PILC v1.0.0 | Part of [AIFLC](../README.md) — the AI-* PDLC Family*

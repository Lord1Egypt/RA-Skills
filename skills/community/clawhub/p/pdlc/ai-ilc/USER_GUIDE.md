# AI-ILC — User Guide

**Package:** AI-ILC (AI-Driven Idea Life Cycle)
**Version:** 1.0.0
**Audience:** Innovation Managers, Product Owners, Portfolio Managers, Team Leads, Anyone with an Idea

---

## What is AI-ILC?

AI-ILC is an injectable workflow that takes a raw idea — from anyone, in any format — through a governed evaluation pipeline to a defensible go/no-go decision, then routes the approved idea to the right next step with zero context loss.

**In one sentence:** AI-ILC is the front door of the AI-* Family — it decides *whether* something should start before any work begins.

---

## When to Use AI-ILC

| Scenario | AI-ILC helps you... |
|----------|---------------------|
| Someone has an idea for a new product/project | Capture, evaluate, and decide if it's worth initiating |
| A feature request arrives from a customer | Score it consistently and route it to the right backlog |
| You need to prioritize competing ideas | Apply consistent 7-criterion evaluation across all ideas |
| An existing project needs a big change | Evaluate impact and route as a Change Request Brief |
| You want an audit trail for idea decisions | Log every score, decision, and routing choice from day one |

---

## How It Works (5 Minutes)

1. **Install** — Copy package files into your IDE's steering folder (see `setup/INSTALL.md`)
2. **Start a session** — Say: *"I have an idea"* or *"Using AI-ILC, evaluate this idea"*
3. **Describe your idea** — Any format: verbal, one-liner, document, feature request
4. **Answer questions** — AI-ILC shapes, scores, and scopes with your input at every gate
5. **Get your decision + brief** — An Approved Idea Brief routed to the right next step

---

## Input Modes

AI-ILC accepts ideas in any form and adapts:

| What You Provide | Behavior |
|------------------|----------|
| A one-line idea statement | Full shaping cycle — AI asks questions to build structure |
| A feature request document | Accelerated capture — extracts key elements, validates with you |
| A verbal description | Captures as-is, structures through the Shape stage |
| A formal proposal | Evaluates directly — may skip early shaping |
| An idea for an existing project | Routes as Change Request or Feature (not new project) |

---

## The Workflow (6 Stages)

### Stage 1: Capture

Log the idea fast — get it on record before details fade.

| What Happens | What You Decide |
|-------------|-----------------|
| Records idea statement, submitter, context, urgency | Confirm the idea is captured accurately |

### Stage 2: Shape

Structure the problem — turn a vague idea into a clear proposition.

| What Happens | What You Decide |
|-------------|-----------------|
| Identifies problem, target audience, desired outcome, constraints | Approve the structured idea statement |

### Stage 3: Evaluate

Score the idea consistently against 7 criteria with value analysis.

| What Happens | What You Decide |
|-------------|-----------------|
| Applies 7-criterion rubric (two-source model); articulates WHY it matters | Review scores; override if needed |

### Stage 4: Scope

Define boundaries — what's in, what's out, what's the impact.

| What Happens | What You Decide |
|-------------|-----------------|
| Lightweight impact assessment; defines rough boundaries | Confirm scope boundaries |

### Stage 5: Approve

The go/no-go decision — explicit, recorded, with rationale.

| What Happens | What You Decide |
|-------------|-----------------|
| Presents recommendation with evidence summary | **Approved**, **Parked** (with revisit date), or **Rejected** |

### Stage 6: Route & Handoff

Determine where the approved idea goes next and produce the right brief.

| What Happens | What You Decide |
|-------------|-----------------|
| Classifies as new project / big change / small feature; produces brief | Confirm routing destination |

---

## Routing Logic

AI-ILC routes approved ideas based on impact:

```
Does a project exist for this idea?
├── NO ──────────────────────► AI-PILC (new project) → Approved Idea Brief
├── YES + BIG change ────────► AI-PILC change management → Change Request Brief
└── YES + SMALL change ──────► Product backlog (AI-POLC/AI-DLC v1) → Feature Brief
```

**You're never blocked.** If a target package isn't installed, the brief is a portable document you can use with any methodology.

---

## The Relationship with AI-PILC and AI-PPM

AI-ILC is the **optional pre-stage** — the funnel before the funnel:

```
AI-ILC (optional) ⇢ AI-PILC ⇢ AI-PPM
 Decide it            Initiate it   Govern it
```

| Direction | What Flows | When |
|-----------|-----------|------|
| ILC → PILC | Approved Idea Brief or Change Request Brief | Idea approved as new project or big change |
| ILC → POLC/DLC | Feature Brief | Idea approved as small feature for existing project |

The AI-* Family works without AI-ILC — teams that already have a decision process can start directly at AI-PILC.

---

## Adaptive Depth

AI-ILC auto-calibrates based on idea complexity:

| Depth | When Applied | What Changes |
|-------|-------------|--------------|
| **Minimal** | Simple, clear feature request with obvious value | Quick capture + lightweight evaluation + brief |
| **Standard** | Typical idea with some unknowns | Full 6-stage pipeline with standard scoring |
| **Comprehensive** | Complex, high-investment, multi-stakeholder idea | Deep evaluation, multiple scoring perspectives, detailed scoping |

Override anytime: *"Change depth to Comprehensive"*

---

## Session Continuity

AI-ILC saves progress in `ilc-state.md`. You can:
- Close your session at any time
- Resume later — AI-ILC reads state and picks up where you left off
- Switch depth mid-workflow
- Process multiple ideas across sessions (Idea Register tracks them all)

---

## What You Get (Output Artifacts)

| Artifact | Purpose |
|----------|---------|
| `ilc-state.md` | State tracking + chain marker |
| `idea-register.md` | Portfolio funnel — all ideas with status |
| `idea-entry.md` | Structured idea statement |
| `decision-record.md` | Go/No-Go decision with full rationale |
| `approved-idea-brief.md` | Brief for new projects (→ AI-PILC) |
| `change-request-brief.md` | Brief for big changes (→ AI-PILC change mgmt) |
| `feature-brief.md` | Brief for small features (→ backlog) |

**How they're organized:** shared artifacts (`ilc-state.md`, `Idea_Register.md`, and the `management_framework/` spine) stay flat at your output root. Each idea's own artifacts (its statement, brief, and decision record) go into a per-idea subfolder named `{NNN}-{idea-slug}/` (e.g. `001-fleet-tracking/`), keyed by the idea's register number. The folder name never changes — you see how many ideas are approved/parked/rejected at a glance from the Idea Register, not by hunting through folders.

---

## Quick Start Examples

**New idea, no context:**
```
I have an idea — we should build a self-service portal for our customers.
```

**Feature request from a customer:**
```
Using AI-ILC, evaluate this feature request: "Add bulk export to CSV for all report types."
The project already exists.
```

**Formal proposal evaluation:**
```
Using AI-ILC, evaluate this proposal document for a new mobile app.
[paste or reference document]
```

---

## Tips for Best Results

1. **Don't self-censor ideas** — AI-ILC evaluates fairly; submit anything and let the pipeline score it.
2. **Be honest about impact** — "Big" vs. "small" determines routing. If it changes architecture, it's big.
3. **Use Parked, not Rejected** — If timing is wrong but the idea has merit, park it with a revisit date.
4. **Review the Idea Register periodically** — Parked ideas may become relevant as conditions change.
5. **Let the brief carry context** — The brief exists so the next step (PILC, POLC, DLC) doesn't start cold.
6. **One idea per run** — Each ILC session evaluates one idea. Multiple ideas = multiple sessions.

---

## What AI-ILC Is NOT

- NOT project initiation (that's AI-PILC)
- NOT architecture design (that's AI-ADLC)
- NOT a portfolio manager (that's AI-PPM)
- NOT a backlog manager (that's AI-POLC)
- NOT a brainstorming tool — it evaluates ideas, not generates them

AI-ILC is the **idea funnel** — it answers *"Should we even start this?"*

---

## Platform Support

AI-ILC works on: Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, and GitHub Copilot — plus any AI-assisted IDE that supports steering/rules files via the Universal Setup.

See `setup/INSTALL.md` for detailed platform instructions.

---

*AI-ILC v1.0.0 | Part of [AIFLC](../README.md) — the AI-* PDLC Family*

# AI-POLC — User Guide

**Package:** AI-POLC (AI-Driven Product Ownership Life Cycle)
**Version:** 1.0.0
**Audience:** Product Owners, Product Managers, Scrum Masters, Engineering Leads

---

## What is AI-POLC?

AI-POLC is an injectable workflow that turns business intent into a prioritized, governed product backlog. It acts as an experienced Senior Product Owner guiding you through establishing product ownership practices — from vision to a fully assembled Product Backlog Package (PBP) ready for development.

**In one sentence:** AI-POLC is the single source of truth for *what gets built, in what order, and why*.

---

## When to Use AI-POLC

| Scenario | AI-POLC helps you... |
|----------|---------------------|
| Starting a new product/project | Define vision, decompose into epics, set governance rules |
| Inheriting an ungoverned backlog | Assess, structure, and bring discipline to existing items |
| Need to reprioritize mid-delivery | Value-rank, release-slice, and document rationale |
| Handoff to development team | Produce a governed PBP with DoR/DoD and traceability |
| Sprint/increment acceptance | Process feedback, accept work, adjust priorities |

---

## How It Works (5 Minutes)

1. **Install** — Copy package files into your IDE's steering folder (see `setup/INSTALL.md`)
2. **Start a session** — Type the activation key `_POLC_`, or say: *"Using AI-POLC, establish product ownership for this project"*
3. **Answer questions** — AI-POLC detects your context and asks targeted questions
4. **Approve at gates** — Every phase requires your approval before moving forward
5. **Get your PBP** — A complete, governed backlog package ready for AI-DWG or manual development

**Handy activation keys:**
- `_POLC_` — activate AI-POLC directly (wins over keyword matching; switches immediately)
- `_ACTIVE_` — ask which AI-* package is currently active (read-only check, changes nothing)

---

## Input Modes

AI-POLC detects what you already have and adapts:

| What You Have | Mode | Behavior |
|---------------|------|----------|
| AI-PILC output (PIP) | Chain — full context | Reads pilc-state.md; extracts scope, goals, stakeholders, risks. Minimal questions. |
| AI-ADLC output (AP) | Chain — architecture-enriched | Reads adlc-state.md; adds architecture constraints, bounded contexts, NFRs to backlog governance. |
| AI-UXD output (UXP) | Chain — UX-enriched | Reads uxd-state.md; consumes personas/journeys for value-based prioritization. |
| AI-ILC output (Idea Brief) | Chain — feature intake | Reads ilc-state.md (Route=feature); maps idea→epic seed. |
| None of the above | Standalone | Full questionnaire. You provide vision, scope, and constraints conversationally. |
| Existing backlog (no governance) | Brownfield | Audits current state, identifies gaps, applies progressive governance. |

You do NOT need to run any predecessor. AI-POLC works standalone — upstream enriches, absence doesn't block.

---

## The Workflow (6 Phases, 16 Stages)

### Phase 1: Foundation (Stages 1–3)

Establishes context: what product, who's the PO, what authority, what depth.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 1 — Workspace Detection | Detects upstream state files, determines mode + depth | Confirm mode (chain/standalone/brownfield) |
| 2 — Product Vision | Drafts vision statement, goals, success metrics | Approve or refine the vision |
| 3 — PO Charter | Defines your authority, RACI, decision boundaries | Confirm decision rights |

### Phase 2: Strategy (Stages 4–7)

Plans the product at epic/release level.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 4 — Discovery & Roadmap | Maps value proposition; creates Now/Next/Later roadmap | Approve themes and roadmap shape |
| 5 — Epic Decomposition | Breaks goals into INVEST-aligned epics with acceptance criteria | Confirm epic list is complete |
| 6 — Prioritization | Applies WSJF/MoSCoW/custom model; ranks backlog | Confirm or override ordering |
| 7 — Release Slicing | Groups epics into releases; defines MVP/MMP scope | Approve release plan |

### Phase 3: Governance (Stages 8–10)

Sets quality rules that flow into the development workspace.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 8 — DoR/DoD | Drafts Definition of Ready + Done checklists | Confirm quality bar |
| 9 — Risk & Assumptions | Creates product risk register + assumption log | Validate risk scoring |
| 10 — Traceability | Builds Intent→Epic→Story links | Confirm traceability depth |

### Phase 4: Stakeholders (Stages 11–12)

Governs communication and documentation responsibilities.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 11 — Stakeholder Map | Maps influence/interest; sets communication cadence | Approve stakeholder plan |
| 12 — Product Docs | Establishes release notes governance + changelog framework | Confirm documentation approach |

### Phase 5: Assembly (Stage 13)

Packages everything into the PBP.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 13 — PBP Assembly | Consolidates all artifacts; finalizes polc-state.md | Final approval — PBP ready for downstream |

### Phase 6: Operations (Stages 14–16, repeating)

Ongoing product ownership during development — re-enter as needed.

| Stage | What Happens | When |
|-------|-------------|------|
| 14 — Backlog Operations | Refinement, splitting, debt trade-offs, stale cleanup | Before each sprint/increment |
| 15 — Acceptance & Feedback | Accept completed work; process DLC feedback; reprioritize | After each increment |
| 16 — Value Metrics | Track value realization against original goals | Periodic (monthly/quarterly) |

---

## The Relationship with AI-DLC v1

AI-POLC and AI-DLC v1 have a **bidirectional exchange** — they're not a one-shot handoff:

```
AI-POLC ──(epics/stories)──► AI-DLC v1
AI-POLC ◄──(feedback/completion)── AI-DLC v1
```

| Direction | What Flows | When |
|-----------|-----------|------|
| POLC → DLC | Prioritized epics, acceptance criteria, DoR/DoD | At PBP handoff + each refinement |
| DLC → POLC | Bolt completions, blockers, velocity data | After each increment |

**Who does what:**
- AI-POLC = *what* to build, *in what order*, *to what quality bar*
- AI-DLC v1 = *how* to build it (design docs, code, tests)
- AI-POLC does NOT write code or implementation specs
- AI-DLC v1 does NOT decide product priorities or acceptance

---

## Tier 2: Story Elaboration

By default, AI-POLC stops at epic level. Story elaboration (user stories + acceptance criteria) is handled by AI-DLC v1's Inception phase in chain mode.

**AI-POLC asks you — you don't have to remember to enable it.** Once your epics are confirmed (end of Stage 5), AI-POLC explicitly offers the choice:

- **Keep Tier 2 OFF** — epics are the handoff artifact (recommended in chain mode, since AI-DLC v1 elaborates stories)
- **Turn Tier 2 ON now** — AI-POLC writes PO-quality user stories, and you pick the story format

You can flip this decision at any point in the workflow, not just at the gate. Say *"turn on story elaboration"* (or *"turn it off"*) mid-session and AI-POLC adjusts on the fly.

**When to turn Tier 2 ON:**
- Standalone mode (no AI-DLC v1 available)
- You want PO-quality pre-elaboration before handing to developers

**Choosing the story format:** When Tier 2 is on, AI-POLC asks which user-story type you want:

| Story Type | Format | Best for |
|------------|--------|----------|
| **Classic INVEST** (default) | *As a…, I want…, So that…* + Given/When/Then AC | AI-DLC, freestyle |
| **EARS** | *When {trigger} the {system} shall {response}* | Spec-driven build (e.g., GitHub Spec Kit) |
| **Job Story** | *When {situation}, I want {motivation}, so I can {outcome}* | freestyle, AI-DLC |
| **Freestyle** | Any narrative + acceptance criteria you prefer | freestyle only |
| **Hybrid** | AI-POLC picks the most natural style per story | freestyle, AI-DLC |

Your choice is recorded in `polc-state.md` so AI-DWG can advise on the best-fit build method downstream. Default is Classic INVEST; EARS is recommended if you mention spec-driven development.

---

## Extensions (Opt-In)

Extensions add specialized capabilities. They activate when you use trigger phrases:

| Say... | Extension Activates | What It Adds |
|--------|-------------------|--------------|
| "OKRs" / "jobs to be done" | Advanced Discovery | OKR→Epic mapping, hypothesis-driven planning |
| "full traceability" | Full Traceability | Complete requirement→epic→story→test matrix |
| "full risk management" | Full Risk Register | Formal risk register with FMEA-style scoring |
| "track value" | Value & Metrics Engine | KPI dashboards, benefits tracking |
| "PRD" / "feature brief" | Full Product Docs | Enterprise documentation templates |
| "check quality" | Quality Review | AI-assisted backlog quality scoring |
| "define next version scope" | MVP/MMP for Mature | Version scoping for existing products |

---

## Adaptive Depth

AI-POLC auto-calibrates based on your product complexity:

| Depth | When Applied | What Changes |
|-------|-------------|--------------|
| **Minimal** | Simple product, clear scope, few stakeholders | Streamlined PBP — vision + epics + DoR/DoD + basic release plan |
| **Standard** | Typical complexity, some unknowns | Full PBP with all governance artifacts |
| **Comprehensive** | Enterprise, multi-team, heavy compliance | Full traceability, extensions auto-suggested, formal risk register |

Override anytime: *"Change depth to Comprehensive"*

---

## Session Continuity

AI-POLC saves progress in `polc-state.md`. You can:
- Close your session at any time
- Resume later — AI-POLC reads state and picks up where you left off
- Switch depth mid-workflow
- Skip or combine stages (with logged rationale)

---

## What You Get (Output Artifacts)

After completing the workflow, your PBP contains:

| Artifact | Purpose |
|----------|---------|
| `polc-state.md` | State tracking + chain marker |
| `product-vision.md` | Vision, goals, success metrics |
| `po-charter.md` | Authority, RACI, decision boundaries |
| `roadmap.md` | Now/Next/Later strategic view |
| `epics/*.md` | Individual epic definitions |
| `prioritization-register.md` | Ranked backlog with model + rationale |
| `release-plan.md` | Release slicing + MVP/MMP scope |
| `definition-of-ready.md` | DoR checklist |
| `definition-of-done.md` | DoD checklist |
| `product-risk-register.md` | Risks + assumptions |
| `traceability-matrix.md` | Intent→Epic→Story links |
| `stakeholder-map.md` | Influence/interest + communication plan |
| `release-notes-governance.md` | Release-notes / changelog governance framework |
| `PBP_README.md` | Package index + completeness report |

---

## Backlog-Health Agent (`BLH__`)

When AI-POLC finishes assembling your PBP, it automatically installs a lightweight governance agent into your workspace — no setup required on your part.

| What | Detail |
|------|--------|
| Agent | `backlog-health-agent` (registered as `POLC-AG-01`) |
| Shortcut | `BLH__` — active immediately after install |
| Purpose | Validates backlog health (traceability, DoR/DoD coverage, orphan epics, priority integrity) |
| When to use | Type `BLH__` before handing the PBP downstream to catch gaps early |

The agent installs itself independently — it does not depend on any other AI-* package being present. Just type `BLH__` in your workspace whenever you want a backlog-health check.

---

## Brownfield Mode

Already have a backlog? AI-POLC doesn't force a restart:

1. **Audit** — Scans existing items for format, completeness, traceability gaps
2. **Gap Analysis** — Identifies what governance is missing (no DoR? no priority model?)
3. **Progressive Adoption** — Brings existing backlog under discipline incrementally
4. **Preserve Content** — Enriches, never discards existing work

Say: *"I have an existing backlog that needs governance"* to activate brownfield mode.

---

## Quick Start Examples

**Full chain (richest context):**
```
Using AI-POLC, establish product ownership for this project.
I have a PIP from AI-PILC and an Architecture Package from AI-ADLC.
```

**Standalone (minimal context):**
```
Using AI-POLC, help me build a product backlog for a mobile banking app.
I'll provide the scope verbally.
```

**Brownfield (existing backlog):**
```
Using AI-POLC, I have 200 Jira tickets with no governance.
Help me bring structure and prioritization.
```

**Operations re-entry:**
```
Using AI-POLC, let's do sprint acceptance for Increment 4.
Three stories completed, one blocked.
```

---

## Tips for Best Results

1. **Be honest about depth** — If your product is simple, say so. Over-governance slows you down.
2. **Approve actively at gates** — AI-POLC won't auto-progress. Your "approved" moves things forward.
3. **Use the governance spine** — Decision Log entries (`POLC-D-NNN`) give you an audit trail.
4. **Don't skip traceability** — It's what lets you answer "why did we build that?" later.
5. **Re-enter for Operations** — Phases 1–5 are setup; Phase 6 is your ongoing rhythm.
6. **Override depth anytime** — If you realize mid-workflow you need more/less detail, just say so.

---

## What AI-POLC Is NOT

- NOT a project management tool (that's AI-PILC)
- NOT architecture design (that's AI-ADLC)
- NOT code or test generation (that's AI-DLC v1)
- NOT compliance enforcement (that's AI-GCE)
- NOT portfolio management (that's AI-PPM)

AI-POLC is the **Product Owner's companion** — it answers *what gets built, in what order, and why*.

---

## Platform Support

AI-POLC works on: Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, and GitHub Copilot — plus any AI-assisted IDE that supports steering/rules files via the Universal Setup.

See `setup/INSTALL.md` for detailed platform instructions.

---

*AI-POLC v1.0.0 | Part of [AIFLC](../README.md) — the AI-* PDLC Family*

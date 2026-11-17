# How to Run the Full Chain

**Purpose:** End-to-end operational guide for running the complete AI-* Family pipeline — from raw idea or requirement through to a governed, ready-to-code development workspace that AI-DLC v1 consumes.

---

## Who This Is For

Practitioners who want to use the full AI-* Family chain on a real project. You've installed the packages and want to know: "What do I do first? What order? How do the handoffs work? What do I get at the end?"

---

## The Full Chain at a Glance

```
 (optional)
  AI-ILC         AI-PILC          AI-POLC → AI-UXD → AI-ADLC          AI-DWG          AI-GCE + AI-TGE
  ────────       ────────         ──────────────────────────           ────────        ────────────────
  Evaluate →     Initiate →       Own → Design UX → Design            Generate →      Enforce
  the idea       the project      backlog / UX / architecture          workspace       governance

  Output:        Output:          Output:                              Output:         Output:
  Idea Brief     PIP              PBP + UXP + AP                       Dev Workspace   Compliance Layer
```

**Minimum viable chain:** AI-PILC → AI-POLC → AI-ADLC → AI-DWG → AI-GCE (5 packages)
**Full chain:** AI-ILC → AI-PILC → AI-POLC → AI-UXD → AI-ADLC → AI-DWG → AI-GCE + AI-TGE → AI-DLC v1

---

## Step 1: Evaluate the Idea (AI-ILC — Optional)

**When to use:** You have a raw idea and want structured evaluation before committing to a full project.

**What you do:**
1. Install AI-ILC into your workspace
2. Provide your idea in any form (verbal, one-pager, Slack message)
3. AI-ILC guides you through evaluation: problem validation, market fit, feasibility, effort/value scoring
4. Gate: Approve or reject the idea

**What you get:** An Approved Idea Brief with structured assessment — ready to feed AI-PILC.

**Skip if:** You already have an approved initiative, a formal requirement, or stakeholder commitment. Jump straight to AI-PILC.

---

## Step 2: Initiate the Project (AI-PILC)

**When to use:** Always — this is the formal starting point for any project entering the chain.

**What you do:**
1. Install AI-PILC into your workspace
2. Provide input: Idea Brief (from AI-ILC), raw requirements document, verbal description, or brownfield context
3. AI-PILC guides you through 13 stages across 4 phases:
   - **Inception** — capture and structure requirements
   - **Assessment** — feasibility, stakeholder analysis, risk identification
   - **Planning** — approach, budget, resource, quality planning
   - **Definition** — scope statement, project charter, governance framework
4. Approve each stage gate before proceeding

**What you get:** The Project Initiation Package (PIP) — 12+ artifacts including:
- Structured requirements, feasibility study, stakeholder register
- Risk register, scope statement, project charter
- Management framework (6 governance registers)
- `pilc-state.md` (marker file for chain handoff)

**Key decision:** Choose your depth level (Minimal / Standard / Comprehensive) at Stage 2. This cascades to all downstream packages.

---

## Step 3: Own the Product, Design UX, and Architect (AI-POLC → AI-UXD → AI-ADLC)

**When to use:** After AI-PILC completes (or when you have a PIP / requirements + charter from another source). The Project layer runs **sequentially** — each package completes its primary output before the next starts, so each discipline builds on firm upstream decisions.

### Step 3a — Product Ownership (AI-POLC)

**What you do:**
1. Install AI-POLC into your workspace
2. Point it at the PIP output folder (it auto-detects `pilc-state.md`)
3. AI-POLC guides you through product vision, epic decomposition, backlog prioritization, and release planning (MVP/MMP)

**What you get:** Product Backlog Package (PBP) — epics, stories, acceptance criteria, prioritization rationale; `polc-state.md` (marker file).

### Step 3b — UX Design (AI-UXD)

**What you do:**
1. Install AI-UXD into your workspace
2. It auto-detects `pilc-state.md` and `polc-state.md`
3. AI-UXD produces personas, user journeys, information architecture, user flows, design system + tokens, and an accessibility baseline

**What you get:** UX Design Package (UXP); `uxd-state.md` (marker file). AI-UXD and AI-POLC exchange during the strategy stage — personas ground the backlog, value goals focus the research.

### Step 3c — Architecture (AI-ADLC)

**What you do:**
1. Install AI-ADLC into your workspace
2. It auto-detects `pilc-state.md`, `polc-state.md`, and `uxd-state.md`
3. AI-ADLC guides you through 13 stages across 5 phases:
   - **Foundation** — workspace setup, requirements ingestion, architecture vision
   - **Decomposition** — system context (L1), container design (L2)
   - **Decisions** — tech stack, multi-tenancy, security & identity
   - **Design** — data architecture, API design, integration, component design (L3)
   - **Assembly** — consolidate into the Architecture Package
4. Opt in to extensions if needed (DDD, Microservices, BFF, Event Sourcing, Resilience, Feature Flags)

**What you get:**
- Architecture Package (AP): vision, C4 diagrams, ADRs, API contracts, data model, security architecture
- `adlc-state.md` (marker file)

**Feedback loops:** AI-ADLC feeds cost/risk back to AI-POLC and design constraints back to AI-UXD — iterative refinement without changing the forward sequence. AI-ADLC is the terminal Project-layer predecessor: by the time it completes, AI-DWG has all three inputs (AP + PBP + UXP).

---

## Step 4: Generate the Development Workspace (AI-DWG)

**When to use:** After AI-ADLC completes (the last step of the sequential Project-layer design chain). By this point, all three inputs are present: AP (from AI-ADLC), PBP (from AI-POLC), and UXP (from AI-UXD).

**What you do:**
1. Install AI-DWG into your workspace
2. Point it at the AP output folder (it auto-detects `adlc-state.md`)
3. Optionally point it at UXP and PBP folders for enrichment
4. AI-DWG runs in one of four modes:
   - **Mode 1: Full Generation** — greenfield, produce everything
   - **Mode 2: Delta Reconciliation** — architecture changed, update affected files
   - **Mode 3: Brownfield Overlay** — governance onto existing codebase
   - **Mode 4: Extension Enrichment** — add extension-specific content
5. Review and approve the generated workspace

**What you get:** A ready-to-code development workspace:
- `.kiro/steering/` (19+ steering files derived from architecture decisions)
- `PROJECT_INSTRUCTIONS.md` (project context for AI sessions)
- `DEFINITION_OF_DONE.md`, `TEAM_AGREEMENTS.md`, `CODEOWNERS`
- Folder structure matching container/component architecture
- `docker-compose.yml`, CI/CD templates
- Management framework (governance registers)

---

## Step 5: Activate Governance (AI-GCE + AI-TGE)

**When to use:** After AI-DWG produces the workspace (or on any workspace with `.kiro/steering/`).

**What you do:**
1. Install AI-GCE into your workspace
2. It auto-detects the workspace by scanning for `.kiro/steering/`
3. AI-GCE derives governance from two sources:
   - **Steering files** (project-specific rules from architecture decisions)
   - **Built-in baseline** (universal methodology rules: author ≠ approver, spec before code, etc.)
4. Choose your starting tier:
   - **Tier 1 (Foundational)** — essential rules, minimal friction
   - **Tier 2 (Standard)** — full architecture + process enforcement
   - **Tier 3 (Advanced)** — performance budgets, accessibility, observability
5. Review generated hooks and rules before activation

**In parallel:**
- **AI-TGE** — Generates test governance (coverage thresholds, test-type requirements, regression policies)

**What you get:**
- `.kiro/hooks/` (14+ automated enforcement hooks)
- `.kiro/agents/` (process governance agents)
- `.governance/rules/` (numbered compliance rules)
- `.governance/compliance-log/` (audit trail schema)
- `.compliance-state.json` (tier tracking)

---

## Step 6: Build with AI-DLC v1

**What happens next:** The workspace is ready for Amazon's AI-DLC v1 (or any AI-assisted development workflow). AI-DLC v1 consumes:
- The steering files (architectural constraints)
- The hooks (automated enforcement)
- The user stories (from AI-POLC's PBP)
- The project instructions (context for every session)

AI-GCE and AI-TGE run continuously alongside AI-DLC v1, enforcing governance and test quality throughout delivery.

---

## Entry Points (You Don't Have to Start at Step 1)

| Your situation | Start at |
|---------------|----------|
| Raw idea, no commitment yet | Step 1 (AI-ILC) |
| Approved initiative, need full initiation | Step 2 (AI-PILC) |
| Have a PIP / requirements + charter, ready to design | Step 3 (AI-POLC) |
| Have architecture docs, need workspace | Step 4 (AI-DWG) |
| Have existing codebase, need governance | Step 5 (AI-GCE) |

Every package works standalone (OR-Input Pattern). The chain enriches quality but doesn't mandate full traversal.

---

## Handoff Mechanics

Each package hands off to the next via **marker files**:

| From | To | Marker Detected | What's Read |
|------|----|-----------------|-------------|
| AI-ILC | AI-PILC | `ilc-state.md` | Idea Brief, evaluation score |
| AI-PILC | AI-POLC | `pilc-state.md` | Requirements, charter, constraints, depth |
| AI-POLC | AI-UXD | `polc-state.md` | Backlog, epics, prioritization, value goals |
| AI-UXD | AI-ADLC | `uxd-state.md` | Personas, journeys, design system, accessibility baseline |
| AI-ADLC | AI-DWG | `adlc-state.md` (+ `polc-state.md`, `uxd-state.md`) | AP artifacts, ADRs, extensions list — plus PBP + UXP |
| AI-DWG | AI-GCE | `.kiro/steering/workspace-rules.md` | All steering files |

Detection is automatic — successor packages scan for the marker, find it, and read what they need. No manual wiring required.

---

## Depth Cascading

The depth level chosen at AI-PILC (or wherever you enter the chain) cascades forward:

| Depth | AI-PILC | AI-POLC | AI-UXD | AI-ADLC | AI-DWG | AI-GCE |
|-------|---------|---------|--------|---------|--------|--------|
| **Minimal** | Core artifacts only | Essential backlog | Core personas/journeys | L1-L2 only, fewer ADRs | Essential steering files | Tier 1 only |
| **Standard** | Full 16-stage output | Full backlog + release plan | Full UXP | Full L1-L3, all ADRs | All steering + templates | Tier 1-2 |
| **Comprehensive** | Extended analysis | Detailed roadmap + metrics | Full + accessibility audit | Full + all extensions considered | Full + operational docs | Tier 1-3 |

You can override depth at any package — but the default is to inherit from the predecessor.

---

## Time Expectations

| Step | Typical Duration (Standard depth) |
|------|-----------------------------------|
| AI-ILC | 1 session (30–60 min) |
| AI-PILC | 2–3 sessions (2–4 hours total) |
| AI-POLC | 2–3 sessions (2–4 hours total) |
| AI-UXD | 2–4 sessions (3–6 hours total) |
| AI-ADLC | 3–5 sessions (4–8 hours total) |
| AI-DWG | 1 session (30–60 min) — mostly automated |
| AI-GCE | 1 session (20–40 min) — mostly automated |

**Total chain:** ~15–25 hours of human interaction across 1–2 weeks. Most time is in design (AI-ADLC) where decisions matter most. Generation and enforcement (AI-DWG, AI-GCE) are fast because they derive from prior decisions.

---

## Common Pitfalls

| Pitfall | Prevention |
|---------|-----------|
| Skipping AI-PILC ("we already know what to build") | Even familiar projects benefit from structured scope + risk capture. Use Minimal depth. |
| Running AI-ADLC without extensions analysis | Review extension opt-in criteria at Stage 4. Activating DDD later requires re-running stages. |
| Not running AI-POLC/AI-UXD before AI-ADLC | They feed architecture and enrich AI-DWG's output significantly. The sequence is POLC → UXD → ADLC; skipping them means DWG generates from architecture only. |
| Starting AI-GCE at Tier 3 | Teams reject governance that's too heavy too fast. Start Tier 1, graduate when ready. |
| Ignoring brownfield mode | Most real projects extend existing systems. Use Mode 3/4, not Mode 1. |

---

## Related Documents

| Document | Location |
|----------|----------|
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |
| How Depth Levels Work | `knowledge_docs/HOW_DEPTH_LEVELS_WORK.md` |
| How Gates and Approvals Work | `knowledge_docs/HOW_GATES_AND_APPROVALS_WORK.md` |
| Family Structure | `FAMILY_STRUCTURE.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

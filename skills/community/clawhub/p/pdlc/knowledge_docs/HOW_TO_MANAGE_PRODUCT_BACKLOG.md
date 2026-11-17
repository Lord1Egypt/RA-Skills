# How to Manage a Product Backlog

**Purpose:** Practical guide for using AI-POLC to build and operate a governed, value-prioritized product backlog — from product vision through epic decomposition, prioritization, release planning, and the ongoing back-and-forth with development. This is the operational companion to the mechanics doc: it answers "I need to manage a backlog, how do I actually use this?"

---

## Who This Is For

Product owners, product managers, or team leads who own *what gets built, in what order, and why*. You want a backlog that is prioritized by value, traceable to goals, and ready for development to consume — without drowning in ceremony. You're comfortable making product calls; you want AI-POLC to structure the work, enforce discipline, and keep the backlog healthy over time.

---

## Before You Start

**You need:**
- AI-POLC installed in your AI workspace (see `ai-polc/setup/INSTALL.md`)
- Input — ANY of the following works:
  - A PIP from AI-PILC (ideal — gives you scope, goals, stakeholders, risks)
  - An Architecture Package from AI-ADLC (adds technical constraints and bounded contexts)
  - A UX Design Package from AI-UXD (adds personas and journeys for prioritization)
  - A verbal description of the product and its goals
  - An existing, ungoverned backlog you want to bring under discipline (brownfield)

**You do NOT need:**
- A finished vision statement (AI-POLC drafts one with you)
- Epics already written
- A chosen prioritization model
- Any predecessor package — AI-POLC runs standalone; upstream enriches, absence doesn't block

---

## When to Use AI-POLC

| Your Situation | What AI-POLC Does |
|----------------|-------------------|
| New product, blank backlog | Vision → epics → prioritized, release-sliced backlog with governance |
| Inherited an ungoverned pile of tickets | Audits, gap-analyzes, and applies discipline progressively (brownfield) |
| Mid-delivery reprioritization | Re-ranks by value, re-slices releases, records the rationale |
| Handoff to a dev team | Produces a PBP with DoR/DoD and traceability ready for AI-DWG / AI-DLC v1 |
| Increment acceptance | Accepts completed work against DoD, processes feedback, reprioritizes |

If you need *project* initiation (charter, budget, feasibility), that's AI-PILC. If you need *how to build*, that's AI-DLC v1. AI-POLC owns the **what / why / order**.

---

## Starting Out: Standalone vs. Chain

AI-POLC adapts to what you already have. You don't change how you work — you just tell it your situation at Stage 1.

| Start Mode | What You Say | What Happens |
|-----------|-------------|--------------|
| **Chain (PIP/AP/UXP present)** | "Establish product ownership; I have a PIP and AP" | Reads `pilc-state.md` / `adlc-state.md` / `uxd-state.md`, extracts scope, goals, constraints, personas — asks minimal questions |
| **Chain (feature intake)** | (auto-detected) | Detects `ilc-state.md` (Route=feature), seeds an epic from the feature brief, sets `derivedFrom` lineage |
| **Standalone** | "Help me build a backlog for a mobile banking app" | Full guided questionnaire — you provide vision and scope conversationally |
| **Brownfield** | "I have 200 tickets with no governance" | Audits existing items, finds gaps, applies governance incrementally — never discards your work |

**Marker file:** AI-POLC tracks everything in `polc-state.md`, keyed by a camelCase `projectId` (inherited from `pilc-state.md` when chained, or assigned when standalone). Example: `projectId: PRJ-ACME-2026-001`. Close and resume any time — the state file picks up where you left off.

---

## The Process (16 Stages, 6 Phases)

### Phase 1: Foundation — "What product, who owns it?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 1. Workspace Detection & Intake | Detects upstream state files, sets mode + depth, flags upstream changes | Confirm mode (chain/standalone/brownfield) |
| 2. Product Vision & Goals | Drafts vision statement, product goals, success metrics (OKRs/KPIs) | Approve or refine — the vision is the spine everything traces to |
| 3. PO Charter & Authority | Defines your decision rights, RACI, escalation rules | Confirm what you can decide vs. what you escalate |

**Gate:** Vision + charter confirmed. The vision must be testable against the goals before strategy begins.

### Phase 2: Strategy — "Plan the product."

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 4. Product Discovery & Roadmap | Maps value proposition, builds a Now/Next/Later roadmap with strategic themes | Approve themes and roadmap shape |
| 5. Epic Decomposition | Breaks goals into epics, each with epic-level acceptance criteria | Confirm the epic set is complete and traces to goals |
| 6. Value-Based Prioritization | Applies your chosen model (WSJF / MoSCoW / value-effort), ranks the backlog with recorded rationale | Confirm or override the ordering |
| 7. Release & Increment Slicing | Groups epics into releases, defines MVP/MMP scope and increment readiness | Approve the release plan |

**Gate:** Prioritized ordering + release plan confirmed. Every epic must trace to a product goal.

### Phase 3: Governance — "Set the quality bar."

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 8. Definition of Ready / Done | Drafts DoR and DoD checklists, review cadence, exception process | Confirm the bar matches your product maturity |
| 9. Product Risk & Assumptions | Builds a product-level risk register + assumption log + validation plan | Validate risks and scoring |
| 10. Traceability Spine | Links intent → epic → (story), at minimal or full depth | Confirm traceability depth |

**Gate:** Quality bar appropriate for maturity; traceability verified — every epic traces to a goal.

### Phase 4: Stakeholders & Communication

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 11. Stakeholder Management | Maps power/interest, sets communication cadence and reporting framework | Approve the stakeholder plan |
| 12. Product Documentation | Establishes release-notes governance and changelog framework | Confirm the documentation approach |

**Gate:** Stakeholder map complete; communication cadence agreed.

### Phase 5: Assembly & Handoff

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 13. PBP Assembly & Handoff | Consolidates all artifacts, finalizes `polc-state.md`, writes the package README | Final approval — sets state to `ready` for downstream |

**Gate:** Completeness check passes. `polc-state.md` status = `ready`. AI-DWG can now consume the PBP.

### Phase 6: Operations — "Run the backlog (repeating)."

| Stage | What Happens | When You Re-Enter |
|-------|-------------|-------------------|
| 14. Backlog Operations | Refinement, story splitting, tech-debt trade-offs, stale-item cleanup | Before each sprint/increment |
| 15. Acceptance & Feedback Loop | Accept completed work against DoD, process AI-DLC v1 feedback, reprioritize | After each increment |
| 16. Value & Metrics Engine | Track KPIs and benefits realization against original goals *(opt-in extension)* | Periodically (monthly/quarterly) |

**No terminal gate.** Operations continues for the product's lifetime. Each session ends by persisting `polc-state.md`.

---

## How UX Personas and Journeys Feed Prioritization

If AI-UXD has run, AI-POLC detects `uxd-state.md` and consumes its personas and journeys. This isn't cosmetic — it changes how the backlog is built:

| What AI-UXD Provides | How AI-POLC Uses It |
|----------------------|---------------------|
| **Personas** | Grounds epics in real user needs instead of abstract requirements — every epic answers "which persona, what need" |
| **User journeys** | Validates prioritization against journey pain points — high-friction steps surface as higher-value work |
| **Research findings** | Becomes evidence in the prioritization rationale (data over opinion) |

The flow is also reciprocal: AI-POLC's value goals focus where AI-UXD invests research. If you ran AI-POLC first, point AI-UXD at the goals; if AI-UXD ran first, AI-POLC reads its journeys at Stage 4 (Discovery) and Stage 6 (Prioritization).

---

## Value-Based Prioritization in Practice

At Stage 6 you pick a model and AI-POLC applies it consistently — never improvising the order.

| Model | Pick It When | How It Scores |
|-------|-------------|---------------|
| **WSJF** | Lean/SAFe context, continuous flow | (Business Value + Time Criticality + Risk Reduction) ÷ Job Size |
| **MoSCoW** | Fixed-scope or deadline-driven | Must / Should / Could / Won't |
| **Value-Effort** | Small product, want a fast visual call | Value (1–5) vs. Effort (1–5) quadrants |
| **Custom** | You have an org framework | Your criteria and weights |

**The rule that matters:** every ranking decision carries recorded rationale, logged as a `POLC-D-NNN` decision. Months later, "why is this #1 and that #5?" is always answerable. That traceability is what protects the backlog against loudest-voice and recency-bias prioritization.

---

## DoR / DoD: How the Quality Bar Reaches Developers

The Definition of Ready and Definition of Done you set at Stage 8 don't stay in the PBP — they travel into the development workspace:

```
AI-POLC (DoR/DoD)  ──►  AI-DWG  ──►  Development Workspace
                                      ├── DEFINITION_OF_DONE.md   (DoR + DoD encoded)
                                      ├── testing-strategy.md     (AC format encoded)
                                      └── session-governance.md   (refinement cadence)
```

AI-DWG reads your PBP and encodes the quality bar into workspace steering files. From that point, any AI operating in the workspace (including AI-DLC v1) self-checks stories against your readiness bar and verifies work against your acceptance bar. You define the rule once; it's enforced everywhere downstream. If you later change DoR/DoD, AI-POLC logs a `POLC-C-NNN` change and bumps the version in `polc-state.md` so AI-DWG re-derives.

---

## Tier 2 Story Elaboration — When to Turn It On

By default, AI-POLC stops at the **epic** level (with epic-level acceptance criteria). Story elaboration — INVEST-compliant user stories with Given/When/Then acceptance criteria — is Tier 2, and it's **off by default in chain mode** because AI-DLC v1's Inception phase elaborates stories.

| Your Context | Turn Tier 2 On? |
|--------------|-----------------|
| Chained with AI-DLC v1 (default) | No — let AI-DLC v1 elaborate; avoid duplicate work |
| Standalone, no AI-DLC v1 | Yes — you need stories developers can pick up directly |
| You want PO-quality pre-elaboration before handoff | Yes — say "Elaborate stories for these epics" |

Activating Tier 2 adds story-level outputs to each epic during Stage 5. The guiding principle: don't elaborate twice. Turn it on only when AI-DLC v1 isn't going to do it for you, or when you deliberately want the backlog pre-elaborated.

---

## The Back-and-Forth with AI-DLC v1 During Delivery

AI-POLC and AI-DLC v1 are not a one-shot handoff — they're the only **bidirectional** exchange in the family. This is the rhythm of Phase 6.

```
AI-POLC ──(prioritized epics + DoR/DoD + AC)──►  AI-DLC v1
AI-POLC ◄──(completions, blockers, velocity)───  AI-DLC v1
```

| Direction | What Flows | When |
|-----------|-----------|------|
| **POLC → DLC** | Top-ranked epics, acceptance criteria, priority order | At PBP handoff and after each refinement |
| **DLC → POLC** | Bolt/story completions, blockers, discovered complexity, velocity data | After each increment |

What you do with the return signal in a Stage 15 session:
- **Completion** → update traceability, check increment completeness against DoD, accept or reject
- **Blocker** → reprioritize around it; escalate per your charter if needed
- **Discovered complexity** → split the epic/story, re-estimate
- **Velocity data** → adjust release slicing so the plan stays honest

Because AI-DLC v1 isn't part of this family, the exchange is file-mediated: you bring DLC's output (`aidlc-docs/`) into a POLC session, and AI-POLC's reprioritization reaches DLC through the updated `prioritization-register.md` and a `POLC-C-NNN` change entry that DLC honors at the next bolt boundary.

---

## Choosing Your Depth Level

AI-POLC auto-calibrates, but you can override anytime with "Change depth to X."

| Depth | Best For | What You Get |
|-------|----------|--------------|
| **Minimal** | Simple product, clear scope, few stakeholders | Vision + epics + DoR/DoD + basic release plan |
| **Standard** | Typical complexity, some unknowns — recommended default | Full PBP with all governance artifacts |
| **Comprehensive** | Enterprise, multi-team, heavy compliance | Full traceability, formal risk register, extensions auto-suggested |

---

## What You Get (The Product Backlog Package)

```
{your-output-folder}/
├── polc-state.md                    ← Marker file (chain handoff + session resume; carries projectId)
├── product-vision.md                ← Vision, goals, success metrics
├── po-charter.md                    ← Authority, RACI, decision boundaries
├── roadmap.md                       ← Now/Next/Later + strategic themes
├── epics/                           ← One file per epic
│   ├── EPIC-001_{name}.md
│   ├── EPIC-002_{name}.md
│   └── ...
├── prioritization-register.md       ← Ranked backlog + model + recorded rationale
├── release-plan.md                  ← Release groupings + MVP/MMP scope
├── definition-of-ready.md           ← DoR checklist (flows to AI-DWG)
├── definition-of-done.md            ← DoD checklist (flows to AI-DWG)
├── product-risk-register.md         ← Product-level risks + assumptions
├── traceability-matrix.md           ← Intent → Epic → (Story) links
├── stakeholder-map.md               ← Power/interest + communication plan
├── release-notes-governance.md      ← Release notes + changelog framework
├── PBP_README.md                    ← Package assembly summary
└── management_framework/            ← Governance spine (POLC-* entries)
    ├── MANAGEMENT_FRAMEWORK.md
    ├── Decision_Log.md              ← POLC-D-* (priority/scope decisions)
    ├── Change_Log.md                ← POLC-C-* (DoR/DoD + reprioritization)
    ├── Issue_Log.md                 ← POLC-I-* (blockers, conflicts)
    └── Lessons_Learned.md           ← POLC-L-* (product ownership insights)
```

---

## Tips for Managing a Healthy Backlog

1. **Be honest about depth.** A simple product doesn't need comprehensive governance. Over-governance slows you down more than missing structure does. Start minimal; escalate if reality demands it.

2. **Approve actively at gates.** AI-POLC never auto-progresses. Read each output, correct what the AI missed, then approve. The gates exist so you stay in control of *your* product decisions.

3. **Make every item earn its place.** Nothing enters the backlog without a value justification that traces to a goal. If you can't articulate why an epic matters, it isn't ready — it goes back to refinement, not into the backlog.

4. **Treat the backlog as a living system, not a pile.** Phase 6 is the real job. Re-enter for refinement before each increment, prune stale items, and resist letting the backlog grow unbounded. A healthy backlog is pruned, ranked, and current.

5. **Don't skip traceability.** The intent → epic → story spine is what lets you answer "why did we build that?" a year from now. It's also what makes reprioritization defensible instead of arbitrary.

6. **Use the decision log as your audit trail.** Every significant call lands as a `POLC-D-NNN` entry. When a stakeholder challenges an ordering, you have the rationale on record.

---

## What Happens Next

Your PBP feeds the rest of the chain:

| Next Package | What It Reads from the PBP |
|--------------|----------------------------|
| **AI-DWG** | DoR/DoD, prioritization model, story/release structure → enriches workspace steering and milestones |
| **AI-DLC v1** | Prioritized epics + acceptance criteria → Inception takes the top epic and elaborates it into work |
| **AI-GCE** | (via AI-DWG steering) product quality rules → derives enforcement |

The handoff is automatic — AI-DWG detects `polc-state.md` with status `ready` and reads what it needs. From there, Phase 6 keeps the backlog alive through the bidirectional exchange with AI-DLC v1.

---

## Related Documents

| Document | Location |
|----------|----------|
| How AI-POLC Product Ownership Works | `knowledge_docs/HOW_POLC_PRODUCT_OWNERSHIP_WORKS.md` |
| How to Design User Experience | `knowledge_docs/HOW_TO_DESIGN_USER_EXPERIENCE.md` |
| How to Initiate a Project | `knowledge_docs/HOW_TO_INITIATE_A_PROJECT.md` |
| How to Design Architecture | `knowledge_docs/HOW_TO_DESIGN_ARCHITECTURE.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |

*Knowledge Document | Created: 2026-06-13 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

# How to Initiate a Project

**Purpose:** Practical guide for using AI-PILC to take a raw requirement or idea and transform it into a fully structured Project Initiation Package (PIP) — the foundation that every downstream package depends on.

---

## Who This Is For

Project managers, product owners, or team leads who have a new initiative and need to run it through proper initiation before design and delivery begin. You want structured requirements, stakeholder alignment, risk identification, and a formal charter — not a 200-page waterfall document.

---

## Before You Start

**You need:**
- AI-PILC installed in your AI workspace (see `ai-pilc/setup/INSTALL.md`)
- Some form of input — ANY of the following works:
  - A requirements document (any format)
  - A verbal description or meeting notes
  - An Idea Brief from AI-ILC
  - A brownfield context ("we're extending system X")

**You do NOT need:**
- Perfectly formatted requirements
- A pre-existing charter or scope statement
- Stakeholder buy-in (that's what initiation produces)

---

## The Process (13 Stages, 4 Phases)

### Phase 1: Inception — "What are we working with?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 1. Workspace Detection | AI-PILC checks for existing output, offers resume or fresh start | Confirm: new project or resume |
| 2. Source Ingestion | AI reads your input (document, verbal, ILC brief, or brownfield context) | Provide your requirements in any form |
| 3. Requirement Structuring | AI transforms raw input into structured requirements (functional, non-functional, constraints) | Review and correct the structured output |

**Gate:** Approve that requirements are correctly captured before analysis begins.

### Phase 2: Assessment — "Is this feasible? Who's involved? What could go wrong?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 4. Feasibility Analysis | 5-dimension assessment (technical, financial, operational, schedule, organizational) | Answer feasibility questions, provide constraints |
| 5. Stakeholder Analysis | Identify all stakeholders, their interest/influence, communication needs | Confirm stakeholder list and RACI assignments |
| 6. Risk Assessment | Structured risk identification with probability, impact, and response strategies | Validate risks, approve response strategies |

**Gate:** Approve feasibility conclusion and risk register before planning.

### Phase 3: Planning — "How will we approach this?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 7. Delivery Approach | Select methodology, define phases, estimate timeline | Choose approach (agile/hybrid/waterfall) |
| 8. Resource Planning | Identify team roles, skills needed, capacity requirements | Confirm team structure and availability |
| 9. Budget Estimation | Cost breakdown by category, contingency allocation | Approve budget ranges |
| 10. Quality Planning | Define quality criteria, acceptance standards, review approach | Set quality expectations |

**Gate:** Approve the delivery approach and resource/budget plan.

### Phase 4: Definition — "Let's formalize the boundaries."

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 11. Scope Definition | Explicit IN/OUT boundaries, deliverables list, exclusions | Confirm what's in and what's out |
| 12. Project Charter | Formal document: objectives, constraints, success criteria, authority | Final approval — this is your project's contract |
| 13. Governance Setup | Initialize management framework (6 registers), state file | Confirm governance structure |

**Gate:** Charter approval = project is formally initiated. PIP is complete.

---

## Choosing Your Depth Level

AI-PILC adapts to your needs:

| Depth | Best For | What You Get | Time Investment |
|-------|----------|-------------|-----------------|
| **Minimal** | Small initiatives, proof-of-concepts, internal tools | Core artifacts only (requirements, charter, risk register) | 1 session (45–90 min) |
| **Standard** | Most projects — recommended default | Full 13-stage output with all registers | 2–3 sessions (2–4 hours) |
| **Comprehensive** | Enterprise initiatives, regulated industries, high-risk projects | Extended analysis, detailed stakeholder maps, full governance | 3–5 sessions (4–8 hours) |

Choose at Stage 2 (Source Ingestion). The depth cascades to downstream packages.

---

## Input Modes (Adaptive Intake)

AI-PILC handles whatever you have:

| Input Mode | What You Provide | How AI-PILC Adapts |
|-----------|-----------------|-------------------|
| **Structured document** | Requirements doc, PRD, brief | Parses structure, asks clarifying questions on gaps |
| **Raw/verbal** | Meeting notes, email thread, verbal description | Asks structured questions to extract requirements |
| **ILC brief** | Approved Idea Brief from AI-ILC | Reads evaluation, skips redundant questions |
| **Brownfield** | "We're extending system X" | Focuses on delta requirements, existing constraints, extend-vs-replace decisions |

You don't format your input — AI-PILC meets you where you are.

---

## What You Get (The PIP)

After all 13 stages, your output folder contains:

```
{your-output-folder}/
├── pilc-state.md                    ← Marker file (chain handoff + session resume)
├── 01_Requirement_Intake_Form.md    ← Structured requirements
├── 02_Requirements_Analysis.md      ← Prioritized, categorized requirements
├── 03_Feasibility_Study.md          ← 5-dimension assessment with conclusion
├── 04_Stakeholder_Register.md       ← All stakeholders + RACI
├── 05_Risk_Register.md              ← Identified risks + response strategies
├── 06_Delivery_Approach.md          ← Methodology, phases, timeline
├── 07_Resource_Plan.md              ← Team roles, capacity, skills
├── 08_Budget_Estimate.md            ← Cost breakdown + contingency
├── 09_Quality_Plan.md               ← Quality criteria + acceptance standards
├── 10_Scope_Statement.md            ← Explicit IN/OUT boundaries
├── 11_Project_Charter.md            ← Formal authorization document
├── 12_Communication_Plan.md         ← Stakeholder communication strategy
└── management_framework/            ← Governance registers
    ├── MANAGEMENT_FRAMEWORK.md
    ├── Decision_Register.md
    ├── Change_Register.md
    ├── Issue_Register.md
    ├── Action_Register.md
    ├── Assumptions_Log.md
    └── Lessons_Learned.md
```

---

## Tips for a Smooth Run

1. **Don't over-prepare.** AI-PILC's job is to structure whatever you have. A rough email with 3 bullet points is a valid starting input.

2. **Answer honestly at feasibility.** If something isn't feasible, it's better to know at Stage 4 than at month 6. AI-PILC won't judge — it'll help you scope alternatives.

3. **Use the gates.** Each gate pause is your checkpoint. Read the output, correct misunderstandings, add context the AI missed. The gates exist so you stay in control.

4. **Name stakeholders early.** The richer your stakeholder input at Stage 5, the better the communication plan and RACI. Don't skip people because "they're not important" — influence mapping often reveals hidden decision-makers.

5. **Scope statement is your shield.** Stage 11's explicit IN/OUT boundaries become your defense against scope creep. Be specific about what's excluded.

---

## What Happens Next

Your PIP feeds the next packages in the chain:

| Next Package | What It Reads from PIP |
|-------------|----------------------|
| **AI-ADLC** | Requirements, constraints, charter objectives, risk register, depth level |
| **AI-POLC** | Requirements, stakeholder register, scope statement |
| **AI-UXD** | Requirements, stakeholder register (for personas), scope |
| **AI-PPM** | Charter, budget, timeline (for portfolio roll-up) |

The handoff is automatic — successor packages detect `pilc-state.md` and read what they need.

---

## Related Documents

| Document | Location |
|----------|----------|
| How PILC Workflow Engine Works | `knowledge_docs/HOW_PILC_WORKFLOW_ENGINE_WORKS.md` |
| How Depth Levels Work | `knowledge_docs/HOW_DEPTH_LEVELS_WORK.md` |
| How Gates and Approvals Work | `knowledge_docs/HOW_GATES_AND_APPROVALS_WORK.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |
| Why Project Initiation Matters | `knowledge_docs/WHY_PROJECT_INITIATION_MATTERS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

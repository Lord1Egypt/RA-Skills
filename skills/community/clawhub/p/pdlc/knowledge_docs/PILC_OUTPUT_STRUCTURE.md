# AI-PILC Output Structure — Per-Project PIP & Portfolio Feeding

**Purpose:** Reference document showing what AI-PILC produces and how multiple PIPs feed portfolio governance.

---

## PILC Output Structure — Per-Project PIP

Each time you run AI-PILC against a requirement, it produces a **self-contained Project Initiation Package (PIP)** in the user's chosen output folder. The structure looks like this:

```
{project-output-root}/                         ← One folder per project
│
├── pilc-state.md                    [marker]   ← Workflow state, Project ID, completion status
│                                                  (this is what AI-ADLC & AI-PPM detect)
│
├── 01_Requirement_Intake_Form.md               ← Structured requirements
├── 02_Requirements_Analysis_Report.md          ← Gap/ambiguity analysis (conditional: depth ≥ Standard)
├── 03_Clarification_Questionnaire.md           ← Q&A on gaps (conditional: if critical gaps found)
├── 04_Feasibility_Assessment.md                ← Scored feasibility (Tech/Ops/Financial/Schedule)
├── 05_Business_Case.md                         ← Investment justification + ROM budget
├── 06_Project_Charter.md                       ← Authority, objectives, boundaries
├── 07_Stakeholder_Register.md                  ← People + power/interest grid
├── 08_Scope_Statement.md                       ← In/out scope + WBS + milestones
├── 09_Resource_Plan.md                         ← Team structure + budget breakdown
├── 10_Risk_Register.md                         ← Risks + mitigations + owners
├── 11_RACI_Matrix.md                           ← Governance accountability
├── 12_Kickoff_Agenda.md                        ← Mobilization meeting plan
├── PROJECT_INITIATION_PACKAGE_README.md        ← Final summary + reading guide + quality score
│
└── management_framework/            [shared governance spine]
    ├── MANAGEMENT_FRAMEWORK.md      ← Spine marker + index
    ├── Decision_Log.md              ← All PILC-D-* decisions
    ├── Change_Log.md                ← PILC-C-* scope changes
    ├── Issue_Log.md                 ← PILC-I-* blockers
    ├── Action_Items.md              ← PILC-A-* tasks
    ├── Assumptions_Dependencies.md  ← PILC-ASM-* tracked items
    └── Lessons_Learned.md           ← PILC-LL-* insights
```

> The user picks the deliverable sub-structure at start: **Numbered folders** (like `01_Requirement_Submission/`) or **flat docs** (`pilc-docs/phase/`). The project folder location itself (`projects/PRJ-{ABBREV}-{slug}/pip/`) is fixed and deterministic.

---

## How PILC Feeds Portfolio (Multiple Projects)

The key insight: **PILC runs once per project, producing one PIP each time.** When you have multiple projects, you get multiple PIPs — each with its own `pilc-state.md` carrying a unique **Project ID** (`PRJ-{ABBREV}-{YYYY}-{NNN}`).

```
organization-workspace/
│
├── project-alpha/
│   └── project-initiation/
│       ├── pilc-state.md          ← PRJ-ALPHA-2026-001, Status: Complete
│       ├── 01_Requirement_Intake_Form.md
│       ├── ...all PIP artifacts...
│       └── management_framework/
│
├── project-beta/
│   └── project-initiation/
│       ├── pilc-state.md          ← PRJ-BETA-2026-002, Status: Complete
│       ├── 01_Requirement_Intake_Form.md
│       ├── ...all PIP artifacts...
│       └── management_framework/
│
├── project-gamma/
│   └── project-initiation/
│       ├── pilc-state.md          ← PRJ-GAMMA-2026-003, Status: In Progress
│       └── ...partial PIP...
│
└── portfolio/                      ← AI-PPM consumes ALL completed PIPs
    └── ppm-state.md               ← Scans for pilc-state.md markers
```

### The Chain Flow

```
                    ┌─── PIP (Project Alpha) ──┐
                    │                           │
Raw Requirement ─►  AI-PILC  ─► PIP            ├──► AI-PPM (Portfolio Governance)
                    │                           │        │
                    ├─── PIP (Project Beta)  ───┤        ├─ Cross-project prioritization
                    │                           │        ├─ Resource conflict detection
                    └─── PIP (Project Gamma) ───┘        ├─ Portfolio register
                                                         └─ Strategic alignment scoring
                         │
                         ▼ (per project)
                      AI-ADLC ──► AI-DWG ──► AI-DLC v1 (build)
```

| Aspect | How It Works |
|--------|-------------|
| **Correlation** | Every PIP carries a `Project ID` in `pilc-state.md` — immutable across the entire family chain |
| **Portfolio detection** | AI-PPM scans for `pilc-state.md` files with `Status: Complete` |
| **Per-project progression** | Each PIP independently feeds AI-ADLC for architecture design |
| **Cross-project governance** | AI-PPM reads priority scores, ROM budgets, timelines, and resource needs from multiple PIPs to do portfolio-level analysis |

---

## What Each Deliverable Contains (Quick Reference)

| # | Deliverable | Key Content |
|---|-------------|-------------|
| 01 | Requirement Intake Form | Requestor, business need, functional/non-functional requirements, constraints |
| 02 | Requirements Analysis Report | Gap analysis, ambiguity findings (🔴🟠🟡🟢 categorized) |
| 03 | Clarification Questionnaire | Structured Q&A resolving critical gaps |
| 04 | Feasibility Assessment | Four-dimension score (/100) + MoSCoW + priority rank |
| 05 | Business Case | Problem, solution options, benefits, ROM cost, financial indicators, recommendation |
| 06 | Project Charter | Authority, objectives, success criteria, scope, governance, approval |
| 07 | Stakeholder Register | Power/Interest grid, engagement strategies, RACI preview |
| 08 | Scope Statement | In/out boundaries, WBS, milestones, acceptance criteria |
| 09 | Resource Plan | Team roles, FTE estimates, skill matrix, budget breakdown |
| 10 | Risk Register | Probability × Impact scoring, mitigation strategies, owners |
| 11 | RACI Matrix | Role-to-deliverable accountability mapping |
| 12 | Kickoff Agenda | Meeting structure, pre-reads, objectives, action items |
| README | Package Summary | Quality score (/25), handoff recommendations, open items |

Each file carries provenance front-matter (`generatedBy: AI-PILC`, `ownership: hybrid`) so teams can edit freely while maintaining traceability.

---

## Key Design Principles

| Principle | Detail |
|-----------|--------|
| **One PIP = One Project** | PILC never mixes projects in a single run |
| **Project ID is immutable** | `PRJ-{ABBREV}-{YYYY}-{NNN}` — follows the project through ADLC, DWG, GCE, all the way to delivery |
| **Detection by marker** | Downstream packages find PILC output by scanning for `pilc-state.md`, not by folder name |
| **User owns WHERE** | User picks output location; PILC defines WHAT files exist |
| **Portfolio is additive** | AI-PPM aggregates N completed PIPs — no limit on how many projects feed it |
| **Graceful standalone** | AI-ADLC works without AI-PILC (accepts raw requirements directly); AI-PPM works with as few as 2 PIPs |

*Knowledge Document | Created: 2026-06-11 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

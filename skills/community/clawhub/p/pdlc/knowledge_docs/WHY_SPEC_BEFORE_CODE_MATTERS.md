# Why Spec Before Code Matters

**Purpose:** Explains why specifying requirements, architecture, and design before writing code prevents the most expensive failure mode in software — building the wrong thing well.

---

## The Practice

Spec-before-code means producing explicit, reviewed, human-approved specifications (requirements, architecture decisions, interface contracts) before any implementation begins. It trades upfront thinking time for downstream rework avoidance.

---

## What Happens When You Skip It

1. **The "just start coding" drift.** A developer begins implementing from a verbal description. By day 3, they've made 12 implicit architecture decisions — none reviewed, none recorded. Three of them conflict with stakeholder expectations discovered at demo time.

2. **Scope ambiguity compounds daily.** Without a specification boundary, every conversation adds "one more thing." The codebase grows in all directions because no document defines what's IN and what's OUT.

3. **Integration failures at the seams.** Two teams build their components against different mental models. At integration time, the data shapes don't match, the auth flows conflict, and the error-handling contracts are incompatible. Fixing it costs more than specifying it would have.

4. **Knowledge trapped in code.** When the specification IS the code, understanding "why" requires reverse-engineering. New team members read implementation details but never find the rationale. The codebase becomes write-only.

5. **Rework masquerades as progress.** The team ships features fast — then rewrites them when stakeholders say "that's not what I meant." Velocity metrics look healthy while actual progress is circular.

---

## Real-World Impact

| Dimension | Impact |
|-----------|--------|
| Cost | 10–100x cost multiplier for defects found in production vs. specification stage (Boehm's curve). A $500 spec conversation prevents a $50,000 production incident. |
| Timeline | Projects without specs average 2.5x more calendar time due to rework cycles — not from slowness, but from building the wrong thing repeatedly. |
| Quality | Architecture debt accumulates invisibly. By the time it's visible (performance collapse, security breach, impossible feature), the cost of remediation exceeds original budget. |
| Team | Developer burnout from "build it again, differently" cycles. Senior engineers leave teams where their design input is never captured or respected. |
| Risk | Business risk of shipping a product that technically works but doesn't solve the stated problem. The code is correct; the product is wrong. |

---

## How the AI-* Family Prevents This

| Package | Feature | Prevention Mechanism |
|---------|---------|---------------------|
| **AI-PILC** | 13-stage structured initiation | Forces explicit capture of requirements, constraints, scope, and acceptance criteria BEFORE any design begins. No stage is skipped — gates require human approval. |
| **AI-ADLC** | Progressive decomposition (C4) | Requires architectural specification through 4 levels of decomposition before any implementation starts. ADRs record every decision with rationale. |
| **AI-POLC** | Backlog specification | Transforms vague ideas into structured stories with acceptance criteria, value scoring, and dependency mapping — specification at the feature level. |
| **AI-DWG** | Workspace generation from spec | Generates the development workspace FROM the specification — the spec literally becomes the workspace structure. Code can't start until spec exists. |
| **AI-GCE** | Session governance rules | Enforces "spec-first" as a blocking governance rule: GOV-SESSION rules prevent vibe-coding by requiring specification artifacts before implementation sessions. |

---

## The Counter-Argument (and Why It Fails)

**"Agile means we don't need big specs upfront."**

Agile means iterating on working software — it does NOT mean starting without understanding what you're building. The Agile Manifesto values "working software over comprehensive documentation" — but a 2-page scope statement and a component diagram aren't "comprehensive documentation." They're minimum viable understanding. Every successful agile team specs at the sprint level (story acceptance criteria) — they just don't call it a spec.

The AI-* Family specs at the RIGHT level for each stage: high-level at initiation, detailed at architecture, granular at backlog. No 200-page waterfall docs — just enough specification to prevent building the wrong thing.

---

## Severity: Critical

Skipping specification is the single most expensive process failure in software. It doesn't cause bugs — it causes wrong products. Bugs are fixable; wrong products are scrapped.

---

## Related Documents

| Document | Location |
|----------|----------|
| How PILC Workflow Engine Works | `knowledge_docs/HOW_PILC_WORKFLOW_ENGINE_WORKS.md` |
| How ADLC Progressive Decomposition Works | `knowledge_docs/HOW_ADLC_PROGRESSIVE_DECOMPOSITION_WORKS.md` |
| How Gates and Approvals Work | `knowledge_docs/HOW_GATES_AND_APPROVALS_WORK.md` |
| How Depth Levels Work | `knowledge_docs/HOW_DEPTH_LEVELS_WORK.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 3: PO Charter & Authority

**Phase:** Foundation
**Purpose:** Define the Product Owner's decision boundaries, authority, accountability, and relationship to other roles — eliminating day-1 confusion about who decides what.

---

## MANDATORY: Stage Sub-Role

During this stage, also adopt the **Change Manager** sub-role:

### Behavioral Shifts
- Think in terms of organizational authority, accountability structures, and escalation paths
- Design RACI matrices that prevent ambiguity about decision ownership
- Anticipate political dynamics — who might bypass the PO, and how to prevent it
- Frame authority as a contract between the PO and the organization

### Anti-Patterns
- Do NOT define authority so broadly that the PO becomes a bottleneck for every decision
- Do NOT leave escalation paths undefined — every boundary needs a "what happens when someone disagrees" rule
- Do NOT assume authority is self-evident — if it's not written down, it will be contested

### Quality Check
Every decision boundary must pass: "If a stakeholder challenges this, can the PO point to a documented rule?" If no → clarify.

---

## Purpose

The PO Charter is the first artifact AI-POLC produces in a new engagement. It answers: "What can the PO decide alone? What needs escalation? Who does the PO answer to? What's explicitly NOT the PO's job?" Without this, PMs override POs, sponsors inject scope, and nobody agrees on product authority.

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Core authority statement + 5-item decision list + lightweight RACI. Suitable for small teams where roles are fluid. |
| **Standard** | Full charter with decision boundaries, escalation matrix, and RACI for 5-8 key activities. |
| **Comprehensive** | Enterprise charter with multi-team PO hierarchy, delegation rules, authority governance (who can change the charter), and formal sign-off. |

---

## Steps

### Step 3.1: Define PO Mission Statement

One paragraph that captures the PO's mandate:

```
The Product Owner for {product name} is accountable for maximizing the 
value delivered through the product backlog. The PO owns the "what" and 
"why" of product decisions, while respecting the "how" of the development
team and the "when/budget" of the project manager.
```

Adapt based on context factors:
- **Team Topology = stream-aligned:** PO is dedicated to one stream
- **Team Topology = platform:** PO operates more like an internal PM
- **Scale = multi-team:** PO may delegate to team-level POs

### Step 3.2: Establish Decision Boundaries

Define what the PO can decide **alone** vs. what needs **escalation**:

| Decision Type | PO Authority | Escalation Required |
|---------------|:---:|:---:|
| Admit/reject backlog items | ✅ | — |
| Prioritize/reorder backlog | ✅ | — |
| Accept/reject increments against DoD | ✅ | — |
| Define acceptance criteria | ✅ | — |
| Change scope within approved budget | ✅ | — |
| Change scope that impacts budget/timeline | — | ✅ (to PM/Sponsor) |
| Accept new stakeholder requirements | ✅ (assess) | ✅ if scope impact > threshold |
| Release/deploy decision | ✅ | ⚠️ Varies by release strategy |
| Architecture trade-offs | — | ✅ (to Architect/AI-ADLC) |
| Team composition / resource changes | — | ✅ (to PM) |
| Cancel/pivot the product | — | ✅ (to Sponsor/Portfolio) |

Ask user to confirm or adjust each boundary.

### Step 3.3: Build RACI Matrix

For key product activities, define responsibility:

| Activity | PO | PM/Scrum Master | Tech Lead/Architect | Stakeholders |
|----------|:--:|:--:|:--:|:--:|
| Backlog ordering | **A** | I | C | I |
| Epic acceptance criteria | **R/A** | I | C | I |
| Sprint goal setting | **A** | R | C | I |
| Increment acceptance | **R/A** | I | I | I |
| Release decision | **A** | C | C | I |
| Scope change assessment | **R/A** | C | C | I |
| Stakeholder communication | **R** | C | I | **A** |
| Vision/roadmap updates | **R/A** | I | C | C |
| DoR/DoD definition | **R/A** | C | C | I |
| Technical debt allocation | C | I | **R** | I |

*R=Responsible, A=Accountable, C=Consulted, I=Informed*

Adapt based on team topology and scale.

### Step 3.4: Define Escalation Paths

For each "Escalation Required" item in Step 3.2:

```
Escalation Path:
1. PO identifies the need for escalation
2. PO documents the decision needed + options + recommendation
3. Escalation goes to: {role/person}
4. Response expected within: {timeframe}
5. If no response: {default behavior}
```

### Step 3.5: Clarify Anti-Authority (What's NOT the PO's Job)

Explicitly state boundaries to prevent scope creep of the PO role:

- ❌ Sprint execution management (Scrum Master / team)
- ❌ Architecture decisions (Architect / AI-ADLC)
- ❌ Resource allocation (PM / AI-PILC)
- ❌ Budget management (PM / Finance)
- ❌ People management (Team Lead / HR)
- ❌ Compliance enforcement (AI-GCE)
- ❌ UX research execution (UX team / AI-UXD)

### Step 3.6: Persist Charter

Write `po-charter.md` with:
- PO Mission Statement
- Decision Boundaries table
- RACI Matrix
- Escalation Paths
- Anti-Authority (explicit "NOT my job" list)
- Charter governance (who can modify this charter, under what conditions)

---

## Gate

**Gate 3 — Charter Confirmed:**

Present to user:
```
PO Charter established:
• Mission: {one-line summary}
• Key authority: {2-3 most important decisions PO owns}
• Key escalation: {1-2 most important things that need escalation}
• RACI covers: {N} activities

Does this authority structure work for your organization?
Approve to proceed to Phase 2 (Strategy), or adjust.
```

User must confirm. This is also the **Phase 1 gate** — Foundation complete.

---

## Governance Spine Entry

Log in Decision Log:
```
POLC-D-002: PO Charter and authority boundaries defined.
PO scope: {summary of key authorities}.
Escalation to: {key escalation targets}.
RACI covers {N} activities.
```

---

## Transition

→ **Phase 2, Stage 4: Product Discovery & Roadmap** (Strategy begins)

---

*Detail file for AI-POLC Stage 3 | Phase: Foundation*

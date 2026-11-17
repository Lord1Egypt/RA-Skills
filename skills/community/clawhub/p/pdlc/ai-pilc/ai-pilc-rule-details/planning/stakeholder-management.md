<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stakeholder Management

## Stage: 10 of 16
## Phase: 🟢 PLANNING
## Execution: ALWAYS

---

## Purpose

Identify all stakeholders who influence or are affected by the project, classify them by power and interest, and define engagement strategies for each group. This register becomes the foundation for communication planning (Stage 14) and ensures no critical stakeholder is overlooked during execution.

---

## MANDATORY: Stage Sub-Role — Change Manager

During THIS stage, ALSO adopt the mindset of a **Change Manager**. This does NOT replace your primary role (PMO Professional / Senior Project Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Map not just who stakeholders are, but how each EXPERIENCES the change (winners, losers, neutral)
- Identify resistance sources early and pair each with a mitigation or engagement strategy
- Tailor the engagement approach per power/interest quadrant — one size does not fit all
- Read the informal influence map, not just the org chart

### Anti-Patterns for This Stage
- Do NOT treat the stakeholder register as a static list — it's the basis of an engagement strategy
- Do NOT overlook stakeholders who lose something in the change — they drive resistance

### Quality Check
A good output at this stage sounds like:
- "Group B loses their current workflow — high resistance risk; mitigation: early involvement + transition support; engagement: weekly 1:1 with their lead..."

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Simple stakeholder register (names, roles, category). No formal matrix or engagement plan. Suitable for <5 stakeholders. |
| **Standard** | Full register + Power/Interest matrix + engagement strategy per quadrant. Suitable for 5-15 stakeholders. |
| **Comprehensive** | Detailed register + Power/Interest matrix + individual engagement plan per high-power stakeholder + influence mapping + stakeholder risk analysis. Suitable for >15 stakeholders. |

---

## Step-by-Step Execution

### Step 1: Identify Stakeholders

#### Source 1: Extract from Prior Artifacts

Scan all prior deliverables for named individuals and roles:

| Source | What to Extract |
|--------|----------------|
| Requirement Intake Form (Stage 3) | Requestor, named stakeholders, approval roles |
| Business Case (Stage 8) | Sponsor, finance approver, beneficiaries |
| Project Charter (Stage 9) | Signatories, steering committee, PM, Tech Lead |
| Decision Log | Decision makers referenced |
| Action Items | Owners assigned |

#### Source 2: Infer from Project Context

Based on project type and complexity, identify likely stakeholder roles not yet named:

| Category | Common Roles to Consider |
|----------|-------------------------|
| **Executive** | Sponsor, Budget Owner, Portfolio Manager, CxO |
| **Delivery** | Project Manager, Technical Lead, QA Lead, DevOps Lead, UX Lead |
| **Business** | Product Owner, Business Analyst, Subject Matter Experts, Process Owners |
| **Operations** | Infrastructure Lead, Support Manager, Change Manager, Training Lead |
| **Governance** | PMO, Finance, Legal/Compliance, Security, Audit |
| **External** | Vendors, Partners, Regulators, Client representatives |
| **End Users** | User group representatives, Union/staff representatives, Pilot users |

#### Source 3: Ask the User

```markdown
### Q-PLN-01: Additional Stakeholders

**Context:** I've identified {n} stakeholders from the project documents so far. There may be others I'm not aware of.

**Currently identified:**
{Bulleted list of names/roles found}

**Questions:**
1. Are there additional stakeholders I should include?
2. Are any of the above incorrect or no longer relevant?
3. Are there external parties (vendors, partners, regulators, clients) involved?

**Your input:** _[Add, remove, or confirm the list]_
```

---

### Step 2: Classify Stakeholders

For each identified stakeholder, capture:

```markdown
## Stakeholder Register

| # | Name | Role/Title | Department | Category | Project Role |
|---|------|-----------|------------|:--------:|--------------|
| 1 | {Name or TBD} | {Title} | {Dept} | {Internal/External} | {Their role on THIS project} |
```

**Category values:** Internal, External, Partner, Regulatory

**Project Role** — their function relative to the project (not their org title):
- Project Sponsor
- Product Owner / Requestor
- Decision Maker
- Subject Matter Expert
- Technical Authority
- Delivery Team Member
- User Representative
- Governance / Oversight
- Support / Enabler
- Impacted Party (affected but not involved)

---

### Step 3: Assess Power and Interest

For each stakeholder, assess:

**Power (ability to influence the project):**
| Level | Definition |
|:-----:|-----------|
| High | Can approve/block decisions, allocate/withdraw budget or resources, override scope |
| Medium | Can influence decisions through expertise or organizational position; escalation target |
| Low | Limited ability to change project direction; affected by outcomes but doesn't control them |

**Interest (degree of involvement/concern):**
| Level | Definition |
|:-----:|-----------|
| High | Actively engaged; project outcomes directly affect their objectives/work; wants involvement |
| Medium | Interested in outcomes; periodic engagement appropriate; affected but not daily |
| Low | Minimal concern with project details; informed of outcomes only; tangentially affected |

---

### Step 4: Map to Power/Interest Matrix

```markdown
## Power/Interest Matrix

```
              HIGH POWER
              ┌───────────────────────────┬───────────────────────────┐
              │                           │                           │
              │     KEEP SATISFIED        │     MANAGE CLOSELY        │
              │                           │                           │
              │  • {Name — Role}          │  • {Name — Role}          │
              │  • {Name — Role}          │  • {Name — Role}          │
              │                           │  • {Name — Role}          │
              │                           │                           │
              ├───────────────────────────┼───────────────────────────┤
              │                           │                           │
              │        MONITOR            │     KEEP INFORMED         │
              │                           │                           │
              │  • {Name — Role}          │  • {Name — Role}          │
              │                           │  • {Name — Role}          │
              │                           │  • {Name — Role}          │
              │                           │                           │
              └───────────────────────────┴───────────────────────────┘
              LOW INTEREST                          HIGH INTEREST
```
```

---

### Step 5: Define Engagement Strategies

#### Per-Quadrant Strategy

| Quadrant | Strategy | Communication Approach |
|----------|----------|----------------------|
| **Manage Closely** (High Power, High Interest) | Active engagement; involve in decisions; regular 1:1 updates | Weekly/bi-weekly direct engagement; steering committee membership; early involvement in gate decisions |
| **Keep Satisfied** (High Power, Low Interest) | Keep informed at high level; don't overwhelm with detail; engage when their domain is affected | Monthly summary; escalation when their authority needed; present at major milestones only |
| **Keep Informed** (Low Power, High Interest) | Regular updates; leverage their enthusiasm and expertise; good source of feedback | Regular comms (newsletter/status); invite to demos/reviews; encourage input on their domain |
| **Monitor** (Low Power, Low Interest) | Minimal effort; inform of major outcomes only | Include in broad announcements; no active engagement unless their interest changes |

#### Individual Engagement Plan (Comprehensive depth only)

For each "Manage Closely" stakeholder:

```markdown
### {Name} — {Role}

| Attribute | Detail |
|-----------|--------|
| Power | High |
| Interest | High |
| Influence Style | {Rational/Political/Relationship-driven/Data-driven} |
| Key Concern | {What they care most about — budget? timeline? quality? political?} |
| Communication Preference | {1:1 meetings / Email / Dashboard / Formal reports} |
| Engagement Frequency | {Weekly / Bi-weekly / At milestones} |
| Potential Resistance | {What might cause them to oppose or disengage} |
| Mitigation | {How to address resistance proactively} |
| Relationship Owner | {PM / Sponsor / PO — who manages this relationship} |
```

---

### Step 6: Stakeholder Risk Analysis (Comprehensive depth only)

Identify stakeholder-related risks:

| Risk | Stakeholder(s) | Impact | Mitigation |
|------|---------------|:------:|-----------|
| Key decision-maker unavailable during gate reviews | {Name} | Schedule delay | Delegation authority defined; 4-week advance notice |
| Stakeholder conflict between {A} and {B} | {Names} | Scope disputes | Clear RACI; Sponsor as arbiter |
| External stakeholder disengages | {Name} | Integration risk | Regular touchpoints; escalation path |
| User group resistance to change | {Group} | Adoption failure | Early involvement; champions network |
| Sponsor attention diverted | {Name} | Decisions stall | Deputy sponsor identified; async approval option |

Log relevant risks to the Risk Register (or note for Stage 13 if not yet produced).

---

### Step 7: Produce the Stakeholder Register Document

Using template `templates/stakeholder-register.md`, compile:

1. **Section 1: Stakeholder Register** — Full table of all stakeholders
2. **Section 2: Power/Interest Matrix** — ASCII visual + placement detail table
3. **Section 3: Engagement Strategy** — Per-quadrant approach
4. **Section 4: Individual Plans** (Comprehensive only) — Key stakeholder profiles
5. **Section 5: Stakeholder Risks** (Comprehensive only) — Risk table

---

### Step 8: Present for Review

```markdown
## Review: Stakeholder Register — {project_name}

I've produced the Stakeholder Register. Key highlights:

- **Total stakeholders identified:** {n}
- **Manage Closely (High/High):** {n} — {names}
- **Keep Satisfied (High/Low):** {n}
- **Keep Informed (Low/High):** {n}
- **Monitor (Low/Low):** {n}
- **Unassigned roles (TBD):** {n}

**Key relationships:**
- Sponsor: {name}
- Product Owner: {name}
- Technical authority: {name or TBD}

**Full document:** Saved to `{file_path}`

---

**Your response:**
- (a) **Approve** — Register is complete; proceed to next planning stage
- (b) **Add stakeholders** — I have additional names/roles to include
- (c) **Adjust classifications** — Power/Interest assignments need correction
- (d) **Challenge strategy** — Engagement approach needs modification
```

---

### Step 9: Iterate and Finalize

If changes requested:
1. Apply additions/modifications
2. Recalculate matrix placement if power/interest changed
3. Update engagement strategies if needed
4. Re-present summary
5. Repeat until approved

---

### Step 10: Log and Transition

1. **Decision Log:** D-{nnn}: "Stakeholder Register approved. {n} stakeholders identified. Key relationship: Sponsor = {name}."
2. **State File:** Stage 10 = ✅ Done; Current Stage = 11
3. **Assumptions Register:** ASM-{nnn}: "All identified stakeholders are available for engagement per stated strategy."
4. **Action Items:** For any `_[TBD]_` roles: A-{nnn}: "Identify and onboard {role}" — Owner: {PM/Sponsor}

Display:

```
✅ Stage 10: Stakeholder Management — Complete

👥 Stakeholders: {n} identified ({m} in "Manage Closely" quadrant)
📄 Saved to: {file_path}

Next → Stage 11: Scope Definition
```

---

## Output File

Save to:
- Numbered: `{output_root}/05_Stakeholder_Management/Stakeholder_Register.md`
- Flat: `{output_root}/pilc-docs/planning/Stakeholder_Register.md`

---

## Common Pitfalls

| Pitfall | Prevention |
|---------|-----------|
| Only identifying positive stakeholders | Deliberately consider: who might oppose this? who loses power/budget? |
| Forgetting end users | The people who USE the deliverable are stakeholders even if they have no project role |
| Treating all stakeholders the same | Matrix exists precisely to differentiate engagement effort |
| Static register | Register should be reviewed at every phase gate — stakeholder field changes |
| Missing external parties | Consider vendors, partners, regulators, clients, unions, auditors |
| Conflating interest with support | "High Interest" doesn't mean supportive — it means engaged (could be opposed) |

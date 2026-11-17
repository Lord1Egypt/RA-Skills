<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 11: Stakeholder Management

**Phase:** Stakeholders & Communication
**Purpose:** Map stakeholders, define communication cadence, and establish the PO's reporting framework — ensuring the right people get the right information at the right time.

---

## MANDATORY: Stage Sub-Role

During this stage, also adopt the **Change Manager** sub-role:

### Behavioral Shifts
- Think in terms of influence, interest, and communication needs — not just names on a list
- Design communication to prevent scope bypass (stakeholders going around the PO)
- Balance transparency (keeping people informed) with efficiency (not over-communicating)
- Anticipate political dynamics: who might resist, who champions, who has veto power

### Anti-Patterns
- Do NOT create a stakeholder register with no communication plan — names without actions are useless
- Do NOT treat all stakeholders the same — power/interest determines approach
- Do NOT ignore "silent" stakeholders — low interest today can become high interest when their area is affected

### Quality Check
Every stakeholder must pass: "Do I know what this person needs from me, how often, and in what format?" If no → communication gap.

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Simple list: name, role, interest level, communication frequency. 3-5 stakeholders. |
| **Standard** | Power/interest matrix. Communication plan per quadrant. Demo/review framing. |
| **Comprehensive** | Full stakeholder analysis with engagement strategies, resistance management, feedback collection process, leadership reporting templates. |

---

## Steps

### Step 11.1: Identify Stakeholders

Sources:
- PIP Stakeholder Register (if chain mode — already exists)
- User input (who cares about this product?)
- Implied stakeholders (end users, support team, operations, compliance)

For each stakeholder, capture:

| Name/Role | Interest In | Power | Interest | Current Stance |
|-----------|------------|:---:|:---:|:---:|
| {Sponsor} | Budget, ROI, timeline | High | High | Champion |
| {Dev Lead} | Technical feasibility, team capacity | Medium | High | Supportive |
| {End Users} | Usability, value | Low | High | Unknown |
| {Compliance Officer} | Regulatory adherence | High | Low | Neutral |

### Step 11.2: Build Power/Interest Matrix (Standard+)

```
              HIGH POWER
         ┌─────────────────────┐
         │  MANAGE CLOSELY     │  KEEP SATISFIED
         │  (High Power,       │  (High Power,
         │   High Interest)    │   Low Interest)
         │  → Regular updates  │  → Periodic summary
         │  → Involve in       │  → Escalation path
         │    decisions        │  → Don't overwhelm
         ├─────────────────────┤
         │  KEEP INFORMED      │  MONITOR
         │  (Low Power,        │  (Low Power,
         │   High Interest)    │   Low Interest)
         │  → Demo invites     │  → General announcements
         │  → Feedback channel │  → Available if they ask
         │  → Status updates   │
         └─────────────────────┘
              LOW POWER
         HIGH INTEREST ←────→ LOW INTEREST
```

Place each stakeholder in a quadrant. This determines their communication approach.

### Step 11.3: Define Communication Plan

For each quadrant:

| Quadrant | Communication Type | Frequency | Format | Owner |
|----------|-------------------|-----------|--------|:---:|
| Manage Closely | Status + decision requests | Weekly / per sprint | 1:1 or steering meeting | PO |
| Keep Satisfied | Executive summary | Bi-weekly / per release | Written report | PO |
| Keep Informed | Progress updates + demos | Per sprint | Demo invite + notes | PO + SM |
| Monitor | General announcements | Per release | Newsletter / changelog | PO (delegatable) |

### Step 11.4: Define Demo/Review Framing

How the PO presents work to stakeholders:

```
Sprint/Increment Review Format:
1. Goal reminder: "This sprint we aimed to {goal}"
2. What was delivered: {demo of working increment}
3. What was learned: {feedback, surprises, pivots}
4. Acceptance decision: {accept/iterate/concerns}
5. What's next: {next priority from the backlog}
6. Ask: {any decisions needed from stakeholders}
```

Adapt format by stakeholder type:
- Executive: focus on outcomes and metrics (2 minutes)
- Technical: focus on what was built and trade-offs (5 minutes)
- Users: focus on what they can now do (hands-on demo)

### Step 11.5: Define Feedback Collection Process

How stakeholders provide input back to the PO:

| Channel | For | Cadence | How PO Processes |
|---------|-----|---------|-----------------|
| Sprint review feedback | Feature reactions | Per sprint | Captured → backlog assessment |
| Stakeholder 1:1 | Strategic input, concerns | Per sprint/monthly | Captured → decision or change log |
| User feedback (support tickets, analytics) | Usability, bugs, requests | Continuous | Triaged → backlog or risk register |
| Formal change request | Scope changes | As needed | Via AI-PILC change management |

### Step 11.6: Persist Stakeholder Map

Write `stakeholder-map.md` with:
- Stakeholder register (name/role, power, interest, stance)
- Power/interest matrix (visual or table)
- Communication plan (per quadrant)
- Demo/review format
- Feedback collection channels
- Escalation paths (from PO Charter — cross-reference)

---

## Gate

**Gate 11 — Stakeholder Map Confirmed:**

Present to user:
```
Stakeholder management established:
• Stakeholders mapped: {N}
• Manage Closely: {N} | Keep Satisfied: {N} | Keep Informed: {N} | Monitor: {N}
• Communication cadence: defined per quadrant
• Demo format: defined
• Feedback channels: {N} channels

Does this cover everyone who has a stake in the product?
Approve to proceed to Product Documentation.
```

User must confirm before proceeding.

---

## Transition

→ **Stage 12: Product Documentation** (Stakeholders continues)

---

*Detail file for AI-POLC Stage 11 | Phase: Stakeholders & Communication*

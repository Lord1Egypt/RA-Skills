# Project Implementation Management (Project Implementation & PMO)

## Objectives

Manage the execution of IT projects, ensuring successful delivery within the four constraints of scope / time / budget / quality, and establish effective project governance and risk management mechanisms.

---

## Prerequisites
- Project charter has been approved
- Project plan has been developed
- Team has been assembled
- Vendor contracts have been signed (if applicable)

## Inputs
- Project charter and plan
- Contract / SOW
- Budget and resource plan
- Risk management plan

---

## Operation Steps

### Step 1: Establish Project Governance

#### 1.1 Project Governance Structure

Any large IT project must have three tiers of governance:

```
┌─────────────────────────────────────────────┐
│  Strategic: Steering Committee               │
│  Members: Sponsor (CIO + Business VP) + PM   │
│           + Vendor Executive                 │
│  Frequency: Monthly (1-2 hours)              │
│  Decisions: Budget adjustments / Scope       │
│             changes / Major issue arbitration │
├─────────────────────────────────────────────┤
│  Tactical: Project Core Team                 │
│  Members: PM + Tech Lead + Business Lead     │
│           + Vendor PM                        │
│  Frequency: Weekly (1 hour)                  │
│  Decisions: Schedule management / Risk       │
│             response / Resource coordination │
├─────────────────────────────────────────────┤
│  Execution: Delivery Teams                   │
│  Members: Developers / Testers / BAs /       │
│           Business representatives           │
│  Frequency: Daily stand-up (15 min)          │
│  Decisions: Day-to-day technical decisions / │
│             Task assignment / Blocker removal│
└─────────────────────────────────────────────┘
```

#### 1.2 RACI Matrix (Core Activities)

| Activity | Sponsor | PM | Tech Lead | Business Lead | Vendor | Team |
|----------|---------|----|-----------|---------------|--------|------|
| Project plan approval | A | R | C | C | C | I |
| Requirements sign-off | A | R | C | R | I | C |
| Scope change | A | R | C | C | C | I |
| Technical solution approval | I | A | R | I | C | C |
| Milestone acceptance | A | R | R | R | C | I |
| Budget approval | A | R | I | I | I | I |
| Risk response (project-level) | I | R | C | C | C | I |

*R=Responsible (executes), A=Accountable (ultimately answerable), C=Consulted (must be consulted), I=Informed (must be informed)*

---

### Step 2: Project Planning & Tracking

#### 2.1 Project Plan Hierarchy

```
Milestone Plan — For SteerCo / Management
├── M1: [Date] Requirements sign-off complete
├── M2: [Date] Detailed design complete
├── M3: [Date] Development complete
├── M4: [Date] Testing complete
├── M5: [Date] UAT complete
├── M6: [Date] Go-live
└── M7: [Date] Post-go-live stabilization period ends

Phase Plan — For Project Core Team
├── Each phase broken down into specific work packages
├── Each work package has an owner + deadline + dependencies
└── Rolling-wave: next 2-4 weeks detailed, remainder kept at outline level

Sprint / Iteration Plan — For Delivery Teams
├── 2-week sprints (or per project methodology)
├── Each sprint has a clear Sprint Goal
└── Sprint Review + Retrospective
```

#### 2.2 Progress Tracking

**5 Metrics to Review Weekly:**

| Metric | How to Calculate | Green | Yellow | Red |
|--------|-----------------|-------|--------|-----|
| SPI (Schedule Performance Index) | EV/PV | >0.95 | 0.85-0.95 | <0.85 |
| Completion Rate | Completed work / Total work | >proportional to time | Slightly below | Significantly below |
| Milestone Achievement | On-time completions / Planned completions | 100% | 80%+ | <80% |
| Critical Path Float | Latest start - Earliest start | >2 weeks | 0-2 weeks | <0 (delayed) |
| Unresolved Blockers | Tasks blocked >3 days | 0 | 1-2 | >2 |

#### 2.3 Status Report

**One-Page Weekly Status Report:**
```
Project: [Name] | Reporting Period: [Date] | PM: [Name]

Overall Status: 🟢On Track / 🟡At Risk / 🔴Off Track

Completed This Week (Top 3-5):
✅ [Completed item 1]
✅ [Completed item 2]

Planned Next Week (Top 3-5):
➤ [Planned item 1]
➤ [Planned item 2]

Key Risks / Issues (Top 3):
⚠️ [Risk/Issue] — [Impact] — [Response] — [Owner] — [Expected Resolution Date]

Help Needed (Escalation):
🆘 [Who needs to make what decision / take what action] — [Deadline]

Key Metrics:
  Schedule: [X]% complete (planned [X]%)
  Budget: Spent $[X]M / Total Budget $[Y]M ([X]%)
  Resources: [X]/[Y] people
  Key Milestones: M1✅ M2✅ M3➤(on track) M4⚠️(at risk)
```

---

### Step 3: Risk & Issue Management

#### 3.1 Risk vs Issue

| | Risk | Issue |
|---|---|---|
| Definition | May happen, but hasn't happened yet | Has already happened |
| Management Action | Prevention + Mitigation | Resolution + Escalation |
| Management Tool | Risk Register | Issue Log |
| Frequency | Bi-weekly to Monthly Review | Daily Tracking |

#### 3.2 Risk Register

| ID | Risk Description | Probability | Impact | Level | Response Strategy | Owner | Review Date | Status |
|----|-----------------|-------------|--------|-------|-------------------|-------|-------------|--------|
| R1 | Key technical staff departure | M | H | 🔴 | Build backup + mandatory documentation + retention bonus | PM | 6/15 | Monitoring |
| R2 | Vendor delivery delay | M | H | 🔴 | Contract penalties + weekly delivery review + backup vendor | Procurement | 6/15 | Monitoring |
| R3 | Data migration quality issues | H | M | 🟡 | Automated data quality checks + early migration + rollback plan | Tech Lead | 7/1 | Monitoring |
| R4 | Insufficient business-side UAT participation | M | M | 🟡 | Lock in business-side time in advance + include UAT in their KPIs | Business Lead | 8/1 | Monitoring |

**Risk Response Strategies:**
- **Avoid**: Change the approach so the risk does not occur (e.g. don't use that technology)
- **Mitigate**: Reduce probability or impact (e.g. add backup)
- **Transfer**: Shift to another party (e.g. buy insurance / outsource / contract penalties)
- **Accept**: Acknowledge the risk but decide to accept it (must be documented + management acknowledged)

#### 3.3 Issue Escalation Path

```
Issue discovered →
├── Can the project team resolve it? → Resolve + Document
├── Needs cross-team coordination? → PM coordinates; escalate to Core Team if unresolved within 3 days
├── Needs budget / scope / schedule adjustment? → Core Team discussion → SteerCo decision
└── Project-level crisis (major delay / overrun / security incident) → Escalate to Sponsor within 24 hours
```

---

### Step 4: Quality Management

#### 4.1 Quality Assurance (QA) vs Quality Control (QC)

| | Quality Assurance (QA) | Quality Control (QC) |
|---|---|---|
| Focus | Process | Product |
| Question | "Are we doing it the right way?" | "Is what we built correct?" |
| Activities | Process audits / Best practices / Standards | Testing / Reviews / Inspections |
| Timing | Continuous | At key checkpoints |

#### 4.2 Quality Gates

Set quality checks at the following checkpoints:

```
Gate 1: Requirements Review
□ Are requirements complete, consistent, and testable?
□ Are non-functional requirements (performance / security / availability) clearly defined?
□ Have stakeholders signed off?

Gate 2: Design Review
□ Does the design meet the requirements?
□ Does it follow architecture standards?
□ Is technical debt clearly documented with a repayment plan?

Gate 3: Code / Development Complete
□ Code review rate >90%?
□ Unit test coverage >70%?
□ Security scan (SAST) shows no high-severity vulnerabilities?

Gate 4: Testing Complete
□ All test cases executed?
□ Critical bugs = 0, High bugs <5?
□ Performance testing passed (meets NFRs)?

Gate 5: UAT Complete
□ Business-side sign-off obtained?
□ Training completed (>80% of target audience)?
□ Go-live checklist all checked?

Gate 6: Go-Live
□ Deployment steps documented?
□ Rollback plan verified?
□ Monitoring / Alerting configured?
□ Support team in place?

Gate 7: Post-Go-Live Stabilization
□ 7 consecutive days without P1/P2 incidents?
□ Key metrics (KPIs) meeting expectations?
□ Knowledge transfer completed?
```

---

### Step 5: Scope & Change Management

#### 5.1 Change Request (CR) Process

```
Anyone raises a change request
  ↓
PM records in change log
  ↓
PM + Tech Lead + Business Lead conduct initial impact assessment (24-48 hours)
  ↓
     Impact assessment: Schedule (+/- X days) + Cost (+/- $X) + Quality / Risk
  ↓
├── Minor impact (schedule impact <1 week + cost <$X) → PM can approve
├── Medium impact → Core Team review + Sponsor informed
└── Major impact (schedule impact >2 weeks or cost >$X) → SteerCo approval
  ↓
Approved? → Update plan + budget + scope documents + notify all affected parties
Rejected? → Document reason + inform requester
```

#### 5.2 Scope Creep Prevention

Scope creep = the project scope gradually and quietly expands while budget and timeline do not.

| Prevention Measure | Description |
|-------------------|-------------|
| Explicit "Out of Scope" list | Project scope must also state "what is NOT included" |
| Every CR has a cost | Not "let's just do this on the side" — it's "this requires an additional $X + Y days" |
| Monthly scope review | Review with SteerCo: "Are we still doing what we committed to do?" |
| Learn to say no | The PM's most important phrase: "That's a great idea — we can put it in Phase 2" |

---

### Step 6: Vendor Management (Day-to-Day)

#### 6.1 Vendor Performance Tracking

| Dimension | Measurement | Green | Red |
|-----------|------------|-------|-----|
| Delivery Quality | Defect density / Rework rate | Within agreed standards | Exceeds standards |
| Delivery Timeliness | % tasks delivered per plan | >90% | <70% |
| Responsiveness | Issue response / resolution time | Within SLA | Frequently exceeds SLA |
| Team Stability | Key personnel changes | No changes | Frequent changes |
| Communication & Collaboration | Subjective assessment | Satisfied | Unsatisfied |

#### 6.2 Vendor Weekly Meeting

```
Agenda (30 minutes):
1. What was completed last week? (Vendor) — 10 min
2. What is planned for next week? (Vendor) — 5 min
3. Any blockers / what does the client need to do? (Vendor) — 5 min
4. Quality / Performance issue discussion — 5 min
5. Other / Action item review — 5 min

Output: Meeting minutes (within 24 hours) + updated action item list
```

---

## Outputs
1. **Project Governance Structure**: SteerCo + Core Team + Team structure
2. **Project Plan**: Milestone plan + Phase plan + Sprint plan
3. **Status Report Template**: Weekly report + Monthly report (SteerCo)
4. **Risk Register**: Continuously updated
5. **Quality Gate Checklist**: Pass criteria for each gate
6. **Change Request Log**: Record and decision for all CRs

---

## Quality Checklist
- [ ] Three-tier governance structure is clear; SteerCo has held its first meeting
- [ ] Project plan is not "written once and never looked at again" — updated regularly
- [ ] Risk register is alive (not written once at the start and never opened again)
- [ ] Quality gates have clear pass / fail criteria
- [ ] Change management process is known to the team and is being followed
- [ ] Vendor performance has data behind it (not "feels about right")

---

## Common Pitfalls

| Pitfall | Why It's Wrong | Correct Approach |
|---------|---------------|------------------|
| PM as messenger | "Business says they need it tomorrow, tech says it can't be done, PM passes messages back and forth" | PM is a problem solver and decision driver, not a messenger |
| Delusional plan precision | Making an 18-month detailed plan from the start — everything changes by month 2 | Rolling-wave planning: next 2-4 weeks detailed, long-term kept at outline level |
| Risk register as decoration | Written but never reviewed in meetings, until risks become issues | Spend 15 minutes reviewing risks at every Core Team meeting |
| Carrying all problems alone | PM doesn't escalate issues; when they finally explode, Sponsor finds out too late | "Bad news early" — the sooner an issue is escalated, the more room there is to solve it |
| Sacrificing quality for schedule | "Just go live first, fix bugs later" → later = never have time to fix | Bug debt = technical debt; allocate 20-30% of each sprint to bug fixes |
| Ignoring team health | 3 months of continuous overtime → attrition spikes, knowledge loss, quality decline | Sustainable pace: overtime is the exception, not the norm; celebrate small wins; care about the team |
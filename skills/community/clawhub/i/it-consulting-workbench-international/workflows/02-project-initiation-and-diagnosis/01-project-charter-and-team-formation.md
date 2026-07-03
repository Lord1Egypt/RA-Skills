# 01 — Project Charter & Team Formation

## Objectives
Within one week of contract signing: complete the project charter, form the project team, run a successful kickoff meeting, and align both teams.

## Prerequisites
- SOW has been signed
- Client has designated a project liaison (typically IT PMO or CIO Office Director)

## Inputs
- Signed SOW (including project scope / deliverables / timeline / fees)
- Proposal (for understanding project background and initial assumptions)
- Background materials provided by the client

---

## Operation Steps

### Step 1: Develop the Project Charter — Day 1-3

The project charter is the "constitution" of the project — everyone must have a shared understanding of it.

**Project Charter Template:**

```markdown
# Project Charter — [Project Name]

## 1. Project Overview
### 1.1 Project Background
[Why was this project initiated? — 2-3 sentences]

### 1.2 Project Objectives (SMART)
- Objective 1: [Specific] [Measurable] [Achievable] [Strategy-relevant] [Time-bound]
- Objective 2: ...
- Objective 3: ...

### 1.3 Project Scope
In Scope:
  - [Specific deliverable/activity 1]
  - [Specific deliverable/activity 2]

Out of Scope — equally important!:
  - [Explicitly excluded item 1]
  - [Explicitly excluded item 2]

## 2. Project Organization
### 2.1 Governance Structure
┌─────────────────────────────────┐
│     Steering Committee (SteerCo) │  ← Strategic decisions / Budget / Major changes
│     Client Sponsor + Our Partner │     Monthly meetings
├─────────────────────────────────┤
│     Core Team                    │  ← Day-to-day decisions / Thematic advancement
│     Client PM + Our PM + Key SMEs│     Weekly meetings
├─────────────────────────────────┤
│     Workstreams                  │  ← Execution level
│     WS1 / WS2 / WS3              │     As needed
└─────────────────────────────────┘

### 2.2 Roles & Responsibilities (RACI Matrix)
Task                      Client Sponsor  Client PM  Our PM  Tech SME  Business SME
Project Objective Approval      A              R         C        I           C
Key Deliverable Sign-off        A              C         R        I           I
Day-to-day Decisions (<5% scope change)  I     C         A        R           R
Major Changes (>5% scope/budget) A             R         C        I           I

A=Accountable  R=Responsible
C=Consulted    I=Informed

### 2.3 Team Roster
| Role | Name | Organization | Allocation | Contact |
|------|------|-------------|-----------|---------|
| Executive Sponsor | | | | |
| Client Project Manager | | | | |
| Our Project Manager | | | | |
| Business SME | | | | |
| Technical SME | | | | |

## 3. Project Plan
### 3.1 Milestone Timeline
Milestone                    Planned Date    Acceptance Criteria
Kickoff Meeting              W1              [Criteria]
Mid-term Review              W6              [Criteria]
Initial Deliverable Review   W10             [Criteria]
Final Deliverable Review     W14             [Criteria]
Executive Final Presentation W16             [Criteria]
Project Closure              W18             [Criteria]

### 3.2 Key Dependencies
- [Our dependency on data X to be provided by client]
- [Client dependency on third-party vendor Y's cooperation]

## 4. Communication Plan
Communication Item        Audience         Frequency    Channel        Owner
Weekly Status Report      Core Team        Every Friday Email          Our PM
Monthly SteerCo Update    Steering Committee Monthly     Meeting+PPT    Our PM
Risk Escalation           Designated Persons Immediate   Phone/In-person Both PMs

## 5. Risk Management
See details in Risk Register (to be established within one week of project start)
- Top 3 Risks Identified:
  1. [Risk description] — Probability [High/Medium/Low] Impact [High/Medium/Low]
  2. ...
  3. ...

## 6. Signatures
[Client Sponsor]              Date: ________
[Our Partner]                 Date: ________
[Client Project Manager]      Date: ________
[Our Project Manager]         Date: ________
```

### Step 2: Running a Successful Kickoff Meeting — Day 3-5

**Pre-Meeting Preparation Checklist:**
- [ ] Project charter draft completed and internally reviewed
- [ ] All key stakeholders have confirmed attendance
- [ ] Meeting room / online link booked
- [ ] Presentation materials prepared (typically 15-20 slides)
- [ ] Any new developments since last client communication understood

**Kickoff Meeting Agenda (90-minute standard version):**

```
0-5min:   Opening & Sponsor Remarks (why this project matters)
5-15min:  Team Introductions (each person: Name/Role/Why I'm here)
15-25min: Project Charter Walkthrough (Objectives/Scope/Plan/Governance)
25-40min: Methodology & Ways of Working (how we'll do it / why this way / what you need to do)
40-55min: Risk & Concerns Discussion (open discussion: "What are you worried about?")
55-75min: Detailed Next Steps (specific work plan for the first 2-4 weeks)
75-85min: Q&A
85-90min: Summary + Consensus confirmation on "What does success look like?"
```

**Key Behaviors at the Kickoff:**

1. **The Sponsor must speak**: If the client Sponsor doesn't attend or speak, that's a red flag. Find a way to ensure the Sponsor delivers at least a 2-minute opening, saying "This project is important to our company" — those words are worth their weight in gold.

2. **Build psychological safety**: During the "Risk & Concerns Discussion" segment, show vulnerability proactively:
   > "Every project has uncertainties. I'd like each person to share one thing you're worried about — this is far more useful than pretending everything is perfect. I'll go first — my concern is that certain key client data may be scattered across too many departments, and collection will take longer than expected."

3. **Show the client team "what's in it for them"**: For each workstream, explain not just what will be done, but "how your daily work will change once this is complete."

### Step 3: Establish Information Infrastructure — Day 1-5

```
Must-create items:
  □ Project shared folder (SharePoint/Google Drive/Feishu/Lark)
    └── 01-Project Management/ (Charter/Plan/Status Reports)
    └── 02-Client Inputs/ (Materials provided by client)
    └── 03-Analysis Work/ (Intermediate analysis files)
    └── 04-Deliverables/ (Formal deliverables)
    └── 05-Meetings & Communications/ (Meeting minutes/Presentation materials)
    └── 06-Reference Materials/ (Industry reports/External data)

  □ Communication channels
    □ Instant messaging group (WeCom/DingTalk/Slack)
    □ Project email list
    □ Escalation path (what situation escalates to whom)

  □ Meeting cadence calendar
    □ Weekly meeting: Every [Day] [Time] (60 min)
    □ Monthly SteerCo: [X]th [Day] of each month (90 min)
    □ Ad-hoc Workshops: Book one week in advance
```

### Step 4: Establish Initial Risk Register — Day 5

```
Risk ID  Risk Description                  Probability  Impact  Level  Mitigation Measure                    Owner     Status
R001     Key person Mike may leave         High         High    🔴     1) Mandatory knowledge sharing 2) Backup person  Client PM  Monitoring
R002     Data acquisition delayed >2 weeks Medium       High    🟡     1) Initiate data requests early            Our PM     Mitigated
R003     Business units uncooperative on interviews  Medium  Medium  🟡     1) Sponsor sends interview notice        Client PM  Monitoring
```

---

## Outputs
1. **Project Charter**: Complete charter with 6 sections + RACI matrix
2. **Kickoff Meeting Minutes**: Including decision records and action items
3. **Project Folder Structure**: Standardized information infrastructure
4. **Risk Register**: Initial risk assessment

## Quality Checklist

- [ ] All 6 sections of the project charter fully completed
- [ ] Every key task in the RACI matrix has an A and an R
- [ ] Out of Scope section is as clear as In Scope
- [ ] Kickoff meeting minutes sent within 24 hours
- [ ] Project folder structure established
- [ ] Risk register established, Top 5 risks have mitigation measures

## Common Pitfalls

| Pitfall | Correct Approach |
|---------|------------------|
| Charter looks great but nobody reads it | The core value of the charter is in the discussion process — align everyone by confirming each item together |
| Kickoff becomes your monologue | Your speaking time <50%, Sponsor + client team >50% |
| Risk register created once and never updated | First agenda item at every weekly meeting is updating risks |
| All communication via formal channels | Build informal communication — having coffee with the client PM is more effective than 10 emails |

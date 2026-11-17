<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Governance & Communication

## Stage: 14 of 16
## Phase: 🟢 PLANNING
## Execution: ALWAYS

---

## Purpose

Define how the project will be governed (who decides what), how information flows (who communicates what to whom and when), and how the team operates day-to-day (methodology specifics, meetings, tools). This stage produces the RACI matrix, communication plan, and operating model documentation.

---

## MANDATORY: Stage Sub-Role — Change Manager

During THIS stage, ALSO adopt the mindset of a **Change Manager**. This does NOT replace your primary role (PMO Professional / Senior Project Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Design communications per audience — executives, team leads, and end-users need different messages, channels, and cadence
- Define governance as "who decides what and how fast" — not bureaucracy but clarity of authority
- Think about information flow: the right information, to the right people, at the right time, in the right format
- Frame the operating model around adoption — "will teams actually follow this cadence?"

### Anti-Patterns for This Stage
- Do NOT treat communication as "send an email" — it's a multi-channel, audience-segmented strategy
- Do NOT design governance so heavy that teams ignore it to stay productive

### Quality Check
A good output at this stage sounds like:
- "RACI: 15 activities × 8 roles; comms plan: 4 audiences, 3 channels each, cadence from weekly to monthly; escalation: 3 tiers with <24h response..."

---

## Depth Adaptation

| Depth | RACI Detail | Comms Plan | Operating Model |
|-------|-------------|-----------|-----------------|
| **Minimal** | Simple RACI (5-8 activities × 4-5 roles). Brief comms summary. | Meeting list with cadence only. | Methodology statement + DoD. |
| **Standard** | Full RACI (10-15 activities × 6-10 roles). Structured comms plan with audience, channel, frequency. | Meeting cadence table + escalation path. | Methodology, ceremonies, DoD, tools. |
| **Comprehensive** | Detailed RACI (15-25 activities × 8-12 roles). Full comms plan with templates, reporting schedule, stakeholder-specific channels. | Meeting cadence + agenda templates + escalation matrix + information flow diagram. | Full operating model with ceremonies, cadence, DoD, tools, ways of working, decision protocols. |

---

## Step-by-Step Execution

### Step 1: Load Context

1. Project Charter (Stage 9) — governance authority matrix, steering committee, methodology
2. Stakeholder Register (Stage 10) — who needs what level of engagement
3. Scope Statement (Stage 11) — activities/deliverables that need RACI assignment
4. Resource Plan (Stage 12) — roles available for RACI assignment
5. Risk Register (Stage 13) — risk review cadence defined there; align comms

---

### Step 2: Build RACI Matrix

#### Define Activities (Rows)

Select key project activities/decisions that need accountability clarity:

| Category | Example Activities |
|----------|-------------------|
| **Strategy & Scope** | Define scope, Approve scope changes, Set priorities, Accept deliverables |
| **Delivery** | Architecture decisions, Development work, Code review, Testing |
| **Planning** | Sprint planning, Resource allocation, Schedule baseline |
| **Quality** | Test strategy, Acceptance testing, Security review, Performance testing |
| **Governance** | Gate decisions, Budget approval, Risk escalation, Go-live decision |
| **Communication** | Status reporting, Stakeholder updates, Steering committee presentations |
| **Change** | Raise change requests, Assess impact, Approve changes, Implement changes |
| **Operations** | Environment provisioning, Deployment, Operational handover, Support |

Select 10-15 activities for Standard depth (adjust per depth level).

#### Define Roles (Columns)

From the Resource Plan and Stakeholder Register, select key roles:

Typical column set:
- Project Sponsor
- Product Owner
- Project Manager
- Technical Lead
- Security Lead
- QA Lead
- Development Team
- Change Manager
- Steering Committee

#### Assign RACI Values

| Value | Definition | Rules |
|:-----:|-----------|-------|
| **R** (Responsible) | Does the work; produces the deliverable | At least one R per row; can be multiple |
| **A** (Accountable) | Ultimate authority; approves/signs off; "the buck stops here" | Exactly ONE per row — never multiple A's |
| **C** (Consulted) | Provides input before decision/action; two-way communication | Domain experts; stakeholders with relevant knowledge |
| **I** (Informed) | Notified after decision/action; one-way communication | Those who need awareness but no input |

**RACI Rules:**
1. Every row MUST have exactly one A
2. Every row MUST have at least one R
3. A and R can be the same person (especially for smaller teams)
4. If a role has no letter in a row, they have no involvement in that activity
5. Minimize C's — too many consulted parties slows decisions
6. The person who is A cannot also be C (you can't consult yourself)

#### Output Format

```markdown
## RACI Matrix

| Activity | Sponsor | PO | PM | Tech Lead | Security | QA | Dev Team | Change Mgr |
|----------|:-------:|:--:|:--:|:---------:|:--------:|:--:|:--------:|:----------:|
| Define scope & requirements | I | A | R | C | C | | | |
| Approve scope changes (major) | A | C | R | C | I | | | I |
| Architecture decisions | I | C | I | A/R | C | | C | |
| Sprint planning | | C | A | R | | C | R | |
| Development & coding | | | I | A | | | R | |
| Security review | I | I | C | C | A/R | | C | |
| Test strategy & execution | | C | I | C | C | A/R | R | |
| Deployment | | I | A | R | C | C | R | |
| Status reporting | I | I | A/R | C | | | | |
| Go-live decision | A | C | R | C | C | C | | I |
| Change management & training | I | C | A | I | | | | R |
| Risk escalation | A | I | R | C | C | | | |
```

---

### Step 3: Define Communication Plan

#### Meeting Cadence

```markdown
## Meeting Cadence

| Meeting | Frequency | Duration | Participants | Purpose | Owner |
|---------|:---------:|:--------:|:-------------|---------|:-----:|
| Steering Committee | {Bi-weekly/Monthly} | {60 min} | {Sponsor, PM, PO, Tech Lead, Security} | Strategic decisions, gate approvals, escalations | PM |
| Project Team Sync | {Weekly} | {30 min} | {PM, all leads} | Status, blockers, cross-team coordination | PM |
| {Sprint Stand-up} | {Daily} | {15 min} | {Dev team, PM, Tech Lead} | Daily progress, impediments | Tech Lead |
| {Sprint Planning} | {Per sprint start} | {60-90 min} | {PM, PO, Tech Lead, Dev team} | Sprint backlog, commitments | PO |
| {Sprint Review/Demo} | {Per sprint end} | {60 min} | {PO, PM, stakeholders} | Demonstrate completed work, feedback | Tech Lead |
| {Sprint Retrospective} | {Per sprint end} | {45 min} | {Delivery team} | Process improvement | PM |
| Sponsor 1:1 | {Monthly} | {30 min} | {PM, Sponsor} | Strategic alignment, escalations, pulse check | PM |
| Risk Review | {Bi-weekly} | {30 min} | {PM, Tech Lead, relevant leads} | Risk register update, new risks, mitigations | PM |
```

**Rules:**
- Meeting cadence must align with methodology from Charter
- Don't over-schedule — every meeting must have clear purpose
- Agile projects: include sprint ceremonies
- Waterfall projects: include phase reviews and gate meetings
- Identify which meetings are optional for which roles

**If methodology is unclear, ask:**

```markdown
### Q-PLN-04: Meeting Cadence

**Context:** The communication plan needs a meeting structure. This depends on your team's working rhythm.

**Options:**
- (a) **Full Agile ceremonies** — Daily stand-up, sprint planning, review, retro, plus steering
- (b) **Light Agile** — Weekly sync, bi-weekly sprint review, monthly steering (no daily stand-up)
- (c) **Waterfall governance** — Weekly status, monthly steering, phase-gate reviews
- (d) **Minimal** — Weekly team sync + monthly steering only

**Recommended:** {Based on Charter methodology and team size}
**Rationale:** {Why}

**Your Decision:** _[awaiting input]_
```

---

### Step 4: Define Reporting Structure

```markdown
## Reporting Structure

| Report | Audience | Frequency | Content | Format | Owner |
|--------|----------|:---------:|---------|:------:|:-----:|
| Weekly Status Report | PM → Steering/Sponsor | Weekly | Progress, risks, blockers, next week plan | Email/Document | PM |
| Sprint Report | PO → Stakeholders | Per sprint | Completed items, velocity, burndown | Dashboard/Email | PM |
| Steering Committee Pack | PM → Steering | Per meeting | Status summary, decisions needed, risks, financials | Presentation | PM |
| Monthly Sponsor Brief | PM → Sponsor | Monthly | Strategic progress, key decisions, escalations | 1:1 verbal + 1-pager | PM |
| Financial Report | PM → Finance/Sponsor | Monthly | Budget vs. actual, forecast, variances | Spreadsheet | PM |
| Risk Report | PM → Steering | Per risk review | Updated register, new risks, trend analysis | Register extract | PM |
| Go-Live Readiness | PM → Steering | Pre go-live | Checklist, sign-offs, rollback plan | Document | PM |
```

---

### Step 5: Define Escalation Path

```markdown
## Escalation Path

```
Level 1: Project Team
  │ Attempt resolution within 24-48 hours
  │ If unresolved ↓
  │
Level 2: Project Manager
  │ Attempt resolution within 48 hours
  │ If unresolved or beyond authority ↓
  │
Level 3: Steering Committee
  │ Decision at next meeting or emergency session
  │ If strategic/existential ↓
  │
Level 4: Project Sponsor (CxO)
  │ Immediate decision authority
  └─────────────────────────────
```

### Escalation Criteria

| Trigger | Escalate To |
|---------|:-----------:|
| Technical blocker (team cannot resolve in 48h) | PM → Tech Lead decision |
| Scope dispute between stakeholders | PM → PO → Steering if unresolved |
| Budget variance approaching threshold | PM → Sponsor → Finance |
| Schedule risk (milestone at risk) | PM → Steering |
| Security/compliance concern | PM → Security Lead → Sponsor if risk-acceptance needed |
| Resource conflict or shortage | PM → Sponsor |
| Stakeholder conflict | PM → Sponsor (mediator) |
| Risk materializing with high impact | PM → Steering (emergency if needed) |
```

---

### Step 6: Define Operating Model Details

#### Definition of Done (DoD)

```markdown
### Definition of Done

A deliverable/feature is considered "Done" when:

- [ ] {Criterion 1 — e.g., Code complete and peer-reviewed}
- [ ] {Criterion 2 — e.g., Unit tests passing (coverage > X%)}
- [ ] {Criterion 3 — e.g., Integration tests passing}
- [ ] {Criterion 4 — e.g., Documentation updated}
- [ ] {Criterion 5 — e.g., Security review (if applicable)}
- [ ] {Criterion 6 — e.g., Deployed to staging}
- [ ] {Criterion 7 — e.g., PO acceptance confirmed}
```

**If specific DoD is unknown, provide a professional default and ask user to confirm.**

#### Tools and Platforms

```markdown
### Project Tools

| Purpose | Tool | Owner | Access |
|---------|------|:-----:|--------|
| Project tracking / backlog | {Jira / Azure DevOps / Linear / etc. or TBD} | PM | All team |
| Communication | {Teams / Slack / Email} | PM | All team + stakeholders |
| Documentation | {Confluence / SharePoint / Wiki / Repo} | PM | All team |
| Source control | {Git — GitHub/GitLab/Bitbucket or TBD} | Tech Lead | Delivery team |
| CI/CD | {Jenkins / GitHub Actions / etc. or TBD} | DevOps | Delivery team |
| Design | {Figma / Miro / Draw.io or TBD} | UX/Tech Lead | Design team |
```

**Rules:**
- If tools are not yet selected, use `_[TBD — to be selected before kickoff]_` and create Action Item
- Don't recommend specific commercial tools unless user has context — ask

---

### Step 7: Decision-Making Protocols (Comprehensive depth)

```markdown
### Decision-Making Protocols

| Decision Type | Process | Quorum | Timeframe |
|--------------|---------|:------:|:---------:|
| Technical (architecture, tech choice) | Tech Lead proposes → PM endorses → Steering ratifies if strategic | Tech Lead + PM | 48 hours |
| Scope (what's in/out) | PO proposes → PM assesses impact → Authority per Charter matrix | PO + PM | Per governance matrix |
| Priority (backlog order) | PO decides; Tech Lead advises on dependencies | PO alone | Immediate |
| People (hire, remove, reassign) | PM recommends → Sponsor approves | PM + Sponsor | 1 week |
| Process (methodology change) | PM proposes → Team retro validates → Steering informed | PM + Team | Sprint boundary |
| Emergency (production incident, security breach) | PM convenes war room → immediate Sponsor escalation | PM + Sponsor | Immediate |
```

---

### Step 8: Assemble Document

Using template `templates/raci-matrix.md`, compile:

1. Section 1: RACI Matrix (table)
2. Section 2: Communication Plan (meeting cadence + reporting structure)
3. Section 3: Escalation Path (visual + criteria table)
4. Section 4: Operating Model (DoD, tools, decision protocols)
5. Section 5: Meeting Schedule Summary (consolidated calendar view)

Validate:
- [ ] Every Stakeholder Register "Manage Closely" person appears in at least one meeting
- [ ] RACI roles match Resource Plan roles (no phantom roles)
- [ ] Meeting cadence aligns with Charter methodology
- [ ] Escalation path aligns with Charter authority matrix
- [ ] Every activity in RACI has at least one corresponding meeting where it's discussed

---

### Step 9: Present for Review

```markdown
## Review: Governance & Communication — {project_name}

I've produced the RACI Matrix and Communication Plan. Key highlights:

- **RACI:** {n} activities × {m} roles mapped
- **Meetings:** {n} recurring meetings defined
- **Reporting:** {n} report types with audience and cadence
- **Escalation:** {n}-level path defined
- **DoD:** {n} criteria
- **Tools:** {n} identified ({m} TBD)

**Key governance highlights:**
- Scope authority: {who}
- Budget authority: {who}
- Go-live authority: {who}
- Daily delivery authority: {who}

**Full document:** Saved to `{file_path}`

---

**Your response:**
- (a) **Approve** — Governance structure is clear; proceed to Mobilization
- (b) **Adjust RACI** — Accountability assignments need changes
- (c) **Change meetings** — Meeting cadence needs revision
- (d) **Modify escalation** — Escalation path needs adjustment
- (e) **Add detail** — Need more specifics in certain areas
```

---

### Step 10: Log and Transition

1. **Decision Log:** D-{nnn}: "Governance & Communication plan approved. RACI: {n} activities. Meeting cadence: {summary}. Methodology: {approach}."
2. **State File:** Stage 14 = ✅ Done; Current Phase = MOBILIZATION; Current Stage = 15
3. **Action Items:** For any TBD tools: A-{nnn}: "Select and set up {tool category}" — Owner: {PM/Tech Lead}

Display:

```
✅ Stage 14: Governance & Communication — Complete

📊 RACI: {n} activities mapped | 📅 {n} meetings defined
📄 Saved to: {file_path}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ PLANNING PHASE COMPLETE (Stages 10-14)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Planning Summary:
   👥 Stakeholders: {n} registered
   📐 Scope: {n} items, {levels}-level WBS
   💰 Budget: {$range} ROM
   ⚠️  Risks: {n} identified ({high} high+)
   🏗️  Governance: RACI + comms defined

Next → MOBILIZATION PHASE (Stages 15-16)
Kickoff preparation and final package assembly.

Proceeding...
```

---

## Output File

Save to:
- Numbered: `{output_root}/09_Governance_Communication/RACI_Matrix.md`
- Flat: `{output_root}/pilc-docs/planning/RACI_Matrix.md`

---

## RACI Quality Checks

| Check | Pass Criteria |
|-------|---------------|
| Single Accountable | Every row has exactly one A |
| No empty rows | Every activity has at least R and A |
| No overloaded roles | No single role has A for >50% of activities (bottleneck) |
| Sponsor not over-engaged | Sponsor should be A only for strategic decisions, not operational |
| PM role clear | PM should be R for coordination, not A for technical decisions |
| Team not excluded | Dev team should be R for delivery activities, not just I |
| Stakeholders covered | All "Manage Closely" stakeholders from register appear in RACI |

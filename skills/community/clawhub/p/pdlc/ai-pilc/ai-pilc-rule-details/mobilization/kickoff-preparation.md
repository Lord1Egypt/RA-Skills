<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Kickoff Preparation

## Stage: 15 of 16
## Phase: 🚀 MOBILIZATION
## Execution: ALWAYS

---

## Purpose

Prepare everything needed for a successful project kickoff meeting — the formal event that transitions the project from initiation to execution. This includes the agenda, attendee list, presentation structure, pre-kickoff checklist, key messages, and immediate post-kickoff actions.

---

## MANDATORY: Stage Sub-Role — Change Manager

During THIS stage, ALSO adopt the mindset of a **Change Manager**. This does NOT replace your primary role (PMO Professional / Senior Project Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Frame the kickoff as the first change-management event — "why now", "what's in it for me", "what's changing" before "what are the deliverables"
- Plan communications per audience segment in the room — sponsors hear governance, team hears operating model, stakeholders hear impact
- Define immediate post-kickoff actions that build momentum and signal "this is real"
- Think about psychological safety — the kickoff sets the tone for how openly people will raise issues later

### Anti-Patterns for This Stage
- Do NOT design the kickoff as a one-directional presentation — plan for two-way engagement
- Do NOT end the kickoff without clear "what happens Monday morning" actions

### Quality Check
A good output at this stage sounds like:
- "Agenda: 12 items with timing and presenter; key message per audience; pre-kickoff checklist (8 items with owners); Week 1 actions: 5 items with owners and dates..."

---

## Depth Adaptation

| Depth | Kickoff Scope |
|-------|--------------|
| **Minimal** | Simple agenda (5-6 items), attendee list, 3-5 post-kickoff actions. No deck structure. Suitable for small teams (<8 people). |
| **Standard** | Full agenda (8-12 items with timing), attendee list with roles, pre-kickoff checklist, suggested deck structure, post-kickoff Week 1 actions. |
| **Comprehensive** | Detailed agenda with presenter assignments and talking points, full deck slide-by-slide structure, key messages framework, success criteria for the meeting, pre-kickoff checklist with owners and status, detailed Week 1 plan. |

---

## Step-by-Step Execution

### Step 1: Load Context

1. Project Charter (Stage 9) — objectives, scope, governance, approach
2. Stakeholder Register (Stage 10) — who should attend
3. Scope Statement (Stage 11) — what to present as scope
4. Resource Plan (Stage 12) — team structure to introduce
5. Risk Register (Stage 13) — top risks to communicate
6. RACI/Governance (Stage 14) — meeting cadence, escalation to establish
7. Business Case (Stage 8) — the "why" narrative

---

### Step 2: Define Attendee List

Pull from Stakeholder Register — categorize by Required vs. Optional:

```markdown
## Attendees

| # | Name | Role | Required / Optional | Purpose at Kickoff |
|---|------|------|:-------------------:|-------------------|
| 1 | {Name} | {Project Sponsor} | Required | Delivers opening; confirms commitment |
| 2 | {Name} | {Product Owner} | Required | Presents scope and priorities |
| 3 | {Name/TBD} | {Project Manager} | Required | Facilitates; presents plan |
| 4 | {Name/TBD} | {Technical Lead} | Required | Presents approach; answers tech questions |
| 5 | {Name} | {Security Lead} | Required | Sets security expectations |
| 6 | {Name} | {SME / UAT Lead} | Required | Domain authority; represents users |
| 7 | {Name/TBD} | {Infrastructure Lead} | Required | Environment readiness |
| 8 | {Name/TBD} | {QA Lead} | Optional | Quality approach awareness |
| 9 | {Name/TBD} | {DevOps Lead} | Optional | CI/CD and deployment awareness |
| 10 | {Name/TBD} | {Development Team reps} | Optional | Team bonding; context |
```

**Rules:**
- Required: Anyone who has an A or R in RACI for the first phase
- Optional: Anyone in "Keep Informed" quadrant or delivery team members
- All Steering Committee members should be Required
- If team is not yet hired, note: "To be invited once onboarded"

---

### Step 3: Build Agenda

```markdown
## Agenda

| # | Topic | Duration | Presenter | Key Points |
|---|-------|:--------:|-----------|------------|
| 1 | Welcome & Introductions | {10 min} | PM | Team introductions; meeting objectives; housekeeping |
| 2 | Sponsor's Opening — Vision & Why | {10 min} | Sponsor | Strategic importance; business context; personal commitment |
| 3 | Project Objectives & Success Criteria | {10 min} | PM / PO | Measurable objectives from Charter; what "done" looks like |
| 4 | Scope Overview — In and Out | {10 min} | PO | In-scope items; explicit exclusions; boundary clarity |
| 5 | High-Level Timeline & Milestones | {10 min} | PM | Milestone schedule; phase structure; target delivery |
| 6 | Team Structure & RACI | {10 min} | PM | Who does what; accountability; how to reach each other |
| 7 | Governance & Communication | {5 min} | PM | Meeting cadence; reporting; escalation path |
| 8 | Delivery Approach & Ways of Working | {10 min} | PM / Tech Lead | Methodology; sprint rhythm; DoD; tools; standards |
| 9 | Top Risks & Mitigation | {5 min} | PM | Top 5 risks; approach to risk management |
| 10 | {Domain-specific topic} | {5 min} | {Specialist} | {Security expectations / compliance / infra readiness} |
| 11 | Immediate Next Steps & First Sprint | {10 min} | PM / Tech Lead | Week 1 plan; first sprint scope; immediate actions |
| 12 | Q&A and Open Discussion | {10 min} | All | Questions; concerns; clarifications |
| | **Total** | **~{n} min** | | |
```

**Rules:**
- Total duration: 60-120 minutes (aim for 90 max for standard projects)
- Sponsor speaks early (shows commitment, then can leave if needed)
- End with concrete next steps (people leave knowing what to do Monday)
- Q&A at end, but encourage questions throughout
- Adjust topics based on project context — add/remove domain-specific items

---

### Step 4: Define Key Messages

```markdown
## Key Messages to Communicate

| # | Message | Why It Matters |
|---|---------|----------------|
| 1 | **WHY** — {Strategic importance of this project} | Sets urgency and alignment |
| 2 | **WHAT** — {Clear scope with explicit boundaries} | Prevents scope assumptions |
| 3 | **HOW** — {Delivery approach and team rhythm} | Everyone knows how we work |
| 4 | **WHO** — {Every role has clear accountability} | No ambiguity about ownership |
| 5 | **WHEN** — {Timeline with phased value delivery} | Realistic expectations |
| 6 | **QUALITY** — {Non-negotiable standards} | Sets the quality bar early |
| 7 | **COMMUNICATION** — {How we'll stay connected} | Trust through transparency |
| 8 | **CHANGE CONTROL** — {Formal process for scope changes} | Protects the team |
```

**Derive each message from project artifacts:**
- WHY → Business Case problem statement + strategic alignment
- WHAT → Scope Statement in/out
- HOW → Charter methodology + RACI
- WHO → Resource Plan + RACI
- WHEN → Scope Statement milestones
- QUALITY → Charter acceptance criteria + NFRs
- COMMUNICATION → Governance comms plan
- CHANGE CONTROL → Scope Statement change control section

---

### Step 5: Produce Pre-Kickoff Checklist

```markdown
## Pre-Kickoff Checklist

| # | Item | Owner | Status | Blocking? |
|---|------|:-----:|:------:|:---------:|
| 1 | Project Charter signed by all signatories | PM / Sponsor | ☐ Pending | Yes |
| 2 | Project Manager appointed and onboarded | Sponsor | ☐ Pending | Yes |
| 3 | Technical Lead appointed and onboarded | Sponsor / PM | ☐ Pending | Yes |
| 4 | Steering Committee members confirmed | PM | ☐ Pending | Yes |
| 5 | Budget approved at ROM level | Sponsor / Finance | ☐ Pending | Yes |
| 6 | Key team members identified (if not recruited) | PM / HR | ☐ Pending | No |
| 7 | Project tracking tool selected and set up | PM / Tech Lead | ☐ Pending | No |
| 8 | Collaboration spaces created (chat, files) | PM | ☐ Pending | No |
| 9 | Kickoff presentation prepared | PM | ☐ Pending | Yes |
| 10 | Meeting invite sent (2 weeks notice minimum) | PM | ☐ Pending | Yes |
| 11 | Risk Register reviewed and current | PM | ☐ Pending | No |
| 12 | First sprint/phase planned at high level | PM / Tech Lead | ☐ Pending | No |
```

**Rules:**
- Mark items as "Blocking" if the kickoff CANNOT happen without them
- Blocking items: Charter signed, PM appointed, budget approved, invite sent, deck ready
- Non-blocking items: nice-to-have before kickoff but can follow in Week 1
- Create Action Items for each pending checklist item

---

### Step 6: Suggest Deck Structure (Standard/Comprehensive)

```markdown
## Kickoff Deck — Suggested Slide Structure

| Slide # | Title | Content |
|:-------:|-------|---------|
| 1 | Title | Project name, date, classification |
| 2 | Sponsor's Opening | Vision and strategic importance |
| 3 | The Problem | Current state pain points (visual) |
| 4 | The Solution | What we're building (high-level diagram or summary) |
| 5 | Objectives | Measurable objectives table |
| 6 | Scope — In | Visual summary of in-scope items |
| 7 | Scope — Out | Explicit exclusions and deferrals |
| 8 | Timeline | Milestone schedule (visual timeline or table) |
| 9 | Delivery Approach | Methodology diagram; sprint rhythm; phases |
| 10 | Team Structure | Org chart or role diagram |
| 11 | RACI Highlights | Simplified accountability for key decisions |
| 12 | Governance & Comms | Meeting cadence; escalation path |
| 13 | Top Risks | Risk summary with mitigation headlines |
| 14 | {Domain Slide} | Security / compliance / infrastructure expectations |
| 15 | Budget Overview | ROM range; phasing (if shareable with audience) |
| 16 | What Happens Next | First sprint plan; Week 1 actions |
| 17 | Q&A | Open floor |
| 18 | Close | Team commitment; energy; next meeting date |
```

---

### Step 7: Define Post-Kickoff Actions (Week 1)

```markdown
## Post-Kickoff Actions (Week 1)

| # | Action | Owner | Due | Priority |
|---|--------|:-----:|:---:|:--------:|
| 1 | Distribute kickoff meeting minutes | PM | Day +1 | High |
| 2 | Share project document repository access | PM | Day +1 | High |
| 3 | Set up all recurring meetings (per comms plan) | PM | Day +2 | High |
| 4 | Configure project tracking tool (backlog, boards) | PM / Tech Lead | Day +3 | High |
| 5 | Begin first sprint/phase work | Tech Lead / Team | Day +1 | High |
| 6 | Schedule key workshops (architecture, requirements deep-dive) | PM | Day +3 | Medium |
| 7 | Initiate recruitment for unfilled roles | PM / HR | Day +1 | Medium |
| 8 | Confirm environment/infrastructure timeline | PM / Infra Lead | Day +3 | Medium |
| 9 | Update project roadmap/tracking to "In Execution" | PM | Day +1 | Low |
| 10 | Send stakeholder communication (project started) | PM | Day +2 | Low |
```

---

### Step 8: Define Success Criteria for the Meeting

```markdown
## Kickoff Success Criteria

The kickoff meeting is considered successful when:

- [ ] All required attendees present (or formally delegated)
- [ ] Sponsor delivers opening and confirms commitment
- [ ] All attendees understand scope boundaries (in and out)
- [ ] All attendees understand their role and governance structure
- [ ] No unresolved questions blocking Week 1 activities
- [ ] Team expresses readiness to begin
- [ ] Next steps and immediate actions are clear with owners and dates
- [ ] Energy and alignment are positive
```

---

### Step 9: Assemble Document

Using template `templates/kickoff-agenda.md`, compile:

1. Section 1: Attendees (table)
2. Section 2: Agenda (timed, with presenters)
3. Section 3: Key Messages (framework)
4. Section 4: Pre-Kickoff Checklist (with status)
5. Section 5: Deck Structure (Standard/Comprehensive)
6. Section 6: Post-Kickoff Actions (Week 1)
7. Section 7: Success Criteria
8. Section 8: Notes & Decisions (empty template for capturing during meeting)

---

### Step 10: Present for Review

```markdown
## Review: Kickoff Preparation — {project_name}

I've produced the Kickoff Agenda and supporting materials. Key highlights:

- **Attendees:** {n} required, {m} optional
- **Agenda:** {n} topics, ~{duration} minutes total
- **Pre-kickoff blockers:** {n} items must be resolved before meeting
- **Week 1 actions:** {n} post-kickoff actions defined
- **Deck:** {n}-slide structure suggested

**Pre-kickoff readiness:**
- Blocking items resolved: {n}/{total_blocking}
- Non-blocking items ready: {n}/{total_non_blocking}

**Full document:** Saved to `{file_path}`

---

**Your response:**
- (a) **Approve** — Kickoff materials are ready; proceed to Package Assembly
- (b) **Adjust agenda** — Topics or timing need revision
- (c) **Change attendees** — Add or remove participants
- (d) **Modify actions** — Post-kickoff plan needs adjustment
- (e) **Add content** — Need additional sections or detail
```

---

### Step 11: Log and Transition

1. **Decision Log:** D-{nnn}: "Kickoff preparation complete. Agenda: {n} topics / {duration} min. {blocking} blocking items pending."
2. **State File:** Stage 15 = ✅ Done; Current Stage = 16
3. **Action Items:** One per pre-kickoff checklist blocking item: A-{nnn}: "{Item}" — Owner: {role}

Display:

```
✅ Stage 15: Kickoff Preparation — Complete

📅 Agenda: {n} topics, ~{duration} min
✅ Checklist: {n} items ({blocking} blocking)
📄 Saved to: {file_path}

Next → Stage 16: Project Initiation Package Assembly
Final consolidation and quality check of all deliverables.

Proceeding...
```

---

## Output File

Save to:
- Numbered: `{output_root}/10_Project_Kickoff/Kickoff_Agenda.md`
- Flat: `{output_root}/pilc-docs/mobilization/Kickoff_Agenda.md`

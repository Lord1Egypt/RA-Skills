# Interview Question Banks

Extended question banks for the Pass 1 (Team Identity) and Pass 2 (Work Structure) interviews. Use the questions in SKILL.md as the core flow; consult this file when:
- The user answers ambiguously and you need follow-up questions
- The team type is unusual and you need specialized prompts
- You're filling gaps in the AI-drafted plan and need to know what's missing

---

## Table of Contents

- [Pass 1: Team Identity — Core](#pass-1-team-identity--core)
- [Pass 1: Team Identity — Follow-ups](#pass-1-team-identity--follow-ups)
- [Pass 2: Work Structure — Core](#pass-2-work-structure--core)
- [Pass 2: Work Structure — Follow-ups](#pass-2-work-structure--follow-ups)
- [Pass 2: Team-Type-Specific Probes](#pass-2-team-type-specific-probes)
- [Gap-Filling Heuristics](#gap-filling-heuristics)

---

## Pass 1: Team Identity — Core

These are the questions in SKILL.md, restated here for reference:

1. **Project purpose** — one-sentence description
2. **Team type** — software dev, marketing, real estate, content, sales, customer success, operations, research, or other (describe)
3. **Project name and ID** — display name + lowercase ID
4. **Agent roster** — which existing agents will be on this team and their per-project role
5. **Client-facing agent** — who receives intake and talks to the client
6. **Feasibility reviewer** — domain expert who validates work is doable before commitment
7. **Quality reviewer** — who checks completed work before client delivery
8. **Operator** — is there a human in the loop, and what's their alias
9. **Other roles** — specialized contributors

---

## Pass 1: Team Identity — Follow-ups

If a user's answer is vague or missing, dig deeper:

### If they don't know what to call their team type
> "Don't worry about the label — describe what the team produces or does. Examples: 'They write blog posts and social copy for our clients.' Or: 'They handle inbound leads and qualify them.' I can pick a category from there."

### If they say they don't have a clear feasibility reviewer
> "Even if you don't have a formal 'reviewer,' someone needs to look at incoming work and say whether the team can actually do it given current capacity, skills, or constraints. Who would catch a problem like 'this requires expertise nobody has' before the team commits to delivering it?"

### If they say they don't have QA
> "Someone needs to be the last set of eyes before the work goes to the client. It doesn't have to be a separate person — it could be the feasibility reviewer doing a final pass. But there should be someone designated. Who is it?"

### If they say no operator
> "If a problem can't be resolved by any agent — say a client goes silent for a week, or two agents disagree on something the spec doesn't cover — who steps in? Even if it's just you, that's the operator."

### If they want all agents to do everything
Push back gently:
> "Specialized roles produce better results than agents trying to do everything. I'll need at least: a client-facing role, a feasibility reviewer, and a QA reviewer. Pick which agents fill those — they can still do other work too."

---

## Pass 2: Work Structure — Core

Restated from SKILL.md:

1. Task manager (Asana / ClickUp)
2. Stages of work (column structure)
3. Shared working medium
4. Definition of "done"
5. Sprint mode (one-at-a-time vs continuous flow)
6. Escalation thresholds
7. Visual / media assets
8. Anything else specific

---

## Pass 2: Work Structure — Follow-ups

### If they're unsure what columns to use

Suggest a default based on team type, then customize. Sensible defaults below.

### If they say "we don't have a shared working medium"
> "Even if work is mostly conversational, agents need somewhere to read shared context — past decisions, current state, reference material. That can be the project folder itself (`workspace/`). Is that enough, or do you have an external system the team uses?"

### If they're confused about sprint mode
> "Think about how new work arrives. Does the client typically hand you one big chunk to do well, or a steady stream of small things? Big chunks → sprint mode. Steady stream → continuous flow. You can change this later."

### If escalation thresholds feel arbitrary
> "These exist so agents don't spin wheels burning AI tokens. The defaults — 24 hours stuck, 2 re-escalations, 48 hours waiting on client — are reasonable for most teams. If your work is faster-paced (e.g., same-day turnaround), tighten these. If slower (e.g., long research projects), loosen them."

### If they're unclear on visual/media handling
Ask:
- "Will any agent need to look at images, video, or audio to do their work?"
- "Will any agent need to produce images, video, or audio as output?"

If either is yes → visual handling needed.

---

## Pass 2: Team-Type-Specific Probes

Use these to flesh out the plan when the user picks a particular team type.

### Software Development
- Frontend / backend / full-stack split?
- Branch and PR conventions? (default suggested in workflow.md)
- Local dev environment standardized?
- Deployment owned by team or separate?
- Test conventions — required or aspirational?

### Marketing / Creative
- Brand guidelines location?
- Channel mix (social, blog, email, paid)?
- Creative director or copy lead?
- Asset library / DAM in use?
- Approval chain — does client see drafts or only finals?

### Real Estate
- Listing source — MLS or direct?
- Photography handled by team or external?
- Pricing authority — who signs off?
- CRM platform?
- Compliance / disclosure requirements?

### Content / Editorial
- Editorial calendar in place?
- Editor / copy editor / fact-checker chain?
- CMS in use?
- SEO requirements?
- Image sourcing rules (rights, attribution)?

### Sales / Outreach
- CRM platform?
- Lead source(s)?
- Qualification criteria?
- Hand-off to closer / account manager?
- Compliance (GDPR, CAN-SPAM, etc.)?

### Customer Success / Support
- Ticketing platform?
- Tier 1 / Tier 2 split?
- Knowledge base location?
- SLA targets?
- Escalation path for technical issues?

### Operations
- What's the operational scope? (logistics, finance, HR ops, etc.)
- Systems of record?
- Approval workflows?
- Audit / compliance requirements?

### Research
- Research domain?
- Sources (papers, web, internal data)?
- Output format (reports, briefings, structured data)?
- Peer review chain?

### Other / Custom
Ask:
- "Walk me through what the team does end-to-end. Start when work arrives, end when it's delivered."
- "Where does the team produce its work?"
- "Who reviews before delivery?"
- "What can go wrong, and who handles it?"

---

## Default Stage Suggestions by Team Type

Use these as starting points. Confirm with user before locking in.

| Team Type | Suggested Stages |
|---|---|
| Software Dev | Backlog → In Progress → In Review → QA → Completed → Blocked |
| Marketing | Brief → In Drafting → Internal Review → Client Review → Approved → Blocked |
| Real Estate | New → Listing Prep → Listed → Under Offer → Closed → Blocked |
| Content | Idea → Drafting → Editing → Fact Check → Published → Blocked |
| Sales | Lead → Qualifying → Engaged → Proposal → Closed-Won/Lost → Blocked |
| Customer Success | New Ticket → In Progress → Awaiting Customer → Resolved → Blocked |
| Operations | Request → Triage → In Progress → Verification → Complete → Blocked |
| Research | Question → Investigating → Drafting → Peer Review → Published → Blocked |

Every team should have a "Blocked" column for work that's stuck waiting on something external.

---

## Gap-Filling Heuristics

When writing the AI-drafted plan in Step 4, you'll inevitably need to fill gaps the user didn't explicitly answer. Use these heuristics. Mark all inferred items with [INFERRED] in the plan.

### Communication frequency
If unspecified, default: agents check their queue at every session start, before any other action.

### Sprint length
If unspecified and using sprint mode, do not invent a fixed length. Sprints end when all committed work is delivered, not on a calendar.

### Re-work loops
If unspecified, default: failed QA review → back to executor with specific failures listed → re-submit when fixed. Same dev escalation rules apply during rework.

### Idle behavior
If unspecified, default: when nothing is in their queue and no task is assigned to them, agents do nothing (do not invent work).

### Decision authority
If unspecified, default: feasibility-reviewer has technical authority within the project; client-facing agent has client-relationship authority; operator has final authority on anything contested.

### "Done" definition
If unspecified for the team type, default: "QA reviewed and approved against the accepted scope, and the operator (if any) has signed off on delivery." Adjust per team.

### Versioning of accepted scope
Always default: scope documents are versioned (`SPEC-v1-[date].md`) and never overwritten. Latest accepted version is referenced from `SPEC-CURRENT.md`. This is universal across team types.

### Mid-sprint scope changes
If unspecified, default: scope changes mid-sprint require client-facing agent to pause work, log the change in DECISIONS.md, get explicit re-acceptance from client, and update SPEC. Avoid silent scope drift.

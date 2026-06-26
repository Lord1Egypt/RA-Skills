---
name: meeting-notes-actions
description: Transform raw meeting notes or transcripts into structured summaries, action items with owners and deadlines, individual follow-up emails, and next meeting agendas. Use when someone has meeting notes to process, needs to send follow-ups, or wants to extract actions from a conversation.
user-invocable: true
argument-hint: "paste your meeting notes or transcript"
---

# Meeting Notes to Actions

You transform raw meeting notes into structured, actionable output. The user pastes messy notes; you produce clean summaries, action items, follow-up emails, and agendas. Everything you produce should be copy-paste ready -- no placeholders, no [INSERT HERE], no filler.

---

## Input Handling

Accept any of the following input formats without complaint:

- **Raw typed notes** -- bullet points, fragments, shorthand, abbreviations
- **Meeting transcripts** -- from Zoom, Teams, Google Meet, Otter.ai, Fireflies, etc.
- **Voice memo transcriptions** -- messy, conversational, full of false starts
- **Slack/Teams thread summaries** -- copied message chains
- **Handwritten note descriptions** -- "I wrote down that..." or photographed note descriptions
- **Mixed formats** -- some structured, some stream-of-consciousness

Do not ask for clarification on format. Parse what you are given. If names are abbreviated or unclear, use what is available and flag ambiguity in the output.

---

## Interaction Modes

Ask the user which mode they want if not obvious from context. Default to **quick process** if they just paste notes without instruction.

### 1. Quick Process
Paste notes, get all five output sections. This is the default.

### 2. Meeting Type Preset
User specifies a meeting type. Adjusts focus and adds type-specific output.

| Type | Focus | Extra Output |
|---|---|---|
| Client call | Deliverables, timeline, budget | Client-facing summary email |
| Standup / scrum | Blockers, yesterday/today | Sprint board update format |
| Board meeting | Decisions, governance | Formal board minutes format |
| 1:1 | Feedback, development, issues | Private notes format |
| Sprint retro | What worked, what didn't, actions | Retro summary with themes |
| Sales call | Needs, objections, next steps | CRM update notes |
| Interview | Candidate assessment | Scorecard summary |

### 3. Follow-up Only
Just generate the individual follow-up emails. Skip the rest.

### 4. Actions Only
Just extract the action items table. Skip the rest.

### 5. Status Update
Generate a project status update from the meeting context.

---

## Output Sections

Produce all five sections in order for quick process mode. For other modes, produce only the relevant sections.

---

### Section 1: Meeting Summary

```markdown
## Meeting Summary

**Date:** [extracted or today's date]
**Attendees:** [extracted from notes]
**Duration:** [if mentioned]
**Purpose:** [inferred from context]

### Key Decisions
- [Decision 1] -- agreed by [who]
- [Decision 2] -- pending [condition]

### Discussion Points
- [Topic 1]: [2-3 sentence summary]
- [Topic 2]: [2-3 sentence summary]

### Open Questions
- [Question 1] -- needs input from [who]
- [Question 2] -- to be resolved by [date/next meeting]
```

**Rules:**
- Extract the date from context. If not mentioned, use today's date.
- List every attendee mentioned by name. Note roles if clear from context.
- Key decisions must state WHO agreed and any conditions.
- Open questions must have an owner or destination (person, next meeting, etc.).
- Keep discussion summaries to 2-3 sentences maximum. No padding.

---

### Section 2: Action Items

```markdown
### Action Items

| # | Action | Owner | Deadline | Priority | Status |
|---|--------|-------|----------|----------|--------|
| 1 | [Specific, measurable action] | [Name] | [Date] | High/Med/Low | Open |
| 2 | [Specific, measurable action] | [Name] | [Date] | High/Med/Low | Open |

**Unassigned Actions (need owners):**
- [Action without clear owner]
```

**Rules:**
- Actions must be specific and measurable. Not "look into X" but "research X and report findings to [person] by [date]."
- If no deadline is mentioned, infer a reasonable one based on context or mark as "TBD -- needs deadline."
- Priority is inferred from discussion emphasis, urgency language, and dependencies.
- If an action has no clear owner, put it in the unassigned section rather than guessing.
- Number actions sequentially. They will be referenced in follow-up emails.

---

### Section 3: Follow-up Emails

Generate one email per attendee (excluding the sender). Each email is personalised to that person's specific actions and relevant decisions.

```markdown
### Follow-up: [Attendee Name]

**Subject:** [Meeting title] -- Actions & Next Steps

Hi [Name],

Thanks for [meeting context -- e.g., "joining today's project review" or "the call this morning"]. Here is a summary of what we covered and your specific actions:

**Your actions:**
- [Action 1] -- by [date]
- [Action 2] -- by [date]

**Key decisions:**
- [Only decisions relevant to this person]

**Next steps:**
- [What happens next for this person or the group]

[Next meeting details if scheduled]

Best,
[Your name]
```

**Rules:**
- Each email must be self-contained. The recipient should not need the full summary to understand their responsibilities.
- Only include decisions and context relevant to that specific person.
- Tone: professional but not corporate. Warm, concise, human.
- Sign off with a placeholder for the sender's name. Use "Best," as the default.
- If there are more than 6 attendees, offer to group emails by team/function instead of individual.
- Subject line must be specific. Not "Meeting follow-up" but "[Project Name] Review -- Actions & Next Steps."

---

### Section 4: Next Meeting Agenda

```markdown
### Suggested Next Meeting Agenda

1. **Review actions from [today's date] meeting**
   - [Action 1] -- [Owner] update
   - [Action 2] -- [Owner] update
2. **Open items carried forward**
   - [Open question 1]
   - [Open question 2]
3. **[New topic inferred from discussion]**
4. **AOB**

*Suggested duration: [time estimate based on agenda items]*
```

**Rules:**
- Always start with a review of previous actions.
- Carry forward any unresolved questions.
- Infer new topics from the discussion trajectory (e.g., if a demo was mentioned as upcoming, add "Demo review").
- Estimate duration based on number of items. 30 mins for 3-4 items, 45 for 5-7, 60 for 8+.
- AOB (Any Other Business) always goes last.

---

### Section 5: Project Status Update

Only include if the meeting context implies an ongoing project. Skip for one-off meetings, interviews, or social calls.

```markdown
### Project Status Update

**Project:** [inferred from context]
**Status:** On Track / At Risk / Blocked
**Last updated:** [meeting date]

**Completed since last update:**
- [Items discussed as done]

**In progress:**
- [Items discussed as ongoing]

**Blocked / at risk:**
- [Items flagged as issues]

**Next milestones:**
- [Upcoming deliverables or deadlines mentioned]
```

**Rules:**
- Status is inferred from tone and content. Blockers mentioned = At Risk or Blocked. Everything on track = On Track.
- Only include items actually discussed. Do not invent progress.
- If the meeting does not relate to a specific project, skip this section entirely and note: "No project status generated -- meeting did not relate to a specific project."

---

## Meeting Type Presets -- Extra Outputs

When a meeting type preset is selected, produce the standard sections PLUS the type-specific extra output.

### Client Call -- Client-facing Summary

```markdown
### Client Summary

Hi [Client name],

Great speaking with you [today/this morning/etc.]. Here is a summary for your records:

**What we agreed:**
- [Decision 1]
- [Decision 2]

**Next steps from our side:**
- [Deliverable 1] -- by [date]
- [Deliverable 2] -- by [date]

**What we need from you:**
- [Item 1] -- by [date]
- [Item 2] -- by [date]

**Next catch-up:** [date/time if scheduled]

Thanks,
[Your name]
```

Client-facing summaries must be polished. No internal jargon, no mention of internal processes. Focus on deliverables and what the client needs to do.

### Standup / Scrum -- Sprint Board Update

```markdown
### Sprint Board Update

**[Person 1]:**
- Yesterday: [completed items]
- Today: [planned items]
- Blockers: [any blockers]

**[Person 2]:**
- Yesterday: [completed items]
- Today: [planned items]
- Blockers: [any blockers]

**Sprint blockers to escalate:**
- [Blocker 1] -- assigned to [who]
```

### Board Meeting -- Formal Minutes

```markdown
### Board Minutes

**Meeting of the Board of [Organisation]**
**Date:** [date]
**Present:** [names and roles]
**Apologies:** [names]
**Chair:** [name]

**1. [Agenda item 1]**
Discussion: [summary]
Resolution: [what was decided]
Vote: [if applicable -- carried/not carried, for/against/abstain]

**2. [Agenda item 2]**
...

**Actions arising:**
| Action | Owner | Deadline |
|--------|-------|----------|
| [Action] | [Name] | [Date] |

**Date of next meeting:** [date]

*Minutes prepared by [placeholder]*
```

### 1:1 -- Private Notes

```markdown
### 1:1 Notes -- [Person] & [Person]

**Date:** [date]

**Topics discussed:**
- [Topic 1]: [key points]
- [Topic 2]: [key points]

**Feedback given:**
- [Feedback point]

**Development / goals:**
- [Goal or development item discussed]

**Actions:**
- [Action 1] -- [Owner] -- by [date]

**Mood / energy check:** [if discussed]

*These notes are private and not for wider distribution.*
```

### Sprint Retro -- Retro Summary

```markdown
### Sprint Retro Summary

**Sprint:** [number/name if mentioned]
**Date:** [date]
**Team:** [attendees]

**What went well:**
- [Item 1]
- [Item 2]

**What didn't go well:**
- [Item 1]
- [Item 2]

**Themes identified:**
- [Theme 1 -- e.g., "Communication gaps between frontend and backend"]
- [Theme 2]

**Actions to improve:**
| Action | Owner | Deadline |
|--------|-------|----------|
| [Action] | [Name] | [Date] |

**Carry forward to next retro:**
- [Item to revisit]
```

### Sales Call -- CRM Update

```markdown
### CRM Update

**Company:** [name]
**Contact:** [name, role]
**Date:** [date]
**Stage:** [Discovery / Proposal / Negotiation / Closed]

**Needs identified:**
- [Need 1]
- [Need 2]

**Objections raised:**
- [Objection 1] -- response: [how it was addressed]

**Budget:** [if discussed]
**Timeline:** [if discussed]
**Decision maker:** [if identified]

**Next steps:**
- [Action 1] -- by [date]

**Follow-up date:** [date]
**Probability:** [High/Med/Low]
```

### Interview -- Scorecard Summary

```markdown
### Interview Scorecard

**Candidate:** [name]
**Role:** [position]
**Date:** [date]
**Interviewer(s):** [names]

**Assessment areas:**

| Area | Rating (1-5) | Notes |
|------|-------------|-------|
| Technical skills | [rating] | [brief notes] |
| Communication | [rating] | [brief notes] |
| Culture fit | [rating] | [brief notes] |
| Problem solving | [rating] | [brief notes] |
| Experience relevance | [rating] | [brief notes] |

**Strengths:**
- [Strength 1]

**Concerns:**
- [Concern 1]

**Overall recommendation:** Advance / Hold / Pass
**Notes:** [any additional context]
```

---

## Tone Rules

- Professional but not corporate. Write like a competent human, not a template.
- Concise. No waffle, no filler, no "I hope this email finds you well."
- UK English by default (organise, colour, behaviour, programme).
- Match the formality of the original notes. Casual meeting = slightly less formal output. Board meeting = formal.
- Action items are direct. "Send the report to Sarah by Friday" not "It would be great if you could look into sending the report."

---

## Edge Cases

- **No attendees mentioned:** Note "Attendees not specified in notes" and proceed.
- **No clear actions:** State "No explicit action items identified" and suggest potential actions based on discussion.
- **Single attendee notes (self-notes):** Skip follow-up emails. Produce summary, actions, and agenda only.
- **Very short notes (< 3 lines):** Ask one clarifying question: "These are quite brief -- is there anything else you remember from the meeting, or shall I work with what's here?"
- **Contradictory information:** Flag contradictions explicitly. "Note: the timeline was mentioned as both 2 weeks and 1 month. Please clarify."
- **Sensitive content:** Process without editorialising. Do not flag content as sensitive unless it contains personal data that should not be in a meeting summary (e.g., salary figures in a group email).

---

## Disclaimer

This skill processes meeting notes you provide. It does not record, transcribe, or access meetings directly. Ensure you have permission to share meeting content before pasting notes.

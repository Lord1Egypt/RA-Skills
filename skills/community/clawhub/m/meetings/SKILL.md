---
name: Meetings
description: Build a personal meeting system for capturing notes, preparing agendas, and never missing follow-ups.
metadata: {"clawdbot":{"emoji":"🤝","os":["linux","darwin","win32"]}}
---

## Core Behavior
- User shares transcript/audio → extract key points and action items
- User has upcoming meeting → help prepare with context
- Proactively alert about meetings and pending follow-ups
- Create `~/meetings/` as workspace

## File Structure
```
~/meetings/
├── upcoming/
│   └── 2024-02-15-client-review.md
├── past/
│   └── 2024/
├── recurring/
│   └── weekly-standup.md
├── people/
│   └── sarah-chen.md
└── follow-ups.md
```

## After Meeting Capture
User pastes transcript or describes meeting:
```markdown
# 2024-02-11-product-sync.md
## Meeting
Product Sync with Engineering

## Date
February 11, 2024, 2:00 PM

## Attendees
Sarah, Mike, Lisa

## Key Points
- Launch pushed to March 15 (was March 1)
- Need additional QA resources
- Design approved, no changes

## Decisions Made
- Hire contractor for QA
- Keep current feature scope

## Action Items
- [ ] Sarah: Send contractor requirements by Wed
- [ ] Mike: Update timeline in Jira
- [ ] Me: Notify stakeholders of new date

## Open Questions
- Budget approval for contractor?

## Next Meeting
Feb 18, same time
```

## Quick Capture
From voice or brief text:
"Just had product sync. Launch moved to March 15. Sarah handling QA contractor. I need to notify stakeholders."

→ Auto-organize into structured format
→ Extract action items
→ Flag follow-ups

## Pre-Meeting Prep
Before scheduled meeting, surface:
```markdown
# Prep: Client Review (Tomorrow 10am)
## Context
- Last met: Jan 15
- Project: Website redesign
- Status: Phase 2, 60% complete

## From Last Meeting
- They wanted mobile mockups — did we deliver?
- Budget concern raised — was it resolved?

## Open Action Items
- [ ] Send revised timeline (was due last week)

## Their Recent Activity
- Sarah emailed about invoice Tuesday

## Suggested Agenda
1. Phase 2 progress update
2. Mobile mockups review
3. Timeline discussion
4. Budget clarification
```

## Follow-ups Tracking
```markdown
# follow-ups.md
## Overdue
- [ ] Send stakeholder update (due Feb 10) — Product Sync
- [ ] Review contract terms (due Feb 8) — Legal Call

## Due This Week
- [ ] Contractor requirements to Sarah (Wed)
- [ ] Timeline update (Fri)

## Waiting On Others
- Mike: Jira update
- Lisa: Design assets
```

## Recurring Meetings
```markdown
# recurring/weekly-standup.md
## Meeting
Weekly Team Standup

## Schedule
Mondays 9:00 AM

## Usual Attendees
Full product team

## Running Notes
### Feb 11
- Sprint on track
- John out next week

### Feb 4
- Delayed by design review
- Added Lisa to project
```

## People Context
```markdown
# people/sarah-chen.md
## Role
VP Product, Acme Corp

## Meeting History
- Feb 11: Product sync — discussed launch delay
- Jan 15: Kickoff — aligned on scope

## Communication Style
- Prefers concise updates
- Wants data to back decisions

## Notes
- Reports to CEO directly
- Budget authority up to $50k
```

## Proactive Alerts
- "Meeting with Sarah in 2 hours — prep ready"
- "3 overdue follow-ups from last week"
- "You promised Mike an update by today"
- "Recurring standup in 30 minutes"

## What To Extract
From transcripts/audio:
- Decisions made
- Action items (who, what, when)
- Open questions
- Key discussion points
- Next meeting date

## What To Surface
- Prep notes before meetings
- Overdue and upcoming follow-ups
- Context on attendees
- Promises you made

## Progressive Enhancement
- Start: capture notes after meetings
- Track action items and follow-ups
- Add prep for important meetings
- Build context on recurring attendees

## What NOT To Do
- Let action items disappear
- Go into meetings without context
- Forget promises made
- Miss recurring meeting patterns

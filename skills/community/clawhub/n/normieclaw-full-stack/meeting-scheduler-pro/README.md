# Meeting Scheduler Pro

**Your AI meeting co-pilot. Not just a booking link.**

Meeting Scheduler Pro is a NormieClaw tool package for [OpenClaw](https://openclaw.com) that handles the full meeting lifecycle: prep → schedule → agenda → follow-up. It connects to Google Calendar via the `gog` CLI, manages your availability through natural conversation, preps you before every call, generates agendas, and creates follow-up tasks when the meeting ends.

## What It Does

- **Scheduling:** "Schedule a 30-min call with Sarah next week" → checks your calendar, suggests 3 available slots, books it when you confirm
- **Availability:** Define working hours, buffer time, no-meeting blocks. Share availability conversationally — no booking page needed
- **Meeting Prep:** Before every meeting, get a brief: who you're meeting, their role, last interaction notes, suggested talking points, recent company news
- **Agendas:** Auto-generate meeting agendas based on purpose, past conversations, and open action items
- **Follow-Up:** After meetings, capture action items, create tasks (pairs with Project Manager Pro), draft follow-up emails
- **Smart Suggestions:** "You have 4 meetings back-to-back with no breaks — want me to add buffers?"

## Quick Start

1. **Install:** Add the `meeting-scheduler-pro` skill to your OpenClaw agent
2. **Run setup:** `bash scripts/setup.sh`
3. **Authenticate:** `gog auth login` (Google Calendar access)
4. **Configure:** Walk through the setup prompt or edit `config/settings.json` directly
5. **Go:** "What meetings do I have tomorrow?" or "Schedule a call with John next week"

## Requirements

- OpenClaw installed and running
- `gog` CLI authenticated with Google Calendar
- Google Calendar as your primary calendar

## Optional Integrations

- **Relationship Buddy** (NormieClaw) — enriches meeting prep with contact history and relationship context
- **Project Manager Pro** (NormieClaw) — receives follow-up tasks created after meetings

## What's Included

```
meeting-scheduler-pro/
├── SKILL.md              # Full agent instructions (core file)
├── SETUP-PROMPT.md       # Guided first-run configuration
├── README.md             # This file
├── SECURITY.md           # Security considerations
├── config/
│   └── settings.json     # Your availability and preferences
├── scripts/
│   ├── setup.sh          # Initial setup and validation
│   ├── export-schedule.sh  # Export meetings to markdown
│   └── weekly-agenda.sh    # Week-ahead meeting prep
├── examples/
│   ├── example-schedule-meeting.md
│   ├── example-meeting-prep.md
│   └── example-follow-up.md
└── dashboard-kit/
    ├── manifest.json
    └── DASHBOARD-SPEC.md
```

## Replaces

| Tool | Annual Cost | What You Lose | What You Gain |
|------|-------------|---------------|---------------|
| Calendly Standard | $96/yr | Round-robin, CRM integrations | AI meeting prep, agendas, follow-ups |
| SavvyCal Basic | $144/yr | Calendar overlay for invitees | Full meeting lifecycle automation |
| Reclaim.ai Starter | $96/yr | Auto-task scheduling | Meeting prep + follow-up engine |
| **Total replaced** | **~$240/yr** | | **$49 one-time** |

## Dashboard

Meeting Scheduler Pro includes dashboard metrics (prefix: `ms_`) for meeting frequency trends, prep completion rates, follow-up tracking, and calendar health scores. See `dashboard-kit/DASHBOARD-SPEC.md` for details.

## Support

This is a NormieClaw tool package. For questions, visit [normieclaw.ai](https://normieclaw.ai).

## License

Proprietary — NormieClaw. All rights reserved.

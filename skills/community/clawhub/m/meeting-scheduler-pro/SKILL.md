# Meeting Scheduler Pro — SKILL.md

> Your AI meeting co-pilot. Not just a booking link.

Meeting Scheduler Pro handles the full meeting lifecycle: prep → schedule → agenda → follow-up. It connects to Google Calendar via the `gog` CLI, manages your availability through conversation, preps you before every call, generates agendas, and creates follow-up tasks when the meeting ends.

---

## Prerequisites

- **OpenClaw** installed and running
- **gog CLI** authenticated with Google Calendar (`gog auth login`)
- **Google Calendar** as your primary calendar
- **config/settings.json** configured with your availability preferences (see Setup)

### Optional Integrations

- **Relationship Buddy** (NormieClaw) — enriches meeting prep with contact history and relationship notes
- **Project Manager Pro** (NormieClaw) — receives follow-up tasks created after meetings

---

## Setup

1. Run the setup script:
   ```bash
   bash scripts/setup.sh
   ```
2. Authenticate gog with Google Calendar:
   ```bash
   gog auth login
   ```
3. Verify calendar access:
   ```bash
   gog calendar list
   ```
4. Edit `config/settings.json` with your working hours, buffer preferences, and meeting defaults.

---

## Core Capabilities

### 1. Calendar Integration

All calendar operations use the `gog` CLI. The agent reads, writes, and queries Google Calendar directly.

**Reading Events:**
```bash
# Today's meetings
gog calendar events list --from today --to today

# This week
gog calendar events list --from "Monday" --to "Friday"

# Specific date range
gog calendar events list --from "2026-03-15" --to "2026-03-22"
```

**Creating Events:**
```bash
gog calendar events create \
  --title "Call with Sarah — Q3 Roadmap" \
  --start "2026-03-18T10:00:00" \
  --end "2026-03-18T10:30:00" \
  --description "Discuss Q3 roadmap priorities and timeline" \
  --attendees "sarah@example.com"
```

**Checking Availability:**
```bash
# Pull events for a date range, then compute open slots against settings.json availability
gog calendar events list --from "2026-03-16" --to "2026-03-20"
```

The agent parses event output and cross-references with your availability windows defined in `config/settings.json` to identify open slots.

---

### 2. Scheduling Engine

The scheduling engine handles the full booking conversation. When a user requests a meeting, the agent:

1. **Parses the request** — extracts attendee(s), duration, preferred timeframe, topic
2. **Checks availability** — pulls calendar events for the requested window, applies availability rules from settings.json
3. **Suggests 3 slots** — prioritizes morning/afternoon preference, avoids back-to-back without buffers, respects no-meeting blocks
4. **Handles negotiation** — if the user or attendee rejects all slots, expands the search window and offers alternatives
5. **Creates the event** — books it on Google Calendar with title, description, attendees, and any video link

#### Scheduling Flow

**Step 1: Parse the Request**

When the user says something like "Schedule a 30-min call with Sarah next week about the roadmap," extract:
- **Who:** Sarah (resolve to email from contacts or ask)
- **Duration:** 30 minutes
- **When:** Next week (Monday–Friday of the following week)
- **Topic:** Roadmap discussion
- **Type:** Call (add video link if configured)

**Step 2: Check Calendar & Suggest Slots**

Query the date range via `gog calendar events list`, parse occupied blocks, and apply settings.json rules (working hours, buffers, no-meeting blocks, lunch).

Present 3 options with context:

```
Here are 3 open slots for a 30-min call with Sarah next week:

1. Monday Mar 16, 10:00–10:30 AM — light morning, no adjacent meetings
2. Tuesday Mar 17, 2:00–2:30 PM — 1-hour gap before your next call
3. Thursday Mar 19, 11:00–11:30 AM — open morning block

Which works? Or want me to look at different times?
```

**Step 4: Book It**

Once confirmed:
```bash
gog calendar events create \
  --title "Call with Sarah — Roadmap Discussion" \
  --start "2026-03-16T10:00:00" \
  --end "2026-03-16T10:30:00" \
  --description "Discuss Q3 roadmap priorities and timeline.\n\nAgenda will be generated before the meeting." \
  --attendees "sarah@example.com"
```

Confirm with: event title, date/time, attendee, and note that prep/agenda will be generated.

#### Edge Cases

- **No email:** Ask for the attendee's email before booking
- **Fully booked:** Expand to the next week and offer alternatives
- **Conflicting preferences:** Note the conflict and suggest the next-best option
- **Recurring:** Offer to make it recurring if the topic suggests regularity

---

### 3. Availability Management

Availability rules live in `config/settings.json`. The agent reads these before every scheduling decision.

See `config/settings.json` for the full structure: working hours, timezone, buffer minutes, no-meeting blocks (day/start/end/label), preferred times for external vs internal, max meetings per day, and lunch block.

#### Dynamic Availability Updates

Users can update availability through conversation:

- "Block off Friday afternoons for focus time" → Agent updates settings.json
- "I'm out of office March 20–22" → Agent checks for conflicts and blocks the dates
- "No meetings before 10 AM this week" → Agent applies a temporary override

#### Availability Sharing

When someone asks for your availability (via the agent), format it conversationally:

```
Sarah asked when you're free next week for a 30-min call. Here's what I'd share:

Available slots:
- Mon 10:00–11:30 AM
- Tue 2:00–4:00 PM
- Thu 9:00–11:00 AM
- Fri 10:00–12:00 PM

Want me to send these options, or adjust anything first?
```

No booking page required — the agent handles the back-and-forth. If the user wants a booking page, generate a simple availability summary they can share.

---

### 4. Meeting Prep

Before every meeting, the agent generates a prep brief. This runs automatically when triggered by a cron/heartbeat check, or on demand when the user asks "What's my next meeting?"

#### Prep Brief Structure

```
📋 MEETING PREP: Call with Sarah Chen
📅 Monday Mar 16, 10:00–10:30 AM
📍 Google Meet (link)

👤 ATTENDEE
- Sarah Chen, VP Product at Acme Corp
- Last met: Feb 3, 2026 (Q2 planning call)
- Connected via: LinkedIn, mutual intro from David

📝 LAST INTERACTION NOTES
- Discussed Q2 product roadmap timeline concerns
- She flagged resource constraints on the mobile team
- Agreed to revisit in 6 weeks (this meeting)

💡 SUGGESTED TALKING POINTS
1. Follow up on mobile team resourcing — did they hire?
2. Q3 roadmap priorities she wants to align on
3. Timeline for the API v2 launch she mentioned last time

⚡ CONTEXT
- Acme Corp announced Series C last month ($45M)
- Their Q1 earnings call mentioned expanding developer tools
- You have an open proposal with them (sent Feb 15)
```

#### Data Sources for Prep

The agent gathers prep context from available sources:

1. **Google Calendar** — meeting title, description, attendees, past meetings with same attendee
2. **Relationship Buddy** (if installed) — contact notes, interaction history, relationship score
3. **Web search** (if enabled) — recent news about the attendee's company, LinkedIn profile context
4. **Meeting history** — past agendas and follow-up notes stored locally
5. **Email context** (via gog) — recent email threads with the attendee

Use `gog calendar events list --query "<name>"` for past meetings and `gog gmail search --query "from:<email>"` for recent emails.

#### When Prep Runs

- **Automated:** Agent checks tomorrow's calendar each evening and preps briefs for all meetings
- **On-demand:** User asks "Prep me for my 2 PM" or "What do I need to know about tomorrow?"
- **Morning brief:** Included in daily briefing if configured — "You have 3 meetings today. Here are your prep briefs."

---

### 5. Agenda Generation

For meetings you're hosting, the agent auto-generates an agenda based on context.

#### Agenda Structure

```
📋 AGENDA: Q3 Roadmap Discussion with Sarah Chen
📅 Monday Mar 16, 10:00–10:30 AM

1. Check-in (2 min)
   - How's the team doing after Q2 push?

2. Q2 Retrospective (8 min)
   - What shipped vs. what slipped
   - Mobile team capacity update

3. Q3 Priorities (12 min)
   - Top 3 roadmap items to align on
   - API v2 timeline and dependencies
   - Resource allocation for new initiatives

4. Open Questions (5 min)
   - Partnership proposal status
   - Any blockers you need help with?

5. Next Steps & Follow-up (3 min)
   - Action items
   - Schedule follow-up if needed

Total: 30 min
```

#### Agenda Generation Logic

1. **Parse meeting purpose** from title and description
2. **Review past meeting notes** with same attendee(s)
3. **Check for open action items** from previous meetings
4. **Allocate time proportionally** based on meeting duration
5. **Include standing items** (check-in, next steps) for recurring meetings
6. **Add open questions** from recent email threads or notes

#### Sharing Agendas

Add the agenda to the calendar event description via `gog calendar events update`, email it to attendees via `gog gmail send`, or both. Always ask the user: "Want me to add this to the invite, email it, or both?"

---

### 6. Follow-Up Engine

After a meeting ends, the agent initiates follow-up. This triggers based on calendar events ending or the user saying "Just got off a call with Sarah."

#### Follow-Up Flow

**Step 1: Check In**
```
Your call with Sarah just ended. How'd it go? Any action items?
```

**Step 2: Capture Notes**
User responds naturally: "Good call. She needs the API docs by Friday. We agreed to push the mobile launch to April. I need to send her the updated timeline."

**Step 3: Parse and Create Tasks**

Extract action items and create structured follow-ups:

```
Got it. Here's what I captured:

Action Items:
1. ☐ Send API docs to Sarah — due Friday Mar 20
2. ☐ Update mobile launch timeline to April — no due date
3. ☐ Send Sarah the updated timeline — due this week

Follow-up Meeting:
- Sarah mentioned revisiting in 2 weeks. Want me to schedule a 30-min follow-up for week of March 30?

Shall I create these tasks in Project Manager Pro?
```

**Step 4: Create Tasks (if Project Manager Pro is installed)**

```bash
# Tasks are created via Project Manager Pro's task creation interface
# The agent formats tasks and passes them to the PM Pro skill
```

If Project Manager Pro isn't installed, tasks are stored as a local note:
```
Follow-up notes saved to: meeting-notes/2026-03-16-sarah-chen-roadmap.md
```

**Step 5: Send Follow-Up Email (optional)**

```
Want me to send Sarah a follow-up email? Here's a draft:

---
Subject: Follow-up: Q3 Roadmap Discussion

Hi Sarah,

Great chatting today. Here's a quick recap:

- I'll send over the API docs by Friday
- We're aligning on an April timeline for the mobile launch
- I'll share the updated timeline this week

Let me know if I missed anything. Talk soon.
---

Send it, edit it, or skip?
```

#### Follow-Up Note Storage

Notes are saved as `meeting-notes/YYYY-MM-DD-attendee-topic.md` with: date, attendees, discussion points, action items (owner + due date), decisions, and next meeting date. These feed back into future meeting prep for the same attendees. See `examples/example-follow-up.md` for a full example.

---

### 7. Smart Suggestions

The agent proactively monitors your calendar and offers suggestions. These surface during daily briefings, heartbeat checks, or when you interact with the scheduler.

#### Calendar Health Checks

**Back-to-back detection:**
```
⚠️ Heads up — you have 4 meetings back-to-back Tuesday (9 AM to 1 PM) with no breaks.
Want me to add 10-min buffers between them? Or move the 11:30 to 2 PM?
```

**Overloaded day warning:**
```
Wednesday has 7 meetings scheduled. Your max is 6.
The least critical one looks like "Team Social Planning" at 4 PM.
Want me to suggest rescheduling it?
```

**Meeting-free day protection:**
```
You have no meetings Friday — nice! Want me to block it as a focus day
so nothing gets booked?
```

**Recurring meeting audit:**
```
You have 3 recurring weekly meetings that haven't had agenda updates in 4+ weeks:
1. Monday standup with Dev Team
2. Wednesday sync with Marketing
3. Friday review with Ops

Worth checking if any of these can go async or biweekly?
```

**Stale relationship nudge:**
```
You haven't met with David Park in 8 weeks. Last meeting was about the
partnership deal. Want me to schedule a 15-min check-in?
```

#### Suggestion Triggers

- **Morning brief:** Calendar health check for today + tomorrow
- **Evening prep:** Next-day meeting prep and conflict detection
- **Weekly review:** Friday afternoon calendar audit for the next week (via `scripts/weekly-agenda.sh`)
- **On scheduling:** When booking a new meeting, flag conflicts or back-to-back issues

---

### 8. Dashboard Integration

Meeting Scheduler Pro tracks metrics for the NormieClaw dashboard.

All 12 metrics are defined in `dashboard-kit/manifest.json` (prefix: `ms_`). Key metrics: meetings today/week, prep completion rate, pending/completed follow-ups, avg meetings/day, busiest day/hour, no-show rate, buffer compliance, agent-booked count, reschedule count.

#### Dashboard Views

See `dashboard-kit/DASHBOARD-SPEC.md` for full visualization specs:
- **Weekly meeting heatmap** — grid showing meeting density by day/hour
- **Meeting frequency trend** — line chart of meetings per week over time
- **Prep completion tracker** — bar chart showing prep rate by week
- **Follow-up pipeline** — kanban-style view of pending vs completed follow-ups
- **Calendar health score** — composite score based on buffer compliance, meeting density, focus time

---

## Conversational Interface Reference

### Scheduling Commands

| User Says | Agent Does |
|-----------|-----------|
| "Schedule a call with Sarah next week" | Checks calendar, suggests 3 slots, books on confirmation |
| "Find 30 minutes for me and John Tuesday" | Scans Tuesday availability, offers slots |
| "Book a 1-hour meeting with the team on Thursday" | Creates group event, sends invites |
| "Reschedule my 2 PM to Friday" | Finds Friday slots, moves the event |
| "Cancel tomorrow's standup" | Confirms and deletes the event |
| "What's my availability next week?" | Generates shareable availability summary |
| "Block off Friday afternoon" | Adds a calendar block, updates settings |

### Prep Commands

| User Says | Agent Does |
|-----------|-----------|
| "Prep me for my next meeting" | Generates prep brief for the next upcoming meeting |
| "What do I need to know about tomorrow?" | Preps all of tomorrow's meetings |
| "Who am I meeting with today?" | Lists today's meetings with attendee context |
| "Generate an agenda for my 10 AM" | Creates and optionally shares an agenda |

### Follow-Up Commands

| User Says | Agent Does |
|-----------|-----------|
| "Just got off a call with Sarah" | Initiates follow-up: asks how it went, captures action items |
| "Meeting with John went great, follow up on the proposal" | Creates task, drafts follow-up email |
| "What action items do I have open?" | Lists all pending follow-up tasks |
| "Send Sarah a follow-up" | Drafts and optionally sends follow-up email |

### Calendar Health Commands

| User Says | Agent Does |
|-----------|-----------|
| "How's my week looking?" | Calendar overview with health check |
| "Am I overbooked?" | Checks against meeting limits, flags issues |
| "Audit my recurring meetings" | Reviews recurring meetings for relevance |
| "Who haven't I met with recently?" | Flags stale relationships based on meeting history |

---

## Integration Points

### Relationship Buddy (NormieClaw)

If Relationship Buddy is installed, Meeting Scheduler Pro pulls:
- Contact notes and relationship history
- Last interaction date and context
- Relationship health score
- Suggested topics based on past conversations

This enriches meeting prep significantly. Without Relationship Buddy, prep relies on calendar history, email context, and web search.

### Project Manager Pro (NormieClaw)

If Project Manager Pro is installed, follow-up tasks are created directly in the task management system:
- Tasks with owners, due dates, and meeting context
- Linked to the originating meeting for traceability
- Included in PM Pro's dashboard metrics

Without PM Pro, tasks are stored as local markdown files.

### Daily Briefing

Meeting Scheduler Pro contributes to the daily briefing:
- Today's meeting count and schedule
- Prep briefs for morning meetings
- Any calendar conflicts or warnings
- Pending follow-up tasks from yesterday

---

## Scripts Reference

### setup.sh
Validates gog installation, checks calendar auth, creates config directory, initializes settings.json with defaults. Run once during installation.

### export-schedule.sh
Exports upcoming meetings (default: next 7 days) to a formatted markdown file. Useful for sharing your schedule or generating a weekly overview.

```bash
bash scripts/export-schedule.sh           # Next 7 days
bash scripts/export-schedule.sh 14        # Next 14 days
bash scripts/export-schedule.sh 7 /tmp/schedule.md  # Custom output path
```

### weekly-agenda.sh
Generates a week-ahead meeting prep document. Pulls next week's meetings, generates prep briefs for each, identifies conflicts, and outputs a comprehensive planning document.

```bash
bash scripts/weekly-agenda.sh             # Next week
bash scripts/weekly-agenda.sh 2026-03-23  # Specific week start date
```

---

## Configuration Reference

All settings live in `config/settings.json`. See the file directly for field names, types, and defaults. Key sections:

- **availability** — working hours, timezone, buffer minutes, no-meeting blocks, lunch block, max meetings/day, preferred times for external vs internal meetings
- **meeting_defaults** — default duration, video link, reminder minutes
- **prep** — auto-prep toggle, web search toggle, email context toggle
- **followup** — auto-prompt toggle, task creation toggle, email draft toggle
- **notes_directory** — where meeting notes are stored
- **integrations** — flags for Relationship Buddy and Project Manager Pro

---

## Troubleshooting

### "gog: command not found"
Install gog: `npm install -g gog` or check your OpenClaw installation — gog should be bundled.

### "Calendar access denied"
Re-authenticate: `gog auth login` — make sure you grant calendar read/write permissions.

### "No events found"
Check that you're querying the correct calendar. `gog calendar list` shows all available calendars. If you use multiple calendars, specify the calendar ID in your queries.

### Prep brief is thin
Prep quality depends on available data. For richer briefs:
- Install Relationship Buddy for contact history
- Enable email context in settings.json
- Enable web search for company news
- Build meeting history by using follow-up features consistently

### Agent suggests times outside working hours
Check `config/settings.json` — ensure `working_hours` and `timezone` are set correctly.

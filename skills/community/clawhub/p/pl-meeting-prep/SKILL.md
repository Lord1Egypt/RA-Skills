---
name: meeting-prep-agent
description: Pre-meeting research, agenda generation, talking points, and post-meeting action item capture. Use when preparing for client meetings, internal reviews, board presentations, vendor negotiations, or stakeholder briefings. Produces structured briefs, agendas, and follow-up documents. NOT for: scheduling (use calendar tools), recurring standup notes, or meetings where you have no context on participants or purpose.
version: 1.0.0
author: PrecisionLedger
tags:
  - meetings
  - productivity
  - research
  - crm
  - accounting
---

# Meeting Prep Agent

Automates pre-meeting research, agenda creation, and post-meeting action tracking. Designed for finance professionals, client advisors, and operations leads who need to show up prepared every time.

---

## When to Use

**Fire this skill when:**
- Irfan has an upcoming client meeting and needs a brief
- Preparing for board, investor, or lender presentations
- Vendor or contract negotiations require background research
- Internal team reviews need structured agendas
- Post-meeting — capturing decisions and action items while context is fresh

**Do NOT use when:**
- Scheduling or rescheduling meetings (use calendar tools)
- Recurring standups with no variable agenda
- Meetings where purpose and participants are completely unknown (need at least a name and topic)
- Real-time meeting facilitation or live note-taking (this is async prep, not live tooling)

---

## Inputs Required

| Field | Required | Example |
|---|---|---|
| Meeting type | Yes | client, board, vendor, internal |
| Participant names/companies | Yes | "John Smith, Apex Roofing" |
| Meeting topic/purpose | Yes | "Q1 financial review" |
| Date/time | Recommended | "Tuesday 2 PM CST" |
| Prior context | Optional | past invoices, notes, deals |
| Duration | Optional | 30 min, 1 hour |

---

## Workflow

### 1. Pre-Meeting Research Brief

Given participant names and company, compile:

```
MEETING BRIEF — [Company Name]
Date: [Date/Time]
Duration: [Duration]
Participants: [Names + Titles]

COMPANY SNAPSHOT
- Industry / Business type
- Size (employees, revenue range if public)
- Key services or products
- Recent news (last 90 days)

RELATIONSHIP HISTORY
- How long as client/prospect
- Prior engagements, invoices, or projects
- Any open issues, disputes, or pending items
- Last communication date and topic

MEETING PURPOSE
- Primary objective (decision, update, pitch, review)
- Secondary objectives
- Success criteria: what does a good outcome look like?

RISK FLAGS
- Overdue invoices or AR exposure
- Compliance issues pending
- Known sensitivities or pain points
```

### 2. Agenda Generation

```
AGENDA — [Meeting Name]
[Date] | [Time] | [Duration]

0:00 — Welcome & introductions (2 min)
0:02 — [Topic 1]: [brief descriptor] (X min)
0:XX — [Topic 2]: [brief descriptor] (X min)
...
X:XX — Open questions / next steps (5 min)
X:XX — Action item review & close (3 min)

Prepared materials: [list any decks, reports, or data needed]
Pre-read for participants: [if any]
```

### 3. Talking Points

For each agenda item, produce:

```
TOPIC: [Name]

KEY POINT: [The single most important thing to communicate]

SUPPORTING DATA:
- [Stat, figure, or fact #1]
- [Stat, figure, or fact #2]

ANTICIPATED QUESTIONS:
- Q: [likely question]
  A: [prepared response]
- Q: [likely pushback]
  A: [response + fallback]

DESIRED OUTCOME: [What you want decided or agreed by end of this item]
```

### 4. Post-Meeting Action Items

Capture immediately after the meeting:

```
MEETING SUMMARY — [Meeting Name]
Date: [Date]
Attendees: [Names]

DECISIONS MADE:
- [Decision 1]
- [Decision 2]

ACTION ITEMS:
| # | Task | Owner | Due Date | Priority |
|---|------|-------|----------|----------|
| 1 | [Task] | [Name] | [Date] | High/Med/Low |

FOLLOW-UPS REQUIRED:
- Send [document/report] to [person] by [date]
- Schedule [next meeting] for [timeframe]

OPEN ITEMS (unresolved):
- [Issue requiring further discussion]

NOTES:
[Any additional context, commitments, or flags]
```

---

## Usage Examples

### Example 1: Client Financial Review Meeting

**Trigger:** "Prep me for Tuesday's meeting with Apex Roofing — Q1 financial review."

**Agent actions:**
1. Research Apex Roofing (industry, size, recent news)
2. Pull any prior invoices, communications, or notes from memory/files
3. Generate 1-page brief with company snapshot + relationship history
4. Draft agenda: Q1 P&L walkthrough → budget vs. actuals → Q2 projections → questions
5. Create talking points for each section with anticipated CFO-level questions
6. Flag any overdue AR or open compliance items as risk flags

**Output:** PDF-ready brief + agenda in `memory/meeting-prep/YYYY-MM-DD-apex-roofing.md`

---

### Example 2: Vendor Contract Negotiation

**Trigger:** "Prep for Thursday's negotiation with SaaS vendor over annual contract renewal."

**Agent actions:**
1. Research vendor (market position, competitor alternatives, pricing benchmarks)
2. Pull current contract terms from memory or files
3. Identify leverage points (renewal timing, usage data, alternatives available)
4. Draft negotiation agenda: current terms review → pain points → desired terms → fallback positions
5. Talking points with BATNA (Best Alternative to Negotiated Agreement) framing

---

### Example 3: Post-Meeting Debrief

**Trigger:** "We just finished the call with John Smith. Here's what happened: [notes dump]."

**Agent actions:**
1. Parse raw notes into structured format
2. Extract and classify: decisions, action items, open items
3. Assign owners and due dates based on context
4. Draft follow-up email copy for Irfan's review (not sent — for approval)
5. Update memory file with relationship context

---

## Output Files

Save all prep materials to:
```
memory/meeting-prep/YYYY-MM-DD-[company-slug].md
```

For recurring clients, maintain a running log:
```
memory/clients/[company-slug]/meeting-log.md
```

---

## Integration Points

- **Calendar:** Read upcoming meetings from gog (Google Calendar) to proactively trigger prep
- **CRM/Notes:** Pull prior client context from memory files or Obsidian
- **Financial data:** Reference AR aging, invoice history, budget files
- **Web research:** Use web_search for recent news on company/participants
- **Email:** Draft follow-up emails for Irfan's review (never send without approval)

---

## Proactive Mode

When integrated with heartbeat:
- Each morning, check calendar for meetings in next 24 hours
- For any meeting >30 min with named participants, auto-generate brief and flag in heartbeat summary
- Alert format: "📋 Meeting prep ready: Apex Roofing (2 PM today) — brief in memory/meeting-prep/"

---

## Quality Standards

- All research must cite source or note "from memory files" vs "web research"
- Talking points should be crisp — one key message per topic, not a wall of text
- Action items must have owner + due date — unassigned tasks don't get done
- Risk flags are mandatory if any AR, compliance, or relationship issues exist
- Never fabricate contact info, financial figures, or company details — flag as "needs verification" if uncertain

---

## Privacy Rules

- Meeting briefs may contain sensitive client data — never share externally
- Post-meeting summaries go to memory files only, not external channels
- If asked to share a brief with a third party, escalate to Irfan

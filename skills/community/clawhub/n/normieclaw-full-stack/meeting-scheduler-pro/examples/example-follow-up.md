# Example: Post-Meeting Follow-Up

> Capturing action items and creating follow-up tasks after a meeting.

---

## The Conversation

**Agent:** Your call with Sarah Chen just ended (11:00–11:30 AM). How'd it go? Any action items?

**You:** Really productive. She confirmed they hired 2 mobile devs so the April launch is back on track. She wants the updated API spec by Monday. We agreed to do a joint demo for her engineering team — I need to prep a slide deck for that. Oh and the partnership thing — she wants to co-develop an integration between our platforms. She'll send a brief by end of week.

**Agent:** Nice — sounds like things are moving. Here's what I captured:

### Action Items

1. ☐ **Send updated API spec to Sarah** — due Monday Mar 23
   - Owner: You
   - Context: She's reviewing with her engineering lead

2. ☐ **Prep slide deck for joint demo** — due before April 2 (demo date)
   - Owner: You
   - Context: Demo for Acme engineering team, focus on API v2 capabilities

3. ☐ **Review partnership brief from Sarah** — due end of this week (Mar 21)
   - Owner: Sarah (you're waiting on this)
   - Context: Co-development integration between platforms

### Key Decisions

- Mobile launch timeline confirmed: April 2026
- API v2 scope: proceeding with 3 core endpoints (agreed last meeting, reconfirmed)
- Partnership exploration: moving forward — Sarah drafting brief

### Follow-Up Meeting

Sarah mentioned doing a quick sync after she sends the partnership brief. Want me to schedule a 20-min call for the week of March 24?

**You:** Yeah, schedule that. And create the tasks.

**Agent:** Done:

**Tasks created:**
1. ☐ Send updated API spec to Sarah — Mon Mar 23
2. ☐ Prep slide deck for joint demo — before Apr 2
3. ☐ Review partnership brief (waiting on Sarah) — Fri Mar 21

**Follow-up meeting:** I'll find a 20-min slot the week of Mar 24 once Sarah confirms her availability. I'll reach out to schedule.

**Draft follow-up email:**

> Subject: Follow-up: Q3 Roadmap Discussion
>
> Hi Sarah,
>
> Great catching up today. Quick recap:
>
> - I'll have the updated API spec over to you by Monday
> - Joint demo for your engineering team — I'll start prepping the deck. April 2 still the target?
> - Looking forward to the partnership brief — exciting direction
>
> Let me know a good time the week of March 24 for a quick follow-up after you send the brief.
>
> Talk soon.

Send this, edit it, or skip?

**You:** Send it.

**Agent:** Sent to sarah.chen@acme.com. Meeting notes saved to `meeting-notes/2026-03-19-sarah-chen-q3-roadmap.md`.

---

## The Saved Meeting Note

File: `meeting-notes/2026-03-19-sarah-chen-q3-roadmap.md`

```markdown
# Call with Sarah Chen — Q3 Roadmap
**Date:** March 19, 2026, 11:00–11:30 AM
**Attendees:** Sarah Chen (VP Product, Acme Corp)

## Key Discussion Points
- Mobile team hired 2 devs, April launch back on track
- API v2 proceeding with 3 core endpoints
- Partnership: co-development integration between platforms
- Sarah drafting partnership brief by end of week

## Decisions Made
- Mobile launch: confirmed April 2026
- API v2 scope: 3 endpoints (reconfirmed)
- Partnership: moving forward pending brief

## Action Items
- [ ] Send updated API spec to Sarah — due Mon Mar 23 (owner: me)
- [ ] Prep slide deck for joint demo — due before Apr 2 (owner: me)
- [ ] Review partnership brief — due Fri Mar 21 (owner: Sarah, I'm waiting)

## Follow-Up
- 20-min sync scheduled for week of Mar 24 (pending Sarah's availability)
- Follow-up email sent Mar 19

## Next Meeting
- Joint demo: April 2, 2026 (with Acme engineering team)
```

---

## What Happened Behind the Scenes

1. Agent detected the calendar event ending and prompted for follow-up
2. Parsed the user's natural language response into structured action items
3. Created tasks (sent to Project Manager Pro if installed, or saved locally)
4. Drafted a follow-up email based on the discussion points
5. Saved a meeting note to the `meeting-notes/` directory
6. Queued a scheduling request for the follow-up meeting
7. Updated dashboard metrics: follow-up completed, tasks created

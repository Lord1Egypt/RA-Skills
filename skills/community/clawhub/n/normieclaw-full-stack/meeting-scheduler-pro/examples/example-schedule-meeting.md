# Example: Scheduling a Meeting

> A full scheduling conversation from request to confirmation.

---

## The Conversation

**You:** Schedule a 30-minute call with Sarah Chen next week to discuss the Q3 roadmap.

**Agent:** Let me check your calendar for next week...

Your availability next week (Mon Mar 16 – Fri Mar 20):

Here are 3 open slots for a 30-min call:

1. **Monday Mar 16, 10:00–10:30 AM** — light morning, your only meeting is at 2 PM
2. **Tuesday Mar 17, 2:00–2:30 PM** — 90-min gap between your 12:30 and 3:30 meetings
3. **Thursday Mar 19, 11:00–11:30 AM** — open morning, nothing until lunch

Wednesday is blocked (deep work morning) and Friday afternoon is your planning block.

Which works? Or want me to look at different times?

**You:** Tuesday afternoon works. Let's do the 2 PM.

**Agent:** Got it. What's Sarah's email? I'll add her to the invite.

**You:** sarah.chen@acme.com

**Agent:** Booked:

📅 **Call with Sarah Chen — Q3 Roadmap**
🕐 Tuesday Mar 17, 2:00–2:30 PM
👤 sarah.chen@acme.com
📍 Google Meet link attached

I'll generate a prep brief and agenda before the meeting. Anything else to add to the invite?

**You:** Nope, that's good.

**Agent:** Done. I'll prep you Tuesday morning.

---

## What Happened Behind the Scenes

1. Agent parsed the request: attendee (Sarah Chen), duration (30 min), timeframe (next week), topic (Q3 roadmap)
2. Pulled calendar events for Mar 16–20 via `gog calendar events list`
3. Applied availability rules from settings.json:
   - Working hours: 9 AM – 5 PM
   - 15-min buffer between meetings
   - Wednesday 9–12 blocked (deep work)
   - Friday afternoon blocked (planning)
   - Lunch: 12–1 PM
4. Generated 3 slot suggestions prioritizing the user's preference for afternoon external calls
5. On confirmation, created the event via `gog calendar events create`
6. Queued a prep brief and agenda for Tuesday morning

---

## Rescheduling Variant

**You:** Actually, Sarah can't do Tuesday. Move it to Thursday.

**Agent:** Thursday 11:00–11:30 AM was the other open slot. Want me to move it there?

**You:** Yeah.

**Agent:** Moved:

📅 **Call with Sarah Chen — Q3 Roadmap**
🕐 Thursday Mar 19, 11:00–11:30 AM (was Tuesday 2 PM)
👤 sarah.chen@acme.com

Sarah will get an updated invite. Prep brief will now generate Thursday morning.

# Meeting Scheduler Pro — Setup Prompt

> First-run configuration. Walk the user through each section and save to `config/settings.json`.

---

## Step 1: Calendar Connection

Run `gog auth login` and `gog calendar list`. Ask:
- Which calendar is your primary? (If multiple, confirm which to schedule on.)
- Any secondary calendars to check for conflicts? (shared team, personal)

Save the primary calendar ID to settings.json.

## Step 2: Working Hours

Ask:
- Working hours? (default: 9 AM – 5 PM)
- Timezone? (default: America/New_York)
- Lunch block? (default: 12–1 PM)

## Step 3: Meeting Preferences

Ask:
- Default meeting length? (default: 30 min)
- Buffer between meetings? (default: 15 min)
- Max meetings/day before warning? (default: 6)
- External calls — morning or afternoon? (default: morning)
- Default video link? (Google Meet, Zoom, etc.)
- Reminder minutes before meetings? (default: 10)

## Step 4: Protected Time

Ask:
- Recurring blocks to never schedule over? (e.g., "Wednesday mornings for deep work," "Friday afternoons for planning")
- Each block needs: day, start, end, label.
- Any upcoming out-of-office dates?

## Step 5: Meeting Prep

Ask:
- Auto-generate prep briefs before meetings? (recommended: yes)
- Search web for attendee/company news? (recommended: yes)
- Pull recent email threads with attendees? (recommended: yes)
- Use Relationship Buddy? (if installed, enables contact history in prep)

## Step 6: Follow-Up

Ask:
- Prompt for follow-up after meetings? (recommended: yes)
- Auto-create tasks from action items? (recommended: yes)
- Use Project Manager Pro? (if installed, tasks sync there; otherwise local notes)
- Draft follow-up emails? (recommended: yes)

## Step 7: Notes Storage

Ask:
- Where to store meeting notes? (default: `meeting-notes/`)

## Step 8: Confirm & Save

Summarize settings back to the user:

```
📅 Calendar: primary (user@example.com)
🕐 Working hours: 9 AM – 5 PM (America/Denver)
🍽️ Lunch: 12–1 PM | ⏱️ Buffer: 15 min
📊 Max meetings/day: 6
🔇 Protected: Wed 9–12 (deep work)
📋 Auto-prep: ON | ✅ Follow-ups: ON
📁 Notes: meeting-notes/
```

Save to `config/settings.json`. Confirm setup complete.

Try these to verify everything works:
- "What meetings do I have tomorrow?"
- "Schedule a call with [name] next week"
- "How's my week looking?"

The agent will start generating prep briefs automatically for upcoming meetings.

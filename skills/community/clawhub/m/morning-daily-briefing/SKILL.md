---
name: Daily Briefing
description: Creates a morning briefing with priorities, calendar, and key updates
---

# Daily Briefing

You create a concise morning briefing so the user starts their day knowing exactly what matters.

## When Triggered

User says: "Brief me", "Morning briefing", "What's on today?", "Start my day"
Or: run automatically via heartbeat/cron if configured.

## Briefing Template

```
☀️ DAILY BRIEFING — [Day, Month Date, Year]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 TODAY'S SCHEDULE
• [Time] — [Event] ([Location/Link])
• [Time] — [Event] ([Location/Link])
• [No meetings today — deep work day!]

🎯 TOP 3 PRIORITIES
1. [Most important thing]
2. [Second priority]
3. [Third priority]

📧 INBOX HIGHLIGHTS
• [Urgent/important emails worth noting]
• [X unread emails, Y flagged]

📰 RELEVANT NEWS
• [Industry news or updates that matter]

⚡ FOLLOW-UPS DUE
• [Person] — [Action] (was due [date])
• [Person] — [Action] (due today)

💡 HEADS UP
• [Upcoming deadlines this week]
• [Meetings to prep for tomorrow]
• [Anything else worth knowing]
```

## Priority Framework

Rank tasks using this matrix:

| | Urgent | Not Urgent |
|---|--------|------------|
| **Important** | DO FIRST — Calendar conflicts, client emergencies, deadlines today | SCHEDULE — Strategic work, planning, relationship building |
| **Not Important** | DELEGATE/QUICK — Admin tasks, routine replies | SKIP — Time-wasters, low-value meetings |

## Data Sources

Pull from whatever's available:
- **Calendar** — Today's events and tomorrow's early events
- **Email** — Unread count, flagged/urgent messages, key senders
- **CRM** — Follow-ups due (if crm-manager skill is active)
- **Tasks/Notes** — Any tracked to-dos or project notes
- **News** — Industry-relevant headlines via web search
- **Weather** — Quick forecast if relevant

## Rules

- Keep it scannable. The whole briefing should take 60 seconds to read.
- Prioritize ruthlessly. Don't list everything — list what matters.
- If calendar is empty, say so (that's useful info — it's a deep work day).
- If no email access, skip that section. Don't fake it.
- End with something useful — a heads-up about tomorrow or this week.
- Adjust tone to time of day. Morning = energetic. Evening recap = reflective.
- Include time zones if the user works across zones.

## Evening Recap (Optional)

If asked at end of day: "How'd today go?" or "End of day recap"

```
🌙 END OF DAY — [Date]
━━━━━━━━━━━━━━━━━━━━

✅ COMPLETED
• [What got done]

🔄 CARRIED OVER
• [What didn't get done — moves to tomorrow]

📝 NOTES
• [Key decisions, insights, things to remember]

📅 TOMORROW PREVIEW
• [First meeting/deadline]
```

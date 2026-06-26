# Privacy And Access

This skill should be useful without collecting more personal data than necessary.

## Storage Rules

Allowed by default:

- Public event metadata.
- Source links.
- Human-written preferences.
- Run summaries.
- Calendar availability summaries, such as open, tight, or conflict.
- Explicitly approved decisions.

Allowed access method:

- Google Calendar availability lookup for the requested scan window.
- Busy/free windows only, unless the user explicitly asks for event details.
- Google Calendar event creation only when the user explicitly asks to add a specific suggested event.

Not allowed by default:

- Raw private data.
- Private messages.
- Raw calendar event titles, descriptions, attendees, locations, account data, or private notes.
- Unapproved liked/disliked event logs.
- Source or taste-profile suggestions in run notes.

## Calendar Writes

When the user explicitly asks to add a suggested event to Google Calendar, create only the requested event.

Allowed fields:

- Title.
- Time and date.
- Address, or online link when the event is online.
- Description.

Do not invite attendees, create recurring events, add Google Meet, or modify other calendar entries unless the user explicitly asks.

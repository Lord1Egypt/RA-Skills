---
name: meeting-scheduler
description: "Schedule meetings between your owner and another person by coordinating with their PA, finding available slots in both calendars, and sending a calendar invite. Use when: your owner wants to meet with someone, needs to find a common free slot, or asks you to set up a meeting. Handles both PA-to-PA coordination and direct scheduling. Works with any LLM model."
---

# Meeting Scheduler Skill

## Minimum Model
Any model that can follow numbered steps. For timezone reasoning or complex constraints, use a medium model.

---

## Full Flow (6 Steps)

### Step 1 — Understand the Request

Before acting, confirm:
- **Who** to meet with
- **Duration** (default: 30 min if not specified)
- **Timeframe** ("this week", "next week", "mornings only", etc.)
- **Meeting type** (video, in-person, phone)

If the request is vague (e.g. "set up a call with Jane") → ask one clarifying question before proceeding.

---

### Step 2 — Find the Other PA

Check `data/pa-directory.json`:

```bash
python3 -c "
import json, sys
try:
    with open('data/pa-directory.json') as f:
        d = json.load(f)
except FileNotFoundError:
    print('ERROR: data/pa-directory.json not found')
    sys.exit(1)

name = 'PERSON_NAME'  # replace with actual name
matches = [p for p in d.get('pas', []) if name.lower() in p['owner'].lower()]

if not matches:
    print('No PA found for:', name)
else:
    for p in matches:
        print('PA:', p['name'], '| Phone:', p['phone'])
"
```

If no PA found → skip to Step 4 and contact the person directly by email.

---

### Step 3 — Check Your Owner's Availability

```bash
#!/bin/bash
# Get the current time and 7 days from now
TODAY=$(date -u +%Y-%m-%dT%H:%M:%SZ)
NEXT_WEEK=$(date -u -d '+7 days' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null \
  || date -u -v+7d +%Y-%m-%dT%H:%M:%SZ)

# Fetch events and print a sorted list
GOG_ACCOUNT=owner@company.com gog calendar events primary \
  --from "$TODAY" \
  --to "$NEXT_WEEK" \
  2>/dev/null \
  | python3 -c "
import sys, json
try:
    events = json.load(sys.stdin)
except json.JSONDecodeError:
    events = []

# Sort by start time and print each event
print('Upcoming events:')
for e in sorted(events, key=lambda x: x.get('start', {}).get('dateTime', '')):
    start = e.get('start', {}).get('dateTime', '')[:16].replace('T', ' ')
    print(' ', start, '—', e.get('summary', 'Untitled'))
"
```

---

### Step 4 — Contact the Other PA

Propose 3–5 specific slots:

```
"Hey [PA Name], [your owner] would like to meet [their owner] for [duration].
Slots that work:
• [Day Date] at [HH:MM TZ]
• [Day Date] at [HH:MM TZ]
• [Day Date] at [HH:MM TZ]
Do any work? Or what times work best?"
```

If no response within 2 hours on a business day → follow up once.
If still no response after 4 hours → tell your owner and suggest contacting the other person directly.

---

### Step 5 — Book the Meeting

Once both agree on a time:

```bash
# Basic calendar event
GOG_ACCOUNT=owner@company.com gog calendar create primary \
  --summary "Meeting: [Owner A] + [Owner B]" \
  --start "YYYY-MM-DDTHH:MM:SS+00:00" \
  --end "YYYY-MM-DDTHH:MM:SS+00:00" \
  --attendees "other-owner@company.com" \
  --description "Scheduled via PA coordination"
```

For video calls, add the meeting link:
```bash
  --description "Video call: https://meet.google.com/xxx-xxxx-xxx"
```

---

### Step 6 — Confirm Both Sides

```
To your owner:
"✅ Done — [Date] at [Time] with [Person]. Calendar invite sent."

To the other PA:
"✅ Invite sent to [Their Owner] for [Date] [Time]. Let me know if anything changes."
```

---

## Find Available Slots (Script)

```python
#!/usr/bin/env python3
"""Find open meeting slots in the owner's calendar."""
import subprocess, json, sys
from datetime import datetime, timedelta, timezone

OWNER_EMAIL = "owner@company.com"  # replace
DURATION_MIN = 30
DAYS_AHEAD = 7
WORK_START_HOUR = 9
WORK_END_HOUR = 18

# Fetch calendar events
try:
    result = subprocess.run(
        ['gog', 'calendar', 'events', 'primary',
         '--from', datetime.now(timezone.utc).isoformat(),
         '--to', (datetime.now(timezone.utc) + timedelta(days=DAYS_AHEAD)).isoformat()],
        env={'GOG_ACCOUNT': OWNER_EMAIL, 'PATH': '/usr/bin:/usr/local/bin:/bin'},
        capture_output=True, text=True, timeout=30
    )
    events = json.loads(result.stdout) if result.stdout.strip() else []
except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
    print("Could not fetch calendar:", e)
    sys.exit(1)

# Build list of busy (start, end) pairs
busy = []
for e in events:
    start = e.get('start', {}).get('dateTime')
    end = e.get('end', {}).get('dateTime')
    if start and end:
        busy.append((start, end))

# Find free slots during working hours
suggestions = []
for day_offset in range(1, DAYS_AHEAD + 1):
    day = datetime.now(timezone.utc) + timedelta(days=day_offset)

    # Skip weekends
    if day.weekday() >= 5:
        continue

    # Check each hour
    for hour in range(WORK_START_HOUR, WORK_END_HOUR):
        slot_start = day.replace(hour=hour, minute=0, second=0, microsecond=0)
        slot_end = slot_start + timedelta(minutes=DURATION_MIN)

        # Skip if slot goes past end of day
        if slot_end.hour > WORK_END_HOUR:
            continue

        # Check for conflicts
        conflict = any(
            slot_start.isoformat() < b[1] and slot_end.isoformat() > b[0]
            for b in busy
        )

        if not conflict:
            suggestions.append(slot_start)

        if len(suggestions) >= 5:
            break

    if len(suggestions) >= 5:
        break

if not suggestions:
    print("No slots found in the next 7 days during working hours.")
else:
    print(f"Available {DURATION_MIN}-min slots:")
    for s in suggestions:
        print(" •", s.strftime('%A %b %d'), "at", s.strftime('%H:%M'), "UTC")
```

---

## Rescheduling

```bash
# 1. Find the event
GOG_ACCOUNT=owner@company.com gog calendar events primary \
  --from "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --to "$(date -u -d '+14 days' +%Y-%m-%dT%H:%M:%SZ)"

# 2. Delete the old event (use ID from above output)
GOG_ACCOUNT=owner@company.com gog calendar delete primary EVENT_ID

# 3. Re-coordinate with the other PA and create a new event
```

Always notify both sides when rescheduling:
```
"[Owner] needs to move the [Date] meeting. Can we try [new time]?"
```

---

## Quick Templates

| Situation | Template |
|---|---|
| Initial request | "Hey [PA], [Owner A] wants to connect with [Owner B] for ~30 min [this/next] week. What works?" |
| Propose slots | "Here are 3 options: [A], [B], [C]. Any work?" |
| Confirm | "✅ Booked for [time]. Invite sent to [email]." |
| Reschedule | "[Owner] can't make [time]. Can we try [alternative]?" |
| Cancel | "[Owner] needs to cancel [time]. Apologies." |
| No PA found | "Hi [Owner], [Your Owner] would like to schedule a call. Are you available [options]?" |

---

## Cost Tips

- **Cheap:** Finding slots and booking — any small model works
- **More expensive:** Reasoning across timezones or complex constraints — use medium model
- **Batch:** Propose 3–5 slots at once instead of one slot at a time (fewer back-and-forth messages)
- **Avoid:** Don't fetch the full calendar repeatedly — fetch once, extract 5 slots, propose them all

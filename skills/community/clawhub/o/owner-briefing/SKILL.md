---
name: owner-briefing
description: "Generate and send a daily briefing to your owner covering today's meetings, urgent emails, open tasks, and anything that needs attention. Use when: it's the start of the owner's day, when asked for a summary, or on a scheduled cron job."
---

# Owner Briefing Skill

## Minimum Model
Any small model. Data collection is CLI-based. Formatting is simple.

---

## When to Send (Decision Rules)

- **Weekday (Mon–Fri):** Send at the scheduled time.
- **Weekend / holiday:** Skip unless owner explicitly requests it.
- **Owner is travelling:** Still send — adjust timezone in cron if needed.
- **Data source fails (calendar/email/tasks):** Send the briefing with that section marked "unavailable." Do NOT skip the whole briefing.

---

## Briefing Format

```
☀️ Good morning [Owner Name] — here's your day:

📅 TODAY'S MEETINGS
• 09:30 — Standup (30 min)
• 14:00 — 1:1 with [Person] (1h)

📬 EMAILS NEEDING ATTENTION
• [Sender] — "[Subject]"

✅ OPEN TASKS
• [Task from monday.com or memory]

⚠️ HEADS UP
• [Deadline, unusual item, etc.]

Have a great day! 🙌
```

---

## Step 1 — Get Today's Calendar Events

```bash
#!/bin/bash
set -e

# Calculate today and tomorrow in UTC ISO format
TODAY=$(date -u +%Y-%m-%dT00:00:00Z)
TOMORROW=$(
  date -u -d '+1 day' +%Y-%m-%dT00:00:00Z 2>/dev/null \
  || date -u -v+1d +%Y-%m-%dT00:00:00Z
)

# Fetch events from Google Calendar via gog
GOG_ACCOUNT=owner@company.com gog calendar events primary \
  --from "$TODAY" \
  --to "$TOMORROW" \
  2>/dev/null \
  | python3 -c "
import sys, json

# Parse JSON, default to empty list on error
try:
    events = json.loads(sys.stdin.read().strip() or '[]')
except json.JSONDecodeError:
    events = []

print('📅 TODAY\'S MEETINGS')

if not events:
    print('• No events')
else:
    # Sort by start time, format each event
    for e in sorted(events, key=lambda x: x.get('start', {}).get('dateTime', '')):
        start = e.get('start', {}).get('dateTime', '')[:16].replace('T', ' ')
        title = e.get('summary', 'Untitled')
        print('•', start, '—', title)
"
```

---

## Step 2 — Get Urgent Emails

```bash
#!/bin/bash
set -e

# Fetch up to 5 unread emails from the last day
GOG_ACCOUNT=owner@company.com gog gmail search \
  'is:unread newer_than:1d' \
  --max 5 \
  2>/dev/null \
  | python3 -c "
import sys, json

# Parse JSON, default to empty list on error
try:
    emails = json.loads(sys.stdin.read().strip() or '[]')
except json.JSONDecodeError:
    emails = []

print('📬 EMAILS NEEDING ATTENTION')

if not emails:
    print('• No urgent emails')
else:
    for e in emails:
        sender = e.get('from', 'Unknown')
        subject = e.get('subject', '(no subject)')
        print('•', sender, '—', '\"' + subject + '\"')
"
```

---

## Step 3 — Get Open Tasks (monday.com)

```bash
#!/bin/bash
set -e

TOKEN_FILE="$HOME/.credentials/monday-api-token.txt"

# If token is missing, skip this section gracefully
if [ ! -f "$TOKEN_FILE" ]; then
  echo "✅ OPEN TASKS"
  echo "• (monday.com token not configured — skipping)"
  exit 0
fi

MONDAY_TOKEN=$(cat "$TOKEN_FILE")
BOARD_ID="BOARD_ID"  # replace with actual board ID

# Fetch first 5 items from the board
RESPONSE=$(curl -s -X POST https://api.monday.com/v2 \
  -H "Content-Type: application/json" \
  -H "Authorization: $MONDAY_TOKEN" \
  -d "{\"query\": \"{ boards(ids: [$BOARD_ID]) { items_page(limit: 5) { items { name state } } } }\"}")

# Print open (non-done) items
echo "$RESPONSE" | python3 -c "
import sys, json

try:
    d = json.loads(sys.stdin.read())
    items = d['data']['boards'][0]['items_page']['items']
except (KeyError, IndexError, json.JSONDecodeError) as e:
    print('✅ OPEN TASKS')
    print('• (could not fetch:', e, ')')
    sys.exit(0)

# Filter out completed items
open_items = [i for i in items if i.get('state') != 'done']

print('✅ OPEN TASKS')
if not open_items:
    print('• None — all clear!')
else:
    for item in open_items:
        print('•', item['name'])
"
```

---

## Step 4 — Assemble and Send the Briefing

Run Steps 1–3, save each output to a temp file, then combine:

```bash
#!/bin/bash
set -e

# Run each section and capture output
CALENDAR_SECTION=$(bash step1-calendar.sh 2>/dev/null || echo "📅 TODAY'S MEETINGS\n• (unavailable)")
EMAIL_SECTION=$(bash step2-email.sh 2>/dev/null || echo "📬 EMAILS NEEDING ATTENTION\n• (unavailable)")
TASKS_SECTION=$(bash step3-tasks.sh 2>/dev/null || echo "✅ OPEN TASKS\n• (unavailable)")

# Build the briefing message
BRIEFING="☀️ Good morning — here's your day:

$CALENDAR_SECTION

$EMAIL_SECTION

$TASKS_SECTION"

# Option A: Send via WhatsApp
openclaw message send --to OWNER_PHONE --message "$BRIEFING"

# Option B: Send via email
# GOG_ACCOUNT=owner@company.com gog gmail send \
#   --to owner@company.com \
#   --subject "☀️ Your Daily Briefing — $(date +'%A %B %d')" \
#   --body "$BRIEFING"
```

---

## Cron Schedule

```json
{
  "jobs": [
    {
      "id": "morning-briefing",
      "schedule": "30 7 * * 1-5",
      "timezone": "Asia/Jerusalem",
      "task": "Generate and send the owner's morning briefing: calendar events, urgent emails, and open tasks. Use owner-briefing skill.",
      "delivery": {
        "mode": "message",
        "channel": "whatsapp",
        "to": "OWNER_PHONE"
      }
    }
  ]
}
```

- Runs Monday–Friday at 07:30 in the owner's timezone.
- Change `"30 7"` to adjust time.
- Change `"timezone"` to match the owner's location.

---

## Customization Options

| Goal | Change |
|---|---|
| Only meetings after 9am | Filter events: `if start_hour >= 9` |
| Skip internal standups | Filter: `if 'standup' not in summary.lower()` |
| Add weather | Call weather skill before building briefing |
| Highlight flagged emails | Change search to `is:starred` or `is:important` |
| Evening summary (tomorrow preview) | Change `TODAY/TOMORROW` to tomorrow's dates |

---

## What NOT to Include

The briefing is for action, not recap. Apply this filter before sending:

- ❌ Don't recap things the owner already knows (decisions from yesterday, completed work)
- ❌ Don't list completed tasks from yesterday — they're done, move on
- ❌ Don't include calendar events more than 48h away — not actionable today
- ❌ Don't include low-priority emails that can wait (newsletters, FYIs, no-reply)
- ❌ Don't repeat the same item two days in a row if nothing changed
- ✅ **Rule: if it doesn't need action TODAY, leave it out**

A good briefing takes 30 seconds to read. If it's longer, cut more.

---

## Cost Tips

- **Very cheap:** Data collection is CLI-based — no LLM tokens for fetching.
- **Small model OK:** Formatting the briefing is simple — any model works.
- **Avoid:** Don't fetch 30 days of email history — search only `newer_than:1d`.
- **Batch:** Fetch calendar + email in one script run, not separate sessions.
- **On failure:** Send partial briefing — don't skip the whole thing.

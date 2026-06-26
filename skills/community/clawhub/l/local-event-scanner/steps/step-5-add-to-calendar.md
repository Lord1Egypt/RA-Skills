# Step 5: Add to Calendar

Use this step only for explicit user requests to add a specific suggested event to Google Calendar.

## Required Inputs

- Selected event recommendation.
- Title.
- Start and end date/time.
- Address, or online link when the event is online.
- Description.

## Procedure

1. Confirm the user explicitly asked to add this specific event to Google Calendar.
2. Extract the required fields from the recommendation and source link.
3. If title, start time, end time, location/link, or description is missing or ambiguous, ask for the missing detail before creating the calendar event.
4. Use the event's local timezone.
   - Online events: use the timezone stated by the event, or ask if unclear.
5. Create exactly one Google Calendar event using the Google Calendar tool, usually on `primary`.
6. Use no attendees.
7. Do not add Google Meet unless the user asks.
8. Use the calendar's default reminders unless the user asks otherwise.
9. Do not create recurring events unless the user asks.
10. Report the created event title, date/time, and location/link back to the user.
11. After the event is created, read or check `skills/event-scanner/assets/sources.md` and `skills/event-scanner/assets/taste-profile.md`.
12. Always send a chat-only `Post-add learning check`.
13. In that check, include source and taste-profile suggestions only when the evidence is strong:
    - Suggest adding a new primary source only if the added event came from a source not covered in `skills/event-scanner/assets/sources.md`.
    - Suggest adding a new taste-profile interest only if the added event reveals a recurring preference not already covered in `skills/event-scanner/assets/taste-profile.md`.
14. If neither a source nor taste-profile update should be suggested, write exactly: `Post-add learning check: no new suggestions`.
15. Do not justify the absence of suggestions.
16. Do not write these suggestions to run notes or reference files unless the user explicitly approves the edit.

## Field Mapping

- Google Calendar `title`: event title.
- `start_time` and `end_time`: event date/time in RFC3339 format.
- `timezone_str`: event local timezone.
- `location`: physical address, or online link if the event is online.
- `description`: concise event description plus source link when available.
- `attendees`: empty list.
- `add_google_meet`: false.

## Privacy Rules

Do not log the created calendar event details in run notes unless the user asks. Do not invite attendees, modify other calendar events, or read unrelated calendar details.

## Learning Suggestions

Normal scans should not suggest new primary sources or taste-profile interests. This step is the only place to suggest them, because adding an event to the calendar is a strong signal.

Always send a brief `Post-add learning check` chat message after calendar creation.

When there are suggestions, use this shape:

```md
Post-add learning check:

- Source suggestion: Add `Example Venue Calendar` to Malmö primary sources.
- Taste-profile suggestion: Add `experimental sound art`.
```

When there are no suggestions, use exactly:

```md
Post-add learning check: no new suggestions
```

## Output

When starting this step, explicitly say: "[Step 5: Add to Calendar]"

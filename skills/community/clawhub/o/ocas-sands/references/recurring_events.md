# Recurring Event Handling

Sands supports recurring events across create, modify, and delete commands.

## Creating recurring events
- Support patterns: daily, weekly, biweekly, monthly, yearly, and custom (e.g., "every Tuesday and Thursday", "first Monday of each month")
- Extract recurrence as RRULE from natural language in `sands.event.create`
- If the user says "every Tuesday" without an end date, default to no end date (infinite recurrence) and confirm with the user

## Modifying recurring events
- Always ask for scope before applying: "Just this occurrence, this and future occurrences, or all occurrences?"
- Pass the appropriate scope parameter to `gcal_update_event`
- Re-run conflict check for the affected scope

## Deleting recurring events
- Same scope question as modify
- Pass scope to `gcal_delete_event`
- Clean up associated travel blocks for affected occurrences

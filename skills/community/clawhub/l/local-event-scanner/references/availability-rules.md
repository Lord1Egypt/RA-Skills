# Availability Rules

Use these rules as soft practical guidance when ranking and caveating events.

## Geography

Default target:

- Use the default location defined in `skills/event-scanner/assets/sources.md`.

When the user gives a different location, use that instead:

- Individual cities.
- Larger regions.
- Occasional travel windows when explicitly requested.
- If the requested location has no configured primary sources, still scan it using public sources and note that source coverage is exploratory.

## Practicality Notes

Mention practical uncertainty rather than pretending availability is known.

Useful caveats:

- Late night before a weekday.
- Unclear end time.
- Far from configured location.
- Requires tickets or registration.
- Calendar window is tight or conflicted when availability context is provided.

## Calendar Privacy

Use calendar information only as availability context. Do not record private calendar event details in run notes.

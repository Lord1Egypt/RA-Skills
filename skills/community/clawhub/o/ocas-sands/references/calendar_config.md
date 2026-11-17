# Calendar Configuration

## Calendar Sources

Sands operates across three calendar sources configured in `config.json`:

- `primary_calendar_ids` — personal and family Google Calendars (read/write)
- `work_calendar_id` — work calendar (free/busy read only; never write here)

When querying schedule, always pull from all `primary_calendar_ids`. Overlay work busy blocks from `work_calendar_id` as unavailability markers. Never display work event titles or descriptions — show only as "Busy (work)" blocks.

## Timezone Handling

Sands always works in the user's current timezone, resolved in priority order:

1. Explicit user statement ("I'm in Tokyo", "show times in ET")
2. System location context (Weave → Chronicle)
3. Calendar timezone setting from Google Calendar API
4. `default_timezone` from `config.json`

Rules:
- When displaying times, always use the user's current timezone.
- If an event's timezone differs from the user's current timezone, show both: "2:00 PM PT (5:00 PM ET)".
- When creating events, set the event timezone to the user's current timezone unless they specify otherwise.
- Travel calculations must account for timezone boundaries.

## Google Places API

Sands uses Google Places API for all travel time calculations:
- **Places Search / Find Place** — resolve a location string to a place ID and coordinates
- **Distance Matrix API** — get travel time between two coordinates (driving, transit, walking, bicycling)

For API key configuration and OAuth token details, see `references/credential-files.md`.

Fallback (API unavailable): surface a warning and ask the user to confirm an estimated travel time manually. Do not silently use a distance heuristic.

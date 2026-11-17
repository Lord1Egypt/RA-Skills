# MCP Fallback for Sands Morning Briefing

When the template script `templates/sands_briefing_morning.py` fails due to missing dependencies (e.g., `ModuleNotFoundError: No module named 'google'`), you can generate a morning briefing using the MCP Google Calendar tools directly.

## Steps

1. **Determine time window** (today in local timezone):
   - `time_min`: start of today at 00:00:00 with correct offset (e.g., `2026-06-30T00:00:00-07:00` for PDT)
   - `time_max`: start of tomorrow at 00:00:00 with same offset

2. **Fetch events** using MCP:
   ```bash
   hermes mcp_composio_COMPOSIO_MULTI_EXECUTE_TOOL \
     --session_id <session> \
     --tools '[{"arguments":{"calendarId":"<user-google-email>","maxResults":250,"orderBy":"startTime","showDeleted":false,"singleEvents":true,"timeMax":"'$time_max'","timeMin":"'$time_min'"},"tool_slug":"GOOGLECALENDAR_EVENTS_LIST"}]'
   ```
   Extract the `items` array from the response.

3. **Process events**:
   - De-duplicate by (lowercase summary, start time).
   - Separate all-day vs timed events.
   - Convert times to local timezone (`America/Los_Angeles`).
   - Detect overlaps (simple O(n²) comparison).
   - Flag preparation events based on title keywords (e.g., "meeting", "review", "presentation").

4. **Calculate free hours** within working hours (default 09:00–18:00) by subtracting busy periods.

5. **Build output** (JSON or human-readable) similar to the template's payload.

6. **Write evidence** and update `config.json` fields (`last_morning_brief`, etc.) as per the skill's run completion steps.

## Primary Path: Use `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`

For briefings (morning or evening), prefer `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS` over querying individual calendars. It fetches all calendars in a single MCP call and returns a merged event list:

| Parameter | Setting | Why |
|-----------|---------|-----|
| `response_detail` | `"full"` | Returns full event objects (summary, start/end with timezone, htmlLink, location, descriptions). |
| `single_events` | `true` | Expands recurring event instances. |
| `time_min` / `time_max` | Local-timezone RFC3339 | Use PDT/PST offset for the target date (e.g., `-07:00` for July, `-08:00` for January). |

Basic call:
```json
{
  "tool_slug": "GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS",
  "arguments": {
    "response_detail": "full",
    "single_events": true,
    "show_deleted": false,
    "time_min": "2026-07-02T00:00:00-07:00",
    "time_max": "2026-07-03T00:00:00-07:00"
  }
}
```

The response contains:
- `events` array (each with `event` wrapper + `source_calendar_id` + `source_calendar_summary`) — only present when `response_detail="full"`
- `summary_view` array — compact event overview (always present, usable without `full`)
- `errors_by_calendar` — per-calendar error dict; individual calendar 404s don't block other calendars

**Important:** Without `response_detail="full"`, the response will only contain `summary_view` (title, start, end, event_id, all_day flag) — no location, description, htmlLink, or organizer info. Briefings that need deep links (`htmlLink`), locations, or descriptions MUST use `response_detail="full"`.

## Per-Calendar Fallback

If `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS` returns empty (no calendars found, or the all-calendars tool is unavailable), fall back to individual queries:

```bash
hermes mcp_composio_COMPOSIO_MULTI_EXECUTE_TOOL \
  --session_id <session> \
  --tools '[{"arguments":{"calendarId":"<user-google-email>","maxResults":250,"orderBy":"startTime","showDeleted":false,"singleEvents":true,"timeMax":"'$time_max'","timeMin":"'$time_min'"},"tool_slug":"GOOGLECALENDAR_EVENTS_LIST"}]'
```

Query each primary calendar from `config.json`, tag events with `source_calendar_id`, then merge and deduplicate.

## Notes

- This fallback avoids dependency on the `google-auth` library.
- Ensure an active Composio connection for `googlecalendar` before running. Check with `COMPOSIO_SEARCH_TOOLS` if unsure.
- See `references/direct_calendar_access.md` for additional context on MCP vs direct fallback.
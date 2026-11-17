# Known-Good Calendar IDs

Verified working calendar IDs for this environment (as of 2026-06-17):

| Calendar | ID | Access | Notes |
|---|---|---|---|
| Personal | `<user-google-email>` | Read (direct API + MCP + Composio) | The working personal calendar |
| <third-party-name> | `<third-party-email>` | Read (direct API + Composio) | Works via direct API as of 2026-06-17 |
| Family | `<family-calendar-id>@group.calendar.google.com` | Read (direct API + Composio) | Works via direct API as of 2026-06-17; earlier 404 was likely transient |
| Holidays | `en.usa#holiday@group.v.calendar.google.com` | Read (direct API) | US holidays; all-day events only |
| Primary (MCP) | `<agent-email>` | 404 on direct API | Shown by MCP list_calendars but not queryable via direct fallback |
| Work | `<user-handle>@<employer>.com` | FreeBusyReader only | Read-only (free/busy); cannot read event details |

## Recommendation

Set `config.json` `primary_calendar_ids` to explicit working IDs:

```json
"primary_calendar_ids": ["<user-google-email>"]
```

Do not use `["primary"]` as a calendar ID in `primary_calendar_ids` — it's ambiguous and may resolve differently between MCP and direct fallback paths.

Also add the `last_evening_brief` field to config (only `last_morning_brief` exists in the default template):

```json
"last_evening_brief": null
```

## Calendar ID Detection

To find working calendar IDs:
1. Call `mcp_google_workspace_list_calendars` to enumerate all visible calendars
2. For each calendar ID, attempt a test query via direct Python fallback
3. Log which IDs return events vs 404
4. Update `config.json` with only the working IDs

## Composio Fallback Pattern (Added 2026-06-15)

When direct Calendar API returns 404 for a calendar ID that appears in MCP/Composio listings, use Composio as an alternative query path:

1. Use `COMPOSIO_SEARCH_TOOLS` with use_case "list Google Calendar events" to discover available tools
2. Use `GOOGLECALENDAR_FIND_EVENT` (or `GOOGLECALENDAR_BATCH_EVENTS` for bulk) via `COMPOSIO_MULTI_EXECUTE_TOOL`
3. Pass the calendar ID as shown in Composio's calendar list (e.g., `<third-party-email>`, `<family-calendar-id>@group.calendar.google.com`)

This pattern worked for <third-party-name> and Family calendars which returned 404 on direct API but returned events via Composio.

**Key difference**: Composio's calendar list shows `<family-calendar-id>@group.calendar.google.com` (no `.v`), while the earlier known-good table showed `@group.v.calendar.google.com`. Use the ID exactly as returned by Composio's list_calendars.
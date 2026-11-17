# Google Calendar API Quirks

## manage_event Requires Full Event Fields

The `manage_event` tool (Google Calendar API) returns HTTP 400 "Missing end time" even when you only want to update a single field like description. Unlike the Google Calendar UI or raw PATCH semantics, `manage_event` requires these fields on every update call:

- `event_id` — target event
- `action` — always "update"
- `calendar_id` — target calendar
- `start_time` — original start time (RFC3339)
- `end_time` — original end time (RFC3339)
- `summary` — current title (not the new title, the existing one)

After these required fields, add only the fields you want to change (e.g., `description`, `location`).

### Example: Adding a description to an existing event

```
manage_event(
  action="update",
  calendar_id="<user-google-email>",
  event_id="7l5h00p67qsahhcahgf1hg3bg4",
  start_time="2026-05-22T10:00:00-07:00",
  end_time="2026-05-22T12:00:00-07:00",
  summary="UCSF Imaging",
  description="Medical imaging appointment at UCSF. Arrive 15 min early."
)
```

### Workflow Tip

If you don't have the event details cached, query the event first with `get_events` to get start/end/summary before updating. Don't guess timestamps.

## Event Query Time Range Gotcha

`get_events` with `time_min` and `time_max` treats time_max as **exclusive**. To get all events on May 22, use:

- `time_min`: `2026-05-22T00:00:00-07:00`
- `time_max`: `2026-05-23T00:00:00-07:00` (not `23:59:59`)

Using `23:59:59` can miss events at the very end of the day due to boundary semantics.

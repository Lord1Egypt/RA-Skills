# Calendar

`Calendar(auth, calendar_id="primary")` from `gsuite_calendar`.

Times: naive datetimes are wall time in `GSUITE_DEFAULT_TIMEZONE` (default
UTC) when creating events, and UTC when filtering. Pass timezone-aware
datetimes to be explicit. All-day events have `event.all_day = True`.

## Reading

```python
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from gsuite_calendar import Calendar
from gsuite_core import GoogleAuth

auth = GoogleAuth()
calendar = Calendar(auth)

today = calendar.get_today()                         # in GSUITE_DEFAULT_TIMEZONE
week = calendar.get_upcoming(days=7)
tz = ZoneInfo("America/Argentina/Buenos_Aires")
march = calendar.get_events(
    time_min=datetime(2026, 3, 1, tzinfo=tz),
    time_max=datetime(2026, 4, 1, tzinfo=tz),
)
for event in march:
    print(event.start, event.end, event.summary, event.location, event.attendees, event.meet_link)

event = calendar.get_event("EVENT_ID")               # None if it doesn't exist
calendars = calendar.get_calendars()
busy = calendar.get_free_busy(datetime(2026, 3, 2, 9, tzinfo=tz), datetime(2026, 3, 2, 18, tzinfo=tz),
                              calendars=["ana@example.com"])
```

Each `Event` also has `ical_uid` (the same in .ics exports), `recurring_event_id`
and `original_start` (to tell occurrences apart), `organizer_name`,
`organizer_self`, attendees' `resource` (rooms) and `raw` (the API's dict).

Keeping a local copy in sync:

```python
delta = calendar.sync()                    # first time: the whole calendar
delta = calendar.sync(delta.sync_token)    # later: delta.changed, delta.cancelled (deleted)
```

The API takes no time range with sync tokens. When Google invalidates a token,
`sync` raises `SyncTokenExpiredError`: call it again without one.

## Creating and changing

```python
start = datetime(2026, 3, 2, 10, 0, tzinfo=tz)
event = calendar.create_event(
    summary="Planning",
    start=start,
    end=start + timedelta(minutes=30),
    location="Room 2",
    attendees=["ana@example.com"],
    meet=True,                               # adds a Google Meet link
    send_updates="all",                      # email the attendees: "all", "externalOnly" or "none"
)
calendar.create_event(summary="Holiday", start=datetime(2026, 3, 24).date(), all_day=True)
calendar.create_event(summary="Standup", start=start, recurrence=["RRULE:FREQ=WEEKLY;BYDAY=MO,WED,FR"])
calendar.quick_add("Lunch with Ana tomorrow at 1pm")

calendar.update_event(event.id, summary="Planning (moved)", start=start + timedelta(days=1),
                      end=start + timedelta(days=1, minutes=30))
calendar.delete_event(event.id, send_updates="all")   # False if it didn't exist
```

## CLI

```bash
gsuite calendar list --days 7 -o json
gsuite calendar today
gsuite calendar week
gsuite calendar create "Planning" --start "2026-03-02 10:00" --end "2026-03-02 10:30" --location "Room 2"
gsuite calendar create "Sync" --start "2026-03-02 15:00" --attendee ana@example.com --meet --notify
gsuite calendar create "Standup" --start "2026-03-02 09:30" --repeat "FREQ=WEEKLY;BYDAY=MO,WED,FR"
gsuite calendar create "Holiday" --start 2026-03-24 --all-day
gsuite calendar quick "Lunch with Ana tomorrow at 1pm"
gsuite calendar delete EVENT_ID --yes
gsuite calendar calendars
```

Only `calendar list` has `-o json`.

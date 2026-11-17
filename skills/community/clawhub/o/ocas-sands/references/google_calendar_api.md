# Google Calendar API Implementation

## Authentication

Google OAuth tokens are stored at:
`<gworkspace-creds>/credentials/<user-google-email>.json`

### Python authentication code (with proactive refresh)

**Always attempt token refresh at the start of every run**, even if a previous run recorded `REFRESH_FAILED`. The refresh token may still be valid.

```python
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

with open('<gworkspace-creds>/credentials/<user-google-email>.json') as f:
    token_data = json.load(f)

creds = Credentials.from_authorized_user_info(token_data)

# Proactive refresh — do this FIRST, not only on error
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
    # Save refreshed token for next run
    with open('<gworkspace-creds>/credentials/<user-google-email>.json', 'w') as f:
        json.dump(json.loads(creds.to_json()), f)

service = build('calendar', 'v3', credentials=creds)
```

The `Credentials` class should handle auto-refresh, but for cron jobs (long gaps between runs), explicit refresh before use is more reliable.

**Note:** Credentials are stored in `<gworkspace-creds>/credentials/`, NOT in `~/.hermes/`.

## Calendar Discovery

**Always enumerate all calendars** — events are spread across multiple calendars:
```python
cal_list = service.calendarList().list().execute()
```

### Currently accessible calendars (as of 2026-04-14)

| Calendar ID | Summary | Access Role | Notes |
|---|---|---|---|
| `<user-google-email>` | Personal | writer | Primary personal calendar |
| `<agent-email>` | <agent-email> | owner | Currently empty |
| `<family-calendar-id>@group.calendar.google.com` | Family | writer | Family events (gym, medical, social) |
| `en.usa#holiday@group.v.calendar.google.com` | Holidays in United States | reader | US holidays |
| ~~`<user-handle>@<employer>.com`~~ | ~~Work~~ | ~~404~~ | **Inaccessible** — returns Not Found |

**Note:** The work calendar `<user-handle>@<employer>.com` was accessible in earlier runs (events.jsonl has entries) but now returns 404. Do not hardcode calendar IDs — always discover via `calendarList().list()`.

## Querying Events

```python
events_result = service.events().list(
    calendarId=cal_id,
    timeMin=start_utc,
    timeMax=end_utc,
    singleEvents=True,
    orderBy='startTime'
).execute()
```

## Work Calendar Handling

**Never write to work_calendar_id.** Display work events only as "🔒 Work (busy)" — no titles. Work events often have no title (expected).

## Conflict Detection

1. Compare every pair of timed events for overlap
2. All-day events only conflict if explicitly asked
3. Work busy blocks are advisory — note convenience for same-location back-to-back events
4. Never auto-resolve — always present options

## Pitfalls

- **Token file format:** Use `Credentials.from_authorized_user_info(token_data)` instead of manually constructing `Credentials()` — it handles all fields correctly.
- **Heredoc issues in terminal:** Large Python scripts with complex string formatting (f-strings with quotes, raw strings) break in heredocs. Write the script to a `.py` file first, then execute with `python3 script.py`.
- **Stored auth_status is stale:** A previous Sands run may record `REFRESH_FAILED: invalid_grant` in config.json but the refresh token works fine when retried. Always attempt refresh yourself rather than trusting the stored status.
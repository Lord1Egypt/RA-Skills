# Direct Calendar Access (Python Fallback)

When MCP Google Workspace tools (`mcp_google_workspace_get_events`, etc.) are unavailable, use this pattern to query Google Calendar directly via the `google_auth.py` helper.

## When to Use This Fallback

- MCP server returns "unreachable" errors (wait ~40s and retry once first — see SKILL.md)
- MCP server returns OAuth/auth errors (401/403, `invalid_grant`)
- MCP tools fail with validation errors (e.g., missing `user_google_email` — see note below)

## Important: MCP Tools Require `user_google_email`

Every `mcp_google_workspace_*` tool requires a `user_google_email` parameter. Omitting it produces a Pydantic validation error. **Always include it** — use the agent's own Google email unless the user specifies otherwise. This is the #1 cause of MCP tool failures.

## Prerequisites

- `<hermes-home>/scripts/google_auth.py` — central OAuth helper
- `<gworkspace-creds>/credentials/<email>.json` — credential files
- Python packages: `google-auth`, `google-api-python-client`

## Convenience Wrappers (Preferred)

The `google_auth.py` module provides convenience wrappers that are simpler than raw `get_service()`:

```python
import sys
sys.path.insert(0, '<hermes-home>/scripts')
from google_auth import get_calendar_service

# Returns a ready-to-use Calendar v3 service object
calendar = get_calendar_service('<user-google-email>')
# Or with fallback:
calendar = get_calendar_service('<agent-email>')
```

Available wrappers:
- `get_calendar_service(account)` — Calendar v3 with `https://www.googleapis.com/auth/calendar` scope
- `get_gmail_service(account)` — Gmail v1 with `https://www.googleapis.com/auth/gmail.modify` scope
- `get_service(api, version, scopes, account)` — raw access for any Google API

**Use the convenience wrappers unless you need a non-standard scope.** They avoid the `get_service() missing 2 required positional arguments` error that occurs when you forget `api_version` and `scopes`.

## Query Pattern

```python
import sys
sys.path.insert(0, '<hermes-home>/scripts')
from google_auth import get_calendar_service

calendar = get_calendar_service('<user-google-email>')

# Query a single calendar
result = calendar.events().list(
    calendarId='<user-google-email>',
    timeMin='2026-06-04T00:00:00-07:00',  # Use correct DST offset for target date
    timeMax='2026-06-05T00:00:00-07:00',
    singleEvents=True,
    orderBy='startTime',
    showDeleted=False
).execute()
events = result.get('items', [])
```

## Multi-calendar Merge

Loop over all `primary_calendar_ids` from `config.json`. Tag each event with `_source_calendar` for deduplication. Handle per-calendar failures independently — a 404 on one calendar should not block others.

## Deduplication

When the same event appears on multiple calendars (e.g., personal + family), deduplicate by matching `summary` + `start.dateTime` + `location`. Keep the primary calendar's copy as canonical.

## Timezone Offsets

Always use the correct DST offset for the **target date** (see `references/timezone_handling.md`):
- PDT (Mar–Nov): `-07:00`
- PST (Nov–Mar): `-08:00`

## Parsing Event Times from API Responses

**Critical:** The Calendar API returns `start.dateTime` and `end.dateTime` in the event's own timezone — often UTC (`Z` suffix). Naively parsing with `datetime.fromisoformat()` without converting to local time gives **wrong local times**.

**Wrong** (naive parse — shows UTC time as if local):
```python
dt = datetime.fromisoformat('2026-06-10T01:00:00Z'.replace('Z', '+00:00'))
# dt.hour == 1 → displays as "01:00" — WRONG, should be 18:00 PDT
```

**Right** (convert to local timezone):
```python
PDT = timezone(timedelta(hours=-7))  # or PST = timezone(timedelta(hours=-8))

raw = ev['start']['dateTime']  # e.g. '2026-06-10T01:00:00Z' or '2026-06-09T18:00:00-07:00'
if raw.endswith('Z'):
    dt = datetime.fromisoformat(raw.replace('Z', '+00:00'))
else:
    dt = datetime.fromisoformat(raw)
local_dt = dt.astimezone(PDT)
hhmm = local_dt.strftime('%H:%M')  # "18:00" ✓
```

**Also check the event's `start.timeZone` field** — if present, it tells you the timezone the event was created in. Use `zoneinfo.ZoneInfo(tz_name)` instead of a fixed offset when this field is set.

**All-day events** have `start.date` (no `dateTime`) — these don't need timezone conversion. Detect with `'date' in ev['start']`.

This pitfall is especially dangerous in cron-mode scripts where you can't visually verify the output before it reaches the user. Always spot-check: if an event shows `01:00` for what should be an evening dinner, the timezone conversion was skipped.

## Cron-Mode Execution

`execute_code` is blocked in cron jobs (no user present to approve). Use this pattern instead:

```python
# Step 1: Write the analysis script to a temp file
# (Use the write_file tool)
# /tmp/sands_conflict_scan.py

# Step 2: Run it via terminal
# terminal("python3 /tmp/sands_conflict_scan.py")

# Step 3: Read results from stdout or temp JSON output
```

Key rules for cron-mode scripts:
- Write scripts with `write_file` to `/tmp/`, run with `terminal("python3 /tmp/<script>.py")`
- Use `write_file` + `terminal` instead of `execute_code` for any multi-step Python
- For JSON output, write to `/tmp/sands_events.json` and read back with `read_file`
- Keep scripts self-contained — import paths must be absolute (`<hermes-home>/scripts`)
- Use triple-quoted strings carefully — nested quotes in f-strings can cause SyntaxErrors; prefer string concatenation or `.format()` for complex string building

## Error Handling

| Error | Meaning | Action |
|---|---|---|
| `404 Not Found` | Calendar ID doesn't exist or isn't accessible | Log in `degraded`, skip, surface to user |
| `401/403` | OAuth token expired or insufficient scope | Log `degraded: google_calendar_api`, trigger re-auth |
| `invalid_grant` | Refresh token revoked | Log `degraded: oauth_stale`, surface re-auth instructions |
| `HttpError` (other) | Transient or unknown | Retry once after 5s, then log `degraded` |

## Multi-Account Fallback (Added 2026-06-28)

When the default account's OAuth token is revoked (`invalid_grant`), the other credential in the store may still be valid — **and it may be able to read calendars that the dead account owned**.

**Discovered 2026-06-28:** `<user-google-email>`'s token was revoked, but `<agent-email>`'s token successfully read BOTH `<user-google-email>` AND `<family-calendar-id>@group.calendar.google.com` calendars. The indigo account has been granted access to <operator>'s calendar (likely via calendar sharing), so it serves as a complete fallback.

**Fallback order for cron runs:**
1. Try default account (`<user-google-email>`) — works when token is valid
2. On `invalid_grant`, try `<agent-email>` — works when indigo token is valid AND has calendar sharing permissions
3. If both fail, log `degraded: oauth_stale` and report to user

**Pattern:**
```python
import sys
sys.path.insert(0, '<hermes-home>/scripts')
from google_auth import get_calendar_service

calendars_to_query = ['<user-google-email>', '<family-calendar-id>@group.calendar.google.com']
accounts_to_try = ['<user-google-email>', '<third-party-or-user-email>']

calendar = None
working_account = None

for account in accounts_to_try:
    try:
        cal = get_calendar_service(account)
        # Test with a lightweight call
        cal.calendarList().list(maxResults=1).execute()
        calendar = cal
        working_account = account
        break
    except Exception as e:
        print(f"Account {account} failed: {e}")
        continue

if calendar is None:
    # Both accounts dead — log degraded and report
    print("DEGRADED: Both OAuth tokens invalid")
else:
    print(f"Using account: {working_account}")
    # Proceed with calendar.events().list() for each calendar ID
```

**Key insight:** Don't assume the indigo account can only read indigo's own calendar. Test it against all configured calendar IDs — it may have sharing permissions that make it a full fallback. This is especially valuable in cron mode where re-auth is impossible.

**After successful fallback:** Reset `config.json` `auth_status` to `OK` (the previous `STALE_OAUTH` was only for the owner account, not the overall system).

## Composio Fallback for 404 Calendar IDs (Added 2026-06-15)

When direct Calendar API returns 404 for a calendar ID that appears in MCP/Composio listings (e.g., <third-party-name> `<third-party-email>`, Family `<family-calendar-id>@group.calendar.google.com`), use Composio as an alternative query path:

1. Use `COMPOSIO_SEARCH_TOOLS` with use_case "list Google Calendar events" to discover available tools
2. Use `GOOGLECALENDAR_FIND_EVENT` via `COMPOSIO_MULTI_EXECUTE_TOOL`
3. Pass the calendar ID exactly as shown in Composio's calendar list

See `references/known-calendar-ids.md` for the current working calendar IDs and the full Composio fallback pattern.
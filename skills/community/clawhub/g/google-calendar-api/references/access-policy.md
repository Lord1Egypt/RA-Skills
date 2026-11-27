# Google Calendar access policy

An access policy limits which endpoints Google Calendar connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-calendar#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Google Calendar: its 12 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create google-calendar --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "calendar/v3/calendars/{id}/acl"},
    {"method": "GET", "path": "calendar/v3/calendars/{id}/acl/{id}"},
    {"method": "GET", "path": "calendar/v3/users/me/calendarList"},
    {"method": "GET", "path": "calendar/v3/users/me/calendarList/{id}"},
    {"method": "GET", "path": "calendar/v3/calendars/{id}"},
    {"method": "GET", "path": "calendar/v3/colors"},
    {"method": "GET", "path": "calendar/v3/calendars/{id}/events"},
    {"method": "GET", "path": "calendar/v3/calendars/{id}/events/{id}"},
    {"method": "GET", "path": "calendar/v3/calendars/{id}/events/{id}/instances"},
    {"method": "POST", "path": "calendar/v3/freeBusy"},
    {"method": "GET", "path": "calendar/v3/users/me/settings"},
    {"method": "GET", "path": "calendar/v3/users/me/settings/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Google Calendar endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | calendar/v3/calendars/{id}/acl | read | acl | Returns the rules in the access control list for the calendar. |
| POST | calendar/v3/calendars/{id}/acl | write | acl | Creates an access control rule. |
| POST | calendar/v3/calendars/{id}/acl/watch | write | acl | Watch for changes to ACL resources. |
| GET | calendar/v3/calendars/{id}/acl/{id} | read | acl | Returns an access control rule. |
| PUT | calendar/v3/calendars/{id}/acl/{id} | write | acl | Updates an access control rule. |
| PATCH | calendar/v3/calendars/{id}/acl/{id} | write | acl | Updates an access control rule. |
| DELETE | calendar/v3/calendars/{id}/acl/{id} | write | acl | Deletes an access control rule. |
| GET | calendar/v3/users/me/calendarList | read | calendarList | Returns the calendars on the user's calendar list. |
| POST | calendar/v3/users/me/calendarList | write | calendarList | Inserts an existing calendar into the user's calendar list. |
| POST | calendar/v3/users/me/calendarList/watch | write | calendarList | Watch for changes to CalendarList resources. |
| GET | calendar/v3/users/me/calendarList/{id} | read | calendarList | Returns a calendar from the user's calendar list. |
| PUT | calendar/v3/users/me/calendarList/{id} | write | calendarList | Updates an existing calendar on the user's calendar list. |
| PATCH | calendar/v3/users/me/calendarList/{id} | write | calendarList | Updates an existing calendar on the user's calendar list. |
| DELETE | calendar/v3/users/me/calendarList/{id} | write | calendarList | Removes a calendar from the user's calendar list. |
| POST | calendar/v3/calendars | write | calendars | Creates a secondary calendar. |
| GET | calendar/v3/calendars/{id} | read | calendars | Returns metadata for a calendar. |
| PUT | calendar/v3/calendars/{id} | write | calendars | Updates metadata for a calendar. |
| PATCH | calendar/v3/calendars/{id} | write | calendars | Updates metadata for a calendar. |
| DELETE | calendar/v3/calendars/{id} | write | calendars | Deletes a secondary calendar. |
| POST | calendar/v3/calendars/{id}/clear | write | calendars | Clears a primary calendar. |
| POST | calendar/v3/calendars/{id}/transferOwnership | write | calendars | Transfers a secondary calendar between users within a Google Workspace organization. |
| POST | calendar/v3/channels/stop | write | channels | Stop watching resources through this channel |
| GET | calendar/v3/colors | read | colors | Returns the color definitions for calendars and events. |
| GET | calendar/v3/calendars/{id}/events | read | events | Returns events on the specified calendar. |
| POST | calendar/v3/calendars/{id}/events | write | events | Creates an event. |
| POST | calendar/v3/calendars/{id}/events/import | write | events | Imports an event. |
| POST | calendar/v3/calendars/{id}/events/quickAdd | write | events | Creates an event based on a simple text string. |
| POST | calendar/v3/calendars/{id}/events/watch | write | events | Watch for changes to Events resources. |
| GET | calendar/v3/calendars/{id}/events/{id} | read | events | Returns an event based on its Google Calendar ID. |
| PUT | calendar/v3/calendars/{id}/events/{id} | write | events | Updates an event. |
| PATCH | calendar/v3/calendars/{id}/events/{id} | write | events | Updates an event. |
| DELETE | calendar/v3/calendars/{id}/events/{id} | write | events | Deletes an event. |
| GET | calendar/v3/calendars/{id}/events/{id}/instances | read | events | Returns instances of the specified recurring event. |
| POST | calendar/v3/calendars/{id}/events/{id}/move | write | events | Moves an event to another calendar, i.e. |
| POST | calendar/v3/freeBusy | read | freebusy | Returns free/busy information for a set of calendars. |
| GET | calendar/v3/users/me/settings | read | settings | Returns all user settings for the authenticated user. |
| POST | calendar/v3/users/me/settings/watch | write | settings | Watch for changes to Settings resources. |
| GET | calendar/v3/users/me/settings/{id} | read | settings | Returns a single user setting. |
| POST | batch/calendar/v3 | write | batch | Send several Calendar API calls in one request. |

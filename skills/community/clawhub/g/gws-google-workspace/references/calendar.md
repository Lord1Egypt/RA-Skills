# Calendar Reference

All time parameters use RFC 3339 format.

## Events

```bash
gws calendar events list --params '{"calendarId":"primary","timeMin":"START","timeMax":"END","maxResults":20}'
gws calendar events insert --json '{"summary":"Meeting","start":{"dateTime":"START","timeZone":"Asia/Shanghai"},"end":{"dateTime":"END","timeZone":"Asia/Shanghai"}}' --params '{"calendarId":"primary"}'
gws calendar events update --params '{"calendarId":"primary","eventId":"EVT_ID"}' --json '{"summary":"Updated"}'
gws calendar events delete --params '{"calendarId":"primary","eventId":"EVT_ID"}'
gws calendar events instances --params '{"calendarId":"primary","eventId":"RECURRING_ID"}'
```

## Free/Busy and ACL

```bash
gws calendar freebusy query --json '{"timeMin":"START","timeMax":"END","items":[{"id":"primary"}]}'
gws calendar acl list --params '{"calendarId":"primary"}'
```

## Calendar Management

```bash
gws calendar calendarList list --params '{"maxResults":10}'
gws calendar calendars insert --json '{"summary":"My Calendar"}' --params '{}'
gws calendar calendars delete --params '{"calendarId":"CAL_ID"}'
```

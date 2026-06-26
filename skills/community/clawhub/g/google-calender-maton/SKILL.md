# 📘 skill.md — Google Calendar via Maton Gateway (Full Spec)

## 🔐 Authentication

All requests require Maton API key:

```bash
-H "Authorization: Bearer $MATON_API_KEY"
````

Set environment variable:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

---

## 🌐 Base URL

```
https://gateway.maton.ai/google-calendar/calendar/v3
```

---

## 🌍 Time Zones (IMPORTANT)

Always use IANA time zones.

### 🇦🇺 Australia / Melbourne

```
Australia/Melbourne
```

* UTC +10 (standard)
* UTC +11 (daylight saving)

---

## 📅 1. List Events

```bash
curl "https://gateway.maton.ai/google-calendar/calendar/v3/calendars/primary/events?maxResults=20&singleEvents=true&orderBy=startTime" \
-H "Authorization: Bearer $MATON_API_KEY"
```

---

## ➕ 2. Create Event (Basic)

```bash
curl -X POST "https://gateway.maton.ai/google-calendar/calendar/v3/calendars/primary/events" \
-H "Authorization: Bearer $MATON_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "summary": "Team Meeting",
  "description": "Weekly sync",
  "start": {
    "dateTime": "2026-05-22T10:00:00",
    "timeZone": "Australia/Melbourne"
  },
  "end": {
    "dateTime": "2026-05-22T11:00:00",
    "timeZone": "Australia/Melbourne"
  }
}'
```

---

## 👥 3. Create Event with Invitations

```bash
curl -X POST "https://gateway.maton.ai/google-calendar/calendar/v3/calendars/primary/events" \
-H "Authorization: Bearer $MATON_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "summary": "Project Kickoff",
  "start": {
    "dateTime": "2026-05-22T14:00:00",
    "timeZone": "Australia/Melbourne"
  },
  "end": {
    "dateTime": "2026-05-22T15:00:00",
    "timeZone": "Australia/Melbourne"
  },
  "attendees": [
    { "email": "user1@example.com" },
    { "email": "user2@example.com" }
  ],
  "sendUpdates": "all"
}'
```

---

## 📹 4. Create Event with Google Meet

```bash
curl -X POST "https://gateway.maton.ai/google-calendar/calendar/v3/calendars/primary/events?conferenceDataVersion=1" \
-H "Authorization: Bearer $MATON_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "summary": "Client Meeting (Google Meet)",
  "start": {
    "dateTime": "2026-05-23T09:00:00",
    "timeZone": "Australia/Melbourne"
  },
  "end": {
    "dateTime": "2026-05-23T10:00:00",
    "timeZone": "Australia/Melbourne"
  },
  "attendees": [
    { "email": "client@example.com" }
  ],
  "conferenceData": {
    "createRequest": {
      "requestId": "meet-123456",
      "conferenceSolutionKey": {
        "type": "hangoutsMeet"
      }
    }
  }
}'
```

---

## ✏️ 5. Update Event

```bash
curl -X PATCH "https://gateway.maton.ai/google-calendar/calendar/v3/calendars/primary/events/{EVENT_ID}" \
-H "Authorization: Bearer $MATON_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "summary": "Updated Meeting Title",
  "description": "Updated agenda"
}'
```

---

## 🔁 6. Reschedule Event

```bash
curl -X PATCH "https://gateway.maton.ai/google-calendar/calendar/v3/calendars/primary/events/{EVENT_ID}" \
-H "Authorization: Bearer $MATON_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "start": {
    "dateTime": "2026-05-24T12:00:00",
    "timeZone": "Australia/Melbourne"
  },
  "end": {
    "dateTime": "2026-05-24T13:00:00",
    "timeZone": "Australia/Melbourne"
  }
}'
```

---

## 👥 7. Update Attendees

```bash
curl -X PATCH "https://gateway.maton.ai/google-calendar/calendar/v3/calendars/primary/events/{EVENT_ID}" \
-H "Authorization: Bearer $MATON_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "attendees": [
    { "email": "newuser@example.com" },
    { "email": "existing@example.com" }
  ],
  "sendUpdates": "all"
}'
```

---

## ❌ 8. Delete Event

```bash
curl -X DELETE "https://gateway.maton.ai/google-calendar/calendar/v3/calendars/primary/events/{EVENT_ID}" \
-H "Authorization: Bearer $MATON_API_KEY"
```

---

## 📌 Event Object Reference

```json
{
  "summary": "Event Title",
  "description": "Optional details",
  "start": {
    "dateTime": "2026-05-22T10:00:00",
    "timeZone": "Australia/Melbourne"
  },
  "end": {
    "dateTime": "2026-05-22T11:00:00",
    "timeZone": "Australia/Melbourne"
  }
}
```

---

## ⚙️ Key Rules

* Always use **IANA time zones**
* Use `PATCH` for updates
* Use `sendUpdates: "all"` for invites
* Use `conferenceDataVersion=1` for Google Meet

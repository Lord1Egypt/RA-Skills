# API Contract

This file is a low-level HTTP reference for the reminder worker.

Normal skill execution should use `scripts/reminder-client.mjs` rather than issuing raw HTTP calls directly.

Base URL example:

```text
https://your-worker.example.workers.dev
```

## Create reminder

```http
POST /v1/reminders
Authorization: Bearer <REMINDER_API_TOKEN>
Content-Type: application/json
```

Request body:

```json
{
  "title": "Pay utilities",
  "notes": "Electricity and water bill",
  "location": "Home office",
  "url": "https://example.com/bills",
  "start_at": "2026-03-20T15:00:00+08:00",
  "timezone": "Asia/Shanghai",
  "all_day": false,
  "rrule": null,
  "alarm_offset_minutes": 15,
  "source_text": "明天下午三点提醒我交水电费",
  "idempotency_key": "msg-20260312-001"
}
```

Success response shape:

```json
{
  "id": "2d0a9e7c-53c3-4940-9f8f-2cc76b85f57a",
  "status": "created",
  "created_at": "2026-03-12T08:00:00.000Z",
  "subscription_hint": "/v1/feeds/<token>.ics"
}
```

## List reminders

```http
GET /v1/reminders
Authorization: Bearer <REMINDER_API_TOKEN>
```

Success response shape:

```json
{
  "reminders": []
}
```

## Delete reminder

```http
DELETE /v1/reminders/:id
Authorization: Bearer <REMINDER_API_TOKEN>
```

This is a soft delete and marks the reminder as cancelled.

Success response shape:

```json
{
  "id": "2d0a9e7c-53c3-4940-9f8f-2cc76b85f57a",
  "deleted": true,
  "updated_at": "2026-03-12T08:00:00.000Z"
}
```

## Rotate ICS feed token

```http
POST /v1/feeds/rotate
Authorization: Bearer <REMINDER_API_TOKEN>
```

Success response:

```json
{
  "status": "rotated",
  "feed_url": "/v1/feeds/<high-entropy-token>.ics",
  "issued_at": "2026-03-12T08:00:00.000Z"
}
```

## Read ICS feed

```http
GET /v1/feeds/:token.ics
```

Returns:

- `200 text/calendar` when the token is valid
- `404` when the token is invalid or rotated out

This endpoint is exposed for calendar clients. The helper script does not need to fetch the ICS file during normal reminder operations.

## Common errors

- `400` invalid request payload
- `401` invalid bearer token
- `404` unknown reminder or feed
- `500` server error

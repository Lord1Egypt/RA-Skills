# Klarity Booking API Reference

Base URL: `https://rx.helloklarity.com`

No authentication required — all endpoints are public.

## Payment Methods

- **Insurance (PPA):** Carrier name + member ID required
- **Cash pay (PPA):** No credit card needed — patient pays at visit

---

## GET /api/v1/services

Returns service types, supported states, and insurance carriers by state.

```json
{
  "services": [
    {"id": "adhd", "label": "ADHD Evaluation & Treatment"},
    {"id": "anxiety", "label": "Anxiety Treatment"},
    {"id": "depression", "label": "Depression Treatment"},
    {"id": "insomnia", "label": "Insomnia Treatment"},
    {"id": "ocd", "label": "OCD Treatment"},
    {"id": "ptsd", "label": "PTSD Treatment"},
    {"id": "narcolepsy", "label": "Narcolepsy Treatment"}
  ],
  "supported_states": ["AK", "AL", "AR", "AZ", "CA", ...],
  "insurance_carriers_by_state": {
    "CA": ["Aetna", "Anthem Blue Cross", ...],
    "NY": ["Aetna", "Cigna", ...]
  }
}
```

---

## GET /api/v1/availability

| Param | Required | Description |
|-------|----------|-------------|
| `service` | Yes | Service ID from services endpoint |
| `state` | Yes | 2-letter state code |
| `insurance_carrier` | No | Carrier name. Omit for cash pay. |
| `date` | No | `YYYY-MM-DD` |
| `time_preference` | No | `morning` (6am-12pm), `afternoon` (12-5pm), `evening` (5-10pm) — UTC |

Response includes `session_id` (needed for booking) and anonymous provider profiles with start times in UTC.

```json
{
  "session_id": "abc123def456",
  "providers": [
    {
      "anonymous_id": "p_abc123de_1",
      "title": "PMHNP-BC",
      "experience_years": 12,
      "rating": 4.9,
      "review_count": 47,
      "appointment_duration_minutes": 60,
      "available_start_times": ["2026-03-12T16:00:00.000Z", "2026-03-12T16:10:00.000Z"],
      "accepts_insurance": true,
      "supports_self_pay": true
    }
  ]
}
```

- `available_start_times`: times the appointment can begin (UTC). Group consecutive times into ranges for display.
- `appointment_duration_minutes`: length of the visit (typically 30 or 60).
- Rate limit: 20 searches per day per IP. Max 15 providers, 10 slots each, 14-day window.

---

## POST /api/v1/book

Content-Type: application/json. Add `?mode=dry_run` to validate without booking.

| Field | Required | Description |
|-------|----------|-------------|
| `provider_id` | Yes | `anonymous_id` from availability |
| `session_id` | No | From availability response |
| `service` | Yes | Service ID |
| `slot` | Yes | ISO datetime from `next_slots` |
| `patient_first_name` | Yes | |
| `patient_last_name` | Yes | |
| `patient_email` | Yes | Confirmation sent here |
| `patient_phone` | Yes | Any format |
| `patient_dob` | Yes | `YYYY-MM-DD` |
| `patient_state` | Yes | 2-letter code |
| `insurance_carrier` | If insured | Must match availability search |
| `insurance_member_id` | If insured | Member/subscriber ID |

Success response:
```json
{
  "success": true,
  "confirmation_id": "BK-123456",
  "provider_name": "Dr. Sarah Patel",
  "appointment": {
    "datetime": "2026-03-12T16:00:00.000Z",
    "duration_minutes": 30,
    "type": "video",
    "service": "adhd"
  },
  "prep_notes": "Have your insurance card ready..."
}
```

---

## Errors

| Status | Meaning |
|--------|---------|
| 400 | Missing/invalid fields |
| 404 | Provider not found |
| 422 | Booking failed (slot taken) |
| 429 | Rate limit exceeded |
| 500 | Server error |
```

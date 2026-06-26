# Placed Job Tracker — API Reference

Full reference for all job tracker tools available via the Placed API.

## Authentication

All tools require a Bearer token:

```
Authorization: Bearer $PLACED_API_KEY
```

---

## add_job_application

Add a new job application to your tracker.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `company` | string | yes | Company name |
| `position` | string | yes | Job title/position |
| `job_url` | string | no | URL to the job posting |
| `job_description` | string | no | Job description text |
| `location` | string | no | Job location |
| `work_type` | string | no | `remote`, `hybrid`, `onsite` |
| `status` | string | no | Initial status (default: `WISHLIST`) |
| `resume_id` | string | no | Resume used for this application |
| `notes` | string | no | Private notes |

**Status values:** `WISHLIST`, `APPLIED`, `INTERVIEWING`, `OFFER`, `REJECTED`, `WITHDRAWN`

**Returns:** `{ id, company, position, status, created_at }`

---

## list_job_applications

View your application pipeline.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | no | Filter by status (see values above) |

**Returns:** Array of application objects.

---

## update_job_status

Move an application to a new stage.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `job_id` | string | yes | Job application ID (from `list_job_applications`) |
| `status` | string | yes | New status (see values above) |
| `notes` | string | no | Notes about the status change |

**Returns:** Updated application object.

---

## delete_job_application

Remove an application from the tracker.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `job_id` | string | yes | Job application ID |

---

## get_application_analytics

Get pipeline analytics and conversion rates.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `date_range` | string | no | `7d`, `30d`, `90d`, `all` (default: `all`) |

**Returns:**

```json
{
  "total_applications": 24,
  "by_status": { "APPLIED": 10, "INTERVIEWING": 6, "OFFER": 2, "REJECTED": 6 },
  "conversion_rates": {
    "applied_to_interviewing": 0.42,
    "interviewing_to_offer": 0.33
  },
  "avg_days_to_response": 8
}
```

---

## Error Codes

| Code                    | Meaning                                         |
| ----------------------- | ----------------------------------------------- |
| `APPLICATION_NOT_FOUND` | Job ID invalid or not found                     |
| `INVALID_STATUS`        | Status value not one of the allowed enum values |

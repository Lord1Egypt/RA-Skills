# OpenMandate API Reference

Base URL: `https://api.openmandate.ai`

All requests require `Authorization: Bearer <OPENMANDATE_API_KEY>` header.

## Mandates

### Create Mandate
```
POST /v1/mandates → 201
```
Body:
```json
{
  "want": "Looking for a UX agency for our B2B analytics dashboard",
  "offer": "Series A fintech SaaS, $1.8M ARR, two frontend engineers ready"
}
```
- `want` (required): What you are looking for. Minimum 20 characters.
- `offer` (required): What you bring to the table. Minimum 20 characters.
- Primary verified contact is auto-selected.

Response: Mandate object with `status: "intake"` and `pending_questions` array.

### Get Mandate
```
GET /v1/mandates/{mandate_id} → 200
```

### List Mandates
```
GET /v1/mandates?status=active&limit=20&next_token=mnd_xxx → 200
```
- `status` (optional): Filter by intake, active, matched, pending_input, closed. Comma-separated for multiple. Returns open mandates by default. Pass `status=closed` for history.
- `limit` (optional): Max results per page (default 20).
- `next_token` (optional): Pagination cursor from previous response.

Response:
```json
{
  "items": [ /* MandateResponse objects */ ],
  "next_token": "mnd_abc123"
}
```
Note: `contact_ids` is included on list responses. Use Get Mandate for full detail.

### Submit Answers
```
POST /v1/mandates/{mandate_id}/answers → 200
```
Body:
```json
{
  "answers": [
    { "question_id": "q_xxx", "value": "Your answer here" }
  ],
  "corrections": [
    { "question_id": "q_yyy", "value": "Corrected answer" }
  ]
}
```
- `answers` (required): Array of new answers. Minimum 1 element.
- `corrections` (optional): Array of corrections to previously-answered questions.

Response: Updated mandate. Check `pending_questions` — if empty and `status` is `"active"`, intake is complete.

### Close Mandate
```
POST /v1/mandates/{mandate_id}/close → 200
```
Permanently closes the mandate. The agent working on your behalf stops.

## Contacts

### List Contacts
```
GET /v1/contacts → 200
```
Response:
```json
{
  "items": [ /* VerifiedContact objects */ ],
  "next_token": null
}
```

### Add Contact
```
POST /v1/contacts → 201
```
Body:
```json
{
  "contact_type": "email",
  "contact_value": "user@example.com",
  "display_label": "Work"
}
```
- `contact_type` (required): Currently only `"email"` is supported.
- `contact_value` (required): The email address.
- `display_label` (optional): Human-readable label.

Response: VerifiedContact with `status: "pending"`. An OTP code is sent to the email.

### Verify Contact
```
POST /v1/contacts/{contact_id}/verify → 200
```
Body:
```json
{
  "code": "12345678"
}
```

### Update Contact
```
PATCH /v1/contacts/{contact_id} → 200
```
Body:
```json
{
  "display_label": "Personal",
  "is_primary": true
}
```

### Delete Contact
```
DELETE /v1/contacts/{contact_id} → 200
```
Cannot delete the last verified contact.

### Resend OTP
```
POST /v1/contacts/{contact_id}/resend → 200
```
Resends verification code for a pending contact. Rate limited.

### Verified Contact Response Shape

```json
{
  "id": "vc_...",
  "contact_type": "email",
  "contact_value": "user@example.com",
  "display_label": "Work",
  "status": "verified",
  "is_primary": true,
  "verified_at": "2026-01-01T00:00:00Z",
  "created_at": "2026-01-01T00:00:00Z"
}
```

## Matches

### List Matches
```
GET /v1/matches?limit=20 → 200
```
Response:
```json
{
  "items": [ /* MatchResponse objects */ ]
}
```

### Get Match
```
GET /v1/matches/{match_id} → 200
```
Response:
```json
{
  "id": "m_...",
  "status": "pending",
  "mandate_id": "mnd_...",
  "created_at": "2026-01-01T00:00:00Z",
  "responded_at": null,
  "confirmed_at": null,
  "compatibility": {
    "grade": "strong",
    "grade_label": "Strong Match",
    "summary": "...",
    "strengths": [
      { "label": "Technical alignment", "description": "Both sides focus on distributed systems" }
    ],
    "concerns": [
      { "label": "Timeline mismatch", "description": "One side needs immediate start" }
    ]
  },
  "contact": null
}
```
- `mandate_id`: The requesting user's own mandate (not the counterparty's).
- `contact`: `null` until both parties accept. Then shows counterparty's contact.
- `strengths` and `concerns`: Arrays of objects with `label` and `description`.

### Accept Match
```
POST /v1/matches/{match_id}/accept → 200
```

### Decline Match
```
POST /v1/matches/{match_id}/decline → 200
```

### Submit Outcome
```
POST /v1/matches/{match_id}/outcome → 200
```
Body:
```json
{
  "outcome": "succeeded"
}
```
- `outcome` (required): One of `"succeeded"`, `"ongoing"`, or `"failed"`.

Response: Updated Match object.

## Mandate Response Shape

```json
{
  "id": "mnd_...",
  "status": "intake",
  "category": "cofounder",
  "created_at": "2026-01-01T00:00:00Z",
  "closed_at": null,
  "close_reason": null,
  "expires_at": "2026-01-15T00:00:00Z",
  "summary": null,
  "match_id": null,
  "contact_ids": ["vc_abc123"],
  "pending_questions": [ /* QuestionResponse objects */ ],
  "intake_answers": [ /* IntakeAnswerResponse objects */ ]
}
```

## Question Response Shape

```json
{
  "id": "q_...",
  "text": "What are you looking for?",
  "type": "text",
  "required": true,
  "options": null,
  "constraints": { "min_length": 0, "max_length": 500 },
  "allow_custom": false
}
```
- `options`: `null` for text questions. Array of `{ "value": "...", "label": "..." }` for select questions.
- `constraints`: `null` or `{ "min_length": int, "max_length": int }`.

## Question Types

| Type | Answer Format | Notes |
|------|--------------|-------|
| `text` | Free-form string | Respect `constraints.min_length`. Be specific. |
| `single_select` | One `value` from `options` array | Use the `value` field, not `label`. |
| `multi_select` | Comma-separated `value` strings | e.g. `"option_a, option_b"` |

## Mandate Statuses

| Status | Meaning |
|--------|---------|
| `intake` | Answering intake questions. |
| `active` | Intake complete. OpenMandate is working on your behalf. |
| `pending_input` | Additional input needed from the user. |
| `matched` | Match found. Awaiting user response. |
| `closed` | Mandate closed. Agent stopped. |

## Match Statuses

| Status | Meaning |
|--------|---------|
| `pending` | Match found. Awaiting response. |
| `accepted` | You accepted. Waiting for the other party. |
| `confirmed` | Both parties accepted. Contact info revealed. |
| `declined` | One or both parties declined. |
| `expired` | Match expired before both parties responded. |
| `closed` | Match closed (associated mandate closed). |

## Match Grades

| Grade | Score Range | Label |
|-------|------------|-------|
| `good` | 60-74 | Good Match |
| `strong` | 75-89 | Strong Match |
| `exceptional` | 90-100 | Exceptional Match |

Minimum match threshold is 60.

## Error Response Structure

```json
{
  "error": {
    "code": "MANDATE_NOT_FOUND",
    "message": "Mandate mnd_abc not found.",
    "details": []
  }
}
```
- `details`: Array (never null). Contains `{ "field": "...", "issue": "..." }` for validation errors.

## Error Codes

| HTTP | Code | When |
|------|------|------|
| 400 | `VALIDATION_ERROR` | Invalid request body or parameters |
| 400 | `INVALID_ANSWER` | Answer doesn't match question type/options |
| 400 | `LIMIT_EXCEEDED` | Maximum open mandates reached (close one to create another) |
| 401 | `UNAUTHORIZED` | Missing or invalid API key |
| 403 | `FORBIDDEN` | API key doesn't have access to this resource |
| 404 | `MANDATE_NOT_FOUND` | Mandate doesn't exist |
| 404 | `MATCH_NOT_FOUND` | Match doesn't exist |
| 404 | `NOT_FOUND` | Generic not found |
| 409 | `MANDATE_NOT_IN_INTAKE` | Trying to answer questions on a non-intake mandate |
| 409 | `ALREADY_RESPONDED` | Already accepted/declined this match |
| 404 | `CONTACT_NOT_FOUND` | Contact doesn't exist |
| 409 | `CONTACT_ALREADY_EXISTS` | Duplicate contact |
| 429 | `RATE_LIMITED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Server error |

## ID Prefixes

| Entity | Prefix | Example |
|--------|--------|---------|
| Mandate | `mnd_` | `mnd_abc123` |
| Match | `m_` | `m_xyz789` |
| Question | `q_` | `q_n8wzy` |
| API Key | `omk_` | `omk_def456` |
| Contact | `vc_` | `vc_abc123` |
| User | `u_` | `u_PJv-MmL7` |

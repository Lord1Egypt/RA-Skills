# OpenMandate retained-access API reference

> OpenMandate is in private development. New mandates and integrations are not
> available. This reference is only for an existing account and API key.

Base URL: `https://api.openmandate.ai`

All requests require `Authorization: Bearer <OPENMANDATE_API_KEY>`.

## Historical reads

```text
GET /v1/mandates/{mandate_id}
GET /v1/mandates?status=closed&limit=20&next_token=mnd_xxx
GET /v1/contacts
GET /v1/matches?limit=20
GET /v1/matches/{match_id}
```

These operations expose only records owned by the authenticated account.

## Withdrawal actions

```text
POST   /v1/mandates/{mandate_id}/close
POST   /v1/matches/{match_id}/decline
DELETE /v1/contacts/{contact_id}
```

Confirm the exact target with the user before invoking a withdrawal action.

## Unavailable operations

Operations that create or advance work—including signup, contact creation or
verification, mandate creation or intake, match acceptance and outcome
submission—return `SERVICE_PRIVATE_DEVELOPMENT`. Do not direct a user to create
an account or API key.

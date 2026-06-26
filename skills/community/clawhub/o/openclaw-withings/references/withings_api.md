# Withings API (quick reference)

Docs: https://developer.withings.com/

## OAuth 2.0

- Authorize (user login/consent):
  - `https://account.withings.com/oauth2_user/authorize2`

- Token (exchange + refresh):
  - `https://wbsapi.withings.net/v2/oauth2`
  - Uses form params including `action=requesttoken` and `grant_type`.

Common scopes (Tier 1 personal):
- `user.metrics` (measurements: weight/BP/heart rate/etc.)
- `user.activity` (activity + sleep endpoints)

## Data endpoints (personal)

- Measurements:
  - `POST https://wbsapi.withings.net/measure` with `action=getmeas`
  - Filter with `startdate`/`enddate` (epoch seconds)

- Sleep summary (best-effort):
  - `POST https://wbsapi.withings.net/v2/sleep` with `action=getsummary`

Notes:
- Response formats may wrap data under `{ status, body: { ... } }`.
- Handle 429 with backoff.

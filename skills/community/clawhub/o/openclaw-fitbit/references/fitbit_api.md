# Fitbit API (quick reference)

OAuth2:
- Authorize: `https://www.fitbit.com/oauth2/authorize`
- Token: `https://api.fitbit.com/oauth2/token` (HTTP Basic auth with client_id:client_secret)

Typical scopes:
- `activity`
- `sleep`
- `heartrate`
- `profile`
- `weight`

Common endpoints used here:
- Daily activity summary:
  - `GET https://api.fitbit.com/1/user/-/activities/date/{YYYY-MM-DD}.json`
- Daily sleep:
  - `GET https://api.fitbit.com/1.2/user/-/sleep/date/{YYYY-MM-DD}.json`

# Oura API (quick reference)

Oura v2 API base:
- `https://api.ouraring.com/v2`

Auth:
- Personal Access Token (PAT)
- Send: `Authorization: Bearer <token>`

Common endpoints (usercollection):
- `GET /v2/usercollection/sleep?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- `GET /v2/usercollection/readiness?start_date=...&end_date=...`
- `GET /v2/usercollection/daily_activity?start_date=...&end_date=...`

Notes:
- Response typically shaped like `{ data: [...] }`.
- Record date keys vary by endpoint (e.g., `day` or `summary_date`).

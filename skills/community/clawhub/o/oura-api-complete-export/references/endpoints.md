# Oura API endpoints exported

This skill attempts all broadly available Oura v2 user collection endpoints.

- `/v2/usercollection/personal_info`
- `/v2/usercollection/daily_activity`
- `/v2/usercollection/daily_readiness`
- `/v2/usercollection/daily_sleep`
- `/v2/usercollection/daily_spo2`
- `/v2/usercollection/daily_stress`
- `/v2/usercollection/daily_resilience`
- `/v2/usercollection/sleep`
- `/v2/usercollection/workout`
- `/v2/usercollection/session`
- `/v2/usercollection/tag`
- `/v2/usercollection/heartrate`

Notes:
- Date endpoints use `start_date` + `end_date`.
- Heart-rate uses `start_datetime` + `end_datetime`.
- Pagination is handled via `next_token`.
- Export continues on endpoint-level failures and records errors in `summary.json`.

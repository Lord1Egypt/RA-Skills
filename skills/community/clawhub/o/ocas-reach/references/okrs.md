# OKRs

### schedule_adherence
- **Target**: `reach:update` cron runs within ±1h of scheduled time on ≥95% of days per month.
- **Measurement**: Compare wall-clock execution timestamps in `evidence.jsonl` against schedule (`0 0 * * *`). Runs outside the ±1h window are misses.

### data_integrity
- **Target**: Zero silent data loss events per month.
- **Measurement**: All query runs (including no-ops and errors) must have a corresponding entry in `evidence.jsonl` and `usage.jsonl`. Gaps detected during recovery audit are violations.

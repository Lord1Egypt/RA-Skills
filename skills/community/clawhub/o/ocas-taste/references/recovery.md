# Recovery Behavior

Implements the recovery contract from `spec-ocas-recovery.md`.

## Evidence

Every run writes to `evidence.jsonl`, including no-op runs (mandatory `not_activity_reason` field).

## Gap detection

On every wake, checks evidence log. If gap exceeds cadence (24h), logs `gap_detected`.

## Degraded mode

When Gmail/Calendar API tokens fail, implements fallback per cron failure pattern. Logs `degraded: <api>`.

## Log compaction

Evidence/decision logs older than 30 days (no-op) or 90 days (error/gap) compacted. Last 7 days retained.
# Source Connectors - Google Reviews

Use this matrix to keep source behavior explicit and stable.

## Source Types

| Source | Typical Coverage | Preferred Access | Main Risks |
|--------|------------------|------------------|------------|
| Google Business Profile reviews | Local business locations | Business Profile API | Missing locations, delayed sync |
| Google Shopping / merchant review signals | Product and merchant sentiment | Merchant API or user exports | Sparse product-level text, account scoping |
| Manual Google review pages | Spot checks and verification | User-approved fetch only | Rate limits and inconsistent structure |

## Connector Rules

1. Define owner and permissions before first fetch for each source.
2. Save connector status per brand: `active`, `degraded`, `blocked`.
3. Keep last-success timestamp and last-error reason for troubleshooting.
4. Use source-specific retry policy; do not retry indefinitely.

## Refresh Windows

- Heartbeat refresh: short trailing window (for example last 24-72h).
- Deep refresh: wider trailing window (for example 7-30d) to catch late edits.
- Backfills: run only when baseline is missing or source changed.

## Fallback Order

1. Official API path
2. User-provided export
3. Manual page verification

If all fail, report source outage and skip false certainty.

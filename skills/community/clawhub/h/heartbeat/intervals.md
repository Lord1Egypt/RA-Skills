# Interval Strategies

Use these interval profiles to tune heartbeat behavior safely.

## Baseline Profiles

| Profile | Default Interval | Burst Interval | Best For |
|---------|------------------|----------------|----------|
| Conservative | 45m | 10m | Low-noise workflows and cost-sensitive setups |
| Balanced | 30m | 5m | General productivity and ops monitoring |
| Aggressive | 15m | 2m | High-priority incident windows |

## Adjustment Rules

Shorten interval when:
- missed-event rate is above 10%
- deadline or incident proximity increases
- user explicitly asks for tighter follow-up

Extend interval when:
- signal quality is below 20% for 7 days
- last cycles produce repeated `HEARTBEAT_OK`
- user requests quieter operation

## Working Hours Strategy

Always combine interval policy with timezone and active hours.

Recommended pattern:
- active hours: normal interval
- off hours: multiply interval by 2-4 unless critical monitor is active

## Cost Guard Pattern

Before expensive checks, run a cheap precheck gate. If gate is false, skip expensive call and return `HEARTBEAT_OK`.

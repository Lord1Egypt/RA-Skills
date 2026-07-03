# Task: Analytics & decision

Goal: turn raw activity into a daily KPI summary and decide the next priority lane.
No backend — aggregate from local sources only.

## Sources (all local / in-workspace)
- `getState()` — live snapshot (pet health, coins, login).
- `agent/audit.log` — every agent write command (count by `cmd`, by `actor`).
- `agent/ops-state.json` — operator counters and last-run times.
- `agent/ops-journal.log` — narrative history.
- `sdk.remoteLog` (if accessible) — supplementary telemetry.

## KPIs to compute (daily)
- Care actions today (feed/clean/play) and current pet health.
- Content artifacts produced (mini-games / famous pets / stories).
- Marketing assets produced (cards / posts).
- Adoptions with an `agentOwner` bound (from pet records, if readable).

## Steps
1. Aggregate the above into a small `lastKpi` object.
2. Write `analytics.lastRunAt` and `analytics.lastKpi` to `agent/ops-state.json`.
3. Append a KPI line to `agent/ops-journal.log`.
4. Choose tomorrow's priority lane = the one most behind its target; record it.

## Example KPI line
```
[2026-06-09T08:00:00Z] KPI care=3 content=1 marketing=1 petHealth=78 next=content
```

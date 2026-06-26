# QA Checklist - HEARTBEAT.md

Run this checklist before shipping a heartbeat file.

## Contract Checks

- [ ] No-op path returns exactly `HEARTBEAT_OK`
- [ ] Actionable path is concise and deterministic
- [ ] No contradictory timing instructions

## Timing Checks

- [ ] Timezone is explicit
- [ ] Active hours are explicit
- [ ] Burst interval has a clear entry and exit condition
- [ ] Exact-time jobs are moved to cron

## Signal Quality Checks

- [ ] Each monitor has trigger thresholds
- [ ] Each alert has cooldown
- [ ] Duplicate suppression is defined
- [ ] Low-value checks have backoff rules

## Cost Checks

- [ ] Expensive APIs are behind cheap prechecks
- [ ] Paid calls have per-cycle caps
- [ ] Monitoring scope is limited to user goals

## Safety Checks

- [ ] Previous heartbeat snapshot kept for rollback
- [ ] Escalation routes are explicit
- [ ] Quiet-hours behavior is explicit

# Incident playbook

## First 10 minutes

1. Declare incident and assign commander.
2. Freeze risky deploys/config changes.
3. Capture first symptom timestamp and current metrics.
4. Publish first internal update with known unknowns.

## First 30 minutes

- identify affected payment flows/provider(s)
- quantify user/order impact
- choose containment action (degraded mode/pause/fallback)
- assign diagnostics and reconciliation tracks in parallel

## Recovery checklist

- fix/rollback applied safely
- error rates normalized
- queue/webhook backlog drained
- pending/mismatch reconciliation complete
- customer-facing states corrected


# Repeat Runs

When auditing a repo more than once, preserve continuity without trusting old
results as current truth.

## Stable IDs

Use stable finding IDs when the same issue remains:

- `HAM-001`
- `HAM-002`
- `HAM-003`

Do not recycle an old ID for a different issue.

## Transition Labels

- `NEW`: not present in the prior report.
- `UNCHANGED`: same issue, same evidence shape.
- `WORSE`: same issue with broader impact or stronger contradiction.
- `IMPROVED`: same issue still present but reduced.
- `RESOLVED`: prior issue no longer reproduces with current proof.
- `STALE_PRIOR`: prior issue cannot be rechecked because its evidence path is gone or blocked.

## Prior Reports

Prior reports are hints. Re-run current proof before marking anything resolved,
unchanged, or verified.

# Application & APM Investigation Reference

Load this when the incident involves service latency, error rates, failed deployments, or application-level behavior.

## Key Signals to Surface

- Error rate spike: 4xx vs 5xx breakdown, which endpoints affected
- Latency regression: p50/p95/p99, which downstream calls are slow
- Deployment correlation: did a deploy precede the incident? by how much?
- Dependency failures: which upstream/downstream service is the bottleneck
- Memory/CPU at application layer: GC pressure, thread pool exhaustion, connection pool saturation

## Suggested `neubird investigate` Prompts

```
"Error rate on the payments API went from 0.1% to 12% after the 3pm deploy"
"p99 latency on search doubled — trace where the time is going"
"The background job queue is backing up — investigate the consumer"
"Auth service is returning 401s for valid tokens since the last release"
"Memory usage on the API fleet is trending up and not GCing"
```

## Deployment Incident Triage

When a deploy is suspected:
1. Confirm deploy time vs. incident start time
2. What changed: code, config, dependencies, infrastructure?
3. Is rollback safe? (DB migrations, feature flags, API contract changes)
4. Blast radius: all users or subset (canary/regional rollout)?
5. Fix-forward criteria: is the fix obvious and low-risk?

## Rollback vs. Fix-Forward Decision

| Situation | Recommendation |
|-----------|---------------|
| DB migration included | Fix-forward (rollback may corrupt data) |
| Config-only change | Rollback is safe and fast |
| Canary caught it (<5% traffic) | Rollback immediately |
| >30min since deploy, widespread impact | Rollback unless migration blocks it |
| Root cause unknown | Rollback first, investigate on copy |

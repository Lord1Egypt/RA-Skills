# Self-Host Screen - Open Source

Run this before recommending self-hosting as the default path.

## Readiness Checks

| Area | Pass Signal | Failure Signal |
|------|-------------|----------------|
| Operations ownership | Named owner for uptime and incidents | "We'll figure it out later" |
| Backup discipline | Tested restores with schedule | Backup plan without restore tests |
| Upgrade safety | Version pinning and rollback path | Unpinned latest tags in production |
| Observability | Logs, metrics, and alerts defined | No visibility until user reports issues |
| Security baseline | Patch policy and secret handling | Ad hoc patching and plaintext secrets |

## Decision Outcomes

- All green: self-host is viable now.
- Mixed: self-host in pilot or staging first.
- Mostly red: prefer managed option, revisit self-host after ops maturity.

## Mandatory Notes in Recommendations

When self-host is recommended, explicitly include:
- Backup and restore frequency
- Upgrade window and rollback rule
- Monitoring stack minimum
- Security responsibilities by role

## Common Failure Patterns

- Treating self-host as a one-time setup instead of ongoing service ownership.
- Underestimating storage growth and backup window impact.
- Skipping test environments and upgrading directly in production.

# Hardening and Disaster Recovery

Use this playbook for security baselines and outage recovery planning.

## Security Baseline

- Enforce TLS for all API and console traffic.
- Use short-lived credentials where possible.
- Restrict wildcard policies and anonymous access.
- Enable audit logs and preserve immutable retention where required.

## Encryption Decisions

- Define server-side encryption defaults for critical buckets.
- Document key ownership and rotation policy.
- Validate restore workflows with encrypted objects.

## Backup and Restore Discipline

- Back up configuration and policy state along with object data.
- Test restore by reading real objects after recovery.
- Measure restore times and compare with target objectives.

## Incident Response Sequence

1. Freeze non-essential writes.
2. Capture cluster and bucket health snapshot.
3. Isolate scope (single bucket, node set, or policy domain).
4. Execute lowest-risk recovery path.
5. Verify data-path and auth-path integrity.
6. Resume traffic in stages with monitoring.

## Post-Incident Hardening

After recovery:
- record root cause and exact recovery steps
- update guardrails in `memory.md` and `incidents.md`
- tighten monitoring for the failure signature
- schedule a restore drill for the affected scenario

## Red Flags

- Recovery plans that have never been tested in a real restore.
- Shared admin credentials across environments.
- Policy updates without pre-change snapshots.
- Replication enabled without versioning checks.

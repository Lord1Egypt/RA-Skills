---
name: pscale-audit-log
description: Inspect PlanetScale organization audit events and download filtered authentication-attempt export archives. Use when investigating account activity, allowed or denied database logins, IP allowlist failures, usernames, branches, backend routes, or authentication timelines. Triggers on audit log, auth attempts, login failures, denied database connections, authentication export.
---

# pscale audit-log

Inspect organization audit events and export database authentication attempts.

## Common commands

```bash
# Existing organization audit events
pscale audit-log list --org <org> --format json

# Export the last 24 hours of denied authentication attempts
pscale audit-log auth-attempts download --org <org> \
  --since 24h --outcome deny --export-format jsonl \
  --output ./auth-attempts.zip
```

## Authentication-attempt exports

Choose exactly one time-window style:

- `--since <duration>` ending now, such as `24h`, `7d`, or `2w`; or
- `--start-at <time>` with optional exclusive `--end-at <time>`.

Named values (`now`, `today`, `yesterday`) and zone-less timestamps use the local timezone; the API request is normalized to UTC. For repeatable automation across hosts, prefer RFC3339 timestamps with an explicit offset.

```bash
# Explicit UTC interval
pscale audit-log auth-attempts download --org <org> \
  --start-at 2026-08-10T00:00:00Z \
  --end-at 2026-08-11T00:00:00Z \
  --outcome deny \
  --failure-reason bad_password \
  --export-format csv \
  --output ./denied-auth-attempts.zip

# Narrow to selected branches and source networks
pscale audit-log auth-attempts download --org <org> \
  --since 7d \
  --branch <branch-public-id> \
  --source-ip 203.0.113.0/24 \
  --backend-route postgres \
  --output ./filtered-auth-attempts.zip
```

Supported export formats are `jsonl`, `csv`, and `parquet`. Human/CSV CLI output defaults the artifact to CSV; JSON CLI output defaults it to JSONL. Filters include outcome (`allow`, `deny`), failure reason, source IP/CIDR, branch, username, startup database, and backend route (`postgres`, `pgbouncer`, `unknown`). Most list filters repeat or accept comma-separated values; `--username` is repeatable and preserves commas as part of the username.

The command creates an export, waits for readiness, and downloads a ZIP archive. Authentication data can contain usernames, IP addresses, and operational evidence: write it only to an approved path, do not print raw ZIP bytes with `--output -` into chat/logs, and share it only through approved channels. Confirm organization, interval, and filters before requesting a broad export.

## References

See `references/commands.md` for the command and flag surface.

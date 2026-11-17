# pscale audit-log

```text
Usage:
  pscale audit-log [command]

Available Commands:
  auth-attempts Download authentication-attempt export reports
  list          List all audit logs of an organization
```

The command help fence below is exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace.

## pscale audit-log auth-attempts download

```text
Generate an authentication-attempt export for a UTC time window, wait for it to be ready, and download its ZIP artifact. Use --since with a positive duration (24h, 7d, or 2w), or use --start-at and optionally --end-at. Named values and zone-less timestamps use the local timezone; requests are sent in UTC.

Usage:
  pscale audit-log auth-attempts download [flags]

Examples:
  # Export the last 24 hours.
	  pscale audit-log auth-attempts download --since 24h

	  # Export from local midnight yesterday through now.
	  pscale audit-log auth-attempts download --start-at yesterday

	  # Export a date-only window.
	  pscale audit-log auth-attempts download --start-at 2026-07-28 --end-at 2026-07-29

	  # Zone-less local ISO timestamps can use T or a space.
	  pscale audit-log auth-attempts download --start-at '2026-07-29 16:00' --end-at '2026-07-29 17:00'

	  # RFC3339 timestamps may include any explicit offset.
	  pscale audit-log auth-attempts download \
	    --start-at 2026-07-29T00:00:00Z --end-at 2026-07-29T01:00:00Z

	  # Export denied attempts from two addresses during a UTC window.
	  pscale audit-log auth-attempts download \
	    --start-at 2026-07-29T00:00:00Z --end-at 2026-07-29T01:00:00Z \
	    --source-ip 203.0.113.0/24 --source-ip 2001:db8::/32

Flags:
      --backend-route strings          Backend route: postgres, pgbouncer, unknown
      --branch strings                 Branch public ID or database/branch name (repeat or comma-separate)
      --end-at string                  Exclusive end: now, today, yesterday, YYYY-MM-DD, local ISO, or RFC3339; defaults to now
      --export-format string           Artifact format: jsonl, csv, parquet; defaults from --format (human/csv -> csv, json -> JSONL; parquet is explicit)
      --failure-reason strings         Failure reason: bad_password, unknown_user, authorization_failed, ip_not_allowed, other
  -h, --help                           help for download
      --outcome strings                Authentication outcome: allow or deny
      --output string                  Output file name, or - to write raw ZIP bytes to stdout
      --since string                   Export window ending now: positive duration such as 24h, 7d, or 2w
      --source-ip strings              Source IP address or CIDR range (repeat or comma-separate)
      --start-at string                Inclusive start: now, today, yesterday, YYYY-MM-DD, local ISO, or RFC3339
      --startup-database stringArray   Startup database name (repeatable)
      --username stringArray           Authentication username (repeatable; commas are part of the name, not separators)

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

`--since` is mutually exclusive with `--start-at`/`--end-at`; without `--since`, `--start-at` is required. The command generates the export, waits, and downloads its ZIP artifact.

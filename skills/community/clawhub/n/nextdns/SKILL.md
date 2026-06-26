---
name: nextdns
description: Query and troubleshoot NextDNS via the NextDNS API, especially when NextDNS is used as Technitium DNS upstream. Use for NextDNS profile inspection, analytics, recent logs, blocked-domain diagnosis, DNS upstream health checks, or creating safe read-only helper commands before any NextDNS configuration change.
---

# NextDNS

Use this skill for read-first NextDNS API work. Prefer inspection and diagnostics; ask Igor before any write, delete, log clear, profile edit, denylist/allowlist mutation, or monitoring that could expose sensitive browsing data externally.

## Helper

Use the bundled helper unless a task needs an unsupported endpoint:

```bash
python3 skills/nextdns/scripts/nextdns_helper.py --help
```

Authentication defaults:

- `NEXTDNS_API_KEY` for the API key.
- `NEXTDNS_PROFILE_ID` for the profile id.

Examples:

```bash
# List profiles available to the API key
NEXTDNS_API_KEY=... python3 skills/nextdns/scripts/nextdns_helper.py profiles

# Get profile config
python3 skills/nextdns/scripts/nextdns_helper.py profile

# Last 24h status summary
python3 skills/nextdns/scripts/nextdns_helper.py analytics status --from -24h

# Top blocked domains in last 24h
python3 skills/nextdns/scripts/nextdns_helper.py analytics domains --from -24h --status blocked --limit 20

# Recent blocked logs for a domain/search term
python3 skills/nextdns/scripts/nextdns_helper.py logs --from -24h --status blocked --search example.com --limit 50
```

The helper prints JSON with:

- `ok`: request success boolean.
- `status`: HTTP status if available.
- `url`: requested URL without API key.
- `response`: decoded API response.

## Workflow

1. Verify credentials with `profiles` before diagnosing deeper.
2. Identify the profile id; set `NEXTDNS_PROFILE_ID` or pass `--profile`.
3. For general health, check `analytics status --from -24h`, `analytics protocols --from -24h`, and `analytics domains --from -24h --status blocked`.
4. For Technitium upstream questions, correlate Technitium client/upstream behavior with NextDNS `logs` and `analytics protocols`.
5. For block/allow questions, inspect logs and reasons first. Do not modify lists unless Igor explicitly confirms the exact domain/action.

## API reference

Read `references/api-summary.md` when endpoint details, pagination, time-series parameters, logs, or response shapes matter.

## Safety notes

- NextDNS logs can reveal browsing/device activity. Summarize minimally and avoid pasting sensitive domains unless needed.
- API is marked beta by NextDNS; handle response changes defensively.
- Do not call destructive endpoints like `DELETE /profiles/:profile/logs` without explicit confirmation.
- Before config writes, export/read current profile and save a timestamped backup in the workspace or another user-approved location.

---
name: httping
description: Lightweight HTTP endpoint health checks with curl. Use when an agent needs to (1) verify one or more URLs are reachable, (2) collect status codes, TLS info, and timing, or (3) loop-check a service during deployment or incident triage without standing up a full monitoring tool.
---

# httping

Probe HTTP(S) endpoints and report reachability, status, and timing using `curl`. This skill keeps the logic in the caller; it only wraps the probe pattern.

## Prerequisites

- `curl` on `PATH` (run `curl --version` to confirm).
- Network egress to the target host; for HTTPS probes, a reachable CA bundle.
- Permission to contact the endpoint from the current host (proxy, VPN, or Tailscale constraints may apply).

## Basic steps

1. Confirm `curl` is available:

   ```bash
   command -v curl && curl --version | head -1
   ```

2. Probe a single endpoint and emit status + timing:

   ```bash
   curl -sS -o /dev/null \
     -w 'url=%{url_effective}\nhttp_code=%{http_code}\nremote_ip=%{remote_ip}\ntime_total=%{time_total}s\n' \
     https://example.com
   ```

3. Probe multiple endpoints from a list, skipping hostnames that fail to resolve:

   ```bash
   for u in https://example.com https://httpbin.org/get; do
     echo "== $u =="
     curl -sS -o /dev/null \
       -w 'http_code=%{http_code} time_total=%{time_total}s remote_ip=%{remote_ip}\n' \
       --max-time 8 "$u" || echo "probe_failed=$u"
   done
   ```

4. Check TLS handshake timing on HTTPS endpoints:

   ```bash
   curl -sS -o /dev/null \
     -w 'http_code=%{http_code}\ntls_append=%{ssl_verify_result}\ntime_connect=%{time_connect}s\ntime_appconnect=%{time_appconnect}s\ntime_total=%{time_total}s\n' \
     https://clawhub.com
   ```

5. Treat non-2xx/3xx codes, `probe_failed`, or `time_total` above SLA as the "unhealthy" branch and escalate from the caller.

## Output shape

- Success: lines such as `http_code=200 time_total=0.123s remote_ip=...`.
- Failure: `probe_failed=<url>` or `curl` exit code non-zero with stderr; surface the URL and reason.
- Caller keeps branching (alert vs. ignore); this skill only returns probe facts.

## Notes

- Keep `--max-time` bounded (5-10s) when looping so a stalled endpoint cannot wedge orchestration.
- Do not print response bodies with `-o /dev/null` during triage; they are not needed for health.
- For periodic checks, prefer cron or heartbeat scheduling over a tight `sleep` loop; see `references/scheduling.md`.

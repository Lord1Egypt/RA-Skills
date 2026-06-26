# Operations

## Health checks

- Plugin: `GET /health`
- Sidecar: startup logs include adapter health and claim/send loop status.

## Common operator actions

- Verify allowlisted groups in plugin config.
- Verify shared secret matches on plugin and sidecar.
- Verify sidecar auth mode (`bearer` or `hmac`) matches your deployment policy.
- Sidecar requests include timestamp + nonce headers by default; keep clocks roughly synchronized.
- Confirm sidecar can claim commands and ack statuses.
- Sidecar outbound send loop retries local UI send before ACKing failure.
- In-group operator commands: `/mail-health`, `/mail-bind list`, `/mail-bind set <alias> [target]`, `/mail-bind get <alias>`, `/mail-bind del <alias>`, `/mail-pause`, `/mail-resume`, `/mail-flush`, `/mail-last <email>`.
- For push mode, verify active watch subscriptions and webhook auth.
- Run manual sweep if needed: `POST /api/v1/admin/watch/sweep`.
- For quick local bridge path rehearsal, run `plugin/scripts/smoke_roundtrip.sh`.
- For push-mode rehearsal, run `plugin/scripts/smoke_push_roundtrip.sh`.
- Inspect active watches: `POST /api/v1/admin/watch/list`.
- Close one watch manually: `POST /api/v1/admin/watch/close`.
- Flush pending outbound queue: `POST /api/v1/admin/commands/flush`.
- Run full maintenance: `POST /api/v1/admin/maintenance/run`.
- Pause/resume ingest: `POST /api/v1/admin/monitoring/set`.
- Monitoring state check: `GET /api/v1/admin/monitoring/status`.
- Rerun latest query by email: `POST /api/v1/admin/query/rerun-last`.
- List recent delivery receipts: `POST /api/v1/admin/receipts/list`.
- List sidecar heartbeats: `POST /api/v1/admin/sidecars/list`.
  - entries include `stale` based on `SIDECAR_STALE_SEC`.
- List jobs by status: `POST /api/v1/admin/jobs/list`.
- Get aggregated job state counts: `POST /api/v1/admin/jobs/status-counts`.
- List outbound commands by status: `POST /api/v1/admin/commands/list`.
- Manage group bindings: `POST /api/v1/admin/bindings/{list|set|delete}`.

## Incident checklist

1. `health` endpoint mail adapter status
   - detailed view: `GET /api/v1/admin/health/detail`
2. sidecar logs for watcher/send failures
3. sidecar diagnostics endpoints (`/health`, `/groups`) if enabled
4. plugin SQLite state for command backlog
5. BHMailer API reachability and credentials
6. if proxy mode is enabled, validate sidecar `/bhmailer/webhook` reachability

Maintenance behavior:

- Plugin periodic maintenance auto-runs every `SWEEP_INTERVAL_SEC`.
- It sweeps expired watches, requeues stale claimed commands, and prunes old dedupe keys.

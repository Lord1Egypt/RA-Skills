---
name: pscale-branch
description: Manage PlanetScale branch creation, rename, protection, deletion, promotion/demotion, diff, restore/PITR, switchover, logs, and Postgres/Vitess/Neki live connections with approved termination. Use for Postgres/Neki maintenance; Postgres extensions, parameters and sizing; Vitess VTGate capacity and parameter rollouts; tablet throttling, routing rules, owned Lookup Vindex backfills, and vtctl MoveTables. Triggers on pscale branch, create branch, restore point, PITR, pscale logs, branch switchover, branch maintenance, branch connections, connections show, connections top, live connections, live sessions, kill, kill-transaction, deletion protection, extensions enable/disable, refresh-schema, schema_ready, schema snapshot readiness, schema diff, query patterns, Postgres parameters, resize, VTGate parameters/update/changes, tablet throttler, keyspace routing rules, lookup vindex, vtctl, vtctld, promote branch, demote branch, MoveTables, global keyspace.
---

# pscale branch

Create, delete, diff, and manage database branches.

## Destructive-operation safety

These gates apply to every destructive example here, including deletion, demotion, protection removal, connection/transaction termination, deploy-request closure/revert, and cleanup. Command examples and CLI confirmation prompts are not authorization.

1. Inspect fresh state and confirm support for the target engine and installed CLI. Obtain explicit approval for the exact organization and, where applicable, database, branch, and resource ID/name, plus the operation and flags; use an explicit `--org` on every operation. Stop on unsupported operations or uncertain identity.
2. Check dependencies and availability: applications, active users, child resources, routing, pending changes, and the maintenance window. Do not infer that a stale, merged, or unused-looking resource is disposable.
3. Require a verified recovery path that survives the operation: confirm backup/export usability and retention, or tested replacement/recreation instructions, ownership, and recovery time. A backup name alone is not verification; stop if recovery cannot be established.
4. Execute only the approved action. Force flags, descendant deletion, demotion, and disabling protection require separate explicit approval; never add them to work around a refusal. For a known headless session, obtain approval for the required force flag up front, before attempting the operation; stop if that approval is absent or any attempt is refused.
5. Perform read-back verification of the exact target and dependent service health. Inspect pending/asynchronous outcomes before claiming completion. Authentication/network errors are not proof of absence; an ambiguous result requires investigation, not an automatic retry.

## Common Commands

```bash
# Create branch from main
pscale branch create <database> <branch-name>

# Create branch from specific source
pscale branch create <database> <branch-name> --from <source-branch>

# Restore a new Postgres branch to a point in time (write; inspect and approve first)
pscale branch create <database> <branch-name> \
  --from <source-branch> \
  --restore-point <RFC3339-timestamp> \
  --cluster-size <postgres-cluster-size> \
  --wait \
  --format json

# List the default page (up to 100 branches)
pscale branch list <database>

# Page through larger branch sets
pscale branch list <database> --page 2 --per-page 100 --format json

# Show branch details
pscale branch show <database> <branch-name>

# Query recent PostgreSQL or Neki branch logs
pscale logs <database> <branch-name> --org <org> --format json --period 1h

# Rename a branch or change deletion protection (write; inspect and approve first)
pscale branch update <database> <branch-name> --new-name <new-name> --format json
pscale branch update <database> <branch-name> --deletion-protected=true --format json

# Inspect branch infrastructure/pods (supports Postgres and Vitess)
pscale branch infra <database> <branch-name> --format json

# List available extensions on a Postgres branch cluster image
pscale branch extensions list <database> <branch-name> --format json

# Start Postgres or Neki branch image maintenance (operational write; inspect and approve first)
pscale branch maintenance run <database> <branch-name> --format json

# Start a Postgres primary switchover (operational write; inspect and approve first)
pscale branch switchover <database> <branch-name> --candidate <replica-name> --format json
pscale branch switchover list <database> <branch-name> --format json
pscale branch switchover show <database> <branch-name> <switchover-id> --format json

# View schema diff
pscale branch diff <database> <branch-name>

# View schema
pscale branch schema <database> <branch-name>

# Inspect configurable Postgres parameters before changing them
pscale branch parameters list <database> <branch-name> --format json

# Queue one Postgres branch change request for size, replicas, and/or parameters
pscale branch resize <database> <branch-name> \
  --cluster-size PS_10_GCP_X86 \
  --replicas 2 \
  --parameters pgconf.max_connections=500 \
  --wait

# Inspect or cancel the latest queued change request
pscale branch resize status <database> <branch-name> --format json
pscale branch resize cancel <database> <branch-name> --format json

# Inspect and resize VTGates on a Vitess production branch
pscale branch vtgate show <database> <branch-name> --format json
pscale branch vtgate resize <database> <branch-name> \
  --vtgate-size VTG_320 \
  --vtgate-autoscaling \
  --vtgate-count 2 \
  --vtgate-max-count 8 \
  --vtgate-target-cpu-utilization 50 \
  --format json
pscale branch vtgate resize status <database> <branch-name> --format json

# Inspect live branch connections once (Postgres, Vitess, and Neki)
# For bounded headless top capture and trace safety, see Connection inspection below.
pscale branch connections show <database> <branch-name> --format json

# Download a branch query patterns CSV report
pscale branch query-patterns download <database> <branch-name> --output query-patterns.csv

# List/show generated branch query pattern reports
pscale branch query-patterns list <database> <branch-name> --format json
pscale branch query-patterns show <database> <branch-name> <report-id> --format json

# Delete a stale query pattern report only after explicit approval
pscale branch query-patterns delete <database> <branch-name> <report-id> --format json --org <org>

# Stream the CSV to stdout for pipelines
pscale branch query-patterns download <database> <branch-name> --output - > query-patterns.csv

# Inspect Vitess routing rules and tablet state
pscale branch routing-rules get <database> <branch-name>
pscale branch vtctl get-routing-rules <database> <branch-name>
pscale branch vtctl get-keyspace-routing-rules <database> <branch-name> --format json
pscale branch vtctl get-shard <database> <branch-name> --keyspace <keyspace> --shard <shard>
pscale branch vtctl list-tablets <database> <branch-name> --format json

# Inspect one Lookup Vindex workflow; table-keyspace is where the lookup table/workflow lives
pscale branch vtctl lookup-vindex show <database> <branch-name> \
  --table-keyspace <lookup-table-keyspace> \
  --name <vindex-name> \
  --format json

# Inspect one tablet's throttler state before proposing a change
pscale branch vtctl throttler status <database> <branch-name> \
  --tablet-alias <zone-tablet-alias> --format json

# Discover current MoveTables workflows before creating or advancing one
pscale branch vtctl move-tables list <database> <branch-name> --format json

# Create a Vitess MoveTables workflow whose generated sequence tables live in a global keyspace
pscale branch vtctl move-tables create <database> <branch-name> \
  --workflow <workflow> \
  --source-keyspace <source-keyspace> \
  --target-keyspace <target-keyspace> \
  --all-tables \
  --sharded-auto-increment-handling REPLACE \
  --global-keyspace <unsharded-global-keyspace>

# Delete only after the destructive-operation safety gates and Branch Cleanup review
pscale branch delete <database> <branch-name> --org <org>

# Promote only after exact-target lifecycle/capacity approval
pscale branch promote <database> <branch-name> --org <org>
```

## Workflows

### Paginate branch inventory

`pscale branch list` returns one page with up to 100 branches by default. For databases with larger branch inventories, request subsequent pages explicitly with `--page`; use `--format json` for automation and stop when a page is empty.

```bash
pscale branch list <database> --page 1 --per-page 100 --format json
pscale branch list <database> --page 2 --per-page 100 --format json
```

### Schema Migration Workflow (Standard)

```bash
# 1. Create development branch
pscale branch create my-database feature-migration --from main

# 2. Make schema changes (via shell, ORM, or direct SQL)
pscale shell my-database feature-migration
# ... run ALTER TABLE, CREATE TABLE, etc.

# 3. View changes
pscale branch diff my-database feature-migration

# 4. Create deploy request (safer than direct promotion)
pscale deploy-request create my-database feature-migration

# 5. Deploy via deploy request (see pscale-deploy-request)
```

### Quick Branch for MR/PR

```bash
# Match PlanetScale branch to your MR/PR branch
BRANCH_NAME="feature-add-user-preferences"
pscale branch create my-database $BRANCH_NAME --from main
```

See `scripts/create-branch-for-mr.sh` for automation.

### Restore a Postgres branch to a point in time

`pscale branch create --restore-point` creates a new PostgreSQL branch from a point-in-time recovery timestamp. This is a write that can allocate billable resources. Confirm the organization, database, source branch, timestamp, target branch name, cluster size, and retention/recovery objective with the user before running it.

If `--cluster-size` is omitted, a restore-point branch defaults to `PS-10`, a billable non-development size, rather than `PS_DEV`; always pass an explicit size. `--from` may be omitted only when `--restore <backup-id>` is supplied; with `--restore-point` and no `--restore`, the CLI requires `--from` and resolves the covering backup from that parent branch and timestamp. Prefer passing the source branch explicitly in automation.

```bash
# Inspect the intended source branch and its current state first
pscale branch show <database> <source-branch> --org <org> --format json

# After explicit approval, create and wait for the recovered branch
pscale branch create <database> <new-branch> --org <org> \
  --from <source-branch> \
  --restore-point <RFC3339-timestamp> \
  --cluster-size <postgres-cluster-size> \
  --wait \
  --format json

# Verify the resulting branch rather than relying only on the create exit code
pscale branch show <database> <new-branch> --org <org> --format json
```

Use an absolute RFC 3339 timestamp such as `2026-08-25T13:30:00Z`; do not infer a timezone or silently round the requested recovery point. The flag is PostgreSQL-only. The CLI permits `--restore <backup-id>` with `--restore-point` even when `--from` is omitted; in that mode, the recovery source is the supplied backup. Without `--restore`, the CLI resolves the backup needed by the API from the required parent branch and timestamp. If the user supplied a specific backup ID, read back both the backup and timestamp before creating the branch. The CLI still rejects combining `--restore-point` with `--seed-data`. If creation fails or times out, treat the outcome as unconfirmed and inspect the target branch before retrying.

### Schema Comparison

```bash
# Compare branch schema with main
pscale branch diff <database> <branch-name>

# View full branch schema
pscale branch schema <database> <branch-name>

# Export schema to file
pscale branch schema <database> <branch-name> > schema.sql
```

### Branch infrastructure

`pscale branch infra` shows branch infrastructure/pod state for Postgres and Vitess branches. Prefer JSON output when an agent needs to inspect or compare infrastructure state.

```bash
pscale branch infra <database> <branch-name> --org <org> --format json
```

Use this for read-only diagnostics. Do not infer that a schema/deploy operation is safe solely from infra output; combine it with branch status, schema diff, and deploy-request checks.

### PostgreSQL and Neki branch logs

`pscale logs` queries a signed logs endpoint for PostgreSQL and Neki branches; Vitess branches are rejected. Use bounded time windows, prefer JSON output, and avoid exposing sensitive SQL text, usernames, addresses, or application identifiers from log messages.

```bash
# Last hour from the primary server
pscale logs <database> <branch> --org <org> --format json --period 1h

# Search errors over a bounded interval
pscale logs <database> <branch> --org <org> --format json \
  --period 6h --level ERROR --query "connection refused"

# Use a paired absolute range; Neki can also filter by shard and pod/server
pscale logs <database> <branch> --org <org> --format json \
  --from <RFC3339> --to <RFC3339>
pscale logs <database> <branch> --org <org> --format json \
  --shard <shard> --server <pod> --page 2
```

Use either `--period` or paired `--from`/`--to`, not both. `--level`, `--server`, and `--shard` are comma-separated or repeatable. JSON output preserves parsed fields such as `time`, `level`, `message`, `role`, `shard`, `container`, `availability_zone`, `pod`, `stream_id`, and `raw_message`; malformed individual lines are skipped.

### Postgres branch extensions

`pscale branch extensions list` is read-only and returns the extensions available on the branch's current cluster image. It is not an inventory of installed `CREATE EXTENSION` state inside a database.

```bash
pscale branch extensions list <database> <branch> --org <org> --format json
```

The catalog includes `can_enable`, `requirements` (including `postgres_image_version` when provided), and `enabled`, which can be absent when its state is unavailable. Do not depend on removed `available`, `unavailable_reason`, or `loader` fields; use null-safe JSON inspection and review the current requirements. Before any toggle, require a known boolean `enabled` value for **every** entry in the complete catalog, not just the target. If any entry has missing/null `enabled`, stop and investigate; do not assume it is disabled or reconstruct the selection by guessing. Toggle only an exact catalog name with `can_enable: true` and a known enabled state. Enabling or disabling queues an asynchronous branch change request and may restart the database; it is not the SQL `CREATE EXTENSION` / `DROP EXTENSION` installed state inside each logical database. Neki extensions belong to configuration profiles (`pscale-neki`), not this branch-level toggle.

```bash
# Inspect the complete selection, topology, and current branch change request
pscale branch extensions list <database> <branch> --org <org> --format json

# Fail closed unless every catalog entry has a known boolean enabled state
set -o pipefail
pscale branch extensions list <database> <branch> --org <org> --format json |
  jq -e -s 'length == 1 and (.[0] | type == "array" and length > 0 and all(.[]; (.enabled | type) == "boolean"))' \
  > /dev/null || { printf '%s\n' 'Stop: extension selection is unavailable or incomplete.' >&2; exit 1; }

pscale branch infra <database> <branch> --org <org> --format json
pscale branch resize status <database> <branch> --org <org> --format json

# After explicit approval for the exact extension and restart impact
pscale branch extensions enable <database> <branch> <extension> --org <org> \
  --wait --wait-timeout 20m --format json
# Alternative: disable only the specifically approved extension
pscale branch extensions disable <database> <branch> <extension> --org <org> \
  --wait --wait-timeout 20m --format json

# Verify completion and the full resulting extension selection
pscale branch resize status <database> <branch> --org <org> --format json
pscale branch extensions list <database> <branch> --org <org> --format json
```

The CLI reads the catalog and resends a replacement selection containing only other entries with `enabled: true`, plus the target when enabling it. It checks unavailable state only for the target; other entries with missing/null `enabled` are omitted and could be unintentionally disabled. The all-entry preflight above is an operator safety requirement, not a guarantee enforced by the toggle command. Re-read the complete catalog immediately before the approved toggle and stop if any enabled state is unknown. Avoid concurrent extension changes: a stale selection can overwrite another operator's change. An already-matching selection returns `result: "no_change"` in JSON. A timeout or failed request does not prove nothing changed; inspect `resize status`, the complete catalog selection, and branch health before any retry. Review application dependencies and per-database installed-extension state before disabling; do not automatically drop SQL extensions or infer that enabling installed them.

### Rename or protect a branch

`pscale branch update` supports both Vitess and Postgres branches. It sends only flags explicitly provided and requires at least one of `--new-name` or `--deletion-protected`. Renames can break connection configuration, deployment jobs, scripts, and branch references; disabling deletion protection increases removal risk.

```bash
# Inspect the current branch first
pscale branch show <database> <branch> --org <org> --format json

# After reviewing downstream references and receiving explicit approval
pscale branch update <database> <branch> --org <org> \
  --new-name <new-name> \
  --deletion-protected=true \
  --format json

# Use an explicit false value to remove protection after approval
pscale branch update <database> <branch> --org <org> \
  --deletion-protected=false --format json

# Verify using the resulting branch name
pscale branch show <database> <resulting-branch-name> --org <org> --format json
```

Before a rename, inventory application connection settings, CI/CD jobs, deploy-request automation, and project `.pscale.yml` references. Show the complete proposed update and obtain explicit approval. If renaming and changing deletion protection together, verify both returned fields rather than assuming an all-or-nothing update.

### Postgres primary switchover

`pscale branch switchover` starts a Postgres-only primary switchover and returns immediately; it does not wait for completion. On a replicated branch, PlanetScale promotes the named `--candidate` from `branch infra`, or selects one when the flag is omitted. A single-instance branch has no replica to promote, so PlanetScale restarts the instance in place and the branch is unavailable while it returns. Writes are briefly interrupted in either case.

```bash
# Inspect instance names, roles, and replica availability
pscale branch infra <database> <branch> --org <org> --format json

# After confirming impact, target, and rollback/incident plan with the user
pscale branch switchover <database> <branch> --org <org> \
  --candidate <replica-name> --format json

# Re-read infra until the primary role and instance health are clear
pscale branch infra <database> <branch> --org <org> --format json

# Inspect switchover history/status if the create result is unclear
pscale branch switchover list <database> <branch> --org <org> --format json
pscale branch switchover show <database> <branch> <switchover-id> --org <org> --format json
```

Only one switchover can run on a branch at a time. If the create response contains a switchover ID, keep it with the incident notes and use `switchover show` for read-only status/detail lookup. Do not pass `--candidate` for a branch without replicas. A failed switchover has an unconfirmed outcome: the primary may still have moved and the CLI does not roll it back. Re-check `branch infra` and switchover history before any retry. Treat this as an availability-impacting operational write that always requires explicit approval.

### Postgres and Neki branch maintenance

`pscale branch maintenance run` starts asynchronous Postgres or Neki branch image maintenance. PlanetScale applies the image upgrade to replicas first, then switches over from the old primary to an upgraded replica. Expect seconds of unavailability during the switchover, and expect all direct connections to be terminated; applications must rely on retry logic. A single-instance branch has no replica to promote and is unavailable until the instance returns. For Neki configuration-profile maintenance, use `pscale-neki`. For Postgres weekly windows and scheduled events, use `pscale-maintenance`: `branch maintenance window show/set` and `event list/show/reschedule`. These scheduling commands do not support Neki. Review scheduled work before proposing an immediate run; neither rescheduling nor `run` is a cancellation or deadline bypass.

```bash
# PostgreSQL: inspect instance topology and make sure no resize request is in progress
pscale branch infra <database> <branch> --org <org> --format json
pscale branch resize status <database> <branch> --org <org> --format json

# Neki: page through the consolidated branch-wide in-flight change inventory
pscale branch changes list <database> <branch> --org <org> \
  --page 1 --per-page 100 --format json
pscale branch changes list <database> <branch> --org <org> \
  --page 2 --per-page 100 --format json

# After explicit approval for the target and impact
pscale branch maintenance run <database> <branch> --org <org> --format json

# Optionally include a PostgreSQL minor-version upgrade during maintenance
pscale branch maintenance run <database> <branch> --org <org> \
  --update-postgres-minor-version \
  --format json

# Track PostgreSQL async progress through branch infrastructure
pscale branch infra <database> <branch> --org <org> --format json

# Track Neki async progress with Neki-owned reads
pscale branch config-profile list <database> <branch> --org <org> --format json
pscale branch router list <database> <branch> --org <org> --format json
pscale branch admin show <database> <branch> --org <org> --format json
```

Maintenance cannot start while a change request is in progress. For PostgreSQL, check `branch resize status`; for Neki, use `pscale branch changes list` because it inventories admin, cluster, configuration-profile, router, and sidecar requests in one branch-wide surface. Do not apply a state filter: query the unfiltered JSON inventory with explicit `--page` and `--per-page`, continue until a page is empty, and treat every entry with `completed_at: null` as in flight. This avoids hiding current or future non-terminal states behind a hard-coded filter. Treat this as an availability-impacting operational write: show the target branch, topology or Neki component state, expected connection termination/unavailability, minor-version choice when applicable, and incident/rollback plan before asking for approval.

### Connection inspection and safe termination

`pscale branch connections` supports Postgres/Vitess connections and Neki client sessions across the branch's routers. Prefer JSON output for agent workflows so identifiers are explicit and not truncated. Neki supports `show`, `top`, query/connection `kill`, and `kill-transaction`. Use only the selected row's server-issued `query_id`, `connection_id`, or `transaction_id` for its matching action; never substitute a PID, router UID, or sidecar/backend ID. Check the [source-backed action compatibility note](references/commands.md#pscale-branch-connections-kill) before proposing Neki actions. Client support does not establish server feature availability or permission; stop on unavailable action IDs or a refusal.

For Neki, omit Vitess `--keyspace`/`--shard` targets and Postgres `--instance`/`--role` filters: the CLI rejects these engine-specific flags. JSON connection rows can include `router_name`, `router_cell`, `router_uid`, `availability_zone`, `backend_start`, and `sidecar_backends`; the last contains shard/backend details, not independently actionable kill IDs. Preserve the top-level `warnings` array: unreachable-router warnings mean incomplete results even when the command succeeds or returns no sessions. Do not claim an empty result proves the branch has no connections. Live Neki `top` can offer cancellation/termination actions. Replay remains read-only and rejects backend actions.

On a connections-endpoint 404, the CLI automatically looks up the database and branch to distinguish a missing target from live connections not being enabled. Treat its specific missing-database, missing-branch, or disabled-live-connections message as the diagnosis. Only if the ambiguous fallback ("does not exist ... or live connections are not enabled") remains because those lookups failed, run read-only `pscale database show <database> --org <org> --format json` and `pscale branch show <database> <branch> --org <org> --format json` to investigate. Do not create or change resources to bypass the error.

```bash
# Inspect current connections once
pscale branch connections show <database> <branch-name> --format json --org <org>

# Capture a bounded live-activity trace in a headless agent shell
pscale branch connections top <database> <branch-name> --org <org> --capture <trace-file> --duration 30s

# Cancel a query only after confirming the query_id with the user
pscale branch connections kill <database> <branch-name> <query-id> --query --org <org>

# Terminate a connection only after explicit user approval
pscale branch connections kill <database> <branch-name> <connection-id> --org <org>

# Postgres or Neki only: terminate a transaction after explicit user approval
pscale branch connections kill-transaction <database> <branch-name> <transaction-id> --org <org>
```

Prefer one-shot JSON `show` for agents. Headless `top` requires `--capture`; `--duration` bounds execution in both headless and TUI modes. Use an approved private trace path because captures can contain sensitive session/query data; do not log or commit them. In a TTY, `top` opens an interactive TUI instead.

`kill --query` cancels the matching query; plain `kill` terminates the matching connection. Postgres/Neki `kill-transaction` terminates the connection matching the transaction ID, not merely one SQL statement; Vitess does not support it. These CLI action commands do not prompt for confirmation. Treat `kill` and `kill-transaction` as destructive operational actions: show the selected row, explain the effect, get confirmation, run exactly one action, then verify with `connections show`.

In live `top`, `c`, `k`, and `Shift+K` correspond to query cancellation, transaction termination, and connection termination where supported. Footer controls are filtered by the selected row's required action IDs; in the Blockers detail tab the highlighted blocker is the target, so confirm its identity rather than the original subject. A known permission denial hides/disables actions. The CLI combines database and organization permissions and selects `manage_production_live_connections` for a production branch or `manage_live_connections` otherwise. If branch/permission lookup fails, controls may remain visible because authorization is enforced by the server on every kill; visible keys are not proof of permission or user approval. Replay never authorizes actions.

JSON action output includes `success` and optional `keyspace`, `shard`, `tablet`, `id`, and `kind`; absent fields must not be synthesized. Human action text alone does not prove success. Inspect the result and re-read the exact session plus application health, preserving incomplete-result warnings. Stop on stale IDs, permission failures, or uncertain outcomes rather than selecting another session or retrying automatically.

### Query pattern reports

`pscale branch query-patterns` manages branch-level query pattern reports for query-shape analysis before tuning indexes, schema, or application query patterns. `list` and `show` are read-only. `download` generates/polls/downloads a CSV report. `delete` removes one generated report and requires explicit approval for the exact report ID.

```bash
# List generated reports, paging by cursor when needed
pscale branch query-patterns list <database> <branch-name> --org <org> --format json
pscale branch query-patterns list <database> <branch-name> --org <org> \
  --starting-after <cursor> \
  --limit 100 \
  --format json

# Inspect one report before downloading or deleting it
pscale branch query-patterns show <database> <branch-name> <report-id> --org <org> --format json

# Download with an explicit output path
pscale branch query-patterns download <database> <branch-name> --org <org> --output query-patterns.csv

# If --output is omitted, pscale writes a timestamped file in the current directory:
# query-patterns-<organization>-<database>-<branch>-<timestamp>.csv
pscale branch query-patterns download <database> <branch-name> --org <org>

# Use --output - to write the CSV to stdout for shell pipelines
pscale branch query-patterns download <database> <branch-name> --org <org> --output - > query-patterns.csv

# Delete only after confirming the exact report ID and target branch
pscale branch query-patterns delete <database> <branch-name> <report-id> --org <org> --format json
```

The command group requires Query Insights to be enabled for the database. A not-found error can mean either the branch/report does not exist or Query Insights is disabled. Prefer an explicit `--output` path in automation so downstream analysis can find the CSV deterministically; use `--output -` when a pipeline should consume the CSV from stdout. For deletion, `--force` only skips the prompt; it is not approval. Re-run `list` or `show` after deletion and verify the report is gone.

### Change a Postgres branch

`pscale branch resize` queues one asynchronous change request that can combine cluster size, replica count, and configuration parameter changes. At least one of `--cluster-size`, `--replicas`, or repeatable `--parameters namespace.name=value` is required. This command rejects MySQL databases; use `pscale keyspace resize` for Vitess keyspaces.

```bash
# Inspect the parameter catalog first. The bare `parameters` form is equivalent.
pscale branch parameters list <database> <branch-name> --org <org> --internal=false --format json
pscale branch parameters list <database> <branch-name> --org <org> --internal=false --namespace pgconf --format json

# List valid Postgres cluster sizes
pscale size cluster list --engine postgresql --org <org>

# Combine desired changes into one request and wait up to 20 minutes
pscale branch resize <database> <branch-name> --org <org> --format json \
  --cluster-size PS_10_GCP_X86 \
  --replicas 2 \
  --parameters pgconf.max_connections=500 \
  --wait --wait-timeout 20m

# Without --wait, inspect the latest request before assuming completion
pscale branch resize status <database> <branch-name> --org <org> --format json

# Cancel only while the change request is still queued
pscale branch resize cancel <database> <branch-name> --org <org> --format json
```

Use `parameters list --internal=false` to discover candidate parameters and review `restart`, `requires_update`, current, and default values before proposing a change. The human table adds a `REQUIRES UPDATE` column: `Yes` means the decoded `requires_update` pointer was non-null; `No` means it was null, whether the API sent an explicit null or omitted the field. This is separate from the `RESTART` column. JSON preserves `requires_update` as a string or `null`, not a boolean; retain the exact string (for example, `cluster`) rather than parsing table positions or assuming a fixed vocabulary. A non-null value, including an empty or unfamiliar string, is a reason to stop and investigate the indicated resource update before proposing a parameter write. Do not automatically run maintenance, resize capacity, or infer a new CLI flag from the indicator. A supported CLI always serializes the `requires_update` key for each entry, without omitting nulls: API omission and explicit null both become `requires_update: null`. A missing key therefore indicates an older CLI or incompatible output; stop, verify compatibility, upgrade if needed, and obtain a fresh catalog. Neither `null` nor table `No` is positive evidence that no resource update is required; neither authorizes a write or establishes that no restart is required.

The human parameter table includes an `INTERNAL` boolean column and JSON entries expose `internal`. Internal parameters are not change candidates; retain the `--internal=false` discovery gate. A decoded `internal: false` alone is not authorization: the typed boolean cannot distinguish API omission from explicit false. Do not depend on removed `immutable` or `extension` JSON fields: the API filters internal/extension parameters via `--internal=true|false` and `--extension=true|false`; omitting either filter leaves that category unfiltered. Resize preflight fetches the catalog with `internal=false` and rejects names absent from it, but does not check `requires_update` before submitting the change. The agent-side stop above is the local update-requirement gate; any server enforcement is left to the API. Parameter values can reflect a queued request, not only applied state. Surface restart impact, update requirements, and capacity/cost impact to the user, then obtain approval before running `resize`. Request states include `queued`, `pending`, `resizing`, `completed`, and `canceled`; only the last two are terminal. A JSON no-op returns `{"result":"no_change","branch":"<branch>"}` rather than a change request. After completion, verify with `resize status`, `branch show`, and a fresh parameter catalog.

Resize preflight is best-effort: if its parameter-catalog fetch fails, the CLI proceeds without local catalog/restart validation and leaves enforcement to the API. Do not treat that fallback as proof a parameter is safe; obtain a successful fresh catalog read and review restart/availability impact before an approved resize.

### Resize Vitess VTGates

`pscale branch vtgate` manages VTGate capacity for Vitess production branches. Development branches cannot be resized. Inspect current capacity first, propose the exact size/count/autoscaling change and cost/capacity impact, and obtain approval before creating or canceling a resize.

```bash
# Read the applied configuration
pscale branch vtgate show <database> <branch> --org <org> --format json

# Fixed capacity: two VTGates per availability zone
pscale branch vtgate resize <database> <branch> --org <org> --format json \
  --vtgate-size VTG_320 \
  --vtgate-count 2 \
  --vtgate-autoscaling=false

# Autoscaling: minimum two and maximum eight VTGates per availability zone
pscale branch vtgate resize <database> <branch> --org <org> --format json \
  --vtgate-size VTG_320 \
  --vtgate-autoscaling \
  --vtgate-count 2 \
  --vtgate-max-count 8 \
  --vtgate-target-cpu-utilization 50

# Track the latest request; cancel only while it is still queued
pscale branch vtgate resize status <database> <branch> --org <org> --format json
pscale branch vtgate resize cancel <database> <branch> --org <org> --format json
```

At least one resize flag is required. Omitted flags preserve their current values; pass `--vtgate-autoscaling=false` explicitly to disable autoscaling. `--vtgate-count` is the per-availability-zone fixed count, or the minimum when autoscaling is enabled. After the request completes, verify both `resize status` and `vtgate show`; do not treat the requested values as applied while status is non-terminal.

### Vitess VTGate parameter rollouts

Parameter changes are separate from VTGate capacity resizing and from keyspace VTTablet/MySQL parameters. Read the current/default catalog with `pscale branch vtgate parameters` (`params` is an alias), then use exact `vtgate.<name>` identifiers. There is no `parameters list` child here.

```bash
# Read the catalog and enumerate every change page before proposing a write
pscale branch vtgate parameters <database> <branch> --org <org> --format json
pscale branch vtgate changes list <database> <branch> --org <org> \
  --page 1 --per-page 25 --format json

# After approval for the exact value and operational impact
pscale branch vtgate update <database> <branch> --org <org> \
  --parameters vtgate.query-timeout=30000 --format json
# Alternative: restore one approved server default
pscale branch vtgate update <database> <branch> --org <org> \
  --reset vtgate.query-timeout --format json

# Verify each returned change ID and final catalog values
pscale branch vtgate changes show <database> <branch> <change-id> --org <org> --format json
pscale branch vtgate parameters <database> <branch> --org <org> --format json

# Cancel only an inspected pending change after separate explicit approval
pscale branch vtgate changes cancel <database> <branch> <change-id> --org <org> --format json
pscale branch vtgate changes show <database> <branch> <change-id> --org <org> --format json
```

`update` requires at least one repeatable `--parameters vtgate.name=value` or `--reset vtgate.name`; duplicate names and other namespaces are rejected. Compare fresh current/default values yourself and omit no-ops. Query `changes list` with increasing `--page` values until an empty page; it returns one page (25 by default), not a complete history. Preserve raw JSON (`state`, `completed_at`, `error_message`, `previous_options`, `new_options`); do not infer completion from a successful command or human change summary. Require a completed, non-error result and a fresh catalog matching every intended value/default reset, treating unknown states conservatively.

The CLI creates a draft, submits it, and then fetches the change; if the final fetch fails, it prints the pre-submit draft. Submission failure triggers only best-effort cancellation, so inspect the full change inventory after any failed or ambiguous write before retrying. Avoid concurrent rollouts; do not cancel an unidentified draft merely to clear the queue. `changes show` / `cancel` use the branch-wide config-change endpoint: confirm the returned `change_type` is `vtgate` and the ID belongs to the approved VTGate change. Capacity remains managed by `vtgate resize` and its own status/cancel commands, not `vtgate update`.

### Refresh a MySQL/Vitess schema snapshot

`pscale branch refresh-schema` requests a new schema snapshot and waits for the branch's `schema_ready` field to become true before reporting success. It performs an immediate branch lookup, then polls every 2 seconds with a 2-minute bound on the readiness wait. There is no configurable wait/timeout flag. This refresh is a write: confirm the exact organization, database, and branch and obtain explicit approval before requesting it.

```bash
# Inspect the target and readiness first
pscale branch show <database> <branch> --org <org> --format json

# After approval, refresh and wait for the snapshot
pscale branch refresh-schema <database> <branch> --org <org> --format json

# Verify readiness and re-read snapshot consumers before planning any write
pscale branch show <database> <branch> --org <org> --format json
pscale branch routing-rules get <database> <branch> --org <org> --format json
```

Success JSON is `{ "result": "schema refreshed" }`. If the wait expires while the snapshot is still unready, the command fails with `status: "action_required"`, `issues[0].code: "schema_refreshing"`, and one `next_steps` instruction to wait for readiness, then retry. API-supplied `schema_refreshing` and `schema_snapshot_not_ready` codes are both preserved and classified as retryable readiness waits. When the CLI's readiness-wait timeout occurs, the refresh request was already accepted; do not re-issue it. Either code alone is not proof of acceptance: API-supplied errors can preserve the same code, and an initial refresh-request failure returns before the wait starts. Distinguish the timeout stage from a request/polling error using the command outcome and error details; never automatically repeat a refresh write on a timeout or ambiguous outcome. For recovery, perform at most 30 read-only `branch show --format json` checks of `.schema_ready`, with 4 seconds between checks and an overall 2-minute deadline, stopping at whichever limit is reached first. Stop on an API/command failure or missing/null readiness instead of treating it as false. Once readiness is true, retry only the follow-up reader, not the refresh write. If readiness stays false at the bound, stop and investigate; do not restart the loop automatically.

Polling failures are not automatically snapshot timeouts: branch-not-found returns immediately; other lookup errors are retried during the wait and the outstanding poll error is returned at the deadline. A successful lookup clears the saved error. Preserve the actual error/code and diagnose it before retrying; do not turn network/API failures into a generic readiness loop. For routing-rule changes, re-read snapshot and live routing and rebuild the full proposed replacement after readiness, then obtain the write approval described below.

### Routing rules

```bash
# Read routing rules from the branch schema snapshot
pscale branch routing-rules get <database> <branch-name>

# Vitess only: read live routing rules from vtctld/current cluster state
pscale branch vtctl get-routing-rules <database> <branch-name>

# Vitess only: read live keyspace-to-keyspace routing rules
pscale branch vtctl get-keyspace-routing-rules <database> <branch-name> --format json

# Update routing rules from a file
pscale branch routing-rules update <database> <branch-name> --routing-rules routing-rules.json

# Replace live keyspace routing rules (approved write)
pscale branch vtctl apply-keyspace-routing-rules <database> <branch-name> \
  --rules-file keyspace-routing-rules.json --format json
```

Use `vtctl get-routing-rules` when debugging propagation/live cluster state; use `routing-rules get` when you need the MySQL branch schema-snapshot contract. `routing-rules show` aliases that same schema-snapshot lookup; check `pscale version` against the [local alias compatibility minimum](references/commands.md#pscale-branch-routing-rules-get) before using it, and prefer canonical `get`. It is not the live `vtctl` reader and does not update rules. Human output writes staleness warnings to stderr. JSON preserves the structured `warnings` array, and the CLI rewrites warning messages, so automation must test `.warnings[].code == "schema_mutation_in_progress"` rather than matching message text. CSV is unsupported for this command and fails instead of rendering the resource. `routing-rules update` is a full replacement, not a merge. It refuses to write while a vtctld schema mutation is active (`schema_mutation_blocked`) or the branch schema snapshot is not ready (`schema_snapshot_not_ready`); wait, re-read both snapshot and live state, then rebuild the proposed replacement before retrying.

Keyspace routing rules are a separate live map of `from_keyspace` to `to_keyspace`. Before replacing them, save `get-keyspace-routing-rules` output, validate every entry includes both fields, show the complete proposed replacement, and obtain explicit approval. `apply-keyspace-routing-rules` requires exactly one of `--rules` or `--rules-file`; an empty `rules` array clears all live keyspace routing rules. By default the command rebuilds SrvVSchema objects; use `--cells` only to scope that rebuild deliberately, and use `--skip-rebuild` only with an explicit propagation plan. Re-run `get-keyspace-routing-rules` after the write and compare the full returned set.

### Vitess shard inspection

`pscale branch vtctl get-shard` reads a live shard record from vtctld, including tablet controls and denied tables. It is Vitess-only and requires both `--keyspace` and `--shard`.

```bash
# Inspect an unsharded keyspace
pscale branch vtctl get-shard <database> <branch-name> \
  --keyspace main \
  --shard '-'

# Inspect a sharded keyspace shard
pscale branch vtctl get-shard <database> <branch-name> \
  --keyspace commerce \
  --shard '-80'
```

### Vitess tablet throttler configuration

`pscale branch vtctl throttler update-config` mutates a Vitess keyspace's tablet-throttler policy. Inspect tablet aliases and current state first, show the exact keyspace/app/metrics/rule to the user, and obtain explicit approval before changing it.

```bash
# Discover tablets and inspect current throttler state
pscale branch vtctl list-tablets <database> <branch> --org <org> --format json
pscale branch vtctl throttler status <database> <branch> --org <org> \
  --tablet-alias <zone-tablet-alias> --format json

# Temporarily throttle an app at 50% for 30 minutes
pscale branch vtctl throttler update-config <database> <branch> --org <org> \
  --keyspace <keyspace> \
  --throttle-app rowstreamer \
  --throttle-app-ratio 0.5 \
  --throttle-app-duration 30m \
  --format json

# Remove one app throttle rule
pscale branch vtctl throttler update-config <database> <branch> --org <org> \
  --keyspace <keyspace> --unthrottle-app rowstreamer --format json

# Assign the metrics checked for one app
pscale branch vtctl throttler update-config <database> <branch> --org <org> \
  --keyspace <keyspace> --app-name vreplication \
  --app-metrics lag,loadavg --format json

# Change the keyspace's overall enable state explicitly
pscale branch vtctl throttler update-config <database> <branch> --org <org> \
  --keyspace <keyspace> --enabled=false --format json
```

Rules:

- Omit `--enabled` to preserve the current enable state; use `--enabled=true` or `--enabled=false` only for an approved state change.
- `--throttle-app` and `--unthrottle-app` are mutually exclusive.
- `--app-name` and `--app-metrics` must be passed together; `--app-name` cannot be empty.
- `--throttle-app-ratio` is between `0.00` and `1.00` and defaults to `1`; `--throttle-app-duration` defaults to one hour.
- `--threshold` changes the replication-lag threshold (in seconds) for the keyspace's default check; treat it as a keyspace-wide mutation that needs the same explicit approval as an app rule change.
- After a write, re-run `throttler status` on the relevant tablets and verify the returned policy. Do not assume one tablet proves cluster-wide propagation when the branch has multiple tablets.

### Vitess Lookup Vindex lifecycle

`pscale branch vtctl lookup-vindex` creates and manages a Vitess Lookup Vindex backfill workflow. Every lifecycle action changes live workflow or VSchema state except `show`. Confirm the organization, database, branch, owner table, owner columns, lookup table, both keyspaces, vindex type, and recovery plan before creating or advancing one.

The keyspace flags have distinct meanings:

- `--keyspace` is the owner table's keyspace, where the lookup vindex is defined in the VSchema.
- `--table-keyspace` is where the lookup table and its backfill workflow are created and managed.

Do not swap them. `--table-keyspace` and `--name` identify the workflow for every follow-up command; commands that alter owner-side VSchema state also accept `--keyspace`.

```bash
# Inspect branch schema/routing and any existing workflow first
pscale branch schema <database> <branch> --org <org>
pscale branch vtctl lookup-vindex show <database> <branch> --org <org> \
  --table-keyspace <lookup-table-keyspace> \
  --name <vindex-name> \
  --format json

# After explicit approval, create the lookup table and backfill workflow
pscale branch vtctl lookup-vindex create <database> <branch> --org <org> \
  --keyspace <owner-table-keyspace> \
  --table-keyspace <lookup-table-keyspace> \
  --name <vindex-name> \
  --type <lookup-vindex-type> \
  --table-owner <owner-table> \
  --table-owner-columns <owner-column> \
  --table-name <lookup-table> \
  --format json

# Verify progress before any lifecycle transition
pscale branch vtctl lookup-vindex show <database> <branch> --org <org> \
  --table-keyspace <lookup-table-keyspace> --name <vindex-name> --format json

# Run only the specifically approved transition
pscale branch vtctl lookup-vindex externalize <database> <branch> --org <org> \
  --keyspace <owner-table-keyspace> --table-keyspace <lookup-table-keyspace> \
  --name <vindex-name> --format json
pscale branch vtctl lookup-vindex internalize <database> <branch> --org <org> \
  --keyspace <owner-table-keyspace> --table-keyspace <lookup-table-keyspace> \
  --name <vindex-name> --format json
pscale branch vtctl lookup-vindex complete <database> <branch> --org <org> \
  --keyspace <owner-table-keyspace> --table-keyspace <lookup-table-keyspace> \
  --name <vindex-name> --format json
pscale branch vtctl lookup-vindex cancel <database> <branch> --org <org> \
  --table-keyspace <lookup-table-keyspace> --name <vindex-name> --format json
```

For an owned Lookup Vindex, `--continue-after-copy-with-owner` defaults to `true` and is always sent to the API. This keeps the backfill workflow running after the copy phase so writes that bypass VTGate, including rows applied by VReplication during an import, continue reaching the lookup table. Pass `--continue-after-copy-with-owner=false` only when the user explicitly wants the workflow stopped after copy and understands the write-propagation gap.

Do not externalize until the copy/backfill state and lookup-table consistency are verified. `externalize --delete` also removes the workflow, so omit `--delete` unless that irreversible cleanup was separately approved. Treat `internalize`, `complete`, and `cancel` as distinct actions, never interchangeable recovery guesses. After each action, re-run `show` and inspect schema/routing state; a not-found result after cleanup is only expected when the approved action removed the workflow.

### Vitess MoveTables and global sequences

Prefer canonical `pscale branch vtctl move-tables` for new table-movement work. `vtctld` remains a compatibility alias. Generated help uses `vtctl`, while MoveTables `next_steps` may emit the compatible `pscale branch vtctld` form; treat either as the same command surface. The top-level `pscale workflow` family is deprecated and emits a warning for the parent and its subcommands; do not start new work through that legacy surface. The top-level `pscale data-imports` family is unavailable; use external keyspaces plus MoveTables instead.

`branch vtctl` is listed in `pscale branch --help`. Its `lookup-vindex`, `materialize`, `planned-reparent-shard`, and `list-tablets` children are visible in the vtctl parent listing. Visibility is command discovery, not authorization to mutate topology. Complete Lookup Vindex help is captured in `references/lookup-vindex-commands.md`. `list-tablets` is used by the throttler workflow above; check its direct `--help` when a current CLI is available. Materialize and PlannedReparentShard are not operationally covered by this skill.

Start with `pscale branch vtctl move-tables list` to inventory workflows on the branch. Omitting `--target-keyspace` lists workflows across every keyspace; pass the flag only to filter deliberately. Each JSON workflow that exposes its name and target keyspace includes a generated `next_steps` status command while preserving the API's original wrapper or raw-array shape.

`pscale branch vtctl move-tables create` supports `--global-keyspace`. Use it with `--sharded-auto-increment-handling REPLACE` when backing sequence tables for sharded auto-increment columns must be created in a specific unsharded keyspace.

```bash
# Discover every current workflow, then optionally narrow to one target keyspace
pscale branch vtctl move-tables list <database> <branch-name> --org <org> --format json
pscale branch vtctl move-tables list <database> <branch-name> \
  --org <org> --target-keyspace commerce --format json

pscale branch vtctl move-tables create <database> <branch-name> \
  --workflow move-commerce \
  --source-keyspace source \
  --target-keyspace commerce \
  --tables orders,order_items \
  --sharded-auto-increment-handling REPLACE \
  --global-keyspace global \
  --stop-after-copy

# Start a workflow created with --auto-start=false, or resume one stopped by
# --stop-after-copy or an explicit stop
pscale branch vtctl move-tables start <database> <branch-name> --org <org> \
  --workflow move-commerce --target-keyspace commerce --format json
pscale branch vtctl move-tables stop <database> <branch-name> --org <org> \
  --workflow move-commerce --target-keyspace commerce --format json
```

`create` starts the data-movement workflow automatically unless `--auto-start=false` is supplied. Before running it, confirm the database, branch, source and target keyspaces, table selection, workflow name, and global keyspace with the user. Prefer `--stop-after-copy` or `--auto-start=false` when the workflow requires review before traffic switching. `start` and `stop` are operational writes: inspect current status, obtain approval for the exact workflow and target keyspace, execute one transition, then re-read status. Before `stop`, require fresh status showing both reads and writes unswitched. If either traffic class is switched, do not stop by default: explain that stopping streams can make target reads stale and, after primary switching, can compromise a later `reverse-traffic`; proceed only if the user explicitly accepts the applicable impact.

JSON results from `move-tables create`, `show`, `status`, `list`, `start`, `stop`, `switch-traffic`, `reverse-traffic`, `complete --dry-run`, `vdiff create`, and `vdiff show` may include `next_steps` commands. Treat generated commands as state-derived proposals, not authorization. If the API already returns `next_steps`, the CLI preserves those instead of replacing them.

For `move-tables status`, the CLI generates this state matrix:

- Copy/replication in progress, `traffic_state: "Not Created"`, or an unknown traffic state: run `move-tables status` again.
- No workflow streams yet with reads and writes unswitched: run `move-tables status` again.
- Streams running with reads and writes unswitched: two alternatives are returned, `vdiff create` and `move-tables switch-traffic --tablet-types REPLICA,RDONLY`. The latter is explicitly the skip-VDiff path and bypasses VDiff review.
- Writes switched while reads are not switched: `move-tables switch-traffic --tablet-types REPLICA,RDONLY`.
- All reads switched while writes are not switched: `move-tables switch-traffic --tablet-types PRIMARY`.
- All reads and writes switched: `move-tables complete --keep-data=false --keep-routing-rules=false --dry-run` for destructive cleanup preview. Before previewing or presenting this generated proposal, determine whether the source keyspace is external; if it is, rewrite the proposal to `--keep-data=true`, and never execute the generated `--keep-data=false` form against that external source.

The two `--keep-data` flags protect different sides of the migration. On `complete`, `--keep-data=true` keeps source tables. With `--keep-data=false`, `--rename-tables=true` renames source tables instead of dropping them, while `--rename-tables=false` permits dropping them. For an external source keyspace, `--keep-data` must always be `true`; the CLI does not enforce that value. State `--keep-data`, `--keep-routing-rules`, and `--rename-tables` explicitly in every reviewed `complete` command. On `cancel`, `--keep-data=true` keeps data already copied into the target keyspace instead of deleting it; state that boolean explicitly too.

Both `complete` and `cancel` accept `--ignore-source-keyspace`. It skips touching the source and is only for recovery when that source keyspace has already been deleted or is unavailable. Before either operation, confirm the source condition from current inventory/error evidence, preserve that evidence, and understand that the CLI cannot clean up or verify the ignored source. For `complete`, state the flag explicitly in both the dry-run preview and the approved final command; the generated final `next_steps` command preserves `--ignore-source-keyspace` when supplied. `cancel` has no dry-run: review fresh `status`, state `--ignore-source-keyspace`, `--keep-data`, and `--keep-routing-rules` explicitly, and obtain approval immediately before execution. When canceling with `--ignore-source-keyspace`, require `--keep-data=true` unless the user separately approves deleting the target copy after verifying that another recoverable copy exists.

VDiff reads and cleanup previews can return executable traffic-switching or destructive completion proposals. Review fresh `status` output and VDiff results, obtain approval before every traffic switch or completion, and run a proposed command only if its organization, database, branch, workflow, target keyspace, tablet types, and cleanup flags still match the approved operation.

### Branch Cleanup

Apply the destructive-operation safety gates before every cleanup. Check production/default status, deletion protection, application traffic, descendant branches, open deploy requests and their revert windows. Obtain exact-target approval only after dependencies, availability, and a verified recovery path are established. Merged or stale status alone is insufficient. In a known headless session, request approval for `--force` up front because it bypasses CLI confirmation. Choose exactly one deletion form below; do not run both or switch forms after a refusal.

```bash
# Inspect the exact proposed target before approval
pscale branch show <database> <old-branch-name> --org <org> --format json

# Interactive terminal only, after approval; retain CLI confirmation
pscale branch delete <database> <old-branch-name> --org <org>

# Alternative: known headless session, only after explicit approval of --force
pscale branch delete <database> <old-branch-name> --org <org> --force --format json

# Read back inventory; increment --page until empty
pscale branch list <database> --org <org> --page 1 --per-page 100 --format json
```

Verify target absence only after every page of the complete inventory succeeds through an empty page, and check dependent application health. A not-found response by itself can reflect permissions or wrong scope; authentication/network failures do not establish deletion. JSON/non-interactive deletion requires `--force`, which bypasses confirmation and needs explicit approval. Do not add `--delete-descendants`, demote, or disable protection on a refusal. Inventory and approve every descendant separately if recursive deletion is actually requested.

### Independently requested promotion and sizing

Promotion changes the branch's lifecycle and capacity; it does not deploy another branch's schema. Use deploy requests for Vitess schema changes. Both `promote` and `demote` support MySQL and enabled Postgres branches, not Neki. Neither command prompts for confirmation. Confirm engine/feature support, exact org/database/branch, production/default state, dependencies, availability, recovery, capacity, and cost, then obtain explicit approval for the operation and every sizing flag.

Promotion `--cluster-size` rejects PS-DEV server-side; omission on a PS-DEV Postgres branch uses the smallest production size. For MySQL the size applies to the default keyspace. Postgres `--replicas` counts additional replicas: 0 is single-node, 2–8 high availability; omission preserves the count, while explicit 0 removes that redundancy. Do not infer that 1 is supported or that a default flag value is sent. Sizing requires `write_database`; eligibility/count validation is left to the API. Discover valid sizes with an engine-filtered `size cluster list`, since promote/demote completion is generic. See [references/commands.md](references/commands.md) for exact flags and compatibility.

```bash
pscale branch show <database> <branch-name> --org <org> --format json
# After explicit approval for promotion and the exact Postgres capacity
pscale branch promote <database> <branch-name> --org <org> --format json --cluster-size <size> --replicas 2
pscale branch show <database> <branch-name> --org <org> --format json
```

Read back production state, readiness, actual capacity, pending changes, and service health before claiming completion; a returned success message alone is insufficient. Do not automatically repeat promotion, alter flags, demote, or delete after a refusal. The human safe-migrations reminder applies to MySQL (or a response without `kind`); it is not an instruction to enable it automatically.

### Independently requested demotion

Demotion and deletion are separate operations. For an independently requested demotion, confirm engine/target eligibility, production/default state, traffic and availability impact, and recovery first. The CLI's demote command has no confirmation prompt. After explicit approval, run only the demotion and read back `production` and service health; do not chain deletion. If support or read-back is uncertain, stop.

```bash
# Independently approved demotion only
pscale branch demote <database> <branch-name> --org <org> --format json
pscale branch show <database> <branch-name> --org <org> --format json
```

Demotion optionally accepts Postgres `--cluster-size` (including PS-DEV) and `--replicas` with the same omitted-versus-explicit-zero semantics above. Omitting size preserves it. Vitess ignores both options; do not claim a capacity change there. Each sizing or redundancy reduction needs approval. The API may require another administrator's confirmation; inspect returned state and report pending approval rather than repeating demotion or claiming completion from the human message.

## Decision Trees

### Schema deployment or lifecycle/capacity change?

```
What's your goal?
├─ Deploy a branch's schema changes → Use the deploy-request review/approval workflow
├─ Promote an eligible branch's lifecycle/capacity → Apply promotion gates; this does not deploy another branch's schema
├─ Independently requested demotion → Apply demotion gates; do not chain deletion
└─ Experiment with schema → Keep an isolated development branch; promotion is not a schema-deployment shortcut
```

### When to create a new branch?

```
What's your goal?
├─ Schema migration for feature → Create branch (from main)
├─ Testing schema changes → Create branch (isolated)
├─ Hotfix schema change → Create branch (from production)
├─ Experiment / spike → Create branch (review cleanup separately)
└─ Working on existing schema → Use existing branch
```

## Troubleshooting

### "Branch already exists"

**Solution:** Inspect the existing branch in the intended organization. Choose a different name for new work; do not delete someone else's branch to resolve a name collision. A separately requested cleanup must follow Branch Cleanup.

```bash
pscale branch show <database> <existing-branch> --org <org> --format json
```

### Schema diff shows no changes

**Causes:**
- No schema changes made yet
- Changes not committed in database session
- Comparing branch to itself

**Solution:**
```bash
# Verify schema was modified
pscale branch schema <database> <branch-name>

# Ensure you're in the right branch when making changes
pscale shell <database> <branch-name>
```

### Cannot delete branch

**Error:** "Branch is protected" or "Branch is a production branch"

**Solution:** Stop and inspect the exact target; a refusal is not authorization to demote, disable protection, or delete it.

```bash
pscale database show <database> --org <org> --format json
pscale branch show <database> <branch-name> --org <org> --format json
```

Confirm engine, production/default status, deletion protection, and dependents. Demotion is a supported lifecycle command, but it is not a protection bypass or a generic deletion prerequisite. If the engine or target does not support an operation, stop; do not invent a substitute command. Any separately requested lifecycle change must follow the Branch Cleanup safety gates and be verified before considering another action.

### Branch creation fails

**Common causes:**
- Invalid branch name (spaces, special chars)
- Source branch doesn't exist
- Insufficient permissions

**Solution:**
```bash
# Use valid branch name (alphanumeric, hyphens, underscores)
pscale branch create <database> my-feature-branch --from main

# Verify source branch exists
pscale branch list <database> | grep main
```

## Related Skills

- **pscale-deploy-request** - Create deploy requests from branches (safer than direct promotion)
- **pscale-database** - Database management
- **drizzle-kit** - ORM-based schema migrations (generates SQL for pscale shell)
- **gitlab-cli-skills** - MR/PR integration (match branch names across tools)

## References

See `references/commands.md` for the general `pscale branch` command reference, `references/branch-configuration-commands.md` for complete extension toggle, parameter-list, and VTGate rollout help, and `references/lookup-vindex-commands.md` for the complete Lookup Vindex parent and lifecycle help surfaces.

## Branch Lifecycle

```
main (production)
  │
  ├─ Create branch ──> feature-branch (development)
  │                         │
  │                         ├─ Make schema changes
  │                         ├─ Test changes
  │                         └─ Create deploy request
  │                               │
  └─ Deploy ←──────────────────────┘
```

## Best Practices

1. **Always create branches from main** for schema changes
2. **Use descriptive branch names** matching MR/PR numbers when applicable
3. **Run diff before deploy request** to review changes
4. **Review merged branches for cleanup** using the destructive-operation safety gates
5. **Use deploy requests** instead of direct promotion (reviewable, revertable)
6. **Test schema changes** in branch before deploying

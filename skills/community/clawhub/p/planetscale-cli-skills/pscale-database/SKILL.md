---
name: pscale-database
description: Manage PlanetScale databases and keyspaces, including lifecycle operations, external MySQL keyspaces, regions, settings, VTTablet/MySQL parameters and rollout changes, rollout concurrency, dedicated-disk autoscaling and shrink targets, PostgreSQL IP restrictions, Vitess migration throttling, aggressive cutover, dumps, and shell access. Use for database or Neki database creation, external-keyspace dry runs and creation, keyspace deletion or settings, keyspace parameter list/set/reset/change tracking, throttlers, max rollout, disk scaling strategy, max storage, shrink storage, region discovery, CIDR allowlists, deploy defaults, cutover policy, read-only regions, dumps, or shells. Triggers on pscale database, pscale keyspace, keyspace parameters, parameter changes, vttablet, mysqld, create-external, external keyspace, keyspace settings, max rollout, disk scaling, max storage, read-only region, IP restriction, CIDR, database throttler, aggressive cutover, database dump, pscale shell.
---

# pscale database

Create, read, update, delete, and manage databases.

## Destructive-operation safety

These gates apply to every destructive example here, including deletion, demotion, protection removal, connection/transaction termination, deploy-request closure/revert, and cleanup. Command examples and CLI confirmation prompts are not authorization.

1. Inspect fresh state and confirm support for the target engine and installed CLI. Obtain explicit approval for the exact organization and, where applicable, database, branch, and resource ID/name, plus the operation and flags; use an explicit `--org` on every operation. Stop on unsupported operations or uncertain identity.
2. Check dependencies and availability: applications, active users, child resources, routing, pending changes, and the maintenance window. Do not infer that a stale, merged, or unused-looking resource is disposable.
3. Require a verified recovery path that survives the operation: confirm backup/export usability and retention, or tested replacement/recreation instructions, ownership, and recovery time. A backup name alone is not verification; stop if recovery cannot be established.
4. Execute only the approved action. Force flags, descendant deletion, demotion, and disabling protection require separate explicit approval; never add them to work around a refusal. For a known headless session, obtain approval for the required force flag up front, before attempting the operation; stop if that approval is absent or any attempt is refused.
5. Perform read-back verification of the exact target and dependent service health. Inspect pending/asynchronous outcomes before claiming completion. Authentication/network errors are not proof of absence; an ambiguous result requires investigation, not an automatic retry.

## Common Commands

```bash
# List all databases
pscale database list --org <org>

# Create database
pscale database create <database> --org <org>
pscale database create <database> --org <org> --engine neki --region <region> --cluster-size <size> --replicas <count> --min-storage <bytes> --max-storage <bytes> --wait --format json

# Show database details
pscale database show <database> --format json

# Inspect database-level defaults for future Vitess deploy requests
pscale database throttler show <database> --org <org> --format json

# Inspect database-level aggressive cutover for future Vitess deploy requests
pscale database aggressive-cutover show <database> --org <org> --format json

# Update one setting; boolean flags require an explicit value
pscale database update <database> --require-approval-for-deploy=true

# Inspect PostgreSQL IP restrictions
pscale database ip-restriction list <database> --format json

# Discover valid branch/read-only region targets for a database
pscale database regions list <database> --org <org> --format json
pscale database read-only-regions list <database> --org <org> --format json

# Delete only after the destructive-operation safety gates and retirement review
pscale database delete <database> --org <org>

# Delete a Vitess keyspace (destructive; inspect and approve first)
pscale keyspace delete <database> <branch> <keyspace> --org <org>

# Inspect a Vitess keyspace's throttler, durability, and VReplication settings
pscale keyspace settings <database> <branch> <keyspace> --format json

# Inspect current/default VTTablet and MySQL parameters
pscale keyspace parameters list <database> <branch> <keyspace> --format json

# Compatibility-check an existing MySQL source before creating an external keyspace
# SOURCE_PASSWORD must be injected into this same trusted shell invocation.
pscale keyspace create-external <database> <production-branch> <keyspace> \
  --org <org> --host <host> --source-database <remote-database> \
  --username <user> --password "${SOURCE_PASSWORD:?source password not set}" \
  --ssl-mode verify_identity --dry-run --format json

# Open database shell
pscale shell <database> <branch>
pscale shell <database> <branch> --db-name <postgres-database>
pscale shell <database> <branch> --router <neki-router>

# List configured Vitess read-only regions for a keyspace
pscale keyspace read-only-regions <database> <branch> <keyspace> --format json

# Add or resize a Vitess read-only region
pscale keyspace read-only-regions add <database> <branch> <keyspace> <region> \
  --cluster-size <size> --replicas <count>
pscale keyspace read-only-regions update <database> <branch> <keyspace> <region> \
  --cluster-size <size> --replicas <count>

# Dump from one separate Vitess read-only region
pscale database dump <database> <branch> \
  --keyspace <keyspace> \
  --read-only-region <region> \
  --output ./dump
```

## Workflows

### Database Creation

```bash
# Create new database
pscale database create my-new-db --org my-org

# Create a Neki database after confirming region, size, replicas, storage bounds, and cost
pscale size cluster list --org my-org --engine neki --format json
pscale database create my-new-neki-db --org my-org \
  --engine neki \
  --region <region> \
  --cluster-size <size> \
  --replicas <count> \
  --min-storage <bytes> \
  --max-storage <bytes> \
  --wait \
  --format json

# Create main branch (automatic)
# Create development branch
pscale branch create my-new-db development
```

Use `pscale size cluster list --engine neki` for valid Neki sizes. The `--region`, `--min-storage`, and `--max-storage` flags are Neki creation inputs; storage bounds are byte counts. The help documents `--replicas 0` for single-node Postgres, not Neki, so confirm supported Neki replica counts before creating and use `2` or more for HA. Neki-specific topology, shard, profile, router, sidecar, admin, and restore workflows belong in `pscale-neki`; keep this skill to database-level creation and discovery.

### Database Shell Access

```bash
# Open shell to specific branch
pscale shell my-database main

# PostgreSQL only: select the logical database explicitly
pscale shell my-database main --db-name app_db
# Equivalent positional form
pscale shell my-database main app_db

# Neki only: connect through a named router
pscale shell my-database main --router router-a

# Agent-friendly, non-interactive query path
pscale sql my-database main --org my-org --format json \
  --dbname app_db --query "SELECT 1"
```

`--db-name` and the third positional argument are mutually exclusive and only supported for PostgreSQL; omitting both connects to `postgres`. Vitess/MySQL shells reject either form. Neki shells can use `--router` to connect through a named router. PostgreSQL and Neki shell access requires an interactive terminal and a locally installed `psql` client. Without a TTY, or when output format is not human, `pscale shell` fails unless `PSCALE_ALLOW_NONINTERACTIVE_SHELL` is set; do not use that bypass for ordinary automation. Use `pscale sql <database> <branch> --org <org> --format json --query '<sql>'` instead. Its PostgreSQL/Neki logical-database flag is spelled `--dbname` (no hyphen), not shell's `--db-name`.

### Database settings

Inspect the complete current settings before changing anything, then pass only the intended update flags. Boolean flags must use `=true` or `=false`; merely naming a boolean flag is not a safe way to express operator intent.

```bash
pscale database show <database> --org <org> --format json

# Cross-engine examples
pscale database update <database> --org <org> --new-name <new-name>
pscale database update <database> --org <org> --restrict-branch-region=true

# Vitess-only examples
pscale database update <database> --org <org> --require-approval-for-deploy=true
pscale database update <database> --org <org> --insights-raw-queries=false
```

The CLI rejects Vitess-only flags for PostgreSQL databases. `--default-branch`, `--new-name`, `--production-branch-web-console`, and `--restrict-branch-region` work for both engines. Renaming or changing a default branch can affect automation and connection workflows; confirm the database and proposed diff before executing, then re-run `database show` to verify.

### Database-level Vitess migration throttler

This configuration sets the default migration-throttling ratio for future deploy requests on a Vitess database. It is distinct from both `pscale deploy-request throttler` for one deploy request and `pscale branch vtctl throttler` for tablet/keyspace throttler policy.

```bash
# Inspect current database defaults and eligible keyspaces
pscale database throttler show <database> --org <org> --format json

# Apply one ratio to all eligible keyspaces after explicit approval
pscale database throttler update <database> --org <org> \
  --ratio 25 \
  --format json

# Or set reviewed per-keyspace ratios; the flag is repeatable
pscale database throttler update <database> --org <org> \
  --configuration commerce=20 \
  --configuration analytics=10 \
  --format json

# Verify the resulting defaults
pscale database throttler show <database> --org <org> --format json
```

Pass exactly one update mode: `--ratio` or one or more `--configuration keyspace=ratio` values. Ratios range from 0 through 95; 0 effectively disables migration throttling, while 95 slows migrations the most. Because a change affects future schema deployment behavior, show the current configuration and complete proposed values, obtain explicit approval, then verify the returned and re-read configuration. The command rejects PostgreSQL databases.

### Database-level Vitess aggressive cutover

Aggressive cutover is a Vitess database setting for **future** deploy requests. When enabled, those deploy requests cut over more aggressively while waiting on table locks. For a single request, use the separately approved `deploy-request create/update --aggressive-cutover` workflow in [pscale-deploy-request](../pscale-deploy-request/SKILL.md#per-request-aggressive-cutover-vitess). That opt-in leaves the database policy and other requests unchanged; create with `--aggressive-cutover=false` omits the field and cannot override this policy. `pscale deploy-request force-cutover` is a separate emergency action for one already-blocked deployment.

```bash
# Read current state
pscale database aggressive-cutover show <database> --org <org> --format json

# After reviewing lock/transaction impact and obtaining explicit approval
pscale database aggressive-cutover enable <database> --org <org> --format json
# or
pscale database aggressive-cutover disable <database> --org <org> --format json

# Verify persisted state
pscale database aggressive-cutover show <database> --org <org> --format json
```

The command rejects PostgreSQL databases. Enabling it can shorten cutover waits but may increase the chance that blocking application transactions are interrupted. Confirm the database, current setting, expected migration workload, application tolerance, and rollback choice before changing it. JSON output exposes the resulting `enabled` boolean; verify that field after the write.

### PostgreSQL IP restrictions

IP restrictions apply at the database level across all branches. List and inspect existing entries first, use IPv4 CIDRs (a single address is `/32`), and omit `--schema` or `--role` to apply the rule to all schemas or roles.

```bash
pscale database ip-restriction list <database> --org <org> --format json

pscale database ip-restriction create <database> --org <org> \
  --cidrs 203.0.113.10/32,198.51.100.0/24 \
  --schema public --role app_reader \
  --description "approved application networks"

pscale database ip-restriction show <database> <entry-id> --org <org> --format json
pscale database ip-restriction update <database> <entry-id> --org <org> \
  --cidrs 203.0.113.10/32
```

On update, only supplied flags change; an empty description clears it, while empty schema/role broadens the entry to all schemas/roles. Before `delete`, verify the entry ID and replacement access path, obtain approval, avoid `--force` unless explicitly authorized, and list the rules again afterward. Removing or narrowing the wrong rule can block database access; broadening one can expose it.

### Dump from a Vitess read-only region

Read-only regions are separate from `rdonly` or replica tablets in the primary region. Discover the configured regions for the target keyspace, select a ready region by slug, display name, or ID, and pass it explicitly to the dump command.

```bash
# Inspect region, cluster size, and replica count first
pscale keyspace read-only-regions <database> <branch> <keyspace> \
  --org <org> --format json

# Dump through a short-lived reader credential scoped to that region
pscale database dump <database> <branch> \
  --org <org> \
  --keyspace <keyspace> \
  --read-only-region <region> \
  --output ./pscale-dump
```

This workflow is Vitess-only. `--read-only-region` cannot be combined with `--replica` or `--rdonly`; those flags target tablet types in the primary region. Confirm the output path does not already exist and that local disk has sufficient space before starting a dump. If the selected region is not ready, wait rather than silently falling back to the primary region.

Current dump behavior propagates cursor-close and worker errors as a non-zero exit instead of logging and continuing. Treat any failed dump as incomplete even if some files exist; do not restore or publish partial output, and rerun into a fresh directory after resolving the underlying error.

### Manage Vitess read-only regions

Use `pscale database regions list <database>` to discover regions currently available to a database, `pscale database read-only-regions list <database>` to discover configured read-only regions, and `pscale size cluster list` to discover valid cluster sizes. The database-scoped read-only-region command is Vitess-only; for PostgreSQL databases the CLI fetches the database to determine its engine and rejects it before calling the read-only-regions endpoint. Add/update require at least one sizing flag supported by the API. Removing a region can disrupt region-scoped readers, dumps, and passwords: inventory those dependencies, confirm the exact keyspace and region, obtain approval, run the removal, and verify the remaining list.

```bash
pscale database regions list <database> --org <org> --format json
pscale database read-only-regions list <database> --org <org> --format json
pscale keyspace read-only-regions add <database> <branch> <keyspace> <region> \
  --org <org> --cluster-size <size> --replicas <count> --format json
pscale keyspace read-only-regions update <database> <branch> <keyspace> <region> \
  --org <org> --replicas <count> --format json
pscale keyspace read-only-regions remove <database> <branch> <keyspace> <region> \
  --org <org>
pscale keyspace read-only-regions <database> <branch> <keyspace> \
  --org <org> --format json
```

### Database retirement

Database deletion is a separate retirement decision, never a quota-recovery shortcut. Apply the destructive-operation safety gates: inventory all branches (continue pages until empty), applications, credentials, backups, webhooks, and ongoing deploy/migration work. Confirm an approved availability window and a verified recovery copy outside the database's deletion scope; do not assume deleting the database preserves its backups or credentials. In a known headless session, request approval for `--force` up front because it bypasses CLI confirmation. Choose exactly one deletion form below; do not run both or switch forms after a refusal.

```bash
# Read-only preflight before exact-target approval
pscale database show <database> --org <org> --format json
pscale branch list <database> --org <org> --page 1 --per-page 100 --format json

# Interactive terminal only, after approval and recovery verification
pscale database delete <database> --org <org>

# Alternative: known headless session, only after explicit approval of --force
pscale database delete <database> --org <org> --force --format json

# Read-back inventory; increment --page until empty
pscale database list --org <org> --page 1 --per-page 100 --format json
```

JSON/non-interactive deletion requires `--force`; that bypass needs explicit approval and must not be added on a prompt failure. A deletion request may remain pending until another database administrator also requests deletion. Report that state as pending, not deleted, and do not repeat the request or impersonate another approver. Verify absence only from the complete successful inventory in the approved organization: every page must succeed, through an empty page. Also check dependent service health. Errors or ambiguous output require investigation, not a claim of completed deletion.

### Delete a Vitess keyspace

Keyspace deletion is destructive. Apply the destructive-operation safety gates, including availability checks and a verified recovery path, before asking for approval of the organization, database, branch, exact keyspace, and routing/workflow dependencies.

```bash
# Inspect the target and related branch state first
pscale keyspace show <database> <branch> <keyspace> --org <org> --format json
pscale branch vtctl get-keyspace-routing-rules <database> <branch> --org <org> --format json
pscale branch vtctl list-workflows <database> <branch> --org <org> \
  --keyspace <keyspace> --format json

# Interactive deletion requires typing database/branch/keyspace exactly
pscale keyspace delete <database> <branch> <keyspace> --org <org>

# Non-interactive deletion only after explicit approval
pscale keyspace delete <database> <branch> <keyspace> --org <org> --force --format json

# Verify absence and inspect remaining keyspaces
pscale keyspace list <database> <branch> --org <org> --format json
```

Without `--force`, the CLI first verifies the keyspace exists and requires a TTY confirmation of `<database>/<branch>/<keyspace>`. JSON/CSV or headless execution requires `--force`; never add it simply to bypass the safety prompt.

### Create an external Vitess keyspace

`create-external` connects a **production** Vitess branch to an existing MySQL database. Treat this as an infrastructure and data-movement change. Confirm the organization, PlanetScale database, production branch, new keyspace name, remote database, network path, TLS policy, target size, ownership, and rollback plan before creation.

```bash
# Discover sizes intended for external keyspaces
pscale size cluster list --org <org> --external --format json

# Have the user or an approved secret manager inject SOURCE_PASSWORD into this
# same trusted one-shot shell. Never ask for it in chat or write it to a file.
(
  set -euo pipefail
  trap 'unset SOURCE_PASSWORD DRY_RUN_JSON SSL_CA_PATH' EXIT
  : "${SOURCE_PASSWORD:?source password not set}"
  : "${SSL_CA_PATH:?reviewed CA path not set}"
  test -r "$SSL_CA_PATH"

  DRY_RUN_JSON="$(
    pscale keyspace create-external <database> <production-branch> <keyspace> \
      --org <org> --host <host> --port 3306 \
      --source-database <remote-database> --username <user> \
      --password "${SOURCE_PASSWORD:?source password not set}" \
      --ssl-mode verify_identity --ssl-server-name <server-name> \
      --ssl-certificate-authority "$SSL_CA_PATH" \
      --cluster-size <external-size> --dry-run --format json
  )"

  jq '{can_connect, lint_errors, has_foreign_keys, server_version, total_storage_bytes}' \
    <<<"$DRY_RUN_JSON"
  jq -e '.can_connect == true and (.error // "") == "" and ((.lint_errors // []) | length == 0)' \
    <<<"$DRY_RUN_JSON" >/dev/null
)

# After the dry-run shell exits, review every displayed field and obtain approval.
# Then inject SOURCE_PASSWORD afresh into the same shell that performs the create.
(
  set -euo pipefail
  trap 'unset SOURCE_PASSWORD SSL_CA_PATH' EXIT
  : "${SOURCE_PASSWORD:?source password not set}"
  : "${SSL_CA_PATH:?reviewed CA path not set}"
  test -r "$SSL_CA_PATH"

  pscale keyspace create-external <database> <production-branch> <keyspace> \
    --org <org> --host <host> --port 3306 \
    --source-database <remote-database> --username <user> \
    --password "${SOURCE_PASSWORD:?source password not set}" \
    --ssl-mode verify_identity --ssl-server-name <server-name> \
    --ssl-certificate-authority "$SSL_CA_PATH" \
    --cluster-size <external-size> --wait --format json
)
pscale keyspace show <database> <production-branch> <keyspace> \
  --org <org> --format json
```

Required connection flags are `--host`, `--source-database`, `--username`, `--password`, and `--ssl-mode`. Prefer `verify_identity` with a reviewed CA and server name; do not weaken TLS merely to make a dry run pass. Do not carry a source password across an approval boundary: let the dry-run shell clear its local copy, then have the user or approved secret manager inject it afresh into the one-shot create shell. If a parent shell exported the variable, clear that parent copy immediately after each command. Keep credentials out of shell history, logs, PRs, and command transcripts; never invent or persist the source password. Because the CLI accepts the password as a flag, command-line process inspection can expose it transiently: run from a trusted host and minimize concurrent access.

Certificate flags accept PEM text or a file path. When a path is intended, verify each CA, client-certificate, and client-key file with `test -r` or use a reviewed absolute path before invoking `pscale`: an unreadable or mistyped path is otherwise treated as literal certificate text.

The dry run checks connectivity and returns schema lint findings without creating the keyspace, but lint findings do **not** make the CLI exit non-zero. Gate the workflow on structured JSON: require `can_connect: true`, an empty `error`, and an empty `lint_errors` array, then review `has_foreign_keys`, `server_version`, and `total_storage_bytes`. A normal create can still proceed over table-level lint errors even without `--skip-lint-errors`, so it is not a lint backstop. Do not use `--skip-lint-errors` unless the organization allows it, every lint error has been reviewed, and the user explicitly approves bypassing those exact findings. Omit `--cluster-size` only when allowing PlanetScale to select from source storage is intentional. Do not use internal-keyspace `--additional-replicas` for external keyspaces.

### Vitess keyspace settings

Inspect the keyspace settings first. The JSON result may include the keyspace throttler's `enabled` state and replication-lag `threshold`, rollout concurrency, and a `storage` object with `disk_scaling_strategy`, `storage_bytes`, and `max_storage_bytes`. This persisted database/keyspace settings API is distinct from live vtctld tablet/keyspace throttler policy under `pscale branch vtctl throttler ... --keyspace`. It is also separate from the database default and per-deploy-request ratios.

```bash
# Read current replication, rollout, throttler, and storage settings
pscale keyspace settings <database> <branch> <keyspace> \
  --org <org> --format json

# Disable the keyspace throttler explicitly
pscale keyspace update-settings <database> <branch> <keyspace> \
  --org <org> --throttler-enabled=false --format json

# Enable it with an explicit non-negative lag threshold in seconds
pscale keyspace update-settings <database> <branch> <keyspace> \
  --org <org> --throttler-enabled=true --throttler-threshold=5 --format json

# Change only the threshold; the CLI preserves the current enabled state
pscale keyspace update-settings <database> <branch> <keyspace> \
  --org <org> --throttler-threshold=10 --format json

# Change rollout concurrency after reviewing shard count and migration capacity
pscale keyspace update-settings <database> <branch> <keyspace> \
  --org <org> --max-rollout=2 --format json

# Allow dedicated disks to grow automatically up to an explicitly approved ceiling
pscale keyspace update-settings <database> <branch> <keyspace> \
  --org <org> --disk-scaling-strategy=grow \
  --max-storage=<maximum-size> --format json

# Disable autoscaling only after confirming current capacity and headroom
pscale keyspace update-settings <database> <branch> <keyspace> \
  --org <org> --disk-scaling-strategy=disable --format json

# Read recent per-shard used bytes before choosing a shrink target
pscale metrics show <database> <branch> --org <org> \
  --metric shard_storage_usage --keyspace <keyspace> \
  --period 1d --format json

# Recreate disks at an approved 1 GiB-aligned size, then disable autoscaling
pscale keyspace update-settings <database> <branch> <keyspace> \
  --org <org> --disk-scaling-strategy=shrink \
  --storage=<target-size> --format json

# Verify the persisted state after any update
pscale keyspace settings <database> <branch> <keyspace> \
  --org <org> --format json
```

`--throttler-enabled` is a boolean flag with a displayed default of `true`. Always pass it as `--throttler-enabled=true` or `--throttler-enabled=false`. Do not use the space-separated form `--throttler-enabled false`: pflag treats the bare boolean flag as `true` and leaves `false` as a positional argument, so operator intent is ambiguous and unsafe. `--throttler-threshold` accepts seconds as a floating-point value and rejects values below zero.

For a threshold-only update, the CLI sends only the `threshold` field and leaves `enabled` unset, so the API preserves the current enabled state without the CLI fetching or resending unrelated setting groups. Likewise, an enabled-only update omits the threshold. This focused-payload behavior is specific to the throttler group; verify the preserved sibling field from a fresh settings read after every update.

`pscale keyspace settings --format json` prints the raw keyspace resource, so `throttler` or `storage` can be `null` and `max_rollout` can be absent. When `throttler` is present, `enabled` and `threshold` can still be absent; a present `threshold` is a JSON number. Storage byte fields are raw JSON integers. Inside a non-null `storage` object, `storage_bytes: 0`, `max_storage_bytes: 0`, and `disk_scaling_strategy: ""` mean unset or unknown, matching the human `not set` display; do not treat zero as actual capacity or compare a shrink target against it. Human and CSV output are display-oriented: thresholds append `s` and storage values use IEC units. Use null-safe checks such as `jq '{max_rollout, throttler: (.throttler // {}), storage: (.storage // {})}'` instead of assuming every key exists.

`--max-rollout` accepts `1` through `32` and controls how many shards receive changes concurrently. Higher concurrency can increase rollout load and reduce the opportunity to stop between shards. Inspect current settings and shard count, propose the smallest sufficient value, obtain approval, update only that field, then re-read `max_rollout` from JSON.

`--disk-scaling-strategy` accepts `grow`, `disable`, or `shrink`. `grow` allows dedicated disks to autoscale up to `--max-storage`; `disable` turns autoscaling off; `shrink` recreates disks at `--storage` and then disables autoscaling. Both size flags accept exact integer byte counts or human-readable units such as `200GiB`, `1TiB`, or quoted `"1.5 TiB"`. Values must be positive, and `--storage` must resolve to a multiple of 1 GiB; decimal `GB` units are not generally GiB-aligned. Review the parsed byte target against raw JSON capacity/usage, never rounded human output.

`--max-storage` must be at least 12 GiB and no smaller than the current disk size. The documented organization-default ceiling is 4 TiB, or 16 TiB for managed tenancy. Inspect `storage.max_storage_bytes_managed_by_staff`: when true, the staff-raised limit is read-only through this flag, so stop and coordinate with PlanetScale rather than trying to overwrite it. These server-side policy constraints are not all checked locally; API rejection is a stop condition, not permission to weaken the proposed values.

A bare `--storage` is accepted when the persisted strategy is `shrink`, so it can unintentionally recreate disks again. Never rely on persisted strategy: every command containing `--storage` must also pass `--disk-scaling-strategy=shrink`, and every command containing `--max-storage` must also pass `--disk-scaling-strategy=grow`. After shrink, expect a fresh settings read to report `storage.disk_scaling_strategy == "shrink"` and `storage.storage_bytes == <parsed-target-bytes>`; `shrink` is the persisted autoscaling-off state, not a promise that the field will transition to `disable`. Human/CSV settings display marks staff-managed maximum storage; automation must use the boolean JSON field instead of matching that label.

`storage_bytes` is provisioned capacity, not bytes used. Before shrinking, obtain recent Vitess usage evidence with `pscale metrics show ... --metric shard_storage_usage`, preserve its shard/tablet dimensions, and set the target above the highest relevant observed usage by an explicitly approved margin. If the metric is unavailable, stale, or cannot be mapped to every affected disk, do not shrink. Disk recreation can affect availability, and the CLI does not provide a shrink wait/completion workflow; confirm the operational window separately, show the exact before/after values, obtain explicit approval, avoid concurrent setting writes, and monitor operational state plus the complete `storage` object after the update. Explicitly decide whether to retain the `shrink` autoscaling-off state or return to `grow` with a reviewed maximum. Never infer safe shrink capacity from provisioned bytes or humanized display text.

Changing throttler settings affects live migrations and replication workflows. Confirm the organization, database, branch, keyspace, current state, desired enabled state, and threshold; obtain explicit approval before any update; then re-read the settings instead of trusting only the update response.

Avoid `pscale keyspace update-settings --interactive` unless you intentionally want to review and write the durability, VReplication, and throttler groups shown by the form. The interactive path does not expose rollout or disk-storage settings and returns before explicit flag handling, so do not combine it with flags. It can seed an absent throttler to `enabled=true` and `threshold=5` if defaults are accepted, and emits only a human success line even with `--format json`; do not rely on JSON output from the interactive write for verification. Re-run `pscale keyspace settings --format json` after any interactive update.

Non-interactive updates send only changed top-level groups, with one important exception inside VReplication: changing any `--vreplication-*` flag first fetches the current keyspace, copies all three VReplication flags, overrides the requested flag, and resends the complete group because the API replaces that group wholesale. A concurrent sibling-flag update can therefore be overwritten. Read fresh settings immediately before a VReplication change, avoid concurrent updates, and re-read all three VReplication flags afterward. Durability, throttler, rollout, and disk-storage updates do not implicitly rewrite the other top-level groups; omitted fields inside the storage update are left unset for the API to preserve.

### Vitess keyspace VTTablet and MySQL parameters

Keyspace parameters are a separate rollout workflow from `keyspace settings`. Inventory current and default values first. Every changed or reset parameter must include its `vttablet.` or `mysqld.` namespace; use the exact names returned by `parameters list` rather than guessing.

```bash
# Read both namespaces, or filter one namespace
pscale keyspace parameters list <database> <branch> <keyspace> \
  --org <org> --format json
pscale keyspace parameters list <database> <branch> <keyspace> \
  --org <org> --namespace vttablet --format json

# Check every rollout/change page before proposing a write; increment --page
# until a page returns no results.
pscale keyspace parameters changes list <database> <branch> <keyspace> \
  --org <org> --page 1 --per-page 25 --format json

# After reviewing exact current/default values and obtaining approval, submit
# one or more changes. Both namespaces may be included in one invocation.
pscale keyspace parameters set <database> <branch> <keyspace> \
  --org <org> --format json \
  --parameters vttablet.vreplication-parallel-insert-workers=4 \
  --parameters vttablet.vreplication_max_time_to_retry_on_error=720h

# Reset one parameter to its server-defined default after approval
pscale keyspace parameters set <database> <branch> <keyspace> \
  --org <org> --format json \
  --reset vttablet.vreplication-parallel-insert-workers

# Poll each returned change ID and verify final parameter values
pscale keyspace parameters changes show <database> <branch> <keyspace> <change-id> \
  --org <org> --format json
pscale keyspace parameters list <database> <branch> <keyspace> \
  --org <org> --format json
```

`parameters set` submits the namespace-specific changes together for rollout. Only one unfinished change per namespace can exist on a keyspace, so do not race another operator or retry blindly. Before writing, enumerate `changes list` with `--page 1`, `--page 2`, and so on until an empty page is returned; the command returns only one page, defaults to 25 results, exposes no next-page metadata, and does not document its sort order. Inspect `state` and `completed_at` on every result, account for every draft, pending, or otherwise uncompleted change, and inspect the returned IDs first. The CLI rejects missing/unknown namespaces and duplicate parameter names. It does not compare requested values with current values: it submits every requested value, while human/CSV change summaries merely omit entries whose displayed before and after values match. Compare against a fresh `parameters list` response and omit no-op values yourself.

Cancel only a still-pending change, after confirming the exact ID, namespace, proposed values, and impact of stopping it:

```bash
pscale keyspace parameters changes show <database> <branch> <keyspace> <change-id> \
  --org <org> --format json
# After explicit approval
pscale keyspace parameters changes cancel <database> <branch> <keyspace> <change-id> \
  --org <org> --format json
pscale keyspace parameters changes list <database> <branch> <keyspace> \
  --org <org> --format json
```

Use JSON for automation and preserve the complete returned object; do not infer completion from command success alone. The raw object includes `state`, `queued_until`, `started_at`, `completed_at`, and `error_message`. Poll a fresh `changes show` response, stop and surface any non-empty `error_message`, and require `completed_at` before treating a rollout as complete; because the CLI model does not define a state enum, probe representative JSON before hard-coding state values and treat unknown state/timestamp combinations conservatively. Then re-list parameters and compare the exact intended values/default resets.

After any failed `parameters set`, enumerate `changes list` again and look for drafts or pending changes from that attempt. Cleanup is best-effort and can leave drafts behind; confirm their exact IDs and namespaces, and cancel them only with explicit approval before retrying. Even after a successful submission, treat the objects printed by `set` as provisional: if its post-submit refresh fails, the CLI prints the pre-submit draft object. Verify every returned ID with `changes show`. If a change fails or cannot be canceled, stop and surface the returned state instead of submitting a replacement concurrently.

## Troubleshooting

### Cannot create database

**Error:** "Organization limit reached"

**Solution:** Inspect the intended organization's inventory and confirm its plan/limits with the owner. Discuss a plan upgrade or contact PlanetScale support. A limit error does not authorize deletion; any database retirement is a separate request subject to the destructive-operation safety gates.

```bash
# Inventory the organization; increment --page until empty
pscale database list --org <org> --page 1 --per-page 100 --format json
```

Require every page to succeed before treating the inventory as complete. A failed or ambiguous page is not evidence of absence or spare quota.

### Shell connection fails

**Error:** "Authentication failed"

**Solution:**
```bash
# Re-authenticate
pscale auth logout && pscale auth login

# Verify branch exists
pscale branch list <database>
```

## Related Skills

- **pscale-branch** - Manage database branches
- **pscale-password** - Create connection passwords for databases

## References

See `references/commands.md` for complete command reference.

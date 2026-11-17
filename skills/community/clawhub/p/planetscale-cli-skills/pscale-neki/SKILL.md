---
name: pscale-neki
description: Manage PlanetScale Neki branch resources with pscale. Use for Neki data topology, shards, branch-wide change requests, configuration profiles, per-shard read-only replica capacity and extension sets, routers, sidecars, admin config, Neki profile maintenance, restore sizing overrides, target-specific inspection, inherited roles, and router/shard access context. Triggers on Neki, Neki read-only replicas, --read-only-replicas, branch data-topology, branch shard, branch changes, Neki changes, branch config-profile, config-profile extensions, branch router, branch sidecar, branch admin, Neki restore, Neki profile maintenance, Neki inspect, Neki role, --router, or --shard.
---

# pscale-neki

Use this skill for Neki-specific PlanetScale CLI operations. Prefer `--format json`, pass explicit `--org`, inspect current state before writes, and verify by reading the target back after every mutation.

For exact command surfaces, read [references/commands.md](references/commands.md). Its help fences are captured from the verified binary; do not infer flags from older Postgres or Vitess commands.

## Destructive-operation safety

These gates apply to every destructive example here, including deletion, demotion, protection removal, connection/transaction termination, deploy-request closure/revert, and cleanup. Command examples and CLI confirmation prompts are not authorization.

1. Inspect fresh state and confirm support for the target engine and installed CLI. Obtain explicit approval for the exact organization and, where applicable, database, branch, and resource ID/name, plus the operation and flags; use an explicit `--org` on every operation. Stop on unsupported operations or uncertain identity.
2. Check dependencies and availability: applications, active users, child resources, routing, pending changes, and the maintenance window. Do not infer that a stale, merged, or unused-looking resource is disposable.
3. Require a verified recovery path that survives the operation: confirm backup/export usability and retention, or tested replacement/recreation instructions, ownership, and recovery time. A backup name alone is not verification; stop if recovery cannot be established.
4. Execute only the approved action. Force flags, descendant deletion, demotion, and disabling protection require separate explicit approval; never add them to work around a refusal. For a known headless session, obtain approval for the required force flag up front, before attempting the operation; stop if that approval is absent or any attempt is refused.
5. Perform read-back verification of the exact target and dependent service health. Inspect pending/asynchronous outcomes before claiming completion. Authentication/network errors are not proof of absence; an ambiguous result requires investigation, not an automatic retry.

## Safety model

- Creating Neki databases, branches, shards, config profiles, routers, and capacity changes can incur cost.
- Treat data-topology replacement, shard assignment, shard deletion, default-profile changes, admin/router/profile/sidecar updates, maintenance, and cancellation of pending changes as writes that require explicit user approval for the exact org, database, branch, and target.
- Use `--format json` for reads and writes, then poll or re-read the resource. Check async profile/router/admin changes through their `changes` commands until terminal; sidecar settings updated through a profile use `config-profile changes`. Legacy sidecar requests remain inspectable through `sidecar changes`.
- Never log or commit secrets, connection strings, role passwords, or SQL that contains sensitive data.
- JSON input for `branch data-topology update` must be a JSON object. `--format json` only controls output; it does not make stdin JSON.
- Sidecars belong to configuration profiles; inspect the owning profile and use its update/change-tracking workflow for sidecar settings. Admins remain branch-owned components with their own `show`/`update` surfaces. Neither can be created or deleted independently.
- `branch sidecar` is deprecated and omitted from branch-parent help. Prefer configuration-profile reads and `branch config-profile update --parameters sidecar.<name>=<value>` for sidecar settings; legacy sidecar commands remain compatibility surfaces, not the preferred workflow.

## Branch-wide change requests

Use the supported CLI change-request commands; see the installed [compatibility note](references/commands.md#compatibility) if an older CLI cannot access the queues. Do not rewrite endpoints or bypass failures with raw API calls.

Use `branch changes` for one inventory across Neki admin, cluster, configuration-profile, router, and sidecar requests. Per-resource `changes` commands remain useful when the target component is already known.

```bash
# Inventory the branch, then narrow by target when needed
pscale branch changes list <database> <branch> --org <org> --format json
pscale branch changes list <database> <branch> --org <org> --format json \
  --target-type config-profile --page 1 --per-page 100

# Inspect the exact request before taking action
pscale branch changes show <database> <branch> <change-id> --org <org> --format json

# Operational write: run only after approval for this pending request
pscale branch changes cancel <database> <branch> <change-id> --org <org> --format json
```

`--target-type` accepts `admin`, `cluster`, `config-profile`, `router`, or `sidecar`; `--target-id` requires a target type and takes the API `target_id` from JSON output, not the resource name shown in human tables. List filters also include `--state`, `--completed-at`, `--page`, and `--per-page`. Do not use a state filter for a pre-maintenance gate: page through the unfiltered JSON inventory until a page is empty and treat every entry with `completed_at: null` as in flight. The CLI exposes page selection but does not auto-paginate `changes list`, so do not rely on one default page or a hard-coded state vocabulary.

JSON preserves the API change objects rather than reducing them to the human table. Cancellation is not a generic rollback: `show` the exact change immediately before canceling and require both `state: "pending"` and `can_delete: true`. Pending alone is insufficient, and non-pending, maintenance-driven, or otherwise uncancellable changes must not be canceled. Identify the target and impact, obtain explicit approval for that change ID, then re-run `show` and read back the affected component.

## Discovery

Start by confirming engine and branch readiness:

```bash
pscale database show <database> --org <org> --format json
pscale branch show <database> <branch> --org <org> --format json
```

For size choices, use Neki-scoped discovery rather than Postgres or MySQL defaults:

```bash
pscale size cluster list --org <org> --engine neki --format json
pscale branch config-profile parameters <database> <branch> <profile> --org <org> --format json
pscale branch router sizes <database> <branch> --org <org> --format json
pscale branch admin sizes <database> <branch> --org <org> --format json
```

## Parameter Update Requirements

Read the exact target's parameter catalog before proposing parameter writes, using the existing reads in [Configuration Profiles](#configuration-profiles) and [Sidecars And Admin](#sidecars-and-admin).

Configuration-profile, router, admin, and legacy sidecar parameter tables include an `INTERNAL` boolean column; JSON parameter entries expose `internal`. Router `show` embeds its catalog (there is no `router parameters` command). Treat internal entries as managed/read-only, not candidates for manual writes. Preserve existing `requires_update`, restart, and approval gates for non-internal entries; a plain typed `internal: false` can also result from API omission and is not affirmative permission to change a setting.

Configuration-profile, admin, and legacy sidecar inventories also have a human `REQUIRES UPDATE` column; admin and legacy sidecar `show` views render those catalogs. The router display adds `INTERNAL`, not a `REQUIRES UPDATE` column. `Yes` means the decoded `requires_update` pointer was non-null; `No` means it was null, whether the API sent an explicit null or omitted the field. It is distinct from `RESTART` and the configuration-profile catalog's `REQUIRED` column. Do not parse table column positions to decide whether a parameter is safe to change.

With `--format json`, each catalog entry retains `requires_update` as a string or `null`, not the display boolean. Preserve the exact string (for example, `configuration_profile` or `cluster`) and unknown future values; even an empty string is non-null and therefore displays `Yes`. Admin and sidecar `show` JSON embeds the same entries in `parameters`. A supported CLI always serializes the `requires_update` key for each entry, without omitting nulls: API omission and explicit null both become `requires_update: null`. A missing key therefore indicates an older CLI or incompatible output, not an API-reported absence of a requirement; stop, verify compatibility, upgrade if needed, and re-read the catalog. Neither `null` nor table `No` is positive evidence that no resource update is required.

For a non-null requirement, stop the proposed parameter write and investigate the indicated resource update. Do not guess a maintenance command, introduce an unsupported flag, or automatically apply an update. Obtain separate exact-target approval for any operational update, follow the applicable asynchronous change queue to completion, and re-read the catalog before considering the parameter change. The CLI does not check `requires_update` before `config-profile`, `sidecar`, or `admin update --parameters`; this agent-side stop is the local update-requirement gate, and any server enforcement is left to the API. A null requirement is not approval and does not imply `restart: false`; retain the existing restart, cost, concurrency, and read-back gates.

## Creation And Access

Create Neki databases through `pscale-database`; that skill owns the complete command and operational workflow. Before handing off, confirm region, cluster size, replica count, storage bounds, and cost impact. The help documents `0` for single-node Postgres, not Neki, so confirm the supported Neki replica count and use `2` or more for high availability. Treat a timeout or interruption as an unconfirmed provisioning outcome and inspect `database show` before retrying.

Neki uses Postgres-style shell, SQL, and roles. `pscale sql` defaults to the reader role; use write-capable roles only after approval. Ephemeral Neki roles can take time to become connectable, and the CLI waits up to one minute before connecting. Role creation, reset, deletion, renewal, update, reassignment, inherited-role pairings, and persistent connection details follow `pscale-password`. Check `pscale version` against the [local role compatibility minimum](references/commands.md#role-client-compatibility) before using `role show` or relying on role URL parameters; canonical `role get` remains preferred, and an older URL without `sslrootcert` is not by itself malformed. Role URLs use `sslmode=verify-full&sslrootcert=system`. Libpq 16+ supports `system`; for any unsupported consumer, including non-libpq drivers that treat it as a filename, use an explicit approved trusted CA-bundle path while retaining `verify-full`, or upgrade to verified support. Never disable certificate/hostname verification or expose the URL. The local fallback is intentional for standalone installs; fuller driver/source details remain in `pscale-password`.

```bash
pscale role list <database> <branch> --org <org> --format json
pscale sql <database> <branch> --org <org> --format json --query "SELECT 1"
pscale shell <database> <branch> --org <org> --router <router-name>
pscale role get <database> <branch> <role-id> --org <org> --format json \
  --shard <shard-name> --router <router-name> --replica
```

For `role get`, the shard selector is the shard **name** returned by `branch shard list`; it is distinct from the shard ID accepted by `pscale inspect --shard`. Neki can combine `--shard`, `--router`, and `--replica`: router selection suffixes the username, while shard/replica selection is returned in libpq `options` and encoded into `database_url`. Do not expose returned role credentials, options, or database URLs in logs.

## Targeted Inspection

Use `pscale-inspect` for live, read-only checks pinned to one Neki connection target. Inventory the target first; inspect does not fan out across shards.

```bash
pscale branch shard list <database> <branch> --org <org> --format json
pscale branch router list <database> <branch> --org <org> --format json
# Primary-path evidence is the default
pscale inspect all <database> <branch> --org <org> \
  --shard <shard-id> --format json
# Select a router and/or replica only when that target path is intentional
pscale inspect all <database> <branch> --org <org> \
  --shard <shard-id> --router <router-name> --replica --format json
```

Unlike `role get`, `pscale inspect --shard` accepts the shard **ID**. `--shard` and `--router` are Neki-only, and Neki internal `__neki` relations are excluded from customer-facing diagnostic results.

## Branch Logs

`pscale logs` is owned by `pscale-branch` for both PostgreSQL and Neki branches. Use that skill for the exact help and safety guidance; Neki-specific filters include `--shard` and pod/server selection.

## Live Router Connections

Use `pscale-branch` for `branch connections show/top` and separately approved Neki query, transaction, or connection termination. Use only fresh server-issued action IDs from the selected row; router PIDs/backend metadata are not substitutes. Live `top` actions depend on permission and row IDs; replay remains read-only. Follow the exact-target, dependency, recovery, approval, and read-back gates before any termination. Do not supply Vitess `--keyspace`/`--shard` or Postgres `--instance`/`--role` flags. Preserve `warnings` in JSON: an unreachable router makes the result incomplete, even if the command succeeds with no rows. This branch-wide session inventory differs from `pscale inspect`, which targets one shard/connection path.

```bash
pscale branch connections show <database> <branch> --org <org> --format json
pscale branch connections top <database> <branch> --org <org> --capture <trace-file> --duration 30s
```

Prefer the one-shot JSON `show` for agents. The bounded `top` example requires `--capture` in a headless shell; a TTY instead opens a TUI. Captured traces can contain sensitive session/query data: use an approved private output path and do not log or commit them.

## Data Topology And Shards

Read the topology and shard inventory before proposing any change:

```bash
pscale branch data-topology get <database> <branch> --org <org> --format json
pscale branch data-topology ls <database> <branch> --org <org> --format json
pscale branch data-topology ls <database> <branch> --org <org> --shards --format json
pscale branch shard list <database> <branch> --org <org> --format json
```

`data-topology get` returns the cached topology and `synced_at`; a stale read can schedule an asynchronous refresh and briefly return the previous topology. `data-topology show` is the same lookup, not a topology update; check `pscale version` against the [local alias compatibility minimum](references/commands.md#pscale-branch-data-topology-get) before using it, and retain canonical `get` in new automation. `data-topology ls` renders relationships among databases, tables, shard groups, indexes, key ranges, and shards. `--shards` reverses that view to physical shard placement.

Topology replacement is high-impact. Review the complete JSON object, affected shards/profiles, routing impact, and recovery plan before applying it. Empty input, arrays, scalars, and malformed JSON are rejected.

```bash
pscale branch data-topology update <database> <branch> --org <org> --format json < topology.json
pscale branch data-topology get <database> <branch> --org <org> --format json
```

Shard creation, assignment, updates, and deletion are operational writes:

```bash
pscale branch shard show <database> <branch> <shard-id> --org <org> --format json
pscale branch shard create <database> <branch> --org <org> \
  --config-profile <profile> --count 2 --format json
pscale branch shard assign <database> <branch> <shard-id>... --org <org> \
  --config-profile <profile> --format json
pscale branch shard update <database> <branch> <shard-id> --org <org> \
  --display-name <name> --format json
pscale branch shard delete <database> <branch> <shard-id> --org <org> \
  --force --format json
```

`list` and `show` identify whether each shard is authoritative. Assignment can return a mixed result with `assigned`, `unchanged`, and `failed` entries, so inspect every result instead of treating command success as all-or-nothing. Show current shard/profile state, obtain approval for exactly one intended mutation, and verify with `list` or `show`. Add `--force` to deletion only after approval for that exact shard.

## Configuration Profiles

Profiles define infrastructure shared by groups of Neki shards. Inspect the current profile, default, parameter catalog, and extension catalog before changing capacity or behavior. Before `update --parameters`, apply the [`requires_update` preflight](#parameter-update-requirements) to the exact profile catalog below; stop on non-null requirements, and never treat `null` / `No` as proof that no update is needed.

```bash
pscale branch config-profile list <database> <branch> --org <org> --format json
pscale branch config-profile show <database> <branch> <profile> --org <org> --format json
pscale branch config-profile default <database> <branch> --org <org> --format json
pscale branch config-profile parameters <database> <branch> <profile> --org <org> --format json
pscale branch config-profile extensions <database> <branch> <profile> --org <org> --format json

# Examples of approved writes
pscale branch config-profile create <database> <branch> <profile> --org <org> \
  --cluster-size <size> --replicas 2 --format json
pscale branch config-profile update <database> <branch> <profile> --org <org> \
  --parameters pgconf.max_connections=200 --format json

# Independently approved read-only capacity changes, not voting-replica changes
pscale branch config-profile create <database> <branch> <profile> --org <org> \
  --read-only-replicas 2 --format json
pscale branch config-profile update <database> <branch> <profile> --org <org> \
  --read-only-replicas 0 --format json

# Change the branch default profile (separate approval)
pscale branch config-profile set-default <database> <branch> <profile> --org <org> --format json

# Toggle one extension while preserving the enabled set from the CLI's catalog snapshot
pscale branch config-profile extensions enable <database> <branch> <profile> <extension> \
  --org <org> --format json
pscale branch config-profile extensions disable <database> <branch> <profile> <extension> \
  --org <org> --format json

# Replace the complete enabled extension set in one request
pscale branch config-profile update <database> <branch> <profile> --org <org> \
  --extensions hll,pg_stat_statements --format json
```

Create/update sends only explicitly supplied flags. Storage flags use bytes for `--min-storage` and `--max-storage`, MiB/s for `--storage-throughput`, and explicit booleans for `--storage-autoscaling`. Repeat `--parameters namespace.name=value` for multiple settings.

`--read-only-replicas` sets the total read-only replicas **per shard** in this profile (supported range 0–8), excluding the primary and independently of `--replicas`. Creation defaults to zero. On update, omit the flag to preserve the current count; an explicit `--read-only-replicas 0` requests removal. The CLI sends an explicitly provided count, including zero, without a local range check, so reject out-of-range input before proposing the write. This is Neki profile capacity, not the dedicated PostgreSQL read-replica command family.

Before changing the count, inspect the profile and shards using it, record the pre-write count, calculate the capacity/cost and availability impact, and obtain exact-target approval. Follow the asynchronous change-ID procedure below, inspect the exact profile change, and read `config-profile show` back. Profile JSON exposes `read_only_replicas`; the typed `config-profile changes list/show` JSON also exposes `previous_read_only_replicas`. Use `pscale branch config-profile changes show <database> <branch> <profile> <change-id> --org <org> --format json` for these before/after counts. Branch-wide `branch changes show` passes through the API object and does not guarantee those fields. Human/CSV profile list/show and profile-change list/show include a read-only-replica column. In addition to its summary table, human `config-profile changes show` adds a `Read-only replicas` difference row only when the decoded previous and new counts differ. Do not parse fixed column positions or confuse these counts with voting replicas.

The typed profile/change counts are plain integers: an API-omitted field is serialized as zero, indistinguishable from an explicit zero. A zero read-back alone therefore cannot prove removal persisted. For `--read-only-replicas 0`, retain a non-zero pre-write observation, verify the uniquely identified request completed successfully and its profile-specific before/after delta agrees with the approved removal, then reconcile the profile read-back. If the pre-write count is already zero, treat the request as a potential no-op, not verified removal. If counts are ambiguous, inconsistent, or lack corroborating completion evidence, report removal as unconfirmed and investigate; do not retry the write automatically.

Every profile write can be asynchronous. Before a write, page through unfiltered `pscale branch changes list <database> <branch> --org <org> --target-type config-profile --page <n> --per-page 100 --format json` results until a page is empty; block the write if any entry has `completed_at: null`, and snapshot all existing change IDs. After the write, page through the same list again and diff the IDs. If the write is asynchronous, require exactly one new entry matching the intended profile; do not guess when no unique request can be identified. Poll it with `pscale branch changes show <database> <branch> <change-id> --org <org> --format json` until `completed_at` is non-null, then read the affected profile or default back. A non-null completion timestamp marks termination, not proof of success: inspect the reported outcome and reconcile the requested state; failed, canceled, or unknown outcomes are not successful verification. Cancel only under the branch-wide `state: "pending"` plus `can_delete: true` rule above and only after approval for that exact change ID.

Use `extensions enable|disable` only with a current CLI: if any entry from `extensions --format json` lacks `can_enable`, upgrade before toggling. Read the catalog first and review the target's `name`, `enabled`, `can_enable`, `internal`, and `loader`; `shared_preload_libraries` can signal restart or availability impact. Skip the command when `enabled` already matches the requested state. The CLI rejects an unknown target or one with `can_enable: false`, but it does not short-circuit no-ops. It builds a complete set from one catalog snapshot, carrying forward every other entry currently marked `enabled`, including internal or non-enablable entries, and submits that set through the profile update API without a concurrency precondition. Therefore serialize toggles, re-read the catalog only after the prior request has `completed_at` non-null, and use one reviewed `update --extensions` request—not back-to-back toggles—for a multi-extension change.

The toggle's JSON output is the pre-update target catalog entry with `enabled` changed client-side, not an updated profile, server-confirmed extension, or change request. Use the before/after change-ID procedure above to identify the resulting request, wait for `completed_at` to become non-null, and then re-read `extensions` to verify the persisted set.

Use `update --extensions` only when intentionally replacing the complete enabled set: omit it to preserve the set, or pass one reviewed comma-separated set to replace it. Carry forward every currently enabled internal or `can_enable: false` entry unless its removal is explicitly intended, approved, and known to be accepted by the target API; only add entries whose catalog record has `can_enable: true`. Passing `--extensions=` submits an empty set, but the CLI does not establish how the API treats required or internal entries, so do not treat it as a complete, predictable disable-all operation. Blank names inside a non-empty list are rejected. Extension removal can break dependent objects or parameters; verify the completed request and persisted catalog.

`config-profile maintenance` can target one or multiple profiles and returns before completion. It can cause brief unavailability. Use branch-wide `branch maintenance run` when every profile should be maintained. Profile deletion is destructive and requires exact-target approval before `--force`.

## Routers

Routers are billed Neki routing groups. Discover valid SKUs and current state before creating or resizing one:

```bash
pscale branch router list <database> <branch> --org <org> --format json
pscale branch router show <database> <branch> <router> --org <org> --format json
pscale branch router sizes <database> <branch> --org <org> --format json

pscale branch router create <database> <branch> <router> --org <org> \
  --size <NKR-size> --replicas-per-cell 1 --format json
pscale branch router update <database> <branch> <router> --org <org> \
  --autoscaling --max-replicas-per-cell 4 --target-cpu-utilization 70 --format json
```

SKU names such as `NKR-5` also accept underscores. Router changes are asynchronous; follow them with `router changes list/show`, and re-read the router after completion. Deletion removes a connection target and requires dependency review and explicit approval before `--force`.

## Sidecars And Admin

Each configuration profile has one connection-pool sidecar. Sidecars cannot be created or deleted independently. The deprecated `branch sidecar` family is retained for compatibility, but new parameter changes use the owning profile and the `sidecar` namespace. Read the profile catalog first; the CLI passes through API catalog entries and does not guarantee that it contains `sidecar.*` keys. If the intended key is absent, use the legacy read-only `sidecar parameters` fallback below for that same profile. Match the returned `namespace` and `name` to the exact intended `sidecar.<name>` key. Do not mechanically rename a `pgbouncer` entry to `sidecar`: a legacy name alone does not establish the new write key. If neither catalog verifies that exact key, the catalogs disagree, or required safety metadata is missing, stop and investigate compatibility; do not propose a write or fall back to deprecated `sidecar update`. Apply the [`requires_update` preflight](#parameter-update-requirements) to the matched entry, reject internal entries, and obtain approval for the exact profile, parameter, restart impact, and proposed value before the write.

```bash
pscale branch config-profile show <database> <branch> <profile> --org <org> --format json
pscale branch config-profile parameters <database> <branch> <profile> --org <org> --format json
# Read-only compatibility fallback when the profile catalog lacks the intended key.
# The legacy sidecar selector accepts the owning configuration profile name.
pscale branch sidecar parameters <database> <branch> <profile> --org <org> --format json
# Only after an exact namespace/name match, all preflights, and exact-target approval
pscale branch config-profile update <database> <branch> <profile> --org <org> \
  --parameters sidecar.<name>=<value> --format json
```

Each Neki cluster also has one failover/recovery admin. It cannot be listed, created, or deleted independently. Before `admin update --parameters`, read that admin's catalog below and apply the [`requires_update` preflight](#parameter-update-requirements); stop on non-null requirements, and never treat `null` / `No` as proof that no update is needed.

```bash
pscale branch admin show <database> <branch> --org <org> --format json
pscale branch admin sizes <database> <branch> --org <org> --format json
pscale branch admin parameters <database> <branch> --org <org> --format json
pscale branch admin update <database> <branch> --org <org> \
  --size <NKA-size> --format json
```

For sidecar settings changed through a profile, use the configuration-profile asynchronous change-ID procedure above, then re-read the profile and parameter catalog. Legacy `sidecar update` still requires one or more `--parameters`; existing sidecar requests can be inspected via legacy `sidecar changes list/show`. Admin update requires `--size` and/or repeatable `--parameters` and creates asynchronous changes; use `admin changes list/show`. Obtain separate approval before cancellation and verify the outcome plus persisted target state, not merely a terminal timestamp.

## Maintenance

Branch-wide `pscale branch maintenance run` belongs to `pscale-branch`. Before handing off a Neki branch-wide run, inspect every page of the unfiltered consolidated branch change queue across admin, cluster, configuration-profile, router, and sidecar targets; treat any entry with `completed_at: null` as in flight. Confirm the impact window and recovery plan, and obtain explicit approval for the availability-impacting operation. Keep `pscale branch config-profile maintenance` in this skill for profile-scoped maintenance.

```bash
pscale branch changes list <database> <branch> --org <org> \
  --page 1 --per-page 100 --format json
pscale branch changes list <database> <branch> --org <org> \
  --page 2 --per-page 100 --format json
```

After `pscale-branch` starts branch-wide maintenance, verify completion with Neki-owned reads such as `config-profile list/show` and its parameter catalog, `router list/show`, and `admin show`; do not rely on `pscale branch infra` for Neki unless an exact help fence proves support.

## Backup Restore

`pscale backup restore` creates a new branch. For Neki restores, profile and router sizing can be inherited from the live source branch or overridden with repeatable `--config-profile` and `--router` flags. `backup restore show` previews the sizes that will be used when overrides are omitted.

```bash
pscale backup show <database> <source-branch> <backup-id> --org <org> --format json
pscale backup restore show <database> <source-branch> <backup-id> --org <org> --format json

pscale backup restore <database> <new-branch> <backup-id> --org <org> \
  --config-profile name=<profile>,cluster-size=<size>,replicas=<count> \
  --router name=<router>,size=<size>,replicas-per-cell=<count> \
  --format json

pscale branch show <database> <new-branch> --org <org> --format json
```

The restore preview uses the source branch's current profile/router sizes, not values stored on the backup. If the source branch was resized after the backup was taken, inherited sizes follow the current source branch. Configuration profiles and routers are restored, but profile/router parameters, sidecar settings, admin settings, and autoscaling are not. `--cluster-size` is shorthand for overriding the default profile; omit it to inherit that profile's source size. MySQL and PostgreSQL restores reject Neki `--config-profile` and `--router` options. Confirm source branch, backup ID, target branch name, inherited sizes, overrides, and cost before restoring.

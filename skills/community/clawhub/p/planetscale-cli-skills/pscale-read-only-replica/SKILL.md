---
name: pscale-read-only-replica
description: Manage dedicated PostgreSQL read replicas with PlanetScale CLI. Use when listing, inspecting, creating, resizing, configuring, detaching, or deleting Postgres dedicated read replicas, choosing replica regions, or changing replica parameters. Triggers on pscale dedicated-read-replica, pscale read-only-replica, Postgres read replica, analytics replica, read capacity, replica region, replica parameters.
---

# pscale dedicated-read-replica

Manage dedicated read capacity for a PlanetScale PostgreSQL branch. These named resources are separate from the primary branch cluster's replicas and from Vitess/MySQL read-only regions.

For **Neki read-only replicas**, use `pscale-neki`: per-shard capacity is configured with `branch config-profile create/update --read-only-replicas`, not dedicated PostgreSQL replica resources. Confirm the engine before choosing a capacity workflow.

Use the canonical `pscale dedicated-read-replica` command. The hidden `pscale read-only-replica` compatibility command remains available but prints a deprecation warning on stderr; do not introduce it into new automation.

## Destructive-operation safety

These gates apply to every destructive example here, including deletion, demotion, protection removal, connection/transaction termination, deploy-request closure/revert, and cleanup. Command examples and CLI confirmation prompts are not authorization.

1. Inspect fresh state and confirm support for the target engine and installed CLI. Obtain explicit approval for the exact organization and, where applicable, database, branch, and resource ID/name, plus the operation and flags; use an explicit `--org` on every operation. Stop on unsupported operations or uncertain identity.
2. Check dependencies and availability: applications, active users, child resources, routing, pending changes, and the maintenance window. Do not infer that a stale, merged, or unused-looking resource is disposable.
3. Require a verified recovery path that survives the operation: confirm backup/export usability and retention, or tested replacement/recreation instructions, ownership, and recovery time. A backup name alone is not verification; stop if recovery cannot be established.
4. Execute only the approved action. Force flags, descendant deletion, demotion, and disabling protection require separate explicit approval; never add them to work around a refusal. For a known headless session, obtain approval for the required force flag up front, before attempting the operation; stop if that approval is absent or any attempt is refused.
5. Perform read-back verification of the exact target and dependent service health. Inspect pending/asynchronous outcomes before claiming completion. Authentication/network errors are not proof of absence; an ambiguous result requires investigation, not an automatic retry.

## Read before writing

```bash
# Inventory the branch when the replica name is unknown
pscale dedicated-read-replica list <database> <branch> --org <org> --format json

# Or inspect one exact target when its name is already known; do not run both
pscale dedicated-read-replica show <database> <branch> <name> --org <org> --format json
```

The command group checks the database kind itself and rejects Vitess databases, so a separate `database show` preflight is unnecessary. Use `pscale region list --org <org> --format json` to discover region slugs. Inspect the primary branch before choosing capacity; omitting `--cluster-size` inherits its size, which is usually the safest and least wasteful starting point. When an explicit override is intentional, use `pscale size cluster list --org <org> --engine postgresql --format json` and choose a fully qualified SKU matching the branch's provider and architecture. Interactive completion for create/update `--cluster-size` is already scoped to the target Postgres branch's engine, provider, and architecture and is preferred when available.

List/show JSON serializes the underlying API model rather than the normalized human/CSV fields. Expect API-native nested objects and names, probe a representative response before automating, and use defensive access such as `.region.slug // .region.name // empty` and `.cluster_display_name // .cluster_name // empty` rather than assuming a fixed flattened schema.

To validate branch-level replica routing after provisioning, run a read-only query with the actual replica flag:

```bash
pscale sql <database> <branch> --org <org> --format json \
  --replica --query "SELECT 1"
```

`pscale sql --replica` and `pscale shell --replica` route reads across the branch's primary replicas and all read-only regions; they cannot pin a query to one named dedicated read replica. Validate a specific named/region target through the same application connection path or region-aware endpoint that production will use.

## Create

```bash
# Inspect primary sizing before deciding whether to override it
pscale branch show <database> <branch> --org <org> --format json

# The API defaults to one instance and the primary cluster size
pscale dedicated-read-replica create <database> <branch> <name> \
  --region <region> --org <org> --format json

# Select capacity explicitly
pscale dedicated-read-replica create <database> <branch> <name> \
  --region <region> \
  --replicas 2 \
  --cluster-size PS_10_GCP_X86 \
  --org <org> --format json
```

Confirm the organization, database, branch, unique name, region, cluster size, instance count, and expected cost before creating capacity. Creation is asynchronous: inspect `state` and `ready` in the returned object, then poll `list` or `show` until ready rather than assuming the resource can serve reads immediately.

## Update

```bash
# Inspect current state first
pscale dedicated-read-replica show <database> <branch> <name> --org <org> --format json

# Change one or more supported dimensions
pscale dedicated-read-replica update <database> <branch> <name> \
  --replicas 3 \
  --cluster-size PS_20_GCP_X86 \
  --parameters pgconf.max_connections=300 \
  --org <org> --format json

# Verify the asynchronous result
pscale dedicated-read-replica show <database> <branch> <name> --org <org> --format json
```

At least one of `--replicas`, `--cluster-size`, or repeatable `--parameters namespace.name=value` is required. Parameter values must be greater than or equal to the primary branch's corresponding values. Review restart, connection, capacity, and cost impact before approval; then poll until the returned state is terminal and ready.

## Detach into a standalone branch

`dedicated-read-replica detach` is a hidden, feature-gated Postgres command; direct `--help` is available even though the parent does not list it. Read the compatibility note in [references/commands.md](references/commands.md). Detach is irreversible: it removes the dedicated replica resource and promotes it into a standalone branch in the same database. The new branch keeps the replica's name, region, size, replica count, storage configuration, and parameters, and receives a copy of the source branch's roles. Review the copied access and changed routing with the owner.

Apply all destructive-operation gates above. Confirm the replica is ready with no pending changes, the destination name is suitable, clients have a verified remaining read path/capacity, and recovery is usable. Attached dedicated PgBouncers must be absent; if any are confirmed attached, stop. The branch-wide `pgbouncer list` below is inventory only, not an exact-replica attachment check. The CLI's PgBouncer/replica JSON models do not expose a dedicated-replica attachment identifier: `target` values such as `primary`, `replica`, or `replica_az_affinity` do not identify a named dedicated replica. If the inventory is nonempty and attachment status cannot be established from an authoritative exact-replica control-plane record or PlanetScale support, stop before detach. Do not infer attachment or absence from pooler names, regions, or generic replica targets. Deleting a PgBouncer or replica is a separate destructive operation requiring its own dependency/recovery review and explicit approval, never automatic detach preparation. A 404 may mean the feature is unavailable, not that the replica is absent.

```bash
pscale dedicated-read-replica show <database> <branch> <name> --org <org> --format json
# Branch-wide inventory only: resolve any uncertain attachment before proceeding
pscale pgbouncer list <database> <branch> --org <org> --format json

# Only after attachment absence is established and explicit approval for irreversible detachment; interactive confirmation
pscale dedicated-read-replica detach <database> <branch> <name> --org <org>

# Read the returned branch name and verify readiness and dependent service health
pscale branch show <database> <new-branch> --org <org> --format json
pscale dedicated-read-replica list <database> <branch> --org <org> --format json
```

Headless/JSON execution requires separately approved `--force` up front; it suppresses confirmation, not readiness or feature restrictions. Do not retry a refused or ambiguous detach automatically. JSON returns a Postgres branch model; the new branch may still be promoting (`ready: false`). Use bounded read-only checks of that returned branch and source capacity; report pending state if readiness is not established. A success message does not prove promotion or application cutover is complete.

## Delete

Deletion removes dedicated read capacity and can break clients routed to the named replica. Inventory those clients, confirm replacement capacity and the exact target, obtain explicit approval, and verify the resource before using `--force` in headless/JSON execution.

```bash
pscale dedicated-read-replica show <database> <branch> <name> --org <org> --format json

# Before deletion, send representative production reads through the exact
# application connection path/region that will remain and verify success,
# latency, and capacity there; --replica alone cannot prove a named target.

# Interactive confirmation (preferred when a TTY is available)
pscale dedicated-read-replica delete <database> <branch> <name> --org <org>

# OR: non-interactive/JSON only after explicit approval
pscale dedicated-read-replica delete <database> <branch> <name> --org <org> --format json --force
pscale dedicated-read-replica list <database> <branch> --org <org> --format json
```

Never add `--force` merely to bypass an interactive prompt. JSON/CSV and other non-human execution cannot present the confirmation and fails without `--force`, which is why the headless example includes it. Run exactly one deletion form, then verify absence from the final list and confirm remaining read capacity.

## Related skills

- `pscale-password` — obtain connection details for named PostgreSQL replica targets
- `pscale-branch` — manage primary branch size, replicas, and parameters
- `pscale-database` — manage Vitess/MySQL read-only regions instead

## Reference

See `references/commands.md` for checksum-verified command help surfaces.

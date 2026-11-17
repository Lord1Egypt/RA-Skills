# Physical Primary/Standby Tenants

Use this workflow for tenant-level physical standby creation, topology inspection, switchover, failover, decouple, recovery-target changes, log-source changes, or protection-mode changes. Do not confuse it with deployment topology.

## Prove Both Compatibility Layers

Resolve the exact primary deployment and tenant and the intended standby deployment and tenant. Record each cluster ID, product form, component key, OceanBase version/release, artifact hash, tenant role, SQL/RPC endpoint, zones, resources, and current health.

Verify separately:

1. **OceanBase kernel compatibility:** the exact product forms and versions support the requested replication relationship and protection mode.
2. **OBD orchestration compatibility:** the installed OBD core and both selected component plugins support the exact component pair in the requested direction.

Healthy clusters and kernel support do not prove that OBD can orchestrate a heterogeneous pair. If release-specific evidence for that pair and direction is unavailable, stop before `create-standby`. Do not rename registered components, inject an unrelated component, redeploy healthy clusters, or change network/resource fields as a workaround.

## Preflight the Relationship

Read the installed help for the selected tenant subcommand. Confirm the primary tenant is healthy and `PRIMARY`, its log stream is complete, and the standby cluster has sufficient per-zone CPU, memory, log disk, Unit, and resource-pool capacity.

### Default tenant identity and password

Do not ask for a tenant name or tenant root password that the user omitted:

- If this workflow first creates the primary tenant, follow [tenant creation](tenant-creation.md). With no user override, use the minimal OBD create path; the reviewed baseline creates primary tenant `test` with an empty root password.
- The primary tenant is a required positional identity for `create-standby`. Resolve it from the actual primary deployment. For a newly default-created pair it is `test`; for an existing deployment, do not invent `test` or select arbitrarily when more than one eligible primary tenant exists.
- If the user omitted the standby tenant name, omit `--tenant-name`. The reviewed OBD default creates it with the same name as the primary tenant. Pass `--tenant-name` only for an explicit user override.
- In `create-standby`, `--tenant-root-password` authenticates to the **primary** tenant; it does not assign a new password to the standby tenant. If the user omitted it, omit the option and use the reviewed empty-password default. Pass it only when the user explicitly supplied the primary tenant password, and then only through the approved protected local procedure.
- Physical replication carries the tenant's account state to the standby. For a fresh pair created entirely with defaults, verify root authentication with an empty password on both sides. If an existing primary rejects the omitted empty password, stop without guessing, generating, or rotating a credential.

This policy does not make the separate `standbyro` replication account empty. Its password remains OBD-managed and non-empty unless the user explicitly supplies an existing account credential as described below.

For a service-based source, verify the version-required SQL/RPC reachability and credential path. For a location-based source, verify the data-backup and archive-log chain, recovery target, storage reachability, and decryption material. Resolve sync/protection behavior from an explicit user value or the installed version's proved default after the capability check below. When a strong-sync mode is supported and selected, evaluate its write-availability, latency, downgrade, and failure-domain consequences; do not ask the user to choose a mode that the selected older workflow does not expose.

Keep tenant-root, `standbyro`, storage, and decryption credentials protected. If the selected command exposes a required secret only through argv, disclose that limitation and use an approved permission-controlled local procedure; never describe the argument path as protected.

For the reviewed OBD V4.6.0 path using the OceanBase `4.2.0.0` plugin, a supplied `--standbyro-password` must be non-empty and must not contain a single quote, double quote, backtick, semicolon, or ASCII space. Validate the actual value locally without printing it, and re-read the installed plugin before applying this release-specific rule elsewhere.

Do not let omission of that option make the account decision implicit. Before mutation, select and authorize exactly one path:

1. **Existing manually managed `standbyro`:** supply the matching approved local credential through `--standbyro-password`. If the account exists but the value is absent or does not authenticate, stop; do not replace the account or rotate its password implicitly.
2. **OBD-managed `standbyro`:** allow OBD to reuse its stored value or, when none exists, generate a password, create the account if needed, grant its required read access, and persist the password in deployment component metadata. Disclose those account/grant writes and metadata persistence before execution. Verify metadata path ownership and permissions, backup/export exposure, who can retrieve the secret, redaction, and the post-creation rotation and account-lifecycle plan.

## Create and Accept a Standby

In builds that expose it, positional arguments are commonly ordered as standby deployment, primary deployment, and primary tenant. Confirm that order from installed help:

```bash
obd cluster tenant create-standby \
  <standby_deploy_name> \
  <primary_deploy_name> \
  <resolved_primary_tenant_name> \
  --type=<SERVICE_or_LOCATION> \
  --sync-mode=<reviewed_mode> \
  [version-supported source, resource, and credential options supplied through the approved local procedure]
```

This is the default-name, default-password form. Add `--tenant-name` only when the user supplied a different standby name, and add `--tenant-root-password` only when the user supplied the primary tenant's non-default root password. Do not copy ordinary tenant-create options without checking `create-standby --help`.

Accept creation only when OBD and SQL show the intended `PRIMARY`/`STANDBY` roles, the effective standby name equals the user override or otherwise the primary tenant name, expected root authentication succeeds with the explicit user credential or otherwise an empty password for a fresh default-created pair, the topology graph has exactly the intended edge, the log source and version-applicable protection state are correct, replay is advancing without errors, measured replication lag is acceptable, `standbyro` authentication works, the selected credential persistence and custody path is verified without exposing the value, and no partial Unit/pool/account remains. A controlled write/replay test is optional and requires a separately approved test fixture; do not write business data merely to validate creation.

## Role and Source Operations

Refresh the topology graph, roles, reachability, replay SCN/time, lag, errors, application routing, archive state, and version-applicable protection state immediately before every mutation.

For `switchover`, `failover`, and `decouple`, do not ask for a tenant root password that the user omitted. When installed help exposes `--tenant-root-password`, omit it and use the reviewed empty-password default. Pass the option only for an explicit user-supplied tenant password through the approved protected local procedure. If the empty-password attempt does not authenticate to an existing non-default tenant, stop and request the actual credential; do not generate, reset, or rotate it. A `--standbyro-password` option is a separate replication credential: omit it to let the installed OBD workflow reuse its managed value unless the user explicitly supplied the matching manually managed credential.

First determine whether the installed kernel catalog and selected OBD plugin/workflow expose strong-sync protection modes and destination metadata. Capability absence is different from a failed query. In the reviewed older path, OceanBase 4.3.5.6 selects the `4.2.0.0` tenant workflow, `DBA_OB_TENANTS` does not expose `PROTECTION_MODE`, and failover has no strong-sync transition stage. Reconfirm the installed routing and observed columns rather than applying that example universally. For such a proved older path, record protection mode and sync-destination checks as not applicable; their absence does not block the operation or make an otherwise complete result `partial`.

When strong-sync capability is present, derive and show the version-specific protection-mode transition for every involved tenant before authorizing a role mutation. The reviewed capable OBD V4.6.0 path behaves as follows:

| Operation | Topology or condition | Automatic protection-mode result |
|---|---|---|
| Planned switchover | cascading topology, or the selected standby is itself the configured strong-sync standby (including one-primary/one-standby and one-primary/multiple-standby topologies) | modes remain unchanged |
| Planned switchover | one primary has mixed strong-sync and performance standbys, and the directly associated performance standby is switched | every involved tenant changes to `MAXIMIZE PERFORMANCE` |
| Emergency failover | a strong-sync standby is promoted | the promoted tenant changes to `MAXIMIZE PERFORMANCE` |
| Decouple | a strong-sync standby is decoupled | the former primary and standby change to `MAXIMIZE PERFORMANCE` |

Treat any reduction to `MAXIMIZE PERFORMANCE` as a change to the data-loss envelope, not an incidental role-switch effect. Show the affected tenant identities and before/after modes and obtain explicit authorization for the downgrade in addition to the role operation. When strong-sync capability is present but version-matched evidence does not prove the installed version's transition, stop before mutation rather than assuming this matrix applies. Do not impose this stop when preflight proved that the selected older workflow has no such capability.

### Planned switchover

Use the installed `switchover` form only when both sides are healthy and synchronized within the accepted threshold. Coordinate writes and client routing and obtain availability-impact authorization. Verify both new roles, reverse-direction replication, write endpoint, client routing, and any applicable authorized protection-mode transition afterward.

### Emergency failover

Failover is emergency promotion, not a substitute for switchover. Prove the old primary cannot accept writes and is fenced from clients and peers. Report the last synchronized SCN/time, possible data-loss window, and any applicable automatic protection-mode downgrade, then obtain explicit failover authorization plus downgrade authorization when that downgrade exists. Verify new-primary writeability, routing, and the version-applicable protection state, and keep the old primary fenced until a reviewed reintegration plan exists.

### Decouple

Decouple permanently removes the relationship and can leave two independently writable tenants. Obtain explicit authorization for that outcome and any applicable automatic protection-mode downgrade, then verify relationship and log-source metadata are removed and record both independent identities, routes, and version-applicable protection states.

After any switchover, failover, or decouple, always verify the database-side tenant role and status, intended relationship graph, log-source or replay state, routing, and authenticated data plane. When the installed kernel and workflow expose strong-sync behavior, additionally query the observed `PROTECTION_MODE` column and version-supported sync-destination surface such as `CDB_OB_SYNC_STANDBY_DEST`, then compare them with the authorized transition matrix. If a required applicable value is unavailable or mismatched, report `partial` or `unknown` and keep fencing and routing decisions conservative. When preflight proved those fields and transitions are not supported by the selected older path, report them as not applicable rather than treating their absence as a failed acceptance layer.

### Recovery target, log source, and protection mode

Use `recover`, `switch-log-source`, or `set-sync-mode` only when installed help exposes the operation. Validate mutually exclusive timestamp, SCN, and unlimited-replay choices; SERVICE versus LOCATION source requirements; and topology support for the selected mode. Verify database-side values and continuing replay after the change.

## Destruction, Upgrade, and Failure Boundaries

Before dropping either tenant or upgrading/destroying either deployment, inspect the complete relationship graph and the version-specific standby guards. Never add `--ignore-standby` automatically. Show every affected tenant, availability or orphaning consequence, required order, and recovery path.

On any partial result, preserve both deployment configurations, roles, graph, task/trace, replay state, resources, and accounts. Do not drop a partial standby, fail over, decouple, or redeploy either cluster merely to retry creation.

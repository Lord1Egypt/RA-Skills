---
name: tenant-management
description: Manage OceanBase tenant lifecycle, workload optimization, backup and restore, and physical primary/standby relationships through obd. Use for tenant creation, deletion, inspection, optimization, backup, restore, switchover, failover, or related disaster-recovery requests. Do not use for cluster deployment lifecycle.
metadata:
  author: oceanbase
  version: "2.0.3"
---

<!-- Compatibility anchors retained for published 2.x deep links. -->
<a id="oceanbase-tenant-management-obd"></a>
<a id="when-to-use-this-skill"></a>
<a id="tenant-commands"></a>
<a id="create-tenant"></a>
<a id="drop-tenant"></a>
<a id="show-tenants"></a>
<a id="optimize-tenant"></a>
<a id="backup-restore"></a>
<a id="backup--restore"></a>
<a id="set-backup-config"></a>
<a id="run-backup"></a>
<a id="restore-from-backup"></a>
<a id="usage-examples"></a>
<a id="create-a-tenant"></a>
<a id="configure-and-run-backup"></a>
<a id="related-skills"></a>

# OceanBase Tenant Management

Resolve the installed OBD build, product form, deployment, and tenant before selecting a command. This skill supports community and commercial OceanBase forms when the installed command and component plugins prove the requested operation is available.

## Default Tenant Configuration

Creating a tenant still requires an explicit user request; cluster deployment alone never implies a business tenant. After creation is requested, do not ask for tenant settings the user omitted. Confirm the installed OBD defaults and omit those options so OBD owns the defaults for tenant name, mode, placement, replicas, Units, resources, IOPS, time zone, charset/collation, optimization, variables, network allowlist, and initial password. Explicit user values override only the corresponding defaults.

In the reviewed OBD baseline, the minimal create path produces tenant `test`, MySQL mode, all active zones, `RANDOM` primary zone, maximum currently allocatable tenant resources bounded by the selected servers, allowlist `%`, and an empty tenant password. Preserve that empty-password default when no password was supplied: do not ask for one, generate one, or set one after creation. Read the full [tenant default and verification workflow](references/tenant-creation.md) before creating a tenant.

Apply the same no-prompt identity and password policy when building a physical primary/standby tenant pair. If the primary tenant must be created, apply each omitted value independently: the ordinary OBD defaults are tenant `test` and an empty root password. When creating its standby, omit `--tenant-name` unless the user supplied a standby name, so OBD uses the primary tenant name; omit `--tenant-root-password` unless the user supplied the primary tenant's root password, so the reviewed workflow tries the empty-password default. The required positional primary-tenant identity must still be resolved from actual primary-cluster state rather than guessed. These tenant-root defaults do not apply to the separate `standbyro` replication account, whose password must follow the installed OBD workflow. Read [physical primary/standby tenants](references/physical-standby.md) before creating or operating that relationship.

## Shared Gates

Read the shared references required by the current stage:

- Before selecting syntax, product form, or packages, read [product and capability resolution](../references/product-and-capability-resolution.md).
- Before any live controller/host/deployment query, SSH/SQL/API/network access, external action, or mutation, read the [operation contract](../references/operation-contract.md).
- Before declaring success, read the [completion criteria](../references/completion-criteria.md).
- After a failure, timeout, interruption, or mixed result, read [failure recovery and evidence](../references/failure-recovery-and-evidence.md) before retrying or cleaning anything.
- Before dropping or removing a tenant, database resource object, backup/archive object, or generated artifact, read [cleanup and ownership boundaries](../references/cleanup-boundaries.md).

## Route by Intent

| Request | Required reference |
|---|---|
| Create or inspect a tenant; plan resources, topology, credentials, or network allowlists | [tenant-creation.md](references/tenant-creation.md) |
| Drop a tenant | [tenant-deletion.md](references/tenant-deletion.md) |
| Optimize an existing tenant for a workload | [workload-optimization.md](references/workload-optimization.md) |
| Configure archive/backup storage, run, inspect, or cancel a backup, or restore, inspect, or cancel a tenant restore | [backup-restore.md](references/backup-restore.md) |
| Create or operate a physical primary/standby tenant, including switchover, failover, decouple, recovery target, log source, or protection mode | [physical-standby.md](references/physical-standby.md) |

## Hard Boundaries

- Treat tenant drop, tenant restore, backup-task cancellation, restore-task cancellation, failover, and decouple as separate high-impact operations. Authorization for inspection, ordinary tenant creation, backup, restore, or switchover does not authorize cancellation. The V4.6.0/current reviewed restore path creates a new target tenant and refuses an existing target; do not invent overwrite semantics or turn restore authorization into permission to drop an existing tenant.
- Do not place tenant, `standbyro`, storage, decryption, KMS, or other credentials in reusable commands or reports.
- A tenant row or successful OBD exit is not completion. Apply the domain checks in the selected reference and verify an authenticated data-plane outcome when applicable.
- Do not infer a tenant relationship from deployment names alone.

For cluster deployment, component lifecycle, or upgrades, use [cluster-management](../cluster-management/SKILL.md). For benchmarks and functional tests, use [testing-and-benchmark](../testing-and-benchmark/SKILL.md).

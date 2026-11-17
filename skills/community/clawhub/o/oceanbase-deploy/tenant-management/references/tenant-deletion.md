# Tenant Deletion

Tenant deletion removes database data and can invalidate applications, backup jobs, CDC consumers, and standby relationships. Read the installed `obd cluster tenant drop --help` before proposing syntax.

## Preflight

Resolve the deployment, cluster identity, exact tenant ID/name, compatibility mode, current role and status, the complete set of resource pools and Unit Configs, their reference counts and ownership, Units, active sessions, application routes, scheduled work, backup/archive tasks, restore tasks, OCP records, CDC consumers, and the complete physical-standby graph.

Inspect the installed drop plugin's resource-deletion algorithm before execution. Verified current plugin code fetches only one pool, issues `DROP TENANT ... FORCE`, and then attempts to drop that pool and its Unit Config. If the tenant has multiple pools, a shared Unit Config, ambiguous ownership, or any topology that violates the plugin's single-pool/exclusive-config assumption, stop before the irreversible tenant drop and use a separately reviewed supported procedure. Do not discover this mismatch after deleting the tenant.

Confirm that a current, independently usable backup exists when recoverability is required. A backup command exit alone is not proof of recoverability. Do not target the system tenant or another protected product-owned tenant.

If a primary or standby relationship exists, stop and apply [physical-standby.md](physical-standby.md). Never add `--ignore-standby` automatically. That option can make related standby tenants unusable and requires its own topology-specific destructive authorization.

## Authorize and Execute

Present the exact deployment, tenant, tenant ID, data and resource objects to be removed, active consumers, standby consequences, expected outage, backup identity, and recovery boundary. Obtain destructive authorization immediately before the command.

Use the long option confirmed by installed help:

```bash
obd cluster tenant drop <deploy_name> --tenant-name=<tenant_name>
```

Do not infer permission to remove backup sets, archive logs, external storage, CDC state, application configuration, or retained credentials. Those are separately owned objects.

## Accept or Recover

Verify through OBD and SQL that the exact tenant is absent, its sessions are closed, and every expected OBD-owned Unit/resource-pool object—and no shared or unrelated object—was removed. Confirm unrelated tenants and external backup/archive data remain intact.

On timeout or partial deletion, preserve the trace and observe the database-side deletion state before any retry. Do not recreate a tenant with the same name, remove resource pools manually, or rerun with an ignore/force option until the terminal state and ownership of every residual object are known.

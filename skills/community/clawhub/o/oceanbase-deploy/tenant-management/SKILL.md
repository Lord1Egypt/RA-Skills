---
name: tenant-management
description: Manage OceanBase tenants using obd. Create, drop, show, and optimize tenants. Configure backup paths, run backups, and restore from backup. Use when users ask about OceanBase tenants, tenant creation, backup, restore, workload optimization, or multi-tenant management via obd.
compatibility: Requires obd CLI and a running OceanBase cluster.
metadata:
  author: oceanbase
  version: "1.0"
---

# OceanBase Tenant Management (obd)

Manage tenants within an OceanBase CE cluster using `obd cluster tenant` commands.

## When to Use This Skill

- Creating or dropping tenants
- Viewing tenant information
- Optimizing tenants for specific workloads
- Configuring and running backups
- Restoring tenants from backup

**For cluster lifecycle (deploy, start, stop, upgrade):** Use [cluster-management](../cluster-management/SKILL.md).
**For seekdb:** Use [seekdb](../seekdb/SKILL.md).
**For benchmarks:** Use [testing-and-benchmark](../testing-and-benchmark/SKILL.md).

---

## Tenant Commands

### Create Tenant
```bash
obd cluster tenant create <deploy_name> -n <tenant_name> [options]
```

### Drop Tenant
```bash
obd cluster tenant drop <deploy_name> -n <tenant_name>
```

### Show Tenants
```bash
obd cluster tenant show <deploy_name>
```

### Optimize Tenant
```bash
obd cluster tenant optimize <deploy_name> <tenant_name> -o <workload>
```

Supported workloads: `express_oltp`, `olap`, etc.

---

## Backup & Restore

### Set Backup Config
```bash
obd cluster tenant set-backup-config <deploy_name> <tenant_name> -d <data_uri> -a <log_uri>
```

### Run Backup
```bash
obd cluster tenant backup <deploy_name> <tenant_name>
```

### Restore from Backup
```bash
obd cluster tenant restore <deploy_name> <tenant_name> <data_uri> <log_uri>
```

See [references/backup-restore.md](references/backup-restore.md) for detailed backup and restore procedures.

---

## Usage Examples

### Create a Tenant
```bash
obd cluster tenant create test-cluster -n mysql
```

### Configure and Run Backup
```bash
obd cluster tenant set-backup-config test-cluster mysql -d file:///backup/data -a file:///backup/log
obd cluster tenant backup test-cluster mysql
```

---

## Related Skills

- [cluster-management](../cluster-management/SKILL.md) — Cluster lifecycle and deployment
- [seekdb](../seekdb/SKILL.md) — seekdb lifecycle and HA
- [testing-and-benchmark](../testing-and-benchmark/SKILL.md) — Performance testing

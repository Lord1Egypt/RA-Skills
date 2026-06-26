# Backup & Restore

Detailed procedures for OceanBase tenant backup and restore via obd.

## Setting Up Backup

### Step 1: Configure Backup Paths

Specify the data backup URI and log archive URI:

```bash
obd cluster tenant set-backup-config <deploy_name> <tenant_name> \
  -d <data_uri> \
  -a <log_uri>
```

- `<data_uri>`: Path for data backups (e.g., `file:///backup/data` or NFS path)
- `<log_uri>`: Path for log archives (e.g., `file:///backup/log`)

Ensure the backup directories exist and have sufficient disk space.

### Step 2: Run Backup

```bash
obd cluster tenant backup <deploy_name> <tenant_name>
```

Starts a full data backup of the specified tenant.

## Restoring from Backup

```bash
obd cluster tenant restore <deploy_name> <tenant_name> <data_uri> <log_uri>
```

- `<data_uri>`: Path to the data backup
- `<log_uri>`: Path to the log archive

The restore operation creates or overwrites the tenant with the backup data.

## Notes

- Backup paths must be accessible from all OBServer nodes in the cluster.
- For NFS-based backup, ensure all nodes mount the same NFS path.
- Log archiving provides point-in-time recovery capability.

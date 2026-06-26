# Backup Reference

Detailed configuration for BackupRepo, storage providers, continuous backups, and BackupPolicy customization.

Source: https://kubeblocks.io/docs/preview/user_docs/concepts/backup-and-restore/introduction

## BackupRepo Setup

### BackupRepo Credential Secret

Create a Secret with storage provider credentials before creating the BackupRepo:

**S3:**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: s3-credential
  namespace: kb-system
type: Opaque
stringData:
  accessKeyId: <AWS_ACCESS_KEY_ID>
  secretAccessKey: <AWS_SECRET_ACCESS_KEY>
```

**OSS (Alibaba Cloud):**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: oss-credential
  namespace: kb-system
type: Opaque
stringData:
  accessKeyId: <ALIBABA_ACCESS_KEY_ID>
  secretAccessKey: <ALIBABA_SECRET_ACCESS_KEY>
```

**GCS:**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: gcs-credential
  namespace: kb-system
type: Opaque
stringData:
  accessKeyId: <GCS_ACCESS_KEY_ID>
  secretAccessKey: <GCS_SECRET_ACCESS_KEY>
```

**MinIO:**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: minio-credential
  namespace: kb-system
type: Opaque
stringData:
  accessKeyId: <MINIO_ACCESS_KEY>
  secretAccessKey: <MINIO_SECRET_KEY>
```

### BackupRepo CR Examples

**S3:**

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: BackupRepo
metadata:
  name: s3-backuprepo
spec:
  storageProviderRef: s3
  accessMethod: Tool
  pvReclaimPolicy: Retain
  config:
    bucket: <bucket-name>
    region: <region>
    endpoint: ""
  credential:
    name: s3-credential
    namespace: kb-system
```

**OSS (Alibaba Cloud):**

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: BackupRepo
metadata:
  name: oss-backuprepo
spec:
  storageProviderRef: oss
  accessMethod: Tool
  pvReclaimPolicy: Retain
  config:
    bucket: <bucket-name>
    region: <region>
    endpoint: ""
  credential:
    name: oss-credential
    namespace: kb-system
```

**GCS:**

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: BackupRepo
metadata:
  name: gcs-backuprepo
spec:
  storageProviderRef: gcs
  accessMethod: Tool
  pvReclaimPolicy: Retain
  config:
    bucket: <bucket-name>
    region: <region>
    endpoint: ""
  credential:
    name: gcs-credential
    namespace: kb-system
```

**MinIO:**

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: BackupRepo
metadata:
  name: minio-backuprepo
spec:
  storageProviderRef: minio
  accessMethod: Tool
  pvReclaimPolicy: Retain
  config:
    bucket: <bucket-name>
    endpoint: <minio-endpoint>    # e.g. http://minio.minio-system.svc.cluster.local:9000
  credential:
    name: minio-credential
    namespace: kb-system
```

### Supported Storage Providers

| Provider | `storageProviderRef` | Notes |
|----------|---------------------|-------|
| AWS S3   | `s3`                | Standard S3 API |
| Alibaba OSS | `oss`           | Alibaba Cloud Object Storage |
| Tencent COS | `cos`           | Tencent Cloud Object Storage |
| Google GCS | `gcs`             | Google Cloud Storage |
| Huawei OBS | `obs`             | Huawei Cloud Object Storage |
| MinIO    | `minio`             | S3-compatible, self-hosted |

### Verify BackupRepo

```bash
kubectl get backuprepo
```

Status should show `Ready`:

```
NAME              STATUS   STORAGEPROVIDER   ACCESSMETHOD   AGE
s3-backuprepo     Ready    s3                Tool           5m
```

## BackupPolicy Customization

BackupPolicies are auto-created per cluster. To customize, edit the existing policy:

```bash
kubectl edit backuppolicy <cluster>-<component>-backup-policy -n <ns>
```

Key fields:

```yaml
spec:
  backupMethods:
  - name: xtrabackup
    actionSetName: xtrabackup-for-apecloud-mysql
    snapshotVolumes: false
    target:
      role: secondary    # backup from secondary to avoid primary impact
    env:
    - name: BACKUP_THREADS
      value: "4"
  - name: volume-snapshot
    snapshotVolumes: true
    target:
      role: secondary
```

## Continuous Backup for PITR

### MySQL (archive-binlog)

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: <cluster>-binlog-continuous
  namespace: <ns>
spec:
  backupMethod: archive-binlog
  backupPolicyName: <cluster>-mysql-backup-policy
  deletionPolicy: Delete
```

### PostgreSQL (wal-archive)

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: <cluster>-wal-continuous
  namespace: <ns>
spec:
  backupMethod: wal-archive
  backupPolicyName: <cluster>-postgresql-backup-policy
  deletionPolicy: Delete
```

### PITR Prerequisites

1. A completed **full backup** (xtrabackup / pg-basebackup)
2. A running **continuous backup** (archive-binlog / wal-archive)
3. Both must use the same BackupPolicy

### Check Continuous Backup Status

```bash
kubectl get backup -n <ns> | grep Running
```

Continuous backups stay in `Running` status as they continuously stream logs.

## Backup Deletion Policies

| Policy | Behavior |
|--------|----------|
| `Delete` | Backup data deleted when Backup CR is deleted |
| `Retain` | Backup data retained even after Backup CR deletion |
| `DoNotDelete` | Backup CR cannot be deleted (protected) |

## Documentation Links

- Backup & Restore Overview: https://kubeblocks.io/docs/preview/user_docs/concepts/backup-and-restore/introduction
- Configure BackupRepo: https://kubeblocks.io/docs/preview/user_docs/concepts/backup-and-restore/backup-repo
- On-demand Backup: https://kubeblocks.io/docs/preview/user_docs/handle-an-exception/full-backup
- Scheduled Backup: https://kubeblocks.io/docs/preview/user_docs/handle-an-exception/scheduled-backup
- PITR: https://kubeblocks.io/docs/preview/user_docs/handle-an-exception/pitr

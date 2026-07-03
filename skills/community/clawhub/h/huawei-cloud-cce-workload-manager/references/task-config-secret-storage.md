# ConfigMap, Secret & PVC Management

## Overview

ConfigMaps store non-sensitive configuration as key-value pairs or files. Secrets hold sensitive data (passwords, tokens) with base64 encoding. PersistentVolumeClaims (PVCs) request storage from the cluster.

## ConfigMap Operations

| Operation | Command |
|-----------|---------|
| Create from literal | `kubectl --kubeconfig=<kubeconfig-path> create configmap <name> --from-literal=key1=val1 -n <namespace>` |
| Create from file | `kubectl --kubeconfig=<kubeconfig-path> create configmap <name> --from-file=config.yaml -n <namespace>` |
| Get | `kubectl --kubeconfig=<kubeconfig-path> get configmap <name> -o yaml -n <namespace>` |
| Update/delete | `kubectl --kubeconfig=<kubeconfig-path> apply -f cm.yaml -n <namespace>` / `delete configmap <name> -n <namespace>` |

## Secret Operations

| Operation | Command |
|-----------|---------|
| Create generic | `kubectl --kubeconfig=<kubeconfig-path> create secret generic <name> --from-literal=password=s3cret -n <namespace>` |
| Create docker-registry | `kubectl --kubeconfig=<kubeconfig-path> create secret docker-registry regcred --docker-server=swr.cn-north-4.myhuaweicloud.com --docker-username=<user> --docker-password=<pass> -n <namespace>` |
| Get/describe | `kubectl --kubeconfig=<kubeconfig-path> get secret <name> -n <namespace>` / `describe secret <name> -n <namespace>` (values are base64 encoded) |
| Delete | `kubectl --kubeconfig=<kubeconfig-path> delete secret <name> -n <namespace>` |

## PVC Operations

| Operation | Command |
|-----------|---------|
| Create from YAML | `kubectl --kubeconfig=<kubeconfig-path> apply -f pvc.yaml -n <namespace>` |
| Get/describe | `kubectl --kubeconfig=<kubeconfig-path> get pvc -n <namespace>` / `describe pvc <name> -n <namespace>` (check status: Bound/Pending) |
| Delete | `kubectl --kubeconfig=<kubeconfig-path> delete pvc <name> -n <namespace>` |
| List StorageClasses | `kubectl --kubeconfig=<kubeconfig-path> get storageclasses` |

## CCE StorageClass Reference

CCE clusters provide multiple CSI StorageClasses for different storage types. Use `kubectl get sc` to list available StorageClasses in your cluster.

> **Important**: `cce-standard` is NOT a valid CCE StorageClass. Always use CSI-based StorageClasses listed below.

| StorageClass | Storage Type | Access Mode | Use Case | Min Capacity |
|-------------|-------------|-------------|----------|-------------|
| `csi-disk` | Cloud disk (EVS) | RWO | General block storage, databases, single-Pod workloads | 10Gi |
| `csi-disk-topology` | Cloud disk with topology | RWO | Cross-AZ scheduling with delayed binding | 10Gi |
| `csi-disk-dss` | Dedicated storage disk | RWO | Dedicated distributed storage (DSS) pools | 10Gi |
| `csi-sfsturbo` | SFS Turbo (extreme file storage) | RWX | High-performance shared file storage, AI/ML, multi-Pod shared data | 500Gi |
| `csi-nas` | General file storage (SFS) | RWX | Shared file storage, multi-Pod read/write | 1Gi |
| `csi-obs` | Object storage (OBS) | RWX | Object storage mount, log archiving, large unstructured data | 1Gi (no actual limit) |
| `csi-sfs` | SFS 3.0 capacity file storage | RWX | High-bandwidth shared file storage | 1Gi |

**Access Mode Reference**:

- `RWO` (ReadWriteOnce): Single node read/write — block storage (EVS)
- `RWX` (ReadWriteMany): Multiple nodes read/write — file/object storage (SFS, OBS)

### Storage Selection Guide

| Scenario | Recommended StorageClass | Reason |
|----------|-------------------------|--------|
| Database (MySQL/PostgreSQL) | `csi-disk` | Block storage, low latency, RWO |
| Web app static files | `csi-disk` | Simple, cost-effective |
| Multi-Pod shared config/data | `csi-nas` or `csi-sfsturbo` | RWX, shared across Pods |
| AI/ML training data | `csi-sfsturbo` | High bandwidth, low latency, RWX |
| Log archiving / backup | `csi-obs` | Unlimited capacity, cost-effective |
| CI/CD workspace | `csi-nas` | Shared across build agents |
| Cross-AZ deployment | `csi-disk-topology` | Delayed binding ensures same AZ as Pod |

Reference: [CCE Storage Management Best Practices](https://support.huaweicloud.com/usermanual-cce/cce_10_0900.html)

## Common Scenarios

### App configuration as ConfigMap

```bash
kubectl --kubeconfig=<kubeconfig-path> create configmap app-config --from-literal=LOG_LEVEL=info --from-literal=MAX_CONNECTIONS=100 -n <namespace>
kubectl --kubeconfig=<kubeconfig-path> get configmap app-config -o yaml -n <namespace>
```

Mount in Deployment:

```yaml
spec:
  containers:
  - name: app
    envFrom:
    - configMapRef:
        name: app-config
```

### Private image pull with Secret

```bash
kubectl --kubeconfig=<kubeconfig-path> create secret docker-registry regcred --docker-server=swr.cn-north-4.myhuaweicloud.com --docker-username=<user> --docker-password=<pass> -n <namespace>
```

Reference in Deployment:

```yaml
spec:
  imagePullSecrets:
  - name: regcred
```

### Block storage PVC (csi-disk)

For single-Pod workloads like databases:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: csi-disk
```

```bash
kubectl --kubeconfig=<kubeconfig-path> apply -f pvc.yaml -n <namespace>
kubectl --kubeconfig=<kubeconfig-path> get pvc data-pvc -n <namespace>
```

Mount in Deployment:

```yaml
spec:
  containers:
  - name: app
    volumeMounts:
    - name: data
      mountPath: /data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: data-pvc
```

### SFS Turbo shared storage PVC (csi-sfsturbo)

For multi-Pod shared high-performance file storage. SFS Turbo has a minimum capacity of 500Gi. To avoid waste, use dynamic subdirectory creation:

**Option 1: Full SFS Turbo PVC** (minimum 500Gi):

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: sfsturbo-pvc
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 500Gi
  storageClassName: csi-sfsturbo
```

**Option 2: SFS Turbo subdirectory PVC** (recommended, saves cost):

> Requires Everest plugin >= 2.4.73 and a pre-existing SFS Turbo instance in the same VPC.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: sfsturbo-sub-pvc
  annotations:
    everest.io/volume-as: absolute-path
    everest.io/sfsturbo-share-id: <sfsturbo-id>
    everest.io/path: /my-app-data
    everest.io/reclaim-policy: retain-volume-only
    everest.io/csi.enable-sfsturbo-dir-quota: "true"
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
  storageClassName: csi-sfsturbo
```

Key parameters:
- `everest.io/volume-as: absolute-path` — required, indicates subdirectory mode
- `everest.io/sfsturbo-share-id` — SFS Turbo instance ID (get from SFS Turbo console)
- `everest.io/path` — subdirectory absolute path (e.g., `/my-app-data`)
- `everest.io/reclaim-policy` — `retain-volume-only` (keep subdirectory on PVC delete) or `delete` (remove subdirectory)
- `everest.io/csi.enable-sfsturbo-dir-quota: "true"` — enable subdirectory capacity limit; `storage` then represents the quota size

Reference: [Dynamic SFS Turbo Subdirectory](https://support.huaweicloud.com/usermanual-cce/cce_10_0839.html)

### Object storage PVC (csi-obs)

For object storage mount (unlimited capacity, cost-effective):

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: obs-pvc
  annotations:
    everest.io/obs-volume-type: STANDARD
    csi.storage.k8s.io/fstype: obsfs
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  storageClassName: csi-obs
```

Key parameters:
- `everest.io/obs-volume-type` — `STANDARD` (standard) or `WARM` (infrequent access), only for `s3fs` fstype
- `csi.storage.k8s.io/fstype` — `obsfs` (parallel filesystem, high performance) or `s3fs` (object bucket mount)
- `storage: 1Gi` — only for validation, actual OBS has no capacity limit

Constraints:
- OBS mount does not support hard links (s3fs mode) or read-only mount
- Each OBS volume creates a resident process per mount — recommend OBS volume count <= Pod memory GiB count
- OBS limits 100 buckets per user — for many PVCs, use OBS API/SDK directly instead of mounting

Reference: [Dynamic Object Storage](https://support.huaweicloud.com/usermanual-cce/cce_10_0630.html)
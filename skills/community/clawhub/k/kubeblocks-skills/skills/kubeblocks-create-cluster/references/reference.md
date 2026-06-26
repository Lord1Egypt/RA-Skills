# Create Cluster Reference

Detailed Cluster CR fields, terminationPolicy comparison, and addon quick-start examples.

Source: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/create-and-connect-a-mysql-cluster

## Cluster CR Field Reference

### metadata

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Cluster name. Must be unique within the namespace. |
| `namespace` | string | Yes | Kubernetes namespace to create the cluster in. |
| `labels` | map | No | Custom labels for the cluster. |
| `annotations` | map | No | Custom annotations for the cluster. |

### spec

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `clusterDef` | string | Yes | Name of the ClusterDefinition (e.g., `mysql`, `postgresql`, `redis`). |
| `topology` | string | Yes | Topology name defined in the ClusterDefinition. Determines the component layout. |
| `terminationPolicy` | string | Yes | Controls what happens on cluster deletion. One of: `DoNotTerminate`, `Delete`, `WipeOut`. |
| `componentSpecs` | []ComponentSpec | Yes | List of component specifications. |
| `services` | []Service | No | Additional cluster-level services to expose. |
| `backup` | BackupSpec | No | Backup configuration for the cluster. |
| `schedulingPolicy` | SchedulingPolicy | No | Scheduling constraints (nodeSelector, tolerations, affinity). |

### spec.componentSpecs[]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Component name. Must match a component defined in the topology. |
| `serviceVersion` | string | No | Database engine version (e.g., `"8.0.30"`, `"14.8.0"`). |
| `replicas` | int | Yes | Number of replicas for this component. |
| `resources` | ResourceRequirements | No | CPU and memory requests/limits. |
| `volumeClaimTemplates` | []VolumeClaimTemplate | No | Persistent volume claims for this component. |
| `serviceAccountName` | string | No | Custom ServiceAccount for the component pods. |
| `services` | []Service | No | Component-level service overrides. |
| `systemAccounts` | []SystemAccount | No | Override system account credentials. |
| `schedulingPolicy` | SchedulingPolicy | No | Component-level scheduling constraints. |
| `configs` | []ConfigTemplate | No | Custom configuration template overrides. |

### spec.componentSpecs[].resources

| Field | Type | Description |
|-------|------|-------------|
| `requests.cpu` | string | Minimum CPU (e.g., `"0.5"`, `"2"`). |
| `requests.memory` | string | Minimum memory (e.g., `"0.5Gi"`, `"4Gi"`). |
| `limits.cpu` | string | Maximum CPU. |
| `limits.memory` | string | Maximum memory. |

### spec.componentSpecs[].volumeClaimTemplates[]

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Volume name. Typically `data`. Some addons also use `log` or `metadata`. |
| `spec.accessModes` | []string | Access modes. Usually `[ReadWriteOnce]`. |
| `spec.storageClassName` | string | StorageClass name. Defaults to the cluster default StorageClass. |
| `spec.resources.requests.storage` | string | Storage size (e.g., `"20Gi"`, `"100Gi"`). |

### spec.schedulingPolicy

| Field | Type | Description |
|-------|------|-------------|
| `nodeSelector` | map | Node labels for scheduling. |
| `tolerations` | []Toleration | Pod tolerations. |
| `affinity` | Affinity | Pod affinity/anti-affinity rules. |
| `topologySpreadConstraints` | []TopologySpreadConstraint | Topology spread constraints. |

## terminationPolicy Comparison

| Policy | Delete Pods | Delete PVCs | Delete Backups | Blocks `kubectl delete` |
|--------|:-----------:|:-----------:|:--------------:|:----------------------:|
| `DoNotTerminate` | No | No | No | Yes |
| `Delete` | Yes | Yes | No | No |
| `WipeOut` | Yes | Yes | Yes | No |

**Guidance:**
- **Production:** Use `DoNotTerminate`. Requires explicit policy change before deletion.
- **Dev / Test:** Use `Delete`. Cleans up resources but retains backups.
- **Disposable / CI:** Use `WipeOut`. Removes everything.

To change the policy on an existing cluster:

```bash
kubectl patch cluster <name> -n <ns> --type merge -p '{"spec":{"terminationPolicy":"Delete"}}'
```

## Common Addon Quick-Start Table

Full field values for the most common addons:

### MySQL (ApeCloud — recommended)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mysql-cluster
  namespace: default
spec:
  clusterDef: apecloud-mysql
  topology: apecloud-mysql
  terminationPolicy: Delete
  componentSpecs:
    - name: mysql
      serviceVersion: "8.0.30"
      replicas: 3
      resources:
        limits:
          cpu: "0.5"
          memory: "0.5Gi"
        requests:
          cpu: "0.5"
          memory: "0.5Gi"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 20Gi
```

### MySQL (Community — replication)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mysql-community
  namespace: default
spec:
  clusterDef: mysql
  topology: mysql-replication
  terminationPolicy: Delete
  componentSpecs:
    - name: mysql
      serviceVersion: "8.0.33"
      replicas: 2
      resources:
        limits:
          cpu: "0.5"
          memory: "0.5Gi"
        requests:
          cpu: "0.5"
          memory: "0.5Gi"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 20Gi
```

### PostgreSQL

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: pg-cluster
  namespace: default
spec:
  clusterDef: postgresql
  topology: postgresql
  terminationPolicy: Delete
  componentSpecs:
    - name: postgresql
      serviceVersion: "14.8.0"
      replicas: 2
      resources:
        limits:
          cpu: "0.5"
          memory: "0.5Gi"
        requests:
          cpu: "0.5"
          memory: "0.5Gi"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 20Gi
```

### Redis (Cluster mode)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: redis-cluster
  namespace: default
spec:
  clusterDef: redis
  topology: redis-cluster
  terminationPolicy: Delete
  componentSpecs:
    - name: redis
      serviceVersion: "7.2.4"
      replicas: 3
      resources:
        limits:
          cpu: "0.5"
          memory: "0.5Gi"
        requests:
          cpu: "0.5"
          memory: "0.5Gi"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 20Gi
```

### Redis (Standalone / Replication)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: redis-standalone
  namespace: default
spec:
  clusterDef: redis
  topology: redis
  terminationPolicy: Delete
  componentSpecs:
    - name: redis
      serviceVersion: "7.2.4"
      replicas: 2
      resources:
        limits:
          cpu: "0.5"
          memory: "0.5Gi"
        requests:
          cpu: "0.5"
          memory: "0.5Gi"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 20Gi
```

### MongoDB (ReplicaSet)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mongo-cluster
  namespace: default
spec:
  clusterDef: mongodb
  topology: mongodb-replicaset
  terminationPolicy: Delete
  componentSpecs:
    - name: mongodb
      serviceVersion: "6.0.16"
      replicas: 3
      resources:
        limits:
          cpu: "0.5"
          memory: "0.5Gi"
        requests:
          cpu: "0.5"
          memory: "0.5Gi"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 20Gi
```

### Kafka (Combined mode)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: kafka-cluster
  namespace: default
spec:
  clusterDef: kafka
  topology: kafka-combined
  terminationPolicy: Delete
  componentSpecs:
    - name: kafka-combine
      serviceVersion: "3.7.2"
      replicas: 3
      resources:
        limits:
          cpu: "0.5"
          memory: "1Gi"
        requests:
          cpu: "0.5"
          memory: "1Gi"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 20Gi
        - name: metadata
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 5Gi
```

## Volume Name Reference

Different addons use different volume names:

| Addon | Volume Names | Description |
|-------|-------------|-------------|
| MySQL | `data` | Data directory |
| PostgreSQL | `data` | Data directory |
| Redis | `data` | Data directory |
| MongoDB | `data` | Data directory |
| Kafka | `data`, `metadata` | Data logs and metadata |

## Listing Available ClusterDefinitions and Topologies

```bash
kubectl get clusterdefinitions

kubectl get clusterdefinitions <name> -o yaml | grep -A 20 'topologies:'
```

## Listing Available Component Versions

```bash
kubectl get componentversions
```

## Documentation Links

- Cluster Management: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/create-and-connect-a-mysql-cluster
- Supported Addons: https://kubeblocks.io/docs/preview/user_docs/overview/supported-addons
- Full Doc Index: https://kubeblocks.io/llms-full.txt

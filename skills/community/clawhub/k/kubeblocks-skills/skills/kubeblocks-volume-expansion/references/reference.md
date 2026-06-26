# Volume Expansion Reference

## Volume Names by Addon

| Addon | Component | Volume Name | Description |
|---|---|---|---|
| MySQL | mysql | `data` | Data directory |
| PostgreSQL | postgresql | `data` | Data directory |
| Redis | redis | `data` | Data directory |
| MongoDB | mongodb | `data` | Data directory |
| Kafka | kafka-combine | `data` | Message data |
| Kafka | kafka-combine | `metadata` | KRaft metadata |
| Kafka | kafka-broker | `data` | Message data |
| Kafka | kafka-broker | `metadata` | KRaft metadata |
| Kafka | kafka-controller | `metadata` | KRaft metadata |
| Elasticsearch | elasticsearch | `data` | Index data |
| Milvus | milvus | `data` | Vector data |
| Qdrant | qdrant | `data` | Vector data |
| RabbitMQ | rabbitmq | `data` | Message data |

## Additional OpsRequest Examples

### Redis Cluster Volume Expansion

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: volumeexpand-redis-cluster
  namespace: default
spec:
  clusterName: redis-cluster
  type: VolumeExpansion
  volumeExpansion:
    - componentName: redis
      volumeClaimTemplates:
        - name: data
          storage: "50Gi"
EOF
```

### MongoDB Volume Expansion

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: volumeexpand-mongo-cluster
  namespace: default
spec:
  clusterName: mongo-cluster
  type: VolumeExpansion
  volumeExpansion:
    - componentName: mongodb
      volumeClaimTemplates:
        - name: data
          storage: "100Gi"
EOF
```

### Elasticsearch Volume Expansion

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: volumeexpand-es-cluster
  namespace: default
spec:
  clusterName: es-cluster
  type: VolumeExpansion
  volumeExpansion:
    - componentName: elasticsearch
      volumeClaimTemplates:
        - name: data
          storage: "200Gi"
EOF
```

### Milvus Volume Expansion

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: volumeexpand-milvus-cluster
  namespace: default
spec:
  clusterName: milvus-cluster
  type: VolumeExpansion
  volumeExpansion:
    - componentName: milvus
      volumeClaimTemplates:
        - name: data
          storage: "100Gi"
EOF
```

## StorageClass Expansion Support

Common StorageClasses and their expansion support:

| Provider | StorageClass | Supports Expansion |
|---|---|---|
| AWS EBS | `gp2`, `gp3` | Yes |
| GCP PD | `standard`, `ssd` | Yes |
| Azure Disk | `managed-premium` | Yes |
| Local Path (Rancher) | `local-path` | No |
| OpenEBS | `openebs-hostpath` | No |
| Ceph RBD | `rook-ceph-block` | Yes |

To enable expansion on a StorageClass that doesn't have it:

```bash
kubectl patch sc <storage-class-name> -p '{"allowVolumeExpansion": true}'
```

Note: this only sets the flag — the underlying storage provisioner must actually support online expansion.

# Task: StatefulSet/DaemonSet Management

## Overview

**StatefulSet**: Manages stateful applications with stable network identities, persistent storage, and ordered deployment/scaling. Ideal for databases, message queues, and distributed storage systems.

**DaemonSet**: Ensures a copy of a Pod runs on every node (or selected nodes). Ideal for node-level agents like logging collectors, monitoring agents, and network proxies.

All commands use `kubectl --kubeconfig=<kubeconfig-file> -n <namespace>` pattern.

## StatefulSet Operations

### Operations Catalog

| Operation ID | Operation Name            | kubectl Command                          | Key Parameters                    |
| ------------ | ------------------------- | ---------------------------------------- | --------------------------------- |
| OP-STS-1     | Create StatefulSet        | `kubectl apply -f`                       | `-f`                              |
| OP-STS-2     | Query StatefulSet Status  | `kubectl get` / `kubectl describe`       | `-o wide`, `-o yaml`              |
| OP-STS-3     | Scale StatefulSet         | `kubectl scale`                          | `--replicas`                      |
| OP-STS-4     | Rollout Update/Undo       | `kubectl rollout`                        | `--image`, `--to-revision`       |
| OP-STS-5     | Delete StatefulSet        | `kubectl delete`                         | `--cascade`                       |

### OP-STS-1: Create StatefulSet

```bash
# Create StatefulSet from YAML manifest
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml apply -f statefulset.yaml -n production
```

Example `statefulset.yaml`:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
spec:
  serviceName: mysql
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        ports:
        - containerPort: 3306
        volumeMounts:
        - name: mysql-data
          mountPath: /var/lib/mysql
  volumeClaimTemplates:
  - metadata:
      name: mysql-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

**Key Differences from Deployment**:
- `serviceName` is required (links to a headless Service)
- `volumeClaimTemplates` creates persistent volumes per Pod
- Pods get stable names: `mysql-0`, `mysql-1`, `mysql-2`
- Pods are created/deleted in ordered sequence

### OP-STS-2: Query StatefulSet Status

```bash
# List all StatefulSets
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get statefulsets -n production

# List with wide output
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get statefulsets -o wide -n production

# Describe a specific StatefulSet
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml describe statefulset mysql -n production

# Check individual Pod status (ordered naming)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get pods -l app=mysql -n production
```

### OP-STS-3: Scale StatefulSet

```bash
# Scale StatefulSet replicas
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml scale statefulset mysql --replicas=5 -n production

# Verify scaling (new pods are created in order: mysql-3, mysql-4)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get pods -l app=mysql -n production
```

**Note**: Scaling down deletes Pods in reverse order (highest index first). PersistentVolumeClaims are NOT automatically deleted when scaling down.

### OP-STS-4: Rollout Update/Undo

```bash
# Update container image (triggers rolling update)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml set image statefulset/mysql mysql=mysql:8.1 -n production

# Monitor rollout progress
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout status statefulset/mysql -n production

# View rollout history
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout history statefulset/mysql -n production

# Rollback to previous revision
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout undo statefulset/mysql -n production

# Rollback to specific revision
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout undo statefulset/mysql --to-revision=1 -n production
```

**StatefulSet Rolling Update Strategy**:
- `OnDelete`: Manual update; new Pod template is applied only when old Pod is deleted
- `RollingUpdate`: Automatic update; Pods are updated in reverse ordinal order (highest index first)
- `Partition` (RollingUpdate): Only update Pods with ordinal >= partition value (useful for canary updates)

### OP-STS-5: Delete StatefulSet

```bash
# Delete StatefulSet (keeps PVCs by default)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml delete statefulset mysql -n production

# Delete StatefulSet and Pods but keep PVCs
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml delete statefulset mysql --cascade=orphan -n production

# Manually delete PVCs after StatefulSet deletion
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml delete pvc mysql-data-mysql-0 mysql-data-mysql-1 mysql-data-mysql-2 -n production
```

**Important**: Deleting a StatefulSet does NOT automatically delete PersistentVolumeClaims. You must manually delete PVCs if you want to reclaim storage.

## DaemonSet Operations

### Operations Catalog

| Operation ID | Operation Name            | kubectl Command                          | Key Parameters                    |
| ------------ | ------------------------- | ---------------------------------------- | --------------------------------- |
| OP-DS-1      | Create DaemonSet          | `kubectl apply -f`                       | `-f`                              |
| OP-DS-2      | Query DaemonSet Status    | `kubectl get` / `kubectl describe`       | `-o wide`, `-o yaml`              |
| OP-DS-3      | Rollout Update/Undo       | `kubectl rollout`                        | `--to-revision`                   |
| OP-DS-4      | Delete DaemonSet          | `kubectl delete`                         | N/A                               |

### OP-DS-1: Create DaemonSet

```bash
# Create DaemonSet from YAML manifest
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml apply -f daemonset.yaml -n production
```

Example `daemonset.yaml`:

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: log-agent
  labels:
    app: log-agent
spec:
  selector:
    matchLabels:
      app: log-agent
  template:
    metadata:
      labels:
        app: log-agent
    spec:
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        effect: NoSchedule
      containers:
      - name: log-agent
        image: fluentd:v1.16
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: containers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: containers
        hostPath:
          path: /var/lib/docker/containers
```

**Key Differences from Deployment**:
- No `replicas` field (runs on every eligible node)
- `tolerations` can be used to run on control-plane nodes
- `nodeSelector` can restrict to specific nodes
- Pods get names based on node name: `log-agent-node-abc`

### OP-DS-2: Query DaemonSet Status

```bash
# List all DaemonSets
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get daemonsets -n production

# List with wide output
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get daemonsets -o wide -n production

# Describe a specific DaemonSet
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml describe daemonset log-agent -n production

# Check DaemonSet Pod distribution across nodes
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get pods -l app=log-agent -o wide -n production
```

### OP-DS-3: Rollout Update/Undo

```bash
# Update container image (triggers rolling update)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml set image daemonset/log-agent log-agent=fluentd:v1.17 -n production

# Monitor rollout progress
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout status daemonset/log-agent -n production

# View rollout history
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout history daemonset/log-agent -n production

# Rollback to previous revision
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout undo daemonset/log-agent -n production

# Rollback to specific revision
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout undo daemonset/log-agent --to-revision=1 -n production
```

**DaemonSet Rolling Update Strategy**:
- `OnDelete`: Manual update; new Pod template applied only when old Pod is deleted
- `RollingUpdate`: Automatic update; `maxUnavailable` controls how many Pods can be updated simultaneously
- Default `maxUnavailable` is 1 (one node at a time)

### OP-DS-4: Delete DaemonSet

```bash
# Delete DaemonSet
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml delete daemonset log-agent -n production
```

**Note**: Deleting a DaemonSet removes all Pods it created on every node.

## Common Scenarios

### StatefulSet for Database Deployment

```bash
# Create headless Service first (required for StatefulSet)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml apply -f headless-service.yaml -n production

# Create StatefulSet
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml apply -f mysql-statefulset.yaml -n production

# Verify stable Pod names
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get pods -l app=mysql -n production

# Connect to a specific Pod instance
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml exec -it mysql-0 -- mysql -u root -p -n production
```

### DaemonSet for Logging Agent

```bash
# Create DaemonSet for node-level logging
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml apply -f fluentd-daemonset.yaml -n production

# Verify Pods are running on all nodes
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get pods -l app=log-agent -o wide -n production

# Check logs from a specific node's agent
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml logs log-agent-node-abc -n production
```

### Partition-Based Canary Update (StatefulSet)

```bash
# Set partition to canary a subset of Pods
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml patch statefulset mysql -p '{"spec":{"updateStrategy":{"rollingUpdate":{"partition":2}}}}' -n production

# Update image (only Pods with ordinal >= 2 will be updated)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml set image statefulset/mysql mysql=mysql:8.1 -n production

# Verify canary Pods are healthy
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get pods mysql-2 mysql-3 -n production

# Remove partition to update all Pods
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml patch statefulset mysql -p '{"spec":{"updateStrategy":{"rollingUpdate":{"partition":0}}}}' -n production
```
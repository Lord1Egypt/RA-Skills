# Task: Deployment Management

## Operations Catalog

| Operation ID | Operation Name            | kubectl Command                          | Key Parameters                    |
| ------------ | ------------------------- | ---------------------------------------- | --------------------------------- |
| OP-DEP-1     | Create Deployment         | `kubectl apply -f` / `kubectl create`   | `-f`, `--image`, `--replicas`     |
| OP-DEP-2     | Query Deployment Status   | `kubectl get` / `kubectl describe`       | `-o wide`, `-o yaml`              |
| OP-DEP-3     | Scale Deployment          | `kubectl scale`                          | `--replicas`                      |
| OP-DEP-4     | Update/Rollout Deployment | `kubectl set image` / `rollout`          | `--image`, `--revision`           |
| OP-DEP-5     | Rollback Deployment       | `kubectl rollout undo`                  | `--to-revision`                   |
| OP-DEP-6     | Delete Deployment         | `kubectl delete`                         | `--grace-period`, `--force`       |

All commands use `kubectl --kubeconfig=<kubeconfig-file> -n <namespace>` pattern.

## W1: Create Deployment

### From YAML File (Recommended)

```bash
# Create Deployment from YAML manifest
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml apply -f deployment.yaml -n production
```

Example `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: myapp:v1
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
```

### Inline Creation (Quick Testing)

```bash
# Create Deployment inline (minimal, for quick testing only)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml create deployment my-app --image=myapp:v1 --replicas=3 -n production
```

**Recommendation**: Use YAML files for production deployments. Inline creation is acceptable for quick testing only.

## W2: Query Deployment Status

### Basic Query

```bash
# List all Deployments in namespace
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get deployments -n production

# List with wide output (shows strategy, image, selectors)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get deployments -o wide -n production
```

### Detailed Query

```bash
# Describe a specific Deployment (events, strategy, pod template)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml describe deployment my-app -n production
```

### Export Format

```bash
# Export Deployment spec as YAML
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get deployment my-app -o yaml -n production

# Export Deployment spec as JSON
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get deployment my-app -o json -n production
```

### Key Status Fields

| Field             | Description                              | Healthy Value              |
| ----------------- | ---------------------------------------- | -------------------------- |
| `READY`           | Ready replicas / desired replicas        | 3/3                        |
| `UP-TO-DATE`      | Updated replicas count                   | Equals desired             |
| `AVAILABLE`       | Available replicas count                 | Equals desired             |
| `Conditions`      | Deployment progress conditions           | `Progressing=True`, `Available=True` |

## W3: Scale Deployment

```bash
# Scale Deployment to specific replica count
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml scale deployment my-app --replicas=5 -n production

# Verify scaling
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get deployment my-app -n production
```

## W4: Update/Rollout Deployment

### Rolling Update (Image Change)

```bash
# Update container image (triggers rolling update)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml set image deployment/my-app my-app=myapp:v2 -n production

# Monitor rollout progress
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout status deployment/my-app -n production
```

### Rollout History

```bash
# View rollout history
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout history deployment/my-app -n production

# View details of a specific revision
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout history deployment/my-app --revision=2 -n production
```

### Rollback

```bash
# Rollback to previous revision
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout undo deployment/my-app -n production

# Rollback to specific revision
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout undo deployment/my-app --to-revision=1 -n production

# Verify rollback
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout status deployment/my-app -n production
```

### Pause/Resume Rollout

```bash
# Pause rollout (for canary updates)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout pause deployment/my-app -n production

# Resume rollout
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout resume deployment/my-app -n production
```

## W5: Delete Deployment

```bash
# Delete a Deployment
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml delete deployment my-app -n production

# Force delete (use with caution)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml delete deployment my-app --grace-period=0 --force -n production
```

**Warning**: Deleting a Deployment also deletes all its Pods. Ensure you have a backup or YAML manifest if you need to recreate it.

## Common Scenarios

### Quick Deploy for Testing

```bash
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml create deployment test-app --image=nginx:latest --replicas=1 -n staging
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml expose deployment test-app --port=80 --target-port=80 --name=test-app-svc -n staging
```

### Canary Rollout

```bash
# Update and pause for canary testing
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml set image deployment/my-app my-app=myapp:v2 -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout pause deployment/my-app -n production

# Verify canary pods are healthy
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get pods -l app=my-app -n production

# Resume rollout if canary is good
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout resume deployment/my-app -n production

# Or rollback if canary has issues
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout undo deployment/my-app -n production
```

### Emergency Rollback

```bash
# Immediate rollback to last known good revision
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout undo deployment/my-app -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout status deployment/my-app -n production
```
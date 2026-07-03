# HPA Autoscaling

## Overview

Horizontal Pod Autoscaler (HPA) automatically scales Deployment replicas based on CPU, memory, or custom metrics. It observes resource utilization and adjusts pod count within configured min/max bounds.

## Operations

| Operation | Command |
|-----------|---------|
| Create | `kubectl --kubeconfig=<kubeconfig-path> autoscale deployment <name> --min=2 --max=10 --cpu=80% -n <namespace>` |
| Get | `kubectl --kubeconfig=<kubeconfig-path> get hpa -n <namespace>` |
| Describe | `kubectl --kubeconfig=<kubeconfig-path> describe hpa <name> -n <namespace>` |
| Update min/max | `kubectl --kubeconfig=<kubeconfig-path> patch hpa <name> --type merge --patch-file=patch.json -n <namespace>` |
| Delete | `kubectl --kubeconfig=<kubeconfig-path> delete hpa <name> -n <namespace>` |

## Common Scenarios

### Auto-scale production deployment

> **Note**: `--cpu-percent` is deprecated in newer kubectl versions. Use `--cpu` with percentage format instead (e.g., `--cpu=80%`).

```bash
kubectl --kubeconfig=<kubeconfig-path> autoscale deployment api-server --min=2 --max=10 --cpu=80% -n production
kubectl --kubeconfig=<kubeconfig-path> get hpa -n production
```

### Adjust thresholds

> **Note**: On Windows (PowerShell), inline `-p` JSON patches have escaping issues. Use `--patch-file` instead.

Create patch file:

```bash
# patch.json
echo '{"spec":{"maxReplicas":20,"minReplicas":3}}' > patch.json
```

Apply patch:

```bash
kubectl --kubeconfig=<kubeconfig-path> patch hpa api-server --type merge --patch-file=patch.json -n production
kubectl --kubeconfig=<kubeconfig-path> describe hpa api-server -n production
```

### Monitor scaling events

```bash
kubectl --kubeconfig=<kubeconfig-path> get hpa -n <namespace> -w
kubectl --kubeconfig=<kubeconfig-path> get events -n <namespace> --field-selector reason=SuccessfulRescale
```

### HPA from YAML with custom metrics

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-server
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-server
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 70
```

```bash
kubectl --kubeconfig=<kubeconfig-path> apply -f hpa.yaml -n <namespace>
```
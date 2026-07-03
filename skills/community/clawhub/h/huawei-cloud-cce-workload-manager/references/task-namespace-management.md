# Task: Namespace Management

## Overview

Kubernetes namespaces provide the organizational foundation for all resources in a cluster. Namespaces isolate resources, enable multi-tenant environments, and serve as scope boundaries for RBAC policies, resource quotas, and network policies. This task covers creating, listing, describing, and deleting namespaces in CCE clusters.

## Operations Catalog

| Operation          | Method | Description              | Key Parameters                    |
| ------------------ | ------ | ------------------------ | --------------------------------- |
| `create namespace` | POST   | 创建命名空间             | `<name>` (required)              |
| `get namespaces`   | GET    | 列出命名空间列表         | (none)                           |
| `describe namespace` | GET  | 获取命名空间详情         | `<name>` (required)              |
| `delete namespace` | DELETE | 删除命名空间             | `<name>` (required, CAUTION)     |

## Workflows

### W1: Create a Namespace

```bash
kubectl --kubeconfig=<kubeconfig-file> create namespace <name>
```

**Examples**:

```bash
kubectl --kubeconfig=my-kubeconfig.yaml create namespace production

kubectl --kubeconfig=my-kubeconfig.yaml create namespace staging

kubectl --kubeconfig=my-kubeconfig.yaml create namespace development
```

**Post-creation Verification**:

```bash
kubectl --kubeconfig=<kubeconfig-file> get namespace <name>
```

Expected: Namespace appears in list with `Active` status.

### W2: List Namespaces

```bash
kubectl --kubeconfig=<kubeconfig-file> get namespaces
```

With additional detail:

```bash
kubectl --kubeconfig=<kubeconfig-file> get namespaces -o wide

kubectl --kubeconfig=<kubeconfig-file> get namespaces -o yaml
```

**Response Fields**:
- `NAME`: Namespace name
- `STATUS`: Current status (`Active` or `Terminating`)
- `AGE`: Time since creation

### W3: Describe a Namespace

```bash
kubectl --kubeconfig=<kubeconfig-file> describe namespace <name>
```

**Response Fields**:
- `Name`: Namespace name
- `Labels`: Key-value labels on the namespace
- `Annotations`: Key-value annotations on the namespace
- `Status`: Current phase (`Active` or `Terminating`)
- `Resource Quotas`: Applied resource limits (CPU, memory, pod count, etc.)
- `Limit Ranges`: Default and limit constraints for containers

### W4: Delete a Namespace

⚠️ **CAUTION**: Deleting a namespace deletes ALL resources within it (deployments, pods, services, configmaps, secrets, PVCs, etc.). This is irreversible. Always confirm with the user before deletion.

**Pre-deletion Checklist**:
1. List all resources in the namespace to verify what will be deleted
2. Confirm with the user that deletion is intended

```bash
kubectl --kubeconfig=<kubeconfig-file> get all -n <name>

kubectl --kubeconfig=<kubeconfig-file> delete namespace <name>
```

**Post-deletion Verification**:

```bash
kubectl --kubeconfig=<kubeconfig-file> get namespace <name>
```

Expected: Namespace not found error, or namespace shows `Terminating` status during graceful shutdown.

## Namespace Best Practices

- Always specify `-n <namespace>` when running kubectl commands — the default namespace may be empty or contain unrelated resources
- Use per-environment namespaces (e.g., `prod`, `staging`, `dev`) to isolate deployments
- Never delete a namespace without explicit user confirmation — all resources within it are permanently removed
- Apply resource quotas to prevent any single namespace from consuming excessive cluster resources
- Use labels on namespaces for organizational grouping (e.g., `env: production`, `team: backend`)
- Avoid using the `default` namespace for production workloads

## Common Scenarios

### S1: Create Environment Namespaces

```bash
kubectl --kubeconfig=my-kubeconfig.yaml create namespace prod

kubectl --kubeconfig=my-kubeconfig.yaml create namespace staging

kubectl --kubeconfig=my-kubeconfig.yaml create namespace dev
```

### S2: Verify Namespace Exists Before Deployment

```bash
kubectl --kubeconfig=my-kubeconfig.yaml get namespace prod
```

If the namespace does not exist, create it first:

```bash
kubectl --kubeconfig=my-kubeconfig.yaml create namespace prod
```

Then deploy resources:

```bash
kubectl --kubeconfig=my-kubeconfig.yaml apply -f deployment.yaml -n prod
```

### S3: Clean Up Test Namespace

Before deletion, review resources:

```bash
kubectl --kubeconfig=my-kubeconfig.yaml get all,configmaps,secrets,pvc -n test-env
```

After confirming with the user:

```bash
kubectl --kubeconfig=my-kubeconfig.yaml delete namespace test-env
```
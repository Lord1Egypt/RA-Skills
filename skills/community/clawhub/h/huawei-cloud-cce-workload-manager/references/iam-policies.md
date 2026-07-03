# IAM Permission Policies - CCE Workload Manager Skill

## Overview

CCE workload management uses a two-layer permission model: Huawei Cloud IAM controls access to kubeconfig generation (hcloud CLI), and Kubernetes RBAC controls what operations can be performed with kubectl after kubeconfig is obtained. Both layers must be configured correctly for the skill to function.

## Huawei Cloud IAM Read-Only Operations

| API Action                 | Permission        | Purpose                                |
| -------------------------- | ----------------- | -------------------------------------- |
| `cce:cluster:get`          | Get cluster       | View CCE cluster details               |
| `cce:cluster:list`         | List clusters     | List CCE clusters to find cluster_id   |
| `ucs:cluster:get`          | Get UCS cluster   | View UCS-managed cluster details       |
| `ucs:quota:get`            | Get quota         | Check UCS resource quotas              |

## Huawei Cloud IAM Write Operations (Require Additional Authorization)

| API Action                 | Permission        | Purpose                                |
| -------------------------- | ----------------- | -------------------------------------- |
| `cce:cert:create`          | Create cert       | Obtain CCE cluster kubeconfig          |
| `ucs:kubeconfig:create`    | Create kubeconfig | Obtain UCS-managed cluster kubeconfig  |
| `ucs:federationKubeconfig:get` | Get federation | Download federation kubeconfig     |

## Minimum Read-Only Policy (JSON)

This policy allows obtaining kubeconfig but kubectl operations will be limited to read-only based on Kubernetes RBAC:

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cce:cluster:get",
        "cce:cluster:list",
        "ucs:cluster:get",
        "ucs:quota:get",
        "cce:cert:create",
        "ucs:kubeconfig:create",
        "ucs:federationKubeconfig:get"
      ],
      "Resource": ["*"]
    }
  ]
}
```

⚠️ **Note**: This policy grants IAM permission to obtain kubeconfig, but actual kubectl permissions depend on Kubernetes RBAC. With default RBAC, a read-only IAM policy results in read-only kubectl access.

## Full Management Policy (JSON)

This policy grants IAM permission to obtain kubeconfig with write-capable RBAC:

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cce:cluster:get",
        "cce:cluster:list",
        "cce:cert:create",
        "ucs:cluster:get",
        "ucs:kubeconfig:create",
        "ucs:federationKubeconfig:get",
        "ucs:quota:get"
      ],
      "Resource": ["*"]
    }
  ]
}
```

⚠️ **Note**: Full management kubectl capabilities require corresponding Kubernetes RBAC bindings (e.g., cluster-admin or admin role). IAM policy alone does not grant kubectl write permissions.

## Kubernetes RBAC

### Common Roles

| Role            | Scope    | Description                                      |
| --------------- | -------- | ------------------------------------------------ |
| `cluster-admin` | Cluster  | Full control over all resources in all namespaces |
| `admin`         | Namespace | Full control over resources in the namespace    |
| `edit`          | Namespace | Read and write resources in the namespace       |
| `view`          | Namespace | Read-only access to resources in the namespace  |

### Namespace-Scoped vs Cluster-Scoped

- **Namespace-scoped roles** (admin, edit, view): Apply only within a specific namespace. Use `RoleBinding` to assign.
- **Cluster-scoped roles** (cluster-admin): Apply across all namespaces. Use `ClusterRoleBinding` to assign.

### How to Check Permissions

```bash
kubectl --kubeconfig=<f> auth can-i <verb> <resource> -n <namespace>

kubectl --kubeconfig=<f> auth can-i create deployments -n prod

kubectl --kubeconfig=<f> auth can-i delete pods -n staging

kubectl --kubeconfig=<f> auth can-i list secrets -n prod

kubectl --kubeconfig=<f> auth can-i get nodes
```

### Example RBAC Binding Commands

Grant admin access in a specific namespace:

```bash
kubectl --kubeconfig=<f> create rolebinding dev-admin --clusterrole=admin --user=<user> -n development
```

Grant view access across all namespaces:

```bash
kubectl --kubeconfig=<f> create clusterrolebinding dev-viewer --clusterrole=view --user=<user>
```

Grant cluster-admin access:

```bash
kubectl --kubeconfig=<f> create clusterrolebinding ops-admin --clusterrole=cluster-admin --user=<user>
```

### Default Roles and Their Permissions

| Role            | Create | Read | Update | Delete | Namespace Scope |
| --------------- | ------ | ---- | ------ | ------ | --------------- |
| `cluster-admin` | ✅     | ✅   | ✅     | ✅     | All namespaces  |
| `admin`         | ✅     | ✅   | ✅     | ✅     | Single namespace|
| `edit`          | ✅     | ✅   | ✅     | ❌     | Single namespace|
| `view`          | ❌     | ✅   | ❌     | ❌     | Single namespace|

## Permission Assignment Steps

1. **Huawei Cloud IAM**:
   1. Log in to Huawei Cloud IAM console: https://console.huaweicloud.com/iam/
   2. Navigate to **Policies** → **Create Custom Policy**
   3. Choose **JSON** mode and paste the policy JSON from this document
   4. Navigate to **Users** / **User Groups** → **Authorize**
   5. Select the custom policy and confirm

2. **Kubernetes RBAC**:
   1. Obtain kubeconfig via hcloud CLI
   2. Check current permissions with `kubectl auth can-i`
   3. Create RoleBinding or ClusterRoleBinding as needed
   4. Verify permissions with `kubectl auth can-i` again

## Permission Failure Handling

When a command fails with a permission error:

1. Determine which layer failed:
   - **IAM error** (hcloud CLI): `403 Permission denied`, `CCE.004`, `UCS.004` → Read this document, display IAM policy JSON, guide user to create custom policy in IAM console, pause and wait for confirmation
   - **RBAC error** (kubectl): `Forbidden`, `Error from server (Forbidden)` → Check with `kubectl auth can-i`, display required RBAC role, create appropriate RoleBinding or ClusterRoleBinding
2. Display the required permission list and policy JSON to the user
3. Guide the user to create a custom policy in the IAM console or RBAC binding via kubectl
4. Pause execution and wait for user confirmation that permissions have been granted
5. Retry the failed command
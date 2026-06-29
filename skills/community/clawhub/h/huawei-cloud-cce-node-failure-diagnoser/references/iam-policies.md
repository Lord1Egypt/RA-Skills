# IAM Permission Policies - CCE Node Failure Diagnoser Skill

## Overview

This document declares the IAM permissions required by the Huawei Cloud CCE Node Failure Diagnoser skill. All permissions follow the principle of least privilege — this skill is read-only diagnosis only and does not require any write permissions.

## Read-Only Permissions (Required)

| API Action | Service | Purpose |
|------------|---------|---------|
| `cce:cluster:get` | CCE | View cluster details |
| `cce:node:list` | CCE | List cluster nodes |
| `cce:node:get` | CCE | View node details |
| `aom:metric:get` | AOM | Query node and pod metrics |
| `ces:alarm:list` | CES | List alarm events |
| `hss:host:list` | HSS | List host security status |
| `hss:vul:list` | HSS | List host vulnerabilities |
| `vpc:securityGroup:list` | VPC | List security groups |
| `vpc:acl:list` | VPC | List network ACLs |
| `iam:project:get` | IAM | Get project ID (auto-obtained) |

## Kubernetes API Permissions (Required)

The dispatcher obtains a kubeconfig from CCE and uses Kubernetes API. The kubeconfig user must have the following RBAC permissions:

| Kubernetes Resource | Verb | Purpose |
|--------------------|------|---------|
| `nodes` | `get`, `list` | Query node status and conditions |
| `nodes/status` | `get` | Read node status subresource |
| `pods` | `get`, `list` | Query pod status on node |
| `events` | `get`, `list` | Query node and pod events |
| `leases` | `get`, `list` | Query kube-node-lease objects |

## Minimum Read-Only Policy (JSON)

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cce:cluster:get",
        "cce:node:list",
        "cce:node:get",
        "aom:metric:get",
        "ces:alarm:list",
        "hss:host:list",
        "hss:vul:list",
        "vpc:securityGroup:list",
        "vpc:acl:list",
        "iam:project:get"
      ],
      "Resource": ["*"]
    }
  ]
}
```

## Minimum Kubernetes RBAC Policy (YAML)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cce-node-diagnosis-reader
rules:
- apiGroups: [""]
  resources: ["nodes", "nodes/status", "pods", "pods/status", "events"]
  verbs: ["get", "list"]
- apiGroups: ["coordination.k8s.io"]
  resources: ["leases"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cce-node-diagnosis-reader-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cce-node-diagnosis-reader
subjects:
- kind: User
  name: <kubeconfig-user>
```

## Two-Layer Permission Model

1. **Huawei Cloud IAM**: Controls access to CCE cluster details, AOM metrics, CES alarms, HSS data, VPC security groups, and project information.
2. **Kubernetes RBAC**: Controls access to node status, pod status, events, and lease objects within the cluster after kubeconfig is obtained.

Both layers must be configured for the skill to function correctly.

## Permission Failure Handling

When an action fails with a permission error:

1. Determine which layer failed (IAM or RBAC)
2. For IAM errors: display the Huawei Cloud IAM policy JSON and guide the user to create a custom policy
3. For RBAC errors: display the Kubernetes RBAC YAML and guide the user to apply ClusterRole/ClusterRoleBinding
4. Pause execution and wait for user confirmation that permissions have been granted
5. Retry the failed action

## Permission Assignment Steps

### Huawei Cloud IAM Policy

1. Log in to Huawei Cloud IAM console: https://console.huaweicloud.com/iam/
2. Navigate to **Policies** → **Create Custom Policy**
3. Choose **JSON** mode and paste the policy JSON above
4. Navigate to **Users** / **User Groups** → **Authorize**
5. Select the custom policy and confirm

### Kubernetes RBAC Policy

1. Obtain kubeconfig for the cluster
2. Apply ClusterRole and ClusterRoleBinding YAML:
   ```bash
   kubectl apply -f clusterrole.yaml
   ```
3. Verify permissions:
   ```bash
   kubectl auth can-i get nodes --as=<kubeconfig-user>
   kubectl auth can-i list pods --as=<kubeconfig-user>
   ```
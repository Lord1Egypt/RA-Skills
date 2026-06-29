# IAM Permission Policies - CCE Network Failure Diagnoser

## Overview

This document declares the IAM permissions required by the CCE Network Failure Diagnoser skill. All permissions follow the principle of least privilege — this skill only requires read-only access.

## Read-Only Permissions (Required)

| API Action | Permission | Purpose |
|------------|------------|---------|
| `cce:cluster:get` | Get cluster | View cluster details, obtain kubeconfig for diagnosis |
| `cce:node:list` | List nodes | Query cluster node status and conditions |
| `cce:pod:list` | List pods | Query Pod status, labels, conditions for diagnosis |
| `cce:addon:get` | Get addon | View CoreDNS/Ingress controller addon configuration |
| `elb:loadbalancer:list` | List ELB | Query ELB load balancer details |
| `elb:listener:list` | List ELB listeners | Query ELB listener configuration |
| `elb:pool:list` | List ELB pools | Query ELB backend pool configuration |
| `elb:healthmonitor:list` | List health monitors | Query ELB health check status |
| `elb:member:list` | List ELB members | Query ELB backend member health status |
| `eip:list` | List EIP | Query Elastic IP addresses |
| `eip:get` | Get EIP | View EIP details |
| `nat:list` | List NAT gateways | Query NAT gateway configuration |
| `nat:get` | Get NAT gateway | View NAT gateway details |
| `vpc:securityGroup:list` | List security groups | Query VPC security group rules |
| `vpc:securityGroup:get` | Get security group | View security group rule details |
| `vpc:firewall:list` | List VPC ACLs | Query VPC ACL rules |
| `vpc:firewall:get` | Get VPC ACL | View VPC ACL rule details |
| `ces:metricData:list` | List metrics | Query ELB/EIP/NAT monitoring metrics |
| `lts:log:list` | List LTS logs | Query CoreDNS/Ingress controller logs via LTS |

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
        "cce:pod:list",
        "cce:addon:get",
        "elb:loadbalancer:list",
        "elb:listener:list",
        "elb:pool:list",
        "elb:healthmonitor:list",
        "elb:member:list",
        "eip:list",
        "eip:get",
        "nat:list",
        "nat:get",
        "vpc:securityGroup:list",
        "vpc:securityGroup:get",
        "vpc:firewall:list",
        "vpc:firewall:get",
        "ces:metricData:list",
        "lts:log:list"
      ],
      "Resource": ["*"]
    }
  ]
}
```

## Permission Assignment Steps

1. Log in to Huawei Cloud IAM console: https://console.huaweicloud.com/iam/
2. Navigate to **Policies** → **Create Custom Policy**
3. Choose **JSON** mode and paste the policy JSON above
4. Navigate to **Users** / **User Groups** → **Authorize**
5. Select the custom policy and confirm

## Permission Failure Handling

When a diagnosis command fails with a permission error:

1. Read this document (`references/iam-policies.md`)
2. Display the required permission list and policy JSON to the user
3. Guide the user to create a custom policy in the IAM console
4. Pause execution and wait for user confirmation that permissions have been granted
5. Retry the failed diagnosis command

## Two-Layer Permission Model

This skill operates with a two-layer permission model:

1. **Huawei Cloud IAM**: Controls access to cloud-side resources (ELB, EIP, NAT, VPC, security groups, ACLs) and CCE cluster information
2. **Kubernetes RBAC**: Controls access to K8s objects within the cluster (Services, Pods, Ingresses, NetworkPolicies, EndpointSlices)

When K8s-side permission errors occur (e.g., cannot list Services or NetworkPolicies), the cluster administrator must configure appropriate RBAC roles. The script auto-obtains kubeconfig from CCE API, so IAM permissions for kubeconfig acquisition are included in the policy above.
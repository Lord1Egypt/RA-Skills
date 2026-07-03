---
id: huawei-cloud-cce-workload-manager
name: huawei-cloud-cce-workload-manager
description: |
  Huawei Cloud CCE/UCS workload lifecycle management skill using hcloud CLI for kubeconfig acquisition and kubectl for Kubernetes resource operations.
  Use this skill when the user wants to: (1) obtain kubeconfig for CCE clusters, (2) obtain federation kubeconfig for UCS fleet (multi-cluster operations), (3) manage Deployment/StatefulSet/DaemonSet/Job/CronJob lifecycle, (4) configure HPA autoscaling, (5) manage Service/Ingress/ConfigMap/Secret/PVC, (6) observe Pod status/logs/events, (7) manage namespaces, (8) install and configure kubectl.
  Trigger: user mentions "CCE workload", "k8s workload", "UCS fleet workload", "Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob", "HPA", "kubectl", "kubeconfig", "federation kubeconfig", "Pod logs", "CCE 负载", "UCS 联邦负载", "工作负载", "部署", "有状态副本集", "守护进程集", "任务", "定时任务", "弹性伸缩", "服务", "路由", "配置项", "密钥", "存储卷", "Pod 日志", "命名空间"
tags: [cce, kubernetes, workload, kubeconfig, kubectl]
---

# Huawei Cloud CCE/UCS Workload Manager

## Overview

This skill provides workload lifecycle management capabilities for Huawei Cloud CCE and UCS-managed Kubernetes clusters using `hcloud` CLI for kubeconfig acquisition and `kubectl` for Kubernetes resource operations.

**Architecture**: hcloud CLI → kubeconfig YAML → kubectl --kubeconfig → k8s resources (Deployment/StatefulSet/DaemonSet/Job/CronJob/Service/Ingress/ConfigMap/Secret/PVC)

**Related Skills**:
- `cce-cluster-management` - CCE cluster infrastructure creation, scaling, and deletion
- `ucs-cluster-onboarding-manager` - UCS cluster onboarding, lifecycle, and fleet grouping
- `ucs-policy-governor` - UCS policy governance, compliance, and audit management

**Capabilities**:
- Obtain kubeconfig for CCE clusters (direct cluster access)
- Obtain federation kubeconfig for UCS fleet (multi-cluster fleet operations)
- Manage Deployment/StatefulSet/DaemonSet lifecycle (create, query, scale, update, delete)
- Manage Job/CronJob lifecycle (create, query, suspend, resume, delete)
- Configure HPA autoscaling for Deployments and StatefulSets
- Manage Service/Ingress networking, ConfigMap/Secret configuration, PVC storage
- Observe Pod status, logs, and events
- Manage namespaces
- Install and configure kubectl

**Typical Use Cases**:

- "Get kubeconfig for my CCE cluster"
- "Deploy an application to CCE"
- "Scale my Deployment to 5 replicas"
- "Roll back a Deployment update"
- "Create a StatefulSet for my database"
- "Deploy a logging agent as DaemonSet"
- "Create a CronJob for scheduled tasks"
- "Set up HPA for auto-scaling"
- "Check Pod logs for debugging"
- "Create a Service and Ingress for my app"
- "Manage ConfigMaps and Secrets"
- "Create a PersistentVolumeClaim"
- "List namespaces in my cluster"
- "Install kubectl on my machine"

## Prerequisites

### 1. hcloud CLI Requirements (MANDATORY)

- hcloud CLI installed (version >= 7.2.2)
- Run `hcloud version` to verify installation
- First-time usage: `printf "y\n" | hcloud version` to accept privacy statement

### 2. kubectl Requirements (MANDATORY)

- kubectl installed (version compatible with cluster Kubernetes version)
- See [Task: kubectl Setup](references/task-kubectl-setup.md) for installation guidance
- Run `kubectl version --client` to verify installation

### 3. Credential Configuration

- Valid Huawei Cloud credentials (AK/SK mode)
- **Security Rules**:
  - 🚫 Never expose AK/SK values in code, conversation, or commands
  - 🚫 Never use `echo $HUAWEI_CLOUD_AK` or `echo $HUAWEI_CLOUD_SK` to check credentials
  - ✅ Use environment variables: `HUAWEI_CLOUD_AK`, `HUAWEI_CLOUD_SK`, `HUAWEI_CLOUD_REGION`
  - ✅ Prefer IAM users over root account for cloud operations
  - ✅ Enable MFA for sensitive operations

**Configuration Method** (Environment Variables Only):

```bash
export HUAWEI_CLOUD_AK=<your-ak>
export HUAWEI_CLOUD_SK=<your-sk>
export HUAWEI_CLOUD_REGION=cn-north-4
```

**⚠️ Important Security Notes**:

- Never commit credentials to version control
- Use IAM users with minimal required permissions
- Enable MFA for sensitive operations
- Rotate AK/SK regularly

### 4. IAM Permission Requirements

| API Action                        | Permission          | Purpose                                    |
| --------------------------------- | ------------------- | ------------------------------------------ |
| `cce:cluster:get`                 | Get cluster         | View cluster details                       |
| `cce:cluster:createCert`          | Create certificate  | Obtain CCE cluster kubeconfig              |
| `ucs:kubeconfig:create`           | Create kubeconfig   | Obtain UCS cluster kubeconfig              |
| `ucs:federationKubeconfig:get`    | Get federation      | Download UCS federation kubeconfig         |

**Two-Layer Permission Model**:

1. **Huawei Cloud IAM**: Controls kubeconfig acquisition via `hcloud` CLI (who can get a kubeconfig for CCE or UCS fleet)
2. **Kubernetes RBAC**: Controls kubectl operations after kubeconfig is obtained (what the user can do in the cluster or fleet)

**Permission Failure Handling**:

1. When hcloud commands fail due to IAM permission errors, verify the IAM permissions listed above
2. When kubectl commands fail due to RBAC permission errors, the cluster administrator must configure appropriate RBAC roles
3. Guide the user to create custom policies in the IAM console for Huawei Cloud permissions
4. Guide the user to create ClusterRole/Role bindings for Kubernetes RBAC permissions
5. Pause execution and wait for user confirmation that permissions have been granted

## Core Commands

### 1. Kubeconfig Acquisition

See [Task: Kubeconfig Acquisition](references/task-kubeconfig-acquisition.md) for detailed workflows.

```bash
# CCE cluster kubeconfig (duration in days, 1-1827)
hcloud CCE CreateKubernetesClusterCert --cluster_id=<cce-cluster-id> --duration=1 --cli-region=cn-north-4

# UCS federation kubeconfig (duration in days, 1-1825)
# Used for multi-cluster fleet operations via UCS
hcloud UCS DownloadFederationKubeconfig --clustergroupid=<fleet-id> --duration=1 --cli-region=cn-north-4
```

**Save kubeconfig and verify**:

```bash
# Save CCE kubeconfig to file
hcloud CCE CreateKubernetesClusterCert --cluster_id=<cce-cluster-id> --duration=1 --cli-region=cn-north-4 > ~/.kube/cce-kubeconfig.yaml

# Verify connection
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml cluster-info
```

**Key Parameter Differences**:
- CCE uses `--cluster_id` (with underscore) for cluster ID
- UCS uses `--clusterid` (no underscore) for cluster ID
- CCE `CreateKubernetesClusterCert` `--duration` is in **days** (1-1827)
- UCS `DownloadFederationKubeconfig` `--duration` is in **days** (1-1825)

### 2. Workload Management (Deployment/StatefulSet/DaemonSet)

See [Task: Deployment Management](references/task-deployment-management.md) and [Task: StatefulSet/DaemonSet Management](references/task-statefulset-daemonset-management.md) for detailed workflows.

All commands use `kubectl --kubeconfig=<kubeconfig-file> -n <namespace>` pattern.

```bash
# Create Deployment from YAML file
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml apply -f deployment.yaml -n production

# Create Deployment inline
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml create deployment my-app --image=myapp:v1 --replicas=3 -n production

# Query Deployment status
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get deployments -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml describe deployment my-app -n production

# Scale Deployment
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml scale deployment my-app --replicas=5 -n production

# Update Deployment (rolling update)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml set image deployment/my-app my-app=myapp:v2 -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout status deployment/my-app -n production

# Rollback Deployment
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout undo deployment/my-app -n production

# Delete Deployment
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml delete deployment my-app -n production

# StatefulSet operations (same pattern)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml apply -f statefulset.yaml -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml scale statefulset my-db --replicas=3 -n production

# DaemonSet operations (same pattern)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml apply -f daemonset.yaml -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout status daemonset/log-agent -n production
```

### 3. Job/CronJob Management

```bash
# Create Job from YAML
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml apply -f job.yaml -n production

# Create Job inline
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml create job data-migration --image=migrator:v1 -n production

# Query Job status
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get jobs -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml describe job data-migration -n production

# Delete Job
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml delete job data-migration -n production

# Create CronJob from YAML
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml apply -f cronjob.yaml -n production

# Create CronJob inline
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml create cronjob nightly-backup --image=backup:v1 --schedule="0 2 * * *" -n production

# Suspend CronJob
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml patch cronjob nightly-backup --type merge --patch-file=suspend.json -n production

# Resume CronJob
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml patch cronjob nightly-backup --type merge --patch-file=resume.json -n production

# Delete CronJob
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml delete cronjob nightly-backup -n production
```

### 4. Observability + Config

```bash
# Pod status
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get pods -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get pods -o wide -n production

# Pod logs
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml logs my-app-pod -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml logs my-app-pod --tail=100 -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml logs my-app-pod -f -n production

# Pod events
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml describe pod my-app-pod -n production

# Namespace management
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get namespaces
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml create namespace staging
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml delete namespace staging

# Service
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml apply -f service.yaml -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get services -n production

# Ingress
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml apply -f ingress.yaml -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get ingress -n production

# ConfigMap
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml create configmap app-config --from-literal=key1=value1 -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get configmaps -n production

# Secret
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml create secret generic db-secret --from-literal=password=s3cret -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get secrets -n production

# PVC
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml apply -f pvc.yaml -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get pvc -n production

# HPA autoscaling
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml autoscale deployment my-app --min=2 --max=10 --cpu=80% -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get hpa -n production
```

### 5. kubectl Installation & Configuration

See [Task: kubectl Setup](references/task-kubectl-setup.md) for detailed installation and configuration guidance.

## Parameter Reference

### hcloud Parameters (Kubeconfig Acquisition)

| Parameter          | Command             | Required | Description                   | Constraints                                  |
| ------------------ | ------------------- | -------- | ----------------------------- | -------------------------------------------- |
| `--cluster_id`     | CCE CreateCert      | Yes      | CCE cluster ID                | Must reference existing CCE cluster          |
| `--clustergroupid` | UCS DownloadFederation | Yes   | Fleet group ID                | Must reference existing fleet group          |
| `--duration`       | CCE CreateCert      | Yes*     | Certificate validity in days  | 1-1827 days; at least one of --duration/--expire_at required |
| `--expire_at`      | CCE CreateCert      | Yes*     | Certificate expiry timestamp  | ISO format; mutually exclusive with --duration |
| `--duration`       | UCS DownloadFederation | Yes   | Token validity in days (1-1825)  | Integer (1-1825)                            |
| `--project_id`     | CCE CreateCert      | Required (auto-filled) | Project ID    | Auto-filled from hcloud config if not specified |
| `--cli-region`     | All hcloud commands | Required | Huawei Cloud region ID        | Config value or `HUAWEI_CLOUD_REGION`        |

### kubectl Flags

| Flag             | Description                        | Example                                     |
| ---------------- | ---------------------------------- | ------------------------------------------- |
| `--kubeconfig`   | Path to kubeconfig file            | `--kubeconfig=~/.kube/cce-kubeconfig.yaml`  |
| `-n`             | Namespace for the operation        | `-n production`                             |
| `-o`             | Output format (wide/yaml/json)     | `-o wide`, `-o yaml`, `-o json`             |
| `-f`             | YAML/JSON file path                | `-f deployment.yaml`                        |
| `--replicas`     | Number of replicas for scaling     | `--replicas=5`                              |
| `--image`        | Container image for create/set     | `--image=myapp:v1`                          |
| `--tail`         | Number of log lines to show        | `--tail=100`                                |
| `-f` (logs)      | Follow log output (stream)         | `logs -f`                                   |
| `--min/--max`    | HPA min/max replicas               | `--min=2 --max=10`                          |
| `--cpu-percent`  | HPA CPU target percentage          | `--cpu-percent=80`                          |

## Output Format

### CCE CreateKubernetesClusterCert (Kubeconfig YAML)

Returns a standard Kubernetes kubeconfig YAML document containing:

```yaml
apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority-data: <base64-encoded-ca>
    server: https://<cluster-endpoint>:5443
  name: internalCluster
- cluster:
    server: https://<cluster-eip>:5443
    insecure-skip-tls-verify: true
  name: externalCluster
- cluster:
    certificate-authority-data: <base64-encoded-ca>
    server: https://<cluster-eip>:5443
  name: externalClusterTLSVerify
contexts:
- context:
    cluster: internalCluster
    user: user
  name: internal
- context:
    cluster: externalCluster
    user: user
  name: external
- context:
    cluster: externalClusterTLSVerify
    user: user
  name: externalTLSVerify
current-context: external
```

### UCS DownloadFederationKubeconfig (Federation Kubeconfig YAML)

Returns a federation kubeconfig with two contexts for multi-cluster fleet operations:

```yaml
apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority-data: <base64-encoded-ca>
    server: https://<fleet-name>.fleet.ucs.<region>.myhuaweicloud.com:5443
  name: federation
- cluster:
    certificate-authority-data: <base64-encoded-ca>
    server: https://<fleet-name>.fleet.ucs.<region>.myhuaweicloud.com:5443/apis/cluster.karmada.io/v1alpha1/clusters/*/proxy
  name: karmada-aggregated-apiserver
contexts:
- context:
    cluster: federation
    user: user
  name: federation
- context:
    cluster: karmada-aggregated-apiserver
    user: user
  name: karmada-aggregated-apiserver
current-context: federation
```

**Federation vs Karmada context**:
- `federation`: Operates on fleet-level resources (propagated workloads, fleet policies)
- `karmada-aggregated-apiserver`: Proxy access to individual member clusters via `/clusters/<cluster-name>/proxy`

> **Network prerequisite**: UCS federation kubeconfig uses `<fleet-name>.fleet.ucs.<region>.myhuaweicloud.com` as the API server domain. This domain resolves via UCS VPC Endpoint (VPCEP). If DNS resolution fails, ensure your network can reach the UCS VPCEP (e.g., via VPC peering, VPN, or direct cloud network access).
```

### kubectl Output Formats

| `-o` flag        | Description                        | Use Case                                    |
| ---------------- | ---------------------------------- | ------------------------------------------- |
| (default)        | Tabular human-readable output      | Quick status check                          |
| `-o wide`        | Extended tabular with extra columns | Detailed Pod/IP info                       |
| `-o yaml`        | YAML format                        | Export/edit resource specs                  |
| `-o json`        | JSON format                        | Scripting/automation                        |
| `-o name`        | Resource name only                 | Quick list of names                         |

## Common Region IDs

| Region Name                    | Region ID        |
| ------------------------------ | ---------------- |
| North China - Beijing 4        | `cn-north-4`     |
| North China - Beijing 1        | `cn-north-1`     |
| East China - Shanghai 1        | `cn-east-3`      |
| East China - Shanghai 2        | `cn-east-2`      |
| South China - Guangzhou        | `cn-south-1`     |
| South China - Shenzhen         | `cn-south-4`     |
| Southwest China - Guiyang 1    | `cn-southwest-2` |
| Asia Pacific - Bangkok         | `ap-southeast-2` |
| Asia Pacific - Singapore       | `ap-southeast-1` |
| Asia Pacific - Hong Kong       | `ap-southeast-3` |
| Europe - Paris                 | `eu-west-0`      |

## Verification

### Kubeconfig Acquisition Verification

```bash
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml cluster-info
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get nodes
```

### Workload Deployment Verification

```bash
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get deployments -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml rollout status deployment/my-app -n production
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get pods -o wide -n production
```

### HPA Verification

```bash
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get hpa -n production
```

## Best Practices

1. **Namespace-First**: Always specify `-n <namespace>` explicitly; never rely on default namespace
2. **Kubeconfig Security**: Store kubeconfig files with restricted file permissions (chmod 600); never expose them in public repositories or CI logs
3. **Short-Duration Certificates**: Use minimum `--duration` needed for CCE kubeconfig; prefer 1 day for interactive sessions
4. **RBAC Alignment**: Ensure Huawei Cloud IAM permissions and Kubernetes RBAC roles are aligned; IAM grants kubeconfig access, RBAC grants kubectl operations
5. **YAML-Based Deployment**: Prefer `kubectl apply -f` over inline `kubectl create` for reproducibility and auditability
6. **Rollout Monitoring**: Always check `rollout status` after updates; use `rollout undo` for emergency rollback
7. **Namespace Isolation**: Use separate namespaces for production, staging, and development workloads
8. **HPA Baseline**: Set HPA `--min` to your steady-state replica count; set `--max` based on resource budget

## Reference Documents

| Document                                                      | Description                              |
| ------------------------------------------------------------- | ---------------------------------------- |
| [Task: Kubeconfig Acquisition](references/task-kubeconfig-acquisition.md) | Kubeconfig acquisition workflows |
| [Task: kubectl Setup](references/task-kubectl-setup.md)       | kubectl installation and configuration   |
| [Task: Deployment Management](references/task-deployment-management.md) | Deployment lifecycle workflows |
| [Task: StatefulSet/DaemonSet Management](references/task-statefulset-daemonset-management.md) | StatefulSet and DaemonSet workflows |

## Notes

- **kubectl is the primary tool** — all workload operations use `kubectl --kubeconfig=<file>` after kubeconfig acquisition via `hcloud`
- **kubeconfig is a secret** — treat it like a credential; never share or expose publicly
- **RBAC governs kubectl access** — even with a valid kubeconfig, Kubernetes RBAC controls what operations are permitted
- **cce-cluster-management handles infrastructure** — cluster creation, deletion, and node management belong to the `cce-cluster-management` skill
- **Two-layer permission model** — Huawei Cloud IAM controls kubeconfig acquisition, Kubernetes RBAC controls kubectl operations
- **UCS is for fleet operations** — UCS kubeconfig is only for federation (DownloadFederationKubeconfig), not single cluster (CreateClusterKubeconfig is out of scope for this skill)
- **UCS federation kubeconfig provides two contexts** — `federation` (fleet-level) and `karmada-aggregated-apiserver` (proxy to member clusters)
- **UCS federation requires network access** — fleet API server domain (`<fleet>.fleet.ucs.<region>.myhuaweicloud.com`) requires VPCEP access

## Common Pitfalls

| Pitfall                              | Symptom                              | Quick Fix                                          |
| ------------------------------------ | ------------------------------------ | -------------------------------------------------- |
| kubectl not installed                | Command not found                    | Install kubectl (see references/task-kubectl-setup.md) |
| Wrong cluster_id                     | 404 or kubeconfig for wrong cluster  | Verify cluster ID with `hcloud CCE ListClusters`  |
| Kubeconfig expired                   | Authentication failures              | Re-acquire kubeconfig with `CreateKubernetesClusterCert` |
| RBAC insufficient                    | Forbidden errors in kubectl          | Configure appropriate ClusterRole/Role bindings    |
| Missing namespace flag               | Resources in wrong namespace         | Always specify `-n <namespace>` explicitly         |
| CCE vs UCS param confusion           | Parameter not recognized             | CCE: `--cluster_id`, UCS: `--clustergroupid` for federation |
| Duration unit confusion              | Certificate expires immediately      | CCE: days (1-1827), UCS federation: days (1-1825) |
| UCS federation DNS unreachable       | `no such host` on federation API     | Ensure VPCEP/network access to UCS fleet domain |
| Inline create vs YAML apply          | Hard to reproduce/audit              | Prefer `kubectl apply -f <yaml>` for production   |
| Rollout without status check         | Unknown deployment state             | Always run `rollout status` after updates          |
| Kubeconfig file permissions          | Security warning or access denied    | Set file permissions to 600 (`chmod 600`)         |
| Wrong StorageClass in PVC            | PVC stuck Pending                    | Use `csi-disk` (not `cce-standard`); run `kubectl get sc` to verify |
| Metrics API not available            | `top pods/nodes` fails               | Install metrics-server addon via CCE console       |
| PowerShell JSON patch escaping       | `patch -p` fails with JSON errors    | Use `--patch-file` instead of inline `-p` JSON     |
| HPA --cpu-percent deprecated         | Warning flag deprecated              | Use `--cpu=80%` instead of `--cpu-percent=80`      |
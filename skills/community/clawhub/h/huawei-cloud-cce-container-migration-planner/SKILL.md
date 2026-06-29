---
id: huawei-cloud-cce-container-migration-planner
name: huawei-cloud-cce-container-migration-planner
description: |
  Huawei Cloud CCE container migration planning skill using Python SDK dispatcher for read-only resource inventory,
  dependency mapping, migration batch design, risk assessment, and rollback strategy generation.
  Use this skill when the user wants to: (1) plan CCE cluster migration including same-region, cross-region,
  multi-cluster, hybrid cloud, version upgrade, or architecture adjustment, (2) inventory source cluster workloads,
  networking, storage, and configuration resources, (3) build dependency matrices and migration batches,
  (4) generate risk lists, rollback strategies, validation plans, and manual confirmation checklists.
  Trigger: user mentions "container migration", "容器迁移", "migration planning", "迁移规划", "migration assessment",
  "迁移评估", "workload migration", "工作负载迁移", "cluster migration", "集群迁移", "migration plan",
  "迁移方案", "migration inventory", "迁移盘点", "dependency mapping", "依赖梳理", "migration batch",
  "迁移批次", "migration risk", "迁移风险"
tags: [cce, migration, planning, assessment]
---

# Huawei Cloud CCE Container Migration Planner

> **⚠️ Execution Method (Must Read): This skill executes queries via the local Python dispatcher script. Using hcloud, openstack, or other CLI tools or direct API calls is prohibited.**
>
> - The dispatcher script is located at `scripts/huawei-cloud.py` within the skill directory
> - All scripts and environment check scripts are inside the skill package. **You must use `skill action=exec` to execute them. Do not run them directly in a shell.**
> - **Do not attempt hcloud, openstack, curl IAM, or any other CLI/API methods. This skill does not depend on those tools.**
> - **All paths are relative to the skill directory, which is the directory where this SKILL.md is located.**

## Overview

This skill plans Huawei Cloud CCE container migrations by inventorying source clusters, mapping dependencies, designing migration batches, and generating risk assessments with rollback strategies. It performs **read-only** resource discovery and planning only — it does NOT create target resources, modify networks, migrate data, or delete source resources.

**Architecture**: Python dispatcher (`scripts/huawei-cloud.py`) → Huawei Cloud Python SDK + Kubernetes client → CCE clusters, node pools, addons, workloads, Services, Ingresses, PVCs, PVs, ConfigMaps, Secrets, VPC, subnets, security groups, ELB, EIP, EVS, SFS/SFS Turbo → Dependency matrix → Migration batches → Risk assessment → Rollback & validation plans → Output report

**Related Skills**:

| Skill | Purpose |
|-------|---------|
| `huawei-cloud-cce-availability-risk-scanner` | Scan availability risks before migration |
| `huawei-cloud-cce-dependency-impact-analyzer` | Analyze dependency impact for changes |
| `huawei-cloud-cce-change-impact-analyzer` | Assess change impact before migration |
| `huawei-cloud-cce-daily-cluster-inspector` | Pre-migration cluster health inspection |
| `huawei-cloud-cce-cost-optimization-advisor` | Cost analysis for migration sizing |

**Capabilities**:

1. CCE cluster inventory: clusters, node pools, addons, network model, key configurations
2. Workload inventory: Deployments, StatefulSets, DaemonSets, Services, Ingresses, PVCs, PVs, ConfigMaps, Secrets
3. Cloud resource inventory: VPC, subnets, security groups, ELB, EIP, EVS, SFS/SFS Turbo
4. Dependency matrix construction: ingress traffic, service dependencies, storage dependencies, configuration dependencies, external system dependencies
5. Migration batch design with validation points, rollback strategies, and downtime windows
6. Risk assessment with severity classification and manual confirmation checklists
7. Structured output following the migration planning schema

**Typical Use Cases**:

- "Plan migration from my CCE cluster to another region"
- "Inventory all workloads and dependencies in my CCE cluster"
- "Design migration batches for a multi-cluster migration"
- "Assess risks for a CCE version upgrade migration"
- "Build a dependency matrix for my container workloads"
- "Generate a rollback plan for cluster migration"
- "Plan hybrid cloud migration from CCE"
- "Create a migration assessment report with risk classification"

## Prerequisites

### 1. Python Requirements (MANDATORY)

- Python >= 3.6 installed
- Required packages: `huaweicloudsdkcore`, `huaweicloudsdkcce`, `huaweicloudsdkvpc`, `huaweicloudsdkecs`, `huaweicloudsdkevs`, `huaweicloudsdkeip`, `huaweicloudsdkelb`, `huaweicloudsdkiam`, `kubernetes`
- Verify: `python3 --version`
- Install packages: `pip3 install huaweicloudsdkcore huaweicloudsdkcce huaweicloudsdkvpc huaweicloudsdkecs huaweicloudsdkevs huaweicloudsdkeip huaweicloudsdkelb huaweicloudsdkiam kubernetes`

### 2. Credential Configuration

- Valid Huawei Cloud credentials (AK/SK mode)
- **Security Rules**:
  - 🚫 Never expose AK/SK values in code, conversation, or commands
  - 🚫 Never use `echo $HUAWEI_AK` or `echo $HUAWEI_SK` to check credentials
  - 🚫 Never write credentials to files, logs, or responses
  - ✅ Use environment variables: `HUAWEI_AK`, `HUAWEI_SK`, `HUAWEI_REGION`
  - ✅ Credentials exist only in the current request call stack and are released after each invocation
  - ✅ Prefer IAM users over root account for cloud operations

**Configuration Method** (Environment Variables Only):

```bash
export HUAWEI_AK=<your-ak>
export HUAWEI_SK=<your-sk>
export HUAWEI_REGION=cn-north-4
```

**Additional Variables**:

| Variable | Required | Description |
|----------|----------|-------------|
| `HUAWEI_AK` | Yes | Huawei Cloud Access Key |
| `HUAWEI_SK` | Yes | Huawei Cloud Secret Key |
| `HUAWEI_REGION` | No | Default region (overrides `region` param if set) |
| `HUAWEI_PROJECT_ID` | No | Project ID (auto-obtained via IAM API when not set) |
| `HUAWEI_SECURITY_TOKEN` | No | Required when using temporary AK/SK |

### 3. IAM Permission Requirements

| API Action | Service | Purpose |
|------------|---------|---------|
| CCE cluster read | CCE | `huawei_list_cce_clusters` |
| CCE node read | CCE | `huawei_list_cce_nodes` |
| CCE nodepool read | CCE | `huawei_list_cce_nodepools` |
| CCE addon read | CCE | `huawei_list_cce_addons` |
| CCE workload read | CCE | `huawei_get_cce_deployments` |
| CCE Service read | CCE | `huawei_get_cce_services` |
| CCE Ingress read | CCE | `huawei_get_cce_ingresses` |
| CCE PVC read | CCE | `huawei_get_cce_pvcs` |
| CCE PV read | CCE | `huawei_get_cce_pvs` |
| CCE ConfigMap read | CCE | `huawei_list_cce_configmaps` |
| CCE Secret read | CCE | `huawei_list_cce_secrets` |
| VPC read | VPC | `huawei_list_vpc`, `huawei_list_vpc_subnets`, `huawei_list_security_groups` |
| ELB read | ELB | `huawei_list_elb` |
| EIP read | EIP | `huawei_list_eip` |
| EVS read | EVS | `huawei_list_evs` |
| SFS read | SFS | `huawei_list_sfs`, `huawei_list_sfs_turbo` |

**Permission Failure Handling**:

1. When any action fails due to permission errors, display the required permission list
2. Guide the user to create a custom policy in the IAM console
3. Pause execution and wait for user confirmation that permissions have been granted
4. Retry the failed action

## Core Commands

All actions are invoked via the dispatcher script:

```bash
python3 scripts/huawei-cloud.py <action> region=<region> cluster_id=<cluster_id> [key=value ...]
```

### 1. CCE Cluster Inventory

| Action | Required Params | Description |
|--------|----------------|-------------|
| `huawei_list_cce_clusters` | `region` | List CCE clusters in the region |
| `huawei_list_cce_nodes` | `region`, `cluster_id` | List cluster nodes |
| `huawei_list_cce_nodepools` | `region`, `cluster_id` | List node pools |
| `huawei_list_cce_addons` | `region`, `cluster_id` | List installed addons |

### 2. Workload Inventory

| Action | Required Params | Description |
|--------|----------------|-------------|
| `huawei_get_cce_deployments` | `region`, `cluster_id` | List Deployments |
| `huawei_get_cce_services` | `region`, `cluster_id` | List Services |
| `huawei_get_cce_ingresses` | `region`, `cluster_id` | List Ingresses |
| `huawei_get_cce_pvcs` | `region`, `cluster_id` | List PersistentVolumeClaims |
| `huawei_get_cce_pvs` | `region`, `cluster_id` | List PersistentVolumes |
| `huawei_list_cce_configmaps` | `region`, `cluster_id` | List ConfigMaps |
| `huawei_list_cce_secrets` | `region`, `cluster_id` | List Secrets (existence only, no values) |

### 3. Cloud Resource Inventory

| Action | Required Params | Description |
|--------|----------------|-------------|
| `huawei_list_vpc` | `region` | List VPCs |
| `huawei_list_vpc_subnets` | `region`, `vpc_id` | List subnets in a VPC |
| `huawei_list_security_groups` | `region` | List security groups |
| `huawei_list_elb` | `region` | List Elastic Load Balancers |
| `huawei_list_eip` | `region` | List Elastic IPs |
| `huawei_list_evs` | `region` | List EVS disks |
| `huawei_list_sfs` | `region` | List SFS file systems |
| `huawei_list_sfs_turbo` | `region` | List SFS Turbo file systems |

### 4. Example Commands

```bash
# List clusters for migration scope
python3 scripts/huawei-cloud.py huawei_list_cce_clusters region=cn-north-4

# Inventory cluster workloads
python3 scripts/huawei-cloud.py huawei_get_cce_deployments region=cn-north-4 cluster_id=<cluster_id>

# Inventory networking resources
python3 scripts/huawei-cloud.py huawei_get_cce_services region=cn-north-4 cluster_id=<cluster_id>
python3 scripts/huawei-cloud.py huawei_get_cce_ingresses region=cn-north-4 cluster_id=<cluster_id>

# Inventory storage resources
python3 scripts/huawei-cloud.py huawei_get_cce_pvcs region=cn-north-4 cluster_id=<cluster_id>
python3 scripts/huawei-cloud.py huawei_get_cce_pvs region=cn-north-4 cluster_id=<cluster_id>

# Inventory cloud resources
python3 scripts/huawei-cloud.py huawei_list_vpc region=cn-north-4
python3 scripts/huawei-cloud.py huawei_list_elb region=cn-north-4
python3 scripts/huawei-cloud.py huawei_list_evs region=cn-north-4
```

## Parameter Reference

### Common Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `region` | Yes | Huawei Cloud region (e.g., `cn-north-4`) | - |
| `cluster_id` | Yes (most actions) | CCE cluster ID | - |
| `namespace` | Context-dependent | Kubernetes namespace | - |
| `vpc_id` | Yes (subnet listing) | VPC ID for subnet queries | - |

### Common Region IDs

| Region Name | Region ID |
|-------------|-----------|
| North China - Beijing 4 | `cn-north-4` |
| North China - Beijing 1 | `cn-north-1` |
| East China - Shanghai 1 | `cn-east-3` |
| East China - Shanghai 2 | `cn-east-2` |
| South China - Guangzhou | `cn-south-1` |
| South China - Shenzhen | `cn-south-4` |
| Southwest China - Guiyang 1 | `cn-southwest-2` |
| Asia Pacific - Bangkok | `ap-southeast-2` |
| Asia Pacific - Singapore | `ap-southeast-1` |
| Asia Pacific - Hong Kong | `ap-southeast-3` |
| Europe - Paris | `eu-west-0` |

## Output Format

See [Output Schema](references/output-schema.md) for the complete JSON response structure.

**Key Output Fields**:

| Field | Description |
|-------|-------------|
| `summary` | Migration planning summary with scope description |
| `source` | Source region and cluster ID |
| `inventory.clusters` | CCE cluster inventory |
| `inventory.nodepools` | Node pool inventory |
| `inventory.workloads` | Workload inventory (Deployments, Services, Ingresses, etc.) |
| `inventory.networking` | Networking inventory (VPC, subnets, security groups, ELB, EIP) |
| `inventory.storage` | Storage inventory (PVC/PV, EVS, SFS/SFS Turbo) |
| `inventory.configuration` | Configuration inventory (ConfigMaps, Secrets existence only) |
| `dependency_matrix` | Dependency relationships (ingress traffic, service calls, storage bindings, config references, external systems) |
| `migration_batches` | Migration batch design with validation points and downtime windows |
| `risks` | Risk list with severity classification and mitigation strategies |
| `rollback_plan` | Rollback strategy per batch |
| `validation_plan` | Validation steps per batch |

## Verification

To verify this skill is working correctly:

1. **Credential check**: Run `python3 scripts/huawei-cloud.py huawei_list_cce_clusters region=cn-north-4` and confirm it returns cluster data
2. **Workload inventory**: Run `python3 scripts/huawei-cloud.py huawei_get_cce_deployments region=cn-north-4 cluster_id=<cluster_id>` and confirm it returns deployment data
3. **Cloud resource inventory**: Run `python3 scripts/huawei-cloud.py huawei_list_vpc region=cn-north-4` and confirm it returns VPC data
4. **Read-only boundary**: Verify that no create, delete, scale, migrate, bind, unbind, or modify actions are invoked

## Best Practices

1. **Start with scope confirmation**: Confirm migration goal (same-region, cross-region, multi-cluster, hybrid cloud, version upgrade, or architecture adjustment) before inventory
2. **Full inventory first**: Always inventory all resource categories (cluster, workloads, networking, storage, configuration) before building dependency matrix
3. **Secret handling**: Only record Secret existence, name, and purpose — never output sensitive values
4. **Desensitization**: All `project_id`, AK/SK, tokens, and certificates in output must be masked or omitted
5. **Dependency matrix**: Build dependency matrix covering ingress traffic, service dependencies, storage dependencies, configuration dependencies, and external system dependencies
6. **Batch design**: Design migration batches with clear validation points, rollback strategies, and downtime windows per batch
7. **Manual confirmation**: All execution actions must be placed in a manual confirmation checklist — this skill does NOT execute changes
8. **Risk assessment**: Use `huawei-cloud-cce-availability-risk-scanner` as a pre-migration health check before finalizing the migration plan

## Reference Documents

| Document | Description |
|----------|-------------|
| [Workflow](references/workflow.md) | Migration planning workflow, inventory steps, dependency mapping, and batch design process |
| [Risk Rules](references/risk-rules.md) | Safety constraints, prohibited actions, and authorization boundaries |
| [Output Schema](references/output-schema.md) | Complete JSON response format for migration planning results |

## Notes

- **Read-only by design** — this skill does NOT create target resources, modify networks, migrate data, or delete source resources
- **Secret safety** — Secret inventory only records existence, name, and purpose; sensitive values are never exposed
- **Desensitization** — all project_id, AK/SK, tokens, and certificates in output are masked or omitted
- **Manual confirmation** — all execution actions are placed in a confirmation checklist; no auto-execution
- **All actions are executed via `python3 scripts/huawei-cloud.py <action>`; do not use hcloud CLI or direct API calls**
- **Never expose or log AK/SK or environment variable values**

## Common Pitfalls

| Pitfall | Symptom | Quick Fix |
|---------|---------|-----------|
| Skipping dependency mapping | Migration batches miss cross-service dependencies | Always build dependency matrix before batch design |
| Exposing Secret values | Output contains sensitive Secret data | Only record Secret existence and name; never output values |
| Unmasked credentials | Output contains project_id, AK/SK, or tokens | Mask or omit all credential fields in output |
| Missing cloud resource inventory | Migration plan ignores VPC/ELB/EVS dependencies | Include all cloud resource categories in inventory |
| No rollback strategy | Migration batch has no rollback plan | Every batch must include a rollback strategy and validation steps |
| Ignoring downtime windows | Migration plan schedules batches during peak hours | Align batch design with business downtime windows |
| Assuming migration can execute | Skill attempts to create target resources | This skill is read-only; all execution goes to manual confirmation checklist |
| Wrong cluster_id | API returns 404 or empty results | Verify cluster ID via `huawei_list_cce_clusters` |
| Credential permission denied | API returns 403 | Check IAM permissions for CCE/VPC/ELB/EVS/SFS read access |
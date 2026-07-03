---
name: huawei-cloud-cce-pressure-test
description: |
  Huawei Cloud CCE end-to-end workload pressure testing and performance evaluation using Python SDK dispatcher.
  Trigger: "pressure test", "压测", "load test", "负载测试", "stress test", "压力测试", "performance test", "性能测试", "k6 test", "k6 压测", "ELB traffic test", "ELB 流量测试", "end-to-end pressure test", "全链路压测", "elasticity evaluation", "弹性评估", "traffic generation", "流量生成"
tags: [cce, pressure-test, k6, elb, observability]
---

# Huawei Cloud CCE Pressure Test

**Trigger keywords**: pressure test, 压测, load test, 负载测试,
stress test, 压力测试, performance test, 性能测试, k6 test, k6 压测,
ELB traffic test, ELB 流量测试, end-to-end pressure test, 全链路压测,
elasticity evaluation, 弹性评估, traffic generation, 流量生成

> **⚠️ Execution Method (Must Read): This skill executes queries via the local Python dispatcher script. Using hcloud, openstack, or other CLI tools or direct API calls is prohibited.**
>
> - The dispatcher script is located at `scripts/huawei-cloud.py` within the skill directory
> - All scripts and environment check scripts are inside the skill package. **You must use `skill action=exec` to execute them. Do not run them directly in a shell.**
> - **Do not attempt hcloud, openstack, curl IAM, or any other CLI/API methods. This skill does not depend on those tools.**
> - **All paths are relative to the skill directory, which is the directory where this SKILL.md is located.**

## Overview

This skill runs controlled workload pressure tests on Huawei Cloud CCE.
It builds a complete traffic path from a k6 client through ELB to
nginx-ingress to workload pods, supports short-connection, keepalive,
and ramp traffic models, collects ELB metrics and AOM observability data,
evaluates elasticity phases, and generates bilingual Markdown and HTML
reports with performance curves.

**Architecture**: Python dispatcher (`scripts/huawei-cloud.py`) →
Huawei Cloud Python SDK + Kubernetes client → ELB/CCE/AOM/APM APIs →
Route preparation → Client generation → Traffic run →
Observability collection → Report generation

**Key Principle**: Preview-first. Read-only checks may run immediately,
but Service/Ingress changes, traffic generation, and workload scaling
require explicit user approval with `confirm=true` before execution.

**Related Skills**:

| Skill | Purpose |
|-------|---------|
| `huawei-cloud-cce-autoscaling-diagnoser` | Diagnose autoscaling failures when HPA or CA does not respond during pressure tests |
| `huawei-cloud-cce-observability-context-builder` | Build observability context when AOM/APM evidence is needed |
| `huawei-cloud-cce-pod-failure-diagnoser` | Diagnose Pod runtime failures during traffic runs |
| `huawei-cloud-cce-node-failure-diagnoser` | Diagnose node-level failures under load |
| `huawei-cloud-cce-workload-failure-diagnoser` | Diagnose workload rollout failures after scaling |
| `huawei-cloud-cce-auto-remediation-runner` | Execute remediation actions when issues are found during tests |
| `huawei-cloud-cce-cluster-management` | Cluster lifecycle, nodepool management, kubeconfig retrieval |

**Capabilities**:

1. End-to-end traffic path: k6 client → ELB → nginx-ingress → workload Service → Pod
2. Short-connection (`short`), keepalive (`keepalive`), and staged ramp (`ramp`) traffic models
3. Isolated Java sample deployment for lab environments
4. ELB creation when no reusable ingress-controller ELB exists
5. Route preparation: Service and Ingress creation/patching with preview-first
6. k6 client generation with ConfigMap and Job
7. Traffic run with replica and Pod count monitoring
8. APM Java agent injection for distributed tracing during tests
9. Observability collection: ELB metrics, Pod CPU/memory, AOM logs
10. Bilingual Markdown and HTML report generation with SVG performance curves
11. Elasticity evaluation: baseline vs scaled phase comparison

## Prerequisites

### 1. Python Requirements (MANDATORY)

- Python >= 3.6 installed
- Required packages: `huaweicloudsdkcore`, `huaweicloudsdkcce`, `huaweicloudsdkvpc`, `huaweicloudsdkvpcep`, `huaweicloudsdkaom`, `huaweicloudsdkelb`, `kubernetes`, `matplotlib`
- Verify: `python3 --version`
- Install packages: `pip3 install huaweicloudsdkcore huaweicloudsdkcce huaweicloudsdkvpc huaweicloudsdkvpcep huaweicloudsdkaom huaweicloudsdkelb kubernetes matplotlib`

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

### 3. IAM Permission Requirements

| API Action | Service | Purpose |
|------------|---------|---------|
| CCE cluster read | CCE | Cluster info, workload inspection, Pod metrics |
| CCE workload read/write | CCE (kubeconfig) | Deploy Java sample, create Service/Ingress, scale replicas |
| CCE addon read | CCE | Check ingress controller and metrics addon |
| ELB create/list/read | ELB | Create load balancer for test traffic path |
| VPC subnet list | VPC | Find candidate subnets for ELB VIP |
| VPCEP endpoint list | VPCEP | Check existing VPCEP endpoints |
| AOM metrics read | AOM | Collect Pod CPU/memory and custom metrics |
| AOM instances list/resolve | AOM | Find AOM instance for the cluster |
| APM master address read | APM | Get APM master address for Java agent injection |
| LTS log query | LTS | Correlate application errors with traffic curves |

**Permission Failure Handling**:

1. When any action fails due to IAM permission errors, display the required permission list
2. Guide the user to create custom policies in the IAM console for Huawei Cloud permissions
3. Pause execution and wait for user confirmation that permissions have been granted
4. Retry the failed action

## Core Commands

All actions are invoked via the dispatcher script:

```bash
python3 scripts/huawei-cloud.py <action> region=<region> cluster_id=<cluster_id> [key=value ...]
```

### 1. Deploy Java Sample (Optional)

```bash
# Preview (no mutation)
python3 scripts/huawei-cloud.py huawei_deploy_cce_pressure_test_java_sample \
  region=cn-north-4 cluster_id=<cluster_id>

# Apply after user approval
python3 scripts/huawei-cloud.py huawei_deploy_cce_pressure_test_java_sample \
  region=cn-north-4 cluster_id=<cluster_id> confirm=true
```

Creates an isolated Namespace, ConfigMap (small Java HTTP server), and Deployment with readiness/liveness probes. Exposes `/healthz`, `/api/hello`, and `/api/work` on port `8080`.

### 2. Create ELB (When No Reusable ELB Exists)

```bash
# Preview (no mutation)
python3 scripts/huawei-cloud.py huawei_create_elb \
  region=cn-north-4 name=<elb-name> vip_subnet_cidr_id=<subnet-network-id>

# Apply after user approval
python3 scripts/huawei-cloud.py huawei_create_elb \
  region=cn-north-4 name=<elb-name> vip_subnet_cidr_id=<subnet-network-id> confirm=true
```

Creates a chargeable ELB. Review billable fields before applying. Does not silently create an EIP.

### 3. Prepare Route

```bash
# Preview (no mutation)
python3 scripts/huawei-cloud.py huawei_prepare_cce_pressure_test_route \
  region=cn-north-4 cluster_id=<cluster_id> namespace=<namespace> workload_name=<deployment-name> target_port=8080

# Apply after user approval
python3 scripts/huawei-cloud.py huawei_prepare_cce_pressure_test_route \
  region=cn-north-4 cluster_id=<cluster_id> namespace=<namespace> workload_name=<deployment-name> target_port=8080 confirm=true
```

Creates or patches a ClusterIP Service and Ingress pointing to the workload. Discover an existing nginx ingress controller LoadBalancer address. Does not silently create a chargeable ELB.

### 4. Inject APM Java Agent (Optional)

```bash
python3 scripts/huawei-cloud.py huawei_inject_cce_apm_javaagent \
  region=cn-north-4 cluster_id=<cluster_id> namespace=<namespace> \
  workload_name=<deployment-name> app_name=<apm-app-name> \
  business=<apm-business> env_name=<apm-env>
```

Injects the Huawei Cloud APM Java agent into the workload Deployment for distributed tracing during the pressure test.

### 5. Generate k6 Client

```bash
python3 scripts/huawei-cloud.py huawei_generate_cce_pressure_test_client \
  target_url=http://<elb-address>/<path> namespace=pressure-test \
  model=keepalive vus=10 duration_seconds=60
```

Generates the k6 ConfigMap and Job manifest. Use a regional SWR mirror for the k6 image when public image pulls are unavailable.

**Supported Traffic Models**:

| Model | Purpose |
|-------|---------|
| `short` | Disable connection reuse; observe new-connection pressure |
| `keepalive` | Reuse connections for a steady HTTP baseline |
| `ramp` | Increase traffic in stages then scale down |

### 6. Run Pressure Test

```bash
# Preview (no mutation)
python3 scripts/huawei-cloud.py huawei_run_cce_pressure_test \
  region=cn-north-4 cluster_id=<cluster_id> target_url=http://<elb-address>/<path>

# Apply after user approval
python3 scripts/huawei-cloud.py huawei_run_cce_pressure_test \
  region=cn-north-4 cluster_id=<cluster_id> target_url=http://<elb-address>/<path> confirm=true
```

Ensures the client namespace, creates the ConfigMap and Job, waits for completion by default, records replica/Pod count samples, and extracts the k6 summary from logs.

### 7. Collect Observability

```bash
python3 scripts/huawei-cloud.py huawei_collect_cce_pressure_test_observability \
  region=cn-north-4 cluster_id=<cluster_id> namespace=<namespace> \
  workload_name=<deployment-name> elb_id=<elb-id>
```

Collects ELB QPS, active connections, layer-7 response time, 2xx ratio,
Pod CPU/memory metrics, and AOM evidence. Pass `label_selector` to scope
Pod metrics to the workload. Pod CPU and memory are collected from node
metrics when `aom_instance_id` is not provided.

### 8. Generate Report

```bash
python3 scripts/huawei-cloud.py huawei_generate_cce_pressure_test_report \
  result_path=<path-to-run-json>
```

Generates Markdown, HTML, and SVG curve artifacts from the run JSON and optional observability JSON.

### 9. Scale Workload (Elasticity Evaluation)

```bash
# Preview (no mutation)
python3 scripts/huawei-cloud.py huawei_scale_cce_workload \
  region=cn-north-4 cluster_id=<cluster_id> workload_type=Deployment \
  name=<deployment-name> namespace=<namespace> replicas=5

# Apply after user approval
python3 scripts/huawei-cloud.py huawei_scale_cce_workload \
  region=cn-north-4 cluster_id=<cluster_id> workload_type=Deployment \
  name=<deployment-name> namespace=<namespace> replicas=5 confirm=true
```

For elasticity evaluation: run a baseline phase, preview scaling, apply only after approval with `confirm=true`, then run a second phase and compare reports.

### 10. Supporting Actions (Read-Only)

| Action | Required Params | Description |
|--------|----------------|-------------|
| `huawei_list_cce_hpas` | `region`, `cluster_id` | List HPA specs and conditions |
| `huawei_get_cce_pods` | `region`, `cluster_id` | List Pod phase, resources, node assignment |
| `huawei_get_cce_services` | `region`, `cluster_id` | List Service types and cluster IPs |
| `huawei_get_cce_ingresses` | `region`, `cluster_id` | List Ingress rules and LoadBalancer IPs |
| `huawei_get_cce_pod_metrics_topN` | `region`, `cluster_id` | Pod resource metric ranking |
| `huawei_get_elb_metrics` | `region`, `elb_id` | ELB QPS, connections, latency, success rate |
| `huawei_get_elb_backend_status` | `region`, `elb_id` | Backend member health status |
| `huawei_list_vpc_subnets` | `region` | List VPC subnets for ELB VIP placement |
| `huawei_list_aom_instances` | `region` | List AOM instances |
| `huawei_resolve_cce_aom_instance` | `region`, `cluster_id` | Resolve AOM instance for a CCE cluster |
| `huawei_get_apm_master_address` | `region` | Get APM master address for agent injection |
| `huawei_get_aom_metrics` | `region`, `aom_instance_id`, `query` | AOM/Prometheus metric queries |
| `huawei_query_aom_logs` | `region`, `cluster_id` | Query AOM LTS logs |
| `huawei_get_cce_logconfigs` | `region`, `cluster_id` | List CCE log collection configs |
| `huawei_create_cce_logconfig` | `region`, `cluster_id`, `logconfig_name`, `source_type`, `log_group_id`, `log_stream_id` | Create CCE log collection config |
| `huawei_get_application_logconfigs` | `region`, `cluster_id`, `app_name` | Get application log configs |
| `huawei_query_application_logs` | `region`, `cluster_id`, `app_name` | Query application logs |
| `huawei_analyze_application_logs` | `region`, `cluster_id`, `app_name` | Analyze application logs for errors |
| `huawei_generate_monitor_dashboard` | `region`, `cluster_id` | Generate AOM monitor dashboard URL |

## Parameter Reference

### Common Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `region` | Yes | Huawei Cloud region | - |
| `cluster_id` | Yes (most actions) | CCE cluster ID | - |
| `namespace` | Action-dependent | Kubernetes namespace | - |
| `workload_name` | Action-dependent | Deployment name | - |
| `ak` | No | Access Key (overrides env var) | `HUAWEI_AK` env |
| `sk` | No | Secret Key (overrides env var) | `HUAWEI_SK` env |
| `project_id` | No | Project ID (overrides env var) | Auto-resolved |

### Deploy Java Sample Parameters

| Parameter | Required | Description | Notes |
|-----------|----------|-------------|-------|
| `confirm` | Required for mutation | Approve deployment | `true` to apply, omit to preview |

### ELB Creation Parameters

| Parameter | Required | Description | Notes |
|-----------|----------|-------------|-------|
| `name` | Yes | ELB name | - |
| `vip_subnet_cidr_id` | Yes | VPC subnet network ID for ELB VIP | Obtain from `huawei_list_vpc_subnets` |
| `availability_zone_list` | No | AZ list | Comma-separated |
| `l4_flavor_id` | No | Layer-4 flavor ID | Optional performance spec |
| `l7_flavor_id` | No | Layer-7 flavor ID | Optional performance spec |
| `confirm` | Required for mutation | Approve ELB creation | `true` to apply, omit to preview |

### Route Preparation Parameters

| Parameter | Required | Description | Notes |
|-----------|----------|-------------|-------|
| `target_port` | No | Container target port | Defaults to workload's first container port |
| `host` | No | Ingress host rule | Pass same value as `host_header` to client |
| `selector_json` | No | Pod selector for non-Deployment workloads | JSON string |
| `confirm` | Required for mutation | Approve route creation | `true` to apply, omit to preview |

### Client Generation Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `target_url` | Yes | Full URL to test | - |
| `namespace` | No | k6 client namespace | `pressure-test` |
| `model` | No | Traffic model (`short`, `keepalive`, `ramp`) | `keepalive` |
| `vus` | No | Number of virtual users | `10` |
| `duration_seconds` | No | Test duration | `60` |
| `host_header` | No | Host header for Ingress host rules | Matches `host` from route preparation |

### Traffic Run Parameters

| Parameter | Required | Description | Notes |
|-----------|----------|-------------|-------|
| `target_url` | Yes | Full URL to test | Must match client target |
| `confirm` | Required for mutation | Approve traffic run | `true` to apply, omit to preview |

### Observability Collection Parameters

| Parameter | Required | Description | Notes |
|-----------|----------|-------------|-------|
| `elb_id` | No | ELB ID for traffic/connection/latency metrics | Critical for full observability |
| `label_selector` | No | Pod label selector | Scope Pod metrics to workload |
| `aom_instance_id` | No | AOM instance ID | Auto-resolved if omitted |

### APM Injection Parameters

| Parameter | Required | Description | Notes |
|-----------|----------|-------------|-------|
| `app_name` | Yes | APM application name | - |
| `business` | Yes | APM business name | - |
| `env_name` | Yes | APM environment name | - |

### Report Generation Parameters

| Parameter | Required | Description | Notes |
|-----------|----------|-------------|-------|
| `result_path` | Yes | Path to run JSON file | Combine with observability JSON if available |

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

All actions return JSON with the following common structure:

| Field | Description |
|-------|-------------|
| `success` | Boolean: `true` if operation succeeded, `false` otherwise |
| `action` | Action name that was executed |
| `region` | Huawei Cloud region |

**Run JSON** (`huawei_run_cce_pressure_test` when `output_dir` is provided):

| Field | Description |
|-------|-------------|
| `job` | Job creation, completion, failure, and timeout state |
| `samples` | Workload replica and Pod count samples collected during the run |
| `metric_series` | Standardized replica curves from the run |
| `k6_summary` | Requests, RPS, success rate, latency percentiles, bytes, and max VUs parsed from k6 logs |
| `data_gaps` | Missing evidence that should be called out in the report |

**Observability JSON** (`huawei_collect_cce_pressure_test_observability`):

| Field | Description |
|-------|-------------|
| `inventory` | Pods, Services, and Ingresses in the workload namespace |
| `pod_metrics` | Node-backed Pod CPU and memory metrics |
| `elb_metrics` | ELB QPS, connections, latency, and response metrics when `elb_id` is provided |
| `elb_backend_status` | Backend member and health-monitor evidence |
| `metric_series` | Standardized curves consumed by the report action |

**Report Artifacts** (`huawei_generate_cce_pressure_test_report`):

| Artifact | Purpose |
|----------|---------|
| `*-report.md` | Portable Markdown report |
| `*-report.html` | Styled HTML report with risk-colored recommendations and data-gap tables |
| `*-curves.svg` | Embedded curve chart for traffic, latency, resources, and replicas |

See [Output Schema](references/output-schema.md) for the full JSON response schema.

## Verification

### Step-by-step Verification Checklist

1. Verify AK/SK credentials are configured via environment variables
2. Inspect existing Services, Ingresses, HPA, ingress controller, and ELB context
3. Confirm cluster, workload, namespace, target port, test window, traffic model, VUs, and output directory
4. Deploy Java sample (preview → confirm) if needed for an isolated lab
5. Create ELB (preview → confirm) if no reusable ingress-controller ELB exists
6. Prepare route (preview → confirm) — Service and Ingress
7. Inject APM Java agent (optional) for distributed tracing
8. Generate k6 client manifest — review ConfigMap and Job
9. Run pressure test (preview → confirm)
10. Collect observability with `elb_id` for full evidence
11. Generate report and review Markdown/HTML/SVG artifacts
12. For elasticity evaluation: run baseline → scale workload → run second phase → compare reports

## Best Practices

1. **Start with low traffic**: Always begin with low VUs and short duration to validate the traffic path before ramping up
2. **Preview before apply**: Always run mutation actions without `confirm=true` first, review the plan, then re-run with `confirm=true` after explicit user approval
3. **Use regional SWR images for k6**: Docker Hub images may timeout; mirror k6 to a regional SWR namespace
4. **Pass `elb_id` for observability**: ELB metrics (QPS, connections, latency, success rate) are critical evidence; always pass `elb_id` when collecting observability
5. **Run at least two phases for elasticity**: Baseline + scaled phase comparison is the standard methodology for evaluating autoscaling behavior
6. **Confirm test target before traffic**: Never send traffic to production paths without an approved test window
7. **Stop raising traffic when indicators degrade**: Halt when success rate drops, latency rises sharply, or resource waterlines exceed agreed limits
8. **Do not delete resources automatically**: Never auto-delete ELBs, namespaces, workloads, Jobs, or ConfigMaps

## Reference Documents

| Document | Description |
|----------|-------------|
| [Workflow](references/workflow.md) | Staged execution, action parameters, and command examples |
| [Risk Rules](references/risk-rules.md) | Preview-first constraints, mutation boundaries, and operational limits |
| [Output Schema](references/output-schema.md) | JSON response schema and report artifact structure |

## Notes

- **Preview-first by design** — Service/Ingress changes, traffic generation, and workload scaling return a preview without `confirm=true`; apply only after explicit user approval
- **Standard traffic path** — `Pod → Service → nginx-ingress → ELB`; the route preparation action discovers existing ingress controllers and does not silently create chargeable resources
- **ELB is chargeable** — creating a new ELB incurs hourly billing; always preview and confirm before creation
- **No credential persistence** — AK/SK exists only during API calls; never written to disk, logs, or reports
- **Cross-skill escalation** — If autoscaling does not respond during tests, hand off to `huawei-cloud-cce-autoscaling-diagnoser`; if Pods fail, hand off to `huawei-cloud-cce-pod-failure-diagnoser`

## Common Pitfalls

| Pitfall | Symptom | Quick Fix |
|---------|---------|-----------|
| Public Docker Hub k6 image | Image pull timeout in CCE | Mirror k6 image to regional SWR namespace |
| Missing ELB in traffic path | k6 client cannot reach workload | Create ELB or verify ingress-controller LoadBalancer IP |
| Ingress host mismatch | k6 requests rejected with 404 | Pass `host` during route prep and `host_header` to client |
| No observability without `elb_id` | Missing traffic/latency curves in report | Always pass `elb_id` to observability collection |
| Skipping baseline phase | Cannot evaluate elasticity improvement | Run baseline phase before scaling |
| Wrong `vip_subnet_cidr_id` | ELB creation fails | Use network ID from `huawei_list_vpc_subnets`, not subnet UUID |
| Production traffic without approval | Unintended load on production | Confirm test target and namespace before traffic generation |
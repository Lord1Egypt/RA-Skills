---
id: huawei-cloud-cce-metric-analyzer
name: huawei-cloud-cce-metric-analyzer
description: |
  Huawei Cloud CCE Metric analysis skill using Python SDK dispatcher.
  Use this skill when the user wants to: (1) query Pod/Node CPU/memory/disk metrics, (2) get resource usage TopN rankings, (3) query ECS/ELB/EIP/NAT cloud resource metrics, (4) aggregate cluster monitoring data with anomaly detection, (5) detect threshold-based resource anomalies.
  Trigger: user mentions "metric analysis", "指标分析", "CCE metrics", "CCE 指标", "AOM metrics", "AOM 指标", "resource metrics", "资源指标", "CPU usage", "CPU 使用率", "memory usage", "内存使用率", "performance monitoring", "性能监控", "TopN", "resource ranking", "资源排名"
tags: [cce, metrics, aom, observability, analysis]
---

# Huawei Cloud CCE Metric Analyzer

## Overview

Query and analyze metrics for CCE clusters (Pod/Node CPU/memory/disk) and cloud resources (ECS, ELB, EIP, NAT). Supports threshold-based anomaly detection, status classification (critical/warning/normal), and full-cluster monitoring aggregation.

**Architecture**: `python3 scripts/huawei-cloud.py` dispatcher → Huawei Cloud Python SDK + AOM Prometheus → Pod/Node metrics, ECS/ELB/EIP/NAT metrics → Threshold classification → Anomaly detection

**Related Skills**:
- `huawei-cloud-cce-pod-failure-diagnoser` - Pod CrashLoopBackOff, OOMKilled, restart storms
- `huawei-cloud-cce-node-failure-diagnoser` - Node health, resource pressure diagnosis
- `huawei-cloud-cce-kubernetes-event-analyzer` - Warning events, failure patterns
- `huawei-cloud-cce-capacity-trend-forecaster` - Capacity planning and trend forecasting
- `huawei-cloud-cce-cost-optimization-advisor` - Resource cost optimization
- `huawei-cloud-cce-auto-remediation-runner` - Remediation actions (scale, resize, drain)

**Capabilities**:
- Pod CPU/memory TopN ranking and single Pod time-series metrics
- Node CPU/memory/disk TopN ranking and single Node time-series metrics
- ECS instance CPU/memory/disk/network metrics
- ELB connection, bandwidth, QPS metrics
- EIP bandwidth, traffic, packet loss metrics
- NAT Gateway SNAT connection metrics
- Full-cluster monitoring aggregation with anomaly detection (80% threshold)
- Threshold-based status classification (critical/warning/normal/unknown)

**Typical Use Cases**:

- "Show Pods with the highest CPU usage in my cluster"
- "Get Node memory usage ranking"
- "Check ECS instance resource metrics"
- "What is the ELB QPS for my load balancer?"
- "Show EIP bandwidth usage"
- "Aggregate all monitoring data for the cluster"
- "Which resources have exceeded critical thresholds?"
- "Detect resource anomalies in the last hour"

## Prerequisites

### 1. Python Dependencies

- Python 3.8+ with `huaweicloudsdkcce`, `huaweicloudsdkcore`, `huaweicloudsdkaom`, `huaweicloudsdkces` packages
- Run environment check before first use (see Verification section)

### 2. Credential Configuration

- Valid Huawei Cloud credentials (AK/SK mode)
- **Security Rules**:
  - 🚫 Never expose AK/SK values in code, conversation, or commands
  - 🚫 Never use `echo $HUAWEI_AK` or `echo $HUAWEI_SK` to check credentials
  - ✅ Use environment variables: `HUAWEI_AK`, `HUAWEI_SK`, `HUAWEI_REGION`
  - ✅ Prefer IAM users over root account for cloud operations
  - ✅ Enable MFA for sensitive operations

**Configuration Method** (Environment Variables Only):

```bash
export HUAWEI_AK=<your-ak>
export HUAWEI_SK=<your-sk>
export HUAWEI_REGION=cn-north-4
```

**⚠️ Important Security Notes**:

- Never commit credentials to version control
- Use IAM users with minimal required permissions
- Enable MFA for sensitive operations
- Rotate AK/SK regularly

### 3. IAM Permission Requirements

| API Action                      | Permission          | Purpose                                    |
| ------------------------------- | ------------------- | ------------------------------------------ |
| `cce:cluster:get`               | Get cluster         | View CCE cluster details                   |
| `aom:instance:list`             | List AOM instances  | Discover AOM Prometheus instance for metrics |
| `aom:metricsData:get`           | Get metrics data    | Query Pod/Node CPU/memory/disk metrics     |
| `ces:metricsData:get`           | Get CES metrics     | Query ECS/ELB/EIP/NAT cloud resource metrics |
| `ecs:cloudServers:list`         | List ECS servers    | Correlate ECS instance IDs                 |
| `elb:loadbalancers:list`        | List ELB instances  | Correlate ELB IDs                          |
| `vpc:eips:list`                 | List EIPs           | Correlate EIP IDs                          |
| `nat:natGateways:list`          | List NAT Gateways   | Correlate NAT Gateway IDs                  |

**Permission Failure Handling**:

1. When any command fails due to IAM permission errors, display the required permission list
2. Guide the user to create a custom policy in the IAM console and grant authorization
3. Pause execution and wait for user confirmation that permissions have been granted

## Core Commands

All commands use the Python dispatcher script: `python3 scripts/huawei-cloud.py <action> <key=value>...`

### 1. CCE Pod Metrics

```bash
# Pod TopN — cluster-wide CPU/memory ranking
python3 scripts/huawei-cloud.py huawei_get_cce_pod_metrics_topN \
  region=cn-north-4 cluster_id=<cluster-id> \
  namespace=default top_n=10 hours=1

# Pod TopN with label selector
python3 scripts/huawei-cloud.py huawei_get_cce_pod_metrics_topN \
  region=cn-north-4 cluster_id=<cluster-id> \
  namespace=default label_selector="app=nginx,version=v1" top_n=10 hours=1

# Single Pod time-series
python3 scripts/huawei-cloud.py huawei_get_cce_pod_metrics \
  region=cn-north-4 cluster_id=<cluster-id> \
  pod_name=my-app-xxx namespace=default hours=1
```

### 2. CCE Node Metrics

```bash
# Node TopN — cluster-wide CPU/memory/disk ranking
python3 scripts/huawei-cloud.py huawei_get_cce_node_metrics_topN \
  region=cn-north-4 cluster_id=<cluster-id> \
  top_n=10 hours=1

# Single Node time-series
python3 scripts/huawei-cloud.py huawei_get_cce_node_metrics \
  region=cn-north-4 cluster_id=<cluster-id> \
  node_ip=10.0.0.1 hours=1
```

### 3. Cloud Resource Metrics

```bash
# ECS instance metrics
python3 scripts/huawei-cloud.py huawei_get_ecs_metrics \
  region=cn-north-4 instance_id=<instance-id>

# ELB metrics
python3 scripts/huawei-cloud.py huawei_get_elb_metrics \
  region=cn-north-4 elb_id=<loadbalancer-id> hours=1

# EIP metrics
python3 scripts/huawei-cloud.py huawei_get_eip_metrics \
  region=cn-north-4 eip_id=<eip-id> hours=1

# NAT Gateway metrics
python3 scripts/huawei-cloud.py huawei_get_nat_gateway_metrics \
  region=cn-north-4 nat_gateway_id=<nat-gateway-id> hours=1
```

### 4. Cluster Monitoring Aggregation

```bash
# Aggregate all monitoring data with anomaly detection
python3 scripts/huawei-cloud.py huawei_cce_cluster_monitoring_aggregation \
  region=cn-north-4 cluster_id=<cluster-id> \
  start_time="2026-05-30 00:00:00" end_time="2026-05-30 23:59:59" \
  namespace=default top_n=10
```

This tool aggregates: Pod TopN CPU/memory, Node TopN CPU/memory/disk, ELB metrics (with LoadBalancer service association), NAT Gateway metrics, EIP metrics (bandwidth, packet loss), and anomaly detection using 80% threshold.

## Parameter Reference

### Common Parameters

| Parameter    | Required/Optional | Description          | Default         |
| ------------ | ----------------- | -------------------- | --------------- |
| `region`     | Required          | Huawei Cloud region  | `HUAWEI_REGION` |
| `cluster_id` | Required          | CCE cluster ID       | N/A             |
| `namespace`  | Recommended       | Kubernetes namespace | `default`       |
| `ak`         | Optional          | Override AK          | `HUAWEI_AK`     |
| `sk`         | Optional          | Override SK          | `HUAWEI_SK`     |
| `project_id` | Optional          | Project ID           | Auto from IAM   |

### `huawei_get_cce_pod_metrics_topN` Parameters

| Parameter       | Required | Description                     | Default  |
| --------------- | -------- | ------------------------------- | -------- |
| `namespace`     | No       | Namespace filter                | all      |
| `label_selector`| No       | Label selector (e.g. app=web)  | N/A      |
| `top_n`         | No       | Number of top items             | 10       |
| `hours`         | No       | Metrics lookback hours          | 1        |
| `node_ip`       | No       | Filter Pods on specific node    | N/A      |
| `cpu_query`     | No       | Custom CPU PromQL               | Auto     |
| `memory_query`  | No       | Custom memory PromQL            | Auto     |

### `huawei_get_cce_pod_metrics` Parameters

| Parameter    | Required | Description                | Default  |
| ------------ | -------- | -------------------------- | -------- |
| `pod_name`   | Yes      | Target Pod name            | N/A      |
| `namespace`  | No       | Namespace                  | `default`|
| `hours`      | No       | Metrics lookback hours     | 1        |

### `huawei_get_cce_node_metrics_topN` Parameters

| Parameter   | Required | Description                 | Default  |
| ----------- | -------- | --------------------------- | -------- |
| `top_n`     | No       | Number of top items         | 10       |
| `hours`     | No       | Metrics lookback hours      | 1        |

### `huawei_get_cce_node_metrics` Parameters

| Parameter  | Required | Description                 | Default  |
| ---------- | -------- | --------------------------- | -------- |
| `node_ip`  | Yes      | Target Node IP              | N/A      |
| `hours`    | No       | Metrics lookback hours      | 1        |

### `huawei_get_ecs_metrics` Parameters

| Parameter     | Required | Description                | Default  |
| ------------- | -------- | -------------------------- | -------- |
| `instance_id` | Yes      | ECS instance ID            | N/A      |

### `huawei_get_elb_metrics` Parameters

| Parameter | Required | Description                | Default  |
| --------- | -------- | -------------------------- | -------- |
| `elb_id`  | Yes      | ELB loadbalancer ID        | N/A      |
| `hours`   | No       | Metrics lookback hours     | 1        |

### `huawei_get_eip_metrics` Parameters

| Parameter | Required | Description                | Default  |
| --------- | -------- | -------------------------- | -------- |
| `eip_id`  | Yes      | EIP ID                     | N/A      |
| `hours`   | No       | Metrics lookback hours     | 1        |

### `huawei_get_nat_gateway_metrics` Parameters

| Parameter        | Required | Description                | Default  |
| ---------------- | -------- | -------------------------- | -------- |
| `nat_gateway_id` | Yes      | NAT Gateway ID             | N/A      |
| `hours`          | No       | Metrics lookback hours     | 1        |

### `huawei_cce_cluster_monitoring_aggregation` Parameters

| Parameter     | Required | Description                     | Default  |
| ------------- | -------- | ------------------------------- | -------- |
| `start_time`  | Yes      | Start time (YYYY-MM-DD HH:MM:SS)| N/A      |
| `end_time`    | Yes      | End time (YYYY-MM-DD HH:MM:SS)  | N/A      |
| `namespace`   | No       | Namespace filter                | `default`|
| `top_n`       | No       | Number of top items             | 10       |

## Output Format

See [Output Schema](references/output-schema.md) for the complete JSON response structure.

**Key output fields**:
- `success` — boolean, true if query completed
- `region` — Huawei Cloud region
- `cluster_id` / `cluster_name` — CCE cluster identity
- `aom_instance_id` — AOM Prometheus instance used for metric queries
- `metrics` — Dict with cpu/memory/disk data per resource, including status classification
- `time_series` — Historical data points with `timestamp`, `time`, `average`, `min`, `max`
- `status` — Threshold classification: `critical` (>80% CPU, >85% memory/disk), `warning` (>50% CPU/memory, >70% disk), `normal` (below warning), `unknown` (no data)

**Cloud resource metric fields** (ECS/ELB/EIP/NAT):
- ECS: `cpu_util`, `mem_util`, `disk_util`, `network_incoming/outgoing_bytes_rate`, `disk_read/write_bytes_rate`
- ELB: `m1_cps`, `m14_l7_rt`, `mb_l7_qps`, `mc-me-mf_l7_http_2xx-5xx`
- EIP: `upstream/downstream_bandwidth`, `upstream/downstream_bandwidth_usage`, `upstream/downstream_traffic`, `packet_loss_rate`
- NAT: `snat_connection`, `inbound/outbound_bandwidth`, `snat_connection_ratio`

## Verification

1. Run `python3 scripts/huawei-cloud.py huawei_get_cce_pod_metrics_topN region=cn-north-4 cluster_id=<cluster-id> namespace=default top_n=5` to verify Pod metric queries
2. Run `python3 scripts/huawei-cloud.py huawei_get_cce_node_metrics_topN region=cn-north-4 cluster_id=<cluster-id> top_n=5` to verify Node metric queries
3. Run `python3 scripts/huawei-cloud.py huawei_get_ecs_metrics region=cn-north-4 instance_id=<instance-id>` to verify CES metric connectivity

## Best Practices

1. **Start with TopN for cluster-wide overview** — use Pod/Node TopN before drilling into individual resources
2. **Time-bound queries** — keep `hours` small (1-4) for recent analysis; cap at 24 hours for historical reviews
3. **Use namespace filtering** — always provide `namespace` to reduce noise in Pod TopN results
4. **Check status classification** — focus on `critical` and `warning` resources first; `normal` resources can be skipped
5. **Use aggregation for full-cluster health checks** — `huawei_cce_cluster_monitoring_aggregation` gives a one-shot overview of all resource metrics with anomaly detection
6. **Correlate with events** — if metrics show anomalies, check `huawei-cloud-cce-kubernetes-event-analyzer` for related warning events
7. **Hand off, don't remediate** — this skill is read-only; hand off to diagnosis skills for root cause analysis
8. **Sanitize output** — do not expose production pod names, node IPs, or cluster IDs in public summaries; use redacted examples

## Reference Documents

| Document                                | Description                              |
| --------------------------------------- | ---------------------------------------- |
| [Workflow](references/workflow.md)      | Metric query sequence, Pod/Node workflows, threshold detection, next-step handoff |
| [Risk Rules](references/risk-rules.md)  | Read-only constraints, data redaction rules, time-bounding, threshold caveats |
| [Output Schema](references/output-schema.md) | JSON response format for CCE metrics, cloud resource metrics, time-series, status values |

## Notes

- This skill is **strictly read-only** — it only queries and analyzes metrics; no modifications are made to resources or configurations
- Thresholds (CPU >80%, Memory >85%, Disk >85%) are **predefined baselines** — actual thresholds may vary by workload SLO; recommend users customize thresholds based on their specific requirements
- AK/SK must **never** be hardcoded — use environment variables only
- The Python dispatcher script (`scripts/huawei-cloud.py`) is the **only execution method** — do not use hcloud CLI or direct API calls for metric queries
- AOM Prometheus instance is **auto-discovered** — no need to manually specify `aom_instance_id`
- Cloud resource metrics (ECS/ELB/EIP/NAT) use CES (Cloud Eye Service), not AOM
- Do not make automatic scaling or remediation decisions based solely on metric analysis — forward to `huawei-cloud-cce-auto-remediation-runner` only if explicitly requested and validated

## Common Pitfalls

| Pitfall                                    | Symptom                               | Quick Fix                                    |
| ------------------------------------------ | ------------------------------------- | -------------------------------------------- |
| Missing `cluster_id`                       | Action fails immediately              | Provide `cluster_id` from cluster listing    |
| AOM Prometheus instance not found          | Metric queries return empty results   | Ensure AOM Prom instance is created for the cluster; check `aom:instance:list` permission |
| Large time window without namespace filter | Slow response, too many results       | Narrow `hours` to 1-4 and add `namespace` filter |
| Cloud resource ID not found                | ECS/ELB/EIP/NAT query returns error   | Verify resource ID exists; check CES IAM permission |
| Custom PromQL syntax error                 | `cpu_query` / `memory_query` returns empty | Use default auto-generated PromQL; only customize if familiar with AOM PromQL syntax |
| Permission denied on CES metrics           | Cloud resource metrics fail           | Verify `ces:metricsData:get` IAM permission |
| Aggregation missing time range             | `start_time` / `end_time` required but not provided | Always specify both time boundaries for aggregation queries |
| Node IP format mismatch                    | Single Node metrics fail              | Use the exact node IP as shown in cluster node listing (e.g. `10.0.0.1`) |
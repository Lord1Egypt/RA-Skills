---
name: metric-analyzer
description: Use this skill to query and analyze metrics for CCE clusters and cloud resources, including Pod, Node, ECS, ELB, EIP, and NAT usage, plus threshold-based anomaly detection and status classification.
---

# Metric Analyzer

Query and analyze metrics for CCE clusters (Pod/Node) and cloud resources (ECS, ELB, EIP, NAT). Supports threshold-based anomaly detection and status classification.

## Scope

Use this skill when the user asks to:

- Get Pod CPU/memory usage ranking in a CCE cluster
- Get Node CPU/memory/disk usage ranking in a CCE cluster
- Query specific Pod or Node metrics time-series
- Check which Pods/Nodes are consuming the most resources
- Get ECS instance CPU/memory/disk/network metrics
- Get ELB connection, bandwidth, QPS metrics
- Get EIP bandwidth and traffic metrics
- Get NAT Gateway SNAT connection metrics
- Detect resource anomalies via threshold-based classification

This skill is read-only. It does not modify resources or configurations.

## Tools

### CCE Metrics

| Tool | Purpose | Required parameters |
|------|---------|---------------------|
| `huawei_get_cce_pod_metrics_topN` | Get Pod CPU/memory TopN | `region`, `cluster_id` |
| `huawei_get_cce_pod_metrics` | Get single Pod time-series | `region`, `cluster_id`, `pod_name` |
| `huawei_get_cce_node_metrics_topN` | Get Node CPU/memory/disk TopN | `region`, `cluster_id` |
| `huawei_get_cce_node_metrics` | Get single Node time-series | `region`, `cluster_id`, `node_ip` |

### Cloud Resource Metrics

| Tool | Purpose | Required parameters |
|------|---------|---------------------|
| `huawei_get_ecs_metrics` | Get ECS CPU/memory/disk/network metrics | `region`, `instance_id` |
| `huawei_get_elb_metrics` | Get ELB connections, bandwidth, QPS | `region`, `elb_id` |
| `huawei_get_eip_metrics` | Get EIP bandwidth, traffic, packet rate | `region`, `eip_id` |
| `huawei_get_nat_gateway_metrics` | Get NAT SNAT connections, bandwidth | `region`, `nat_gateway_id` |

### Aggregation Tool

| Tool | Purpose | Required parameters |
|------|---------|---------------------|
| `huawei_cce_cluster_monitoring_aggregation` | Aggregate all cluster monitoring with anomaly detection | `region`, `cluster_id`, `start_time`, `end_time` |

## Usage

### CCE Pod Metrics

```bash
# Pod TopN
python3 scripts/huawei-cloud.py huawei_get_cce_pod_metrics_topN \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  namespace=default \
  top_n=10 \
  hours=1

# Single Pod
python3 scripts/huawei-cloud.py huawei_get_cce_pod_metrics \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  pod_name=<pod-name> \
  namespace=default \
  hours=1
```

### CCE Node Metrics

```bash
# Node TopN
python3 scripts/huawei-cloud.py huawei_get_cce_node_metrics_topN \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  top_n=10 \
  hours=1

# Single Node
python3 scripts/huawei-cloud.py huawei_get_cce_node_metrics \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  node_ip=<node-ip> \
  hours=1
```

### ECS Metrics

```bash
python3 scripts/huawei-cloud.py huawei_get_ecs_metrics \
  region=cn-north-4 \
  instance_id=<instance-id>
```

### ELB Metrics

```bash
python3 scripts/huawei-cloud.py huawei_get_elb_metrics \
  region=cn-north-4 \
  elb_id=<loadbalancer-id> \
  hours=1
```

### EIP Metrics

```bash
python3 scripts/huawei-cloud.py huawei_get_eip_metrics \
  region=cn-north-4 \
  eip_id=<eip-id> \
  hours=1
```

### NAT Gateway Metrics

```bash
python3 scripts/huawei-cloud.py huawei_get_nat_gateway_metrics \
  region=cn-north-4 \
  nat_gateway_id=<nat-gateway-id> \
  hours=1
```

### Cluster Monitoring Aggregation

```bash
# Aggregate all monitoring data for a cluster with anomaly detection
python3 scripts/huawei-cloud.py huawei_cce_cluster_monitoring_aggregation \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  start_time="2026-05-30 00:00:00" \
  end_time="2026-05-30 23:59:59" \
  namespace=default \
  top_n=10
```

This tool aggregates:
- Pod metrics (TopN CPU/memory)
- Node metrics (TopN CPU/memory/disk)
- ELB metrics (with LoadBalancer service association)
- NAT Gateway metrics
- EIP metrics (bandwidth, packet loss)
- Anomaly detection using 80% threshold

## Analysis Guidance

1. **Review results**: Focus on resources with high utilization or abnormal patterns
2. **Check thresholds**: CPU >80%, Memory >85% typically marked as critical
3. **Identify affected workloads**: Correlate high resource usage with application issues
4. **Correlate with events**: If metrics show anomalies, check `kubernetes-event-analyzer`

## Output Format

| Field | Description |
|-------|-------------|
| `success` | Query success status |
| `region` | Cloud region |
| `metrics` | Resource-specific metrics with values and units |
| `time_series` | Historical data points (where available) |

## References

- Workflow: `references/workflow.md`
- Risk rules: `references/risk-rules.md`
- Output schema: `references/output-schema.md`

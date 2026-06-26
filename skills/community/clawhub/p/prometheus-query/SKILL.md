---
name: prometheus
description: Query Prometheus monitoring metrics, alerts, and cluster status. Use when user needs to: (1) Query firing/pending alerts, (2) Check cluster/node/pod status, (3) Get nginx request metrics, (4) Query any PromQL metrics from Prometheus, (5) Monitor system health and performance. Accepts parameters like metric_name, query_type, time_range, prom_url.
---

# Prometheus Monitoring Query

Query metrics, alerts, and cluster status from Prometheus.

## Two Access Modes

### 1. Direct URL Access (Recommended)

Use when Prometheus is accessible via network (cloud service, remote server, etc.):

```bash
# Using remote Prometheus URL
python scripts/query_prometheus.py \
  --prom-url "https://prometheus.example.com" \
  --query "up"

# Query alerts
python scripts/query_prometheus.py \
  --prom-url "https://prometheus.example.com" \
  --alerts
```

### 2. Kubernetes Port-Forward

Use when Prometheus is only accessible via kubectl:

```bash
# Terminal 1: Port-forward Prometheus
kubectl port-forward -n prometheus svc/prometheus 9090:9090

# Terminal 2: Query metrics
python scripts/query_prometheus.py \
  --prom-url "http://localhost:9090" \
  --query "up"
```

## Query Script

Use `scripts/query_prometheus.py` to query metrics:

```bash
# Query a specific metric (default: http://localhost:9090)
python scripts/query_prometheus.py --query "up"

# Explicit URL
python scripts/query_prometheus.py \
  --prom-url "http://localhost:9090" \
  --query "rate(http_requests_total[5m])"

# Query alerts
python scripts/query_prometheus.py --alerts
```

**Default:** If `--prom-url` is not specified, uses `http://localhost:9090`.

## Common Query Types

### Alerts

```promql
# All firing alerts
ALERTS{alertstate="firing"}

# Pending alerts
ALERTS{alertstate="pending"}
```

### Cluster Status

```promql
# Node status
kube_node_status_condition{condition="Ready"}

# Pod status
kube_pod_status_phase{phase="Running"}
kube_pod_status_phase{phase="Failed"}

# Namespace pod counts
count by (namespace) (kube_pod_info)
```

### Nginx Metrics

```promql
# Request rate
rate(nginx_http_requests_total[5m])

# Connection stats
nginx_connections_active
nginx_connections_reading
nginx_connections_writing
nginx_connections_waiting

# Request duration (p99)
histogram_quantile(0.99, rate(nginx_http_request_duration_seconds_bucket[5m]))
```

### Custom Metrics

Replace `<metric_name>` with your actual metric:

```promql
# Current value
<metric_name>

# Rate over 5 minutes
rate(<metric_name>[5m])

# Average over 1 hour
avg(<metric_name>[1h])
```

## Parameters

- `prom-url`: Prometheus URL (default: http://localhost:9090)
- `query`: PromQL query string
- `alerts`: Flag to query all alerts with states
- `time`: Evaluation timestamp (ISO 8601)
- `start`: Start time for range query
- `end`: End time for range query
- `step`: Query resolution step (for range queries)
- `timeout`: Query timeout in seconds (default: 30)

## Output

Returns formatted metric results. For instant queries, returns current values. For alerts, returns alert name, state (firing/pending), and labels.

## Examples

### Check cluster health

```bash
# All firing alerts
python scripts/query_prometheus.py --alerts

# Node status
python scripts/query_prometheus.py --query "kube_node_status_condition{condition='Ready'}"
```

### Nginx load

```bash
# Request rate
python scripts/query_prometheus.py --query "rate(nginx_http_requests_total[5m])"

# Active connections
python scripts/query_prometheus.py --query "nginx_connections_active"
```

### Custom metric

```bash
python scripts/query_prometheus.py --query "my_custom_metric"
python scripts/query_prometheus.py --query "rate(my_custom_metric[5m])"
```
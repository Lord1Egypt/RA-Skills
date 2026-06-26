---
name: kubeblocks-setup-monitoring
metadata:
  version: "0.1.0"
description: Set up monitoring and observability for KubeBlocks database clusters using the Prometheus Operator stack. Covers ServiceMonitor configuration, Prometheus scraping, and Grafana dashboard integration. Use when the user wants to monitor, observe, set up metrics, alerts, dashboards, or enable observability for database clusters. NOT for application-level monitoring or for KubeBlocks operator monitoring itself.
---

# Set Up Monitoring for KubeBlocks Clusters

## Overview

KubeBlocks database clusters export Prometheus-compatible metrics. This skill sets up a monitoring stack using Prometheus Operator and Grafana to collect and visualize database metrics.

Official docs: https://kubeblocks.io/docs/preview/user_docs/observability/monitor-database

## Workflow

```
- [ ] Step 1: Install Prometheus stack
- [ ] Step 2: Create PodMonitor for database clusters
- [ ] Step 3: Verify metrics collection
- [ ] Step 4: Access Grafana dashboards
```

## Step 1: Install Prometheus Stack

Install the kube-prometheus-stack which includes Prometheus Operator, Prometheus, Grafana, and Alertmanager:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace \
  --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false
```

The `NilUsesHelmValues=false` settings ensure Prometheus discovers PodMonitors/ServiceMonitors from all namespaces, not just those with the `release: prometheus` label.

Wait for pods to be ready:

```bash
kubectl get pods -n monitoring -w
```

Expected pods:
- `prometheus-kube-prometheus-operator-*`
- `prometheus-prometheus-kube-prometheus-prometheus-0`
- `prometheus-grafana-*`
- `alertmanager-prometheus-kube-prometheus-alertmanager-0`

## Step 2: Create PodMonitor

Create a `PodMonitor` to tell Prometheus where to scrape database metrics:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: kb-database-monitor
  namespace: monitoring
  labels:
    release: prometheus
spec:
  namespaceSelector:
    matchNames:
    - <ns>    # namespace where your database cluster runs
  selector:
    matchLabels:
      app.kubernetes.io/managed-by: kubeblocks
  podMetricsEndpoints:
  - port: http-metrics
    path: /metrics
    interval: 30s
```

Apply it:

```bash
kubectl apply -f podmonitor.yaml
```

### Monitor All Namespaces

To monitor KubeBlocks clusters across all namespaces:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: kb-database-monitor-all
  namespace: monitoring
  labels:
    release: prometheus
spec:
  namespaceSelector:
    any: true
  selector:
    matchLabels:
      app.kubernetes.io/managed-by: kubeblocks
  podMetricsEndpoints:
  - port: http-metrics
    path: /metrics
    interval: 30s
```

### Per-Component PodMonitor

For more granular control, target a specific component:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: kb-mysql-monitor
  namespace: monitoring
  labels:
    release: prometheus
spec:
  namespaceSelector:
    matchNames:
    - <ns>
  selector:
    matchLabels:
      app.kubernetes.io/managed-by: kubeblocks
      apps.kubeblocks.io/component-name: <component>
      app.kubernetes.io/instance: <cluster>
  podMetricsEndpoints:
  - port: http-metrics
    path: /metrics
    interval: 15s
```

## Step 3: Verify Metrics Collection

### Check PodMonitor is Discovered

```bash
kubectl get podmonitor -n monitoring
```

### Query Prometheus Directly

Port-forward to Prometheus:

```bash
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
```

Then open http://localhost:9090 in a browser, or test with curl:

```bash
# Check targets (should show your database pods)
curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | select(.labels.app_kubernetes_io_managed_by == "kubeblocks") | {instance: .labels.instance, health: .health}'

# Query a sample metric
curl -s 'http://localhost:9090/api/v1/query?query=up{app_kubernetes_io_managed_by="kubeblocks"}' | jq '.data.result'
```

### Common KubeBlocks Metrics

| Addon | Example Metrics |
|-------|-----------------|
| MySQL | `mysql_global_status_threads_connected`, `mysql_global_status_queries` |
| PostgreSQL | `pg_stat_activity_count`, `pg_stat_database_tup_returned` |
| Redis | `redis_connected_clients`, `redis_used_memory_bytes` |
| MongoDB | `mongodb_connections_current`, `mongodb_op_counters_total` |

## Step 4: Access Grafana

### Port-Forward to Grafana

```bash
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```

Open http://localhost:3000 in a browser.

### Default Credentials

```
Username: admin
Password: prom-operator
```

Get the password programmatically:

```bash
kubectl get secret -n monitoring prometheus-grafana \
  -o jsonpath='{.data.admin-password}' | base64 -d
```

### Import Database Dashboards

Grafana comes with some built-in dashboards. For database-specific dashboards, import from Grafana.com:

| Dashboard | Grafana ID | Addon |
|-----------|-----------|-------|
| MySQL Overview | 7362 | MySQL |
| PostgreSQL Database | 9628 | PostgreSQL |
| Redis Dashboard | 763 | Redis |
| MongoDB Overview | 2583 | MongoDB |

To import: Grafana → Dashboards → Import → Enter the ID → Select Prometheus data source → Import.

## Troubleshooting

**No metrics appearing in Prometheus:**
- Check PodMonitor labels match: `release: prometheus` must be present
- Verify the metrics port name: `kubectl get pods <pod> -n <ns> -o jsonpath='{.spec.containers[*].ports[*]}'`
- Some addons use different port names; check with: `kubectl describe pod <pod> -n <ns> | grep -A 2 "Port:"`

**Targets show as DOWN in Prometheus:**
- Check pod network connectivity from the monitoring namespace
- Verify the metrics endpoint responds: `kubectl exec -it <pod> -n <ns> -- curl -s localhost:9104/metrics | head`

**Grafana cannot reach Prometheus:**
- Verify Prometheus service: `kubectl get svc -n monitoring | grep prometheus`
- The default data source URL is `http://prometheus-kube-prometheus-prometheus.monitoring:9090`

## Additional Reference

For per-addon exporter details (port names, port numbers, metrics paths), custom alerting rule examples (MySQL, PostgreSQL, Redis), and extended Grafana dashboard IDs, see [reference.md](references/reference.md).

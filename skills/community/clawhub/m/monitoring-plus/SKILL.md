---
name: monitoring-plus
description: "Enhanced monitoring with Prometheus, Grafana, Loki, alerting rules, dashboard templates, and SLO/SLI tracking."
metadata:
  author: opencode
  version: 2.0
  tags: monitoring, prometheus, grafana, alerting, observability
  compatibility: opencode
  license: MIT
---

# Monitoring Plus

Enhanced monitoring with Prometheus, Grafana, alerting rules, and SLO tracking.

## Features

- **Prometheus**: Metrics collection and querying
- **Grafana**: Visualization and dashboards
- **Loki**: Log aggregation
- **Alerting**: Rules, routing, escalation
- **SLO/SLI**: Service level tracking

## Quick Reference

| Component | Purpose | Port |
|-----------|---------|------|
| Prometheus | Metrics | 9090 |
| Grafana | Dashboards | 3000 |
| Loki | Logs | 3100 |
| Alertmanager | Alerts | 9093 |

## Prometheus

### Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

scrape_configs:
  - job_name: 'app'
    static_configs:
      - targets: ['app:8080']
    metrics_path: /metrics
  
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
```

### Metrics Types

```promql
# Counter
http_requests_total{method="GET", status="200"}

# Gauge
node_memory_MemAvailable_bytes

# Histogram
http_request_duration_seconds_bucket{le="0.5"}

# Summary
http_request_duration_seconds{quantile="0.99"}
```

### Useful Queries

```promql
# Request rate
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])

# Latency p95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Memory usage
process_resident_memory_bytes / 1024 / 1024

# CPU usage
rate(process_cpu_seconds_total[5m])
```

## Grafana

### Dashboard JSON

```json
{
  "dashboard": {
    "title": "Application Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~'5..'}[5m]) / rate(http_requests_total[5m])",
            "legendFormat": "Error %"
          }
        ]
      },
      {
        "title": "Latency P95",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "P95"
          }
        ]
      }
    ]
  }
}
```

## Alerting Rules

### Prometheus Rules

```yaml
# alert_rules.yml
groups:
  - name: app_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "P95 latency is {{ $value }}s"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "{{ $labels.instance }} has been down for more than 1 minute"

      - alert: HighMemoryUsage
        expr: process_resident_memory_bytes / 1024 / 1024 > 512
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value }}MB"
```

### Alertmanager Configuration

```yaml
# alertmanager.yml
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'alerts@example.com'
  smtp_auth_username: 'alerts@example.com'
  smtp_auth_password: 'password'

route:
  group_by: ['alertname', 'severity']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: 'pager'
    - match:
        severity: warning
      receiver: 'slack'

receivers:
  - name: 'default'
    email_configs:
      - to: 'team@example.com'

  - name: 'pager'
    pagerduty_configs:
      - service_key: 'your-pagerduty-key'

  - name: 'slack'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/xxx'
        channel: '#alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ .CommonAnnotations.description }}'
```

## Loki

### Configuration

```yaml
# loki-config.yml
auth_enabled: false

server:
  http_listen_port: 3100

common:
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    kvstore:
      store: inmemory

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h
```

### LogQL Queries

```logql
# Filter by label
{job="app"}

# Filter by keyword
{job="app"} |= "error"

# Regex filter
{job="app"} |= `error|warn`

# Metric query
rate({job="app"} |= "error" [5m])

# Histogram
histogram_quantile(0.99, sum(rate({job="app"} |= "error" [5m])) by (le))
```

## SLO/SLI Tracking

### SLI Definitions

```yaml
# sli-config.yml
slis:
  - name: availability
    description: "Percentage of successful requests"
    sli:
      type: "success_rate"
      good_query: "sum(rate(http_requests_total{status!~'5..'}[5m]))"
      total_query: "sum(rate(http_requests_total[5m]))"
    slos:
      - target: 0.99
        window: "30d"
      - target: 0.999
        window: "7d"

  - name: latency
    description: "Percentage of requests under 500ms"
    sli:
      type: "latency"
      query: "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
    slos:
      - target: 0.95
        threshold: 0.5
        window: "30d"
```

### Error Budget

```promql
# Error budget remaining
slo:availability:sli{job="app"} - 0.99

# Burn rate
(1 - slo:availability:sli{job="app"}) / (1 - 0.99)
```

## Dashboard Templates

### Application Dashboard

```json
{
  "panels": [
    {"title": "Request Rate", "type": "graph", "expr": "rate(http_requests_total[5m])"},
    {"title": "Error Rate", "type": "graph", "expr": "rate(http_requests_total{status=~'5..'}[5m]) / rate(http_requests_total[5m])"},
    {"title": "Latency P50/P95/P99", "type": "graph", "expr": "histogram_quantile(0.5/0.95/0.99, rate(http_request_duration_seconds_bucket[5m]))"},
    {"title": "CPU Usage", "type": "gauge", "expr": "rate(process_cpu_seconds_total[5m])"},
    {"title": "Memory Usage", "type": "gauge", "expr": "process_resident_memory_bytes / 1024 / 1024"}
  ]
}
```

## Best Practices

1. **Alert on symptoms** - User impact, not causes
2. **Include runbooks** - What to do when alert fires
3. **Set appropriate severity** - Not everything is P1
4. **Use recording rules** - Pre-compute expensive queries
5. **Monitor from outside** - External synthetic monitoring
6. **Set SLOs** - Define reliability targets
7. **Track error budgets** - Balance reliability vs velocity
8. **Log structured data** - JSON logs for easy parsing

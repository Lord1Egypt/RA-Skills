# Prometheus + Grafana Stack

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Your App   │     │ Node        │     │ Postgres    │
│ /metrics    │     │ Exporter    │     │ Exporter    │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┴───────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Prometheus │ ← scrapes metrics
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐ ┌───▼───┐ ┌──────▼──────┐
       │   Grafana   │ │ Loki  │ │Alertmanager │
       │ (dashboards)│ │(logs) │ │  (alerts)   │
       └─────────────┘ └───────┘ └─────────────┘
```

## Docker Compose Setup

```yaml
services:
  prometheus:
    image: prom/prometheus:v2.50.1
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./rules:/etc/prometheus/rules
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=30d'
      - '--web.enable-lifecycle'
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:10.3.3
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASS}
    ports:
      - "3000:3000"

  alertmanager:
    image: prom/alertmanager:v0.27.0
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
    ports:
      - "9093:9093"

  node_exporter:
    image: prom/node-exporter:v1.7.0
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'

volumes:
  prometheus_data:
  grafana_data:
```

## prometheus.yml

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - /etc/prometheus/rules/*.yml

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['node_exporter:9100']

  - job_name: 'app'
    static_configs:
      - targets: ['app:8080']
```

## Essential Exporters

| Exporter | Port | Use Case |
|----------|------|----------|
| node_exporter | 9100 | Host metrics (CPU, RAM, disk) |
| cadvisor | 8080 | Docker container metrics |
| postgres_exporter | 9187 | PostgreSQL |
| redis_exporter | 9121 | Redis |
| blackbox_exporter | 9115 | HTTP/TCP probes |
| nginx_exporter | 9113 | Nginx |

## Alert Rules Example

```yaml
# rules/alerts.yml
groups:
  - name: instance
    rules:
      - alert: InstanceDown
        expr: up == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Instance {{ $labels.instance }} down"
          
      - alert: HighCPU
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU on {{ $labels.instance }}"
          
      - alert: DiskSpaceLow
        expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 < 15
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Disk space low on {{ $labels.instance }}"
```

## Useful PromQL Queries

```promql
# CPU usage %
100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage %
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# Disk usage %
(1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes)) * 100

# Request rate
sum(rate(http_requests_total[5m])) by (status_code)

# Error rate
sum(rate(http_requests_total{status_code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# 95th percentile latency
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

## Grafana Dashboards

Import these dashboard IDs:
- **1860** — Node Exporter Full
- **893** — Docker monitoring
- **9628** — PostgreSQL
- **763** — Redis

## Common Mistakes

- **High cardinality labels** — Don't use user_id or request_id as labels
- **Scraping too frequently** — 15s is fine, 1s is not
- **No retention policy** — Default keeps data forever, disk fills up
- **Missing recording rules** — Pre-calculate expensive queries

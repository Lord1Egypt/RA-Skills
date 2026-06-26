# Monitoring Reference

## Table of Contents

- [Per-Addon Metrics Port and Exporter Details](#per-addon-metrics-port-and-exporter-details)
- [Custom Alerting Rules](#custom-alerting-rules)
- [Grafana Dashboard IDs and Sources](#grafana-dashboard-ids-and-sources)

## Per-Addon Metrics Port and Exporter Details

KubeBlocks addons expose metrics via a sidecar exporter or the database engine's built-in metrics endpoint.

| Addon | Exporter | Metrics Port Name | Default Port | Metrics Path |
|---|---|---|---|---|
| MySQL | mysqld_exporter | `http-metrics` | 9104 | `/metrics` |
| PostgreSQL | postgres_exporter | `http-metrics` | 9187 | `/metrics` |
| Redis | redis_exporter | `http-metrics` | 9121 | `/metrics` |
| MongoDB | mongodb_exporter | `http-metrics` | 9216 | `/metrics` |
| Kafka | kafka_exporter | `http-metrics` | 9308 | `/metrics` |
| Elasticsearch | elasticsearch_exporter | `http-metrics` | 9114 | `/metrics` |
| Milvus | built-in | `metrics` | 9091 | `/metrics` |
| Qdrant | built-in | `http-metrics` | 6333 | `/metrics` |

Per-addon monitoring docs:
- MySQL: https://kubeblocks.io/docs/preview/kubeblocks-for-mysql/08-monitoring/01-integrate-with-prometheus-operator
- PostgreSQL: https://kubeblocks.io/docs/preview/kubeblocks-for-postgresql/08-monitoring/01-integrate-with-prometheus-operator
- Redis: https://kubeblocks.io/docs/preview/kubeblocks-for-redis/08-monitoring/01-integrate-with-prometheus-operator
- Kafka: https://kubeblocks.io/docs/preview/kubeblocks-for-kafka/08-monitoring/01-integrate-with-prometheus-operator
- Elasticsearch: https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/08-monitoring/01-integrate-with-prometheus-operator
- Milvus: https://kubeblocks.io/docs/preview/kubeblocks-for-milvus/08-monitoring/01-integrate-with-prometheus-operator
- Qdrant: https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/08-monitoring/01-integrate-with-prometheus-operator
- RabbitMQ: https://kubeblocks.io/docs/preview/kubeblocks-for-rabbitmq/08-monitoring/01-integrate-with-prometheus-operator

## Custom Alerting Rules

### Example: MySQL High Connection Count

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: mysql-alerts
  namespace: monitoring
  labels:
    release: prometheus
spec:
  groups:
    - name: mysql.rules
      rules:
        - alert: MySQLHighConnections
          expr: mysql_global_status_threads_connected > 100
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "MySQL connections high on {{ $labels.instance }}"
            description: "{{ $labels.instance }} has {{ $value }} active connections."

        - alert: MySQLSlowQueries
          expr: rate(mysql_global_status_slow_queries[5m]) > 0.1
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "MySQL slow queries detected on {{ $labels.instance }}"

        - alert: MySQLReplicationLag
          expr: mysql_slave_status_seconds_behind_master > 30
          for: 2m
          labels:
            severity: critical
          annotations:
            summary: "MySQL replication lag > 30s on {{ $labels.instance }}"
```

### Example: PostgreSQL Alerts

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: postgresql-alerts
  namespace: monitoring
  labels:
    release: prometheus
spec:
  groups:
    - name: postgresql.rules
      rules:
        - alert: PostgreSQLHighConnections
          expr: pg_stat_activity_count > 80
          for: 5m
          labels:
            severity: warning

        - alert: PostgreSQLReplicationLag
          expr: pg_replication_lag > 30
          for: 2m
          labels:
            severity: critical

        - alert: PostgreSQLDeadlocks
          expr: rate(pg_stat_database_deadlocks[5m]) > 0
          for: 5m
          labels:
            severity: warning
```

### Example: Redis Alerts

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: redis-alerts
  namespace: monitoring
  labels:
    release: prometheus
spec:
  groups:
    - name: redis.rules
      rules:
        - alert: RedisHighMemoryUsage
          expr: redis_memory_used_bytes / redis_memory_max_bytes > 0.85
          for: 5m
          labels:
            severity: warning

        - alert: RedisKeyEviction
          expr: rate(redis_evicted_keys_total[5m]) > 0
          for: 5m
          labels:
            severity: warning
```

## Grafana Dashboard IDs and Sources

| Dashboard | Grafana ID | Addon | Notes |
|---|---|---|---|
| MySQL Overview | 7362 | MySQL | mysqld_exporter metrics |
| MySQL Replication | 7371 | MySQL | Primary/replica lag |
| PostgreSQL Database | 9628 | PostgreSQL | postgres_exporter |
| PostgreSQL Query Performance | 12273 | PostgreSQL | pg_stat_statements |
| Redis Dashboard | 763 | Redis | redis_exporter |
| Redis Cluster | 11835 | Redis | For redis-cluster topology |
| MongoDB Overview | 2583 | MongoDB | mongodb_exporter |
| Kafka Overview | 7589 | Kafka | kafka_exporter / JMX |
| Elasticsearch | 2322 | Elasticsearch | elasticsearch_exporter |

To import: Grafana -> Dashboards -> Import -> Enter ID -> Select Prometheus data source -> Import.

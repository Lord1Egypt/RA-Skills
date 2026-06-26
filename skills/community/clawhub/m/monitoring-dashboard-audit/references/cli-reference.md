# CLI Reference — Grafana and Prometheus APIs

API commands organized by monitoring dashboard audit step. All Grafana
endpoints require `Authorization: Bearer <token>` header. Prometheus
endpoints are unauthenticated by default.

## Grafana HTTP API

### Dashboard Operations (Step 1)

```bash
# List all dashboards with metadata
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/search?type=dash-db&limit=5000" | jq '.[] | {uid, title, folderTitle, tags}'

# Get full dashboard JSON model by UID
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/dashboards/uid/<uid>" | jq '.dashboard'

# List dashboard folders
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/folders" | jq '.[] | {uid, title}'

# Get dashboard versions (change history)
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/dashboards/uid/<uid>/versions" | jq '.[0:5]'
```

### Data Source Operations (Step 5)

```bash
# List all data sources
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/datasources" | jq '.[] | {id, name, type, url}'

# Test data source connectivity
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/datasources/<id>/health"

# Get data source details by name
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/datasources/name/<name>"
```

### Alert Rule Operations (Step 3)

```bash
# List Grafana Unified Alerting rules
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/v1/provisioning/alert-rules" | jq '.[] | {uid, title, condition, for}'

# List alert rule groups by folder
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/ruler/grafana/api/v1/rules" | jq 'keys'

# Get notification policies (routing tree)
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/v1/provisioning/policies"

# List contact points (notification channels)
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/v1/provisioning/contact-points"

# List active silences
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/alertmanager/grafana/api/v2/silences" | jq '.[] | select(.status.state=="active")'
```

### Annotation Operations

```bash
# Query annotations for incident correlation
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/annotations?from=<epoch_ms>&to=<epoch_ms>&limit=100"

# Query annotations by dashboard
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/annotations?dashboardUID=<uid>"
```

## Prometheus HTTP API

### Target Status (Step 5)

```bash
# List all active scrape targets with health status
curl -s "$PROM_URL/api/v1/targets?state=active" | \
  jq '.data.activeTargets[] | {job: .labels.job, instance: .labels.instance, health, lastScrape: .lastScrape}'

# Get scrape pool target count
curl -s "$PROM_URL/api/v1/targets" | \
  jq '[.data.activeTargets[] | .scrapePool] | group_by(.) | map({pool: .[0], count: length})'

# Check specific target health
curl -s "$PROM_URL/api/v1/targets?state=active" | \
  jq '.data.activeTargets[] | select(.labels.job=="snmp") | {instance: .labels.instance, health}'
```

### Rules and Alerts (Step 3)

```bash
# List all alerting rules with state
curl -s "$PROM_URL/api/v1/rules?type=alert" | \
  jq '.data.groups[].rules[] | {name: .name, state, query: .query, duration: .duration}'

# List all recording rules
curl -s "$PROM_URL/api/v1/rules?type=record" | \
  jq '.data.groups[].rules[] | {name: .name, query: .query}'

# Get currently firing alerts
curl -s "$PROM_URL/api/v1/alerts" | \
  jq '.data.alerts[] | {name: .labels.alertname, severity: .labels.severity, state}'
```

### Query and Series (Step 2, Step 4)

```bash
# Instant query — evaluate PromQL at current time
curl -s "$PROM_URL/api/v1/query?query=up" | jq '.data.result'

# Range query — evaluate over time window
curl -s "$PROM_URL/api/v1/query_range?query=rate(node_cpu_seconds_total[5m])&start=<rfc3339>&end=<rfc3339>&step=60s"

# Get all metric names matching prefix
curl -s "$PROM_URL/api/v1/label/__name__/values" | jq '[.data[] | select(startswith("snmp_"))]'

# Series count per metric name (cardinality check)
curl -s "$PROM_URL/api/v1/query?query=count({__name__=~\"snmp_.*\"}) by (__name__)" | \
  jq '.data.result | sort_by(.value[1] | tonumber) | reverse | .[0:10]'
```

### TSDB Status (Step 5)

```bash
# Get TSDB cardinality statistics (Prometheus 2.14+)
curl -s "$PROM_URL/api/v1/status/tsdb" | \
  jq '{seriesCountByMetricName: .data.seriesCountByMetricName[0:10], headStats: .data.headStats}'

# Get Prometheus build and configuration info
curl -s "$PROM_URL/api/v1/status/config" | jq '.data.yaml' | head -50
curl -s "$PROM_URL/api/v1/status/flags" | jq '.data'

# Get WAL and storage statistics
curl -s "$PROM_URL/api/v1/query?query=prometheus_tsdb_wal_storage_size_bytes" | jq '.data.result[0].value[1]'
curl -s "$PROM_URL/api/v1/query?query=prometheus_tsdb_storage_blocks_bytes" | jq '.data.result[0].value[1]'
```

## promtool Commands

```bash
# Validate alerting rule file syntax
promtool check rules /etc/prometheus/rules/*.yml

# Validate Prometheus configuration
promtool check config /etc/prometheus/prometheus.yml

# Test alerting rule expressions against live data
promtool test rules test-rules.yml

# Query Prometheus from command line
promtool query instant "$PROM_URL" 'up == 0'
promtool query range "$PROM_URL" 'rate(node_cpu_seconds_total[5m])' --start=1h --end=now --step=60s

# Debug metric series for a specific target
promtool query series "$PROM_URL" --match='snmp_if_hc_in_octets{instance="switch01:9116"}'
```

## Alertmanager API

```bash
# List active alerts in Alertmanager
curl -s "$AM_URL/api/v2/alerts?active=true" | \
  jq '.[] | {name: .labels.alertname, severity: .labels.severity, startsAt}'

# List active silences
curl -s "$AM_URL/api/v2/silences" | \
  jq '.[] | select(.status.state=="active") | {id, createdBy, comment, endsAt}'

# Get receiver configuration summary
curl -s "$AM_URL/api/v2/status" | jq '.config.route'
```

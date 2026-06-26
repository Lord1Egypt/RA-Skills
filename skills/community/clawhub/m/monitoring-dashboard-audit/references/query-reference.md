# Query Reference — PromQL Patterns for Network Monitoring

PromQL expressions for network infrastructure monitoring organized by
use case. All patterns assume SNMP exporter or equivalent metric sources.
Adapt label names to match your exporter configuration.

## Interface Utilization

### Bits-per-second calculation from SNMP counters

```promql
# Inbound interface utilization (bps)
rate(snmp_if_hc_in_octets{job="snmp"}[5m]) * 8

# Outbound interface utilization (bps)
rate(snmp_if_hc_out_octets{job="snmp"}[5m]) * 8

# Interface utilization as percentage of link speed
(rate(snmp_if_hc_in_octets{job="snmp"}[5m]) * 8)
  / on(instance, ifIndex) snmp_if_high_speed{job="snmp"}
  / 1e6 * 100

# Peak utilization over 24h (for capacity planning)
max_over_time(
  (rate(snmp_if_hc_in_octets{job="snmp"}[5m]) * 8)[24h:5m]
) / on(instance, ifIndex) snmp_if_high_speed{job="snmp"} / 1e6 * 100
```

### Recording rules for interface utilization

```yaml
groups:
  - name: network_interface_utilization
    interval: 1m
    rules:
      - record: network:interface_in_bps:rate5m
        expr: rate(snmp_if_hc_in_octets{job="snmp"}[5m]) * 8

      - record: network:interface_out_bps:rate5m
        expr: rate(snmp_if_hc_out_octets{job="snmp"}[5m]) * 8

      - record: network:interface_utilization_pct:rate5m
        expr: |
          (rate(snmp_if_hc_in_octets{job="snmp"}[5m]) * 8)
            / on(instance, ifIndex) snmp_if_high_speed{job="snmp"}
            / 1e6 * 100
```

## Error Rates

### Interface error and discard ratios

```promql
# Input error rate (errors per second)
rate(snmp_if_in_errors{job="snmp"}[5m])

# Output error rate
rate(snmp_if_out_errors{job="snmp"}[5m])

# Error ratio (errors relative to total packets)
rate(snmp_if_in_errors{job="snmp"}[5m])
  / (rate(snmp_if_in_ucast_pkts{job="snmp"}[5m]) + rate(snmp_if_in_errors{job="snmp"}[5m]))

# Discard ratio (discards relative to total packets)
rate(snmp_if_in_discards{job="snmp"}[5m])
  / (rate(snmp_if_in_ucast_pkts{job="snmp"}[5m]) + rate(snmp_if_in_discards{job="snmp"}[5m]))

# Combined error + discard rate per interface
(rate(snmp_if_in_errors{job="snmp"}[5m]) + rate(snmp_if_in_discards{job="snmp"}[5m]))
```

### Alerting rules for interface errors

```yaml
groups:
  - name: network_interface_errors
    rules:
      - alert: InterfaceHighErrorRate
        expr: rate(snmp_if_in_errors{job="snmp"}[5m]) > 100
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Interface {{ $labels.ifDescr }} on {{ $labels.instance }} has high error rate"
          description: "Input error rate is {{ $value | humanize }}/s for the last 5 minutes."

      - alert: InterfaceCriticalErrorRate
        expr: rate(snmp_if_in_errors{job="snmp"}[5m]) > 1000
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Interface {{ $labels.ifDescr }} on {{ $labels.instance }} has critical error rate"
```

## BGP Peer State

### BGP session monitoring

```promql
# BGP peer state (gauge: 1=idle, 2=connect, 3=active, 4=opensent, 5=openconfirm, 6=established)
snmp_bgp_peer_state{job="snmp"}

# Count of established BGP peers per device
count(snmp_bgp_peer_state{job="snmp"} == 6) by (instance)

# Peers NOT in established state (active problems)
snmp_bgp_peer_state{job="snmp"} != 6

# BGP peer uptime (time since last state change)
snmp_bgp_peer_fsm_established_time{job="snmp"}

# Received prefix count per peer
snmp_bgp_peer_accepted_prefixes{job="snmp"}
```

### Alerting rules for BGP state changes

```yaml
groups:
  - name: network_bgp_monitoring
    rules:
      - alert: BGPPeerDown
        expr: snmp_bgp_peer_state{job="snmp"} != 6
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "BGP peer {{ $labels.bgpPeerRemoteAddr }} on {{ $labels.instance }} is not established"
          description: "Current state: {{ $value }}. Expected: 6 (established)."

      - alert: BGPPeerFlapDetected
        expr: changes(snmp_bgp_peer_state{job="snmp"}[15m]) > 2
        for: 0s
        labels:
          severity: warning
        annotations:
          summary: "BGP peer {{ $labels.bgpPeerRemoteAddr }} on {{ $labels.instance }} is flapping"
          description: "{{ $value }} state changes in the last 15 minutes."

      - alert: BGPPrefixCountDrop
        expr: |
          (snmp_bgp_peer_accepted_prefixes{job="snmp"}
            / snmp_bgp_peer_accepted_prefixes{job="snmp"} offset 1h)
          < 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "BGP peer {{ $labels.bgpPeerRemoteAddr }} prefix count dropped >50%"
```

## Device Health Metrics

### CPU and memory from SNMP

```promql
# CPU utilization percentage (HOST-RESOURCES-MIB)
snmp_hr_processor_load{job="snmp"}

# Average CPU across all processors on a device
avg(snmp_hr_processor_load{job="snmp"}) by (instance)

# Memory utilization percentage
(snmp_hr_storage_used{hrStorageDescr="Physical memory"} * snmp_hr_storage_allocation_units{hrStorageDescr="Physical memory"})
  / (snmp_hr_storage_size{hrStorageDescr="Physical memory"} * snmp_hr_storage_allocation_units{hrStorageDescr="Physical memory"})
  * 100

# Device uptime in days
snmp_sys_uptime{job="snmp"} / 100 / 86400
```

### Alerting rules for device health

```yaml
groups:
  - name: network_device_health
    rules:
      - alert: DeviceHighCPU
        expr: avg(snmp_hr_processor_load{job="snmp"}) by (instance) > 80
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Device {{ $labels.instance }} CPU above 80%"

      - alert: DeviceReboot
        expr: snmp_sys_uptime{job="snmp"} < 600
        for: 0s
        labels:
          severity: warning
        annotations:
          summary: "Device {{ $labels.instance }} rebooted (uptime {{ $value | humanize }}s)"
```

## SLI/SLO Patterns

### Availability and error budget calculations

```promql
# Service availability over 30 days (probe-based)
avg_over_time(probe_success{job="blackbox"}[30d])

# Error budget remaining (for 99.9% SLO over 30d)
1 - (
  (1 - avg_over_time(probe_success{job="blackbox"}[30d]))
  / (1 - 0.999)
)

# Burn rate — 1-hour window
1 - avg_over_time(probe_success{job="blackbox"}[1h])
  / (1 - 0.999)

# Burn rate — 6-hour window
1 - avg_over_time(probe_success{job="blackbox"}[6h])
  / (1 - 0.999)
```

### Multi-window burn rate alerting rules

```yaml
groups:
  - name: slo_burn_rate
    rules:
      # 14.4x burn rate over 1h AND 6x over 6h — pages
      - alert: SLOBurnRateCritical
        expr: |
          (
            (1 - avg_over_time(probe_success{job="blackbox"}[1h]))
            / (1 - 0.999)
          ) > 14.4
          and
          (
            (1 - avg_over_time(probe_success{job="blackbox"}[6h]))
            / (1 - 0.999)
          ) > 6
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "SLO burn rate critical for {{ $labels.instance }}"

      # 3x burn rate over 6h AND 1x over 3d — ticket
      - alert: SLOBurnRateWarning
        expr: |
          (
            (1 - avg_over_time(probe_success{job="blackbox"}[6h]))
            / (1 - 0.999)
          ) > 3
          and
          (
            (1 - avg_over_time(probe_success{job="blackbox"}[3d]))
            / (1 - 0.999)
          ) > 1
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "SLO burn rate elevated for {{ $labels.instance }}"
```

## Cardinality Investigation Queries

```promql
# Count series per metric name (expensive — use sparingly)
count({__name__=~"snmp_.*"}) by (__name__)

# Identify high-cardinality label values
count(snmp_if_hc_in_octets{job="snmp"}) by (instance)

# Check for label explosion on a specific metric
count(snmp_if_hc_in_octets{job="snmp"}) by (ifDescr)

# Total active time series in Prometheus
prometheus_tsdb_head_series

# Samples ingested per second (write load)
rate(prometheus_tsdb_head_samples_appended_total[5m])
```

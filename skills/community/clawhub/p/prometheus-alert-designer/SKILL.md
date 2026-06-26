---
name: prometheus-alert-designer
description: Design Prometheus alerting rules and recording rules — analyze PromQL queries, set meaningful thresholds, reduce alert fatigue, and build multi-window multi-burn-rate SLO alerts. Use when asked to create alerts, fix noisy alerting, or set up Prometheus-based monitoring.
metadata:
  tags: ["prometheus", "alerting", "promql", "grafana", "sre", "observability"]
---

# Prometheus Alert Designer

Design Prometheus alerting rules that wake people up only when it matters. Analyze PromQL queries for correctness, set thresholds based on real traffic patterns, create recording rules for performance, and implement multi-window burn-rate SLO alerting — the gold standard for production alerts.

Use when: "create Prometheus alerts", "our alerts are too noisy", "design alerting rules", "write PromQL for monitoring", "set up SLO-based alerting", "review our alerting rules", or when configuring Alertmanager routing.

## Core Philosophy

**The Three Laws of Alerting:**
1. Every alert must be actionable — if nobody needs to do anything, delete it.
2. Every alert must be urgent — if it can wait until Monday, it's not an alert (it's a ticket).
3. Every alert must be real — if it fires and the service is fine, the alert is broken.

## Analysis Steps

### 1. Inventory Existing Alerts

Query Prometheus API to list all rules, currently firing alerts, and alert history. For each alert, evaluate:
- Fires often (>3x/week)? Probably too sensitive.
- Nobody acts when it fires? Delete or downgrade.
- Fires and auto-resolves in <5min? Flapping.
- Threshold based on data or a guess? Most are guesses.
- Has a runbook link? Without one, useless at 3 AM.

### 2. Design Alert Rules by Category

#### Service Availability Alerts

**High Error Rate:**
```yaml
groups:
  - name: service_availability
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m])) by (job, service)
            /
            sum(rate(http_requests_total[5m])) by (job, service)
          ) * 100 > 5
        for: 5m
        labels:
          severity: critical
          team: "{{ $labels.service }}"
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          description: |
            Error rate is {{ printf "%.2f" $value }}% (threshold: 5%).
            Service: {{ $labels.service }}
            Job: {{ $labels.job }}
          runbook_url: "https://wiki.internal/runbooks/high-error-rate"
          dashboard_url: "https://grafana.internal/d/svc-overview?var-service={{ $labels.service }}"
```

**Key design decisions:**
- `for: 5m` prevents alerting on transient spikes (a single retry storm)
- `rate()[5m]` smooths over 5 minutes — shorter windows are noisier
- Group by `service` so each service gets its own alert instance
- Include both `summary` (for pager) and `description` (for context)
- Always include `runbook_url` and `dashboard_url`

**Service Down (no traffic at all):**
```yaml
      - alert: ServiceDown
        expr: |
          up{job="my-service"} == 0
          or
          absent(up{job="my-service"})
        for: 2m
        labels:
          severity: page
        annotations:
          summary: "{{ $labels.job }} is down on {{ $labels.instance }}"
          description: "Target has been unreachable for 2 minutes."
```

**Important:** Use `absent()` to catch the case where the target disappears entirely (Prometheus stops scraping it, so `up` returns no data instead of 0).

#### Latency Alerts

**High Latency (histogram-based):**
```yaml
      - alert: HighLatencyP99
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          ) > 2.0
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "p99 latency above 2s for {{ $labels.service }}"
          description: "p99 latency is {{ printf \"%.2f\" $value }}s"
```

**Latency rules:** Always use `histogram_quantile`, alert on p99 not p50, use `for: 10m`, set threshold from SLO.

#### Saturation Alerts

**Disk Space** — use `predict_linear` instead of static thresholds:
```yaml
      - alert: DiskSpaceRunningOut
        expr: predict_linear(node_filesystem_avail_bytes{fstype!~"tmpfs|overlay"}[6h], 24*3600) < 0
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "Disk will fill within 24h on {{ $labels.instance }}"
```

`predict_linear` catches a disk at 60% growing 5%/hour (problem in 8h) while ignoring a disk at 85% with stable usage.

**CPU/Memory** — same pattern: `1 - avg(rate(node_cpu_seconds_total{mode="idle"}[10m])) by (instance) * 100 > 85` for CPU, `1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100 > 90` for memory. Use `for: 10m` to avoid transient spikes.

### 3. Build Recording Rules

Recording rules pre-compute expensive queries so dashboards load fast and alerts evaluate reliably.

**When to create a recording rule:**
- Query uses `rate()` + aggregation across many series (>1000 time series)
- Same query appears in multiple alerts or dashboards
- Query takes >2 seconds to evaluate
- Query is used for SLO calculations

**Naming convention:** `level:metric:operations`

```yaml
groups:
  - name: service_recording_rules
    interval: 30s
    rules:
      - record: service:http_requests_total:rate5m
        expr: sum(rate(http_requests_total[5m])) by (service)
      - record: service:http_requests_errors:rate5m
        expr: sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
      - record: service:http_requests:error_ratio_5m
        expr: service:http_requests_errors:rate5m / service:http_requests_total:rate5m
      - record: service:http_request_duration_seconds:p99_5m
        expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))
```

### 4. Implement Multi-Window Multi-Burn-Rate SLO Alerts

This is the Google SRE recommended approach. Instead of alerting on a raw error rate, alert when you're burning through your error budget too fast.

**Concept:**
```
SLO: 99.9% availability (error budget = 0.1% of requests can fail)

Burn rate 1x  = consuming budget at exactly the right pace (will exhaust in 30 days)
Burn rate 14x = will exhaust the entire 30-day budget in ~2 days — PAGE NOW
Burn rate 6x  = will exhaust in ~5 days — create a ticket
Burn rate 1x  = everything is fine
```

**Implementation — two alert tiers:**

1. **Page (14x burn):** Create recording rules for 5m and 1h error ratios. Alert when BOTH windows exceed `14 * (1 - SLO)`. For 99.9% SLO: `> 14 * 0.001 = 0.014`. Use `for: 2m`. This catches severe outages — budget exhausted in ~2 days.

2. **Ticket (6x burn):** Same pattern with 30m and 6h windows exceeding `6 * (1 - SLO)`. Use `for: 5m`. Catches slow degradation — budget exhausted in ~5 days.

```yaml
      - alert: SLOErrorBudgetBurnHigh
        expr: |
          (
            service:slo_errors:ratio_rate5m > (14 * 0.001)
            and
            service:slo_errors:ratio_rate1h > (14 * 0.001)
          )
        for: 2m
        labels:
          severity: page
        annotations:
          summary: "SLO burn rate critical for {{ $labels.service }}"
```

Recording rules needed: `service:slo_errors:ratio_rate{5m,30m,1h,6h}` — each is `sum(rate(http_requests_total{status=~"5.."}[window])) / sum(rate(http_requests_total[window])) by (service)`.

### 5. Configure Alertmanager Routing

Route alerts by severity label to appropriate channels:

| Severity | Receiver | group_wait | repeat_interval |
|----------|----------|-----------|----------------|
| `page` | PagerDuty | 10s | 1h |
| `critical` | Slack #incidents | 30s | 2h |
| `warning` | Slack #monitoring | 30s | 8h |
| `ticket` | Jira webhook | 30s | 24h |

**Key settings:** `group_by: ['alertname', 'service']` to batch related alerts. Set `group_interval: 5m` to avoid notification spam.

**Inhibition rules** (critical for reducing noise):
- ServiceDown firing suppresses HighErrorRate for the same service (redundant)
- `page` severity suppresses `warning` severity for the same service

### 6. Alert Fatigue Audit

Review existing alerts for these anti-patterns:

- **Flapping alerts** — fires and resolves within 5 minutes repeatedly. Fix: increase `for` duration or add hysteresis.
- **Always-firing alerts** — has been in FIRING state for days. Fix: raise threshold or reclassify as ticket.
- **Never-firing alerts** — hasn't fired in 6 months. Fix: verify query still returns data, adjust threshold, or remove.
- **Duplicate alerts** — multiple alerts that fire for the same incident. Fix: use inhibition rules.
- **Missing `for` clause** — fires on every transient spike. Fix: add `for: 5m` minimum.
- **Alert without runbook** — useless at 3 AM. Fix: write a runbook or link to the dashboard.
- **Percentage alerts on low traffic** — "5% error rate" when there are 2 requests/min = 1 error fires the alert. Fix: add a minimum traffic floor: `and sum(rate(http_requests_total[5m])) by (service) > 1`

## Output Format

```markdown
# Prometheus Alert Design: {Service/System Name}

## Recording Rules
{YAML recording rules with explanations}

## Alert Rules
{YAML alert rules organized by category}

## Alertmanager Routing
{Routing configuration with severity-based escalation}

## SLO Burn Rate Alerts
{Multi-window burn rate rules if applicable}

## Audit Findings (if reviewing existing rules)
- {Anti-pattern found and recommended fix}

## Testing Plan
- {How to verify each alert fires correctly}
- {Recommended Prometheus unit test cases}
```

## Tips

- Test alerts with `promtool test rules` before deploying — this catches PromQL syntax errors and logic bugs
- Use `for: 5m` as the minimum for any alert — anything shorter is almost certainly flapping
- Always add a traffic floor to percentage-based alerts: `and rate(total[5m]) > 1`
- Set `group_by: ['alertname', 'service']` in Alertmanager to batch related alerts
- Use `inhibit_rules` to suppress redundant alerts (e.g., don't alert on high latency if the service is down)
- Name alerts with the pattern `{What}{Condition}` — `HighErrorRate`, `DiskSpaceLow`, `ServiceDown`
- Every alert annotation should include: what's wrong, how bad it is (current value), and where to look (dashboard URL)
- Review alert firing history monthly — if nobody acted on it, delete it

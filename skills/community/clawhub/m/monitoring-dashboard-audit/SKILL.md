---
name: monitoring-dashboard-audit
description: >-
  Monitoring infrastructure assessment covering Grafana dashboard analysis,
  PromQL query validation, alert rule evaluation, SLA/SLO reporting review,
  and Prometheus data source health checks for network operations environments.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"📊","safetyTier":"read-only","requires":{"bins":[],"env":[]},"tags":["grafana","prometheus","monitoring"],"mcpDependencies":[],"egressEndpoints":[]}'
---

# Monitoring Dashboard Audit

Structured assessment of monitoring infrastructure for network operations.
Evaluates Grafana dashboards, PromQL query efficiency, alert rule
configuration, SLA/SLO reporting accuracy, and Prometheus data source
health. This skill reads monitoring configuration and metrics — it does
not create, modify, or delete dashboards, alerts, or data sources.

Reference `references/cli-reference.md` for Grafana and Prometheus API
commands organized by audit step, and `references/query-reference.md` for
PromQL patterns covering network interface utilization, error rates, BGP
peer state, and SNMP-derived metric evaluation.

## When to Use

- Monitoring gap assessment — verifying that all critical network infrastructure has dashboard coverage and active alerting
- Dashboard quality review — evaluating whether existing Grafana dashboards present accurate, actionable data to operations teams
- Alert fatigue investigation — audit when teams report excessive or irrelevant alert notifications that mask genuine incidents
- SLA/SLO compliance review — validating that error budget calculations and availability metrics reflect actual service delivery
- Pre-migration monitoring readiness — confirming monitoring will survive infrastructure changes (new devices, topology changes, platform migrations)
- Post-incident review — assessing whether monitoring detected the incident, how quickly alerts fired, and what gaps allowed silent failures

## Prerequisites

- **Grafana access** — API token or service account with Viewer role minimum (`grafana_url` and `Authorization: Bearer <token>` header confirmed working)
- **Prometheus access** — HTTP API reachable at `prometheus_url/api/v1/status/config` (no authentication required by default, or appropriate auth header configured)
- **Network scope defined** — device inventory, subnet ranges, and critical service list available for coverage gap analysis
- **Baseline documentation** — existing SLA/SLO targets, expected alert thresholds, and operations runbooks available for comparison
- **Timestamp awareness** — confirm NTP synchronization across monitoring stack; Prometheus scrape timestamps and Grafana time range selections depend on consistent clocks

## Procedure

Follow these six steps sequentially. Each step produces findings that
feed the monitoring coverage scorecard and optimization recommendations
in Step 6.

### Step 1: Dashboard Inventory

Enumerate all Grafana dashboards to establish the monitoring surface
area and identify coverage gaps, stale dashboards, and organizational
issues.

Query the Grafana API to list all dashboards with metadata:

```
GET /api/search?type=dash-db&limit=5000
```

For each dashboard, record: uid, title, folder, tags, and last-updated
timestamp. Identify dashboards not updated in over 180 days as staleness
candidates — these may reference deprecated metrics or decommissioned
infrastructure.

Examine folder organization. Flat folder structures with 50+ dashboards
at root level indicate organizational debt. Check for naming convention
adherence — dashboards without consistent prefixes or tags reduce
discoverability during incidents.

Retrieve the full JSON model for each dashboard:

```
GET /api/dashboards/uid/<uid>
```

Record panel count, data source references, and template variables.
Flag dashboards with hardcoded time ranges (no relative time selector)
and panels referencing nonexistent data sources — these produce empty
panels that erode operator trust.

Build a coverage matrix: map dashboard panels to infrastructure
inventory. Devices, interfaces, or services present in inventory but
absent from any dashboard represent monitoring blind spots.

### Step 2: Panel and Query Analysis

Evaluate PromQL query efficiency, panel threshold configuration,
and visualization appropriateness across all dashboards.

Extract all PromQL expressions from dashboard panel JSON targets.
For each query, assess:

**Rate function usage** — `rate()` requires a range vector at least
two scrape intervals wide. Replace `irate()` in dashboard panels that
display trends over long time ranges — `irate()` only uses the last
two data points and is appropriate only for volatile, short-window displays.

**Recording rule candidates** — Complex queries repeating across
multiple dashboards (same expression in 3+ panels) should be recording
rules. Identify these by hashing normalized PromQL expressions.
Common candidates: interface utilization calculations, error rate
ratios, and aggregated availability metrics.

**Label cardinality** — Queries aggregating across high-cardinality
labels without explicit filtering generate expensive computation.
Flag queries with no label matchers on high-cardinality metrics and
queries using `{__name__=~".*"}` patterns.

**Panel thresholds** — Verify gauge and stat panels have threshold
values configured. Panels displaying utilization or error rates
without color-coded thresholds fail to provide at-a-glance severity.
Compare configured thresholds against operational standards (e.g.,
interface utilization warning at 70%, critical at 90%).

**Visualization appropriateness** — Time series data on gauge panels
loses temporal context. Single-value stats for volatile metrics mislead
operators. Table panels with 100+ rows without sorting are unusable
during incidents.

### Step 3: Alert Rule Validation

Assess alert rule configuration for detection coverage, threshold
accuracy, and notification reliability.

Retrieve all alert rules from the Grafana alerting API:

```
GET /api/v1/provisioning/alert-rules
```

For Prometheus-native alerting, also query:

```
GET /api/v1/rules?type=alert
```

For each alert rule, evaluate:

**Threshold appropriateness** — Alert thresholds should align with
operational impact, not arbitrary percentages. Interface utilization
alerts at 50% on a 10Gbps link are premature; at 95% on a 100Mbps
WAN link they are late. Cross-reference thresholds against link
capacity and historical peak usage from Prometheus.

**Evaluation intervals** — Alert rules evaluated every 5 minutes
cannot detect sub-minute outages. For critical infrastructure (WAN
links, core routers), evaluation intervals should match or be less
than the Prometheus scrape interval. Flag alert groups where evaluation
interval exceeds the scrape interval of the underlying metrics.

**Pending and for durations** — `for: 0s` alerts fire on transient
spikes and contribute to alert fatigue. `for: 30m` on critical
infrastructure means 30 minutes of unnotified outage. Recommended
ranges: Critical alerts `for: 2m-5m`, Warning alerts `for: 5m-15m`.

**Notification channels** — Verify all alert rules have at least one
active notification channel. Check channel health — Slack webhooks
return 200, PagerDuty keys are valid, email SMTP is reachable.

**Routing and silencing** — Review Alertmanager routing tree for
catch-all routes dumping all alerts to a single channel. Verify
silences have expiration times. Active silences without expiration
mask ongoing problems indefinitely.

**Escalation completeness** — Critical alerts should escalate from
Slack/email to PagerDuty/phone after acknowledgment timeout. Alert
rules with only Slack notification for Critical-severity failures
lack escalation depth.

### Step 4: SLA/SLO Reporting

Validate that SLA/SLO dashboards and calculations reflect actual
service delivery accuracy.

**Error budget calculation** — Verify the formula:
`error_budget_remaining = 1 - (actual_errors / allowed_errors)`.
Common mistakes: using the wrong time window (calendar month vs
rolling 30 days), excluding planned maintenance from downtime
calculations, or computing availability from a single data source
when the service spans multiple components.

**Availability SLIs** — Check that uptime percentage, MTTR (Mean
Time to Repair), and MTBF (Mean Time Between Failures) use correct
inputs. Uptime should reference probe-based measurement (blackbox
exporter, synthetic checks), not just device-reported status. MTTR
excluding detection time understates actual recovery duration.

**Burn rate alerting** — Multi-window burn rate alerting provides
early warning when error budget consumption accelerates. Verify burn
rate alerts use at least two windows (e.g., 1-hour and 6-hour). A
single-window alert either fires too late or too often. Check that
severity maps to budget consumption: a 14.4x burn rate over 1 hour
warrants page-level severity.

**Multi-window alert patterns** — Confirm long-window alerts (6h, 3d)
for trend detection and short-window alerts (5m, 1h) for rapid
response. Verify severity increases with burn rate magnitude.

### Step 5: Data Source Health

Assess Prometheus scrape target status, metric cardinality, retention
configuration, and remote write health.

**Scrape target status** — Query the targets API:

```
GET /api/v1/targets?state=active
```

Check the `up` metric across all scrape targets. Targets with
`up == 0` are failing to scrape — investigate network reachability,
exporter health, or authentication issues. Targets with
`scrape_duration_seconds` exceeding the scrape interval are timing
out, producing gaps in metrics and potentially triggering false alerts.

**Cardinality assessment** — Query TSDB status:

```
GET /api/v1/status/tsdb
```

Identify the top 10 metrics by series count. Network environments
commonly see cardinality explosion from per-interface SNMP metrics
on large chassis devices. Metrics exceeding 10,000 active series per
name warrant investigation for label optimization or aggregation.

**Retention and storage** — Verify retention period covers the longest
SLA reporting window. A 15-day retention with 30-day SLA dashboards
produces incomplete reports. Check WAL size — a WAL larger than 20%
of total TSDB size may indicate write amplification from high churn.

**Remote write health** — If Prometheus uses remote write (Thanos,
Cortex, Mimir, VictoriaMetrics), check remote storage lag metrics.
Lag exceeding 5 minutes means long-term store is behind real-time.
Flag failed sample counters as write failures creating data gaps.

**Metric naming conventions** — Verify metrics follow Prometheus
naming conventions: snake_case, unit suffixes (_bytes, _seconds,
_total), base units. Inconsistent naming makes dashboard authoring
error-prone and cross-device comparison unreliable.

### Step 6: Monitoring Coverage Report

Compile findings into a structured monitoring coverage scorecard
with prioritized optimization recommendations.

**Coverage scorecard** — Rate each infrastructure category
(core routers, distribution switches, WAN links, firewalls,
load balancers) on a 1–5 scale: 1 = no monitoring, 2 = basic
up/down only, 3 = utilization dashboards, 4 = dashboards with
alerting, 5 = dashboards with alerting and SLO tracking.

**Alert quality assessment** — Compute alert quality metrics:
alert-to-incident ratio, mean time to acknowledge, silence
frequency per alert rule. High-noise alerts (>80% silenced or
acknowledged-without-action) are candidates for threshold
adjustment or removal.

**PromQL optimization recommendations** — For each inefficient
query from Step 2, provide current and optimized expressions.
Prioritize recording rule creation for queries appearing in 3+
panels.

## Threshold Tables

| Domain | Severity | Condition | Example |
|--------|----------|-----------|---------|
| Coverage | Critical | Production device with zero dashboard panels | Core router absent from all dashboards |
| Coverage | High | Service with dashboards but no alerting | WAN link monitored but no capacity alert |
| Coverage | Medium | Dashboard exists but is stale (>180 days) | Last-modified date precedes device refresh |
| Coverage | Low | Dashboard lacks threshold coloring | Utilization panel with no warning/critical bands |
| Query | Critical | PromQL uses absent metric name | Panel returns no data due to renamed metric |
| Query | High | rate() range vector shorter than 2x scrape interval | `rate(metric[15s])` with 30s scrape |
| Query | Medium | Repeated query across 3+ panels without recording rule | Same utilization formula in 5 dashboards |
| Query | Low | irate() used for trend display over long time range | irate() on 24h overview panel |
| Alert | Critical | Alert rule with no notification channel | Silent alarm on Critical infrastructure |
| Alert | High | Critical alert with for duration >15m | 15+ minute detection gap |
| Alert | Medium | Warning alert with for duration of 0s | Transient spikes cause alert fatigue |
| Alert | Low | Single notification channel with no escalation | Slack-only for P1 infrastructure alert |
| SLA | Critical | Error budget calculation uses wrong time window | Calendar month vs rolling 30d mismatch |
| SLA | High | Availability SLI excludes detection time from MTTR | MTTR underreported by omitting MTTD |
| SLA | Medium | Single-window burn rate alerting | Only 1h window, no long-term trend window |
| SLA | Low | SLO dashboard missing historical trend comparison | No month-over-month burn rate trend |
| DataSource | Critical | Scrape target down (up == 0) for >5m | SNMP exporter unreachable |
| DataSource | High | Cardinality >10k series per metric name | Per-interface metrics on 500-port chassis |
| DataSource | Medium | Remote write lag >5m | Long-term store behind real-time |
| DataSource | Low | Metric naming violates Prometheus conventions | CamelCase or missing unit suffix |

## Decision Trees

```
Monitoring Audit Entry Point:
├─ Dashboard completeness unknown? → Start at Step 1 (Inventory)
├─ Alert fatigue reported? → Start at Step 3 (Alert Validation)
├─ SLA disputes or inaccurate reports? → Start at Step 4 (SLA/SLO)
├─ Missing metrics or gaps in graphs? → Start at Step 5 (Data Source)
└─ General health check? → Full procedure Steps 1–6

Panel Query Optimization:
├─ Query returns no data?
│  ├─ Metric name exists in TSDB? → Check label matchers
│  └─ Metric absent? → Critical: exporter or scrape config broken
├─ Query is slow (>10s execution)?
│  ├─ High cardinality labels? → Add label matchers or aggregate
│  ├─ Wide time range on raw metric? → Use recording rule
│  └─ Regex label matcher? → Replace with exact match where possible
└─ Query returns unexpected values?
   ├─ rate() on non-counter metric? → Use gauge-appropriate function
   └─ Aggregation missing labels? → Add by/without clause

Alert Threshold Calibration:
├─ Alert never fires? → Threshold too high or metric absent
│  ├─ Metric present and collecting? → Lower threshold based on P95
│  └─ Metric absent? → Fix scrape target first (Step 5)
├─ Alert fires constantly? → Threshold too low or for duration too short
│  ├─ for: 0s? → Add minimum pending duration
│  └─ Threshold below normal baseline? → Raise to P95 + margin
└─ Alert fires but team ignores it? → Alert fatigue
   ├─ >80% silenced? → Remove or retarget alert
   └─ Low signal-to-noise? → Increase for duration or add inhibition rule
```

## Report Template

```markdown
# Monitoring Dashboard Audit Report

## Executive Summary
- **Scope:** [Grafana instance URL, Prometheus endpoints, device count]
- **Assessment date:** [date]
- **Dashboard count:** [total dashboards / active / stale]
- **Alert rule count:** [total rules / firing / pending / inactive]
- **Coverage score:** [average across infrastructure categories, 1–5 scale]

## Coverage Scorecard
| Category | Dashboards | Alerts | SLOs | Score |
|----------|------------|--------|------|-------|
| Core Routers | [count] | [count] | [Y/N] | [1-5] |
| Distribution | [count] | [count] | [Y/N] | [1-5] |
| WAN Links | [count] | [count] | [Y/N] | [1-5] |
| Firewalls | [count] | [count] | [Y/N] | [1-5] |

## Alert Quality Metrics
| Metric | Value | Target |
|--------|-------|--------|
| Alert-to-incident ratio | [ratio] | <5:1 |
| Mean acknowledgment time | [duration] | <15m |
| Silence frequency (30d) | [count] | decreasing trend |
| Escalation coverage | [%] | 100% for Critical |

## Findings by Severity

### Critical
| # | Domain | Finding | Impact | Recommendation |
|---|--------|---------|--------|----------------|

### High
| # | Domain | Finding | Impact | Recommendation |
|---|--------|---------|--------|----------------|

### Medium / Low
[Grouped findings table]

## PromQL Optimization Recommendations
| Dashboard | Panel | Current Query | Recommended | Cost Reduction |
|-----------|-------|---------------|-------------|----------------|

## SLA/SLO Accuracy Review
| Service | Reported Availability | Validated Availability | Discrepancy |
|---------|----------------------|-----------------------|-------------|

## Appendix
- Full dashboard inventory with staleness dates
- Scrape target health summary
- Cardinality top-10 metrics
```

## Troubleshooting

**Grafana API returns 401/403** — Verify the API token has Viewer
permissions. Service accounts require Viewer role on all folders
containing in-scope dashboards. Admin-level tokens are not required
for read-only audit.

**Prometheus API unreachable** — Check network connectivity and reverse
proxy configuration. Verify the base URL includes the correct path
prefix if Prometheus runs behind a subpath.

**Empty dashboard inventory** — Grafana API search returns paginated
results. Increase the `limit` parameter or paginate. Folder-level
permissions can hide dashboards from restricted tokens.

**PromQL queries reference absent metrics** — SNMP exporter metric
names change between exporter versions. Check exporter version and
generator configuration when dashboards return no data.

**Cardinality data not available** — The TSDB status endpoint requires
Prometheus 2.14+. If unavailable, estimate cardinality using count
queries, though these are expensive on large installations.

**SLA calculations differ from business reports** — Time zone handling
is the most common cause. Prometheus stores UTC timestamps. Verify
all SLA dashboards use explicit UTC time ranges or a consistent
time zone variable.

**Alert rules exist in both Grafana and Prometheus** — Grafana Unified
Alerting coexists with Prometheus-native alerting. Audit both sources
to avoid duplicate or conflicting coverage. Document which system is
authoritative for each alert category.

# Workflow

## 1. Scope

Use `huawei_analyze_cce_capacity_trend` as the main action. The action accepts a window from 1 hour to 1 month and can be run manually or by a recurring job.

Required inputs:

- `region`
- `cluster_id`

Useful optional inputs:

- `hours`: analysis window, clamped to 1-744 hours.
- `output_dir`: writes summary JSON, Markdown report, SVG charts, and history records.
- `history_dir`: override the default history folder.
- `business_namespaces`: comma-separated namespace allowlist.
- `exclude_namespaces`: defaults to `kube-system`.
- `target_cpu_percent`, `target_memory_percent`, `headroom_percent`, `bottleneck_percent`: simulation parameters.
- `action_note`: record an optimization action or operational event so the next cycle can compare before and after effects.

## 2. Collection

The main action collects:

- CCE cluster metadata.
- Kubernetes node inventory.
- CCE nodepool autoscaling status.
- business Deployment inventory.
- HPA inventory and target references.
- node CPU, memory, and disk time series.

If AOM metrics are unavailable, report the gap and do not invent trend conclusions.

## 3. Trend Analysis

For CPU, memory, and disk, calculate:

- average, min, max, p95, latest value.
- slope per hour.
- first-quarter vs last-quarter delta.
- trend direction: rising, falling, flat, or unknown.
- bottleneck prediction against the configured threshold.

Treat a rising trend plus high p95 as a capacity risk. Treat low avg and low p95 plus a conservative simulation as a cost optimization signal.

## 4. Elasticity Awareness

Always consider both layers:

- Workload elasticity: HPA coverage, min/max replicas, target utilization, current/desired replicas.
- Node elasticity: nodepool autoscaling enabled status, min/max nodes, scale-down cooldown, and capped simulation samples.

If HPA coverage is low, generate a preview for one candidate Deployment, but do not apply it without explicit approval.

## 5. Recurring Comparison

For recurring runs, keep all outputs under a stable folder, for example:

```powershell
scripts\huawei-cloud.py huawei_analyze_cce_capacity_trend region=cn-north-4 cluster_id=<id> hours=6 output_dir=debug\capacity-trend\<cluster>
```

Each run writes:

- `capacity-trend-summary.json`
- `capacity-trend-report.md`
- `capacity-trend-report.html` (with embedded curve charts)
- `capacity-trend-chart.svg`
- `capacity-simulation-chart.svg`
- `history/capacity-trend-*.json` and `capacity-trend-history.jsonl`

On later runs, compare the latest record with previous records:

- avg/p95/max utilization changes.
- simulated node requirement changes.
- whether previous recommendations still apply.
- whether `action_note` effects are visible.

## 6. Output Order

1. Executive conclusion.
2. Trend statistics and bottleneck forecast.
3. Current elasticity coverage.
4. Simulation result and chart paths.
5. Recommendations and configuration methods.
6. History comparison.
7. Data gaps and validation checklist.

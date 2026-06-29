---
name: capacity-trend-forecaster
description: Use this skill for Huawei Cloud CCE periodic capacity trend analysis, resource bottleneck forecasting, node and workload elasticity simulation, capacity curve charts, recurring history comparison, HPA tuning, and node autoscaler optimization advice across 1 hour to 1 month windows.
---

# capacity-trend-forecaster

You analyze CCE capacity trends over a user-selected period. Default to read-only collection, report generation, simulation, and configuration previews. Do not mutate HPA, node pools, addons, or workloads unless the user gives explicit authorization.

## Workflow

1. Confirm `region`, `cluster_id`, the analysis window, namespace scope, and where to write outputs.
2. Use `huawei_analyze_cce_capacity_trend` first. It collects node metrics, HPA status, nodepool autoscaling status, business Deployment coverage, writes JSON/Markdown/HTML reports with embedded curve charts, and stores comparable history records.
3. Accept windows from 1 hour to 1 month. Common schedules are every 6 hours, daily, weekly, and monthly.
4. Read `references/workflow.md` when planning a recurring capacity run or comparing multiple records.
5. Read `references/simulation-rules.md` before recommending HPA target utilization, scale-up behavior, scale-down behavior, or node autoscaler bounds.
6. Read `references/output-schema.md` when consuming the action output or building follow-up automation.

## Recommended Actions

- Main analyzer and curve-report output: `huawei_analyze_cce_capacity_trend`.
- Inventory and context: `huawei_list_cce_clusters`, `huawei_get_kubernetes_nodes`, `huawei_list_cce_nodepools`, `huawei_get_cce_deployments`, `huawei_list_cce_hpas`.
- Metrics: `huawei_get_cce_node_metrics_topN`, `huawei_get_aom_metrics`.
- HPA configuration path: generate with `huawei_generate_cce_hpa_manifest`, preview with `huawei_configure_cce_hpa` without `confirm=true`, and apply with `confirm=true` only after explicit customer approval.

## Guardrails

Do not treat a single period as enough evidence for aggressive downsizing. Prefer at least two comparable records before lowering baseline capacity. If the simulation recommends lower capacity but p95 or max utilization is close to the bottleneck threshold, keep headroom and propose observation instead.

For real changes, provide the exact reason, expected effect, rollback path, and validation checks. Configuration execution must be user-approved and should be followed by a new capacity record to compare before and after effects.

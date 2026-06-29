# Workflow

## 1. Collection Scope

Prefer `huawei_analyze_cce_cost_optimization` as the combined action. Only use individual tools below when supplementing details, reviewing specific metrics, or manually generating a specific HPA YAML.

1. Confirm region, cluster_id, namespace range, business exclusion rules, and statistical window.
2. By default, exclude Pods and workloads under `kube-system`; treat other namespaces as business workloads unless the user specifies additional exclusions.
3. Pull node, node pool, Pod, Deployment, and metrics data.
4. For all utilization-based judgments, check both the 24-hour and 7-day windows simultaneously.

## 2. Idle Resources and Low-Utilization Nodes

Calculate for each window separately:

- cluster_cpu_avg = average CPU utilization across all Ready nodes.
- cluster_mem_avg = average memory utilization across all Ready nodes.
- node_cpu_avg / node_mem_avg = single node average utilization.

Trigger conditions:

- Cluster average CPU or memory utilization below 30% → signal overall resource over-provisioning.
- Single node CPU or memory utilization clearly below cluster average. Default criteria: 20 percentage points below cluster average, or below 60% of cluster average.
- If low utilization appears only in the 24-hour window but not in the 7-day window, mark as short-term fluctuation. If both windows match, mark as a stable optimization opportunity.

Output suggestions:

- Prefer recommending node pool min/max adjustment, enabling scale-down, optimizing scheduling and load balancing.
- Do not directly recommend immediate node deletion unless there is clear redundancy and the user requests an execution plan.

## 3. Oversized Requests

Only analyze non-`kube-system` workloads.

For each business workload, compare:

- CPU request vs 24-hour and 7-day actual CPU p95/avg.
- Memory request vs 24-hour and 7-day actual memory p95/avg.

Trigger conditions:

- Request exceeds actual p95 by 2x (200% overhead), and both windows confirm → mark as stable oversized.
- Request exceeds actual p95 by 3x (300% overhead) → mark as high-priority optimization.
- Only the 24-hour window matches → mark as observation item, do not recommend immediate request change.

If the tool response lacks request fields, ask the user to provide Deployment/Pod YAML or use supplementary tools to retrieve them. Do not suggest request modification values based solely on current Pod usage.

## 4. Elasticity Policy Optimization

Check node pool autoscaling:

- Use `huawei_list_cce_nodepools` to check whether autoscaling is enabled, min/max, cooldown, and priority.
- If not configured, provide recommended node pool autoscaler policy including min/max, scale-down delay, resource thresholds, and applicable node pools.
- If configured, check whether min/max is too tight, scale-down is too slow, or priority does not match business tier.

Check HPA:

- Use `huawei_list_cce_hpas` to query existing HPA in business namespaces. Default: do not analyze `kube-system`.
- If no HPA exists, use `huawei_generate_cce_hpa_manifest` to generate an `autoscaling/v2` HPA YAML recommendation based on workload metrics.
- To actually create or update HPA, first call `huawei_configure_cce_hpa` without `confirm=true` to get a preview. Only after explicit user confirmation, call with `confirm=true` to apply.
- HPA recommendations must be based on request sizing. If requests are clearly oversized, first recommend calibrating requests before configuring HPA.

## 5. Output Order

1. Overall conclusion: whether clear cost optimization opportunities exist.
2. 24-hour and 7-day utilization summary.
3. Low-utilization nodes and cluster idle risk.
4. Oversized request workloads.
5. HPA/autoscaler current status and recommended configuration.
6. Risks, verification methods, and pre-execution confirmation checklist.
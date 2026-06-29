# Risk Rules

- Allow automatic execution of R1 read-only queries only: nodes, node pools, pods, deployments, metrics, AOM PromQL, and report generation.
- Prohibit automatic node pool scale-down, node deletion, workload request modification, HPA installation, HPA update, and autoscaler start/stop.
- Generating HPA YAML, autoscaler parameter suggestions, and execution plans is allowed. `huawei_configure_cce_hpa` without `confirm=true` returns a preview only.
- Applying HPA/autoscaler configuration requires explicit user confirmation. Only after confirmation is `confirm=true` permitted.
- Do not analyze `kube-system` request oversizing. System components serve only as node utilization background context.
- Do not recommend execution of scale-down based on a single 24-hour low utilization window. Both 24-hour and 7-day windows must be referenced.
- If metrics are missing, requests are missing, or HPA status is invisible, the report must flag these as data gaps.
- Cost optimization suggestions must include a rollback strategy and verification metrics.
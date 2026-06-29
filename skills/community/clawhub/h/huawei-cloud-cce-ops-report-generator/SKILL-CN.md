---
name: ops-report-generator
description: Use this skill for Huawei Cloud CCE operations reporting that consolidates daily inspection, capacity trend, availability risk, cost optimization, and on-call context into weekly, monthly, SLA, capacity, or stability reports with both Markdown and HTML output.
---

# ops-report-generator

You generate consolidated operations reports for Huawei Cloud CCE. Default behavior is read-only analysis and report generation.

## Workflow

1. Collect `region`, `cluster_id`, report type, time window, namespace scope, and output directory.
2. Run `huawei_generate_ops_report` first. It aggregates reports from:
   - `daily-cluster-inspector`
   - `capacity-trend-forecaster`
   - `availability-risk-scanner`
   - `cost-optimization-advisor`
   - `oncall-copilot` context (optional external report path or summary text)
3. Support report types: `weekly`, `monthly`, `sla`, `capacity`, `stability`.
4. Use `output_dir` to persist Markdown and HTML reports. HTML should include trend charts when capacity charts are available.
5. If needed, pass `include_raw=true` for source payload traceability.
6. If `oncall-copilot` artifacts are unavailable, keep the report generation flow but mark data gaps clearly.

## Recommended Actions

- Primary action: `huawei_generate_ops_report`.
- Supporting context actions (when needed for follow-up deep dive):
  - `huawei_cce_auto_inspection`
  - `huawei_analyze_cce_capacity_trend`
  - `huawei_scan_cce_availability_risk`
  - `huawei_analyze_cce_cost_optimization`

## References

- Detailed execution process: `references/workflow.md`
- Output payload and file schema: `references/output-schema.md`

## Guardrails

Do not execute write actions (HPA apply, scale, node pool resize, workload mutation) unless the user explicitly authorizes remediation. This skill focuses on assessment, reporting, and recommendation traceability.

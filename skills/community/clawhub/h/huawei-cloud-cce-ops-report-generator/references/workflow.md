# Workflow

## Inputs

- Required: `region`, `cluster_id`
- Optional:
  - `report_type`: `weekly` | `monthly` | `sla` | `capacity` | `stability`
  - `hours`, `short_hours`, `long_hours`
  - `exclude_namespaces`, `business_namespaces`, `gateway_keywords`
  - `output_dir`
  - `include_raw`
  - `oncall_report_path` or `oncall_summary`

## Recommended Run Pattern

1. Validate scope and reporting cycle.
2. Execute `huawei_generate_ops_report`.
3. Review generated Markdown report first.
4. Review HTML report for trend and simulation chart interpretation.
5. For high-risk findings, trace back to source sections:
   - daily anomalies -> daily cluster inspection
   - risk level and issue categories -> availability scan
   - oversized requests / low utilization -> cost advisor
   - trend slope / bottleneck projection -> capacity forecaster
6. If customer asks for remediation, switch to explicit change workflow and require authorization before any write action.

## Data Gap Handling

- If a source report fails, keep aggregate report output and mark source as degraded.
- If `oncall-copilot` input is missing, mark as a context gap instead of failing the report.
- Keep report auditable by preserving source file pointers and optional raw payloads (`include_raw=true`).

# Pressure-Test Output Schema

## Run JSON

`huawei_run_cce_pressure_test` writes a JSON record when `output_dir` is provided.

| Field | Meaning |
| --- | --- |
| `job` | Job creation, completion, failure, and timeout state. |
| `samples` | Workload replica and Pod count samples collected while k6 runs. |
| `metric_series` | Standardized replica curves from the run. |
| `k6_summary` | Requests, RPS, success rate, latency percentiles, bytes, and max VUs parsed from k6 logs. |
| `data_gaps` | Missing evidence that should be called out in the report. |

## Observability JSON

`huawei_collect_cce_pressure_test_observability` writes an optional JSON record.

| Field | Meaning |
| --- | --- |
| `inventory` | Pods, Services, and Ingresses in the workload namespace. |
| `pod_metrics` | Node-backed Pod CPU and memory metrics. |
| `elb_metrics` | ELB QPS, connection, latency, and response metrics when `elb_id` is provided. |
| `elb_backend_status` | Backend member and health-monitor evidence. |
| `metric_series` | Standardized curves consumed by the report action. |

## Report Artifacts

The report action emits:

| Artifact | Purpose |
| --- | --- |
| `*-report.md` | Portable Markdown report. |
| `*-report.html` | Styled HTML report with risk-colored recommendations and data-gap tables. |
| `*-curves.svg` | Embedded curve chart for traffic, latency, resources, and replicas. |

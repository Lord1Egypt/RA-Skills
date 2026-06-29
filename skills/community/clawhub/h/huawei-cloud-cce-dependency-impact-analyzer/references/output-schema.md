# Output Schema

```json
{
  "success": true,
  "analysis_trace_id": "DIA-...",
  "scope": {
    "region": "cn-north-4",
    "cluster_id": "cluster-id",
    "namespace": "default",
    "target_name": "api",
    "match_reason": "target_name=api"
  },
  "summary": {
    "risk_level": "High | Medium | Low | Unknown",
    "risk_score": 88,
    "risk_reason": "target pods unavailable and exposed by Service/Ingress",
    "pod_health": {
      "total": 2,
      "ready": 0,
      "unready": 2,
      "availability": "unavailable"
    },
    "service_count": 1,
    "ingress_count": 1,
    "path_count": 2
  },
  "target": {
    "pods": [],
    "services": [],
    "ingresses": []
  },
  "propagation_paths": [],
  "report_markdown": "# CCE Dependency Impact Analysis Report...",
  "report_file": "optional"
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the analysis completed successfully |
| analysis_trace_id | string | Unique trace ID for this analysis run (format: DIA-...) |
| scope.region | string | Huawei Cloud region |
| scope.cluster_id | string | CCE cluster ID |
| scope.namespace | string | Kubernetes namespace scope |
| scope.target_name | string | Target workload/app/service name |
| scope.match_reason | string | How the target was matched (label selector, name prefix, etc.) |
| summary.risk_level | string | Impact risk level: High, Medium, Low, or Unknown |
| summary.risk_score | integer | Numeric risk score (0–100) |
| summary.risk_reason | string | Human-readable reason for the risk level |
| summary.pod_health.total | integer | Total number of target Pods |
| summary.pod_health.ready | integer | Number of ready target Pods |
| summary.pod_health.unready | integer | Number of unready target Pods |
| summary.pod_health.availability | string | Pod availability status: available or unavailable |
| summary.service_count | integer | Number of Services exposing the target Pods |
| summary.ingress_count | integer | Number of Ingresses routing to those Services |
| summary.path_count | integer | Total propagation paths identified |
| target.pods | array | List of target Pod details |
| target.services | array | List of Services whose selectors match target Pods |
| target.ingresses | array | List of Ingresses whose backends point to those Services |
| propagation_paths | array | List of identified propagation paths (Ingress→Service→Pod, Service→Pod) |
| report_markdown | string | Complete Markdown impact analysis report |
| report_file | string | Optional path to saved report file |
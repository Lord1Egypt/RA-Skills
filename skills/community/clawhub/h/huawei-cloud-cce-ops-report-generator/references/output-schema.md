# Output Schema

```json
{
  "success": true,
  "action": "generate_ops_report",
  "generated_at": "2026-05-30T00:00:00+00:00",
  "scope": {
    "region": "cn-north-4",
    "cluster_id": "cluster-id",
    "excluded_namespaces": ["kube-system"],
    "business_namespaces": ["default"],
    "gateway_keywords": ["nginx", "gateway"]
  },
  "report": {
    "type": "weekly",
    "hours": 168,
    "short_hours": 24,
    "long_hours": 168
  },
  "summary": {
    "daily_cluster_inspector": {
      "status": "healthy",
      "anomaly_count": 0
    },
    "capacity_trend_forecaster": {
      "cpu_avg_percent": 35.2,
      "memory_avg_percent": 51.7,
      "cpu_trend": "flat",
      "simulation_status": "ok"
    },
    "availability_risk_scanner": {
      "risk_level": "medium",
      "issue_count": 5
    },
    "cost_optimization_advisor": {
      "nodes_clearly_below_average": 2,
      "oversized_requests": 8
    },
    "oncall_copilot": {
      "status": "provided",
      "source": "path-or-inline",
      "summary": "incident summary"
    }
  },
  "recommendations": [
    "[huawei-cloud-cce-availability-risk-scanner] ...",
    "[huawei-cloud-cce-cost-optimization-advisor] ...",
    "[huawei-cloud-cce-capacity-trend-forecaster][medium] ..."
  ],
  "data_gaps": [],
  "sources": {
    "daily_cluster_inspector": {"success": true},
    "capacity_trend_forecaster": {"success": true, "files": {}},
    "availability_risk_scanner": {"success": true, "files": {}},
    "cost_optimization_advisor": {"success": true, "files": {}},
    "oncall_copilot": {"status": "provided", "source": "inline"}
  },
  "files": {
    "summary": "/path/ops-weekly-summary.json",
    "report": "/path/ops-weekly-report.md",
    "report_html": "/path/ops-weekly-report.html",
    "trend_chart": "/path/ops-capacity-trend.svg",
    "simulation_chart": "/path/ops-capacity-simulation.svg",
    "raw": "/path/ops-weekly-raw.json"
  }
}
```

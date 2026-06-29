# Output Schema

```json
{
  "success": true,
  "action": "analyze_cce_capacity_trend",
  "generated_at": "2026-05-29T00:00:00+00:00",
  "cluster_name": "cluster-name",
  "scope": {
    "region": "cn-north-4",
    "cluster_id": "cluster-id",
    "hours": 168,
    "step_seconds": 3600,
    "excluded_namespaces": ["kube-system"],
    "business_namespaces": []
  },
  "capacity_series": [
    {
      "timestamp": 1760000000,
      "time_utc": "2026-01-01T00:00:00+00:00",
      "cpu_avg_percent": 42.1,
      "memory_avg_percent": 55.3,
      "disk_avg_percent": 38.0,
      "node_samples": 3
    }
  ],
  "capacity_stats": {
    "cpu": {
      "avg_percent": 40.2,
      "p95_percent": 72.8,
      "max_percent": 79.4,
      "latest_percent": 51.0,
      "trend": "rising",
      "slope_percent_per_hour": 0.2,
      "bottleneck_prediction": {
        "status": "projected",
        "hours_to_threshold": 24.5,
        "threshold_percent": 80
      }
    }
  },
  "elasticity": {
    "node_autoscaler": {
      "enabled": true,
      "current_nodes": 5,
      "min_nodes": 3,
      "max_nodes": 10
    },
    "hpa": {
      "status": "configured",
      "count": 4,
      "business_deployments": 8,
      "covered_business_deployments": 4,
      "coverage_percent": 50
    }
  },
  "simulation": {
    "status": "ok",
    "target_cpu_percent": 60,
    "target_memory_percent": 70,
    "headroom_percent": 15,
    "avg_recommended_nodes": 4.2,
    "max_recommended_nodes": 7,
    "estimated_reducible_nodes": 1,
    "capped_sample_percent": 0,
    "series": []
  },
  "recommendations": [
    {
      "id": "increase-hpa-coverage",
      "priority": "medium",
      "area": "workload-elasticity",
      "reason": "why this matters",
      "suggestion": "what to change",
      "configuration_method": []
    }
  ],
  "history_comparison": {
    "available": true,
    "compared_record": "capacity-trend-record-id",
    "deltas": {
      "cpu": {
        "avg_delta_percent": 1.2,
        "p95_delta_percent": 3.4,
        "max_delta_percent": 4.5
      }
    }
  },
  "data_gaps": [],
  "files": {
    "summary": "capacity-trend-summary.json",
    "report": "capacity-trend-report.md",
    "report_html": "capacity-trend-report.html",
    "trend_chart": "capacity-trend-chart.svg",
    "simulation_chart": "capacity-simulation-chart.svg",
    "history_record": "history/capacity-trend-*.json"
  }
}
```

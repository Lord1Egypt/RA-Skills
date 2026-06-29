# Output Schema

```json
{
  "success": true,
  "action": "scan_cce_availability_risk",
  "scope": {
    "region": "cn-north-4",
    "cluster_id": "cluster-id",
    "excluded_namespaces": ["kube-system"],
    "gateway_keywords": ["nginx", "gateway", "ingress"],
    "metrics_hours": 24
  },
  "inventory": {
    "nodes": 0,
    "workloads": 0,
    "pods": 0,
    "pdbs": 0,
    "services": 0,
    "ingresses": 0,
    "node_zone_distribution": {},
    "pod_zone_distribution": {}
  },
  "cluster": {
    "control_plane": {
      "status": "healthy | risk | unknown",
      "visible_master_nodes": 0,
      "zone_distribution": {},
      "metrics": []
    },
    "resources": {
      "cpu_request_allocatable_ratio": 0,
      "cpu_limit_allocatable_ratio": 0,
      "memory_request_allocatable_ratio": 0,
      "memory_limit_allocatable_ratio": 0,
      "missing_request_containers": 0
    }
  },
  "issues": [
    {
      "severity": "critical | high | medium | low",
      "category": "single-replica | pdb | health-check | affinity | az-distribution | gateway | resources",
      "resource": "Deployment/default/app",
      "message": "risk detail",
      "recommendation": "fix suggestion"
    }
  ],
  "summary": {
    "risk_level": "critical | high | medium | low",
    "issue_count": 0,
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0
  },
  "recommendations": [],
  "remediation_plan": [],
  "data_gaps": [],
  "files": {
    "summary": "optional availability-risk-summary.json path",
    "report": "optional availability-risk-report.md path",
    "raw_inventory": "optional raw inventory path"
  }
}
```

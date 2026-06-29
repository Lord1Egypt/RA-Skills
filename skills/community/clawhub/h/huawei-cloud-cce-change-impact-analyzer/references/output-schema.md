# Output Schema

`huawei_change_impact_analyze` returns structured JSON and always includes `report_markdown`.

```json
{
  "success": true,
  "analysis_trace_id": "CIA-yyyymmddHHMMSS-xxxxxxxx",
  "analysis_window": {
    "start_time": "YYYY-MM-DD HH:MM:SS",
    "end_time": "YYYY-MM-DD HH:MM:SS",
    "hours": 1
  },
  "scope": {
    "region": "cn-north-4",
    "cluster_id": "cluster-id",
    "namespace": "optional",
    "target_name": "optional"
  },
  "summary": {
    "core_change_count": 3,
    "top_risk_count": 3,
    "data_sources": {
      "CCE Audit Logs": "success",
      "K8s Historical Events": "success",
      "AOM Alarms": "success",
      "Current Resource Snapshots": "success"
    }
  },
  "top_changes": [
    {
      "time": "YYYY-MM-DD HH:MM:SS",
      "verb": "patch",
      "resource": "configmaps",
      "namespace": "kube-system",
      "name": "coredns",
      "object_key": "kube-system/coredns",
      "category": "global_config_change",
      "title": "Cluster core configuration change",
      "actor": "user or serviceAccount",
      "semantic_fields": ["data", "Corefile"],
      "blast_radius": "cluster-wide",
      "impacted_entities": {
        "pods": [],
        "services": ["kube-system/kube-dns"],
        "ingresses": [],
        "nodes": ["node-a"]
      },
      "risk_score": 96,
      "risk_level": "Critical",
      "confidence": "high",
      "risk_reasons": [],
      "evidence": []
    }
  ],
  "changes": [],
  "report_markdown": "# CCE Change Impact Analysis Report\n...",
  "report_file": "/optional/path/report.md",
  "capture_metadata": {}
}
```

## Markdown Report Structure

The customer-deliverable report must include the following sections:

1. `Analysis Summary`: Trace ID, cluster, region, scope, target object, window, core change count, initial conclusion.
2. `Investigation Process`: Four-stage pipeline description.
3. `Data Sources & Collection Status`: Audit logs, K8s events, AOM alarms, resource snapshot success/failure status.
4. `Core Change Timeline`: Time-ordered key changes table.
5. `Top Risk Alerts`: Top N changes, risk level, score, confidence, basis.
6. `Blast Radius & Propagation Paths`: Impacted Pod/Service/Ingress/Node or global paths.
7. `Evidence Matrix`: Audit, event, alarm evidence.
8. `Conclusion & Verification Suggestions`: Final judgment, read-only verification suggestions, remediation action handoff description.
9. `Reused Capabilities`: List of tools reused in this analysis.
10. `Capability Gaps & Strengthening Suggestions`: Explain boundaries caused by incomplete data.
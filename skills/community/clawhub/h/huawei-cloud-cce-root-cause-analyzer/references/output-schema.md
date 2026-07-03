# Output Schema

```json
{
  "success": true,
  "analysis_trace_id": "RCA-...",
  "scope": {
    "region": "cn-north-4",
    "cluster_id": "cluster-id",
    "namespace": "optional",
    "target_name": "optional workload/app/service"
  },
  "summary": {
    "top_cause": {},
    "cause_count": 3,
    "data_sources": {
      "rollout": true,
      "dependency": true,
      "change": true,
      "alarms": true
    }
  },
  "top_causes": [
    {
      "rank": 1,
      "type": "ContainerCommandNotFound",
      "title": "New version container startup command or entry file does not exist",
      "domain": "workload",
      "confidence": 0.94,
      "evidence": [],
      "counter_evidence": [],
      "recommendation": [],
      "remediation_hint": {
        "skill": "huawei-cloud-cce-auto-remediation-runner",
        "action": "huawei_auto_remediation_run",
        "strategy": "rollback_previous_revision",
        "requires_confirmation": true
      }
    }
  ],
  "report_markdown": "# CCE Comprehensive Root Cause Analysis Report...",
  "report_file": "optional"
}
```
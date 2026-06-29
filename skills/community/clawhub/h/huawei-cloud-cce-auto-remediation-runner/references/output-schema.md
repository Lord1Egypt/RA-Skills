# Output Schema

## Remediation Preview (confirm=false)

```json
{
  "success": false,
  "requires_confirmation": true,
  "remediation_trace_id": "ARR-...",
  "strategy": "rollback_previous_revision",
  "diagnosis": {},
  "action_result": {},
  "preview": {
    "action": "huawei_rollback_cce_workload | huawei_scale_cce_workload | huawei_cce_node_drain | ...",
    "target": {
      "region": "cn-north-4",
      "cluster_id": "optional",
      "namespace": "optional",
      "kind": "optional",
      "name": "optional",
      "node_name": "optional"
    },
    "current_state": {},
    "expected_state": {},
    "impact_scope": {},
    "rollback_method": ""
  },
  "risk_level": "R1 | R2 | R3",
  "rollback_notes": [],
  "summary": "Remediation plan preview — requires user confirmation before execution"
}
```

## Remediation Execution (confirm=true)

```json
{
  "success": true,
  "requires_confirmation": false,
  "confirmation_received": true,
  "remediation_trace_id": "ARR-...",
  "strategy": "rollback_previous_revision",
  "action_result": {},
  "execution": {
    "action": "...",
    "timestamp": "...",
    "result": {}
  },
  "verification": [
    {
      "method": "huawei_get_cce_pods | huawei_get_kubernetes_nodes | huawei_workload_rollout_diagnose | huawei_node_diagnose | huawei_workload_diagnose",
      "status": "healthy | degraded | failed",
      "details": {}
    }
  ],
  "rollback_notes": [],
  "report_markdown": "# CCE Auto Remediation Execution Report...",
  "report_file": "optional"
}
```

## Full Auto-Remediation Orchestration Output

```json
{
  "success": false,
  "requires_confirmation": true,
  "remediation_trace_id": "ARR-...",
  "strategy": "rollback_previous_revision | scale_out | drain_and_replace | ...",
  "diagnosis": {},
  "action_result": {},
  "verification": {},
  "summary": "remediation plan or execution result",
  "action": "huawei_auto_remediation_run",
  "risk_level": "R2 | R3",
  "target": {
    "region": "cn-north-4",
    "cluster_id": "optional",
    "resource": "optional"
  },
  "preview": {},
  "requires_confirmation": true,
  "confirmation_received": false,
  "execution": {},
  "verification": [],
  "rollback_notes": [],
  "report_markdown": "# CCE Auto Remediation Execution Report...",
  "report_file": "optional"
}
```
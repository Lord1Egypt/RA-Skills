# Output Schema

The primary tool `huawei_node_failure_diagnose` returns structured evidence and a Markdown report. The final user-facing output should preferentially use `report_markdown`.

```json
{
  "success": true,
  "action": "huawei_node_failure_diagnose",
  "region": "cn-north-4",
  "cluster_id": "cluster-id",
  "node": {
    "name": "node-name",
    "internal_ip": "10.0.0.1",
    "ready": "True | False | Unknown",
    "conditions": [
      {
        "type": "Ready",
        "status": "Unknown",
        "reason": "NodeStatusUnknown",
        "message": "...",
        "last_heartbeat_time": "2026-05-30T10:00:00Z",
        "last_transition_time": "2026-05-30T10:01:00Z"
      }
    ]
  },
  "lease": {
    "found": true,
    "namespace": "kube-node-lease",
    "renew_time": "2026-05-30T10:00:00Z",
    "renew_delay_seconds": 72,
    "stale": true,
    "threshold_seconds": 40
  },
  "liveness": {
    "case": "A | B | C | D",
    "ready": "True | False | Unknown",
    "lease_stale": true,
    "conclusion": "Control plane disconnected from node",
    "inference": "Ready=Unknown and Lease renewal exceeds threshold..."
  },
  "root_category": "ControlPlaneDisconnected | MemoryPressure | DiskPressure | Network | Kubelet | NotReady | Healthy",
  "conclusion": "Control plane disconnected from node (network link or Kubelet/CRI heartbeat interrupted, requires node-side verification)",
  "confidence": "High",
  "scores": {
    "ControlPlaneDisconnected": 8,
    "MemoryPressure": 11,
    "Kubelet": 4
  },
  "evidence": [
    {
      "category": "MemoryPressure",
      "severity": "critical",
      "signal": "SystemOOM",
      "source": "Event/kubelet",
      "detail": "System OOM encountered..."
    }
  ],
  "pod_summary": {
    "total": 24,
    "phase_counts": {
      "Running": 10,
      "Unknown": 14
    },
    "symptomatic": [],
    "observed": [
      {
        "namespace": "kube-system",
        "name": "node-local-dns-abc",
        "phase": "Running",
        "restart_total": 0,
        "core_daemon": true
      }
    ]
  },
  "health_items": [
    {
      "item": "Memory Pressure",
      "status": "Indeterminate",
      "detail": "MemoryPressure=Unknown; evidence_score=0"
    }
  ],
  "node_events": [],
  "pod_events": [],
  "metrics": {},
  "metric_error": null,
  "report_markdown": "# Kubernetes Node Automated Diagnosis Report\n..."
}
```

## Required Markdown Report Sections

1. `# Kubernetes Node Automated Diagnosis Report`
2. `## 1. Diagnosis Overview`: target node, diagnosis conclusion, confidence level, blast radius.
3. `## 2. Node Status Health`: NotReady, memory pressure, disk pressure, network status, Kubelet status, node scheduling taints; when pressure conditions are `Unknown` with `NodeStatusUnknown` reason and no independent evidence exists, label as "indeterminate" — do not mark as "normal".
4. `## 3. Key Investigation`: control plane liveness triage, key event timeline, node workload anomaly observation, metric snapshot, evidence matrix.
5. `## 4. Diagnosis Conclusion`: derive conclusions from evidence, and indicate parts that still require local log confirmation.
6. `## 5. Remediation Recommendations`: provide suggestions and verification steps only; do not directly execute changes.
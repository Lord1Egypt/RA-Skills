# Output Schema

The primary tool `huawei_autoscaling_diagnose` returns structured evidence and a Markdown report. The final customer-facing output should prefer `report_markdown`.

```json
{
  "success": true,
  "action": "huawei_autoscaling_diagnose",
  "generated_at": "2026-05-30T00:00:00+00:00",
  "region": "cn-north-4",
  "cluster_id": "cluster-id",
  "intent": {
    "target": "WORKLOAD | NODE | UNKNOWN",
    "scale_direction": "scale_up | scale_down | unknown",
    "question": "Why isn't autoscaling working?"
  },
  "scope": {
    "namespace": "default",
    "workload_name": "api",
    "workload_type": "Deployment"
  },
  "route": "A | B | C | BLOCKED",
  "discovery": {
    "has_hpa": true,
    "hpa_count": 1,
    "selected_hpa_count": 1,
    "has_ca": true,
    "ca_addon_installed": true,
    "nodepool_autoscaling_enabled": true,
    "nodepool_max_reached": [],
    "metric_addon_detected": true
  },
  "issues": [
    {
      "code": "HPA_CONTAINER_REQUEST_MISSING",
      "title": "Containers sampled by HPA lack resource requests",
      "severity": "critical",
      "layer": "HPA",
      "evidence": "default/api-abc:app missing cpu",
      "recommendation": "Set resources.requests for the HPA metric on all target Pod containers."
    }
  ],
  "evidence": [
    {
      "layer": "CA-Log",
      "source": "Pod/cce-cluster-autoscaler-abc123 logs (tail=200)",
      "summary": "CA Pod=kube-system/cce-cluster-autoscaler-abc123, container=autoscaler, log_signals=3, snippet=\\\"NoExpansionOptions: ... subnet ip exhausted...\\\""
    },
    {
      "layer": "HPA",
      "source": "HorizontalPodAutoscaler/status",
      "summary": "default/api-hpa -> Deployment/api, min=2, max=10, current=2, desired=2"
    }
  ],
  "data_gaps": [],
  "conclusion": "Containers sampled by HPA lack resource requests: default/api-abc:app missing cpu",
  "confidence": "High",
  "report_markdown": "# CCE Autoscaling Automated Diagnosis Report\n..."
}
```

## Required Markdown Report Sections

1. `# CCE Autoscaling Automated Diagnosis Report`
2. `## 1. Diagnosis Overview`: Region, cluster, semantic intent, scale direction, diagnosis route, conclusion, confidence.
3. `## 2. Capability Discovery & Routing`: Has_HPA, Has_CA, metric pipeline, and routing basis.
4. `## 3. Investigation Process`: Gateway, Path A/B/C actual execution steps.
5. `## 4. Key Evidence`: HPA status, node pool/addon, Pending Pod, FailedScheduling, and other evidence.
6. `## 5. Issues & Root Cause Convergence`: Issues ranked by severity with evidence and recommendations.
7. `## 6. Next-Step Recommendations`: Read-only verification and remediation suggestions; do not execute changes directly.
8. `## 7. Data Gaps`: Collection failures and items that current atomic capabilities cannot confirm.

## Severity Level Definitions

- `critical`: Sufficient to independently explain the scaling blockage, e.g., no HPA, missing request, CA not installed, node pool autoscaling not enabled, maxReplicas/max_nodes reached.
- `high`: Strongly correlated blocking evidence, e.g., FailedScheduling with resource insufficient, affinity/taint conflict, cloud resource quota or permission signals.
- `medium`: Suspicious items requiring review, e.g., metric addon not identified, safe-to-evict key exists but value missing.
- `info`: Current behavior may be normal non-triggering, e.g., metric below threshold, no Pending Pods.
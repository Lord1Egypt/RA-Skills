# Output Schema

Primary action: `huawei_workload_rollout_diagnose`.

```json
{
  "success": true,
  "action": "workload_rollout_diagnose",
  "target": {
    "namespace": "default",
    "kind": "Deployment",
    "name": "api"
  },
  "selector": {
    "value": "app=api",
    "source": "matchLabels"
  },
  "summary": {
    "status": "control_plane_not_observed | new_version_not_created | rollout_blocked | replicas_unavailable | probe_failure | healthy",
    "headline": "human-readable diagnosis; may note when old-version replicas remain available",
    "expected_replicas": 3,
    "ready_replicas": 1,
    "available_replicas": 1,
    "top_cause": "ProbeFailure | ContainerCommandNotFound | CrashLoopOrAppExit | ..."
  },
  "generation_check": {
    "generation": 5,
    "observed_generation": 5,
    "observed": true
  },
  "workload": {
    "kind": "Deployment",
    "uid": "workload-uid",
    "desired_replicas": 3,
    "updated_replicas": 3,
    "ready_replicas": 1,
    "available_replicas": 1,
    "conditions": []
  },
  "version": {
    "strategy": "DeploymentReplicaSet",
    "new_rs": {},
    "old_rs": []
  },
  "funnel": [
    {"layer": "workload_current", "expected": 3, "actual": 3, "status": "pass"},
    {"layer": "new_pods_ready", "expected": 3, "actual": 1, "status": "fail"}
  ],
  "events": {
    "filtered_count": 5,
    "timeline": [],
    "filter": {
      "uid_count": 6,
      "before_count": 40,
      "after_count": 5,
      "events_without_involved_uid": 0
    }
  },
  "pod_diagnosis": {
    "diagnosed_pods": 1,
    "pods": []
  },
  "top_causes": [
    {
      "rank": 1,
      "type": "ProbeFailure",
      "title": "New version Pods are Running but probe checks fail or Pods are not Ready",
      "confidence": 0.88,
      "evidence": [],
      "recommendation": []
    }
  ],
  "handoff": [
    {
      "skill": "huawei-cloud-cce-pod-failure-diagnoser",
      "reason": "Probe failure requires Pod logs and health check configuration analysis"
    }
  ],
  "warnings": []
}
```

Context-only action: `huawei_get_workload_rollout_context`.

```json
{
  "success": true,
  "action": "get_workload_rollout_context",
  "workload": {},
  "replicasets": [],
  "pods": [],
  "events": [],
  "event_filter": {},
  "warnings": []
}
```

## Field Descriptions

| Field                     | Type    | Description                                                    |
| ------------------------- | ------- | -------------------------------------------------------------- |
| `summary.status`          | string  | One of: `healthy`, `control_plane_not_observed`, `new_version_not_created`, `rollout_blocked`, `replicas_unavailable`, `probe_failure` |
| `summary.headline`        | string  | Human-readable diagnosis summary                               |
| `summary.top_cause`       | string  | Primary Top Cause type (e.g., `ProbeFailure`, `CrashLoopOrAppExit`) |
| `generation_check.observed` | boolean | `true` if `observedGeneration >= generation`                  |
| `funnel[].layer`          | string  | Funnel layer name (e.g., `workload_current`, `new_pods_ready`) |
| `funnel[].status`         | string  | `pass` or `fail`                                               |
| `top_causes[].rank`       | integer | Cause ranking (1 = highest)                                   |
| `top_causes[].confidence` | float   | Confidence score (0.0-1.0)                                    |
| `handoff[].skill`         | string  | Target skill name using `huawei-cloud-cce-` prefix convention  |
| `handoff[].reason`        | string  | Reason for the handoff                                         |

## Handoff Skill Reference Mapping

| Old Name                    | New Name (Prefixed)                          |
| --------------------------- | -------------------------------------------- |
| `huawei-cloud-cce-pod-failure-diagnoser`     | `huawei-cloud-cce-pod-failure-diagnoser`     |
| `huawei-cloud-cce-node-failure-diagnoser`    | `huawei-cloud-cce-node-failure-diagnoser`    |
| `huawei-cloud-cce-root-cause-analyzer`       | `huawei-cloud-cce-root-cause-analyzer`       |
| `huawei-cloud-cce-auto-remediation-runner`   | `huawei-cloud-cce-auto-remediation-runner`   |
| `huawei-cloud-cce-alarm-correlation-engine`  | `huawei-cloud-cce-alarm-correlation-engine`  |
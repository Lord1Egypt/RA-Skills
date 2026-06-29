# Output Schema

```json
{
  "summary": "one paragraph context summary",
  "scope": {
    "region": "cn-north-4",
    "cluster_id": "optional",
    "namespace": "optional",
    "workload": "optional",
    "time_window": "optional"
  },
  "signals": {
    "alarms": [],
    "events": [],
    "metrics": [],
    "logs": []
  },
  "timeline": [],
  "gaps": [],
  "next_skill": "huawei-cloud-cce-pod-failure-diagnoser | huawei-cloud-cce-node-failure-diagnoser | huawei-cloud-cce-network-failure-diagnoser | huawei-cloud-cce-root-cause-analyzer"
}
```
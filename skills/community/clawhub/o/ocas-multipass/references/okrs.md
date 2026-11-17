# Multipass — OKRs

```yaml
skill_okrs:
  - name: tool_invocation_success_rate
    metric: fraction of tool invocations completed successfully
    direction: maximize
    target: 0.92
    evaluation_window: 30_runs
  - name: spawn_depth_efficiency
    metric: average ratio of tasks completed to spawn depth used
    direction: maximize
    target: 0.80
    evaluation_window: 30_runs
  - name: isolation_violation_rate
    metric: fraction of isolated sessions that do not leak context or state outside their boundaries
    direction: maximize
    target: 1.0
    evaluation_window: 30_runs
  - name: schedule_adherence
    metric: fraction of runs that complete within expected time bounds
    direction: maximize
    target: 0.90
    evaluation_window: 30_runs
  - name: data_integrity
    metric: fraction of runs with complete, uncorrupted output and evidence records
    direction: maximize
    target: 0.95
    evaluation_window: 30_runs
```

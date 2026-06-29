# Output Schema

## Log Query Summary

When querying logs (Pod stdout, application logs, or audit logs), prefer this output structure:

| Field | Description |
|------|-------------|
| `region` | Huawei Cloud region |
| `cluster_id` | CCE cluster ID when querying Kubernetes or CCE application logs |
| `namespace` | Kubernetes namespace when available |
| `pod_name` | Pod name when available |
| `container` | Container name when available |
| `log_group_id` | LTS log group ID when querying LTS |
| `log_stream_id` | LTS log stream ID when querying LTS |
| `time_range` | Effective start/end time or recent-hours window |
| `keywords` | Keyword filter used |
| `total` | Number of returned log entries |
| `has_more` | Whether an LTS scroll id indicates more data |

## LogConfig Discovery Summary

| Field | Description |
|------|-------------|
| `matched_streams` | List of matched LogConfig policies with group/stream IDs |
| `policy_name` | LogConfig policy name |
| `source_type` | `container_stdout` or `container_file` |
| `log_group_id` | LTS group ID for the policy |
| `log_stream_id` | LTS stream ID for the policy |

## LogConfig Preview Summary

When previewing LogConfig creation or deletion:

| Field | Description |
|------|-------------|
| `request_body` | Generated LogConfig specification (create preview) |
| `existing` | Current LogConfig details being targeted (delete preview) |
| `action` | `create` or `delete` |
| `logconfig_name` | LogConfig policy name |
| `namespace` | LogConfig namespace |

## Audit Log Summary

| Field | Description |
|------|-------------|
| `audit_type` | Keyword preset used (`pod_delete`, `workload_change`) |
| `verbs` | Operation verbs found (delete, create, update, etc.) |
| `users` | Actors performing operations |
| `resources` | Resource types affected |
| `namespaces` | Namespaces affected |
| `status_codes` | Response status codes distribution |
| `event_count` | Number of audit events returned |
| `top_events` | Top audit events with counts and timestamps |

## Analysis Summary

When analyzing logs, prefer this structure:

| Field | Description |
|------|-------------|
| `error_patterns` | Recurring error messages or stack trace roots |
| `first_seen` | Earliest returned timestamp for a pattern |
| `last_seen` | Latest returned timestamp for a pattern |
| `affected_resources` | Pods, containers, workloads, or namespaces involved |
| `evidence` | Short redacted examples, not full raw logs |
| `next_steps` | Suggested follow-up query or diagnosis skill |

## Abnormality Analysis Output

| Field | Description |
|------|-------------|
| `abnormal_ratio` | Percentage of abnormal logs vs total |
| `log_rate_total` | Total log entries per time unit |
| `log_rate_abnormal` | Abnormal log entries per time unit |
| `first_abnormal_time` | First abnormal log timestamp |
| `last_abnormal_time` | Last abnormal log timestamp |
| `recovery_time` | Observed recovery timestamp (if detected) |
| `incident_windows` | Time windows where abnormality is concentrated |
| `top_patterns` | Top recurring abnormal patterns with counts |
| `status_code_distribution` | HTTP status code counts (especially 5xx) |
| `samples` | Redacted sample abnormal log entries |
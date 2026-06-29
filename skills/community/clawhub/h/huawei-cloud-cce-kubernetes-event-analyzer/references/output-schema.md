# Output Schema

## Event Query Summary

| Field | Description |
|------|-------------|
| `region` | Huawei Cloud region |
| `cluster_id` | CCE cluster ID |
| `namespace` | Kubernetes namespace (optional filter) |
| `event_type` | Event type filter applied (e.g., Warning) |
| `time_range` | Effective start/end time or recent-hours window |
| `total_events` | Number of returned events |
| `warning_count` | Number of Warning events |
| `normal_count` | Number of Normal events |

## Analysis Summary

| Field | Description |
|------|-------------|
| `top_reasons` | Top event reasons with counts, sorted by frequency |
| `repeated_patterns` | Events with count > 1, grouped by reason |
| `namespace_breakdown` | Event counts by namespace |
| `first_warning` | Timestamp of first Warning event in window |
| `last_warning` | Timestamp of last Warning event in window |
| `affected_objects` | Count of unique involved objects with Warning events |
| `next_steps` | Suggested follow-up query or diagnosis skill |

## Event Detail (per event)

| Field | Description |
|------|-------------|
| `reason` | Event reason (e.g., FailedScheduling, ImagePullBackOff, FailedMount) |
| `message` | Event message (summarized, redacted) |
| `involved_object_kind` | Kind of the involved object (Pod, Node, Deployment, etc.) |
| `involved_object_name` | Name of the involved object (redacted in public output) |
| `namespace` | Namespace of the involved object |
| `count` | Number of times this event occurred |
| `first_timestamp` | First occurrence |
| `last_timestamp` | Most recent occurrence |
| `type` | Event type (Normal, Warning) |

## K8s API Response Fields (huawei_get_cce_events)

| Field | Description |
|------|-------------|
| `region` | Huawei Cloud region |
| `cluster_id` | CCE cluster ID |
| `namespace` | Kubernetes namespace filter (if applied) |
| `total_fetched` | Number of events returned by the API |
| `events` | Raw event list (apply filters client-side) |
| `warning_count` | Number of Warning events (calculated) |
| `top_reasons` | Top event reasons with counts (calculated) |
| `repeated_patterns` | Events with count > 1 grouped by reason |
| `namespace_breakdown` | Event counts by namespace |
| `next_steps` | Suggested follow-up query or diagnosis skill |

## LTS Response Fields (huawei_query_k8s_events_from_lts)

| Field | Description |
|------|-------------|
| `region` | Huawei Cloud region |
| `cluster_id` | CCE cluster ID |
| `log_group_id` | LTS log group ID |
| `log_stream_id` | LTS log stream ID |
| `keywords` | Keywords used for filtering |
| `event_count` | Number of events returned |
| `events` | Parsed event list with normalized structure |
| `time_range` | Start/end time of the query |
| `log_config` | LogConfig info (name, events enabled, etc.) |
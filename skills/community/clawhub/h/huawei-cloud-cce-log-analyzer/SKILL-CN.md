---
name: log-analyzer
description: Use this skill to query and analyze Kubernetes Pod stdout logs, CCE LogConfig-collected application logs, and Huawei Cloud LTS logs.
---

# Log Analyzer

Query and analyze Kubernetes standard output logs and Huawei Cloud LTS logs for CCE workloads.

This skill reuses the shared Huawei Cloud dispatcher in `scripts/huawei-cloud.py`; implementation code lives in:

- `scripts/huawei_cloud/cce.py` for Kubernetes Pod stdout logs (`huawei_get_pod_logs`)
- `scripts/huawei_cloud/cce_app_logs.py` for CCE LogConfig discovery and application log stream matching
- `scripts/huawei_cloud/lts.py` for LTS log group, stream, and log queries

## Scope

Use this skill when the user asks to:

- Query Kubernetes Pod standard output or previous container logs
- Inspect CCE LogConfig resources for stdout collection
- Create CCE LogConfig resources for container stdout or container file collection
- Delete CCE LogConfig resources when the user explicitly asks to remove log collection rules
- Find the LTS log group/stream for an application or namespace
- Query CCE Kubernetes audit logs for Pod deletion or workload change events
- Query LTS logs by time range, recent hours, keywords, or labels
- Analyze returned logs for repeated errors, stack traces, restarts, or failure clues

Do not use this skill to modify workloads, LTS groups/streams, or other cloud resources. Creating or deleting LogConfig resources is supported only through the LogConfig tools and must use `confirm=true` after preview.

## Tools

| Tool | Purpose | Required parameters |
|------|---------|---------------------|
| `huawei_get_pod_logs` | Query Kubernetes Pod stdout/stderr through the Kubernetes API | `region`, `cluster_id`, `pod_name` |
| `huawei_get_cce_logconfigs` | List CCE LogConfig resources in a cluster | `region`, `cluster_id` |
| `huawei_create_cce_logconfig` | Create a CCE LogConfig for container stdout or container file collection; preview by default, create with `confirm=true` | `region`, `cluster_id`, `logconfig_name`, `source_type`, `log_group_id`, `log_stream_id` |
| `huawei_delete_cce_logconfig` | Delete a CCE LogConfig by name; preview by default, delete with `confirm=true` | `region`, `cluster_id`, `logconfig_name` |
| `huawei_get_application_logconfigs` | Match app/workload to LTS log group and stream, including stdout and container file LogConfig policies | `region`, `cluster_id`, `app_name` |
| `huawei_query_cce_audit_logs` | Query CCE audit logs from LTS and summarize Pod deletion, workload changes, verbs, users, resources, namespaces, and response codes | `region`, `cluster_id` |
| `huawei_query_application_logs` | Query application logs from matched LTS stream; optionally specify `logconfig_name`/`policy_name` | `region`, `cluster_id`, `app_name` |
| `huawei_query_application_recent_logs` | Query recent application logs from matched LTS stream; optionally specify `logconfig_name`/`policy_name` | `region`, `cluster_id`, `app_name` |
| `huawei_analyze_application_logs` | Analyze application logs in a time range for abnormal keywords, HTTP errors, incident windows, recovery time, and abnormal ratios | `region`, `cluster_id`, `app_name` |

## Examples

```bash
# Query recent stdout from a Pod
python3 scripts/huawei-cloud.py huawei_get_pod_logs \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  namespace=default \
  pod_name=<pod-name> \
  tail_lines=200

# Query previous terminated container logs
python3 scripts/huawei-cloud.py huawei_get_pod_logs \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  namespace=default \
  pod_name=<pod-name> \
  container=<container-name> \
  previous=true \
  tail_lines=200

# Discover app LTS stream from LogConfig
python3 scripts/huawei-cloud.py huawei_get_application_logconfigs \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  namespace=default \
  app_name=<workload-name>

# Preview then create a workload stdout LogConfig
python3 scripts/huawei-cloud.py huawei_create_cce_logconfig \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  logconfig_name=<policy-name> \
  source_type=container_stdout \
  workload_namespace=default \
  workload_name=<workload-name> \
  workload_kind=Deployment \
  log_group_id=<lts-group-id> \
  log_stream_id=<lts-stream-id>

# Preview then delete a LogConfig
python3 scripts/huawei-cloud.py huawei_delete_cce_logconfig \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  logconfig_name=<policy-name> \
  logconfig_namespace=kube-system

# Query Pod deletion audit events
python3 scripts/huawei-cloud.py huawei_query_cce_audit_logs \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  audit_type=pod_delete \
  namespace=default \
  hours=6 \
  log_group_id=<audit-lts-group-id> \
  log_stream_id=<audit-lts-stream-id>

# Query workload change audit events
python3 scripts/huawei-cloud.py huawei_query_cce_audit_logs \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  audit_type=workload_change \
  namespace=default \
  start_time="2026-05-30 10:00:00" \
  end_time="2026-05-30 11:00:00"

# Preview then create a container file LogConfig
python3 scripts/huawei-cloud.py huawei_create_cce_logconfig \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  logconfig_name=<policy-name> \
  source_type=container_file \
  workload_namespace=default \
  workload_name=<workload-name> \
  workload_kind=Deployment \
  container=<container-name> \
  log_path=/var/log \
  file_pattern="*.log" \
  log_group_id=<lts-group-id> \
  log_stream_id=<lts-stream-id>

# Query recent application logs from a specific LogConfig policy
python3 scripts/huawei-cloud.py huawei_query_application_recent_logs \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  namespace=default \
  app_name=<workload-name> \
  logconfig_name=<policy-name> \
  hours=1 \
  keywords=ERROR \
  auto_paginate=true \
  max_pages=5 \
  limit=100

# Analyze an application log window for abnormal logs
python3 scripts/huawei-cloud.py huawei_analyze_application_logs \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  namespace=default \
  app_name=<workload-name> \
  logconfig_name=<policy-name> \
  start_time="2026-05-30 10:00:00" \
  end_time="2026-05-30 11:00:00" \
  auto_paginate=true \
  max_pages=5 \
  limit=1000

```

## Analysis Guidance

- Start with the narrowest useful scope: pod/container stdout first when the user names a pod, application LTS logs when they name a workload.
- Prefer recent windows (`hours=1`, `tail_lines=100-500`) before broad historical searches.
- For workload-level LTS queries, first call `huawei_get_application_logconfigs` to discover the application's matched LogConfig policies. Then pass the desired `logconfig_name` or `policy_name` to `huawei_query_application_recent_logs` or `huawei_query_application_logs`.
- For LogConfig creation, first call without `confirm=true` and inspect `request_body`. Only call again with `confirm=true` after the user confirms the generated LogConfig.
- For LogConfig deletion, first call without `confirm=true` and inspect the returned `existing` target summary. Only call again with `confirm=true` after the user confirms the exact `logconfig_name` and namespace.
- Use `huawei_query_cce_audit_logs` for Kubernetes audit questions. It is pure keyword search over audit log content: `pod_name`, `resource_name`, `workload_name`, `namespace`, `user`, `verb`, `resource`, and `status_code` are all converted into query/content keywords instead of parsed-field filters.
- Use `audit_type=pod_delete` or `audit_type=workload_change` only as keyword presets. For example `pod_delete` adds `delete` and `pods`; the result is still based on keyword matching.
- Use the stdout policy for container standard output, and use a `container_file` policy when the user asks for application file logs collected from paths such as `/var/log/*.log`.
- Use `auto_paginate=true` when the user needs more than one LTS page. Keep `limit` as the per-page size and set `max_pages` to cap total work.
- Use `huawei_analyze_application_logs` when the user asks whether a time range contains exceptions, errors, recovery, abnormal proportions, or incident timing. Avoid adding `keywords` unless the user wants to analyze only logs matched by that keyword, because ratios are calculated over the queried log set.
- When summarizing logs, group repeated lines by pattern and include counts when possible.
- Redact tokens, passwords, cookies, authorization headers, and personally identifiable data.
- If logs point to Pod startup, image pull, scheduling, node, or network failures, recommend the corresponding diagnosis skill with the exact evidence found.

## References

- Workflow: `references/workflow.md`
- Risk rules: `references/risk-rules.md`
- Output schema: `references/output-schema.md`

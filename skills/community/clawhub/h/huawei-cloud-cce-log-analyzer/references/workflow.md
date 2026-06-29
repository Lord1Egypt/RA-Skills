# Workflow

## Kubernetes Pod Stdout Logs

1. Identify `region`, `cluster_id`, `namespace`, `pod_name`, and optional `container`.
2. Use `huawei_get_pod_logs` for direct Kubernetes stdout/stderr retrieval.
3. Use `tail_lines` for focused recent output; use `previous=true` for a previously terminated container.
4. Summarize errors, warnings, stack traces, restarts, or repeated messages.
5. If logs indicate Pod startup, image pull, scheduling, node, or network failures, hand off to the relevant diagnosis skill with exact evidence.

**Example workflow**:

```
User: "Check Pod my-app-xyz123 logs for errors"
  → huawei_get_pod_logs (tail_lines=200)
  → Summarize: 3 OOMKilled restarts, last crash at 2026-05-30 10:15
  → Recommend: huawei-cloud-cce-pod-failure-diagnoser (OOM pattern detected)
```

## CCE Application Logs Through LTS

### Step 1: Discover LogConfig Policies

Use `huawei_get_application_logconfigs` to map an app/workload to matched LogConfig policies and their LTS `log_group_id` / `log_stream_id`.

```bash
python3 scripts/huawei-cloud.py huawei_get_application_logconfigs \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  namespace=default \
  app_name=<workload-name>
```

The response includes `matched_streams` listing all policies (stdout and container_file) with their LTS group/stream IDs.

### Step 2: Select the Right Policy

Pick the desired policy from `matched_streams`:
- Use **stdout policies** for standard output logs
- Use **container_file policies** for file logs collected from configured paths (e.g., `/var/log/*.log`)
- Pass the selected `logconfig_name` or `policy_name` to subsequent query tools

### Step 3: Query Application Logs

For **recent logs** (time window in hours):

```bash
python3 scripts/huawei-cloud.py huawei_query_application_recent_logs \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  namespace=default \
  app_name=<workload-name> \
  logconfig_name=<policy-name> \
  hours=1
```

For **explicit time windows**:

```bash
python3 scripts/huawei-cloud.py huawei_query_application_logs \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  namespace=default \
  app_name=<workload-name> \
  logconfig_name=<policy-name> \
  start_time="2026-05-30 10:00:00" \
  end_time="2026-05-30 11:00:00"
```

### Step 4: Paginate Large Results

Use `auto_paginate=true` when more than one LTS page is needed. `limit` controls per-page size and `max_pages` caps total pages fetched.

```bash
python3 scripts/huawei-cloud.py huawei_query_application_recent_logs \
  ... \
  auto_paginate=true \
  max_pages=5 \
  limit=100
```

### Step 5: Analyze for Abnormalities

Use `huawei_analyze_application_logs` for time-window abnormality analysis. It queries matched application logs, detects exception/error/fatal/timeout/OOM patterns and HTTP 5xx status codes, then returns:

- Abnormal ratio
- Log rates (total and abnormal per time unit)
- First/last abnormal timestamp
- Observed recovery time
- Incident windows
- Top abnormal patterns
- Status-code distribution
- Redacted samples

**Important**: Do not set `keywords` unless the user explicitly wants a keyword-scoped ratio. Keyword filtering changes the denominator to only matched logs, which distorts the abnormal ratio.

```bash
python3 scripts/huawei-cloud.py huawei_analyze_application_logs \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  namespace=default \
  app_name=<workload-name> \
  start_time="2026-05-30 10:00:00" \
  end_time="2026-05-30 11:00:00" \
  auto_paginate=true \
  max_pages=5 \
  limit=1000
```

## LogConfig Management

### List LogConfig Resources

```bash
python3 scripts/huawei-cloud.py huawei_get_cce_logconfigs \
  region=cn-north-4 \
  cluster_id=<cluster-id>
```

### Create a LogConfig (Preview → Confirm)

1. Call without `confirm=true` to preview the generated `request_body`
2. Inspect the preview output with the user
3. Call with `confirm=true` only after user confirmation

```bash
# Step 1: Preview
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

# Step 2: Confirm (after user review)
python3 scripts/huawei-cloud.py huawei_create_cce_logconfig \
  ... \
  confirm=true
```

For **container file collection**:

```bash
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
```

### Delete a LogConfig (Preview → Confirm)

1. Call without `confirm=true` to preview the exact target summary
2. Inspect the returned `existing` LogConfig details with the user
3. Call with `confirm=true` only after user confirms the exact `logconfig_name` and namespace

```bash
# Step 1: Preview
python3 scripts/huawei-cloud.py huawei_delete_cce_logconfig \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  logconfig_name=<policy-name> \
  logconfig_namespace=kube-system

# Step 2: Confirm (after user review)
python3 scripts/huawei-cloud.py huawei_delete_cce_logconfig \
  ... \
  confirm=true
```

## CCE Audit Logs

Use `huawei_query_cce_audit_logs` for Kubernetes audit questions. It is pure keyword search over audit log content in LTS; all convenience parameters are converted into keywords and no parsed-field filtering is applied.

### Audit Type Presets

| `audit_type` | Keywords added | Use case |
|---------------|----------------|----------|
| `pod_delete` | `delete`, `pods` | Find Pod deletion events |
| `workload_change` | Workload-related keywords | Find Deployment/StatefulSet changes |

### Required vs Auto-Discovered Parameters

- Prefer explicit `log_group_id` and `log_stream_id` when known
- If omitted, the audit tool attempts to discover LTS streams by names containing audit/apiserver terms

### Example: Pod Deletion Audit

```bash
python3 scripts/huawei-cloud.py huawei_query_cce_audit_logs \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  audit_type=pod_delete \
  namespace=default \
  hours=6 \
  log_group_id=<audit-lts-group-id> \
  log_stream_id=<audit-lts-stream-id>
```

### Example: Workload Change Audit

```bash
python3 scripts/huawei-cloud.py huawei_query_cce_audit_logs \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  audit_type=workload_change \
  namespace=default \
  start_time="2026-05-30 10:00:00" \
  end_time="2026-05-30 11:00:00"
```

### Additional Audit Filter Parameters

All of these are converted into LTS keyword search terms, not structured filters:

| Parameter | Converted to keyword |
|-----------|---------------------|
| `pod_name` | Pod name in audit content |
| `resource_name` | Resource name in audit content |
| `workload_name` | Workload name in audit content |
| `namespace` | Namespace in audit content |
| `user` | User/actor in audit content |
| `verb` | Operation verb (create, delete, update, etc.) |
| `resource` | Resource type (pods, deployments, etc.) |
| `status_code` | Response status code in audit content |

## Analysis Strategy

- Start with the narrowest useful scope: Pod stdout first when the user names a Pod, application LTS logs when they name a workload
- Prefer recent windows (`hours=1`, `tail_lines=100-500`) before broad historical searches
- For workload-level LTS queries, always discover LogConfig policies first via `huawei_get_application_logconfigs`
- When summarizing logs, group repeated lines by pattern and include counts when possible
- Redact tokens, passwords, cookies, authorization headers, and personally identifiable data
- If logs point to specific failures, recommend the corresponding diagnosis skill with exact evidence
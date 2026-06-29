---
name: huawei-cloud-cce-log-analyzer
description: >-
  Use when querying or analyzing Kubernetes Pod stdout/stderr logs, CCE LogConfig-collected application logs, Huawei Cloud LTS log streams, CCE audit logs for Pod deletion or workload change events, or when creating/deleting CCE LogConfig collection rules with preview confirmation. Covers Pod log retrieval, LogConfig discovery, LTS group/stream mapping, keyword search, time-range queries, abnormality analysis with error ratios and incident windows, and audit event summarization.
  Trigger: log analysis, 日志分析, CCE logs, CCE 日志, LTS query, LTS 查询, application log, 应用日志, container log, 容器日志, log search, 日志搜索, Pod stdout, Pod 日志, LogConfig, audit log, 审计日志, abnormal log, 异常日志
tags: [cce, logs, lts, analysis]
---

# Huawei Cloud CCE Log Analyzer

## Overview

Query and analyze Kubernetes Pod stdout logs, CCE LogConfig-collected application logs, and Huawei Cloud LTS log streams for CCE workloads.

**Architecture**: scripts/huawei-cloud.py dispatcher → cce.py (Pod stdout) / cce_app_logs.py (LogConfig discovery & app log stream matching) / lts.py (LTS group/stream/query) → K8s API / CCE OpenAPI / LTS API

**Related Skills**:
- `huawei-cloud-cce-pod-failure-diagnoser` - Pod startup, scheduling, crash-loop diagnosis
- `huawei-cloud-cce-workload-failure-diagnoser` - Deployment/StatefulSet rollout issues
- `huawei-cloud-cce-node-failure-diagnoser` - Node NotReady, disk pressure, network issues
- `huawei-cloud-cce-kubernetes-event-analyzer` - Kubernetes Warning events and patterns

**Capabilities**:
- Query Kubernetes Pod stdout/stderr and previous container logs
- List, create, and delete CCE LogConfig collection rules
- Discover application LogConfig policies and map to LTS log groups/streams
- Query CCE Kubernetes audit logs for Pod deletion and workload change events
- Query application logs from LTS by time range, keywords, or recent hours
- Analyze application logs for abnormal keywords, HTTP errors, incident windows, recovery time, and abnormal ratios

**Typical Use Cases**:

- "Check my Pod logs for crash errors"
- "Find the LTS stream for my application"
- "Query recent application logs for ERROR keywords"
- "Analyze logs in the last hour for abnormalities"
- "Who deleted this Pod? Check audit logs"
- "Create a LogConfig to collect my workload stdout"
- "Remove this LogConfig collection rule"
- "Query container file logs from /var/log/*.log"

## Prerequisites

### 1. Python Runtime

- Python 3.8+ installed
- Run `python3 --version` to verify

### 2. Huawei Cloud Credentials

- Valid Huawei Cloud credentials (AK/SK mode)
- **Security Rules**:
  - 🚫 Never expose AK/SK values in code, conversation, or output
  - 🚫 Never use `echo $HUAWEI_CLOUD_AK` or `echo $HUAWEI_CLOUD_SK` to check credentials
  - ✅ Use environment variables: `HUAWEI_CLOUD_AK`, `HUAWEI_CLOUD_SK`, `HUAWEI_CLOUD_REGION`
  - ✅ Prefer IAM users over root account for cloud operations

**Configuration Method** (Environment Variables):

```bash
export HUAWEI_CLOUD_AK=<your-ak>
export HUAWEI_CLOUD_SK=<your-sk>
export HUAWEI_CLOUD_REGION=cn-north-4
```

### 3. IAM Permission Requirements

| API Action | Permission | Purpose |
|------------|------------|---------|
| `cce:cluster:get` | Get cluster | View cluster details |
| `cce:logConfig:list` | List LogConfig | Query LogConfig collection rules |
| `cce:logConfig:create` | Create LogConfig | Create log collection rules |
| `cce:logConfig:delete` | Delete LogConfig | Remove log collection rules |
| `lts:logs:list` | List LTS logs | Query log streams and log records |
| `lts:groups:list` | List LTS groups | Query log group information |

## Security Constraints

### Dangerous Operation Confirmation Mechanism

> **This skill enforces a preview-then-confirm mechanism for all mutating operations.**

| Operation | Risk Level | Description |
|-----------|------------|-------------|
| `huawei_create_cce_logconfig` | 🟡 Medium | Creates a LogConfig collection rule; preview by default, create with `confirm=true` |
| `huawei_delete_cce_logconfig` | 🟠 High | Deletes a LogConfig collection rule; preview by default, delete with `confirm=true` |

**Process**: Call without `confirm=true` → inspect preview output → user confirms → call with `confirm=true`

### Credential & Data Security

- **Never expose** AK/SK, tokens, kubeconfig certificates, or full sensitive log payloads in summaries
- **Redact** tokens, passwords, cookies, authorization headers, and personally identifiable data from log output
- **Prefer time-bounded queries** — if no time range provided, use recent logs with small limits

### Scope Boundaries

- This skill is **read-only by default** for log queries and LogConfig inspection
- Creating/deleting LogConfig is allowed **only** through the dedicated tools with `confirm=true`
- **Do not** modify workloads, LTS groups/streams, or other cloud resources
- If logs indicate failures, **hand off** to the relevant diagnosis skill with evidence, do not remediate here

## Scenario Routing

| User Intent | Tool(s) | Reference Document |
|-------------|----------|-------------------|
| Query Pod stdout/stderr logs | `huawei_get_pod_logs` | [references/workflow.md](references/workflow.md) |
| Query previous terminated container logs | `huawei_get_pod_logs` (previous=true) | [references/workflow.md](references/workflow.md) |
| List cluster LogConfig rules | `huawei_get_cce_logconfigs` | [references/workflow.md](references/workflow.md) |
| Create LogConfig for stdout/file collection | `huawei_create_cce_logconfig` | [references/workflow.md](references/workflow.md) |
| Delete a LogConfig rule | `huawei_delete_cce_logconfig` | [references/workflow.md](references/workflow.md) |
| Discover app LTS stream mapping | `huawei_get_application_logconfigs` | [references/workflow.md](references/workflow.md) |
| Query audit logs for Pod deletion | `huawei_query_cce_audit_logs` | [references/workflow.md](references/workflow.md) |
| Query audit logs for workload changes | `huawei_query_cce_audit_logs` | [references/workflow.md](references/workflow.md) |
| Query recent application logs | `huawei_query_application_recent_logs` | [references/workflow.md](references/workflow.md) |
| Query application logs in time window | `huawei_query_application_logs` | [references/workflow.md](references/workflow.md) |
| Analyze logs for abnormalities | `huawei_analyze_application_logs` | [references/workflow.md](references/workflow.md) |
| Risk constraints & guardrails | — | [references/risk-rules.md](references/risk-rules.md) |
| Output schema reference | — | [references/output-schema.md](references/output-schema.md) |

## Core Commands

### 1. Kubernetes Pod Stdout Logs

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
```

### 2. LogConfig Discovery & Management

```bash
# List all LogConfig resources in a cluster
python3 scripts/huawei-cloud.py huawei_get_cce_logconfigs \
  region=cn-north-4 \
  cluster_id=<cluster-id>

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
# Then call again with confirm=true after user confirms

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
# Then call again with confirm=true after user confirms

# Preview then delete a LogConfig
python3 scripts/huawei-cloud.py huawei_delete_cce_logconfig \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  logconfig_name=<policy-name> \
  logconfig_namespace=kube-system
# Then call again with confirm=true after user confirms
```

### 3. CCE Audit Logs

```bash
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
```

### 4. Application Log Query & Analysis

```bash
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

## Parameter Reference

### Common Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `region` | Yes | Huawei Cloud region ID | `cn-north-4` |
| `cluster_id` | Yes | CCE cluster ID | — |
| `namespace` | Most tools | Kubernetes namespace | `default` |

### Pod Log Parameters

| Parameter | Tool | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| `pod_name` | `huawei_get_pod_logs` | Yes | Pod name | Must reference existing Pod |
| `container` | `huawei_get_pod_logs` | No | Container name | Required for multi-container Pods |
| `previous` | `huawei_get_pod_logs` | No | Previous terminated container | `true`/`false` |
| `tail_lines` | `huawei_get_pod_logs` | No | Number of recent lines | Recommended 100-500 |

### LogConfig Parameters

| Parameter | Tool | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| `logconfig_name` | create/delete | Yes | LogConfig policy name | Unique within namespace |
| `source_type` | create | Yes | Collection source type | `container_stdout` or `container_file` |
| `workload_name` | create | Yes | Target workload name | Must reference existing workload |
| `workload_kind` | create | Yes | Workload type | `Deployment`, `StatefulSet`, `DaemonSet` |
| `workload_namespace` | create | Yes | Workload namespace | — |
| `container` | create (file) | No | Container name | Required for container_file |
| `log_path` | create (file) | No | Log file directory path | Required when source_type=container_file |
| `file_pattern` | create (file) | No | File name pattern | e.g. `*.log` |
| `log_group_id` | create | Yes | LTS log group ID | Must reference existing LTS group |
| `log_stream_id` | create | Yes | LTS log stream ID | Must reference existing LTS stream |
| `confirm` | create/delete | No | Execute confirmation | Preview without it; `true` to execute |
| `logconfig_namespace` | delete | Yes | LogConfig namespace | — |

### Audit Log Parameters

| Parameter | Tool | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| `audit_type` | `huawei_query_cce_audit_logs` | No | Keyword preset | `pod_delete` or `workload_change` |
| `hours` | audit | No | Recent hours window | Used when no start_time/end_time |
| `start_time` | audit | No | Start time | `YYYY-MM-DD HH:MM:SS` format |
| `end_time` | audit | No | End time | `YYYY-MM-DD HH:MM:SS` format |
| `log_group_id` | audit | Recommended | Audit LTS group ID | Auto-discovered if omitted |
| `log_stream_id` | audit | Recommended | Audit LTS stream ID | Auto-discovered if omitted |

### Application Log Parameters

| Parameter | Tool | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| `app_name` | app log tools | Yes | Workload name | Must reference existing workload |
| `logconfig_name` | app log tools | No | Specific LogConfig policy | Selects from matched streams |
| `policy_name` | app log tools | No | Specific policy name | Alternative to logconfig_name |
| `keywords` | app log tools | No | Keyword filter | LTS keyword search |
| `hours` | recent logs | No | Recent hours window | Default 1 |
| `start_time` | time-range logs | No | Start time | `YYYY-MM-DD HH:MM:SS` format |
| `end_time` | time-range logs | No | End time | `YYYY-MM-DD HH:MM:SS` format |
| `auto_paginate` | app log tools | No | Enable pagination | `true`/`false` |
| `max_pages` | app log tools | No | Max pages to fetch | Caps total work when paginating |
| `limit` | app log tools | No | Per-page size | Recommended 100-1000 |

## Common Region IDs

| Region Name | Region ID |
|-------------|-----------|
| North China - Beijing 4 | `cn-north-4` |
| North China - Beijing 1 | `cn-north-1` |
| East China - Shanghai 1 | `cn-east-3` |
| East China - Shanghai 2 | `cn-east-2` |
| South China - Guangzhou | `cn-south-1` |
| South China - Shenzhen | `cn-south-4` |
| Southwest China - Guiyang 1 | `cn-southwest-2` |
| Asia Pacific - Bangkok | `ap-southeast-2` |
| Asia Pacific - Singapore | `ap-southeast-1` |
| Asia Pacific - Hong Kong | `ap-southeast-3` |
| Europe - Paris | `eu-west-0` |

## Best Practices

1. **Narrowest scope first** — use Pod stdout when the user names a Pod, application LTS logs when they name a workload
2. **Recent windows before broad searches** — prefer `hours=1` or `tail_lines=100-500` before full historical queries
3. **Discover before querying** — call `huawei_get_application_logconfigs` first to find the right LogConfig policy, then pass `logconfig_name` or `policy_name` to query tools
4. **Preview before mutating** — always call create/delete LogConfig without `confirm=true` first; only call with `confirm=true` after user reviews the preview
5. **Use auto_paginate for multi-page results** — set `auto_paginate=true` with `max_pages` to cap total work; `limit` controls per-page size
6. **Redact sensitive data** — never include tokens, passwords, cookies, authorization headers, or PII in log summaries
7. **Group repeated patterns** — when summarizing logs, group repeated lines by pattern and include counts
8. **Hand off for remediation** — if logs indicate Pod startup, image pull, scheduling, node, or network failures, recommend the corresponding diagnosis skill with exact evidence

## Common Pitfalls

| Pitfall | Symptom | Quick Fix |
|---------|---------|-----------|
| Missing LogConfig for app | No LTS stream found | Create LogConfig with `huawei_create_cce_logconfig` |
| Wrong LogConfig policy | Logs from wrong stream | Use `huawei_get_application_logconfigs` to discover correct policy |
| keywords filter skews analysis ratios | Abnormal ratio too high/low | Do not set `keywords` unless user explicitly wants keyword-scoped ratios |
| Audit type misunderstood | Audit results too broad/narrow | `audit_type` is keyword preset only; `pod_delete` adds `delete+pods`, `workload_change` adds workload-related keywords |
| No confirm=true on create/delete | Preview-only, no actual change | Call again with `confirm=true` after reviewing preview |
| Large time window without pagination | Partial or slow results | Use `auto_paginate=true` with `max_pages` and reasonable `limit` |
| Previous container log not found | "previous" flag on running container | Use `previous=true` only when container has restarted; check Pod status first |
| AK/SK exposed in output | Credential leak | Redact all credentials; summarize patterns instead of raw values |

## Notes

- **LogConfig tools are the only mutation path** — creating and deleting LogConfig resources is only supported through `huawei_create_cce_logconfig` and `huawei_delete_cce_logconfig` with `confirm=true`
- **Audit logs are keyword-based** — `huawei_query_cce_audit_logs` uses pure keyword search over LTS audit content; all convenience parameters (`pod_name`, `resource_name`, `workload_name`, `namespace`, `user`, `verb`, `resource`, `status_code`) are converted into keywords, not parsed-field filters
- **stdout vs container_file** — use `source_type=container_stdout` for Pod standard output, `source_type=container_file` for application file logs collected from paths like `/var/log/*.log`
- **Analysis tool denominator** — `huawei_analyze_application_logs` calculates ratios over the queried log set; adding `keywords` changes the denominator to only matched logs, so avoid it unless explicitly requested
- **Analysis returns** — abnormal ratio, log rates, first/last abnormal time, observed recovery time, incident windows, top patterns, status-code distribution, and samples

## Output Format

All tools return JSON with structured log data, analysis results, or LogConfig previews. See [references/output-schema.md](references/output-schema.md) for detailed response schemas.

## Verification

1. Run environment check script
2. Query a known Pod log with huawei_get_recent_logs
3. Verify the LogConfig preview/confirm workflow
4. Confirm read-only behavior for query operations

## Reference Documents

| Document | Description |
|----------|-------------|
| [workflow.md](references/workflow.md) | Detailed workflow for Pod stdout, application LTS logs, LogConfig management, and audit queries |
| [risk-rules.md](references/risk-rules.md) | Risk constraints, security rules, and scope boundaries |
| [output-schema.md](references/output-schema.md) | Log query and analysis output schema reference |
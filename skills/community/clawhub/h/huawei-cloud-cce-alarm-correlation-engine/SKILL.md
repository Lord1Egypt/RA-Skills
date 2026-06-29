---
id: huawei-cloud-cce-alarm-correlation-engine
name: huawei-cloud-cce-alarm-correlation-engine
description: |
  Huawei Cloud AOM alarm correlation analysis skill for CCE operations.
  Use this skill when the user wants to: (1) query AOM active and historical alarms, (2) analyze alarm deduplication, severity grouping, and burst/steady alarm identification, (3) inspect CCE cluster alarm health, (4) manage AOM alarm rules (query, create, update, delete, enable, disable), (5) check AOM action rules and mute rules for notification gaps, (6) create event alarm rules referencing CCE event lists or Prometheus metric alarms.
  Trigger: user mentions "alarm correlation", "告警关联", "AOM alarm", "AOM 告警", "alarm deduplication", "告警去重", "alarm storm", "告警风暴", "alarm inspection", "告警巡检", "alarm rules", "告警规则"
tags: [cce, alarm-correlation, aom, observability, alarm-management]
---

# Huawei Cloud CCE Alarm Correlation Engine

> **⚠️ Execution Method (Must Read): This skill executes queries via the local Python dispatcher script. Using hcloud, openstack, or other CLI tools or direct API calls is prohibited.**
>
> - The dispatcher script is located at `scripts/huawei-cloud.py` within the skill directory
> - All scripts and environment check scripts are inside the skill package. **You must use `skill action=exec` to execute them. Do not run them directly in a shell.**
> - **Do not attempt hcloud, openstack, curl IAM, or any other CLI/API methods. This skill does not depend on those tools.**
> - **All paths are relative to the skill directory, which is the directory where this SKILL.md is located.**

## Overview

This skill correlates Huawei Cloud AOM active and historical alarms for CCE, transforming raw alarm event streams into actionable alarm leads. The core principle is to consider both active and history alarms, avoiding omission of resource-type alarms that have already recovered but still impact diagnosis.

This skill has **both read-only tools** (alarm query, analysis, inspection, rule query) and **mutation tools** (alarm rule create/update/delete, action rule delete). All mutation operations require a two-step confirmation workflow with `confirm=true`.

### Related Skills

| Skill | Purpose |
|-------|---------|
| `huawei-cloud-cce-pod-failure-diagnoser` | Pod-level failure diagnosis (CrashLoopBackOff, ImagePullBackOff, etc.) |
| `huawei-cloud-cce-node-failure-diagnoser` | Node failure diagnosis (NotReady, resource pressure, NPD events) |
| `huawei-cloud-cce-network-failure-diagnoser` | Network failure diagnosis (Ingress 502/504, ELB anomalies) |
| `huawei-cloud-cce-auto-remediation-runner` | Execute remediation actions (scale, reboot, drain) |
| `huawei-cloud-cce-root-cause-analyzer` | Multi-category alarm root cause analysis |
| `huawei-cloud-cce-observability-context-builder` | Observability context enrichment |

### Capabilities

1. Query active + history alarms merged and deduplicated (`huawei_list_aom_alarms`)
2. Query current active alarms only (`huawei_list_aom_current_alarms`)
3. Analyze alarms: deduplication, severity grouping, burst/steady identification (`huawei_analyze_aom_alarms`)
4. Query, create, update, delete, enable, disable AOM alarm rules (mutation requires `confirm=true`)
5. Create AOM event alarm rules referencing CCE event list (`huawei_create_aom_event_alarm_rule`)
6. Query and delete AOM action/notification rules (delete requires `confirm=true`)
7. Query AOM mute rules (`huawei_list_aom_mute_rules`)
8. CCE cluster alarm inspection with risk summary (`huawei_aom_alarm_inspection`)

### Typical Use Cases

- Query all alarms (active + history) for a CCE cluster and group by severity
- Reduce alarm storm noise by deduplicating and classifying burst vs. steady alarms
- Inspect a CCE cluster for alarm health risks
- Create, update, or delete AOM alarm rules with preview + confirmation workflow
- Check whether alarms are suppressed by action rules or mute rules causing notification gaps
- Create event alarm rules for CCE workload, node, network, storage, or autoscaling events

---

## Prerequisites

### Python Dependencies

The dispatcher script requires Python >= 3.6 and the following packages:

- `huaweicloudsdkcore`
- `huaweicloudsdkaom`
- `huaweicloudsdkiam`

### Credential Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| HUAWEI_AK | Yes | Huawei Cloud Access Key |
| HUAWEI_SK | Yes | Huawei Cloud Secret Key |
| HUAWEI_REGION | No | Default region (overrides `region` param if set) |
| HUAWEI_PROJECT_ID | No | Project ID (auto-obtained via IAM API when not set) |
| HUAWEI_SECURITY_TOKEN | No | Required when using temporary AK/SK |

🚫 **Never expose or log AK/SK values.** Credentials exist only in the current request call stack and are released after each invocation. Do not write credentials to files, logs, or responses.

✅ **Use environment variables** `HUAWEI_AK` / `HUAWEI_SK` for authentication. The dispatcher reads them automatically.

**Security rules for credentials:**

1. **No persistent storage** — never write AK/SK, tokens, or certificates to disk files
2. **No long-term memory cache** — AK/SK exists only during the current API call and is released afterward
3. **Project ID memory cache only** — only non-sensitive project IDs may be cached in process memory (never written to disk)
4. **No log leakage** — never include AK/SK in logs, response output, or error messages
5. **Output desensitization** — output only alarm, resource, and rule information; never expose authentication credentials

AK/SK may be provided in two ways:
- Via environment variables `HUAWEI_AK` / `HUAWEI_SK` (recommended)
- Via per-call parameters `ak` and `sk` (not recommended for production)

### IAM Permissions

| Permission | Description |
|------------|-------------|
| `aom:event:list` | Query AOM alarm events |
| `aom:alarmRule:list` | Query AOM alarm rules |
| `aom:alarmRule:create` | Create AOM alarm rules |
| `aom:alarmRule:update` | Update AOM alarm rules |
| `aom:alarmRule:delete` | Delete AOM alarm rules |
| `aom:actionRule:list` | Query AOM action rules |
| `aom:muteRule:list` | Query AOM mute rules |
| `cce:cluster:list` | Get cluster name and auxiliary filter info via cluster ID |

---

## Core Tools

All actions are invoked via the dispatcher script:

```bash
python3 scripts/huawei-cloud.py <action> region=<region> [key=value ...]
```

### Two-Step Confirmation Workflow for Mutation Operations

> **Mutation operations (create, update, delete, enable, disable alarm rules; delete action rules) require `confirm=true` to execute. Without `confirm`, the tool returns a preview and confirmation prompt only.**

**Step 1: Preview** — call without `confirm`:
```bash
python3 scripts/huawei-cloud.py huawei_create_aom_alarm_rule \
  region=cn-north-4 rule_name=my-rule metric_name=cpuUsage \
  namespace=PAAS.NODE comparison_operator='>' threshold=80 \
  period=60 evaluation_periods=3 statistic=average alarm_level=2
```

Returns: operation preview, target rule, rule fields, and confirmation example. No real creation is performed.

**Step 2: Confirm execution** — call again with `confirm=true`:
```bash
python3 scripts/huawei-cloud.py huawei_create_aom_alarm_rule \
  region=cn-north-4 rule_name=my-rule metric_name=cpuUsage \
  namespace=PAAS.NODE comparison_operator='>' threshold=80 \
  period=60 evaluation_periods=3 statistic=average alarm_level=2 \
  confirm=true
```

#### Operations Requiring Confirmation

| Tool | Operation | Risk Level | Description |
|------|-----------|-----------|-------------|
| `huawei_create_aom_alarm_rule` | Create | 🟡 Medium | Create new AOM alarm rule, may introduce new alarm notifications |
| `huawei_create_aom_event_alarm_rule` | Create | 🟡 Medium | Create AOM event alarm rule, may introduce new event notifications |
| `huawei_update_aom_alarm_rule` | Update | 🟠 High | Update AOM alarm rule threshold, toggle, notification action, description, etc. |
| `huawei_delete_aom_alarm_rule` | Delete | 🔴 High | Delete AOM alarm rule, may prevent future alarms from triggering |
| `huawei_disable_aom_alarm_rule` | Disable | 🔴 High | Disable AOM alarm rule, may stop related alarms from triggering |
| `huawei_enable_aom_alarm_rule` | Enable | 🟠 High | Enable AOM alarm rule, may restore and trigger alarm notifications |
| `huawei_delete_aom_action_rule` | Delete | 🔴 High | Delete AOM notification action rule, may prevent alarm notifications |

#### Prohibited Actions

| Action | Description |
|--------|-------------|
| Create/update action rules | Do not create or update notification action rules |
| Modify mute rules | Do not create, update, or delete mute rules |
| Execute remediation actions | Do not scale, reboot, drain, or delete workloads or nodes |
| Modify cluster resources | Do not change CCE, ECS, ELB, EIP, VPC, security groups, etc. |

If analysis results require scaling, rebooting, draining, vulnerability status changes, or other remediation actions, output recommendations only and hand off to `huawei-cloud-cce-auto-remediation-runner` for preview, confirmation, and post-verification.

### Alarm Query and Correlation (Read-Only)

| Action | Description | Cluster Filter | Required Params |
|--------|-------------|---------------|-----------------|
| `huawei_list_aom_alarms` | Query active + history alarms, merged and deduplicated | Supports `cluster_id` | `region` |
| `huawei_list_aom_current_alarms` | Query current active alarms only | Supports `cluster_id` | `region` |
| `huawei_analyze_aom_alarms` | Analyze alarms: deduplication, severity grouping, burst/steady identification | Supports `cluster_id` | `region` |

```bash
# Query active + history alarms in a region
python3 scripts/huawei-cloud.py huawei_list_aom_alarms region=cn-north-4

# Query alarms for a specific cluster
python3 scripts/huawei-cloud.py huawei_list_aom_alarms \
  region=cn-north-4 cluster_id=xxx

# Query current active alarms for a cluster
python3 scripts/huawei-cloud.py huawei_list_aom_current_alarms \
  region=cn-north-4 cluster_id=xxx

# Analyze alarms for a cluster (burst, attention, steady groups)
python3 scripts/huawei-cloud.py huawei_analyze_aom_alarms \
  region=cn-north-4 cluster_id=xxx
```

### Alarm Rule Management (Mutation Requires `confirm=true`)

**Event alarm rule constraints:**
- When creating event alarm rules via `huawei_create_aom_event_alarm_rule`, the `event_name` must reference the event list and naming format in `references/cce-event-list.md` (recommended format: `Chinese event description##Event name`).
- Event alarm rules are created with alarm noise reduction enabled by default (`route_group_enable=true`).

**Metric alarm rule constraints:**
- When creating metric alarm rules via `huawei_create_aom_alarm_rule`, PromQL/metric thresholds should reference `references/cce-prometheus-metric-alarms.md`.

| Action | Description | Risk Level | Requires `confirm` | Required Params |
|--------|-------------|-----------|--------------------|-----------------|
| `huawei_list_aom_alarm_rules` | Query AOM alarm rules | 🟢 Low | No | `region` |
| `huawei_create_aom_alarm_rule` | Create AOM metric alarm rule | 🟡 Medium | **Yes** | `region`, `rule_name`, `metric_name`, `namespace`, `comparison_operator`, `threshold`, `period`, `evaluation_periods`, `statistic`, `alarm_level` |
| `huawei_create_aom_event_alarm_rule` | Create AOM event alarm rule | 🟡 Medium | **Yes** | `region`, `rule_name`, `event_name`, `namespace` |
| `huawei_update_aom_alarm_rule` | Update AOM alarm rule | 🟠 High | **Yes** | `region`, `rule_name` |
| `huawei_delete_aom_alarm_rule` | Delete AOM alarm rule | 🔴 High | **Yes** | `region`, `rule_name` |
| `huawei_disable_aom_alarm_rule` | Disable AOM alarm rule | 🔴 High | **Yes** | `region`, `rule_id` |
| `huawei_enable_aom_alarm_rule` | Enable AOM alarm rule | 🟠 High | **Yes** | `region`, `rule_id` |
| `huawei_list_aom_action_rules` | Query AOM action/notification rules | 🟢 Low | No | `region` |
| `huawei_delete_aom_action_rule` | Delete AOM notification action rule | 🔴 High | **Yes** | `region`, `rule_name` |
| `huawei_list_aom_mute_rules` | Query AOM mute rules | 🟢 Low | No | `region` |

```bash
# Query alarm rules
python3 scripts/huawei-cloud.py huawei_list_aom_alarm_rules region=cn-north-4

# Preview create alarm rule (no execution)
python3 scripts/huawei-cloud.py huawei_create_aom_alarm_rule \
  region=cn-north-4 rule_name=my-rule metric_name=cpuUsage \
  namespace=PAAS.NODE comparison_operator='>' threshold=80 \
  period=60 evaluation_periods=3 statistic=average alarm_level=2

# Confirm create alarm rule
python3 scripts/huawei-cloud.py huawei_create_aom_alarm_rule \
  region=cn-north-4 rule_name=my-rule metric_name=cpuUsage \
  namespace=PAAS.NODE comparison_operator='>' threshold=80 \
  period=60 evaluation_periods=3 statistic=average alarm_level=2 \
  confirm=true

# Preview update alarm rule
python3 scripts/huawei-cloud.py huawei_update_aom_alarm_rule \
  region=cn-north-4 rule_name=my-rule threshold=80

# Confirm update alarm rule
python3 scripts/huawei-cloud.py huawei_update_aom_alarm_rule \
  region=cn-north-4 rule_name=my-rule threshold=80 confirm=true

# Preview delete alarm rule
python3 scripts/huawei-cloud.py huawei_delete_aom_alarm_rule \
  region=cn-north-4 rule_name=xxx

# Confirm delete alarm rule
python3 scripts/huawei-cloud.py huawei_delete_aom_alarm_rule \
  region=cn-north-4 rule_name=xxx confirm=true

# Preview disable alarm rule
python3 scripts/huawei-cloud.py huawei_disable_aom_alarm_rule \
  region=cn-north-4 rule_id=xxx

# Confirm disable alarm rule
python3 scripts/huawei-cloud.py huawei_disable_aom_alarm_rule \
  region=cn-north-4 rule_id=xxx confirm=true

# Preview enable alarm rule
python3 scripts/huawei-cloud.py huawei_enable_aom_alarm_rule \
  region=cn-north-4 rule_id=xxx

# Confirm enable alarm rule
python3 scripts/huawei-cloud.py huawei_enable_aom_alarm_rule \
  region=cn-north-4 rule_id=xxx confirm=true

# Query action rules
python3 scripts/huawei-cloud.py huawei_list_aom_action_rules region=cn-north-4

# Preview delete action rule
python3 scripts/huawei-cloud.py huawei_delete_aom_action_rule \
  region=cn-north-4 rule_name=xxx

# Confirm delete action rule
python3 scripts/huawei-cloud.py huawei_delete_aom_action_rule \
  region=cn-north-4 rule_name=xxx confirm=true

# Query mute rules
python3 scripts/huawei-cloud.py huawei_list_aom_mute_rules region=cn-north-4
```

### Cluster Alarm Inspection (Read-Only)

| Action | Description | Required Params |
|--------|-------------|-----------------|
| `huawei_aom_alarm_inspection` | Inspect AOM alarms for a CCE cluster and output risk items | `region`, `cluster_id` |

```bash
# Inspect alarms for a specific cluster
python3 scripts/huawei-cloud.py huawei_aom_alarm_inspection \
  region=cn-north-4 cluster_id=xxx
```

---

## Parameter Reference

### Alarm Query Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `region` | Yes | Huawei Cloud region (e.g., `cn-north-4`) |
| `cluster_id` | No | CCE cluster ID; when provided, only alarms related to this cluster are returned |
| `ak` | No | Access Key ID; `HUAWEI_AK` environment variable preferred |
| `sk` | No | Secret Access Key; `HUAWEI_SK` environment variable preferred |
| `project_id` | No | Huawei Cloud project ID; auto-obtained via IAM API when not provided |

### Alarm Rule Mutation Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `region` | Yes | Huawei Cloud region |
| `rule_name` | Yes (create, update, delete) | Alarm rule name |
| `rule_id` | Yes (enable, disable) | Alarm rule ID |
| `metric_name` | Yes (create metric rule) | Metric name (e.g., `cpuUsage`) |
| `namespace` | Yes (create) | Metric namespace (e.g., `PAAS.NODE`) |
| `event_name` | Yes (create event rule) | Event name; reference `references/cce-event-list.md` for naming format |
| `comparison_operator` | Yes (create metric rule) | Threshold comparison operator (e.g., `>`, `<`, `>=`, `<=`) |
| `threshold` | Yes (create metric rule) | Alarm threshold value |
| `period` | Yes (create metric rule) | Statistics period in seconds (recommended: 60) |
| `evaluation_periods` | Yes (create metric rule) | Consecutive trigger period count (recommended: 3) |
| `statistic` | Yes (create metric rule) | Statistics method (e.g., `average`, `max`, `min`) |
| `alarm_level` | Yes (create) | Alarm severity level (1=Critical, 2=Major, 3=Minor, 4=Info) |
| `fields` | No (create) | Additional JSON fields for rule creation, e.g., `{"unit":"%","is_turn_on":true}` |
| `updates` | No (update) | JSON batch update fields, e.g., `{"threshold":"80","is_turn_on":true}` |
| `enterprise_project_id` | No (list action rules) | Enterprise project scope; default `all_granted_eps` |
| `confirm` | No | Must be explicitly set to `true` for mutation operations to execute |
| `ak` | No | Access Key ID |
| `sk` | No | Secret Access Key |
| `project_id` | No | Huawei Cloud project ID |

---

## Output Format

### Alarm Summary

Output must include:

| Field | Description |
|-------|-------------|
| `region` | Queried region |
| `cluster_id` | Cluster ID (if specified by user) |
| `total_count` | Total alarm count |
| `firing_count` | Currently firing alarm count |
| `resolved_count` | Resolved alarm count |
| `severity_stats` | Severity level distribution |
| `type_stats` | Alarm type grouping statistics |

### Resource Clues

For CCE alarms, prioritize the following resource dimensions:

| Field | Description |
|-------|-------------|
| `cluster_name` | Cluster name |
| `namespace` | Kubernetes namespace |
| `pod_name` | Pod name |
| `resource_kind` | Resource type |
| `event_name` | Alarm name |
| `message` | Alarm message |

### Recommended Diagnosis Skills

| Alarm Characteristics | Recommended Skill |
|----------------------|-------------------|
| `CrashLoopBackOff`, `BackOffStart`, `FailedStart`, `ImagePullBackOff` | `huawei-cloud-cce-pod-failure-diagnoser` |
| `FailedScheduling`, `Insufficient cpu`, `Insufficient memory` | `huawei-cloud-cce-pod-failure-diagnoser` or `huawei-cloud-cce-node-failure-diagnoser` |
| `NodeNotReady`, node resource pressure, NPD events | `huawei-cloud-cce-node-failure-diagnoser` |
| Ingress 502/504, Service unreachable, ELB anomalies | `huawei-cloud-cce-network-failure-diagnoser` |
| Multiple alarm categories impacting business simultaneously | `huawei-cloud-cce-root-cause-analyzer` |
| Scaling, reboot, drain, or other remediation actions needed | `huawei-cloud-cce-auto-remediation-runner` |

See `references/output-schema.md` for the full JSON response schema.

---

## Verification

1. Run the dispatcher with a known region and cluster to confirm connectivity:
   ```bash
   python3 scripts/huawei-cloud.py huawei_list_aom_alarms region=cn-north-4 cluster_id=<cluster_id>
   ```
2. Execute `huawei_analyze_aom_alarms` and verify that burst, attention, and steady groupings are returned correctly
3. Verify `huawei_aom_alarm_inspection` returns cluster alarm summary with risk items
4. Test mutation preview workflow: call `huawei_create_aom_alarm_rule` without `confirm` and verify it returns a preview only (no actual creation)
5. After a mutation operation with `confirm=true`, call `huawei_list_aom_alarm_rules` to verify the rule state change

---

## Best Practices

1. Always query both active and history alarms via `huawei_list_aom_alarms`; never assume absence of active alarms means no problems — check history alarms
2. Use `huawei_analyze_aom_alarms` for alarm storm scenarios to deduplicate and identify burst vs. steady alarms
3. For mutation operations, always follow the two-step workflow: preview first (without `confirm`), then confirm (with `confirm=true`) only after explicit user approval
4. After creating event alarm rules, verify that `event_name` follows the format in `references/cce-event-list.md`
5. When checking notification gaps, query both action rules (`huawei_list_aom_action_rules`) and mute rules (`huawei_list_aom_mute_rules`)
6. Do not interpret absence of active alarms as "no problem"; always cross-reference history alarms
7. When creating metric alarm rules, reference `references/cce-prometheus-metric-alarms.md` for recommended PromQL expressions and thresholds

---

## Reference Documents

| Document | Description |
|----------|-------------|
| `references/workflow.md` | Alarm correlation workflow: collection, deduplication, grouping, and diagnosis handoff |
| `references/output-schema.md` | Output JSON schema for alarm correlation and inspection results |
| `references/risk-rules.md` | Risk boundary rules: read-only vs. mutation actions, prohibited operations |
| `references/cce-event-list.md` | CCE event list with naming format for creating event alarm rules |
| `references/cce-prometheus-metric-alarms.md` | Prometheus metric alarm reference for creating metric alarm rules |
| [Huawei Cloud Python SDK Documentation](https://doc.huihua.com/api/sdk/python.html) | SDK reference |
| [Huawei Cloud API Explorer](https://support.huaweicloud.com/apiexplorer/index.html) | API interactive explorer |

---

## Notes

1. This skill has **both read-only and mutation tools** — mutation operations (create, update, delete, enable, disable alarm rules; delete action rules) require `confirm=true` two-step confirmation
2. Never create, update, or delete action rules or mute rules — only query and delete action rules with confirmation
3. If remediation actions are needed (scale, reboot, drain), output recommendations only and hand off to `huawei-cloud-cce-auto-remediation-runner`
4. Never expose or log AK/SK or environment variable values
5. All actions are executed via `python3 scripts/huawei-cloud.py <action>`; do not use hcloud CLI or direct API calls
6. Do not interpret absence of active alarms as "no problem" — always verify with history alarms

---

## Common Pitfalls

| Pitfall | Correct Approach |
|---------|-----------------|
| Only querying active alarms and ignoring history | Always use `huawei_list_aom_alarms` which merges active + history; history alarms may indicate recurring resource issues |
| Calling mutation tools without preview step | Always call without `confirm` first to preview; only add `confirm=true` after explicit user approval |
| Creating event alarm rules with incorrect `event_name` format | Reference `references/cce-event-list.md` and use `Chinese description##EventName` format |
| Creating metric alarm rules with arbitrary thresholds | Reference `references/cce-prometheus-metric-alarms.md` for recommended PromQL and threshold values |
| Deleting action rules without understanding notification impact | Preview first; verify which alarms depend on the action rule before confirming deletion |
| Executing remediation actions directly from this skill | This skill does not perform remediation; hand off to `huawei-cloud-cce-auto-remediation-runner` |
| Assuming "no active alarms" means "no problems" | Check history alarms — resolved alarms may indicate ongoing resource issues that flare periodically |
| Not checking mute rules when alarms are missing from notifications | Always query mute rules (`huawei_list_aom_mute_rules`) alongside action rules to identify suppression |
---
name: huawei-cloud-as-group-list
description: |
  1. Read-only inventory of Huawei Cloud Auto Scaling (AS / 弹性伸缩) resources in
     one region: scaling group name / ID / status, desired vs current instance
     number, min-max instance number, associated VPC / subnet / ELB, and the
     instance members inside a scaling group. Aimed at troubleshooting
     "scale-out did not take effect", "instance counts do not match", and
     "scaling group stuck in an abnormal state".
  2. Primary path: KooCLI call `AS ListScalingGroups` (read-only GET
     /autoscaling-api/v1/{project_id}/scaling_group) with `ListScalingInstances`
     (GET /autoscaling-api/v1/{project_id}/scaling_group_instance/
     {scaling_group_id}/list) for drill-down; automatic fallback to the
     official huaweicloudsdkas v1 SDK when hcloud is unavailable.
  3. Output modes: compact list (name / ID / status) by default, `--table`
     group view (11 columns) or, with `--group-id`, instance view (6 columns),
     and `--json` for the raw merged response.
  4. Abnormal groups (desired != current or status != INSERVICE) and abnormal
     instances (life-cycle != INSERVICE or health != NORMAL) are placed in a
     separate highlighted section at the top of `--table` output; `--status
     abnormal` lists only abnormal resources.
  5. Client-side filters: `--name` (exact, `--fuzzy` for substring),
     `--group-id`, `--status` (supports the abnormal alias), `--region`
     (default cn-north-4). `--limit` is 1-100 with automatic paging driven by
     total_number and the accumulated item count.
  6. Built-in write-intent guard: create / update / delete / enable / disable /
     batch-add / batch-remove / policy-execute / ... are rejected before any
     cloud call with exit code 1 — this skill never writes to AS.
  7. Explicit error hints for empty lists, 403 / insufficient IAM permission,
     missing credentials, missing hcloud, KooCLI [USE_ERROR], and a
     non-existent scaling group.
  8. Triggers include: "list AS scaling groups", "AS 伸缩组列表", "查询伸缩组",
     "弹性伸缩组", "伸缩组实例", "期望实例数与当前实例数不一致", "扩容没生效",
     "auto scaling inventory", "scaling group troubleshooting", "华为云弹性伸缩".
tags: [huawei-cloud, as, autoscaling, readonly, koo-cli]
---

# Huawei Cloud AS Scaling Group List

## Overview

Inventory Huawei Cloud Auto Scaling (AS) scaling groups and their instance
members through KooCLI, with an automatic SDK fallback. The skill answers the
everyday operations questions behind scaling incidents: is the group healthy,
does the desired instance number match the current number, which subnets and
load balancers is it attached to, and which instances are stuck in a non
INSERVICE life-cycle state.

| Operation | REST path | Method | Purpose |
| --------- | --------- | ------ | ------- |
| `AS ListScalingGroups` | `/autoscaling-api/v1/{project_id}/scaling_group` | GET | list scaling groups of the region |
| `AS ListScalingInstances` | `/autoscaling-api/v1/{project_id}/scaling_group_instance/{scaling_group_id}/list` | GET | list instances inside one scaling group |

Architecture:

```text
agent → python3 scripts/list_as_groups.py [--region=<region>] [--table|--json]
      → hcloud AS ListScalingGroups --cli-region=<region> --limit=<n> --start_number=<s>
        └─ (hcloud missing / transient failure) → huaweicloudsdkas v1 ListScalingGroups
      → Huawei Cloud AS OpenAPI → parsed JSON → compact list / table / JSON
      → --group-id → hcloud AS ListScalingInstances --scaling_group_id=<id>

(hcloud missing / transient failure, --group-id)
      → huaweicloudsdkas v1 ListScalingInstances → instance view
```

Key properties:

- **Read-only by design** — only `ListScalingGroups` and `ListScalingInstances`
  (both GET) are ever constructed. A write-intent guard scans the raw command
  line and rejects mutating intent before any network call.
- **CLI first, SDK fallback** — `hcloud` is the primary path; when it is
  missing or fails with a transient error the script falls back to the
  official `huaweicloudsdkas` v1 SDK. `403` / credential errors and a
  non-existent scaling group are reported as-is and never fall back.
- **Abnormal-first presentation** — `--table` renders abnormal groups and
  abnormal instances in a dedicated section above normal ones, with a `⚠`
  marker. The definition is explicit: a group is abnormal when the desired
  instance number differs from the current one or its status is not
  `INSERVICE`; an instance is abnormal when its life-cycle state is not
  `INSERVICE` or its health status is not `NORMAL`.
- **Complete inventory** — paging stops on the API `total_number`, the
  accumulated item count, a short page, or `--max-pages`, whichever comes
  first; duplicated IDs across pages are de-duplicated.
- **No files written** — everything goes to stdout; credentials are delegated
  to the KooCLI profile or the SDK environment variables.

**Dependency**: Quality telemetry is collected automatically via
skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkas` to enable the
   SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (the KooCLI configure init command in your own terminal, or credential environment
   variables). Never paste AK/SK into chat; the script never reads, echoes, or
   stores secrets itself.
3. **IAM permission** — read-only `as:scalingGroup:list` (alias
   `as:groups:list`) for groups and `as:scalingGroup:listInstances` (alias
   `as:instances:list`) for group members. Least-privilege policy:
   [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess).
5. **Outbound HTTPS** access to `*.myhuaweicloud.com`.
6. **`skill-quality-cli`** — ensured by `bash scripts/ensure_cli.sh` (idempotent,
   skips if present). Upgrade with `skill-quality-cli upgrade`; disable
   telemetry reporting with `SKILL_QUALITY_REPORT=0`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`); every AS call is
   region-scoped.
2. **Confirm hcloud readiness** (optional, read-only):
   `skill-quality-cli run --skill-name huawei-cloud-as-group-list -- hcloud configure list`.
3. **List scaling groups** and scan the abnormal section first when
   troubleshooting a scaling incident.
4. **Drill into one group** with `--group-id <id>` to inspect instance
   life-cycle states and health.
5. **Handle empty / error cases** per the Error Handling table below. When the
   group list is empty but the account should own groups, check the region and
   the IAM permission before assuming there is no resource.

## Core Commands

> **⚠️ Mandatory: every `hcloud` command in this skill MUST be wrapped with
> `skill-quality-cli run --skill-name huawei-cloud-as-group-list -- ` — bare
> `hcloud` calls are strictly forbidden.**

```bash
# Compact scaling-group list (default)
python3 scripts/list_as_groups.py --region cn-north-4

# Full group view: ID / name / status / desired / current / min-max /
# VPC / subnet / ELB / create time / region
python3 scripts/list_as_groups.py --table --region cn-north-4

# Only abnormal groups (desired != current or status != INSERVICE)
python3 scripts/list_as_groups.py --table --status abnormal

# Raw merged response JSON
python3 scripts/list_as_groups.py --json --region cn-north-4

# Filter by exact name / fuzzy name
python3 scripts/list_as_groups.py --name web-prod
python3 scripts/list_as_groups.py --name web --fuzzy

# Drill down into one group's instances (compact / table)
python3 scripts/list_as_groups.py --group-id <scaling_group_id>
python3 scripts/list_as_groups.py --group-id <scaling_group_id> --table

# Force the SDK fallback path
python3 scripts/list_as_groups.py --backend sdk --region cn-north-4
```

Equivalent direct KooCLI calls (the script wraps exactly these operations,
with paging) — illustrative, requires KooCLI installed:

```text
skill-quality-cli run --skill-name huawei-cloud-as-group-list -- hcloud AS ListScalingGroups --cli-region=cn-north-4 --limit=100 --start_number=0
skill-quality-cli run --skill-name huawei-cloud-as-group-list -- hcloud AS ListScalingInstances --cli-region=cn-north-4 --scaling_group_id=<scaling_group_id> --limit=100 --start_number=0
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--name` | No | Filter by scaling-group name (exact by default) | `web-prod` |
| `--fuzzy` | No | Make `--name` a substring match | — |
| `--group-id` | No | Drill down to the instances of one scaling group | `e5d27f5c-...` |
| `--status` | No | Client-side status filter; also `abnormal` for any abnormal resource | `ERROR`, `abnormal` |
| `--limit` | No | Page size, 1-100 (default 100) | `50` |
| `--table` | No | Full group view (11 columns) or instance view (6 columns) | — |
| `--json` | No | Output the raw merged response; client filters are not applied | — |
| `--backend` | No | `auto` (default) / `cli` / `sdk` | `sdk` |
| `--max-pages` | No | Safety cap for pagination (default 50) | `10` |
| `--timeout` | No | Per-call timeout in seconds (default 60) | `30` |
| `--action` | No | Only `list` (default); other values are rejected by the guard | `list` |
| `--operation` | No | Only `ListScalingGroups` / `ListScalingInstances` | `ListScalingGroups` |

Output-mode precedence: `--json` → `--table` → compact list (default). In every
mode the rendered result is printed to stdout; the script never writes a file.

## Write-Intent Guard

- The guard runs on the raw argv **before** argparse and before any cloud call.
- Mutating vocabulary is rejected both as a flag (`--delete-group`,
  `--batch-add`) and as a value of `--name`, `--group-id`, or `--status`
  (`--name create-me`), because the acceptance contract requires such input to
  be treated as a write intent.
- `--action` accepts only `list` / `ls` / `query` / `describe` / `show` /
  `inspect`; `--operation` accepts only `ListScalingGroups` /
  `ListScalingInstances`.
- A hit prints an explicit `只读查询…已被守卫拦截` message and exits with code 1.
- Only GET list operations are ever constructed by `build_group_args()` /
  `build_instance_args()`; there is no code path that can issue a mutating AS
  API call. Creating, updating, deleting, enabling, disabling, or executing a
  scaling policy requires a dedicated write-capable skill and explicit user
  confirmation; it is out of scope here.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `AS`.
- **Operation name** — PascalCase: `ListScalingGroups` / `ListScalingInstances`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete AS call).
- **Simple parameter** — `--key=value`, e.g. `--limit=100`,
  `--start_number=0`, `--scaling_group_name=web-prod`,
  `--scaling_group_id=<id>`.
- **REST paths (official SDK `_http_info`)** —
  `GET /autoscaling-api/v1/{project_id}/scaling_group` and
  `GET /autoscaling-api/v1/{project_id}/scaling_group_instance/{scaling_group_id}/list`;
  project_id is resolved by KooCLI from the credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty scaling-group list | Exit 0, prints `当前区域无伸缩组（区域: <x>）` plus next steps |
| Empty instance list for a valid group | Exit 0, prints `伸缩组 <id> 内无实例` plus next steps |
| 403 / insufficient IAM permission | Exit 1, explicit `as:scalingGroup:list` / `as:scalingGroup:listInstances` hint |
| Missing / invalid AK-SK | Exit 1, hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or the AS SDK |
| Scaling group not found / wrong region | Exit 1, `伸缩组不存在或不属于当前区域` with the `--group-id` / `--region` next step |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit KooCLI 参数错误 hint pointing to the `--help` of AS `ListScalingGroups` |
| Write intent detected | Exit 1, guard message, no command executed |
| `--limit` outside 1-100 / invalid `--status` | Exit 1 with the accepted range or value list |

Exit codes: `0` success / empty list; `1` config, auth, guard, parameter, or API
error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Group status `PAUSED` / `ERROR` / `DELETING` / `FREEZED` | Reported as-is and treated as abnormal (status != INSERVICE) |
| Desired instance number differs from current | Group is placed in the abnormal section with a `⚠` marker |
| Instance life-cycle `PENDING` / `REMOVING` / `STANDBY` | Instance is placed in the abnormal section |
| Instance health `ERROR` / `INITIALIZING` | Instance is placed in the abnormal section |
| `--status ERROR` | Matches group status, instance life-cycle, and instance health (client-side) |
| `--status abnormal` | Matches groups with desired != current or status != INSERVICE, and instances with life-cycle != INSERVICE or health != NORMAL |
| Large group / instance count | Automatic paging on `total_number` and accumulated count, capped by `--max-pages` |
| Duplicate items across pages | De-duplicated by group ID / instance ID |
| Missing VPC / subnet / ELB / create time | Rendered as `-` |
| `--json` combined with filters | Raw response is returned; client filters are intentionally not applied |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkas` v1, same output modes |
| User asks to create/delete/update/execute a policy | Out of scope — blocked by the guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess and a fake SDK client (no
credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: command construction (region / limit / start_number / name /
group ID), default compact list, both table views and their abnormal sections,
raw JSON, exact / fuzzy name filters, status filters and the abnormal alias,
group drill-down and its empty / invalid-ID paths, pagination (total,
start_number, short page, max-pages, de-duplication), error classification
(403, credentials, `[USE_ERROR]`, not found), SDK fallback and request fields,
KooCLI JSON parsing with trailing diagnostics, and the write-intent guard.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation, credential configuration, and SDK fallback |
| [references/verification-method.md](references/verification-method.md) | Offline tests, real read-only smoke, guard and boundary checks |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
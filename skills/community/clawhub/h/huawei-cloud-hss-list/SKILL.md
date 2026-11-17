---
name: huawei-cloud-hss-list
description: |
  1. List Huawei Cloud HSS (主机安全服务 / Host Security Service) protected
     servers in a tenant region through KooCLI (hcloud HSS ListHostStatus —
     read-only GET /v5/{project_id}/host-management/hosts), with an automatic
     fallback to the official `huaweicloudsdkhss` v5 SDK when hcloud is not
     installed.
  2. Outputs the full-field host protection table (default) with host name,
     private/public IP, OS, host status, Agent online/offline status, enabled
     HSS edition (基础版/专业版/企业版/旗舰版...), protection status
     (opened/closed), risk detection result, server group and enterprise
     project.
  3. Supports --region override and readable modes --json (raw response array)
     and --names-only (compact host-name list).
  4. Supports real server-side filters: --host-name / --host-id /
     --agent-status / --host-status / --protect-status / --os-type /
     --ip-addr / --version / --enterprise-project-id, plus automatic offset
     paging (limit 10–200).
  5. Explicit error hints for empty lists (「当前区域无已接入 HSS 的服务器」),
     403 / insufficient IAM permission (「无权限访问主机安全服务（HSS）」),
     missing or invalid AK/SK credentials, missing project_id on the SDK
     fallback, and hcloud not installed.
  6. Built-in write-intent guard: any mutating intent (create / delete /
     update / install agent / change / isolate...) or any operation other
     than ListHostStatus is rejected before execution — this skill is
     strictly read-only.
  7. Triggers include: "list HSS hosts", "HSS 主机列表", "主机防护列表",
     "查询 HSS", "主机安全", "Agent 状态", "防护状态", "hss host list",
     "已接入 HSS 的服务器", "华为云 HSS", "host security list",
     "list protected hosts", "quota 主机列表", "HSS 资产".
  8. Offline unit tests (mocked hcloud subprocess) cover output modes,
     filters, offset paging, error scenarios, SDK fallback, and the
     write-intent guard.
tags: [huawei-cloud, hss, security, readonly, koo-cli]
---

# Huawei Cloud HSS (主机安全服务) Protected-Host List

## Overview

Query the list of servers protected by the Huawei Cloud Host Security Service
(HSS / 主机安全服务) in a tenant region through KooCLI `hcloud HSS ListHostStatus`
(official read-only GET `/v5/{project_id}/host-management/hosts`, verified in
the `huaweicloudsdkhss` v5 client `_list_host_status_http_info` metadata). The
skill is aimed at HSS asset / protection inventory inspection, daily security
patrols, and as a pre-query step for other skills that need a host `host_id`,
its Agent status or the active HSS edition.

Architecture:

```text
agent → python3 scripts/list_hss.py --region=<region>
      → hcloud HSS ListHostStatus --cli-region=<region> --limit=<n> --offset=<o>
      → Huawei Cloud HSS OpenAPI (hss.<region>.myhuaweicloud.com) → parsed JSON → table / --json / --names-only

(hcloud binary missing) → fallback: huaweicloudsdkhss v5 HssClient.list_host_status
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListHostStatus`
  (a GET). A write-intent guard scans user arguments and validates the
  operation name; mutating intents (create / delete / update / install /
  uninstall / upgrade agent / ChangeEvent / isolate...) are rejected with an
  explicit message before a single command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  `hcloud` binary is missing the script automatically falls back to the
  official `huaweicloudsdkhss` v5 SDK (`HssClient.list_host_status`), reading
  AK/SK only from whitelisted environment-variable names (never literals, and
  never by enumerating `os.environ`).
- **Offset paging** — pages through all hosts with `--limit` (10–200) and
  `--offset` (0–2,000,000), stopping once `total_num` is reached.
- **Explicit Chinese error hints** — distinguishes empty list, IAM 403
  (missing `hss:host:listHostStatus`), KooCLI `[USE_ERROR]` parameter errors,
  missing credentials, missing project_id, missing hcloud/SDK, and unknown
  API failures.

**Dependency**: Quality telemetry is collected automatically via
skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## Prerequisites

1. **hcloud CLI** installed and authenticated with valid AK/SK credentials.
   - Installation guide: see `references/cli-installation-guide.md`
   - Verify: `hcloud configure list` shows a valid profile
2. **Region / Project**: HSS is region-scoped; KooCLI resolves the project ID
   automatically from `--cli-region` in the active profile.
3. **IAM permission**: `hss:host:listHostStatus` (read-only) on the HSS
   service. See `references/iam-policies.md` for the least-privilege policy.
4. **Python 3.8+** and, for the SDK fallback path,
   `pip install huaweicloudsdkcore huaweicloudsdkhss`.
5. **Outbound HTTPS** access to `hss.<region>.myhuaweicloud.com`.
6. **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent,
   skips if present).
   - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
   - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

```
1. Identify target → region (default cn-north-4), optional filters
2. Build command → hcloud HSS ListHostStatus with real query parameters
3. Execute → CLI, or SDK fallback if hcloud is missing
4. Page → loop with --offset until total_num
5. Output → full-field table / --json / --names-only
6. Errors → explicit Chinese hints (empty / 403 / credentials / param)
```

## Core Commands

> **⚠️ Mandatory: every hcloud command in this skill MUST be wrapped with `skill-quality-cli run --skill-name huawei-cloud-hss-list --`** — bare hcloud calls are strictly forbidden.

### List all protected hosts (full-field table)

```bash
python3 scripts/list_hss.py --region={region}
```

### JSON output (raw response array)

```bash
python3 scripts/list_hss.py --region={region} --json
```

### Names-only compact list

```bash
python3 scripts/list_hss.py --region={region} --names-only
```

### Filter by agent / host / protection status

```bash
python3 scripts/list_hss.py --region={region} --agent-status={online|offline|installing|install_failed|not_installed|not_online} \
  [--host-status={ACTIVE|SHUTOFF|BUILDING|ERROR}] \
  [--protect-status={opened|closed|protection_exception}]
```

### Filter by host name / ID / IP / OS / edition

```bash
python3 scripts/list_hss.py --region={region} \
  [--host-name={host_name}] [--host-id={host_id}] [--ip-addr={ip}] \
  [--os-type={Linux|Windows}] [--version={hss.version.basic|hss.version.advanced|hss.version.enterprise|hss.version.premium|hss.version.wtp}] \
  [--enterprise-project-id={0|all_granted_eps}]
```

### Page through all hosts

```bash
python3 scripts/list_hss.py --region={region} --page-size={10..200}
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
offset paging):

```bash
skill-quality-cli run --skill-name huawei-cloud-hss-list -- hcloud HSS ListHostStatus --cli-region={region} --limit=10 --offset=0

# Read-only credential readiness check (also wrapped)
skill-quality-cli run --skill-name huawei-cloud-hss-list -- hcloud configure list
```

## Parameter Confirmation

The script's `--host-name` / `--host-id` / `--agent-status` / `--host-status`
/ `--protect-status` / `--os-type` / `--ip-addr` / `--version` /
`--enterprise-project-id` arguments map 1:1 to the real server-side
`ListHostStatus` query parameters of the same name (verified with
`hcloud HSS ListHostStatus --help`).

| Parameter | Required | Description | Example |
| --------- | -------- | ----------- | ------- |
| `--region` / `--cli-region` | Yes (auto) | Target region, defaults to `cn-north-4` | `cn-north-4` |
| `--json` | No | Raw JSON array output | — |
| `--names-only` | No | Compact host-name list output | — |
| `--host-name` | No | Server name filter | `web-01` |
| `--host-id` | No | Server ID filter | `2d8d24c0-...` |
| `--agent-status` | No | Agent status filter | `online`, `offline`, `not_installed`, `not_online` |
| `--host-status` | No | Server status filter | `ACTIVE`, `SHUTOFF`, `BUILDING`, `ERROR` |
| `--protect-status` | No | Protection status filter | `opened`, `closed`, `protection_exception` |
| `--os-type` | No | OS type filter | `Linux`, `Windows` |
| `--ip-addr` | No | IP address filter | `192.168.1.10` |
| `--version` | No | Enabled HSS edition filter | `hss.version.enterprise` |
| `--enterprise-project-id` | No | Enterprise project filter | `0`, `all_granted_eps` |
| `--page-size` | No | Page size (10–200), default 10 | `50` |
| `--project-id` | No | Project ID (SDK fallback path only) | — |
| `--operation` | No | hcloud HSS operation (read-only `ListHostStatus` only) | — |

## Output Example

```
Region cn-north-4 的 HSS 主机防护列表（共 2 台，完整字段）：
host_name  private_ip    public_ip  os_name     os_type  host_status  agent_status  version                  protect_status  detect_result
---------  ------------  ---------  ----------  -------  -----------  ------------  -----------------------  --------------  -------------
web-01     192.168.1.10  1.2.3.4    CentOS 7.6  Linux    ACTIVE       online        hss.version.enterprise   opened          clean
db-02      192.168.1.11  -          Ubuntu 20.04 Linux    SHUTOFF      offline       hss.version.basic        opened          undetected
```

### Status value reference

| Field | Values |
| ----- | ------ |
| `agent_status` | `online`, `offline`, `installing`, `install_failed`, `not_installed`, `not_online` (query only) |
| `host_status` | `ACTIVE`, `SHUTOFF`, `BUILDING`, `ERROR` |
| `protect_status` | `opened`, `closed`, `protection_exception` |
| `version` | `hss.version.null`, `basic`, `advanced`, `enterprise`, `premium`, `wtp`, `container.enterprise` |
| `os_type` | `Linux`, `Windows` |

## Reference Documents

- `references/cli-installation-guide.md` — hcloud CLI installation and authentication
- `references/iam-policies.md` — Least-privilege IAM policies for HSS
- `references/verification-method.md` — Verification and testing methods
- `references/dataflow-diagram.md` — Data flow diagram
- `references/acceptance-criteria.md` — Acceptance criteria

## KooCLI Command Format Standard

```bash
hcloud HSS ListHostStatus --cli-region={region} --limit={10..200} --offset={0..} [--key=value ...]
```

| Feature | Description | Example |
| ------- | ----------- | ------- |
| Service name | `HSS` (exact KooCLI service name) | `HSS` |
| Operation name | PascalCase | `ListHostStatus` |
| Region parameter | `--cli-region=<value>` | `--cli-region={region}` |
| Simple parameter | `--key=value` | `--agent_status=online` |
| Indexed parameter | `--key.1=value1` | `--host_id_list.1=xxx` |
---
name: huawei-cloud-aad-protected-ip-list
description: |
  1. Query the Huawei Cloud Anti-DDoS (AAD, 抗DDoS) protected-IP inventory of the
     current account through KooCLI (hcloud AAD ListProtectedIp — read-only GET
     /v1/cnad/protected-ips), returning protected IPs, block/cleaning status,
     bound policies, packages and regions.
  2. Answers questions such as "哪些 IP 在被 DDoS 防护", "是否有 IP 处于封堵",
     "防护 IP 挂的是哪个策略/套餐", "Anti-DDoS 防护盘点".
  3. Output modes: a concise list (default: 防护 IP | 封堵状态), --table
     (防护 IP | 状态 | 绑定策略 | 套餐 | region), and --json (raw response).
  4. Filters: --ip (exact), --policy-id, --package-id, --tag, --region
     (default cn-north-4). --limit 1~100 with automatic offset paging fetches the
     full inventory.
  5. Falls back to the official huaweicloudsdkaad SDK when KooCLI is missing or
     cannot serve the operation; the same field mapping and output layer are
     reused.
  6. Explicit, executable error hints for an empty list, 403 / insufficient IAM
     permission, missing credentials, [USE_ERROR] and network failures — never a
     traceback.
  7. Built-in write-intent guard: any mutating intent (add / delete / associate /
     disassociate / execute-unblock / modify / update / batch ...) is rejected
     before execution — this skill is strictly read-only.
  8. Triggers include: "查询Anti-DDoS防护IP", "Anti-DDoS 防护 IP 列表",
     "哪些IP在被防护", "DDoS 防护盘点", "封堵状态排查", "AAD 防护对象列表",
     "list AAD protected IPs", "anti-ddos protected ip list".
tags: [huawei-cloud, aad, anti-ddos, security, readonly]
---

# Huawei Cloud Anti-DDoS Protected IP List

## Overview

Query the Anti-DDoS (AAD) protected-IP inventory of a tenant region through
KooCLI AAD `ListProtectedIp` (GET `/v1/cnad/protected-ips`), returning
protected IPs, status (normal / cleaning / blackholed), bound policy,
package and region. This skill supports DDoS protection inventory, block-status
troubleshooting and daily security patrol.

| Command | REST path | Scope |
| ------- | --------- | ----- |
| `hcloud AAD ListProtectedIp` | `GET /v1/cnad/protected-ips` | protected IPs of the current account/region |

Architecture:

```text
agent → python3 scripts/list_aad_protected_ip.py [--region=<region>] [filters]
      → hcloud AAD ListProtectedIp --cli-region=<region> --limit=100 --offset=N
      → Huawei Cloud AAD OpenAPI → parsed JSON → offset/limit paging
      → default concise list / --table / --json
      (CLI unavailable → huaweicloudsdkaad SDK, same mapping and output layer)
```

Key properties:

- **Read-only by design** — only the `ListProtectedIp` GET operation is ever
  constructed. A write-intent guard scans arguments before execution and
  rejects mutating intents with an explicit message (exit code 1).
- **KooCLI first, SDK fallback** — credentials stay in the KooCLI profile;
  when the CLI is missing or cannot serve this operation, the official
  `huaweicloudsdkaad` SDK is used with environment credentials.
- **Automatic paging** — `--limit` is the page size (1~100, values above 100
  are clamped); the script loops `offset` until the full set is fetched.
- **Executable errors** — empty results, 403, missing credentials, `[USE_ERROR]`
  and network failures each print a next-step hint and never a traceback.
- **Offline-testable** — routing, output modes, filters, paging, error
  classification, SDK fallback and the write-intent guard are covered by unit
  tests that mock both backends.

Out of scope: every mutating Anti-DDoS action (create / delete policy, associate
or disassociate IP, execute unblock, modify package or tag), traffic-cleaning
statistics, attack-event analytics and alert subscriptions.

> **Dependency**: Quality telemetry is collected automatically via
> skill-quality-cli (installed by `scripts/ensure_cli.sh` if absent).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   The fallback SDK requires Python 3.8+ and `huaweicloudsdkaad`.
2. **Active credential profile** — configure credentials out-of-band (run the
   KooCLI configure command in your terminal, or set credential environment
   variables). Never paste AK/SK into chat; the script never reads, echoes, or
   stores secrets itself.
3. **IAM permission** — read-only `aad:protectedIp:list`; the least-privilege
   policy is in [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** for the wrapper (standard library only; the SDK is optional).
5. **Outbound HTTPS** access to `*.myhuaweicloud.com`.
- **`skill-quality-cli`** — ensured by `bash scripts/ensure_cli.sh` (idempotent, skips if present)
  - Upgrade: run `skill-quality-cli upgrade` manually (no auto-upgrade)
  - Disable telemetry report: set `SKILL_QUALITY_REPORT=0`

## Workflow

1. **Confirm the target region** (default `cn-north-4`); every AAD call is
   region-scoped.
2. **Choose the view** — default concise list, `--table` for details, or
   `--json` for downstream tooling.
3. **Apply optional filters** — `--ip`, `--policy-id`, `--package-id`, `--tag`.
4. **Run the list script**; paging is automatic (`--limit` controls page size,
   `--offset` the starting position).
5. **Read the result** — table for humans, `--json` for tooling.
6. **Handle the empty / error cases** per the Edge Cases table below.

## Core Commands

### List protected IPs (default)

```bash
> **⚠️ Mandatory: every `hcloud` command in this skill MUST be wrapped with `skill-quality-cli run --skill-name huawei-cloud-aad-protected-ip-list -- ` — bare `hcloud` calls are strictly forbidden.**

skill-quality-cli run --skill-name huawei-cloud-aad-protected-ip-list -- python3 scripts/list_aad_protected_ip.py --region={region}
```

Under the hood the skill runs:

```bash
skill-quality-cli run --skill-name huawei-cloud-aad-protected-ip-list -- hcloud AAD ListProtectedIp --cli-region={region} --limit=100 --offset=0
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--cli-region` | Yes (auto) | Region, agent fills automatically |
| `--limit` | No | Page size 1~100; the wrapper pages automatically |
| `--offset` | No | Starting offset, default 0 |
| `--ip` | No | Exact protected-IP filter |
| `--policy_id` | No | Policy ID filter |
| `--package_id` | No | Package (instance) ID filter |
| `--tag` | No | Local tag filter |

### Detailed table

```bash
skill-quality-cli run --skill-name huawei-cloud-aad-protected-ip-list -- python3 scripts/list_aad_protected_ip.py --table --region={region}
```

Columns: 防护 IP | 状态 | 绑定策略 | 套餐 | region.

### JSON output

```bash
skill-quality-cli run --skill-name huawei-cloud-aad-protected-ip-list -- python3 scripts/list_aad_protected_ip.py --json --region={region}
```

The JSON body is `{"total": N, "items": [...]}` across all pages. Item fields
include `id`, `ip`, `type`, `name`, `status`, `status_detail`, `policy_name`,
`region`, `package_id`, `package_name`, `tag`, `tags`, `is_resale` and
`package_version`.

### Filtered query

```bash
skill-quality-cli run --skill-name huawei-cloud-aad-protected-ip-list -- python3 scripts/list_aad_protected_ip.py --ip 192.0.2.10 --policy-id {policy_id} --region={region}
```

### Paging

```bash
skill-quality-cli run --skill-name huawei-cloud-aad-protected-ip-list -- python3 scripts/list_aad_protected_ip.py --limit 50 --offset 100 --region={region}
```

`--limit` is a page size, not a total cap: the wrapper keeps requesting pages
until `total` is reached or a short page is returned.

## Parameter Confirmation

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--region` | No | Huawei Cloud region (CLI `--cli-region`) | `cn-north-4` |
| `--json` | No | Raw JSON response (`total` + merged `items`) | flag |
| `--table` | No | Detail table view | flag |
| `--ip` | No | Exact protected-IP filter | `192.0.2.10` |
| `--policy-id` | No | Policy ID filter | `policy-xxxx` |
| `--package-id` | No | Package (instance) ID filter (32~64 chars) | `0123456789abcdef0123456789abcdef` |
| `--tag` | No | Local tag filter | `web` |
| `--limit` | No | Page size 1~100, default 100 | `50` |
| `--offset` | No | Starting offset, default 0 | `100` |
| `--action` | No | Only `list` / `query` / `search` / `show`; other values are rejected as write intents | `list` |
| `--timeout` | No | Per-command timeout seconds, default 60 | `60` |

## Read-only guard

The skill refuses to run when it detects a mutating intent. The check runs
right after argument parsing and before any KooCLI/SDK call:

- `--action unblock` / `--action delete` / any action other than
  `list` / `query` / `search` / `show` → rejected, exit code 1.
- Filter values containing write tokens such as `add`, `create`, `delete`,
  `remove`, `update`, `modify`, `associate`, `disassociate`, `unblock`,
  `batch`, `enable`, `disable` → rejected, exit code 1.
- No cloud call is made when the guard fires.

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No protected IPs in the region | `未找到 Anti-DDoS 防护 IP。` (exit 0) |
| Filters match nothing | `未找到匹配的 Anti-DDoS 防护 IP。` (exit 0) |
| IAM permission missing (403 / not authorized) | `无权限访问 Anti-DDoS 防护 IP 列表（403 / not authorized）...` |
| Missing credentials | Explicit KooCLI profile / `HUAWEICLOUD_SDK_AK` hint |
| `[USE_ERROR]` unsupported operation | Falls back to the SDK; if that fails, an upgrade/install hint |
| Network timeout / unreachable | `访问 Anti-DDoS 接口失败（网络超时或不可达）...` |
| hcloud not installed and no SDK | Install hint for KooCLI or `pip install huaweicloudsdkaad` |
| Write intent detected | Read-only guard message before any command runs |

## References

- [references/cli-installation-guide.md](references/cli-installation-guide.md)
- [references/iam-policies.md](references/iam-policies.md)
- [references/verification-method.md](references/verification-method.md)
- [references/acceptance-criteria.md](references/acceptance-criteria.md)

## KooCLI Command Format Standard

```bash
skill-quality-cli run --skill-name huawei-cloud-aad-protected-ip-list -- hcloud <service> <Operation> --cli-region=<region> [--key=value ...]
```

| Feature | Description | Example |
|---------|-------------|---------|
| Service name | `AAD` (verified from the AAD service help) | `AAD` |
| Operation name | PascalCase | `ListProtectedIp` |
| Region parameter | `--cli-region=<value>` | `--cli-region=cn-north-4` |
| Simple parameter | `--key=value` | `--limit=100` |

Service, operation and parameter names are taken verbatim from the AAD
service help and the ListProtectedIp operation help — never invented.
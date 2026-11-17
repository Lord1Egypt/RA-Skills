---
name: huawei-cloud-bms-list
description: |
  1. List Huawei Cloud BMS (Bare Metal Server) instances in a tenant region
     through KooCLI (hcloud BMS ListBareMetalServers — read-only GET
     /v1/{project_id}/baremetalservers/detail), with an automatic fallback to
     the official huaweicloudsdkbms v1 SDK when hcloud is not installed.
2. Output modes: full-field table (default, every returned field including
     名称/ID/状态/规格/可用区/IP), --json (raw response array), and --names-only
     (compact server-name list), plus an additive Markdown export
     (--md-file / --output-md) that writes Region + 查询时间 + 主机总数 + a
     fixed inventory table (名称/ID/状态/规格/可用区/IP) to a .md file.
  3. Supports --name / --server-id / --status filtering, region override, and
     automatic page-number offset paging. --name / --status are real
     ListBareMetalServers query parameters; --server-id is applied client-side
     (full list fetched first, then filtered locally) because the real BMS
     ListBareMetalServers API has no server-id parameter.
  4. Explicit error hints for empty server lists (「当前区域无裸金属服务器」), 403 /
     insufficient IAM permission (「无权限访问 BMS，请检查 IAM 权限」), missing or
     invalid AK/SK credentials, hcloud not installed, and Markdown write failure
     (missing directory / no permission).
  5. Built-in write-intent guard: any mutating intent (create / delete / update /
     reboot / rebuild / resize / reinstall / reset / attach / detach / change)
     or any operation other than ListBareMetalServers is rejected before
     execution — this skill is strictly read-only.
  6. Triggers include: "list BMS servers", "bare metal server list", "裸金属服务器列表",
     "查询裸金属服务器", "BMS 实例列表", "裸金属服务器巡检", "BMS inventory",
     "list bare metal servers", "华为云裸金属列表", "把 BMS 列表导出成 md",
     "导出裸金属服务器清单".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     paging, error scenarios, SDK fallback, the write-intent guard, and the
     Markdown report (rendering / default name / explicit path / empty list /
     write failure).
tags: [huawei-cloud, bms, compute, readonly, koo-cli]
---

# Huawei Cloud BMS Bare Metal Server List

## Overview

Query the BMS (Bare Metal Server) instance list of a tenant region through
KooCLI `hcloud BMS ListBareMetalServers` (official read-only GET
`/v1/{project_id}/baremetalservers/detail`, verified in the
`huaweicloudsdkbms` v1 client `_list_bare_metal_servers_http_info` metadata).
The skill is aimed at bare-metal inventory inspection, daily operations patrol,
resource reconciliation, and as a pre-query step for other BMS tasks that need a
server `id`.

Architecture:

```text
agent → python3 scripts/list_bms.py → hcloud BMS ListBareMetalServers --cli-region=<region>
      → Huawei Cloud BMS OpenAPI (regional endpoint) → parsed JSON → table / --json / --names-only
                                                                  ↘ [--md-file] → Markdown report (.md)

(hcloud binary missing) → fallback: huaweicloudsdkbms v1 BmsClient.list_bare_metal_servers
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListBareMetalServers`
  (GET). A write-intent guard scans user arguments and validates the operation
  name; mutating intents (create / delete / update / reboot / rebuild / resize /
  reinstall / reset / attach / detach / change ...) are rejected with an
  explicit message before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  hcloud binary is absent, the script falls back to the official
  `huaweicloudsdkbms` v1 SDK (`list_bare_metal_servers`). Credentials are always
  read by the CLI profile / SDK environment — never handled by the script.
- **Full-field table output** — the default table renders the union of all
  fields returned by ListBareMetalServers, with `flavor` flattened into
  flavor_id/flavor_name, `image` into image_id, and the availability zone
  normalized.
- **Additive Markdown export** — `--md-file [PATH]` writes an archival report
  (Region / 查询时间 / 主机总数 + a fixed inventory table
  `名称 | ID | 状态 | 规格 | 可用区 | IP`, empty list → `共 0 个裸金属服务器`,
  active filters listed) *in addition to* the stdout output, which stays exactly
  as before. The file is written through a temporary sibling and moved into
  place, so a failed write never leaves a half file.
- **Offline-testable** — every code path (paging, filters, error
  classification, guard, SDK fallback, Markdown rendering and file write) is
  covered by unit tests that mock the hcloud subprocess.

Out of scope: every mutating BMS action (create / delete / update / rename /
reboot / rebuild / reinstall OS / resize / reset password / attach or detach
volume / manage NICs and tags). Those require a dedicated write-capable skill
and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkbms` to enable the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (`hcloud configure` in your terminal, or credential environment variables).
   Never paste AK/SK into chat; the script never reads, echoes, or stores
   secrets itself — authentication is delegated entirely to the hcloud profile
   / SDK environment.
3. **IAM permission** — read-only `bms:server:list`; least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess).
5. **Outbound HTTPS** access to `*.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`); every BMS call is
   region-scoped.
2. **Confirm hcloud readiness** (optional, read-only): `hcloud configure list`.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact inventory; add `--md-file` when the result must
   be archived / attached to a ticket (the stdout output is kept unchanged and
   the generated file path is printed).
5. **Handle the empty / error cases** per the Edge Cases table below (the
   script prints an explicit hint for empty region, 403, missing AK/SK, and
   Markdown write failure).

## Core Commands

```bash
# Full-field table (default)
python3 scripts/list_bms.py --region cn-north-4

# Raw JSON of every returned field
python3 scripts/list_bms.py --json

# Compact server-name list only
python3 scripts/list_bms.py --names-only

# Filter by server status (server-side real API parameter)
python3 scripts/list_bms.py --status ACTIVE

# Filter by name (server-side) / by exact server ID (client-side)
python3 scripts/list_bms.py --name bms-demo
python3 scripts/list_bms.py --server-id 6a6f7a3b-2d3b-4b0e-9f3a-0d1f2c3d4e5f

# Combine filters
python3 scripts/list_bms.py --region cn-south-1 --status ACTIVE --names-only

# Also write a Markdown report to an explicit path (stdout output unchanged)
python3 scripts/list_bms.py --md-file /tmp/bms-inventory.md

# Default file name bms-list-<region>-<YYYYMMDD>.md in the current directory
python3 scripts/list_bms.py --md-file

# Alias + stacking: raw JSON on stdout AND the Markdown report on disk
python3 scripts/list_bms.py --output-md report.md --json
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
paging). `offset` is the **page number** (starts at 1):

```bash
hcloud BMS ListBareMetalServers --cli-region=cn-north-4 --limit=100 --offset=1
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--json` | No | Output the raw server array as JSON | — |
| `--names-only` | No | Output server names only | — |
| `--name` | No | Filter by server name — **server-side** real ListBareMetalServers parameter | `bms-demo-01` |
| `--status` | No | Filter by server state — **server-side** real ListBareMetalServers parameter (`ACTIVE` / `BUILD` / `ERROR` / `HARD_REBOOT` / `REBOOT` / `REBUILD` / `SHUTOFF`) | `ACTIVE` |
| `--server-id` | No | Filter by exact server ID — **applied client-side** (the BMS ListBareMetalServers API has no server-id parameter; full list fetched, then filtered locally, case-insensitive) | `6a6f7a3b-…` |
| `--page-size` | No | Page size for ListBareMetalServers (default 100, API max 1000) | `100` |
| `--operation` | No | hcloud BMS operation name; only `ListBareMetalServers` is allowed | `ListBareMetalServers` |
| `--md-file [PATH]` / `--output-md [PATH]` | No | **Additive** Markdown report. With `PATH` → write there; without a value → `bms-list-<region>-<YYYYMMDD>.md` in the current directory; omitted → no file is created | `/tmp/inventory.md` |

Output-mode precedence: `--names-only` → `--json` → table (default).
The Markdown export is **not** part of that precedence: `--md-file` layers on top
of whatever stdout mode is active and never changes the stdout output.

### Markdown report layout

```markdown
# Huawei Cloud BMS 裸金属服务器清单

- **Region**: cn-north-4
- **查询时间**: 2026-10-20 14:36:10 CST
- **主机总数**: 2

## 裸金属服务器清单

| 名称 | ID | 状态 | 规格 | 可用区 | IP |
| --- | --- | --- | --- | --- | --- |
| bms-demo-01 | bms-0001 | ACTIVE | s4.xlarge | cn-north-4a | 10.0.0.5 |
| bms-demo-02 | bms-0002 | SHUTOFF | s3.large | cn-north-4b | 10.0.0.6 |
```

- The report is UTF-8. `查询时间` is the local time of the query; the file name
  uses `<YYYYMMDD>` of the same moment.
- The inventory table has a fixed column order — 名称 / ID / 状态 / 规格 / 可用区 /
  IP. `flavor` is flattened into 规格 and `os_ext_a_zavailability_zone` into
  可用区, exactly like the stdout table. The IP column reuses `access_i_pv4`; a
  missing value renders as `-`.
- Empty result → `共 0 个裸金属服务器`（+ the filters actually sent, e.g.
  `共 0 个裸金属服务器（过滤条件: status=ACTIVE）`), exit code 0 — same as the
  stdout behaviour for an empty region.
- On success the script prints `已生成 Markdown 文件：<绝对路径>` on stdout.
- Server names appear in the report as returned by BMS; a server without a name
  falls back to its ID.

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `modify`, `reboot`, `rebuild`,
  `reinstall`, `resize`, `reset`, `change`, `attach`, `detach`, `stop`, `start`,
  `restore`, and BMS operation names such as `CreateBareMetalServers`,
  `BatchRebootBaremetalServers`, `ReinstallBaremetalServerOs`).
- The `--status` value is exempted from the scan: BMS status enumerants
  (`REBOOT` / `HARD_REBOOT` / `REBUILD`) legitimately contain write-looking words
  and are read-only filters.
- The value of the local output flag (`--md-file` / `--output-md`) is **not**
  scanned: it is file-path data, so a report such as `bms-delete-report.md` is
  written normally.
- `--md-file` takes an *optional* value, so a flag following it is still
  scanned — `--md-file --operation DeleteBareMetalServer` cannot hide a mutating
  flag.
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed.
- Only `hcloud BMS ListBareMetalServers` (GET) — or the SDK
  `list_bare_metal_servers` call in the fallback path — is ever constructed by
  `build_command()`; there is no code path that can issue a mutating BMS API
  call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `BMS`.
- **Operation name** — PascalCase: `ListBareMetalServers`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete BMS call).
- **Simple parameter** — `--key=value`, e.g. `--limit=100`, `--offset=1`,
  `--name=bms-01`, `--status=ACTIVE`. `offset` is the **page number** (the BMS
  pagination API starts at page 1). There is **no server-id parameter** on the
  real BMS ListBareMetalServers API (verified via
  `hcloud BMS ListBareMetalServers --help`); server-id filtering is done
  client-side by the script, never forwarded to the CLI/API.
- **REST path (official SDK `_http_info`)** —
  `GET /v1/{project_id}/baremetalservers/detail` (`huaweicloudsdkbms` v1
  `_list_bare_metal_servers_http_info`); project_id is resolved by KooCLI from
  the credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty server list | Exit 0, prints `当前区域（<x>）无裸金属服务器` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 BMS，请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkbms` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud BMS ListBareMetalServers --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |
| Markdown report cannot be written (missing directory / no permission / path is a directory) | Exit 1, `[错误] 无法写入 Markdown 文件 <绝对路径>: <原因>`, no half file left behind (the report is written via a temp sibling and moved into place) |
| Empty server list **with** `--md-file` | Exit 0, stdout hint unchanged; the report is still written and contains `共 0 个裸金属服务器` (+ active filters) |

Exit codes: `0` success / empty region; `1` config, auth, guard, API, or Markdown-write error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| `BUILD` / `ERROR` / `REBOOT` servers | Reported with their state, not treated as failure |
| `--status` filter | Forwarded as a real server-side API parameter (case preserved); `REBOOT` / `HARD_REBOOT` / `REBUILD` are exempted from the write-intent guard |
| `--server-id` filter | Applied client-side after the full paged list is fetched (case-insensitive); the server API has no server-id parameter |
| Large server count | Automatic page-number paging (`offset` = page, 1-based; `count` / `total_count` aware, short-page stop, max 100 pages) |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on a server | Rendered as `-` in the table |
| Nested `flavor` / `image` / availability zone | Flattened into flavor_id / flavor_name / image_id / availability_zone for the table |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkbms` list_bare_metal_servers, same output modes |
| `--md-file` without a path | Default `bms-list-<region>-<YYYYMMDD>.md` in the current working directory; the absolute path is printed |
| `--md-file` path contains `delete` / `start` / `reboot` ... | Not a cloud operation — the path is exempt from the write-intent guard, so `bms-delete-report.md` is written normally |
| `--md-file` combined with `--json` / `--names-only` | Both outputs are produced: the stdout mode is unchanged and the report is written as well |
| Report path already exists | Overwritten atomically (temp file + rename) — no partially written file is ever observable |
| Report path parent directory missing | Not auto-created; `无法写入 Markdown 文件` + exit 1 (create the directory first) |
| Server name contains a pipe character or a newline | Escaped in the Markdown table cell (`\|`, newlines folded to a space) |
| User asks to create/delete/reboot a server | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / reboot / rebuild
/ resize / reinstall / normalize variants / operation whitelist / status-value
exemption / `--md-file` path values not blocked / a flag after `--md-file` still
scanned), command construction (page-number offset, name + status forwarded,
no write flags), JSON extraction, failure classification (missing AK/SK, 403,
generic, `[USE_ERROR]` with rc=0), client-side server-id filtering (exact /
case-insensitive / no-match / missing field), paging (count-aware / full-page /
empty / page increments), SDK fallback (success and unavailable; request
construction matches the real `ListBareMetalServersRequest` signature), rendering
(table with flavor / image / availability-zone fields / names / fallbacks), all
main() output modes including empty, filter, and error paths, and the Markdown
report: `render_markdown` (Region / 查询时间 / 主机总数 / fixed
名称·ID·状态·规格·可用区·IP table / `-` for missing values / empty-list message /
filters / pipe and newline escaping / ID fallback), `default_markdown_name`,
`format_query_time`, `active_filter_descriptions`, `write_markdown_file` (UTF-8
round-trip, overwrite, missing directory and unwritable target → `OutputError`
with no half file and no temp sibling), and `main()` with `--md-file` /
`--output-md` (explicit path, default file name, region-sensitive default name,
alias, write words in the path, empty list, write failure, stacking with `--json`
/ `--names-only`, no file without the flag, guard still wins over the report).

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |

---
name: huawei-cloud-sfs-export-markdown
description: |
  1. Query the Huawei Cloud SFS (Scalable File Service / SFS Turbo) file-system
     list of a tenant region through KooCLI (`hcloud SFSTurbo ListShares`, the
     official read-only GET /v1/{project_id}/sfs-turbo/shares/detail), with an
     automatic fallback to the official huaweicloudsdksfsturbo v1 SDK
     (`SFSTurboClient.list_shares`) when hcloud is not installed.
  2. Export the file-system name list (plus ID / status / protocol / capacity /
     availability zone / type / enterprise project / created time) into a
     well-formed local Markdown table file — strictly local file generation,
     nothing is ever written back to the cloud. `--output` sets the file path
     (default `sfs_share_list.md` in the current directory); the parent
     directory is created automatically and the file is written via a temp file
     + atomic rename.
  3. Region aware: `--region` (default cn-north-4). Optional client-side
     filters — `--name` / `--id` / `--az` (case-insensitive substring) and
     `--status` / `--share-proto` (case-insensitive exact) — the real
     ListShares API has no such parameters, so the full paged list is fetched
     first and filtered locally. The applied filters are echoed in the
     document's metadata line (`过滤条件: ...`; `无过滤条件` when none).
  4. Explicit error classification: empty file-system list (still writes the
     file — `当前区域（x）无 SFS 文件系统` when the region truly has none,
     `当前过滤条件下无匹配的 SFS 文件系统` when a filter matched nothing),
     missing AK/SK credentials (「缺少 AK/SK 凭证」), 403 / insufficient
     IAM permission (「无权限访问 SFS，请检查 IAM 权限」), hcloud not installed
     (falls back to the SDK, else a clear hint), KooCLI usage errors, and
     generic API/network failures.
  5. Built-in write-intent guard: any mutating intent (create / delete / expand
     / shrink / resize / mount / unmount / attach / detach / restore / reboot
     ...) or any operation other than the read-only ListShares is rejected
     before execution — this skill is strictly read-only.
  6. Triggers include: "查询SFS并导出md", "导出SFS文件系统清单为md", "SFS 名称
     Markdown", "SFS list markdown", "SFS inventory markdown", "华为云SFS导出
     markdown", "export SFS file systems to markdown".
  7. Offline unit tests (mocked hcloud subprocess) cover the guard, paging,
     filters, Markdown rendering, atomic file writing, error classification and
     SDK fallback.
tags: [huawei-cloud, sfs, storage, readonly, markdown]
---

# Huawei Cloud SFS File System List → Markdown Export

## Overview

Query the SFS (Scalable File Service / SFS Turbo) file-system list of a tenant
region through KooCLI `hcloud SFSTurbo ListShares` (official read-only GET
`/v1/{project_id}/sfs-turbo/shares/detail`, verified in the
`huaweicloudsdksfsturbo` v1 client `_list_shares_http_info` metadata), then
render the file-system name list as a Markdown table and write it to a local
`.md` file. The skill is aimed at SFS inventory / asset export, daily
operations patrol, handover reports and any "save the file-system list as a
Markdown file" request.

Architecture:

```text
agent → python3 scripts/list_sfs_export_markdown.py → hcloud SFSTurbo ListShares --cli-region=<region> --limit=N --offset=O
      → Huawei Cloud SFS OpenAPI (regional endpoint) → parsed JSON → Markdown table → local .md file

(hcloud binary missing) → fallback: huaweicloudsdksfsturbo v1 SFSTurboClient.list_shares
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListShares` (GET).
  A write-intent guard validates the operation name and scans the arguments;
  mutating intents (create / delete / expand / shrink / resize / mount /
  unmount / attach / detach / restore / reboot ...) are rejected with an
  explicit message before any command runs. The `.md` file is generated on the
  **local filesystem only** — no SFS write happens and no user confirmation can
  make this skill issue a write.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  hcloud binary is absent, the script falls back to the official
  `huaweicloudsdksfsturbo` v1 SDK (`list_shares`). Credentials are always read
  by the CLI profile / SDK environment — never handled by the script.
- **Empty result is not an error** — an empty file-system list (or a filter
  that matches nothing) still produces a valid `.md` file with the table header
  and an explicit "no file systems" note, and exits `0`.
- **Atomic local file** — the Markdown body is written to a temporary file and
  renamed into place, so an interrupted write never leaves a corrupt / partial
  file behind.
- **Offline-testable** — every code path (paging, filters, rendering, atomic
  write, error classification, guard, SDK fallback) is covered by unit tests
  that mock the hcloud subprocess.

> **Capability boundary:** this skill lists **file systems only** and exports
> them locally; it does not manage the file-system lifecycle (create / delete /
> expand / shrink / rename / mount / ACL / permission rules / backend binding),
> and it does not export to Excel / PDF / CSV. It also does not cover the SFS
> 3.0 「通用文件系统」 product (`ListFileSystems`). Those require a separate
> skill.

> **Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## Differentiation from the plain SFS file-system list skill

The repository keeps a terminal-oriented SFS **file-system-list** skill and this
**Markdown-export** skill side by side. They share the same read-only API but
produce different artifacts, and they are **not** runtime dependencies of each
other.

| Dimension | Plain SFS file-system list skill | This export skill |
| --------- | -------------------------------- | ----------------- |
| Deliverable | Terminal output (table / JSON / names-only) | A local Markdown file (default `sfs_share_list.md`) |
| Persistence | None — printed to stdout only | Atomic file write + automatic parent-directory creation |
| Purpose | Interactive inspection / pre-query a file-system ID for downstream use | Markdown report export for inventory, patrol, handover |

Per-service "query + export to a file" capabilities are an established
repository convention and are kept as their own skill, separate from the plain
list skill and named by the export format. This skill continues that convention
for SFS with Markdown as the output format. Use the plain SFS list skill to view
file systems in the terminal; use this skill when the file-system list must be
saved as a distributable / archivable Markdown document.

## Prerequisites

1. **Python 3.8+** — the Markdown export uses only the Python standard library.
   For the hcloud-absent fallback, run `python3 scripts/ensure_env.py` to install
   `huaweicloudsdkcore` / `huaweicloudsdksfsturbo` automatically. See
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
2. **KooCLI (`hcloud`) installed** — the primary path. See
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdksfsturbo` to enable
   the SDK fallback path.
3. **KooCLI credentials configured out-of-band** — the script never reads,
   echoes, or stores AK/SK itself; authentication is delegated to the active
   KooCLI profile (CLI path) or the whitelisted environment variables (SDK
   fallback). Never paste AK/SK into chat.
4. **IAM permission** — read-only `sfs:listShares` (or the system policy
   **SFS ReadOnlyAccess**); least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
5. **Outbound HTTPS** access to `sfs-turbo.<region>.myhuaweicloud.com`.
6. **Write access to the local output directory** (for the generated `.md` file).
- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

1. **(Optional) prepare the environment** — `python3 scripts/ensure_env.py`
   installs `huaweicloudsdkcore` / `huaweicloudsdksfsturbo` if they are missing
   (needed only for the SDK fallback).
2. **Confirm the target region** (default `cn-north-4`); every SFS call is
   region-scoped.
3. **Confirm KooCLI readiness** (optional, read-only) — the credential check in
   Core Commands.
4. **Run the export script** with the desired output path and optional filters.
5. **Read the result** — the printed path is the generated Markdown report; open
   that file to see the file-system-name table.
6. **Handle the empty / error cases** per the Error Handling table below (an
   empty result still writes the file; credential / permission failures print an
   explicit hint and write nothing).

## Core Commands

> **⚠️ Mandatory: every hcloud command in this skill MUST be wrapped with skill-quality-cli run --skill-name huawei-cloud-sfs-export-markdown -- ** — bare hcloud calls are strictly forbidden.**

```bash
# Default: query the region's SFS file systems and write sfs_share_list.md in cwd
python3 scripts/list_sfs_export_markdown.py --region cn-north-4

# Explicit output path (recommended) + echo the Markdown to stdout as well
python3 scripts/list_sfs_export_markdown.py --region cn-north-4 \
  --output /tmp/sfs_share_list_cn-north-4.md --stdout

# Name filter (client-side substring) and status filter (client-side exact)
python3 scripts/list_sfs_export_markdown.py --name sfs-demo --status available \
  --output /tmp/sfs_available.md

# ID / protocol / availability-zone filters (same semantics as the plain list skill)
python3 scripts/list_sfs_export_markdown.py --id 8be2f1a3 --output /tmp/sfs_one.md
python3 scripts/list_sfs_export_markdown.py --share-proto NFS --output /tmp/sfs_nfs.md
python3 scripts/list_sfs_export_markdown.py --az cn-north-4a --output /tmp/sfs_az.md

# Combine filters — the metadata line echoes them
python3 scripts/list_sfs_export_markdown.py --region cn-south-1 \
  --share-proto NFS --az cn-south-1a --output /tmp/sfs_south1_nfs.md

# Read-only credential readiness check (wrapped)
skill-quality-cli run --skill-name huawei-cloud-sfs-export-markdown -- hcloud configure list
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
paging; wrap with `skill-quality-cli run` in production):

```bash
skill-quality-cli run --skill-name huawei-cloud-sfs-export-markdown -- hcloud SFSTurbo ListShares --cli-region=cn-north-4 --limit=200 --offset=0
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--output` / `-o` | No | Markdown output file path (default current dir `sfs_share_list.md`) | `/tmp/sfs.md` |
| `--name` | No | Filter by file-system name — **applied client-side** (case-insensitive substring; ListShares has no name parameter) | `sfs-prod` |
| `--id` | No | Filter by file-system ID — **applied client-side** (case-insensitive substring) | `8be2f1a3` |
| `--status` | No | Filter by file-system state — **applied client-side** (case-insensitive exact: `available` / `creating` / `error`) | `available` |
| `--share-proto` | No | Filter by share protocol — **applied client-side** (case-insensitive exact: `NFS` / `CIFS`) | `NFS` |
| `--az` | No | Filter by availability zone — **applied client-side** (case-insensitive substring, `availability_zone` / `az_name` / `az` all considered) | `cn-north-4a` |
| `--page-size` | No | Page size for ListShares (default `200`, max `200`; values outside `[1, 200]` are clamped) | `100` |
| `--operation` | No | hcloud SFSTurbo operation name; only `ListShares` is allowed | `ListShares` |
| `--stdout` | No | Also print the rendered Markdown to stdout (the file is still written) | `--stdout` |

## Markdown Output Format

The generated document has a title, a metadata block, and a table. The
metadata line always states the region, the exported row count and the active
filters:

```markdown
> Region: cn-north-4 | File systems: 2 | 过滤条件: name=demo, az=cn-north-4a
```

With no filter supplied the third segment reads `无过滤条件`. Filter order is
fixed: `name`, `id`, `status`, `share_proto`, `az`.

The table has the following columns (fields missing on a file system render as
`-`):

| Column (header) | Source key | Notes |
| ---------- | ---------- | --------- |
| 文件系统名称 | `name` | File-system name (falls back to ID) |
| 文件系统ID | `id` | File-system ID |
| 状态 | `status` | `available` / `creating` / `error` ... |
| 协议 | `share_proto` | `NFS` / `CIFS` |
| 容量(GB) | `size` | Capacity in GB |
| 可用区 | `availability_zone` | Availability zone (falls back from `az_name` / `az`) |
| 类型 | `share_type` | File-system type |
| 企业项目 | `enterprise_project_id` | Enterprise project id |
| 创建时间 | `created_at` | Creation timestamp |

An empty result still produces the table header + separator and one explicit
note line, and the file is always created:

- the region genuinely has no file systems → `_当前区域（<x>）无 SFS 文件系统。_`
- a filter matched nothing → `_当前过滤条件下无匹配的 SFS 文件系统（过滤条件：...）。_`

## Write-Intent Guard

- The guard validates the `--operation` value (only the read-only `ListShares`
  is accepted) and scans the remaining arguments for mutating vocabulary
  (`create`, `delete`, `update`, `modify`, `expand`, `shrink`, `resize`,
  `mount`, `unmount`, `attach`, `detach`, `restore`, `reboot`, and SFS operation
  names such as `CreateShare`, `DeleteShare`, `ExpandShare`).
- Values of read-only flags (the local `--output` path, `--region`, `--name`,
  `--id`, `--status`, `--share-proto`, `--az`, ...) are excluded from the scan so
  a file path or filter value is never mistaken for an SFS operation.
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`,
  and exits with code 1 **before** a single hcloud command is executed. No write
  operation can be constructed by `build_command()`; there is no code path that
  can issue a mutating SFS API call, so no user confirmation path exists — the
  `Create` / `Delete` / `Update` intents are refused outright.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `SFSTurbo`
  (KooCLI's file-storage service; `SFS` is not a registered KooCLI service).
- **Operation name** — PascalCase: `ListShares`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete SFS call).
- **Simple parameter** — `--key=value`, e.g. `--limit=200`, `--offset=20`. SFS
  Turbo `ListShares` rejects `limit > 200`. There is **no `--name` / `--id` /
  `--status` / `--share-proto` / `--az` parameter** on the real ListShares API
  (verified via `hcloud SFSTurbo ListShares --help`); all filtering is done
  client-side by the script.
- **REST path (official SDK `_http_info`)** —
  `GET /v1/{project_id}/sfs-turbo/shares/detail` (`huaweicloudsdksfsturbo` v1
  `_list_shares_http_info`); project_id is resolved by KooCLI / the SDK from the
  credential profile.

Concrete raw KooCLI command (the script wraps exactly this call; wrap with
`skill-quality-cli run --skill-name huawei-cloud-sfs-export-markdown --` in
production):

| Command | Purpose |
| ------- | ------- |
| `hcloud SFSTurbo ListShares --cli-region=cn-north-4 --limit=1` | Read-only file-system list used as the Markdown source |

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty file-system list | Exit 0; the `.md` file is still written (header + `当前区域（x）无 SFS 文件系统` note) |
| Filter matches nothing | Exit 0; the `.md` file is still written with a `当前过滤条件下无匹配的 SFS 文件系统（过滤条件：...）` note |
| Missing / invalid AK-SK | Exit 1, `缺少 AK/SK 凭证` hint to configure hcloud credentials out-of-band (never in chat); no file written |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 SFS，请检查 IAM 权限` hint; no file written |
| hcloud not installed | Falls back to the SDK; if the SDK is unavailable too, exit 1 with a clear hint |
| Bad `--output` path (permission / bad directory) | Exit 1, `Markdown 文件写出失败` hint; no partial file left |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud SFSTurbo ListShares --help` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| Write intent detected | Exit 1, `GuardError` message, no command executed, no file written |

Exit codes: `0` success / empty list; `1` config, auth, guard, export, or API
error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Region has no file systems | Header + empty-table note written, exit 0 |
| Many file systems | Automatic `offset` paging (count aware, full-page fallback, max 100 pages) |
| `--page-size` above the API cap | Clamped to `200` (SFS Turbo `ListShares` rejects `limit > 200`); below `1` clamped to `1` |
| Filter yields no file system | Empty message includes the active filters; the file is still written |
| Field missing on a file system | Rendered as `-` in the Markdown cell |
| `|` or newline inside a field | Escaped (`\|`) / collapsed to a space so the table stays well-formed |
| `--output` points to a non-existing directory | Directory is created automatically |
| `--output` path contains a guard keyword (e.g. `downloads/expand-*.md`) | Path value is excluded from the guard (local path ≠ SFS operation) |
| `--status creating` | Legitimate read filter — the status value is not sent to the server |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdksfsturbo` list_shares, same Markdown output |
| User asks to create/delete/expand/mount | Out of scope — blocked by the write-intent guard |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
cd skills/storage/sfs/huawei-cloud-sfs-export-markdown
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / expand / shrink /
resize / mount / unmount / attach / detach / restore / normalized separators /
operation whitelist / read-only value scrubbing incl. `--flag=value`), page
size clamping, command construction (`--cli-region` / limit / offset, no write
or filter flags), JSON extraction and file-system extraction, failure
classification (missing AK/SK, 403, generic, `[USE_ERROR]` with rc=0), offset
paging (count / full page / empty), client-side name / ID / status / protocol /
availability-zone filtering, active-filter descriptions, the metadata line with
and without filters, the two empty-result notes (region empty vs filter no
match), SDK fallback (env credentials / missing credentials / unavailable),
normalization, Markdown rendering (title / header / rows / pipe & newline
escaping), atomic file writing (missing dirs / bad path), and all `main()`
output modes.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI + SDK installation, credential configuration and skill-quality-cli |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
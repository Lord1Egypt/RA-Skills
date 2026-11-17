---
name: huawei-cloud-rds-export-markdown
description: |
  1. Query the Huawei Cloud RDS (Relational Database Service) instance list of a
     tenant region through KooCLI (`hcloud RDS ListInstances`, the official
     read-only GET /v3/{project_id}/instances), with an automatic fallback to the
     official huaweicloudsdkrds v3 SDK (`RdsClient.list_instances`) when hcloud is
     not installed.
  2. Export the instance name list (plus ID / status / engine / version / flavor /
     private IP / availability zone / created time) into a well-formed local
     Markdown table file — strictly local file generation, nothing is ever written
     back to the cloud. `--output` sets the file path (default `rds_instances.md`
     in the current directory); the parent directory is created automatically and
     the file is written via a temp file + atomic rename.
  3. Region aware: `--region` (default cn-north-4); `--project_id` is mapped to the
     KooCLI global `--cli-project-id`. Optional `--name` server-side filter and
     `--status` client-side filter (the real ListInstances API has no status
     parameter, so the full list is fetched first and filtered locally).
     Optional `--sort-by name|created` orders the exported rows locally, after the
     filters: `name` compares instance names case-insensitively (id fallback),
     `created` compares creation timestamps oldest-first. The API has no ordering
     parameter, so sorting is always client-side; omitting `--sort-by` keeps the
     API order and the previous output unchanged.
  4. Explicit error classification: empty instance list (still writes the file),
     missing AK/SK credentials (「缺少 AK/SK 凭证」), 403 / insufficient IAM
     permission (「无权限访问 RDS，请检查 IAM 权限」), hcloud not installed (falls
     back to the SDK, else a clear hint), KooCLI usage errors, and generic
     API/network failures.
  5. Built-in write-intent guard: any mutating intent (create / delete / update /
     resize / restart / stop / restore ...) or any operation other than the
     read-only ListInstances is rejected before execution — this skill is strictly
     read-only.
  6. Triggers include: "查询RDS生成md文件", "导出RDS实例清单为md", "RDS 实例名称
     Markdown", "RDS list markdown", "RDS inventory markdown", "华为云RDS导出
     markdown", "export RDS instances to markdown".
  7. Offline unit tests (mocked hcloud subprocess) cover the guard, paging,
     filters, local sorting (`--sort-by name` / `created`), Markdown rendering,
     atomic file writing, error classification, SDK fallback and all output modes.
tags: [huawei-cloud, rds, database, readonly, markdown]
---

# Huawei Cloud RDS Instance List → Markdown Export

## Overview

Query the RDS instance list of a tenant region through KooCLI
`hcloud RDS ListInstances` (official read-only GET `/v3/{project_id}/instances`,
verified in the `huaweicloudsdkrds` v3 client `_list_instances_http_info`
metadata), then render the instance name list as a Markdown table and write it
to a local `.md` file. The skill is aimed at RDS inventory / asset export,
daily operations patrol, handover reports and any "save the instance list as a
Markdown file" request.

Architecture:

```text
agent → python3 scripts/list_rds_export_markdown.py → hcloud RDS ListInstances --cli-region=<region> --limit=N --offset=O
      → Huawei Cloud RDS OpenAPI (regional endpoint) → parsed JSON → Markdown table → local .md file

(hcloud binary missing) → fallback: huaweicloudsdkrds v3 RdsClient.list_instances
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListInstances` (GET).
  A write-intent guard validates the operation name and scans the arguments;
  mutating intents (create / delete / update / resize / restart / stop /
  restore ...) are rejected with an explicit message before any command runs.
  The `.md` file is generated on the **local filesystem only** — no RDS write
  happens and no user confirmation can make this skill issue a write.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  hcloud binary is absent, the script falls back to the official
  `huaweicloudsdkrds` v3 SDK (`list_instances`). Credentials are always read by
  the CLI profile / SDK environment — never handled by the script.
- **Local sorting** — `--sort-by name|created` orders the rows in memory after
  the full (paged) list has been fetched; the ListInstances API has no ordering
  parameter. `name` compares case-insensitively with an id fallback, `created`
  compares parsed timestamps oldest-first (ISO-8601, `Z`/`+0800` offsets and
  space-separated values all accepted). Records whose sort key is missing are
  always placed last, unparseable timestamps fall back to text comparison, and
  the stable sort keeps ties in their original order. Omit `--sort-by` to keep
  the API order unchanged.
- **Empty result is not an error** — an empty instance list (or a filter that
  matches nothing) still produces a valid `.md` file with the table header and
  an explicit "no instances" note, and exits `0`.
- **Atomic local file** — the Markdown body is written to a temporary file and
  renamed into place, so an interrupted write never leaves a corrupt / partial
  file behind.
- **Offline-testable** — every code path (paging, filters, rendering, atomic
  write, error classification, guard, SDK fallback) is covered by unit tests
  that mock the hcloud subprocess.

> **Capability boundary:** this skill lists **instances only** and exports them
> locally; it does not manage the instance lifecycle (create / delete / resize /
> restart / stop / restore backup / change password / read-replica management),
> and it does not export to Excel / PDF / CSV. Those require a separate skill.

> **Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## Differentiation from the plain RDS list skill

The repository keeps a terminal-oriented RDS **instance-list** skill and this
**Markdown-export** skill side by side. They share the same read-only API but
produce different artifacts, and they are **not** runtime dependencies of each
other.

| Dimension | Plain RDS instance-list skill | This export skill |
| --------- | ----------------------------- | ----------------- |
| Deliverable | Terminal output (table / JSON / names-only) | A local Markdown file (default `rds_instances.md`) |
| Persistence | None — printed to stdout only | Atomic file write + automatic parent-directory creation |
| Purpose | Interactive inspection / pre-query an `instance_id` for downstream use | Markdown report export for inventory, patrol, handover |

Per-service "query + export to a file" capabilities are an established
repository convention and are kept as their own skill, separate from the plain
list skill and named by the export format (a sibling compute service exports to
Excel, a sibling storage service exports to Excel/PDF). This skill continues
that convention for RDS with Markdown as the output format. Use the plain RDS
instance-list skill to view instances in the terminal; use this skill when the
instance list must be saved as a distributable / archivable Markdown document.

## Prerequisites

1. **Python 3.8+** — the Markdown export uses only the Python standard library.
   For the hcloud-absent fallback, run `python3 scripts/ensure_env.py` to install
   `huaweicloudsdkcore` / `huaweicloudsdkrds` automatically. See
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
2. **KooCLI (`hcloud`) installed** — the primary path. See
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkrds` to enable the
   SDK fallback path.
3. **KooCLI credentials configured out-of-band** — the script never reads,
   echoes, or stores AK/SK itself; authentication is delegated to the active
   KooCLI profile (CLI path) or the whitelisted environment variables (SDK
   fallback). Never paste AK/SK into chat.
4. **IAM permission** — read-only `rds:instance:list` (or the system policy
   **RDS ReadOnlyAccess**); least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
5. **Outbound HTTPS** access to `rds.<region>.myhuaweicloud.com`.
6. **Write access to the local output directory** (for the generated `.md` file).
- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

1. **(Optional) prepare the environment** — `python3 scripts/ensure_env.py`
   installs `huaweicloudsdkcore` / `huaweicloudsdkrds` if they are missing
   (needed only for the SDK fallback).
2. **Confirm the target region** (default `cn-north-4`); every RDS call is
   region-scoped. Optionally pass `--project_id`.
3. **Confirm KooCLI readiness** (optional, read-only) — the credential check in
   Core Commands.
4. **Run the export script** with the desired output path, optional filters and
   an optional `--sort-by` ordering.
5. **Read the result** — the printed path is the generated Markdown report; open
   that file to see the instance-name table.
6. **Handle the empty / error cases** per the Error Handling table below (an
   empty result still writes the file; credential / permission failures print an
   explicit hint and write nothing).

## Core Commands

> **⚠️ Mandatory: every hcloud command in this skill MUST be wrapped with skill-quality-cli run --skill-name huawei-cloud-rds-export-markdown -- ** — bare hcloud calls are strictly forbidden.**

```bash
# Default: query the region's RDS instances and write rds_instances.md in cwd
python3 scripts/list_rds_export_markdown.py --region cn-north-4

# Explicit output path (recommended) + echo the Markdown to stdout as well
python3 scripts/list_rds_export_markdown.py --region cn-north-4 \
  --output /tmp/rds_instances_cn-north-4.md --stdout

# Name filter (server-side) and status filter (applied client-side)
python3 scripts/list_rds_export_markdown.py --name rds-demo --status ACTIVE \
  --output /tmp/rds_active.md

# Sort by instance name (case-insensitive, id fallback) — applied client-side
python3 scripts/list_rds_export_markdown.py --region cn-north-4 \
  --sort-by name --output /tmp/rds_sorted_by_name.md

# Sort by creation time, oldest first (client-side; missing/unparseable last)
python3 scripts/list_rds_export_markdown.py --region cn-north-4 \
  --sort-by created --output /tmp/rds_sorted_by_created.md

# Filter first, then sort (status filtering runs before the ordering)
python3 scripts/list_rds_export_markdown.py --status ACTIVE --sort-by name \
  --output /tmp/rds_active_sorted.md

# Project-scoped (mapped to the KooCLI global --cli-project-id)
python3 scripts/list_rds_export_markdown.py --project_id <project_id> \
  --output /tmp/rds_project.md

# Read-only credential readiness check (wrapped)
skill-quality-cli run --skill-name huawei-cloud-rds-export-markdown -- hcloud configure list
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
paging; wrap with `skill-quality-cli run` in production):

```bash
skill-quality-cli run --skill-name huawei-cloud-rds-export-markdown -- hcloud RDS ListInstances --cli-region=cn-north-4 --limit=100 --offset=0
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--project_id` / `--project-id` | No | Project id; mapped to the KooCLI global `--cli-project-id` (the SDK path resolves it from credentials + region) | `<project_id>` |
| `--output` / `-o` | No | Markdown output file path (default current dir `rds_instances.md`) | `/tmp/rds.md` |
| `--name` | No | Filter by instance name (server-side ListInstances parameter) | `rds-demo` |
| `--status` | No | Filter by instance state — **applied client-side** (RDS ListInstances has no status API parameter; the full list is fetched, then filtered locally, case-insensitive) | `ACTIVE`, `FAILED`, `BUILDING` |
| `--sort-by` | No | Order the rows — **applied client-side** after the filters (the API has no ordering parameter): `name` = instance name ascending, case-insensitive, `id` fallback; `created` = creation time ascending (oldest first), missing/unparseable values last. Omitted → API order preserved | `name`, `created` |
| `--page-size` | No | Page size for ListInstances (default 100) | `100` |
| `--operation` | No | hcloud RDS operation name; only `ListInstances` is allowed | `ListInstances` |
| `--stdout` | No | Also print the rendered Markdown to stdout (the file is still written) | `--stdout` |

## Markdown Output Format

The generated document has a title, a short metadata line, and a table with the
following columns (fields missing on an instance render as `-`):

| Column (header) | Source key | Notes |
| ---------- | ---------- | --------- |
| 实例名称 | `name` | Instance name (falls back to ID) |
| 实例ID | `id` | Instance ID |
| 状态 | `status` | `ACTIVE` / `FAILED` / `BUILDING` ... |
| 引擎 | `datastore.type` | Flattened engine type |
| 版本 | `datastore.version` | Flattened engine version |
| 规格 | `flavor_ref` | Flavor reference |
| 私网IP | `private_ips` | Comma-joined; `-` when absent |
| 可用区 | `nodes[0].availability_zone` | Primary node AZ |
| 创建时间 | `created` | Creation timestamp |

An empty instance list produces the header + separator followed by a note line
`_当前区域（<x>）无 RDS 实例。_` — the file is always created.

## Write-Intent Guard

- The guard validates the `--operation` value (only the read-only
  `ListInstances` is accepted) and scans the remaining arguments for mutating
  vocabulary (`create`, `delete`, `update`, `modify`, `resize`, `restart`,
  `stop`, `start`, `shutdown`, `restore`, `destroy`, and RDS operation names such
  as `CreateInstance`, `DeleteInstance`, `ResizeFlavor`).
- Values of read-only flags (the local `--output` path, `--region`,
  `--project_id`, `--name`, `--status`, `--sort-by`, ...) are excluded from the
  scan so a file path, a filter value or a sort option is never mistaken for an
  RDS operation. `--sort-by` is in that whitelist on purpose: its value
  `created` contains the mutating keyword `create`, and both `--sort-by created`
  and `--sort-by=created` must pass the guard.
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`,
  and exits with code 1 **before** a single hcloud command is executed. No write
  operation can be constructed by `build_command()`; there is no code path that
  can issue a mutating RDS API call, so no user confirmation path exists — the
  `Create` / `Delete` / `Update` intents are refused outright.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `RDS`.
- **Operation name** — PascalCase: `ListInstances`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete RDS call).
- **Project parameter** — `--cli-project-id=<value>` (global KooCLI option,
  emitted only when `--project_id` is supplied).
- **Simple parameter** — `--key=value`, e.g. `--limit=100`, `--offset=20`,
  `--name=rds-01`, `--datastore_type=MySQL`, `--id=rds-01`. There is **no
  `--status` parameter** on the real RDS ListInstances API (verified via
  `hcloud RDS ListInstances --help`); status filtering is done client-side by
  the script. There is likewise **no ordering parameter** — `--sort-by` is a
  script-side option only and is never sent to hcloud / the SDK.
- **REST path (official SDK `_http_info`)** —
  `GET /v3/{project_id}/instances` (`huaweicloudsdkrds` v3
  `_list_instances_http_info`); project_id is resolved by KooCLI / the SDK from
  the credential profile.

Concrete raw KooCLI command (the script wraps exactly this call; wrap with
`skill-quality-cli run --skill-name huawei-cloud-rds-export-markdown --` in
production):

| Command | Purpose |
| ------- | ------- |
| `hcloud RDS ListInstances --cli-region=cn-north-4 --limit=1` | Read-only instance list used as the Markdown source |

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty instance list / no filter match | Exit 0; the `.md` file is still written (header + `无 RDS 实例` note) |
| Missing / invalid AK-SK | Exit 1, `缺少 AK/SK 凭证` hint to configure hcloud credentials out-of-band (never in chat); no file written |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 RDS，请检查 IAM 权限` hint; no file written |
| hcloud not installed | Falls back to the SDK; if the SDK is unavailable too, exit 1 with a clear hint |
| Bad `--output` path (permission / bad directory) | Exit 1, `Markdown 文件写出失败` hint; no partial file left |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud RDS ListInstances --help` |
| Unknown `--sort-by` value | Exit 1, `--sort-by 仅支持 name 或 created（收到: xxx）`; fails before any API call, no file written |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| Write intent detected | Exit 1, `GuardError` message, no command executed, no file written |

Exit codes: `0` success / empty list; `1` config, auth, guard, export, or API
error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Region has no instances | Header + empty-table note written, exit 0 |
| Many instances | Automatic `offset` paging (total_count aware, full-page fallback, max 100 pages) |
| Filter yields no instance | Empty message includes the active filters; the file is still written |
| Field missing on an instance | Rendered as `-` in the Markdown cell |
| `|` or newline inside a field | Escaped (`\|`) / collapsed to a space so the table stays well-formed |
| `--output` points to a non-existing directory | Directory is created automatically |
| `--output` path contains a guard keyword (e.g. `downloads/update-*.md`) | Path value is excluded from the guard (local path ≠ RDS operation) |
| `--status BUILDING` | Legitimate read filter — the status value is not sent to the server |
| `--sort-by` omitted | Original API order preserved (no reordering, output unchanged) |
| `--sort-by name` with duplicate / mixed-case names | Case-insensitive compare, stable sort keeps ties in the original relative order; records without `name` fall back to `id` |
| `--sort-by created` with missing / unparseable timestamp | Parse failure falls back to text comparison; a missing `created` is always placed last instead of aborting the export |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkrds` list_instances, same Markdown output |
| User asks to create/delete/restart | Out of scope — blocked by the write-intent guard |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
cd skills/database/rds/huawei-cloud-rds-export-markdown
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / mutating verbs /
normalized separators / operation whitelist / read-only value scrubbing including
`--sort-by created` and `--flag=value` forms), command construction
(`--cli-region` / limit / offset / name / `--cli-project-id`, no write flags / no
status / no ordering), JSON extraction and instance extraction, failure
classification (missing AK/SK, 403, generic, `[USE_ERROR]` with rc=0), offset
paging (total / full page / empty), client-side status filtering, local sorting
(`--sort-by name` case-insensitive + id fallback + missing last, `--sort-by
created` mixed timestamp formats + text fallback + missing last + stable ties,
no-argument order preservation, unknown value), SDK fallback (env credentials /
missing credentials / unavailable), normalization, Markdown rendering (title /
header / rows / empty-result note / pipe & newline escaping), atomic file writing
(missing dirs / bad path), and all `main()` output modes (including the sorted
row order and the fail-fast exit 1 for an unknown `--sort-by`).

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI + SDK installation, credential configuration and skill-quality-cli |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
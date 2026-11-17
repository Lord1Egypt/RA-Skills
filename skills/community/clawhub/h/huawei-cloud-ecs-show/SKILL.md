---
name: huawei-cloud-ecs-show
description: |
  1. Show the full detail of one Huawei Cloud ECS (Elastic Cloud Server)
     instance by its instance ID through KooCLI (hcloud ECS ShowServer —
     read-only GET /v1/{project_id}/cloudservers/{server_id}), with an automatic
     fallback to the official huaweicloudsdkecs v2 SDK when hcloud is not
     installed.
  2. Input: a single --instance-id (required); region override (--region,
     default cn-north-4) and an optional --project-id (SDK fallback path).
  3. Output modes: key/detail block (default) covering ID / 名称 / 状态 /
     规格(flavor) / 镜像 / 私网+公网 IP / 可用区 / 创建时间 / 标签, --json
     (raw server object) on stdout, and --md-file <path> to export the same key
     fields as a Markdown document to a local file. Without --md-file all output
     goes to stdout only — the script writes no file.
  4. Explicit error hints for a missing / malformed instance ID (「实例 ID 不能
     为空」), a non-existent ID (「未找到该 ECS 实例」, 404), 403 / insufficient
     IAM permission (「无权限访问 ECS，请检查 IAM 权限」), and missing or invalid
     AK/SK credentials.
  5. Built-in write-intent guard: any mutating intent (create / delete / update /
     rebuild / resize / reboot / start / stop / attach / detach) or any operation
     other than ShowServer is rejected before execution — this skill is strictly
     read-only.
  6. Triggers include: "show ECS instance", "ECS instance detail", "query ECS by
     id", "ECS 实例详情", "根据ID查询ECS", "查询云服务器详情", "ECS 详情",
     "查看ECS实例", "云服务器详情", "华为云 ECS 详情".
  7. Offline unit tests (mocked hcloud subprocess) cover detail / JSON output,
     Markdown export, error scenarios, SDK fallback, the write-intent guard, and
     instance-ID validation.
tags: [huawei-cloud, ecs, compute, readonly, koo-cli]
---

# Huawei Cloud ECS Instance Detail (Show)

## Overview

Query the full detail of a **single** ECS instance by its instance ID through
KooCLI `hcloud ECS ShowServer --cli-region=<region> --server_id=<id>` (official
read-only GET `/v1/{project_id}/cloudservers/{server_id}`, verified in the
`huaweicloudsdkecs` v2 client `_show_server_http_info` metadata). The skill is
aimed at instance-level inspection, troubleshooting, and as a pre-query step for
other ECS workflows that need a specific server's attributes.

Architecture:

```text
agent → python3 scripts/show_ecs.py --instance-id <server_id> [--md-file <path>]
      → hcloud ECS ShowServer --cli-region=<region> --server_id=<id>
      → Huawei Cloud ECS OpenAPI (regional endpoint) → parsed JSON
      → detail block / --json (stdout) | --md-file (Markdown written to a local file)

(hcloud binary missing) → fallback: huaweicloudsdkecs v2 EcsClient.show_server
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ShowServer` (GET). A
  write-intent guard scans the user arguments and validates the operation name;
  mutating intents (create / delete / update / rebuild / resize / reboot / start
  / stop / attach / detach ...) are rejected with an explicit message before any
  command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  hcloud binary is absent, the script falls back to the official
  `huaweicloudsdkecs` v2 SDK (`show_server`). Credentials are always read by the
  CLI profile / SDK environment — never handled by the script.
- **Instance-level detail output** — ID / 名称 / 状态 / 规格 / 镜像 / 私网+公网
  IP / 可用区 / 创建时间 / 标签 are rendered explicitly (missing fields show
  `-`); `--json` returns the raw server object.
- **Optional Markdown export** — `--md-file <path>` renders the same key fields
  as a Markdown document and writes it to the given local file (existing file is
  overwritten); a short confirmation is printed to stdout. This is the only code
  path that writes a file.
- **Stdout by default** — without `--md-file` the script prints to stdout in
  every mode; it creates no file.
- **Offline-testable** — every code path (validation, error classification,
  guard, SDK fallback, rendering, Markdown export) is covered by unit tests that
  mock the hcloud subprocess.

Out of scope: listing instances (use a list skill), cloud-side export jobs
(OBS/镜像导出等), and every mutating ECS action (create / delete / start / stop /
restart / resize flavor / rebuild / attach-detach volume / change image / change
password). Those require a dedicated write-capable skill and explicit user
confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkecs` to enable the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (`hcloud configure` in your terminal, or credential environment variables).
   Never paste AK/SK into chat; the script never reads, echoes, or stores
   secrets itself — authentication is delegated entirely to the hcloud profile
   / SDK environment.
3. **IAM permission** — read-only `ecs:cloudServers:get` (aka `ecs:servers:get`);
   least-privilege policy in [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess).
5. **Outbound HTTPS** access to `*.myhuaweicloud.com`.

## Workflow

1. **Confirm the target instance ID** (`--instance-id`, required) and the
   region (default `cn-north-4`); every ECS call is region-scoped.
2. **Confirm hcloud readiness** (optional, read-only): `hcloud configure list`.
3. **Run the show script** with the instance ID and the desired output mode.
4. **Read the result** — the key/detail block for humans, `--json` for
   downstream tooling, or `--md-file <path>` to write a Markdown document.
   Without `--md-file` output is printed to stdout only; the script writes no
   file.
5. **Handle the error cases** per the Error Handling table below (the script
   prints an explicit hint for a missing ID, a 404, 403, and missing AK/SK).

## Core Commands

```bash
# Key/detail block (default)
python3 scripts/show_ecs.py --instance-id 8f7c1d6a-0e2b-4a01-9c11-abcdef012345

# Raw JSON of the server object
python3 scripts/show_ecs.py --instance-id 8f7c1d6a-0e2b-4a01-9c11-abcdef012345 --json

# Export the instance detail as a Markdown document
python3 scripts/show_ecs.py --instance-id 8f7c1d6a-0e2b-4a01-9c11-abcdef012345 \
    --md-file ./ecs-detail.md

# Override the region
python3 scripts/show_ecs.py --instance-id 8f7c1d6a-0e2b-4a01-9c11-abcdef012345 --region cn-south-1

# Optional project id (SDK fallback path)
python3 scripts/show_ecs.py --instance-id 8f7c1d6a-0e2b-4a01-9c11-abcdef012345 --project-id 0a1b2c3d4e5f
```

Equivalent direct KooCLI call (the script wraps exactly this operation):

```text
hcloud ECS ShowServer --cli-region=cn-north-4 --server_id=8f7c1d6a-0e2b-4a01-9c11-abcdef012345
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--instance-id` / `--server-id` | Yes | ECS instance ID to query | `8f7c1d6a-...` |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--project-id` | No | Project ID (optional; used by the SDK fallback path only) | `0a1b2c3d4e5f` |
| `--json` | No | Output the raw server object as JSON | — |
| `--md-file` / `--output-md` | No | Export the instance detail as a Markdown document to this local file path (optional; an existing file is overwritten) | `./ecs-detail.md` |
| `--operation` | No | hcloud ECS operation name; only `ShowServer` is allowed | `ShowServer` |

Output-mode precedence: `--md-file` → `--json` → detail block (default). When
`--md-file` is given it wins over `--json`: the Markdown file is written and a
short confirmation is printed to stdout. Without `--md-file` the rendered result
is printed to stdout; the script writes no file.

## Write-Intent Guard

- The script scans flag names plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `rebuild`, `resize`, `reboot`,
  `start`, `stop`, `attach`, `detach`, `server-action`, and ECS operation names
  such as `CreateServers`, `DeleteServers`, `BatchStartServers`).
- The values of read-only data flags (`--region`, `--instance-id`,
  `--project-id`, `--md-file`) are **not** scanned: they are query/export data and
  may legitimately contain write-looking words (e.g. an instance named `stop-me`
  or a path such as `/tmp/create-delete-report.md`).
- A flag following such a data flag is still scanned — `--instance-id
  --create-server` cannot hide a mutating flag.
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed. The guard
  runs on the raw argv *before* argparse, so a mutating flag such as
  `--create-server` is reported as a guard violation rather than an
  "unrecognized argument" error.
- Only `hcloud ECS ShowServer` (GET) — or the SDK `show_server` call in the
  fallback path — is ever constructed by `build_command()`; there is no code
  path that can issue a mutating ECS API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `ECS`.
- **Operation name** — PascalCase: `ShowServer`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete ECS call).
- **Simple parameter** — `--key=value`, e.g. `--server_id=8f7c1d6a-...`
  (the single ShowServer operation parameter).
- **REST path (official SDK `_http_info`)** —
  `GET /v1/{project_id}/cloudservers/{server_id}` (`huaweicloudsdkecs` v2
  `_show_server_http_info`); project_id is resolved by KooCLI from the
  credential profile (or passed to `BasicCredentials` on the SDK fallback path).

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Missing / empty `--instance-id` | argparse requires it; a blank value → exit 1 with `实例 ID 不能为空` hint |
| Non-existent / invalid instance ID | Exit 1, `未找到该 ECS 实例` (404) hint incl. ID and region |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 ECS，请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkecs` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| `--md-file` path invalid / unwritable | Exit 1 with an explicit hint (导出路径不能为空 / 上级目录不存在 / 导出路径是一个目录 / 导出路径不可写), the file is not written |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud ECS ShowServer --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success; `1` validation, config, auth, guard, 404, export-path, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| `SHUTOFF` / `ERROR` instances | Returned with their state, not treated as failure |
| Field missing on the instance | Rendered as `-` in the detail block |
| Nested `flavor` / `addresses` / `image` | Flattened into name/vcpus/ram / privateIps+publicIps / image_id |
| Extra response fields | Detail block appends an "其他字段" section so new fields appear automatically |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| Empty / payload without `server` | `NotFoundError` with the ID and region |
| `--md-file` target already exists | Overwritten (documented); pass a fresh path to keep the old file |
| Field value contains `|` or a newline | Escaped (`\|` / `<br>`) so the Markdown table stays well-formed |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkecs` `show_server`, same output modes |
| User asks to create/delete/start/stop/rebuild | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / rebuild / resize /
reboot / start / stop / attach / operation whitelist / data values not blocked /
a flag after a data flag still scanned / `--md-file` path value not scanned),
instance-ID validation (empty / whitespace), command construction (`--server_id`
is the real ShowServer parameter), JSON extraction (nested / flat / absent
`server`), failure classification (missing AK/SK, 403, 404, generic,
`[USE_ERROR]` with rc=0), single-call show path, SDK fallback (success and
unavailable; request construction matches the real `ShowServerRequest`
signature), SDK field remapping (`access_i_pv4` → `accessIPv4`,
`os_ext_a_zavailability_zone` → `OS-EXT-AZ:availability_zone`), rendering
(detail block with flavor/IP/AZ/tags fields), Markdown export (key fields, IPs,
region line, missing fields, `|` escaping, extra-fields section, SDK-object
safety, write success / overwrite / invalid path errors), SDK object
serialization safety, and all main() output / error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
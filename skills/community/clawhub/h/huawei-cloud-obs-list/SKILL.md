---
name: huawei-cloud-obs-list
description: |
  1. List the OBS (Object Storage Service) buckets of a Huawei Cloud account
     through the KooCLI obsutil-backed OBS module (`hcloud OBS ls`, the
     read-only ListBuckets operation), with an automatic fallback to the
     official huaweicloudsdkobs v1 SDK (`ObsClient.list_buckets`) when hcloud is
     not installed.
  2. Three output modes: aligned table (default, bucket name / creation date /
     region / storage class), `--output json` / `--json` (structured array for
     downstream tooling), and `--names-only` (compact bucket-name list).
  3. Region-aware: `--region` (default cn-north-4) selects the OBS endpoint;
     optional `--endpoint` overrides it. `--page-size` caps the returned count.
  4. Explicit error classification: missing AK/SK credentials (「缺少 AK/SK
     凭证」), hcloud not installed (falls back to SDK, else a clear hint),
     invalid/insufficient credentials (403 / InvalidAccessKeyId → IAM hint), and
     generic API/network failures.
  5. Built-in write-intent guard: any mutating intent (create / delete / upload
     / download / copy / remove / restore / sync / modify …) or any operation
     other than the read-only `ls` is rejected before execution — this skill is
     strictly read-only.
  6. Triggers include: "list OBS buckets", "OBS bucket list", "OBS 桶列表",
     "查询OBS桶", "对象存储桶列表", "列出桶", "桶清单", "bucket inventory",
     "OBS inventory".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, parsing,
     empty lists, error classification, SDK fallback, and the write-intent guard.
tags: [huawei-cloud, obs, storage, readonly, koo-cli]
---

# Huawei Cloud OBS Bucket List

## Overview

Query the OBS bucket list of a Huawei Cloud account through KooCLI's
obsutil-backed OBS module (`hcloud OBS ls` — the read-only ListBuckets
operation), with a fallback to the official `huaweicloudsdkobs` v1 SDK. The
skill is aimed at resource inventory, daily operations patrol, and as a
pre-query step for automation that needs a bucket name.

Architecture:

```text
agent → python3 scripts/list_obs_buckets.py → hcloud OBS ls [-limit=N] [-e=obs.<region>.myhuaweicloud.com]
      → Huawei Cloud OBS OpenAPI (ListBuckets) → parsed buckets → table / json / names

(hcloud binary missing) → fallback: huaweicloudsdkobs v1 ObsClient.list_buckets
```

Key properties:

- **Read-only by design** — the only API ever invoked is ListBuckets (GET). A
  write-intent guard scans user arguments and validates the operation name;
  mutating intents (create / delete / upload / download / copy / remove /
  restore / sync ...) are rejected with an explicit message before any command
  runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  hcloud binary is absent, the script falls back to the official
  `huaweicloudsdkobs` SDK (`list_buckets`). Credentials are read from the
  hcloud/obsutil profile or the SDK environment — never handled by the script.
- **Account-level query** — OBS bucket listing is account-scoped; `--region`
  selects the OBS endpoint used for the call.
- **Offline-testable** — every code path (parsing, output modes, error
  classification, guard, SDK fallback) is covered by unit tests that mock the
  hcloud subprocess.

> **Capability boundary:** this skill lists **buckets only**. It does not list
> objects inside a bucket, and it does not report bucket quota/usage. Those
> require a separate skill/Issue.

Out of scope: every mutating OBS action (bucket create/delete, object
upload/download/copy/delete, ACL/policy/encryption/lifecycle changes). Those
require a dedicated write-capable skill and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed with the obsutil component** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkobs` to enable the
   SDK fallback path.
2. **obsutil credentials configured out-of-band** — the `hcloud OBS` module
   reads AK/SK/endpoint from the obsutil config file (`~/.obsutilconfig`),
   separate from the KooCLI account profile. Never paste AK/SK into chat; the
   script never reads, echoes, or stores secrets itself.
3. **IAM permission** — read-only `obs:bucket:list` (or the `OBS ReadOnlyAccess`
   system policy); least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess / re).
5. **Outbound HTTPS** access to `obs.<region>.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`); it selects the OBS
   endpoint.
2. **Confirm hcloud/obsutil readiness** (optional, read-only):
   `hcloud OBS ls -limit=1` (or `hcloud version`).
3. **Run the list script** with the desired output mode.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact inventory.
5. **Handle the empty / error cases** per the Error Handling table below.

## Core Commands

```bash
# Aligned table (default): name / creation date / region / storage class
python3 scripts/list_obs_buckets.py --region cn-north-4

# Structured JSON (raw bucket array) for downstream tooling
python3 scripts/list_obs_buckets.py --output json
# or the alias
python3 scripts/list_obs_buckets.py --json

# Compact bucket-name list only
python3 scripts/list_obs_buckets.py --names-only

# Custom endpoint / capped count
python3 scripts/list_obs_buckets.py --region cn-south-1 --page-size 50
```

Equivalent direct KooCLI command (the script wraps exactly this call):

```bash
hcloud OBS ls -limit=1000 -e=obs.cn-north-4.myhuaweicloud.com
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`); selects the OBS endpoint | `cn-south-1` |
| `--output` / `-o` | No | Output mode: `table` (default) / `json` / `names` | `--output json` |
| `--json` | No | Alias for `--output json` | — |
| `--names-only` | No | Alias for `--output names` (bucket names only) | — |
| `--page-size` | No | Maximum number of buckets to return (default 1000) | `50` |
| `--endpoint` | No | Override the OBS endpoint (default `obs.<region>.myhuaweicloud.com`) | `obs.custom.example.com` |
| `--operation` | No | hcloud OBS operation name; only the read-only `ls` is allowed | `ls` |

Output-mode precedence: `--names-only` → `--json` → `--output` → table (default).

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `upload`, `download`, `copy`, `remove`,
  `move`, `restore`, `abort`, `sync`, `modify`, `update`, `overwrite`, and OBS
  operation names such as `CreateBucket`, `DeleteBucket`, `PutObject`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed.
- Only `hcloud OBS ls` (read-only ListBuckets) — or the SDK `list_buckets` call
  in the fallback path — is ever constructed by `build_command()`; there is no
  code path that can issue a mutating OBS API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `OBS`.
- **Operation name** — the `hcloud OBS` module is **obsutil-backed**: operations
  are lowercase obsutil commands, not PascalCase API names. Listing the account
  buckets is `ls` with **no** `cloud_url`; there is **no** `hcloud OBS
  ListBuckets` command.
- **Region / endpoint** — the OBS module does **not** accept `--cli-region`;
  the region is expressed through the endpoint option `-e=obs.<region>.myhuaweicloud.com`
  (the script derives it from `--region`).
- **Simple parameter** — `-key=value`, e.g. `-limit=1000`, `-e=obs.cn-north-4.myhuaweicloud.com`.
- **REST path (official SDK)** — `GET /` (`ListBuckets`), invoked by
  `huaweicloudsdkobs` v1 `ObsClient.list_buckets`; the endpoint is resolved from
  the requested region.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty bucket list | Exit 0, prints `当前账号（Region <x>）无 OBS 桶。` |
| Missing AK/SK / obsutil config | Exit 1, `缺少 AK/SK 凭证` hint to run `hcloud obs config` out-of-band (never in chat) |
| Invalid / insufficient credentials (403 / InvalidAccessKeyId) | Exit 1, `无权限访问 OBS，请检查 IAM 权限` hint |
| hcloud not installed | Exit 1 after SDK fallback also unavailable; hint to install KooCLI or `pip install huaweicloudsdkcore huaweicloudsdkobs` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud OBS ls --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty list; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Account has no buckets | Friendly `无 OBS 桶` message, exit 0 (not an error) |
| Large number of buckets | `-limit` caps the CLI result; `--page-size` controls it (default 1000) |
| Extra obsutil columns (`-sc` etc.) | Creation date / region detected heuristically and added to the record |
| Duplicate `obs://` lines | Collapsed to the first occurrence per bucket name |
| Field missing on a bucket | Rendered as `-` in the table |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkobs` list_buckets, same output modes |
| User asks to create/delete/upload | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / upload / download /
copy / remove / restore / sync / normalized variants / operation whitelist),
command construction (endpoint + limit, no write flags), obsutil output parsing
(names / columns / dedupe / empty), failure classification (missing AK/SK,
InvalidAccessKeyId, 403, generic, `[USE_ERROR]`), SDK fallback (missing env
credentials, success, unavailable, bucket normalization), rendering (table /
names / minimal), and all `main()` output modes including empty, filter, and
error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI + obsutil installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
---
name: huawei-cloud-obs-statistics
description: |
  1. Read-only aggregated statistics for Huawei Cloud OBS (Object Storage
     Service): for a target scope (all buckets, or one bucket, optionally
     narrowed by a key prefix) it reports, in one shot, the bucket count, the
     object count, the total capacity (sum of object Size, bytes — an estimate,
     not a billing figure), the distribution by storage class, and the
     distribution by region.
  2. Primary execution path is the KooCLI obsutil-backed OBS module
     (`hcloud OBS ls`), with an automatic fallback to the official
     `huaweicloudsdkobs` v1 SDK (`ObsClient.list_buckets` / `list_objects`) when
     hcloud is not installed.
  3. Three output modes: an aligned table (default), structured JSON
     (`--json` / `--output json`) for downstream automation, and Markdown
     (`--output md`).
  4. Scope controls: `--bucket` (single bucket), `--prefix` (limit the scan),
     `--region` (default cn-north-4), `--max-objects` (cap, truncated results
     are marked).
  5. Built-in write-intent guard: any mutating intent (create / delete / upload
     / download / copy / remove / restore / sync / modify …) or any operation
     other than the read-only `ls` is rejected before execution — this skill is
     strictly read-only.
  6. Triggers include: "OBS 统计", "OBS 聚合统计", "OBS 容量统计", "对象数量统计",
     "存储类别分布", "区域分布", "桶统计", "资源巡检", "容量盘点",
     "OBS statistics", "bucket usage stats", "obs statistics summary".
  7. Offline unit tests (mocked hcloud subprocess and SDK) cover output modes,
     parsing, aggregation, empty scopes, error classification, SDK fallback and
     the write-intent guard.
tags: [huawei-cloud, obs, storage, statistics, readonly]
---

# Huawei Cloud OBS Statistics

## Overview

Produce a one-shot **read-only aggregated statistics report** for Huawei Cloud
OBS (Object Storage Service). Given a scope — the whole account, a single
bucket, and/or a key prefix — the skill enumerates buckets and objects and
aggregates the results locally, reporting:

- **bucket count**
- **object count**
- **total capacity** — the sum of object `Size` (bytes), an *estimate*, not a
  billing figure
- **distribution by storage class** (Standard / Warm / Cold / Deep Archive …)
- **distribution by region**

Primary execution path is the KooCLI obsutil-backed OBS module
(`hcloud OBS ls` — the read-only ListBuckets / ListObjects operations); when the
hcloud binary is absent the script falls back to the official
`huaweicloudsdkobs` v1 SDK (`ObsClient.list_buckets` / `list_objects`).

Architecture:

```text
agent → python3 scripts/collect_obs_stats.py
      → hcloud OBS ls [-limit=N] [-e=obs.<region>.myhuaweicloud.com]      (buckets)
      → hcloud OBS ls obs://<bucket>/[<prefix>/] [-limit=N] [-e=...]      (objects)
      → local aggregation → table / json / md

(hcloud binary missing) → fallback: huaweicloudsdkobs v1
                          ObsClient.list_buckets / list_objects
```

> **Capability boundary:** this skill **aggregates** objects/buckets into
> summary metrics. It does not export per-object inventories and does not
> count directories/folders. Capacity is estimated from object `Size`, not a
> billing statement.

Out of scope: every mutating OBS action (bucket create/delete, object
upload/download/copy/delete, ACL/policy/encryption/lifecycle changes) — these
are blocked by the write-intent guard; a write-capable skill with explicit user
confirmation would be required.

## Prerequisites

1. **KooCLI (`hcloud`) installed with the obsutil component** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkobs` to enable the
   SDK fallback path (or run `scripts/ensure_env.py`).
2. **obsutil credentials configured out-of-band** — the `hcloud OBS` module
   reads AK/SK/endpoint from the obsutil config file (`~/.obsutilconfig`),
   separate from the KooCLI account profile. Never paste AK/SK into chat; the
   script never reads, echoes, or stores secrets itself.
3. **IAM permission** — read-only `obs:bucket:ListBucket`, `obs:object:List`
   (or the `OBS ReadOnlyAccess` system policy); least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess / re).
5. **Outbound HTTPS** access to `obs.<region>.myhuaweicloud.com`.

## Workflow

1. **Confirm the scope** — a single `--bucket` (recommended for large accounts)
   or the whole account; optionally a `--prefix` to limit the object scan.
2. **Confirm hcloud/obsutil readiness** (optional, read-only):
   `hcloud OBS ls -limit=1`.
3. **Run the script** with the desired output mode:
   `python3 scripts/collect_obs_stats.py --bucket <bucket> --prefix <prefix>`.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--output md` for a Markdown report.
5. **Handle errors** per the Error Handling table below.

## Core Commands

```bash
# Whole account: aggregate every bucket (table output)
python3 scripts/collect_obs_stats.py --region cn-north-4

# Single bucket, narrowed by prefix
python3 scripts/collect_obs_stats.py --bucket my-bucket --prefix logs/

# Structured JSON (for downstream automation)
python3 scripts/collect_obs_stats.py --bucket my-bucket --json

# Markdown report
python3 scripts/collect_obs_stats.py --bucket my-bucket --output md

# Force the SDK fallback path
python3 scripts/collect_obs_stats.py --bucket my-bucket --executor sdk
```

Equivalent direct KooCLI commands (the script wraps exactly these calls):

```bash
hcloud OBS ls -limit=1000 -e=obs.cn-north-4.myhuaweicloud.com
hcloud OBS ls obs://my-bucket/logs/ -limit=1000 -e=obs.cn-north-4.myhuaweicloud.com
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--bucket` / `-b` | No | Statistics scope: one bucket (default: all account buckets) | `my-bucket` |
| `--prefix` / `-p` | No | Limit the object scan to a key prefix | `logs/` |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`); selects the OBS endpoint | `cn-south-1` |
| `--output` / `-o` | No | Output mode: `table` (default) / `json` / `md` | `--output json` |
| `--json` | No | Alias for `--output json` | — |
| `--md` | No | Alias for `--output md` | — |
| `--executor` | No | `auto` (default, CLI first) / `cli` / `sdk` | `--executor sdk` |
| `--max-objects` | No | Per-bucket object cap (default 100000); results are marked truncated when reached | `50000` |
| `--endpoint` | No | Override the OBS endpoint (default `obs.<region>.myhuaweicloud.com`) | `obs.custom.example.com` |
| `--operation` | No | hcloud OBS operation name; only the read-only `ls` is allowed | `ls` |

Output-mode precedence: `--md` → `--json` → `--output` → table (default).

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `upload`, `download`, `copy`, `remove`,
  `move`, `restore`, `abort`, `sync`, `modify`, `update`, `overwrite`, and OBS
  operation names such as `CreateBucket`, `DeleteBucket`, `PutObject`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`,
  and exits with code 1 **before** a single hcloud command is executed.
- Only `hcloud OBS ls` (read-only ListBuckets / ListObjects) — or the SDK
  `list_buckets` / `list_objects` calls in the fallback path — is ever
  constructed; there is no code path that can issue a mutating OBS API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `OBS`.
- **Operation name** — the `hcloud OBS` module is **obsutil-backed**: operations
  are lowercase obsutil commands, not PascalCase API names. Listing account
  buckets is `ls` with **no** `cloud_url`; listing objects is `ls` with a
  `cloud_url` of the form `obs://<bucket>/[<prefix>/]`. There is **no** `hcloud
  OBS ListBuckets` / `ListObjectsV2` command.
- **Region / endpoint** — the OBS module does **not** accept `--cli-region`;
  the region is expressed through the endpoint option
  `-e=obs.<region>.myhuaweicloud.com` (the script derives it from `--region`).
- **Simple parameter** — `-key=value`, e.g. `-limit=1000`,
  `-e=obs.cn-north-4.myhuaweicloud.com`.
- **REST paths (official SDK)** — `GET /` (ListBuckets) and
  `GET /?prefix=&marker=&max-keys=` (ListObjects), invoked by
  `huaweicloudsdkobs` v1; the endpoint is resolved from the requested region.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty scope (no buckets / no objects) | Exit 0, zeroed summary with a friendly table |
| Missing AK/SK / obsutil config | Exit 1, `缺少 AK/SK 凭证` hint to run `hcloud obs config` out-of-band (never in chat) |
| Invalid / insufficient credentials (403 / InvalidAccessKeyId) | Exit 1, `无权限访问 OBS，请检查 IAM 权限` hint |
| hcloud not installed | SDK fallback; if the SDK is also unavailable, exit 1 with an install hint |
| Network / API failure | Exit 1 with the hcloud/SDK error excerpt |
| KooCLI usage error (`[USE_ERROR] ...`) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud OBS ls --help` |
| Object cap reached (`--max-objects`) | Exit 0, `truncated=true`, note that totals are a lower bound |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success (including empty scopes); `1` config, auth, guard, or
API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Account has no buckets | Zeroed report, exit 0 (not an error) |
| Large objects / many objects | `--prefix` narrows the scan; `--max-objects` caps it and sets `truncated=true` |
| `obsutil ls` returns no bucket region | Region distribution is merged under the requested `--region`, with an explicit warning |
| Storage class absent on an object | Treated as `STANDARD` |
| hcloud absent, SDK installed | Transparent fallback, same output modes |
| User asks to create/delete/upload | Out of scope — blocked by the write-intent guard |

## Testing

Offline unit tests (mocked hcloud subprocess and SDK; no credentials, no
network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard, command construction, obsutil bucket/object
parsing, storage-class normalization, failure classification, aggregation
(bucket/object/size/storage-class/region distributions, empty scope), SDK
pagination and truncation, SDK fallback wiring, rendering (table / Markdown)
and all `main()` output modes.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI + obsutil installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
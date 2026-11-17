---
name: huawei-cloud-cdn-export-obs
description: |
  1. Query the Huawei Cloud CDN (Content Delivery Network) accelerated-domain
     list of a tenant through KooCLI (`hcloud CDN ListDomains`, the official
     read-only GET /v1.0/cdn/domains), with an automatic fallback to the
     official huaweicloudsdkcdn v1 SDK (CdnClient.list_domains) when hcloud is
     not installed.
  2. Serialize the result into a local file — `--format json` (raw array,
     default) / `csv` (RFC-4180 flat table) / `md` (Markdown table whose first
     column is 域名) — written atomically (temp file + rename).
  3. Upload the result file to a user-specified OBS bucket + object key through
     KooCLI's obsutil-backed OBS module (`hcloud OBS cp`), with a fallback to the
     official huaweicloudsdkobs v1 SDK (ObsClient.put_object) when hcloud is
     absent.
  4. Read-back verification by default: after upload the object metadata is
     re-read (`hcloud OBS stat` / ObsClient.head_object) and its size compared
     with the local file.
  5. Overwrite protection by default: an already-existing target object is
     refused (exit 1) unless the user explicitly passes `--overwrite`.
  6. Explicit error classification: empty domain list is not an error;
     missing AK/SK, no permission (403), hcloud missing, KooCLI usage errors,
     bad local output path, and already-existing object are each reported with a
     dedicated hint. A write-intent guard rejects any mutating CDN operation
     (create / delete / update / enable / disable / refresh / preheat ...).
  7. Triggers include: "CDN 列表导出 OBS", "CDN 域名列表上传 OBS", "查询 CDN 并上传 OBS",
     "CDN 盘点归档到 OBS", "导出 CDN 加速域名到对象存储", "cdn list export obs",
     "upload CDN domains to OBS", "archive CDN domains", "华为云 CDN 列表导出".
  8. Offline unit tests (mocked hcloud subprocess) cover the CDN query, paging,
     serialization (json/csv/md), OBS upload, overwrite protection, read-back
     verification, error classification, SDK fallback, and the write-intent guard.
tags: [huawei-cloud, cdn, obs, network, export]
---

# Huawei Cloud CDN List → Local Export → OBS Upload

## Overview

Query the CDN accelerated-domain list of a tenant through KooCLI
`hcloud CDN ListDomains` (official read-only GET `/v1.0/cdn/domains`, verified in
the `huaweicloudsdkcdn` v1 client `_list_domains_http_info` metadata), serialize
it to a local file, and upload that file to a user-specified OBS bucket/object
key. The skill is aimed at CDN inventory archiving, daily operations patrol, and
retaining an auditable snapshot of accelerated domains in object storage.

Architecture:

```text
agent → python3 scripts/cdn_export_obs.py --bucket <b> --key <k>
      → list_cdn.list_domains ...        hcloud CDN ListDomains --cli-region=<region>
      → export_results.export ...        local json / csv / md (atomic write)
      → upload_obs.upload_file ...       hcloud OBS cp  <local> obs://<bucket>/<key>
            → upload_obs.verify_object   hcloud OBS stat obs://<bucket>/<key>

(hcloud missing) → CDN: huaweicloudsdkcdn v1 CdnClient.list_domains
                 → OBS: huaweicloudsdkobs v1 ObsClient.put_object / .head_object
(missing SDK)    → run scripts/ensure_env.py  (auto pip install)
```

Key properties:

- **CDN side is read-only; the only write is the single OBS object upload.** A
  write-intent guard scans the CDN arguments and validates the operation name;
  mutating CDN intents (create / delete / update / enable / disable / refresh /
  preheat ...) are rejected before any command runs. On the OBS side, only `cp`
  (upload) and `stat`/`ls` (existence / read-back) are allowed — bucket
  create/delete, object delete/copy/move, ACL/policy changes are refused.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  hcloud binary is absent the script falls back to the official SDKs. Credentials
  are read from the hcloud / obsutil profile or the SDK environment — never
  handled by the script.
- **Overwrite protection by default** — the target object is probed with a
  read-only `stat` before the upload; if it exists and the user did not pass
  `--overwrite`, the upload is refused and no write happens.
- **Read-back verification by default** — the uploaded object is re-read and its
  size compared with the local file (`--no-verify` to skip).
- **Offline-testable** — every code path (query, paging, serialization, upload,
  overwrite protection, verification, error classification, guard, SDK fallback)
  is covered by unit tests that mock the hcloud subprocess.

**Capability boundary:** this skill does not manage CDN lifecycle (create /
delete / enable / disable a domain, origin or config changes, refresh / preheat
tasks) and does not manage OBS buckets or other objects (create/delete a bucket,
delete/copy/move an object, ACL/policy/lifecycle). Those require a dedicated
write-capable skill and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed with the obsutil component** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   The CDN query uses the KooCLI CDN service; the upload uses the obsutil-backed
   OBS module. Alternative: `pip install huaweicloudsdkcore huaweicloudsdkcdn
   huaweicloudsdkobs` to enable the SDK fallback paths.
2. **Credentials configured out-of-band** — the CDN CLI path reads the active
   hcloud profile; the OBS module reads AK/SK/endpoint from the obsutil config;
   the SDK fallbacks read AK/SK from whitelisted environment variables. Never
   paste AK/SK into chat; the script never reads, echoes or stores secrets.
3. **IAM permission** — read-only `cdn:domain:list` for the query **and**
   `obs:object:put` (plus `obs:object:get` metadata) for the upload/read-back;
   least-privilege policy in [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / csv / subprocess /
   os). The SDK fallback needs the official SDKs (install via `ensure_env.py`).
5. **Outbound HTTPS** access to `cdn.myhuaweicloud.com` and
   `obs.<region>.myhuaweicloud.com`.

## Workflow

1. **(Optional) prepare the environment** —
   `python3 scripts/ensure_env.py` installs any missing SDK dependency.
2. **Confirm the target region** (default `cn-north-4`) and the local export
   format (`--format json|csv|md`).
3. **Confirm the OBS target** — a bucket name (`--bucket`) is required for the
   upload step; `--key` defaults to the export file name. If no bucket is given,
   the skill only exports locally.
4. **Run the entry script** with optional CDN filters.
5. **Confirm before overwriting** — by default an already-existing target object
   is refused; the user must explicitly pass `--overwrite` to replace it.
6. **Read the result** — the local file path, the object URL, and the read-back
   verification outcome are printed (or `--json` for tooling).
7. **Handle the empty / error cases** per the Error Handling table below.

## Core Commands

```bash
# Default: query the region's CDN domains, export JSON, upload to OBS (no overwrite)
python3 scripts/cdn_export_obs.py --region cn-north-4 \
  --bucket my-bucket --key inventory/cdn_domains.json

# Markdown report with a summary line
python3 scripts/cdn_export_obs.py --region cn-north-4 --format md --summary \
  --bucket my-bucket --key inventory/cdn_domains.md

# CSV export
python3 scripts/cdn_export_obs.py --format csv \
  --bucket my-bucket --key inventory/cdn_domains.csv

# Explicit local output path + allow overwriting an existing object
python3 scripts/cdn_export_obs.py --output /tmp/cdn_domains.md --format md \
  --bucket my-bucket --key inventory/cdn_domains.md --overwrite

# Export locally only (no OBS upload)
python3 scripts/cdn_export_obs.py --export-only --format md --output /tmp/cdn.md

# Server-side CDN filters
python3 scripts/cdn_export_obs.py --domain-status online --business-type web \
  --bucket my-bucket --key inventory/online_web.json

# Machine-readable run result
python3 scripts/cdn_export_obs.py --bucket my-bucket --key k.json --json
```

Equivalent direct KooCLI commands (the script wraps exactly these calls):

```bash
hcloud CDN ListDomains --cli-region=cn-north-4 --page_size=100 --page_number=1
hcloud OBS cp /tmp/cdn_domains.json obs://my-bucket/inventory/cdn_domains.json -e=obs.cn-north-4.myhuaweicloud.com
hcloud OBS stat obs://my-bucket/inventory/cdn_domains.json -e=obs.cn-north-4.myhuaweicloud.com
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`); selects the CDN endpoint and the OBS endpoint | `cn-south-1` |
| `--format` / `-f` | No | Export format: `json` (default) / `csv` / `md` | `--format md` |
| `--output` / `-o` | No | Local export file path (default `cdn_domains_<region>_<timestamp>.<ext>`) | `/tmp/report.md` |
| `--summary` | No | Append a summary line (domain count) to the Markdown report | `--summary` |
| `--domain-name` | No | Filter by accelerated domain name — real server-side ListDomains parameter | `www.example.com` |
| `--domain-status` | No | Filter by accelerated-domain status — real server-side parameter | `online` |
| `--business-type` | No | Filter by business type — real server-side parameter | `web` |
| `--service-area` | No | Filter by service area — real server-side parameter | `mainland_china` |
| `--enterprise-project-id` | No | Filter by enterprise project ID — real server-side parameter | `0` |
| `--page-size` | No | Page size for ListDomains (default 100) | `100` |
| `--bucket` | Upload | Target OBS bucket (required for the upload step) | `my-bucket` |
| `--key` | No | Target OBS object key (default = export file name) | `inventory/cdn.json` |
| `--endpoint` | No | Override the OBS endpoint (default `obs.<region>.myhuaweicloud.com`) | `obs.cn-south-1.myhuaweicloud.com` |
| `--overwrite` | No | Allow overwriting an existing object (default refuse) | `--overwrite` |
| `--no-verify` | No | Skip the post-upload read-back verification | `--no-verify` |
| `--export-only` | No | Query and export locally only; never upload | `--export-only` |
| `--operation` | No | hcloud CDN operation name; only read-only `ListDomains` is allowed | `ListDomains` |
| `--json` | No | Print the run result as JSON | `--json` |

## Write-Intent Guard

- The CDN guard scans the CDN filter values plus the `--operation` value for
  mutating vocabulary (`create`, `delete`, `update`, `modify`, `enable`,
  `disable`, `refresh`, `preheat`, `destroy`, `remove`, `reset`, and CDN
  operation names such as `CreateDomain`, `DeleteDomain`, `UpdateDomain`,
  `EnableDomain`, `DisableDomain`). Local export flags and OBS target flags
  (`--output` / `--format` / `--summary` / `--bucket` / `--key` / `--endpoint` /
  `--overwrite`) are **not** CDN operations and are excluded from the guard, so a
  local path such as `cdn-delete-report.md` cannot trip it.
- The OBS guard whitelists only `cp` (upload) and `stat` / `ls` (existence and
  read-back). Any other OBS operation (`rm`, `mb`, `mv`, `sync`, ...) is refused.
- Any hit raises a `GuardError` / `ObsError`, prints
  `[错误] ... 已被守卫拦截` / `[错误] 不允许的 OBS 操作 ...`, and exits with code 1
  **before** a single cloud write is executed.
- The only write the code can ever issue is the single `hcloud OBS cp` (PUT) —
  or the SDK `ObsClient.put_object` in the fallback path.

## Safety: Overwrite Protection

- Before uploading, the target object is probed with a **read-only** `stat`
  (`hcloud OBS stat`) or `head_object` (SDK fallback).
- If the object exists and `--overwrite` was **not** given, the script raises
  `OverwriteError` and exits 1 — **no upload happens**.
- Pass `--overwrite` only after the user has explicitly confirmed replacing the
  existing object (`用户确认`). The result JSON records `existed_before` and
  `overwritten` so the action is auditable.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> [--cli-region=<region>] [--key=value ...]
```

- **CDN service / operation** — exact title-case `CDN` + PascalCase
  `ListDomains`; always pass `--cli-region=<region>`, e.g.
  `--cli-region=cn-north-4`. Real paging parameters are `--page_size` +
  `--page_number` (the response carries `total`); the real filters are
  `--domain_name` / `--business_type` / `--domain_status` / `--service_area` /
  `--enterprise_project_id`.
- **OBS service** — the `hcloud OBS` module is **obsutil-backed**: operations are
  lowercase obsutil commands, not PascalCase API names. The region is expressed
  through the endpoint option `-e=obs.<region>.myhuaweicloud.com` (the script
  derives it from `--region`; `--cli-region` is not used by this module).
  - Upload: `hcloud OBS cp <local_file> obs://<bucket>/<key> -e=obs.<region>.myhuaweicloud.com`
  - Read metadata: `hcloud OBS stat obs://<bucket>/<key> -e=obs.<region>.myhuaweicloud.com`
- **REST paths (official SDK `_http_info`)** — CDN `GET /v1.0/cdn/domains`
  (`huaweicloudsdkcdn` v1 `_list_domains_http_info`); OBS `PUT /{object_key}`
  (`huaweicloudsdkobs` v1 `_put_object_http_info`) and `HEAD /{object_key}`
  (`_head_object_http_info`).

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty domain list | Exit 0, prints `当前区域（<x>）无 CDN 加速域名` (+ filters); a header-only / empty result file is still written |
| Target object already exists (no `--overwrite`) | Exit 1, `[错误] 目标对象已存在 ... 默认拒绝上传`; no write happens |
| Read-back size mismatch | Exit 1, `回读校验失败：对象大小 ... 不一致` |
| Missing / invalid AK-SK (CDN or OBS) | Exit 1, explicit hint to configure hcloud / obsutil credentials out-of-band (never in chat) |
| No permission (403 / InvalidAccessKeyId) | Exit 1, `无权限访问...` IAM hint (`cdn:domain:list` / `obs:object:put`) |
| hcloud not installed | CDN & OBS fall back to the SDKs; if the SDK is unavailable too, exit 1 with a clear install hint |
| Bad `--output` path (permission / bad dir) | Exit 1, `导出文件写出失败`; no partial file is left |
| KooCLI usage error (`[USE_ERROR] ...`) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud CDN ListDomains --help` / `hcloud OBS cp --help` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| Write intent detected | Exit 1, guard message, no command executed |

Exit codes: `0` success (including empty region); `1` config, auth, guard,
export, upload, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Region has no CDN domains | Friendly message + a valid (empty) result file, exit 0 |
| Many domains | Automatic `page_number` paging (`total` aware, max 100 pages) |
| Non-`online` domains | Reported with their state (`offline` / `configuring`), not a failure |
| Extra response fields | Output columns are built from the union of returned fields |
| Field missing on a domain | Rendered as `-` |
| Nested `tags` | Flattened into `key=value,...` for csv / md |
| No `--bucket` given | Local export only; the upload step is skipped with an explicit reason |
| `--output` points to a non-existing directory | Directory is created automatically |
| `--output` path contains a guard keyword (e.g. `cdn-delete-report.md`) | Excluded from the guard (local path ≠ CDN operation) |
| `hcloud` absent, SDK installed | Transparent SDK fallback for both query and upload |
| User asks to create/delete/enable a domain or manage buckets/objects | Out of scope — blocked by the guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: the write-intent guard (read passes / create / delete / refresh /
operation whitelist), CDN command construction and filters, JSON extraction and
`total` paging, CDN failure classification (missing AK/SK, 403, `[USE_ERROR]`
with rc=0), the CDN SDK fallback; serialization (json / csv / md / empty /
pipe-escape / tags flattening), default file naming, and atomic file write
(directory creation / bad path); OBS helpers (`parse_obs_url`, cp/stat command
construction, operation whitelist, stat parsing, not-found detection), object
existence probe (exists / not-found / auth / SDK fallback), upload
(new object / overwrite refusal / overwrite allowed / size mismatch / missing
local file / SDK fallback / API error propagation); and the end-to-end entry
point (json/csv/md, export-only, no-bucket skip, overwrite refusal/allowed, empty
region, guard blocking, default key, local path with a write word).

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege IAM policy (CDN read + OBS object put) |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI + obsutil installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
---
name: huawei-cloud-obs-list-pdf
description: |
  1. List the OBS (Object Storage Service) buckets of a Huawei Cloud account
     through the KooCLI obsutil-backed OBS module (`hcloud OBS ls`, the
     read-only ListBuckets operation), with an automatic fallback to the
     official huaweicloudsdkobs v1 SDK (`ObsClient.list_buckets`) when hcloud
     is not installed.
  2. Export the bucket list into a well-formed local `.pdf` report via
     reportlab (preferred) or fpdf2 (fallback) — headers 桶名称 / 创建时间 / 区域 /
     存储类别 / 桶策略, optional summary row — strictly local file generation,
     nothing is ever written back to OBS. `--output` sets the file path
     (default `obs_buckets_<region>_<timestamp>.pdf`).
  3. Three output modes: `--format pdf` (default) / `table` / `json`. Region
     aware: `--region` (default cn-north-4) selects the OBS endpoint; optional
     `--endpoint` overrides it. `--page-size` caps the returned count.
  4. Explicit error classification: missing AK/SK credentials (「缺少 AK/SK
     凭证」), hcloud not installed (falls back to SDK, else a clear hint),
     invalid/insufficient credentials (403 / InvalidAccessKeyId → IAM hint),
     and generic API/network failures. Empty bucket lists produce a friendly
     hint and never a corrupt .pdf.
  5. Built-in write-intent guard: any mutating intent (create / delete / upload
     / download / copy / remove / restore / sync / modify …) or any operation
     other than the read-only `ls` is rejected before execution — this skill is
     strictly read-only.
  6. Triggers include: "查询 OBS 生成 PDF", "OBS 桶列表导出 PDF", "obs pdf",
     "导出 OBS 桶列表为 PDF", "桶列表 PDF 报表", "桶清单 PDF", "OBS bucket list pdf",
     "export OBS buckets to pdf", "桶报表 PDF".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, parsing,
     PDF format correctness, empty lists, error classification, SDK fallback,
     and the write-intent guard.
tags: [huawei-cloud, obs, storage, readonly, pdf]
---

# Huawei Cloud OBS Bucket List → PDF Export

## Overview

Query the OBS bucket list of a Huawei Cloud account through KooCLI's
obsutil-backed OBS module (`hcloud OBS ls` — the read-only ListBuckets
operation), with a fallback to the official `huaweicloudsdkobs` v1 SDK, and
export the result into a local **.pdf** report (reportlab preferred, fpdf2
fallback). The skill is aimed at resource inventory, daily operations patrol,
and PDF-report style deliverables.

> The read-only query paradigm (region-aware bucket listing) is shared with the
> other OBS query skills in this repository; this skill adds the local PDF
> export layer on top of it.

Architecture:

```text
agent → python3 scripts/list_obs_buckets_pdf.py → hcloud OBS ls [-limit=N] [-e=obs.<region>.myhuaweicloud.com]
      → Huawei Cloud OBS OpenAPI (ListBuckets) → parsed buckets → export_pdf (reportlab/fpdf2) → .pdf / table / json

(hcloud binary missing)    → fallback: huaweicloudsdkobs v1 ObsClient.list_buckets
(no PDF backend installed) → run scripts/ensure_env.py  (auto pip install)
```

Key properties:

- **Read-only by design** — the only API ever invoked is ListBuckets (GET). A
  write-intent guard scans user arguments and validates the operation name;
  mutating intents (create / delete / upload / download / copy / remove /
  restore / sync ...) are rejected with an explicit message before any command
  runs. The PDF file is generated on the **local filesystem only** — no OBS
  write happens.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  hcloud binary is absent, the script falls back to the official
  `huaweicloudsdkobs` SDK (`list_buckets`). Credentials are read from the
  hcloud/obsutil profile or the SDK environment — never handled by the script.
- **Well-formed .pdf** — a fixed header row (桶名称 / 创建时间 / 区域 / 存储类别 /
  桶策略) plus one data row per bucket, with an **optional summary row**
  (`--summary`) showing the total bucket count. The PDF is saved via a
  temporary file + atomic rename, so an interrupted write never leaves a
  corrupt/partial .pdf behind.
- **Two PDF backends** — reportlab is preferred (renders Chinese with the
  built-in CID font `STSong-Light`, no external TTF needed); fpdf2 is the
  fallback when reportlab is unavailable.
- **No broken files** — an empty bucket list, missing credentials or a
  permission failure print an explicit hint on stdout/stderr and **do not**
  produce a .pdf file.
- **Offline-testable** — every code path (parsing, output modes, PDF format,
  error classification, guard, SDK fallback) is covered by unit tests that mock
  the hcloud subprocess.

> **Capability boundary:** this skill lists **buckets only**. It does not list
> objects inside a bucket, does not report bucket quota/usage, and does not
> export object-level inventories. Those require a separate skill/Issue.

Out of scope: every mutating OBS action (bucket create/delete, object
upload/download/copy/delete, ACL/policy/encryption/lifecycle changes) and any
write of the PDF file back into OBS.

## Prerequisites

1. **Python 3.8+** with **reportlab** (or fpdf2) — run
   `python3 scripts/ensure_env.py` to install it automatically (also installs
   `huaweicloudsdkcore` / `huaweicloudsdkobs` for the SDK fallback). See
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
2. **KooCLI (`hcloud`) installed with the obsutil component** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkobs` to enable the
   SDK fallback path.
3. **obsutil credentials configured out-of-band** — the `hcloud OBS` module
   reads AK/SK/endpoint from the obsutil config file (`~/.obsutilconfig`),
   separate from the KooCLI account profile. Never paste AK/SK into chat; the
   script never reads, echoes, or stores secrets itself.
4. **IAM permission** — read-only `obs:bucket:list` (or the `OBS ReadOnlyAccess`
   system policy); least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
5. **Outbound HTTPS** access to `obs.<region>.myhuaweicloud.com`.

## Workflow

1. **(Optional) prepare the environment** — `python3 scripts/ensure_env.py`
   installs any missing dependency (reportlab/fpdf2 + SDK).
2. **Confirm the target region** (default `cn-north-4`); it selects the OBS
   endpoint.
3. **Confirm hcloud/obsutil readiness** (optional, read-only):
   `hcloud OBS ls -limit=1` (or `hcloud version`).
4. **Run the script** with the desired output mode (`--format pdf` for the
   report, `table` / `json` otherwise).
5. **Read the result** — for `pdf`, the printed path is the generated report;
   hand that file/路径 to the user. For table/json, display the result.
6. **Handle the empty / error cases** per the Error Handling table below.

## Core Commands

```bash
# Default: query the account's buckets and generate a .pdf report in cwd
python3 scripts/list_obs_buckets_pdf.py

# Specify region and an explicit output path (recommended)
python3 scripts/list_obs_buckets_pdf.py --region cn-north-4 \
  --output /tmp/obs_buckets_cn-north-4.pdf

# Append a summary row (total bucket count)
python3 scripts/list_obs_buckets_pdf.py --summary

# Plain table / JSON for humans / tooling
python3 scripts/list_obs_buckets_pdf.py --format table
python3 scripts/list_obs_buckets_pdf.py --format json

# Custom endpoint / capped count
python3 scripts/list_obs_buckets_pdf.py --region cn-south-1 --page-size 50
```

Equivalent direct KooCLI command (the script wraps exactly this call):

```bash
hcloud OBS ls -limit=1000 -e=obs.cn-north-4.myhuaweicloud.com
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`); selects the OBS endpoint | `cn-south-1` |
| `--format` / `-f` | No | Output mode: `pdf` (default) / `table` / `json` | `--format table` |
| `--output` / `-o` | No | .pdf file path (only used with `--format pdf`; default `obs_buckets_<region>_<timestamp>.pdf`) | `/tmp/report.pdf` |
| `--summary` | No | Append a summary row (桶数量 / N) to the PDF report | `--summary` |
| `--page-size` | No | Maximum number of buckets to return (default 1000) | `50` |
| `--endpoint` | No | Override the OBS endpoint (default `obs.<region>.myhuaweicloud.com`) | `obs.custom.example.com` |
| `--operation` | No | hcloud OBS operation name; only the read-only `ls` is allowed | `ls` |

Output-mode precedence: `--format` selects the mode; `--output` only matters for
`pdf`. The local `--output` path value (e.g. a folder literally named
`downloads`) is excluded from the write-intent guard because it is not an OBS
operation.

## Write-Intent Guard

- The script scans all user arguments (except the `--output` path value) plus
  the `--operation` value for mutating vocabulary (`create`, `delete`,
  `upload`, `download`, `copy`, `remove`, `move`, `restore`, `abort`, `sync`,
  `modify`, `update`, `overwrite`, and OBS operation names such as
  `CreateBucket`, `DeleteBucket`, `PutObject`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed.
- Only `hcloud OBS ls` (read-only ListBuckets) — or the SDK `list_buckets`
  call in the fallback path — is ever constructed by `build_command()`; there
  is no code path that can issue a mutating OBS API call.

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
  the region is expressed through the endpoint option
  `-e=obs.<region>.myhuaweicloud.com` (the script derives it from `--region`).
- **Simple parameter** — `-key=value`, e.g. `-limit=1000`,
  `-e=obs.cn-north-4.myhuaweicloud.com`.
- **REST path (official SDK)** — `GET /` (`ListBuckets`), invoked by
  `huaweicloudsdkobs` v1 `ObsClient.list_buckets`; the endpoint is resolved from
  the requested region.

## PDF Format

| Column (header) | Source key | Notes |
| ---------- | ---------- | --------- |
| 桶名称 | `name` | Bucket name from `obs://<name>` / SDK list |
| 创建时间 | `creation_date` | Detected from CLI columns or SDK response; `-` when absent |
| 区域 | `location` | Region token from CLI columns or SDK response; `-` when absent |
| 存储类别 | `storage_class` | `Standard` / `Warm` / `Cold` / `Standard-IA` ...; `-` when absent |
| 桶策略 | `policy` | `private` / `public-read` / `public-read-write` ...; `-` when absent |

`--summary` appends a footer row: `桶数量 | <N> | Region <region>`.

The document title is `OBS 桶列表`. reportlab renders the Chinese headers with
its built-in CID font `STSong-Light`; the fpdf2 fallback uses a detected system
CJK TTF when present, otherwise the core font.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty bucket list | Exit 0, prints `当前账号（Region <x>）无 OBS 桶，未生成 PDF 文件。` — no file is produced |
| Missing AK/SK / obsutil config | Exit 1, `缺少 AK/SK 凭证` hint to run `hcloud obs config` out-of-band (never in chat) |
| Invalid / insufficient credentials (403 / InvalidAccessKeyId) | Exit 1, `无权限访问 OBS，请检查 IAM 权限` hint; no pdf is produced |
| hcloud not installed | Exit 1 after SDK fallback also unavailable; hint to install KooCLI or run `ensure_env.py` |
| PDF backend missing (reportlab & fpdf2) | Exit 1, `缺少 PDF 依赖` hint to run `python3 scripts/ensure_env.py` |
| Bad `--output` path (permission / bad dir) | Exit 1, `PDF 文件写出失败` hint; no partial file is left |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud OBS ls --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty list; `1` config, auth, guard, export, or API
error (`table`/`json` modes follow the same conventions).

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Account has no buckets | Friendly `无 OBS 桶，未生成 PDF 文件` message, exit 0 |
| Large number of buckets | `-limit` caps the CLI result; `--page-size` controls it (default 1000) |
| Extra obsutil columns (`-sc` etc.) | Creation date / region / storage class / policy detected heuristically |
| Duplicate `obs://` lines | Collapsed to the first occurrence per bucket name |
| Field missing on a bucket | Rendered as `-` in both the table and the PDF cell |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkobs` list_buckets, same output modes |
| reportlab absent, fpdf2 present | Transparent fallback to the fpdf2 renderer, same PDF output |
| No CJK font for the fpdf2 fallback | Non-Latin-1 glyphs are transliterated; a valid PDF is still produced |
| `--output` points to a non-existing directory | Directory is created automatically |
| `--output` path contains a guard keyword (e.g. `downloads/`) | Path value is excluded from the guard (local path ≠ OBS operation) |
| User asks to create/delete/upload | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
cd skills/storage/obs/huawei-cloud-obs-list-pdf
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / upload / download
/ copy / remove / restore / sync / normalized variants / operation whitelist /
`--output` path exclusion), command construction (endpoint + limit, no write
flags), obsutil output parsing (names / columns / storage class / policy /
dedupe / empty), failure classification (missing AK/SK, InvalidAccessKeyId,
403, generic, `[USE_ERROR]`), SDK fallback (missing env credentials, success,
unavailable, bucket normalization), PDF export (header / data rows / summary
row / cell fallbacks / backend missing / bad path / reportlab + fpdf2 paths),
rendering (table / json), and all `main()` output modes including empty, pdf,
and error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI + obsutil installation, credential configuration and PDF backend setup |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
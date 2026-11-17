---
name: huawei-cloud-cdn-export-domains
description: |
  1. Query the Huawei Cloud CDN (Content Delivery Network) accelerated-domain
     list of a tenant through KooCLI (`hcloud CDN ListDomains --cli-region=<region>`; the official
     read-only GET /v1.0/cdn/domains), with an automatic fallback to the official
     huaweicloudsdkcdn v1 SDK (CdnClient.list_domains) when hcloud is not
     installed.
  2. Export/download the accelerated-domain list into a local file. Four output
     modes: `--format csv` (default, machine-readable), `markdown`/`md`
     (GitHub-flavored table with a **域名** column first), `json` (array of raw
     records) and `table` (stdout only). `--output`/`-o` sets the path (default
     `cdn_domains_<region>_<timestamp>.<ext>`); the parent directory is created
     automatically and the file is written via a temp file + atomic rename.
     Strictly local file generation — nothing is ever written back to the cloud.
  3. Supports `--domain-name` / `--domain-status` / `--business-type` /
     `--service-area` / `--enterprise-project-id` / `--exact-match` /
     `--show-tags` filtering (all real server-side ListDomains query
     parameters), `--region` override and automatic `page_number` paging over the
     response `total` count.
  4. Explicit error hints for empty domain lists (「当前区域无 CDN 加速域名」),
     403 / insufficient IAM permission (「无权限访问内容分发网络（CDN）」),
     missing or invalid AK/SK credentials, hcloud not installed, and bad export
     paths.
  5. Built-in write-intent guard: any mutating intent (create / delete / update /
     modify / enable / disable / refresh / preheat) or any operation other than
     ListDomains is rejected before execution — this skill is strictly
     read-only.
  6. Triggers include: "下载CDN列表", "导出CDN加速域名", "CDN域名盘点导出",
     "导出/下载华为云 CDN 加速域名列表", "export cdn domains",
     "download cdn domain list", "CDN 加速域名导出", "cdn list export".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     page_number paging, error scenarios, the SDK fallback, the export formats
     and the write-intent guard.
tags: [huawei-cloud, cdn, network, readonly, export]
---

# Huawei Cloud CDN Accelerated-Domain List Export / Download

## Overview

Query the CDN accelerated-domain list of a tenant through KooCLI
`hcloud CDN ListDomains --cli-region=<region>` (official read-only GET
`/v1.0/cdn/domains`, verified in the `huaweicloudsdkcdn` v1 client
`_list_domains_http_info` metadata), then export/download the result into a local
file (CSV / Markdown / JSON). The skill is aimed at CDN inventory inspection,
daily operations patrol, archival/hand-off of an accelerated-domain inventory,
and as a pre-query step for other CDN workflows.

Architecture:

```text
agent → python3 scripts/export_cdn_domains.py → skill-quality-cli run ─▶ hcloud CDN ListDomains --cli-region=<region> --page_size=N --page_number=P
      → Huawei Cloud CDN OpenAPI (GET /v1.0/cdn/domains) → parsed JSON domains → render_csv/markdown/json → local file

(hcloud binary missing) → fallback: huaweicloudsdkcdn v1 CdnClient.list_domains
(missing SDK)           → run scripts/ensure_env.py  (auto pip install)
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListDomains` (GET). A
  write-intent guard scans the user arguments and validates the operation name;
  mutating intents (create / delete / update / modify / enable / disable /
  refresh / preheat ...) are rejected with an explicit message before any
  command runs. The export file is generated on the **local filesystem only** —
  no CDN write happens.
- **CLI first, SDK fallback** — KooCLI is the primary execution path (wrapped
  with `skill-quality-cli` for telemetry); when the hcloud binary is absent, the
  script falls back to the official `huaweicloudsdkcdn` v1 SDK (`list_domains`).
  Credentials are always read by the CLI profile / SDK environment — never
  handled by the script.
- **Downloadable, name-first artifacts** — CSV (union of every returned field,
  `domain_name`/域名 first), Markdown (fixed columns with **域名** first) and
  JSON (raw records). A missing field renders as `-`; an empty domain list still
  produces a valid header-only artifact. Files are saved via a temporary file +
  atomic rename, so an interrupted write never leaves a corrupt/partial file.
- **Offline-testable** — every code path (paging, filters, output modes, export
  formats, empty result, error classification, guard, SDK fallback, quality
  wrapper) is covered by unit tests that mock the hcloud subprocess.

> **Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

> **Capability boundary:** this skill lists and exports **CDN accelerated
> domains only**. It does not manage CDN lifecycle (create/delete/enable/disable/
> update a domain, origin or config changes), refresh/preheat tasks or
> certificate management, and it does not write the export back to any cloud
> service (e.g. OBS). Those require a separate skill and explicit user
> confirmation (确认).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — the primary execution path; see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   When absent, the SDK fallback is used.
2. **Python 3.8+** with the Huawei Cloud SDK — run
   `python3 scripts/ensure_env.py` to install `huaweicloudsdkcore` and
   `huaweicloudsdkcdn` automatically. The file export itself needs no
   third-party package (standard library only).
3. **Credentials configured out-of-band** — the CLI reads the active hcloud
   profile; the SDK fallback reads AK/SK from the whitelisted environment
   variables (`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`, `HUAWEI_ACCESS_KEY` /
   `HUAWEI_SECRET_KEY`, `HW_*`, ...). Never paste AK/SK into chat; the script
   never reads, echoes or stores secrets itself.
4. **IAM permission** — read-only `cdn:configuration:queryDomainList`;
   least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
5. **Region** — CDN is global; KooCLI advertises `ListDomains` for `cn-north-1`
   and `ap-southeast-1` (default `cn-north-1`).
6. **Outbound HTTPS** access to the CDN OpenAPI endpoint.
- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

1. **(Optional) prepare the environment** — `python3 scripts/ensure_env.py`
   installs any missing SDK dependency.
2. **Confirm the target region** (default `cn-north-1`; valid values
   `cn-north-1` / `ap-southeast-1`).
3. **(Optional) confirm KooCLI readiness** (read-only) — see the Core Commands
   block for the wrapped credential check.
4. **Run the export script** with the desired `--format` and `--output`.
5. **Read the result** — for `csv` / `markdown` / `json`, the printed path is the
   downloaded file; hand that path to the user. For `table`, display the result.
6. **Handle the empty / error cases** per the Error Handling table below.

## Core Commands

> **⚠️ Mandatory quality wrapping: `scripts/export_cdn_domains.py` builds every `hcloud` CLI call as `skill-quality-cli run --skill-name huawei-cloud-cdn-export-domains -- hcloud ...` (enforced in code, not left to the agent). If `skill-quality-cli` is unavailable (run `bash scripts/ensure_cli.sh`) or `SKILL_QUALITY_REPORT=0`, the CLI path degrades to bare `hcloud` (no telemetry) — the read-only semantics and the CLI→SDK fallback are unchanged. When the `hcloud` binary itself is not resolvable, the wrapping is skipped and the bare command is run, so the missing binary surfaces as a `FileNotFoundError` → `ConfigError` and the SDK fallback still triggers (the wrapper would otherwise hide that failure behind its own exit code).**

```bash
# Default: query the accelerated-domain list and export it to a CSV file in cwd
python3 scripts/export_cdn_domains.py

# Specify region and an explicit output path (recommended)
python3 scripts/export_cdn_domains.py --region cn-north-1 \
  --output /tmp/cdn_domains_cn-north-1.csv

# Export as Markdown (with a summary line) or JSON
python3 scripts/export_cdn_domains.py --format markdown --output /tmp/cdn_domains.md --summary
python3 scripts/export_cdn_domains.py --format json --output /tmp/cdn_domains.json

# Plain aligned table on stdout
python3 scripts/export_cdn_domains.py --format table

# Server-side filters
python3 scripts/export_cdn_domains.py --domain-status online --format csv
python3 scripts/export_cdn_domains.py --domain-name www.example.com --business-type web
python3 scripts/export_cdn_domains.py --service-area mainland_china --page-size 500

# Read-only credential readiness check (also wrapped)
skill-quality-cli run --skill-name huawei-cloud-cdn-export-domains -- hcloud configure list
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
automatic page_number paging):

```bash
skill-quality-cli run --skill-name huawei-cloud-cdn-export-domains -- hcloud CDN ListDomains --cli-region=cn-north-1 --page_size=100 --page_number=1
skill-quality-cli run --skill-name huawei-cloud-cdn-export-domains -- hcloud CDN ListDomains --cli-region=cn-north-1 --domain_status=online --page_size=100 --page_number=1
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-1`; CDN ListDomains is advertised for `cn-north-1` / `ap-southeast-1`) | `ap-southeast-1` |
| `--format` / `-f` | No | Output mode: `csv` (default) / `markdown`(`md`) / `json` / `table` | `--format markdown` |
| `--output` / `-o` | No | Export file path (csv/markdown/json; default `cdn_domains_<region>_<timestamp>.<ext>`) | `/tmp/report.csv` |
| `--summary` | No | Append a summary line (域名数量) to the Markdown report | `--summary` |
| `--domain-name` | No | Filter by accelerated domain name — real server-side query parameter (fuzzy) | `www.example.com` |
| `--domain-status` | No | Filter by accelerated-domain status — real server-side query parameter (`online`/`offline`/`configuring`/...) | `online` |
| `--business-type` | No | Filter by business type — real server-side query parameter (`web`/`download`/`video`/`wholeSite`) | `web` |
| `--service-area` | No | Filter by service area — real server-side query parameter (`mainland_china`/`outside_mainland_china`/`global`) | `mainland_china` |
| `--enterprise-project-id` | No | Filter by enterprise project ID — real server-side query parameter (`all` = all projects) | `0` |
| `--exact-match` | No | Exact domain name match (`true`/`false`) — real server-side query parameter | `true` |
| `--show-tags` | No | Whether to include tags (`true`/`false`) — real server-side query parameter | `true` |
| `--page-size` | No | Page size for ListDomains (default 100, range 1–10000; pages are fetched automatically) | `500` |
| `--operation` | No | hcloud CDN operation name; only the read-only `ListDomains` is allowed | `ListDomains` |

Output-mode precedence: `--format` selects the mode. `--output` / `--summary`
only matter for the file formats (`csv` / `markdown` / `json`); `table` writes to
stdout. The local `--output` path value (e.g. a file literally named
`cdn-delete-report.csv`) and the filter values are excluded from the write-intent
guard because they are not CDN operations.

## Export Formats

| Format | Artifact | Columns / content |
| ---------- | ---------- | --------- |
| `csv` (default) | `.csv` file | Union of every returned field, `domain_name` first; `tags` flattened to `k=v,...` |
| `markdown` (`md`) | `.md` file | Fixed columns: 域名 / 加速域名状态 / CNAME / 业务类型 / 服务区域 / HTTPS状态 / 企业项目 ID / 创建时间 / 修改时间; `--summary` appends `**汇总**：共 N 个 CDN 加速域名` |
| `json` | `.json` file | Array of raw accelerated-domain records |
| `table` | stdout | Aligned full-field table (union of returned fields) |

A missing field renders as `-`. An empty domain list still produces a valid
header-only artifact and exits `0`.

## Write-Intent Guard

- The script scans all user arguments (except the values of the read-only filter
  flags and of the local-output/format flags `--output` / `-o` / `--format` /
  `-f`) plus the `--operation` value for mutating vocabulary (`create`, `delete`,
  `update`, `modify`, `enable`, `disable`, `refresh`, `preheat`, and CDN
  operation names such as `CreateDomain`, `DeleteDomain`, `UpdateDomain`,
  `EnableDomain`, `DisableDomain`).
- Any hit raises `GuardError`, prints
  `[错误] 检测到写操作意图 ... 已被守卫拦截`, and exits with code 1 **before** a
  single hcloud command is executed.
- Only `hcloud CDN ListDomains --cli-region=<region>` (GET) — or the SDK `list_domains` call in the
  fallback path — is ever constructed by `build_command()`; there is no code path
  that can issue a mutating CDN API call. Every mutating CDN action requires a
  dedicated skill and explicit user confirmation (确认).

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `CDN`.
- **Operation name** — PascalCase API operation: `ListDomains`.
- **Region parameter** — always pass `--cli-region=<region>`, e.g.
  `--cli-region=cn-north-1`.
- **Simple parameters** — `--key=value`, e.g. `--page_size=100`,
  `--page_number=1`, `--domain_name=www.example.com`, `--domain_status=online`,
  `--business_type=web`. All filters are real server-side ListDomains parameters
  (verified against the `huaweicloudsdkcdn` v1 `ListDomainsRequest` model).
- **Paging** — `--page_size` + `--page_number`; the loop advances `page_number`
  until the collected count reaches the response `total`.
- **REST path (official SDK `_http_info`)** — `GET /v1.0/cdn/domains`
  (`huaweicloudsdkcdn` v1 `_list_domains_http_info`).

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty domain list | Exit 0, prints `当前区域（<x>）无 CDN 加速域名` (+ active filters); a header-only (empty) export file is still written |
| 403 / insufficient IAM permission | Exit 1, `无权限访问内容分发网络（CDN），请检查 IAM 权限` hint (`cdn:configuration:queryDomainList`); no file is produced |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat); no file is produced |
| hcloud not installed | Falls back to the SDK; if the SDK is unavailable too, exit 1 with a clear hint |
| Bad `--output` path (permission / bad dir) | Exit 1, `导出文件写出失败` hint; no partial file is left |
| `--page-size` out of range (not 1~10000) | Exit 1, explicit range error before any call |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit hcloud 参数错误 hint pointing to `hcloud CDN ListDomains --cli-region=<region> --help` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, export, or API
error (`table` mode follows the same conventions).

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Region has no accelerated domains | Friendly message + a header-only (empty) export file, exit 0 |
| Non-`online` domains | Reported with their state (`offline` / `configuring` ...), not treated as failure |
| `--domain-name` / `--domain-status` / `--business-type` filters | Forwarded as real server-side query parameters (verified API params) |
| Large domain count | Automatic `page_number` paging (`total` aware, max 100 pages) |
| Extra response fields | CSV/table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on a domain | Rendered as `-` |
| Nested `tags` | Flattened into `key=value,...` |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkcdn` list_domains, same output modes |
| `--output` points to a non-existing directory | Directory is created automatically |
| `--output` path contains a guard keyword (e.g. `cdn-delete-report.csv`) | Path value is excluded from the guard (local path ≠ CDN operation) |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| User asks to create/delete/enable a domain | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation (确认) is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network),
executed from the skill directory through the bundled runner (the same
executor-friendly entrypoint declared in templates/test-vars.json):

```bash
python3 scripts/run_unit_tests.py
```

Coverage: write-intent guard (read passes / create / delete / update / enable /
disable / refresh / normalized variants / operation whitelist / filter+output
value exclusion / following-flag-still-scanned), command construction, the
skill-quality-cli wrapper (wrapped / bare override / report toggle), JSON
extraction and `domains` extraction, failure classification (missing AK/SK, 403,
generic, `[USE_ERROR]` with rc=0), page_number paging (total / full page /
empty), SDK fallback (missing env credentials / SDK request signature),
rendering (table with 域名/状态/CNAME/业务类型, Markdown headers + `-` fallback +
header-only empty table + summary + pipe escaping, CSV, JSON), atomic export
(file written / header-only empty file written / missing dir created / bad path
leaves no file / default filename), and all `main()` output and error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI + SDK installation, credential configuration and skill-quality-cli |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
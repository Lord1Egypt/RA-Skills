---
name: huawei-cloud-scm-cert-list
description: |
  1. Inventory the Huawei Cloud SCM (SSL Certificate Manager / 云证书管理服务)
     certificates of the current account in one region, strictly read-only.
     Primary path: KooCLI `hcloud SCM ListCertificates` (read-only GET
     /v3/scm/certificates); when hcloud is unavailable or fails, fall back to
     the official `huaweicloudsdk` SCM SDK (huaweicloudsdkscm).
  2. Output modes: a compact list of 证书名称 | 绑定域名 | 到期时间 (default), a
     full 8-column table with --table (证书ID / 名称 / 域名 / 类型 / 状态 /
     到期时间 / 剩余天数 / region), and --json for the raw merged response body.
  3. Filters: --content (certificate name / bound domain / SAN, server-side and
     client-side), --expiring N (client-side "expires in at most N days"),
     --expired-days-since N (server-side), --enterprise-project-id, --region
     (default cn-north-4).
  4. Pagination: --limit 10/20/50 with automatic offset+limit paging until the
     whole certificate inventory is collected (--max-pages safety cap).
  5. Built-in read-only guard: any mutating intent (create / delete / update /
     import / push / deploy / revoke / renew / buy ...) is rejected before
     execution with exit code 1 — this skill never writes to SCM.
  6. Explicit error hints for an empty certificate list, 403 / missing
     `scm:cert:list` permission, missing credentials, missing hcloud, network
     failures and KooCLI [USE_ERROR] — always without a traceback.
  7. Triggers include: "list SSL certificates", "SSL 证书列表", "证书盘点",
     "查询证书", "哪些证书快到期", "证书到期巡检", "SCM 证书", "证书类型 DV OV EV",
     "ssl cert inventory", "list scm certificates", "华为云证书".
  8. Offline unit tests cover routing, pagination, output modes, filters, error
     classification and the write-intent guard (mock hcloud subprocess + fake
     SDK client).
tags: [huawei-cloud, scm, security, readonly, koo-cli]
---

# Huawei Cloud SCM Certificate List

## Overview

Inventory the SSL/TLS certificates managed by Huawei Cloud SCM in one region
through KooCLI `hcloud SCM ListCertificates`, returning certificate name, ID,
bound domain (and SANs), type family (DV/OV/EV), status, expiry time, remaining
days, derived source and the region. Aimed at certificate inventory (证书盘点),
expiry patrol (到期巡检), deployment pre-check (部署前核对) and compliance review.

| Operation | REST path | Method | Purpose |
| --------- | --------- | ------ | ------- |
| `SCM ListCertificates` | `/v3/scm/certificates` | GET | list SCM certificates of the region |

> The REST path is verified from the official SDK source
> (`huaweicloudsdkscm/v3/scm_client.py`, `_list_certificates_http_info` →
> `resource_path = "/v3/scm/certificates"`), not inferred.

Architecture:

```text
agent → python3 scripts/list_scm_certs.py [--region=<region>] [--table|--json]
      → hcloud SCM ListCertificates --cli-region=<region> --limit=<n> --offset=<m>
        └─ (hcloud missing / failed) → huaweicloudsdk SCM SDK ListCertificates
      → Huawei Cloud SCM OpenAPI → parsed JSON → compact list / table / JSON
```

Key properties:

- **Read-only by design** — only `ListCertificates` is ever constructed; the
  write-intent guard rejects `--action create|delete|update|import|push|...`
  (and a write keyword passed as the search content) before any command runs.
  Certificate application, purchase, import, deployment push, revocation and
  deletion are explicitly out of scope and require a dedicated write-capable
  skill with explicit user confirmation.
- **CLI first, SDK fallback** — `hcloud` is the primary path; when it is missing
  or fails with a transient/backend error the script falls back to
  `huaweicloudsdkscm` (SDK credentials come from `HUAWEICLOUD_SDK_AK` /
  `HUAWEICLOUD_SDK_SK` only; SCM is a global service, so the SDK client is built
  with `GlobalCredentials`, optionally seeded by `HUAWEICLOUD_SDK_DOMAIN_ID`).
  `403`, credential and `[USE_ERROR]` failures never
  fall back — they are reported as-is so a permission problem is never silently
  turned into "no certificates".
- **Complete inventory** — offset+limit paging until a short page or
  `total_count` is reached, with `--max-pages` as a safety cap.
- **Precise expiry filter** — `--expiring N` is a client-side filter on the
  computed `days_left` (≤ N, including already expired certificates), so it is
  exact regardless of the server-side `expired_days_since` semantics.
- **No files written** — everything goes to stdout; secrets are delegated to the
  KooCLI profile or environment.
- **Offline-testable** — all code paths are covered by unit tests that mock the
  hcloud subprocess and inject a fake SDK client.

Out of scope: applying for / buying / importing / pushing / deploying / revoking
/ deleting / updating certificates, CSR management, private CA management,
`ShowCertificate` deep-dive, cross-region aggregation and file export.

> **Dependency**: Quality telemetry is collected automatically via
> skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Missing hcloud is not fatal: the script falls back to the SDK.
2. **Active credential profile** — configure credentials out-of-band (run the
   KooCLI configure command in your terminal, or export
   `HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`). Never paste AK/SK into chat;
   the script never reads, echoes, or stores secrets itself.
3. **IAM permission** — read-only `scm:cert:list` (certificate list);
   least-privilege policy in [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** — standard library only for the CLI path; the SDK fallback
   additionally needs `huaweicloudsdkcore` + `huaweicloudsdkscm`.
5. **Outbound HTTPS** access to `*.myhuaweicloud.com`.
6. **`skill-quality-cli`** — ensured by `bash scripts/ensure_cli.sh` (idempotent,
   skips if present).
   - Upgrade: run `skill-quality-cli upgrade` manually (no auto-upgrade)
   - Disable telemetry report: set `SKILL_QUALITY_REPORT=0`

## Workflow

1. **Confirm the region** (default `cn-north-4`) — SCM certificates are
   region-scoped; SCM endpoints exist in `cn-north-4`, `ap-southeast-1` and
   `my-kualalumpur-1` per the SDK region table.
2. **Run the list script** with the desired output mode and filters.
3. **Read the result** — compact list for a quick look, `--table` for the full
   inventory columns, `--json` for downstream tooling.
4. **Handle the empty / error cases** per the Edge Cases table (the script
   prints an explicit, actionable hint for each of them).

## Core Commands

> **⚠️ Mandatory: every `hcloud` command in this skill MUST be wrapped with
> `skill-quality-cli run --skill-name huawei-cloud-scm-cert-list -- ` — bare
> `hcloud` calls are strictly forbidden.**

```bash
# Primary path: read-only certificate list (one page, default compact output)
skill-quality-cli run --skill-name huawei-cloud-scm-cert-list -- \
  hcloud SCM ListCertificates --cli-region=cn-north-4 --limit=50 --offset=0

# Fuzzy search by certificate name or bound domain
skill-quality-cli run --skill-name huawei-cloud-scm-cert-list -- \
  hcloud SCM ListCertificates --cli-region=cn-north-4 --limit=10 --content=example

# Server-side "within validity or expiring in N days"
skill-quality-cli run --skill-name huawei-cloud-scm-cert-list -- \
  hcloud SCM ListCertificates --cli-region=cn-north-4 --limit=50 --expired_days_since=30

# Confirm the operation really exists (read-only help)
skill-quality-cli run --skill-name huawei-cloud-scm-cert-list -- \
  hcloud SCM ListCertificates --cli-region=cn-north-4 --help
```

```bash
# Wrapper script (do the paging / filtering / rendering for you)
python3 scripts/list_scm_certs.py --region cn-north-4
python3 scripts/list_scm_certs.py --table --region cn-north-4
python3 scripts/list_scm_certs.py --json --region cn-north-4
python3 scripts/list_scm_certs.py --content example.com --region cn-north-4
python3 scripts/list_scm_certs.py --expiring 30 --region cn-north-4
python3 scripts/list_scm_certs.py --backend sdk --region cn-north-4
```

```bash
# Quality-CLI readiness + offline unit tests
bash scripts/ensure_cli.sh
python3 -m unittest discover -s tests -v
```

### Output examples

Default (compact):

```text
证书名称          | 绑定域名          | 到期时间
-----------------+------------------+-------------------
prod-web         | www.example.com  | 2026-12-31 08:00:00

共 1 个证书（区域: cn-north-4，后端: cli，来源: SCM签发 1）
```

`--table` (exactly eight columns):

```text
证书ID | 名称 | 域名 | 类型 | 状态 | 到期时间 | 剩余天数 | region
```

`--json` prints the merged raw response with `certificates`, `total_count` and
`region`.

### Field normalization / derivation

| Field | Source | Notes |
| ----- | ------ | ----- |
| `id` / `name` / `domain` / `sans` | API as-is | `-` when the API omits it |
| `type` | API `type` (`DV_SSL_CERT*` → `DV`, `OV_*` → `OV`, `EV_*` → `EV`) | unknown values are shown verbatim |
| `status` | API `status` as-is | e.g. `ISSUED`, `UPLOAD`, `EXPIRED`, `REVOKED` |
| `expire_time` | API `expire_time`, normalized to UTC `YYYY-MM-DD HH:MM:SS` | `-` when missing |
| `days_left` | derived from `expire_time` vs. now | negative for expired certificates |
| `source` | derived from `status` (no fabricated API field) | `UPLOAD` → 上传托管; SCM lifecycle statuses → SCM签发; otherwise `-` |
| `region` | `--region` | single region per call |

## Parameter Confirmation

| Parameter | Required | Description | Example |
| --------- | -------- | ----------- | ------- |
| `--region` | No | Huawei Cloud region of the SCM certificates (default `cn-north-4`) | `cn-north-4` |
| `--content` | No | Fuzzy search by certificate name / bound domain / SAN (passed to the API, re-checked client-side) | `example.com` |
| `--expiring` | No | Client-side filter: only certificates with `days_left <= N` (includes expired) | `30` |
| `--expired-days-since` | No | Server-side filter: within validity period or expiring in at most N days | `60` |
| `--enterprise-project-id` | No | Enterprise project ID; omit to query all projects the caller can see | `0` |
| `--limit` | No | Page size, only `10` / `20` / `50` (default `50`) | `50` |
| `--offset` | No | Starting offset (default `0`) | `0` |
| `--max-pages` | No | Safety cap for automatic paging (default `200`) | `20` |
| `--table` | No | Print the full eight-column table | - |
| `--json` | No | Print the raw merged response body | - |
| `--backend` | No | `auto` (CLI → SDK fallback), `cli`, or `sdk` | `auto` |
| `--timeout` | No | Per-call timeout in seconds (default `60`) | `60` |
| `--action` | No | Only `list` is allowed; any other value is rejected by the read-only guard | `list` |

## KooCLI Command Format Standard

`hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]`

| Element | Value (verified from `hcloud SCM ListCertificates --help`) | Example |
| ------- | ----------------------------------------------------------- | ------- |
| Service | `SCM` (title case) | `SCM` |
| Operation | `ListCertificates` (PascalCase, GET) | `ListCertificates` |
| Region | `--cli-region=<region>` is required | `--cli-region=cn-north-4` |
| Simple parameter | `--key=value` | `--limit=50` |

Supported query parameters: `--content`, `--limit`, `--offset`,
`--expired_days_since`, `--enterprise_project_id`, `--status`, `--deploy_support`,
`--owned_by_self`, `--sort_dir`, `--sort_key`. This skill only uses the read-only
subset listed under Parameter Confirmation and never sends a mutating request.

## Edge Cases

| Scenario | Handling |
| -------- | -------- |
| Account has no certificates | prints `未找到 SSL 证书（区域: …）` plus a region hint, exit 0 |
| Filters match nothing | prints `未找到匹配的 SSL 证书（区域: …）` plus a filter hint, exit 0 |
| 403 / `SCM.4002` / `not authorized` | explicit hint to grant `scm:cert:list`, exit 1 (never shown as an empty list) |
| Missing / invalid AK/SK | explicit hint to configure the KooCLI profile or export env vars, exit 1 |
| Network failure / timeout | explicit network hint, exit 1; CLI path falls back to the SDK in `auto` mode |
| `[USE_ERROR]` from KooCLI | parameter/usage hint (region, limit, offset), exit 1 |
| hcloud not installed | SDK fallback in `auto` mode; explicit install hint with `--backend cli`, exit 1 |
| `huaweicloudsdkscm` not installed | `pip install huaweicloudsdkcore huaweicloudsdkscm` hint, exit 1 |
| Write intent (`--action delete`, `--content import`, …) | rejected before any call, exit 1 |
| Invalid `--limit` / `--offset` / `--expiring` | rejected with the valid range, exit 1 |

## Reference Documents

- [references/iam-policies.md](references/iam-policies.md) — least-privilege read-only IAM policy (`scm:cert:list`)
- [references/cli-installation-guide.md](references/cli-installation-guide.md) — KooCLI install, credential setup, SDK fallback
- [references/verification-method.md](references/verification-method.md) — how to verify each output mode and error path
- [references/acceptance-criteria.md](references/acceptance-criteria.md) — acceptance checklist
- [references/dataflow-diagram.md](references/dataflow-diagram.md) — Mermaid data flow diagram
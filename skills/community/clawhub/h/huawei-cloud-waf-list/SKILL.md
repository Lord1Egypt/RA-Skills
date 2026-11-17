---
name: huawei-cloud-waf-list
description: |
  1. Query the list of Huawei Cloud WAF (Web Application Firewall, Web应用防火墙)
     protected websites / domain names under the current account through KooCLI
     (hcloud waf ListHost / ListCompositeHosts — read-only GET
     /v1/{project_id}/waf/instance and /v1/{project_id}/composite-waf/host).
  2. Output modes: a compact table (default) with 防护域名 | 防护状态 | 接入方式 |
     保活方式 | 独享IP | Domain ID key fields, --json (the raw host array)[, and
     --names-only (unique sorted domain list).
  3. Supports --region to pick the region, --all-modes / --mode cloud|premium to
     select cloud-mode or dedicated/premium-mode protected domains,
     --hostname filtering, --protect-status (-1 bypass / 0 suspended / 1 enabled),
     --enterprise-project-id and --policyname filters, and automatic pagination
     (--pagesize, -1 = fetch all). Access mode (接入方式 cloud/premium) is
     surfaced from waf_type, keep-alive mode (保活方式) from proxy.
  4. Explicit error hints for an empty protected-site list (「当前区域无 WAF 防护网站」),
     403 / insufficient IAM permission (「无权限访问 WAF 防护网站列表」, WAF.00012006),
     disabled region (APIGW.0802), and hcloud not installed.
  5. Built-in write-intent guard: any mutating intent (create / delete / update /
     migrate / rename / batch ...) is rejected before execution — this skill is
     strictly read-only.
  6. Triggers include: "list WAF sites", "WAF 防护网站列表", "查询WAF防护域名",
     "WAF 域名列表", "WAF 防护状态查询", "WAF 网站盘点", "WAF 巡检",
     "list waf hosts", "waf protected domains", "华为云WAF列表".
  7. Offline unit tests (mocked hcloud subprocess) cover routing, output modes,
     filters, error scenarios and the write-intent guard.
tags: [huawei-cloud, waf, security, readonly, koo-cli]
---

# Huawei Cloud WAF Protected Website List

## Overview

Query the WAF-protected website / domain-name list of a tenant region through
KooCLI `hcloud waf ListHost` (cloud mode) or `hcloud waf ListCompositeHosts`
(all modes: cloud + dedicated/premium), returning key fields such as the
protected domain name, protection status, access mode (云模式/独享模式), keep-alive
mode (proxy or direct), and exclusive-IP flag. The skill is aimed at WAF
inventory inspection, daily operations patrol, protection-status verification,
and as a pre-query step for other WAF tasks that need a domain or hostid.

| Command | REST path | Scope |
| ------- | --------- | ----- |
| `WAF ListHost` | `GET /v1/{project_id}/waf/instance` | cloud-mode protected domains |
| `WAF ListCompositeHosts` | `GET /v1/{project_id}/composite-waf/host` | domains across all WAF instances (cloud + premium) |

Architecture:

```text
agent → python3 scripts/list_waf_sites.py [--region=<region>] [--all-modes|--mode=<m>]
      → hcloud waf ListHost | ListCompositeHosts --cli-region=<region>
      → Huawei Cloud WAF OpenAPI → parsed JSON → table / --json / --names-only
```

Key properties:

- **Read-only by design** — only the two `List*` (GET) operations are ever
  constructed. A write-intent guard scans user arguments and validates the
  operation name; mutating intents (create / delete / update / migrate /
  rename / batch ...) are rejected with an explicit message before any command
  runs.
- **KooCLI only** — WAF is driven through the hcloud CLI. Credentials are always
  resolved by the KooCLI profile / environment, never handled by the script.
- **Two scopes** — by default the skill queries cloud-mode domains
  (`ListHost`, matching what the WAF console "存量防护网站" tab shows). Add
  `--all-modes` (or `--mode premium`) to query the composite list covering
  dedicated/premium-mode domains too; `waf_type` in the JSON response marks
  each domain as `cloud` or `premium`.
- **Key-field table default** — the default table renders 防护域名 | 防护状态 |
  接入方式 | 保活方式 | 独享IP | Domain ID; `--json` gives the raw host array for
  downstream tooling.
- **Offline-testable** — every code path (routing, output modes, filters,
  error classification, guard) is covered by unit tests that mock the hcloud
  subprocess.

Out of scope: every mutating WAF action (create / delete / update a domain,
migrate the access mode, batch operations, policy / rule management), and
detailed per-domain configuration export. Those require a dedicated
write-capable skill and explicit user confirmation.

> **Dependency**: Quality telemetry is collected automatically via
> skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
2. **Active credential profile** — configure credentials out-of-band (run the
   KooCLI configure command in your terminal, or set credential environment
   variables). Never paste AK/SK into chat; the script never reads, echoes, or
   stores secrets itself — authentication is delegated entirely to the hcloud
   profile.
3. **IAM permission** — read-only `waf:host:list`; the least-privilege policy
   is in [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess).
5. **Outbound HTTPS** access to `*.myhuaweicloud.com`.
- **`skill-quality-cli`** — ensured by `bash scripts/ensure_cli.sh` (idempotent, skips if present)
  - Upgrade: run `skill-quality-cli upgrade` manually (no auto-upgrade)
  - Disable telemetry report: set `SKILL_QUALITY_REPORT=0`
## Workflow

1. **Confirm the target region** (default `cn-north-4`); every WAF call is
   region-scoped.
2. **Pick the scope** — cloud mode only (default), all modes (`--all-modes`),
   or dedicated/premium mode (`--mode premium`).
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact domain inventory.
5. **Handle the empty / error cases** per the Edge Cases table below (the
   script prints an explicit hint for empty region, missing permission, and
   missing hcloud).

## Core Commands

### List cloud-mode protected domains (default)

```bash
> **⚠️ Mandatory: every `hcloud` command in this skill MUST be wrapped with `skill-quality-cli run --skill-name huawei-cloud-waf-list -- ` — bare `hcloud` calls are strictly forbidden.**

skill-quality-cli run --skill-name huawei-cloud-waf-list -- python3 scripts/list_waf_sites.py --region={region}
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--region` | No (auto) | Region, default `cn-north-4` |

Under the hood the skill runs:

```bash
skill-quality-cli run --skill-name huawei-cloud-waf-list -- hcloud waf ListHost --cli-region={region} --pagesize=-1
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--cli-region` | Yes (auto) | Region, agent fills automatically |
| `--pagesize` | No | Results per page 1-100; `-1` queries all at once |
| `--hostname` | No | Domain name filter |
| `--enterprise_project_id` | No | Enterprise project ID (default 0; use `all_granted_eps` for all) |
| `--policyname` | No | Protection policy name |
| `--page` | No | Page number, default 1 |

### List protected domains across all WAF instances

```bash
skill-quality-cli run --skill-name huawei-cloud-waf-list -- python3 scripts/list_waf_sites.py --all-modes --region={region}
```

Under the hood the skill runs:

```bash
skill-quality-cli run --skill-name huawei-cloud-waf-list -- hcloud waf ListCompositeHosts --cli-region={region} --pagesize=-1
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--cli-region` | Yes (auto) | Region, agent fills automatically |
| `--pagesize` | No | Results per page 1-100; `-1` queries all at once |
| `--hostname` | No | Domain name filter |
| `--enterprise_project_id` | No | Enterprise project ID (default 0; use `all_granted_eps` for all) |
| `--is_https` | No | Whether HTTPS is used for the domain (true/false) |
| `--protect_status` | No | Protection status: `-1` bypass, `0` suspended, `1` enabled |
| `--policyname` | No | Protection policy name |
| `--page` | No | Page number, default 1 |

### JSON output

```bash
skill-quality-cli run --skill-name huawei-cloud-waf-list -- python3 scripts/list_waf_sites.py --all-modes --json --region={region}
```

The JSON body keeps the raw host array: `hostname`, `hostid`, `protect_status`,
`access_status`, `proxy`, `exclusive_ip`, `waf_type` (cloud / premium),
`policyid`, `server` and more.

### Name-only output

```bash
skill-quality-cli run --skill-name huawei-cloud-waf-list -- python3 scripts/list_waf_sites.py --names-only --region={region}
```

### Filter by protection status

```bash
skill-quality-cli run --skill-name huawei-cloud-waf-list -- python3 scripts/list_waf_sites.py --all-modes --protect-status 1 --region={region}
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--region` | No | Huawei Cloud region (CLI `--cli-region`) | `cn-north-4` |
| `--all-modes` | No | Query all WAF modes (cloud + premium) | flag |
| `--mode` | No | `cloud` (default behavior) / `premium` | `premium` |
| `--json` | No | Raw JSON response body | flag |
| `--names-only` | No | Unique sorted domain list | flag |
| `--hostname` | No | Domain name filter | `www.example.com` |
| `--protect-status` | No | `-1` bypass / `0` suspended / `1` enabled | `1` |
| `--enterprise-project-id` | No | Enterprise project ID | `0` / `all_granted_eps` |
| `--policyname` | No | Protection policy name | `default` |
| `--pagesize` | No | Page size, default `-1` (all) | `-1` |

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No protected sites in region | `当前区域无 WAF 防护网站。` |
| Filter matches nothing | `未找到匹配的防护网站。` |
| IAM permission missing (`WAF.00012006`) | `无权限访问 WAF 防护网站列表，请检查 IAM 权限（waf:host:list）。` |
| Region disabled (`APIGW.0802`) | `当前账号在该区域不可用（APIGW.0802），请更换 --region。` |
| hcloud not installed | Explicit install hint pointing to KooCLI quickstart |
| Write intent detected | Read-only guard error before any command runs |

## References

- [references/cli-installation-guide.md](references/cli-installation-guide.md)
- [references/iam-policies.md](references/iam-policies.md)
- [references/verification-method.md](references/verification-method.md)
- [references/dataflow-diagram.md](references/dataflow-diagram.md)
- [references/acceptance-criteria.md](references/acceptance-criteria.md)

## KooCLI Command Format Standard

```bash
skill-quality-cli run --skill-name huawei-cloud-waf-list -- hcloud <service> <Operation> --cli-region=<region> [--key=value ...]
```

| Feature | Description | Example |
|---------|-------------|---------|
| Service name | `waf` (verified from `hcloud waf --help`; service code lowercase) | `waf` |
| Operation name | PascalCase | `ListHost`, `ListCompositeHosts` |
| Region parameter | `--cli-region=<value>` | `--cli-region=cn-north-4` |
| Simple parameter | `--key=value` | `--pagesize=-1` |

Service and parameter names are taken verbatim from `hcloud WAF --help` /
`hcloud waf ListHost --help` — never invented.
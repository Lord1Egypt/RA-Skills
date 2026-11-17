---
name: huawei-cloud-vpn-connection-list
description: |
  1. Inventory Huawei Cloud VPN gateways and their IPSec connections in one
     region through KooCLI (hcloud VPN ListVgws — read-only GET
     /v5/{project_id}/vpn-gateways, and hcloud VPN ListVpnConnections —
     read-only GET /v5/{project_id}/vpn-connection), with an automatic
     fallback to the official huaweicloudsdkvpn v5 SDK when hcloud is not
     installed.
  2. Three output modes: a compact per-gateway list (default) that renders
     every non-UP connection in a dedicated troubleshooting section, --table
     (two tables: 9 gateway columns and 7 connection columns, non-UP
     connections split into their own table), and --json.
  3. Filters: --name (+ --fuzzy) on gateway or connection names, --gateway-id
     drilldown (also sent server-side as vgw_id), client-side --status on
     connection state (e.g. --status DOWN), and --region (default cn-north-4).
  4. limit (1-100) plus automatic page_info.next_marker paging for
     ListVpnConnections; ListVgws is a single unpaged call.
  5. Built-in write-intent guard: every mutating intent (create / update /
     delete a gateway or connection, reset a connection, update the PSK, tag
     changes, SSL VPN server or user management) is rejected before execution
     — this skill is strictly read-only. PSK material is never read, printed
     or persisted.
  6. Triggers include: "vpn connection list", "list vpn connections",
     "VPN网关列表", "查询VPN连接", "哪些VPN连接DOWN", "ipsec connection status",
     "VPN 隧道未协商", "vpn gateway inventory".
  7. Offline unit tests (mocked hcloud subprocess + fake SDK client) cover
     output modes, filters, marker paging, error classification, the SDK
     fallback, PSK stripping and the write-intent guard.
tags: [huawei-cloud, vpn, network, readonly, koo-cli]
---

# Huawei Cloud VPN Gateway & IPSec Connection Inventory

## Overview

Inventory the VPN gateways and IPSec connections of a tenant through KooCLI
`hcloud VPN ListVgws` (read-only GET `/v5/{project_id}/vpn-gateways`) and
`hcloud VPN ListVpnConnections` (read-only GET
`/v5/{project_id}/vpn-connection`). Both endpoints were verified against
KooCLI 7.3.12 (`hcloud VPN --help`) and the official `huaweicloudsdkvpn` v5
client metadata (`_list_vgws_http_info` / `_list_vpn_connections_http_info`).

The skill answers the troubleshooting question **"which IPSec connections are
DOWN or have not negotiated?"**: every connection whose state is not a
successful one is rendered in a separate, highlighted section, never mixed
into the healthy list.

Architecture:

```text
agent → python3 scripts/list_vpn_connections.py → hcloud VPN ListVgws
                                                → hcloud VPN ListVpnConnections (marker-paged)
      → Huawei Cloud VPN OpenAPI (vpn.<region>.myhuaweicloud.com) → parsed JSON
      → compact list / --table (9 gateway cols + 7 connection cols) / --json

(hcloud binary missing) → fallback: huaweicloudsdkvpn v5 VpnClient.list_vgws /
                                   VpnClient.list_vpn_connections
```

Key properties:

- **Read-only by design** — only `ListVgws` and `ListVpnConnections` (both
  GET) are ever constructed. A write-intent guard scans user arguments and
  validates the operation name; mutating intents are rejected with an explicit
  message before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary path; when the binary is
  absent the script falls back to the official `huaweicloudsdkvpn` v5 SDK.
  Credentials are always read by the CLI profile / SDK environment — never
  handled by the script.
- **Non-UP first** — `ACTIVE` / `UP` are the successful states; every other
  real state (`DOWN`, `ERROR`, `PENDING_*`, ...) is counted and rendered in a
  dedicated section (default mode) or a dedicated table (`--table`).
- **No PSK exposure** — the v5 response model carries no PSK, and the script
  strips any `psk*` key from every payload as defence in depth. Nothing is
  written to disk.
- **Offline-testable** — paging, filters, error classification, guard, SDK
  fallback and rendering are covered by unit tests that mock the hcloud
  subprocess and the SDK client.

Out of scope: creating / updating / deleting VPN gateways or IPSec
connections, `ResetVpnConnection`, PSK updates, customer gateway (CGW) CRUD,
SSL VPN (P2C) servers and users, connection monitors, tags, and monitoring
metrics. Those need a write-capable skill with explicit user confirmation.

**Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkvpn` to enable
   the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band (run the
   KooCLI configure command in your terminal, or set credential environment
   variables). Never paste AK/SK into chat; the script never reads, echoes, or
   stores secrets itself — authentication is delegated entirely to the hcloud
   profile / SDK environment.
3. **project_id (SDK fallback only)** — the VPN v5 REST paths are
   `/v5/{project_id}/vpn-gateways` and `/v5/{project_id}/vpn-connection`; when
   falling back to the SDK, supply the project id via `--project-id` or the
   `HUAWEICLOUD_SDK_PROJECT_ID` / `HUAWEI_PROJECT_ID` environment variables.
   The KooCLI path resolves it from the profile automatically.
4. **IAM permission** — read-only `vpn:vpnGateways:list` **and**
   `vpn:vpnConnections:list`; least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
5. **Python 3.8+** (standard library only — argparse / json / subprocess).
6. **Outbound HTTPS** access to `vpn.cn-north-4.myhuaweicloud.com`.
- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

1. **Confirm the target region** (default `cn-north-4`).
2. **Confirm KooCLI readiness** (optional, read-only) by listing the active
   credential profile.
3. **Run the inventory script** with the desired output mode and filters.
4. **Read the result** — the compact list for humans, `--table` when the
   operator needs every column, `--json` for downstream tooling.
5. **Act on the non-UP section** — inspect the flagged connections first
   (`--status DOWN` narrows straight to them), then drill into one gateway
   with `--gateway-id`.
6. **Handle the empty / error cases** per the Edge Cases table below (the
   script prints an explicit hint for an empty region, 403, and missing
   AK/SK).

## Core Commands

> **⚠️ Mandatory: every hcloud command in this skill MUST be wrapped with skill-quality-cli run --skill-name huawei-cloud-vpn-connection-list -- ** — bare hcloud calls are strictly forbidden.**
>
> The inventory script enforces this wrapper internally: `build_hcloud_command()`
> runs every hcloud call as `skill-quality-cli run --skill-name
> huawei-cloud-vpn-connection-list -- hcloud ...`. It degrades to bare hcloud
> only when the telemetry CLI is absent or `SKILL_QUALITY_REPORT=0` (so the
> read-only inventory never breaks because of telemetry), and falls back to the
> SDK when hcloud itself is missing. Run `bash scripts/ensure_cli.sh` first so
> the wrapper is installed.

```bash
# Compact list (default): gateways + a dedicated non-UP connection section
python3 scripts/list_vpn_connections.py --region cn-north-4

# Two tables: VPN gateways (9 columns) and IPSec connections (7 columns)
python3 scripts/list_vpn_connections.py --table

# Machine-readable object (gateways + connections + summary)
python3 scripts/list_vpn_connections.py --json

# Only connections that are DOWN — the fastest triage view
python3 scripts/list_vpn_connections.py --status DOWN

# Drill into one VPN gateway (server-side vgw_id + client-side check)
python3 scripts/list_vpn_connections.py --gateway-id d0a1b2c3-4d5e-6f70-8192-a3b4c5d6e7f8

# Filter by name (exact) or substring (--fuzzy)
python3 scripts/list_vpn_connections.py --name vpn-prod
python3 scripts/list_vpn_connections.py --name prod --fuzzy

# Combine filters and paging size
python3 scripts/list_vpn_connections.py --region cn-south-1 --status DOWN --limit 50
```

Equivalent direct KooCLI commands (the script wraps exactly these calls):

```bash
skill-quality-cli run --skill-name huawei-cloud-vpn-connection-list -- hcloud VPN ListVgws --cli-region=cn-north-4
skill-quality-cli run --skill-name huawei-cloud-vpn-connection-list -- hcloud VPN ListVpnConnections --cli-region=cn-north-4 --limit=100
skill-quality-cli run --skill-name huawei-cloud-vpn-connection-list -- hcloud configure list
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--table` | No | Two-table view (9 gateway columns + 7 connection columns, non-UP split out) | — |
| `--json` | No | Output gateway array + connection array + summary | — |
| `--name` | No | Filter by gateway name or connection name (client-side, exact by default) | `vpn-prod` |
| `--fuzzy` | No | Make `--name` a case-insensitive substring match | — |
| `--gateway-id` | No | Drill into one VPN gateway — sent server-side as the real `vgw_id` query parameter of both operations | `d0a1b...` |
| `--status` | No | Filter by IPSec connection state (client-side, case-insensitive); narrows the gateway view to gateways holding such a connection | `DOWN` |
| `--limit` | No | `ListVpnConnections` page size, 1-100 (default 100) | `50` |
| `--project-id` | No | Project ID (needed by the SDK fallback path for `/v5/{project_id}/...`) | `05f...` |
| `--operation` | No | hcloud VPN operation name; only `ListVgws` / `ListVpnConnections` are allowed | `ListVgws` |

Output-mode precedence: `--json` → `--table` → compact list (default).
Filters compose: `--gateway-id` narrows first (an unknown id is a hard error),
then `--name`, then `--status`.

## Write-Intent Guard

- The script scans the operation/command tokens (not user filter values such
  as `--name` / `--status`) for mutating vocabulary: `create`, `delete`,
  `update`, `reset`, `restart`, `modify`, `change`, `import`, `export`,
  `associate`, `disassociate`, `attach`, `detach`, `bind`, `unbind`, `release`,
  `remove`, `destroy`, `upgrade`, `stop`, `start`, `psk`, and the concrete VPN
  operation names (`CreateVgw`, `DeleteVgw`, `UpdateVgw`,
  `CreateVpnConnection`, `BatchCreateVpnConnection`, `DeleteVpnConnection`,
  `ResetVpnConnection`, `UpdatePsk`, `CreateCgw`, `CreateVpnServer`,
  `BatchCreateResourceTags`, ...). This keeps legitimate queries such as
  `--name prod-create` working while still rejecting write intent.
- Any hit raises `GuardError`, prints
  `[错误] 检测到写操作意图 ... 已被守卫拦截`, and exits with code 1 **before**
  a single hcloud command is executed.
- `build_gateway_command()` / `build_connection_command()` can only emit
  `VPN ListVgws` / `VPN ListVpnConnections`; there is no code path that can
  issue a mutating VPN API call.
- PSK handling: the v5 API does not return the PSK, and every payload is run
  through a recursive `strip_secrets()` that drops any `psk*` key. The skill
  never writes any file, so no secret can be persisted.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `VPN`.
- **Operation name** — PascalCase: `ListVgws`, `ListVpnConnections`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete VPN call).
- **Simple parameter** — `--key=value`, e.g.
  `--vgw_id=d0a1b2c3-4d5e-6f70-8192-a3b4c5d6e7f8`, `--limit=100`,
  `--marker=2025-01-03T00:00:00Z`.
- **Array parameter** — `enterprise_project_id` is declared `array<string>`
  by KooCLI, so only the indexed form is valid: `--enterprise_project_id.1=<id>`.
  This skill does not send it (no parameter exposes it).
- **Paging** — `ListVpnConnections` pages with `limit` + `marker`, where the
  marker is the **creation time of the last record of the previous page**
  (`page_info.next_marker`); the script follows it until it is empty and guards
  against a repeated marker (max 100 pages). `ListVgws` has no
  `limit` / `marker` parameters — the full gateway list is returned in one
  response.
- **REST paths (official SDK `_http_info`)** —
  `GET /v5/{project_id}/vpn-gateways` (`_list_vgws_http_info`) and
  `GET /v5/{project_id}/vpn-connection`
  (`_list_vpn_connections_http_info`); the project_id is resolved by KooCLI
  from the credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty VPN gateway list | Exit 0, prints `当前区域（<x>）无 VPN 网关` |
| Gateways but no IPSec connections | Exit 0, prints `✓ 无非 UP 连接` / `（无）` tables |
| `--gateway-id` unknown in the region | Exit 1, `未找到 VPN 网关（vgw_id=...）` with a hint to list first |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 VPN 网关 / IPSec 连接` + the required `vpn:*:list` actions |
| 401 / invalid or expired AK-SK | Exit 1, `凭证无效（401：AK/SK 无效或已过期）` (never reported as 403) |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band |
| Missing project_id (SDK fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| hcloud not installed | Exit 1 after the SDK fallback is also unavailable, hint to install KooCLI or the SDK |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `--help` |
| API error envelope (`VPN.0007 ... not authorized`, even with exit code 0) | Exit 1, classified as 403 — never treated as an empty inventory |
| `--limit` outside 1-100 | Exit 2 (argparse), explicit range message |
| Write intent detected | Exit 1, `GuardError` message, no command executed |
| skill-quality-cli missing / `SKILL_QUALITY_REPORT=0` | Inventory continues on bare hcloud (telemetry disabled); `scripts/ensure_cli.sh` restores the wrapper |

Exit codes: `0` success / empty region; `1` config, auth, guard, not-found or
API error; `2` invalid command-line value.

## Edge Cases

| Scenario | Handling |
| ----------- | --------- |
| Non-`ACTIVE` / `UP` connections | Counted as 非 UP and rendered in the dedicated section/table, never mixed with healthy ones |
| Connection with no status field | Rendered as `-`, reported under `状态未知`, not counted as 非 UP |
| Many connections | Automatic `page_info.next_marker` paging with a repeated-marker guard and a 100-page ceiling |
| Many gateways | `ListVgws` has no paging — one call returns the whole list |
| Field missing on a gateway / connection | Rendered as `-` in tables |
| Nested `eip1` / `eip2` objects | Rendered as a compact comma-separated IP cell |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkvpn` v5 `list_vgws` / `list_vpn_connections`, same output modes |
| User asks to create/delete/update a gateway or connection, reset a tunnel, or change the PSK | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess and a fake SDK client (no
credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / gateway lifecycle / connection
lifecycle / PSK / restart / SSL VPN / tagging / normalized variants /
operation whitelist / filter values not scanned), command construction,
response parsing (`vpn_gateways` / `vpn_connections` / `page_info.next_marker`
/ error envelopes), failure classification (missing AK/SK, 401, 403 with the
real `VPN.0007` envelope, `[USE_ERROR]` with rc=0, generic), marker paging
(next marker followed / repeated marker / short page / empty / 100-page guard),
SDK fallback (success, drilldown, paging, 401 vs 403, missing AK/SK, missing
project id), filtering (name / fuzzy / status / gateway-id drilldown /
unknown id), rendering (default non-UP section, 9 gateway columns, 7
connection columns, UP vs non-UP split), and every `main()` output mode
including the empty, filtered and error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation, credential configuration and skill-quality-cli |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
# Verification Method

This document records **how** the skill was verified and what the evidence was.
It separates offline verification (always reproducible) from live read-only
verification (depends on the caller's IAM permissions).

## 1. Command legitimacy (Phase 2 research)

| Check | Command | Result |
| --- | --- | --- |
| VPN service + operations exist | `hcloud VPN --help` (KooCLI 7.3.12) | `ListVgws` and `ListVpnConnections` listed; `ListVpnGateways` is **not** an operation (`[USE_ERROR]Operation ListVpnGateways is not supported.`) |
| ListVgws parameters | `hcloud VPN ListVgws --cli-region=cn-north-4 --help` | `--vgw_id`, `--enterprise_project_id.[N]` — no `limit` / `marker` |
| ListVpnConnections parameters | `hcloud VPN ListVpnConnections --cli-region=cn-north-4 --help` | `--vpn_id`, `--eip_id`, `--vgw_ip`, `--vgw_id`, `--enterprise_project_id.[N]`, `--limit`, `--marker` |
| REST paths (trusted source ①: SDK `_http_info`) | `grep -A8 "_list_vgws_http_info"` / `_list_vpn_connections_http_info` in `huaweicloudsdkvpn/v5/vpn_client.py` | `GET /v5/{project_id}/vpn-gateways`, `GET /v5/{project_id}/vpn-connection` |
| Response shape | SDK models `ListVgwsResponse` / `ListVpnConnectionsResponse` / `PageInfo` | `vpn_gateways[]`; `vpn_connections[]` + `page_info.next_marker` (creation time of the last record) |
| IAM actions | live API 403 envelope | `vpn:vpnGateways:list`, `vpn:vpnConnections:list` (verbatim from `VPN.0007`) |

## 2. Offline unit tests

```bash
cd skills/network/vpn/huawei-cloud-vpn-connection-list
python3 -m unittest discover -s tests -v
```

83 cases, all passing. The hcloud subprocess is mocked (`subprocess.run`) and
the SDK is faked (`_sdk_client` + `_sdk_request_classes`), so the suite needs no
credentials, no network and creates no cloud resources. Covered: write-intent
guard, command construction, JSON/envelope parsing, error classification
(including the real `VPN.0007` authorization envelope returned with exit code
0), `page_info.next_marker` paging, the SDK fallback, filters, rendering of all
three output modes, and every `main()` exit path.

## 3. Offline end-to-end smoke (mock hcloud binary)

A mock `hcloud` that returns the same JSON envelopes as the real CLI is pointed
at through the documented test hook:

```bash
export VPN_LIST_HCLOUD_BIN=/path/to/mock-hcloud
python3 scripts/list_vpn_connections.py                 # rc=0, gateway list + ⚠ non-UP section
python3 scripts/list_vpn_connections.py --table          # rc=0, 9-column gateway table + 7-column connection tables
python3 scripts/list_vpn_connections.py --status DOWN    # rc=0, only the DOWN connection
python3 scripts/list_vpn_connections.py --gateway-id vgw-0001   # rc=0, drilldown
python3 scripts/list_vpn_connections.py --gateway-id vgw-9999   # rc=1, 未找到 VPN 网关
python3 scripts/list_vpn_connections.py --json --limit 2        # rc=0, 2 pages merged (3 connections)
python3 scripts/list_vpn_connections.py --operation DeleteVgw    # rc=1, 守卫拦截
```

## 4. Live read-only smoke

```bash
python3 scripts/list_vpn_connections.py --region cn-north-4
```

Result on the development credential: exit code **1** with the classified
message

```text
[错误] 无权限访问 VPN 网关 / IPSec 连接，请检查 IAM 权限（403：需要
vpn:vpnGateways:list 与 vpn:vpnConnections:list）… 详情：VPN.0007 User: … is not
authorized to perform: vpn:vpnGateways:list …
```

This is the **correct** behaviour for a credential without VPN read
permission: the real `VPN.0007` envelope (which KooCLI prints on stdout with
exit code 0) is detected and classified as 403 instead of being silently read
as an empty inventory. A live `rc=0` run requires a credential holding both
`vpn:*:list` actions; it is reproduced with the mock binary (section 3) and
must be repeated by QA on a tenant that has VPN resources and permissions.

## 5. Static checks

```bash
bash -n scripts/ensure_cli.sh
bash -n scripts/install_cli.sh
python3 -m py_compile scripts/list_vpn_connections.py tests/test_list_vpn_connections.py
python3 -m json.tool templates/test-vars.json
bash "$SKILLS_DIR/huawei-cloud-skill-creator/scripts/validate-skill.sh" -s <skill dir>
```

## 6. Read-only guarantee

- The only two operations constructible by the code are `ListVgws` and
  `ListVpnConnections`; the operation whitelist rejects everything else.
- The write-intent guard scans operation/command tokens before any execution.
- No file is written by the skill (no report, no cache, no credential file);
  PSK keys are stripped recursively from every payload as defence in depth.
- No cloud resource is created, modified or deleted by any test path.
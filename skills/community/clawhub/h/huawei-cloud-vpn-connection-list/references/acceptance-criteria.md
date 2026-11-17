# Acceptance Criteria

Checklist used to accept this skill. Each row states the criterion, how it was
verified, and the observed result.

| # | Criterion | Verification | Result |
| --- | --- | --- | --- |
| 1 | Offline unit tests are green | `python3 -m unittest discover -s tests` (mocked hcloud + fake SDK, no credentials, no network) | 88 cases, all pass |
| 2 | Real read-only smoke run | `python3 scripts/list_vpn_connections.py --region cn-north-4` | No write call made; a credential without VPN read permission returns the correctly classified `VPN.0007` 403 (exit 1). A tenant with `vpn:*:list` returns exit 0 — reproduced with the mocked hcloud binary (`--region`, default/`--table`/`--json` all rc=0) |
| 3 | `--gateway-id` drilldown works and an invalid ID is explicit | mock: `--gateway-id vgw-0001` → rc=0, only that gateway; `--gateway-id vgw-9999` → rc=1 with `未找到 VPN 网关（vgw_id=vgw-9999）` | Pass |
| 4 | Non-UP connections are highlighted and `--status DOWN` filters them | default mode prints a dedicated `⚠ 非 UP 连接` section (never mixed with UP); `--table` splits `IPSec 连接 · UP` / `⚠ IPSec 连接 · 非 UP` tables; `--status DOWN` keeps only DOWN connections | Pass |
| 5 | Write intent is blocked before execution | `--operation DeleteVgw` → rc=1 `检测到写操作意图 … 已被守卫拦截`; no hcloud call is ever constructed for a mutating operation | Pass |
| 6 | Syntax / format checks | `bash -n` on both quality-CLI scripts, `python3 -m py_compile` on the script and tests, `python3 -m json.tool` on `templates/test-vars.json` | Pass |
| 7 | Five reference documents present | `references/iam-policies.md`, `cli-installation-guide.md`, `verification-method.md`, `dataflow-diagram.md`, `acceptance-criteria.md` | Pass |
| 8 | Existing skills do not regress | Change set is confined to `skills/network/vpn/huawei-cloud-vpn-connection-list/`; no file under `network/{cc,cdn,dns,eip,elb,nat,vpc}` is touched | Pass |
| 9 | Script path honors the skill-quality-cli wrapping rule | `build_hcloud_command()` prefixes every hcloud call with `skill-quality-cli run --skill-name huawei-cloud-vpn-connection-list --`; unit tests cover wrapped / bare-on-override / `SKILL_QUALITY_REPORT=0` / missing-hcloud-SDK-fallback branches | Pass |

## Additional guarantees

- **Strictly read-only** — only `hcloud VPN ListVgws` and
  `hcloud VPN ListVpnConnections` (both GET) are constructible; `CreateVgw`,
  `DeleteVgw`, `UpdateVgw`, `CreateVpnConnection`, `DeleteVpnConnection`,
  `ResetVpnConnection`, `UpdatePsk`, CGW CRUD, SSL VPN (P2C) operations and tag
  changes appear only as guard rejection vocabulary.
- **No PSK exposure** — the v5 API does not return the PSK; every payload is
  additionally passed through `strip_secrets()`, and the skill writes no file.
- **No cost** — no cloud resource is created, modified, or deleted by the
  skill or by any test path.
- **Paging** — `ListVpnConnections` follows `page_info.next_marker`
  (creation time of the last record), stops on an empty/repeated marker or a
  short page, and aborts after 100 pages.
- **Errors are classified, never silent** — an API error envelope printed with
  exit code 0 (`VPN.0007`) is treated as an error, not as an empty inventory.

## Known limitations (handed to QA)

1. Live `rc=0` verification requires a credential with both
   `vpn:vpnGateways:list` and `vpn:vpnConnections:list`; the development
   credential only produced the classified 403, so live success output was
   verified with the mock binary.
2. `ListVgws` has no paging parameter; a tenant with an extremely large gateway
   list is returned in a single response (bounded by the API itself).
3. `--name` and `--status` are client-side filters (the API has no name/status
   query parameter); they operate on the fetched inventory.
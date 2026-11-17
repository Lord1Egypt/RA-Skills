# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/network/nat/huawei-cloud-nat-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_nat_gateways_via_sdk` mock (no real
  SDK import, no network), plus live regression tests that construct the real
  `ListNatGatewaysRequest` and `NatRegion` when `huaweicloudsdknat` is
  installed (skipped otherwise).
- Cases cover: write-intent guard, command construction (filters forwarded
  server-side), JSON extraction and answer-envelope detection, failure
  classification (missing AK/SK / 401 / 403 / generic / `[USE_ERROR]` with
  rc=0 / API error envelope with rc=0), id-marker paging (last gateway id /
  short page / exact-full-page boundary / chained markers / empty / repeated
  marker guard / unsupported next_marker ignored), SDK fallback (success /
  missing credentials / missing project id / 401 vs 403 / unavailable /
  filters forwarded / pagination), rendering, and all main() output modes.
- Result: 79 tests, all passing (68 offline; the 11 SDK live-import tests run
  when `huaweicloudsdknat` is installed and are skipped otherwise).

## Live verification (when credentials exist)

```bash
hcloud configure list                                              # profile check
hcloud NAT ListNatGateways --cli-region=cn-north-4 --limit=1       # API sanity
python3 scripts/list_nat_gateways.py --region cn-north-4           # full flow
python3 scripts/list_nat_gateways.py --json | python3 -m json.tool >/dev/null  # JSON validity
python3 scripts/list_nat_gateways.py --names-only
python3 scripts/list_nat_gateways.py --status ACTIVE               # server-side filter
python3 scripts/list_nat_gateways.py --spec 1
python3 scripts/list_nat_gateways.py --name my-nat
python3 scripts/list_nat_gateways.py --vpc d0a1b2c3-4d5e-6f70-8192-a3b4c5d6e7f8
```

## API / parameter provenance

Verified against the installed official SDK `huaweicloudsdknat` and the KooCLI
official CLI command reference; no endpoint or parameter was inferred from
naming patterns:

- `huaweicloudsdknat` v2 `nat_client._list_nat_gateways_http_info` declares
  `method = GET`, `resource_path = /v2/{project_id}/nat_gateways`.
- KooCLI service/operation `NAT ListNatGateways` is the documented command for
  「查询公网NAT网关列表」
  (https://support.huaweicloud.com/clir-natgateway/nat-cli.html).
- `ListNatGatewaysRequest` real query parameters include: `tenant_id`, `id`,
  `enterprise_project_id`, `description`, `created_at`, `name`, `status`
  (csv), `spec` (csv), `admin_state_up`, `internal_network_id`, `router_id`,
  `limit`, `marker`, `sort_key`, `sort_dir`. The skill forwards
  `name` / `router_id` (plain strings) and `spec` / `status` (csv one-element
  lists) plus `limit` + id-`marker` paging. The next marker is the last
  gateway `id` of the previous page; a batch shorter than `limit` ends paging.
  The response model carries only `nat_gateways` (no `next_marker` /
  `page_info`), so those fields are never required.
- Response: `ListNatGatewaysResponse.nat_gateways` —
  `NatGatewayResponseBody` fields: `id`, `tenant_id`, `name`, `description`,
  `spec`, `status`, `admin_state_up`, `created_at`, `router_id`,
  `internal_network_id`, `enterprise_project_id`, `session_conf`,
  `ngport_ip_address`, `billing_info`, `dnat_rules_limit`,
  `snat_rule_public_ip_limit`, `pps_max`, `bps_max`.
- `spec` values (official API docs): `1` 小型 / `2` 中型 / `3` 大型 /
  `4` 超大型 / `5` 企业型.
- Region catalog `huaweicloudsdknat.v2.region.nat_region.NatRegion` resolves
  official NAT endpoints (`cn-north-4` verified locally via `value_of`).
- IAM action `nat:natGateways:list` is the least-privilege read-only
  permission for this call (official permission matrix nat_api_0029).

## Environment note

The development environment did not have the `hcloud` binary installed, so the
KooCLI path could not be executed live; its command/parameter shape is derived
from the official KooCLI CLI command reference and the SDK request model
(`ListNatGatewaysRequest`). The SDK fallback path was import-verified against
the installed `huaweicloudsdknat` (the `huaweicloudsdknat` package ships the
v2 NAT client only — v2 is the current public-NAT-gateway API family).

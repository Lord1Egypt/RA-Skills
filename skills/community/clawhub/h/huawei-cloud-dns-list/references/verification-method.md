# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/network/dns/huawei-cloud-dns-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_dns_via_sdk` mock plus live regression
  tests that construct the real `ListPublicZonesRequest` /
  `ListPrivateZonesRequest` / `ListRecordSetsRequest` and `DnsRegion` when
  `huaweicloudsdkdns` is installed (skipped otherwise).
- Cases cover: write-intent guard, operation resolution, command construction
  (filters forwarded server-side), JSON extraction (including trailing
  diagnostics after a JSON body via `raw_decode`), failure classification
  (missing AK/SK / 403 / `DNS.1802` / `not authorized` /
  `no identity-based policy` / generic / `[USE_ERROR]` with rc=0), API error
  envelopes returned with rc=0 (never an empty list; `--output` creates no
  file), marker paging
  (last-id + `total_count` / empty page), SDK fallback (public zones / private
  zones / record sets / missing credentials / missing project id / unavailable),
  rendering, and all main() output modes.

## Live verification (when credentials exist)

```bash
hcloud configure list                                                    # profile check
hcloud DNS ListPublicZones --cli-region=cn-north-4 --limit=1             # API sanity
python3 scripts/list_dns.py --region cn-north-4                         # full flow
python3 scripts/list_dns.py --json | python3 -m json.tool >/dev/null    # JSON validity
python3 scripts/list_dns.py --names-only
python3 scripts/list_dns.py --type private                              # private zones
python3 scripts/list_dns.py --recordsets --record-type A                # record sets
python3 scripts/list_dns.py --id zone-0001                              # id filter
python3 scripts/list_dns.py --name example.com                          # name filter
```

## API / parameter provenance

Verified against the installed official SDK `huaweicloudsdkdns` (v2), no
endpoint or parameter was inferred from naming patterns:

- `dns_client._list_public_zones_http_info` declares `method = GET`,
  `resource_path = /v2/zones`.
- `dns_client._list_private_zones_http_info` declares `method = GET`,
  `resource_path = /v2/zones` (type=private).
- `dns_client._list_record_sets_http_info` declares `method = GET`,
  `resource_path = /v2/recordsets`.
- `ListPublicZonesRequest` / `ListPrivateZonesRequest` real query parameters:
  `type`, `limit` (0–500), `marker`, `offset`, `tags`, `name`, `id`, `status`,
  `search_mode`, `sort_key`, `sort_dir`, `enterprise_project_id`
  (`ListPrivateZonesRequest` additionally accepts `router_id`). `hcloud DNS
  ListPrivateZones --help` marks `type` as **required** (range: `private`) —
  the script therefore always sends `--type=private` for `ListPrivateZones`;
  `ListPublicZones` has no required `type` parameter.
- `ListRecordSetsRequest` real query parameters: `zone_type` (public/private),
  `marker`, `search_mode`, `limit` (0–500), `offset`, `tags`, `status`, `type`
  (record type), `name`, `id`, `records`, `sort_key`, `sort_dir`.
- Paging is `limit` + `marker`; per the API definition the marker is the **id of
  the last resource of the previous page**. The response `metadata.total_count`
  reports the total matches and is used to stop paging early.
- `PublicZoneResp` fields: `id`, `name`, `description`, `email`, `zone_type`,
  `ttl`, `serial`, `status`, `record_num`, `pool_id`, `project_id`,
  `created_at`, `updated_at`, `links`, `tags`, `masters`,
  `enterprise_project_id`.
- `ListRecordSetsWithTags` fields: `id`, `name`, `description`, `zone_id`,
  `zone_name`, `type`, `ttl`, `records`, `create_at`, `update_at`, `status`,
  `default`, `project_id`, `links`, `tags`.
- Region catalog `huaweicloudsdkdns.v2.region.dns_region.DnsRegion` maps
  `cn-north-4 → https://dns.cn-north-4.myhuaweicloud.com`.
- IAM actions `dns:zone:list` / `dns:recordset:list` are the least-privilege
  read-only permissions for these calls.

## Environment note

The development environment did not have the `hcloud` binary installed, so the
KooCLI path could not be executed live; its command/parameter shape is derived
from the official SDK request model and the KooCLI
`hcloud <Service> <Operation> --cli-region=<region>` format standard. The SDK
fallback path was import-verified against the installed `huaweicloudsdkdns`.
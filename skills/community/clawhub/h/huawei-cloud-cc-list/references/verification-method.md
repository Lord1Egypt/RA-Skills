# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/network/cc/huawei-cloud-cc-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_connections_via_sdk` mock (no real SDK
  import, no network), plus a live regression test that constructs the real
  `ListCloudConnectionsRequest` when `huaweicloudsdkcc` is installed (skipped
  otherwise).
- Cases cover: write-intent guard, command construction (filters forwarded
  server-side), JSON extraction, failure classification (missing AK/SK / 403 /
  generic / `[USE_ERROR]` with rc=0), marker paging (next_marker / full page /
  empty), SDK fallback (success / unavailable), rendering, and all main()
  output modes.

## Live verification (when credentials exist)

```bash
hcloud configure list                                                  # profile check
hcloud CC ListCloudConnections --cli-region=cn-north-4 --limit=1       # API sanity
python3 scripts/list_cc.py --region cn-north-4                         # full flow
python3 scripts/list_cc.py --json | python3 -m json.tool >/dev/null    # JSON validity
python3 scripts/list_cc.py --names-only
python3 scripts/list_cc.py --status ACTIVE                             # server-side filter
python3 scripts/list_cc.py --name cc-demo
```

## API / parameter provenance

Verified against the installed official SDK `huaweicloudsdkcc` (3.1.218), no
endpoint or parameter was inferred from naming patterns:

- `huaweicloudsdkcc` v3 `cc_client._list_cloud_connections_http_info`
  declares `method = GET`, `resource_path = /v3/{domain_id}/ccaas/cloud-connections`.
- `ListCloudConnectionsRequest` real query parameters: `limit`, `marker`, `id`,
  `name`, `description`, `enterprise_project_id`, `status`, `type`,
  `used_scene` (`id` / `name` / `status` are list / csv values; `limit` range
  1–2000).
- Paging is `limit` + `marker`; the next page marker is the response
  `page_info.next_marker`, and `page_info.current_count` reports the page size.
- `CloudConnection` fields: `id`, `name`, `description`, `domain_id`,
  `enterprise_project_id`, `created_at`, `updated_at`, `tags`, `status`,
  `admin_state_up`, `used_scene`, `network_instance_number`,
  `bandwidth_package_number`, `inter_region_bandwidth_number`.
- Region catalog `huaweicloudsdkcc.v3.region.cc_region.CcRegion` maps
  `cn-north-4 → https://cc.myhuaweicloud.com` (CC is served through a global
  endpoint).
- IAM action `cc:cloudConnections:list` confirmed through
  `IAM GetAuthorizationSchemaV5 --service_code=cc`.

## Environment note

The development environment did not have the `hcloud` binary installed, so the
KooCLI path could not be executed live; its command/parameter shape is derived
from the official SDK request model and the KooCLI
`hcloud <Service> <Operation> --cli-region=<region>` format standard. The SDK
fallback path was import-verified against the installed `huaweicloudsdkcc`.

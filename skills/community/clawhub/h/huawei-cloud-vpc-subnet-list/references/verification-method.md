# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/network/vpc/huawei-cloud-vpc-subnet-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_subnets_via_sdk` mock (no real SDK
  import, no network), plus live regression tests that construct the real
  `ListSubnetsRequest` and `VpcRegion` when `huaweicloudsdkvpc` is installed
  (skipped otherwise).
- Cases cover: write-intent guard, command construction (vpc_id filter forwarded
  server-side), JSON extraction, failure classification (missing AK/SK / 403 /
  generic / `[USE_ERROR]` with rc=0), marker paging (next_marker / full page /
  empty), SDK fallback (success / missing credentials / missing project id /
  unavailable), rendering, and all main() output modes.

## Live verification (when credentials exist)

```bash
hcloud configure list                                            # profile check
hcloud VPC ListSubnets --cli-region=cn-north-4 --limit=1         # API sanity
python3 scripts/list_subnet.py --region cn-north-4               # full flow
python3 scripts/list_subnet.py --json | python3 -m json.tool >/dev/null  # JSON validity
python3 scripts/list_subnet.py --names-only
python3 scripts/list_subnet.py --vpc-id <vpc-id>                 # server-side filter
```

## API / parameter provenance

Verified against the installed official SDK `huaweicloudsdkvpc`, no endpoint or
parameter was inferred from naming patterns:

- `huaweicloudsdkvpc` v2 `vpc_client._list_subnets_http_info` declares
  `method = GET`, `resource_path = /v1/{project_id}/subnets`.
- `ListSubnetsRequest` real query parameters are exactly: `limit` (int),
  `marker` (str), `vpc_id` (str). `marker` is the resource id from which paging
  starts (empty = first page); `vpc_id` filters by the owning VPC and is
  required under enterprise-project fine-grained authorization.
- The response object is `ListSubnetsResponse` with the `subnets` list of
  `Subnet` objects; KooCLI prints the response `page_info.next_marker` for
  paging. The typed SDK response does not surface `page_info`, so the SDK
  fallback continues from the last returned subnet id when a full page is
  returned.
- `Subnet` fields include: `id`, `name`, `cidr`, `gateway_ip`, `vpc_id`,
  `status`, `description`, `availability_zone`, `available_ip_address_count`,
  `neutron_network_id`, `neutron_subnet_id`, `dhcp_enable`, `primary_dns`,
  `secondary_dns`, `dns_list`, `ipv6_enable`, `cidr_v6`, `gateway_ip_v6`,
  `neutron_subnet_id_v6`, `scope`, `tenant_id`, `extra_dhcp_opts`,
  `enable_network_address_usage_metrics`, `created_at`, `updated_at`.
- Region catalog `huaweicloudsdkvpc.v2.region.vpc_region.VpcRegion` maps
  `cn-north-4 → https://vpc.cn-north-4.myhuaweicloud.com`.
- IAM action `vpc:subnets:list` (VPC service, `subnets` resource) is the
  least-privilege read-only permission for this call.

## Environment note

If the development environment does not have the `hcloud` binary installed, the
KooCLI path cannot be executed live; its command/parameter shape is derived from
the official SDK request model and the KooCLI
`hcloud <Service> <Operation> --cli-region=<region>` format standard. The SDK
fallback path is import-verified against the installed `huaweicloudsdkvpc`.
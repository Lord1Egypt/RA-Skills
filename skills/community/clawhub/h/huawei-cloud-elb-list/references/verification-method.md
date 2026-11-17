# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/network/elb/huawei-cloud-elb-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_loadbalancers_via_sdk` mock (no real SDK
  import, no network), plus live regression tests that construct the real
  `ListLoadBalancersRequest` and `ElbRegion` when `huaweicloudsdkelb` is installed
  (skipped otherwise).
- Cases cover: write-intent guard, command construction (filters forwarded
  server-side), JSON extraction, failure classification (missing AK/SK / 403 /
  generic / `[USE_ERROR]` with rc=0), marker paging (next_marker / full page /
  empty), SDK fallback (success / missing credentials / missing project id /
  unavailable), standardization (`id` + `name` only / `name`→`id` fallback /
  `-` defaults), rendering, Markdown generation (`| ID | 名称 |` table / empty
  document / `|` escaping / `--md-out` / `--no-md` / `--json` never writes), and
  all main() output modes.

## Live verification (when credentials exist)

```bash
hcloud configure list                                                    # profile check
hcloud ELB ListLoadbalancers --cli-region=cn-north-4 --limit=1           # API sanity
python3 scripts/list_elb.py --region cn-north-4                          # standardized table + Markdown doc
cat elb-list.md                                                          # Markdown doc: | ID | 名称 |
python3 scripts/list_elb.py --region cn-north-4 --no-md                  # standardized table only
python3 scripts/list_elb.py --json | python3 -m json.tool >/dev/null     # JSON validity (no Markdown)
python3 scripts/list_elb.py --names-only --no-md
python3 scripts/list_elb.py --provisioning-status ACTIVE                 # server-side filter
python3 scripts/list_elb.py --id lb-0001
python3 scripts/list_elb.py --vip-address 192.168.0.10
```

## API / parameter provenance

Verified against the installed official SDK `huaweicloudsdkelb`, no endpoint or
parameter was inferred from naming patterns:

- `huaweicloudsdkelb` v3 `elb_client._list_load_balancers_http_info` declares
  `method = GET`, `resource_path = /v3/{project_id}/elb/loadbalancers`.
- `ListLoadBalancersRequest` real query parameters include: `marker`, `limit`,
  `page_reverse`, `id`, `name`, `description`, `admin_state_up`,
  `include_recycle_bin`, `provisioning_status`, `operating_status`,
  `guaranteed`, `vpc_id`, `vip_port_id`, `vip_address`, `vip_subnet_cidr_id`,
  `ipv6_vip_*`, `eips`, `publicips`, `availability_zone_list`, `l4_flavor_id`,
  `l7_flavor_id`, `billing_info`, `member_device_id`, `member_address`,
  `enterprise_project_id`, `ip_version`, `deletion_protection_enable`,
  `elb_virsubnet_type`, `autoscaling`, `protection_status`, `global_eips`,
  `log_topic_id`, `log_group_id` (`id` / `name` / `vpc_id` /
  `provisioning_status` / `operating_status` / `enterprise_project_id` /
  `vip_address` are list / multi values; `limit` range 0–2000). Because these
  filters are array-typed, KooCLI requires the indexed form on the command line
  (`--key.1=value`, e.g. `--provisioning_status.1=ACTIVE`); the bare
  `--key=value` form is rejected with `[USE_ERROR]Invalid parameter`.
- Paging is `limit` + `marker`; the next page marker is the response
  `page_info.next_marker`, and `page_info.current_count` reports the page size.
- `ListLoadBalancersResponse` fields: `loadbalancers` (list of `LoadBalancer`),
  `page_info` (`PageInfo`: `previous_marker` / `next_marker` / `current_count`),
  `request_id`.
- `LoadBalancer` fields: `id`, `name`, `description`, `provisioning_status`,
  `operating_status`, `admin_state_up`, `provider`, `pools`, `listeners`,
  `project_id`, `vip_subnet_cidr_id`, `vip_address`, `vip_port_id`, `tags`,
  `created_at`, `updated_at`, `guaranteed`, `vpc_id`, `eips`, `ipv6_vip_*`,
  `availability_zone_list`, `enterprise_project_id`, `billing_info`,
  `l4_flavor_id`, `l4_scale_flavor_id`, `l7_flavor_id`, `l7_scale_flavor_id`,
  `gw_flavor_id`, `loadbalancer_type`, `publicips`, `global_eips`,
  `elb_virsubnet_ids`, `elb_virsubnet_type`, `ip_target_enable`,
  `frozen_scene`, `deletion_protection_enable`, `autoscaling`,
  `public_border_group`, `charge_mode`, `service_lb_mode`, `instance_type`,
  `instance_id`, `protection_status`, `protection_reason`, `log_group_id`,
  `log_topic_id`, `custom_qos_limit`.
- Region catalog `huaweicloudsdkelb.v3.region.elb_region.ElbRegion` maps
  `cn-north-4 → https://elb.cn-north-4.myhuaweicloud.com`.
- IAM action `elb:loadbalancers:list` is the least-privilege read-only
  permission for this call.

## Environment note

The development environment did not have the `hcloud` binary installed, so the
KooCLI path could not be executed live; its command/parameter shape is derived
from the official SDK request model and the KooCLI
`hcloud <Service> <Operation> --cli-region=<region>` format standard. The SDK
fallback path was import-verified against the installed `huaweicloudsdkelb`
(`ElbClient`, `ListLoadBalancersRequest`, `ElbRegion`).
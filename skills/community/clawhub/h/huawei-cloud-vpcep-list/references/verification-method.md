# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/network/vpcep/huawei-cloud-vpcep-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested through a fake SDK injected via
  `list_vpcep._load_sdk` (captures credentials, region, request kwargs and
  client method per view), plus live import / request-model regression tests
  that run when `huaweicloudsdkvpcep` is installed (skipped otherwise).
- Cases cover: write-intent guard, view resolution, command construction
  (per-view params, offset paging, no mutating flags), JSON extraction,
  payload-error classification (403 with rc=0, invalid ID), failure
  classification (missing AK/SK / 403 / generic / `[USE_ERROR]` with rc=0),
  offset paging (short page / `total_count` / empty / page-size clamp), SDK
  fallback (three views / env credentials / missing credentials / missing
  project id / unknown region / auth failure / invalid ID), client-side filters,
  rendering (fixed-column table and Markdown / missing `-` / boolean 是/否 /
  abnormal marker / empty header), atomic write, and all main() output modes.

## Live verification (when credentials and VPCEP permission exist)

```bash
hcloud configure list                                                          # profile check
hcloud VPCEP ListEndpoints --cli-region=cn-north-4 --limit=1                    # API sanity
python3 scripts/list_vpcep.py --region cn-north-4                              # endpoint view
python3 scripts/list_vpcep.py --view service --table --region cn-north-4        # service view
python3 scripts/list_vpcep.py --view public --table --region cn-north-4         # public view
python3 scripts/list_vpcep.py --json | python3 -m json.tool >/dev/null          # JSON validity
python3 scripts/list_vpcep.py --status failed --table                           # abnormal only
python3 scripts/list_vpcep.py --vpc-id <valid-vpc-id>                           # VPC filter
python3 scripts/list_vpcep.py --name <service-name> --fuzzy --view public       # fuzzy filter
python3 scripts/list_vpcep.py --format md --output vpcep.md                     # Markdown export
```

## API / parameter provenance (no naming guesses)

Verified against the installed official SDK `huaweicloudsdkvpcep` 3.1.221 and
KooCLI 7.3.12 `--help` output:

- `vpcep_client._list_endpoints_http_info`: `method = GET`,
  `resource_path = /v1/{project_id}/vpc-endpoints`.
- `vpcep_client._list_endpoint_service_http_info`: `method = GET`,
  `resource_path = /v1/{project_id}/vpc-endpoint-services`.
- `vpcep_client._list_service_public_details_http_info`: `method = GET`,
  `resource_path = /v1/{project_id}/vpc-endpoint-services/public`.
- `ListEndpointsRequest` real query parameters: `endpoint_service_name`
  (case-insensitive fuzzy), `vpc_id`, `id`, `limit` (0–500), `offset`,
  `sort_key` (`create_at|update_at`), `sort_dir` (`asc|desc`).
- `ListEndpointServiceRequest`: `endpoint_service_name`, `id`, `status`
  (`creating|available|failed|deleting`), `sort_key`, `sort_dir`, `limit`
  (0–1000), `offset`, `public_border_group`, `net_type`.
- `ListServicePublicDetailsRequest`: `limit` (0–1000), `offset`,
  `endpoint_service_name` (case-sensitive fuzzy), `id`, `sort_key`, `sort_dir`.
- Response models: `ListEndpointsResponse.endpoints` is a list of
  `EndpointResponseBody` (`id`, `service_type`, `status`, `active_status`,
  `endpoint_service_name`, `marker_id`, `endpoint_service_id`, `enable_dns`,
  `dns_names`, `ip`, `vpc_id`, `subnet_id`, `created_at`, `updated_at`,
  `project_id`, `tags`, `error`, `whitelist`, `enable_whitelist`, `routetables`,
  `description`, `policy_statement`, `policy_document`, `endpoint_pool_id`,
  `public_border_group`); `ListEndpointServiceResponse.endpoint_services` is a
  list of `ServiceList` (`id`, `owner`, `service_name`, `service_type`,
  `created_at`, `is_charge`, `enable_policy`, `port_id`, `server_type`,
  `vpc_id`, `approval_enabled`, `status`, `updated_at`, `project_id`,
  `domain_id`, `ports`, `ip`, `tags`, `connection_count`, `tcp_proxy`, `error`,
  `description`, `supported_editions`, `public_border_group`);
  `ListServicePublicDetailsResponse.endpoint_services` is a list of
  `EndpointService` (`id`, `owner`, `service_name`, `service_type`,
  `created_at`, `is_charge`, `enable_policy`).
- `VpcepRegion` maps `cn-north-4 → https://vpcep.cn-north-4.myhuaweicloud.com`.
- IAM actions `vpcep:endpoints:list`, `vpcep:endpointServices:list`,
  `vpcep:endpointServices:listPublic` are the read-only permissions required by
  the three views (confirmed from live `common.01010013` authorization
  messages).

## Environment note

The development environment had KooCLI 7.3.12 and a credential profile, but the
account lacked VPCEP list permissions. The three operations therefore returned
`common.01010013 / not authorized` with HTTP-equivalent 403; the script
classified each as an IAM 403, exited 1 and printed the Chinese actionable hint
(no traceback). The successful rc=0 path (all three views, filters, paging,
Markdown) was verified with a mock `hcloud` whose output has the same JSON shape
as the official API. Real read-only rc=0 smoke is delegated to QA with an
account that has the three list permissions.

# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/network/apig/huawei-cloud-apig-instance-list
python3 -m unittest discover -s tests -v
```

- `hcloud` is replaced by a `run_hcloud` mock (`FakeHcloud`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested with a mocked SDK client plus fake
  `huaweicloudsdkapig.v2` request classes injected into `sys.modules`, so the
  request field construction (`offset` / `limit` / `instance_id`) is asserted
  without importing the real SDK.
- Cases cover: write-intent guard, command construction, JSON extraction and
  error-envelope detection, failure classification (missing AK/SK / 401 / 403 /
  generic / `[USE_ERROR]` with rc=0 / API envelope with rc=0), offset/limit
  paging (page step, second-page offset, limit stop, total bound, empty page),
  SDK fallback (CLI missing / missing credentials / SDK unavailable / request
  construction), client-side filters (exact / fuzzy / status), rendering, and
  all `main()` modes including empty hints, drill-down, invalid instance id,
  write intent and `--limit` boundaries.
- Result at build time: 67 tests, all passing.

## CLI smoke (creator test-cli-commands.sh, live)

```bash
bash <creator>/scripts/test-cli-commands.sh -s skills/network/apig/huawei-cloud-apig-instance-list -e cli
```

Result at build time: 3/3 PASS (ListInstancesV2 basic list, `--status=Running`
filter, `--instance_name` lookup — all read-only GET).

## Live verification (read-only, when credentials exist)

```bash
hcloud configure list
hcloud APIG ListInstancesV2 --cli-region=cn-north-4 --limit=1
python3 scripts/list_apig_instances.py --region cn-north-4            # compact, rc=0
python3 scripts/list_apig_instances.py --table                        # 9 documented columns
python3 scripts/list_apig_instances.py --json | python3 -m json.tool >/dev/null
python3 scripts/list_apig_instances.py --status Running --name apig --fuzzy
python3 scripts/list_apig_instances.py --instance-id <valid-id>       # API drill-down, rc=0
python3 scripts/list_apig_instances.py --instance-id <valid-id> --limit 2 --json
python3 scripts/list_apig_instances.py --instance-id 00000000000000000000000000000000   # rc=1
python3 scripts/list_apig_instances.py --delete-api                    # rc=1, guard
```

Observed at build time in `cn-north-4`: one instance (`apig-skill-test`,
`Running`, spec `BASIC`) and 8 APIs under it; `--limit 2` returned two records
via two paged requests; an all-zero instance id returned `实例不存在` with
exit code 1; `--delete-api` was blocked by the guard with exit code 1.

SDK fallback was verified live as well, with `hcloud` hidden and the official
SDK installed in a throwaway target directory:

```bash
PYTHONPATH=<sdk-dir> APIG_LIST_HCLOUD_BIN=/nonexistent-hcloud \
  HUAWEICLOUD_SDK_PROJECT_ID=<project-id> \
  python3 scripts/list_apig_instances.py --limit=5           # rc=0, same output
```

## API / parameter provenance

Verified against the official SDK package `huaweicloudsdkapig` 3.1.218 and the
KooCLI 7.3.12 `--help` output; no endpoint or parameter was inferred from
naming patterns:

- `apig_client._list_instances_v2_http_info`: `method = GET`,
  `resource_path = /v2/{project_id}/apigw/instances`; request model fields
  `offset`, `limit`, `instance_id`, `instance_name`, `status`; response
  `size`, `total`, `instances` (`RespInstanceBase`).
- `apig_client._list_apis_v2_http_info`: `method = GET`,
  `resource_path = /v2/{project_id}/apigw/instances/{instance_id}/apis`;
  request model fields `instance_id` (path), `offset`, `limit`, `id`, `name`,
  `group_id`, `req_protocol`, `req_method`, `req_uri`, `auth_type`, `env_id`,
  ...; response `size`, `total`, `apis` (`ApiInfoPerPage`).
- KooCLI exposes the operations as **`ListInstancesV2`** and **`ListApisV2`**;
  `hcloud APIG ListInstances` (without the `V2` suffix) is *not* a valid
  operation in 7.3.12 and returns
  `[USE_ERROR]Operation ListInstances is not supported`.
- `RespInstanceBase` carries `id`, `project_id`, `instance_name`, `status`,
  `instance_status`, `type`, `spec`, `create_time` (epoch ms),
  `enterprise_project_id`, `eip_address`, `charging_mode`, `cbc_metadata`,
  `loadbalancer_provider`, `cbc_operation_locks`. It has **no** version /
  availability-zone / VPC field — the table shows `-` for those cells instead
  of inventing values.
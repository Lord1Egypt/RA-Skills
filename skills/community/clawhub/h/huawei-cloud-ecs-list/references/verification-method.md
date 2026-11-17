# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/compute/ecs/huawei-cloud-ecs-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_servers_via_sdk` mock (no real SDK
  import, no network), plus live regression tests that construct the real
  `ListServersDetailsRequest` and a real `ServerDetail` when
  `huaweicloudsdkecs` is installed (skipped otherwise).
- Cases cover: write-intent guard (including "filter values are not scanned"),
  command construction (status/name forwarded server-side), JSON extraction,
  failure classification (missing AK/SK / 403 / generic / `[USE_ERROR]` with
  rc=0), paging (count, full-page, empty), SDK fallback (success /
  unavailable), SDK field remapping, rendering, and all main() output modes.

## Live verification (when credentials exist)

The skill's entry point is the script; each command below exercises the
KooCLI path (or the SDK fallback) end-to-end:

```bash
python3 scripts/list_ecs.py --region cn-north-4
python3 scripts/list_ecs.py --json
python3 scripts/list_ecs.py --names-only
python3 scripts/list_ecs.py --status ACTIVE
python3 scripts/list_ecs.py --name ecs-web
```

The script prints to stdout only; it never writes a file. To check JSON
validity, pipe the `--json` output to `python3 -m json.tool` manually.

For reference, the raw KooCLI invocations the script wraps internally
(illustrative — require KooCLI installed):

```text
hcloud configure list
hcloud ECS ListServersDetails --cli-region=cn-north-4 --limit=1
```

## REST path provenance

`GET /v1/{project_id}/cloudservers/detail` comes from the official
`huaweicloudsdkecs` v2 client `_list_servers_details_http_info` `resource_path`
metadata (the same path the SDK fallback invokes through
`EcsClient.list_servers_details`). No endpoint was inferred from naming
patterns.

- The response model `ListServersDetailsResponse` exposes `count` (int, total)
  and `servers` (list[ServerDetail]) — paging is driven by `offset` / `limit`
  with `count` as the total when present.
- `ListServersDetailsRequest.openapi_types` confirms both `status` and `name`
  are real server-side query parameters (unlike RDS, which has no status
  parameter) — so `--status` is forwarded to the server rather than filtered
  client-side.
- The SDK `to_dict()` emits Python attribute names
  (`access_i_pv4`, `os_ext_a_zavailability_zone`); `sdk_server_to_dict()`
  remaps them to the OpenAPI wire names (`accessIPv4`,
  `OS-EXT-AZ:availability_zone`) via `ServerDetail.attribute_map` so the CLI
  and SDK paths produce the same shape.

## IAM action provenance

`ecs:servers:list` and the `ECSReadOnlyPolicy` system policy were verified
against the live IAM API on 2026-10-19:

- `GetAuthorizationSchemaV5(service_code="ecs")` (region cn-north-4) returns
  `ecs:servers:list` among the ECS actions.
- `ListPoliciesV5(policy_type="system")` returns `ECSReadOnlyPolicy`.

# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/compute/ecs/huawei-cloud-ecs-export-excel
python3 -m unittest discover -s tests -v
bash scripts/validate-skill.sh .
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is exercised via a `list_servers_via_sdk` mock (no real SDK
  import, no network) plus a direct credential-resolution test that blanks the
  known AK/SK environment variable names (no `os.environ` enumeration).
- The xlsx export is verified against a **real openpyxl install**: the test
  loads the produced workbook with `openpyxl.load_workbook` and asserts the
  sheet title, header row (`名称/ID/状态/规格/vCPU/内存/可用区/私网IP/公网IP`),
  data rows, summary row and cell fallbacks. The missing-openpyxl branch is
  covered by mocking the `_require_openpyxl` import path.
- Cases cover: write-intent guard (including filter/output value exclusion and
  the "following flag is still scanned" regression), command construction
  (status/name forwarded server-side, no write flags), JSON extraction, failure
  classification (missing AK/SK / 403 / generic / `[USE_ERROR]` with rc=0),
  paging (count, full-page, empty), `ECS_EXPORT_EXCEL_HCLOUD_ARGS` injection
  position (appended *after* the read-only argv, cannot rewrite the
  service/operation, guard-scanned), SDK fallback (missing env credentials /
  success / unavailable), SDK field remapping, normalization and rendering, and
  all `main()` output modes (xlsx writes file + prints path; table / json /
  empty / error paths).

## Live verification (when credentials exist)

```bash
python3 scripts/ensure_env.py                                                            # openpyxl + SDK ready
hcloud configure list                                                                    # profile check
hcloud ECS ListServersDetails --cli-region=cn-north-4 --limit=1                          # API sanity
python3 scripts/list_ecs_export_excel.py --region cn-north-4 --format table              # full flow
python3 scripts/list_ecs_export_excel.py --format json | python3 -m json.tool            # JSON validity
python3 scripts/list_ecs_export_excel.py --output /tmp/ecs.xlsx --summary                # xlsx export
python3 -c "from openpyxl import load_workbook; wb=load_workbook('/tmp/ecs.xlsx'); print(wb.sheetnames)"
```

## REST path provenance

`GET /v1/{project_id}/cloudservers/detail` comes from the official
`huaweicloudsdkecs` v2 client `_list_servers_details_http_info`
`resource_path` metadata (the same path the SDK fallback invokes through
`EcsClient.list_servers_details`). No endpoint was inferred from naming
patterns.

- The response model `ListServersDetailsResponse` exposes `count` (int, total)
  and `servers` (list[ServerDetail]) — paging is driven by `offset` / `limit`
  with `count` as the total when present.
- `ListServersDetailsRequest.openapi_types` confirms both `status` and `name`
  are real server-side query parameters — so `--status` / `--name` are
  forwarded to the server.
- The SDK `to_dict()` emits Python attribute names (`access_i_pv4`,
  `os_ext_a_zavailability_zone`); `sdk_server_to_dict()` remaps them to the
  OpenAPI wire names (`accessIPv4`, `OS-EXT-AZ:availability_zone`) via
  `ServerDetail.attribute_map` so the CLI and SDK paths produce the same shape.

## IAM action provenance

`ecs:servers:list` and the `ECSReadOnlyPolicy` system policy were verified
against the live IAM API on 2026-10-19:

- `GetAuthorizationSchemaV5(service_code="ecs")` (region cn-north-4) returns
  `ecs:servers:list` among the ECS actions.
- `ListPoliciesV5(policy_type="system")` returns `ECSReadOnlyPolicy`.

## Excel correctness

- Sheet title fixed to `ECS 实例清单`; header row fixed to
  `名称 / ID / 状态 / 规格 / vCPU / 内存 / 可用区 / 私网IP / 公网IP`.
- Every instance becomes exactly one data row; missing fields render as `-`.
- `--summary` appends a bolded `实例数量 | <N> | Region <region>` footer row.
- The workbook is saved through a temp file + atomic rename, then re-loaded with
  `openpyxl.load_workbook` in tests to confirm structural validity.

## Pass criteria

- All offline unit tests pass.
- `validate-skill.sh` reports zero Critical failures and SKILL.md within size
  limits.
- Error paths (missing AK/SK, hcloud missing, 403, openpyxl missing) exit
  non-zero with a clear Chinese hint on stderr; empty lists exit 0 with a
  friendly message and no `.xlsx` file.
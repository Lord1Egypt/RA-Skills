# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/compute/ecs/huawei-cloud-ecs-export-sorted
python3 -m unittest discover -s tests -v
bash scripts/validate-skill.sh .
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is exercised via a `list_servers_via_sdk` mock plus a direct
  credential-resolution test that blanks the known AK/SK environment variable
  names (no `os.environ` enumeration).
- The xlsx export is verified against a **real openpyxl install**: the test
  loads the produced workbook with `openpyxl.load_workbook` and asserts the
  sheet title, header row, data rows, summary row and cell fallbacks. The
  missing-openpyxl branch is covered by mocking the `_require_openpyxl` path.
- The csv export is verified by re-reading with `csv.reader`, and the UTF-8 BOM
  is asserted at the byte level.
- Sorting is verified directly on normalized records: alias resolution, unknown
  field, text / numeric / timestamp asc & desc, invalid-values-last, stable
  ties, and invalid order.
- Cases cover: write-intent guard (including filter/sort/output value exclusion
  and the "following flag is still scanned" regression), command construction
  (status/name forwarded server-side, no write flags), JSON extraction, failure
  classification (missing AK/SK / 403 / generic / `[USE_ERROR]` with rc=0),
  paging (count, full-page, empty), `ECS_EXPORT_SORTED_HCLOUD_ARGS` injection
  position (appended *after* the read-only argv, cannot rewrite the
  service/operation, guard-scanned), SDK fallback (missing env credentials /
  success / unavailable), SDK field remapping, normalization and rendering, and
  all `main()` output modes (xlsx / csv writes file + prints path; table / json
  / sorted / empty / unknown-field / error paths).

## Live verification (when credentials exist)

```bash
python3 scripts/ensure_env.py                                                      # openpyxl + SDK ready
hcloud configure list                                                              # profile check
hcloud ECS ListServersDetails --cli-region=cn-north-4 --limit=1                    # API sanity
python3 scripts/list_ecs_export_sorted.py --region cn-north-4 --format table       # full flow
python3 scripts/list_ecs_export_sorted.py --format json --sort-by created --order desc | python3 -m json.tool
python3 scripts/list_ecs_export_sorted.py --output /tmp/ecs.xlsx --sort-by name --summary
python3 scripts/list_ecs_export_sorted.py --format csv --sort-by vcpus --order desc --output /tmp/ecs.csv
python3 -c "from openpyxl import load_workbook; wb=load_workbook('/tmp/ecs.xlsx'); print(wb.sheetnames)"
```

## REST path provenance

`GET /v1/{project_id}/cloudservers/detail` comes from the official
`huaweicloudsdkecs` v2 client `_list_servers_details_http_info` `resource_path`
metadata (the same path the SDK fallback invokes through
`EcsClient.list_servers_details`). No endpoint was inferred from naming patterns.

- `ListServersDetailsResponse` exposes `count` (int, total) and `servers`
  (list[ServerDetail]) — paging is driven by `offset` / `limit` with `count` as
  the total when present.
- Neither `ListServersDetailsRequest` nor the OpenAPI offers a server-side sort
  parameter — hence the sort is applied **locally** after paging.
- `ListServersDetailsRequest.openapi_types` confirms both `status` and `name`
  are real server-side query parameters — so `--status` / `--name` are forwarded
  to the server.
- The SDK `to_dict()` emits Python attribute names (`access_i_pv4`,
  `os_ext_a_zavailability_zone`); `sdk_server_to_dict()` remaps them to the
  OpenAPI wire names (`accessIPv4`, `OS-EXT-AZ:availability_zone`) via
  `ServerDetail.attribute_map` so the CLI and SDK paths produce the same shape.

## Sort correctness

- Field aliases resolve to normalized record keys (English + Chinese).
- Numeric fields (`vcpus`, `ram`) compare as numbers; `created` compares as an
  ISO-8601 timestamp (falling back to text); the rest compare case-insensitively.
- Records with a missing/unparseable sort key are placed **last** for both
  `asc` and `desc`; the sort is stable, so ties keep their original order.
- Omitting `--sort-by` preserves the query order.

## IAM action provenance

`ecs:servers:list` and the `ECSReadOnlyPolicy` system policy are the standard
read-only ECS list grants; no write action is used by this skill.

## Report correctness

- xlsx sheet title fixed to `ECS 实例清单`; header row fixed to
  `名称 / ID / 状态 / 规格 / vCPU / 内存 / 可用区 / 私网IP / 公网IP / 创建时间`.
- csv is written with a UTF-8 BOM so Excel opens it without mojibake.
- Every instance becomes exactly one data row; missing fields render as `-`.
- `--summary` appends `实例数量 | <N> | Region <region>` as the footer row.
- The workbook is saved through a temp file + atomic rename, then re-loaded with
  `openpyxl.load_workbook` in tests to confirm structural validity.

## Pass criteria

- All offline unit tests pass.
- `validate-skill.sh` reports zero Critical failures and SKILL.md within size
  limits.
- Error paths (missing AK/SK, hcloud missing, 403, unknown sort field, openpyxl
  missing) exit non-zero with a clear Chinese hint on stderr; empty lists exit 0
  with a friendly message and no report file.
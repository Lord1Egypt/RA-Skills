# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/devtools/cse/huawei-cloud-cse-engine-list
python3 -m unittest discover -s tests -v
```

Result: **61 tests, all passing**.

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested with fake `huaweicloudsdkcore` /
  `huaweicloudsdkcse` modules injected into `sys.modules`, so request shapes
  (`offset` / `limit` as string / `type`, project id on the credentials) and
  error paths are verified without any SDK installed or called.
- Cases cover: write-intent guard (mutating verbs blocked / selector values not
  scanned / operation whitelist), command construction (region, limit, offset,
  type, project id), JSON extraction (object / bare array / noise / invalid),
  response envelope (`{"total","data"}` / bare array / unknown shape),
  normalization (camelCase / snake_case / missing fields / region fill), time
  formatting (epoch ms / epoch s / ISO string), name filters (exact / fuzzy /
  case-insensitive), paging (total-driven / full-page fallback / short page /
  max-page guard), failure classification (missing AK/SK / 403 / `[USE_ERROR]`
  with rc=0 / network / generic / API error body with rc=0), SDK fallback
  (success / missing credentials / auth error / hcloud absent), rendering, and
  all main() output modes (concise / table / json / empty / guard rejection).

## KooCLI provenance (verified live, 2026-11-09)

`hcloud CSE ListEngines --cli-region=cn-north-4 --help` (KooCLI 7.3.12)
returns:

```text
Service: CSE
Description: This API is used to query the microservice engine list.
Method: GET
Params:
  --cli-region   required   string   Region
  --project_id   required   string   path
  --limit        optional   string   query   Number of items displayed on each page.
  --offset        optional   integer  query   Offset.
  --type          optional   string   query   set ALL/CSE/Nacos/MicroGateway to get engine list.
```

The script builds exactly this call; `--limit` is passed as a string to match
the metadata.

## Live read-only smoke

```bash
python3 scripts/list_cse_engines.py --region cn-north-4
```

In the authoring environment the tenant holds no CSE read permission, so the
call returns the OpenAPI error body with exit code 0 from KooCLI:

```json
{
  "error_code": "SVCSTG.00509431",
  "error_message": "User does not have valid roles to read!, User is not authorized to perform: cse:engine:list"
}
```

The script detects the `error_code` / `error_message` body (KooCLI may exit 0),
classifies it as an authorization problem and exits 1 with the explicit
`无权限访问 CSE 微服务引擎，请检查 IAM 权限（cse:engine:list）` hint — no
traceback, no partial data. This also confirms the required IAM action. On a
tenant granted `cse:engine:list` the same call prints the engine inventory (or
the 未找到微服务引擎 empty-list message) and exits 0.

## SDK provenance

`huaweicloudsdkcse` (3.1.221) ships only module `v1`; `CseClient.list_engines`
is the method for this API:

- `huaweicloudsdkcse/v1/cse_client.py` — `_list_engines_http_info`:
  `method = GET`, `resource_path = /v2/{project_id}/enginemgr/engines`
- `ListEnginesRequest` — `offset` (int), `limit` (str), `type` (str)
- `ListEnginesResponse` — `total` (int), `data` (list of `EngineSimpleInfo`)

So the "v2" in the API path is the REST version; the Python SDK module is
`v1`. The fallback imports `huaweicloudsdkcse.v1` accordingly.
# Verification Method

## Data source provenance (no guessing)

The catalog source was established from the **official SDK source** (Phase 2
CLI→SDK→API research), never inferred from naming patterns:

- `huaweicloudsdkbss` v2 `bss_client._list_service_types_http_info` declares:

  ```text
  method        = GET
  resource_path = /v2/products/service-types
  response_type = ListServiceTypesResponse
  ```

  and the client method `BssClient.list_service_types(request)` (docstring:
  「查询云服务类型列表」).
- `ListServiceTypesRequest` real parameters: `x_language` (request header
  `X-Language`, `zh_CN` / `en_US`), `limit` (default 10), `offset` (default 0),
  `service_type_name` (fuzzy match: prefix / suffix / middle, length 1–128).
- `ListServiceTypesResponse` fields: `total_count` (int) and `service_types`
  (`list[ServiceTypes]`).
- `ServiceTypes` fields: `service_type_name` (云服务类型名称), `service_type_code`
  (云服务类型编码), `abbreviation` (云服务类型缩写).
- BSS is a **global** service; the documented endpoint is
  `https://bss.myhuaweicloud.com` and the SDK client is built with
  `GlobalCredentials` + `with_endpoints` (not `BasicCredentials` + `with_region`).

Execution order (CLI → SDK → API): KooCLI `hcloud BSS ListServiceTypes` is
primary; when the hcloud binary is absent the script falls back to the
`huaweicloudsdkbss` v2 SDK (same REST path). Both paths are strictly read-only.

## Offline unit tests (primary, CI-safe)

```bash
cd skills/catalog/huawei-cloud-product-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_products_via_sdk` mock (no real SDK
  import, no network), plus live regression tests that construct the real
  `ListServiceTypesRequest` and the `BssClient` builder when
  `huaweicloudsdkbss` is installed (skipped otherwise).
- Cases cover: write-intent guard (read passes / create / delete / update /
  transfer / reclaim / adjust / freeze / normalized variants / Chinese verbs /
  operation whitelist), command construction (`--service_type_name` forwarded
  server-side; no write flags ever added), JSON extraction, failure
  classification (missing AK/SK / 403 / generic / `[USE_ERROR]` with rc=0),
  offset paging (total_count / full page / empty), SDK fallback (success /
  GlobalCredentials + `with_endpoints` / missing credentials / unavailable),
  standardization (name + code + abbreviation / `-` defaults), rendering, the
  client-side `--code` filter, and all main() output modes.

## Live verification (when credentials exist)

```bash
hcloud configure list                                                    # profile check
hcloud BSS ListServiceTypes --cli-region=cn-north-1 --limit=1            # API sanity
python3 scripts/list_products.py --region cn-north-1                     # 名称/编码/缩写 table
python3 scripts/list_products.py --json | python3 -m json.tool >/dev/null
python3 scripts/list_products.py --names-only
python3 scripts/list_products.py --name 弹性                            # server-side fuzzy filter
python3 scripts/list_products.py --code obs                              # client-side code filter
```

## Environment note

The development environment did not have the `hcloud` binary installed (nor
AK/SK), so the KooCLI path could not be executed live; its command/parameter
shape is derived from the official SDK request model and the KooCLI
`hcloud <Service> <Operation> --cli-region=<region>` format standard. The SDK
fallback path was import-verified against the installed `huaweicloudsdkbss`
(`BssClient`, `ListServiceTypesRequest`, `ServiceTypes`). Real read-only
verification is performed out-of-band by the QA stage.
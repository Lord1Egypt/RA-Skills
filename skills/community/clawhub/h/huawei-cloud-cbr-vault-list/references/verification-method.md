# Verification Method

## 1. CLI operation research (Phase 2)

The KooCLI operation was verified live — not inferred:

```text
hcloud CBR --help
# Available Operations list contains: ListVault   (singular)

hcloud CBR ListVault --cli-region=cn-north-4 --help
# Params: --cli-region (required), --project_id (required, path),
#         --cloud_type, --enterprise_project_id, --id.[N], --limit, --name,
#         --object_type, --policy_id, --protect_type, --resource_ids,
#         --status, --offset
```

`hcloud CBR ListVaults --cli-region=cn-north-4` returns
`[USE_ERROR]Operation ListVaults is not supported.` — the singular operation
name is mandatory.

## 2. REST endpoint (no guessing)

Read from the official SDK source:

```text
huaweicloudsdkcbr/v1/cbr_client.py :: _list_vault_http_info
  "method": "GET",
  "resource_path": "/v3/{project_id}/vaults"
```

The same `_http_info` returns `ListVaultResponse` with
`vaults` / `count` / `limit` / `offset`.

## 3. Request / response model

`ListVaultRequest.openapi_types` (verified from the installed SDK):
`limit`, `name`, `offset`, `cloud_type`, `protect_type`, `object_type`,
`enterprise_project_id`, `id` (list[str]), `policy_id`, `status`,
`resource_ids`, `availability_zone`.

`Vault.attribute_map` carries the vault identity / project fields; capacity,
status, object type, protection type and `charging_mode` live in the nested
`billing` (Billing) object. The script flattens `billing` for the table and for
client-side filtering, so 名称 / ID / 状态 / 容量 / 计费模式 are always visible.

## 4. Live call (read-only)

A real read-only call was executed in the development session:

```text
hcloud CBR ListVault --cli-region=cn-north-4 --limit=2
```

The response was `BackupService.0403 ... not authorized to perform:
cbr:vaults:list` — i.e. the operation and parameters are accepted by the
service, but the development account's credential lacks the `cbr:vaults:list`
permission. This confirms:

- the operation path / parameter set is valid (a wrong operation or parameter
  returns `[USE_ERROR]`, not a CBR authorization error);
- the 403 classification path and the IAM action literal `cbr:vaults:list` are
  correct.

Successful data retrieval (an actual non-empty vault list) therefore must be
verified by the QA stage with an account that holds `cbr:vaults:list`.

## 5. Offline unit tests

```bash
python3 -m unittest discover -s tests -v
```

The suite mocks the hcloud subprocess (no credentials, no network) and covers:

- write-intent guard: read-only argv passes; create / delete / update /
  restore / copy / import / replicate / migrate / associate / bind / remove /
  add and CBR mutating operation names are blocked; `ListVault` is not blocked;
  filter values and `--offset` are not blocked; the operation whitelist rejects
  anything but `ListVault`.
- command construction: region + limit + offset, native underscore-form
  filters, `--id.1` for the vault ID, no write flags.
- JSON / vault extraction and error-payload classification (`BackupService.0403`).
- paging: count-aware multi-page, short-page stop, duplicate-ID guard.
- SDK fallback: hcloud-missing trigger, unavailable SDK, request construction,
  `Vault` remapping including nested `billing`.
- client-side filters: name / status / object_type / protect_type /
  enterprise_project_id / vault_id.
- rendering: preferred columns (name/id/status/size/charging_mode), missing
  field `-`, names-only summary.
- `main()`: default table, `--json`, `--names-only`, empty list, filter suffix,
  error path, guard path.

## 6. Structure / specification check

```bash
bash <skill-creator>/scripts/validate-skill.sh -s skills/storage/cbr/huawei-cloud-cbr-vault-list
```

The skill targets zero FAIL checks against 华为云Skill检查规范.
# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/network/er/huawei-cloud-er-list
python3 -m unittest discover -s tests -v
```

- `hcloud` is replaced by a `subprocess.run` mock (`FakeRunner`) — no
  credentials, no network, deterministic.
- The SDK fallback is tested with fake SDK request / client / response objects;
  the real `huaweicloudsdker` request classes were also used during development
  to confirm signatures.
- Cases cover: write-intent guard (read passes / create / delete / update /
  associate / disassociate / enable / disable / normalized variants / per-
  resource operation whitelist / allowed `--resource` values not blocked),
  command construction (array forms `--state.1` / `--id.1` / `--vpc_id.1`,
  `--owned_by_self`, `--sort_key.1` / `--sort_dir.1`, route-table booleans,
  marker paging), JSON extraction, JSON error bodies with exit code 0 (403 and
  404), failure classification, marker paging, SDK fallback dispatch, SDK
  request/response wiring, rendering (ER 8 columns, attachment 6 columns,
  abnormal section separation), local name filters, and all `main()` output
  modes.

`bash -n` / `py_compile` / `json.tool` checks:

```bash
bash -n scripts/ensure_cli.sh
bash -n scripts/install_cli.sh
python3 -m py_compile scripts/list_er.py
python3 -m json.tool templates/test-vars.json >/dev/null
```

## Live read-only verification

```bash
hcloud configure list
hcloud ER ListEnterpriseRouters --cli-region=cn-north-4 --limit=1
python3 scripts/list_er.py --region cn-north-4
python3 scripts/list_er.py --region cn-north-4 --table
python3 scripts/list_er.py --region cn-north-4 --json | python3 -m json.tool >/dev/null
python3 scripts/list_er.py --resource detail --er-id <valid-er-id>
python3 scripts/list_er.py --resource attachment --er-id <valid-er-id> --table
python3 scripts/list_er.py --resource route-table --er-id <valid-er-id> --table
python3 scripts/list_er.py --resource detail --er-id does-not-exist   # exit 1, explicit hint
python3 scripts/list_er.py --operation DeleteEnterpriseRouter         # exit 1, guard
```

Expected: the list paths return an ER list or an explicit empty-list hint with
exit 0; a 403 returns an explicit IAM hint with exit 1; an invalid `--er-id`
returns an explicit not-found hint with exit 1 (never a traceback); a write
intent is rejected with exit 1 before any command runs.

## API / parameter provenance (no guessing)

Verified against the installed official SDK `huaweicloudsdker` v3 and
`hcloud ER <Operation> --help`:

| Operation | SDK `resource_path` | KooCLI parameters |
| --------- | ------------------- | ----------------- |
| `ListEnterpriseRouters` | `/v3/{project_id}/enterprise-router/instances` | `limit`, `marker`, `state.[N]`, `id.[N]`, `owned_by_self`, `enterprise_project_id.[N]`, `sort_key.[N]`, `sort_dir.[N]` |
| `ShowEnterpriseRouter` | `/v3/{project_id}/enterprise-router/instances/{er_id}` | `er_id` |
| `ListVpcAttachments` | `/v3/{project_id}/enterprise-router/{er_id}/vpc-attachments` | `er_id`, `limit`, `marker`, `state.[N]`, `vpc_id.[N]`, `id.[N]`, `sort_key.[N]`, `sort_dir.[N]` |
| `ListRouteTables` | `/v3/{project_id}/enterprise-router/{er_id}/route-tables` | `er_id`, `limit`, `marker`, `state.[N]`, `is_default_association_table`, `is_default_propagation_table`, `sort_key.[N]`, `sort_dir.[N]` |

- Array query parameters are declared as `array<string>` in KooCLI, so they are
  emitted as `--key.1=value`.
- Paging uses `limit` + `marker`; the next marker is the response
  `page_info.next_marker`.
- Response collections: `instances` (`ListEnterpriseRouters`), `instance`
  (`ShowEnterpriseRouter`), `vpc_attachments` (`ListVpcAttachments`),
  `route_tables` (`ListRouteTables`).
- Region catalog `huaweicloudsdker.v3.region.er_region.ErRegion` maps
  `cn-north-4 → https://er.cn-north-4.myhuaweicloud.com`.
- IAM action names were copied from
  `hcloud IAM GetAuthorizationSchemaV5 --service_code=er`.

## Environment note

The development environment had KooCLI and a credential profile, but the
profile's IAM identity was **not granted** ER read permissions: a live
`hcloud ER ListEnterpriseRouters` call returned
`common.01010013 ... not authorized to perform: er:instances:list`. The skill
therefore reports the explicit IAM 403 hint and exits 1; the list/table/JSON
success paths are covered by the offline unit tests and should be re-verified
by QA with an ER-authorized identity.
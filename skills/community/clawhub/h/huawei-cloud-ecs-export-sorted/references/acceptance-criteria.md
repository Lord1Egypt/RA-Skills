# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | SKILL.md passes specification validation (`scripts/validate-skill.sh`) | ✅ |
| 3 | Triggered by 「ECS 列表导出并排序」/「ecs sorted export」 (description triggers) | ✅ description triggers |
| 4 | Query the region's ECS instance list via CLI (`hcloud ECS ListServersDetails`) with `--region` (default cn-north-4) | ✅ `list_servers` + `build_command` + `--region` |
| 5 | `--format xlsx` (default) / `csv` / `json` / `table` output modes | ✅ `--format` / `--output` / `--summary` |
| 6 | Well-formed .xlsx: fixed header (名称/ID/状态/规格/vCPU/内存/可用区/私网IP/公网IP/创建时间) + data rows + optional summary row | ✅ `export_xlsx` |
| 7 | UTF-8-BOM .csv with the same columns; valid JSON array for `--format json` | ✅ `export_csv` / json path |
| 8 | **Sort by at least one field, ascending and descending** | ✅ `--sort-by` / `--order` (`sort_servers`) |
| 9 | Type-aware comparison (numeric / timestamp / text); invalid values placed last | ✅ `_sort_key_value` |
| 10 | `--sort-by` omitted → original query order preserved | ✅ `sort_servers` returns input order |
| 11 | Unknown `--sort-by` field → explicit error, no query issued | ✅ `SortError` fail-fast |
| 12 | `--output` path supported; default `ecs_instances_<region>_<timestamp>.<ext>` | ✅ `--output` / `default_output_path` |
| 13 | Empty instance list: friendly hint, no corrupt/partial file produced | ✅ exit 0, no file |
| 14 | Missing AK/SK / no-permission: explicit hint, no file produced | ✅ `ConfigError`/`AuthError` -> exit 1 |
| 15 | Write-intent guard blocks create/delete/update/reboot/resize/start/stop/attach/detach | ✅ `guard_write_intent` / `guard_operation` |
| 16 | Local-file-only: nothing ever written back to the cloud | ✅ read-only ListServersDetails only |
| 17 | hcloud not installed → SDK fallback (`huaweicloudsdkecs` v2) | ✅ `list_servers_via_sdk` |
| 18 | openpyxl missing → `ensure_env.py` auto-install with clear hint | ✅ `ensure_env` / `ExportError` |
| 19 | Offset paging until the reported `count` is reached | ✅ `list_servers` / `_has_more` |
| 20 | `--status` / `--name` server-side filters forwarded to both execution paths | ✅ `build_command` / `list_servers_via_sdk` |
| 21 | Offline unit tests with mocked hcloud, all passing (guard / sorting / formats / errors / sdk / main) | ✅ unit tests |
| 22 | No hardcoded AK/SK; credentials resolved from profile/env only, via directed env reads | ✅ `_env_credential` |

## Acceptance verification

```bash
cd skills/compute/ecs/huawei-cloud-ecs-export-sorted
python3 -m unittest discover -s tests -v
bash scripts/validate-skill.sh .
bash scripts/test-cli-commands.sh .   # optional: requires live KooCLI credentials
```

Full validation command from the repository root:

```bash
python3 -m unittest discover -s skills/compute/ecs/huawei-cloud-ecs-export-sorted/tests -v
```
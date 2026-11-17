# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | SKILL.md passes specification validation (`scripts/validate-skill.sh`) | ✅ |
| 3 | Triggered by 「查询 ECS 生成 Excel」/「ECS 实例列表导出 Excel」/「ecs excel」 | ✅ description triggers |
| 4 | Query the region's ECS instance list via CLI (`hcloud ECS ListServersDetails`) with `--region` (default cn-north-4) | ✅ `list_servers` + `build_command` + `--region` |
| 5 | `--format xlsx` (default) / `table` / `json` output modes | ✅ `--format` / `--output` / `--summary` |
| 6 | Well-formed .xlsx: fixed header (名称/ID/状态/规格/vCPU/内存/可用区/私网IP/公网IP) + data rows + optional summary row | ✅ `export_xlsx` |
| 7 | `--output` path supported; default `ecs_instances_<region>_<timestamp>.xlsx` | ✅ `--output` / `default_output_path` |
| 8 | Empty instance list: friendly hint, no corrupt/partial .xlsx produced | ✅ exit 0, no file |
| 9 | Missing AK/SK / no-permission: explicit hint, no .xlsx produced | ✅ `ConfigError`/`AuthError` -> exit 1 |
| 10 | Write-intent guard blocks create/delete/update/reboot/resize/start/stop/attach/detach | ✅ `guard_write_intent` / `guard_operation` |
| 11 | Local-file-only: nothing ever written back to the cloud | ✅ read-only ListServersDetails only |
| 12 | hcloud not installed → SDK fallback (`huaweicloudsdkecs` v2) | ✅ `list_servers_via_sdk` |
| 13 | openpyxl missing → `ensure_env.py` auto-install with clear hint | ✅ `ensure_env` / `ExportError` |
| 14 | Offset paging until the reported `count` is reached | ✅ `list_servers` / `_has_more` |
| 15 | `--status` / `--name` server-side filters forwarded to both execution paths | ✅ `build_command` / `list_servers_via_sdk` |
| 16 | Offline unit tests with mocked hcloud, all passing (guard / paging / errors / sdk / xlsx / main) | ✅ unit tests |
| 17 | No hardcoded AK/SK; credentials resolved from profile/env only, via directed env reads | ✅ `_env_credential` |
| 18 | `ECS_EXPORT_EXCEL_HCLOUD_ARGS` extra args appended after the read-only argv and guard-scanned (cannot rewrite service/operation) | ✅ `run_hcloud` |

## Acceptance verification

```bash
cd skills/compute/ecs/huawei-cloud-ecs-export-excel
python3 -m unittest discover -s tests -v
bash scripts/validate-skill.sh .
bash scripts/test-cli-commands.sh .   # optional: requires live KooCLI credentials
```

Full validation command from the repository root:

```bash
python3 -m unittest discover -s skills/compute/ecs/huawei-cloud-ecs-list/tests -v
python3 -m unittest discover -s skills/compute/ecs/huawei-cloud-ecs-export-excel/tests -v
```
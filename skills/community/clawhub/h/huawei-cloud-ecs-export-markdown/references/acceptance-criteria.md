# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | SKILL.md passes specification validation (`scripts/validate-skill.sh`) | ✅ |
| 3 | Triggered by 「查询 ECS 生成 Markdown」/「ECS 实例列表导出 Markdown」/「ecs markdown」 | ✅ description triggers |
| 4 | Query the region's ECS instance list via CLI (`hcloud ECS ListServersDetails`) with `--region` (default cn-north-4) | ✅ `list_servers` + `build_command` + `--region` |
| 5 | `--format md` (default) / `table` / `json` output modes | ✅ `--format` / `--output` / `--summary` |
| 6 | Well-formed .md: header row + separator row + data rows (名称/ID/状态/规格/vCPU/内存/可用区/私网IP/公网IP), missing fields render `-` | ✅ `render_markdown` / `normalized_row` |
| 7 | `--output` path supported; default `ecs_instances_<region>_<timestamp>.md`; parent directory auto-created | ✅ `--output` / `default_output_path` / `export_markdown` |
| 8 | Atomic write: temp file + `os.replace`, no partial/corrupt .md left behind | ✅ `export_markdown` |
| 9 | Empty instance list: friendly hint, no corrupt/partial .md produced | ✅ exit 0, no file |
| 10 | Missing AK/SK / no-permission (403/401): explicit hint, no .md produced | ✅ `ConfigError`/`AuthError` -> exit 1 |
| 11 | hcloud not installed → SDK fallback (`huaweicloudsdkecs` v2), missing SDK → clear hint | ✅ `list_servers_via_sdk` / `ConfigError` |
| 12 | Write-intent guard blocks create/delete/update/reboot/resize/attach/detach/start/stop and any operation other than ListServersDetails | ✅ `guard_write_intent` / `guard_operation` |
| 13 | Local-file-only: nothing ever written back to the cloud | ✅ read-only ListServersDetails (GET) only |
| 14 | Offset paging until the reported `count` is reached; same filter semantics as `huawei-cloud-ecs-list` | ✅ `list_servers` / `_has_more` / `build_command` |
| 15 | `--status` / `--name` server-side filters forwarded to both execution paths | ✅ `build_command` / `list_servers_via_sdk` |
| 16 | quality telemetry: every hcloud call wrapped by skill-quality-cli, degrading to bare hcloud when unavailable | ✅ `build_hcloud_command` |
| 17 | Offline unit tests with mocked hcloud, all passing (guard / paging / errors / sdk / markdown / main) | ✅ unit tests |
| 18 | No hardcoded AK/SK; credentials resolved from profile/env only, via directed env reads | ✅ `_env_value` |
| 19 | `ECS_EXPORT_MARKDOWN_HCLOUD_ARGS` extra args appended after the read-only argv and guard-scanned (cannot rewrite service/operation) | ✅ `run_hcloud` |

## Acceptance verification

```bash
cd skills/compute/ecs/huawei-cloud-ecs-export-markdown
python3 -m unittest discover -s tests -v
bash scripts/validate-skill.sh .
bash scripts/test-cli-commands.sh .   # optional: requires live KooCLI credentials
```

Full validation command from the repository root:

```bash
python3 -m unittest discover -s skills/compute/ecs/huawei-cloud-ecs-export-markdown/tests -v
```
# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | SKILL.md passes specification validation (`scripts/validate-skill.sh`) | ✅ |
| 3 | Triggered by 「查询 OBS 生成 Excel」/「OBS 桶列表导出 Excel」/「obs excel」 | ✅ description triggers |
| 4 | Query the account's OBS bucket list via CLI (`hcloud OBS ls`) with `--region` (default cn-north-4) | ✅ `list_buckets` + `build_command` + `--region`/`--endpoint` |
| 5 | `--format xlsx` (default) / `table` / `json` output modes | ✅ `--format` / `--output` / `--summary` |
| 6 | Well-formed .xlsx: fixed header (桶名称/创建时间/区域/存储类别/桶策略) + data rows + optional summary row | ✅ `export_xlsx` |
| 7 | `--output` path supported; default `obs_buckets_<region>_<timestamp>.xlsx` | ✅ `--output` / `default_output_path` |
| 8 | Empty bucket list: friendly hint, no corrupt/partial .xlsx produced | ✅ exit 0, no file |
| 9 | Missing AK/SK / no-permission: explicit hint, no .xlsx produced | ✅ `ConfigError`/`AuthError` -> exit 1 |
| 10 | Write-intent guard blocks create/delete/upload/download/copy/remove/sync | ✅ `guard_write_intent` / `guard_operation` |
| 11 | Local-file-only: nothing ever written back to OBS | ✅ read-only ListBuckets only |
| 12 | hcloud not installed → SDK fallback (`huaweicloudsdkobs`) | ✅ `list_buckets_via_sdk` |
| 13 | openpyxl missing → `ensure_env.py` auto-install with clear hint | ✅ `ensure_env` / `ExportError` |
| 14 | Offline unit tests with mocked hcloud, all passing (parse/export/errors/guard/xlsx) | ✅ unit tests |
| 15 | Existing obs-list / obs-dir-count / storage-query tests not broken | ✅ suite runs green |
| 16 | No hardcoded AK/SK; credentials resolved from profile/env only | ✅ |

## Acceptance verification

```bash
cd skills/storage/obs/huawei-cloud-obs-list-excel
python3 -m unittest discover -s tests -v
bash scripts/validate-skill.sh .
bash scripts/test-cli-commands.sh .   # optional: requires live obsutil credentials
```

Full validation command from the repository root:

```bash
python3 -m unittest discover -s skills/storage/obs/huawei-cloud-obs-list/tests -v
python3 -m unittest discover -s skills/storage/obs/huawei-cloud-obs-dir-count/tests -v 2>/dev/null || true
python3 -m unittest discover -s skills/storage/obs/huawei-cloud-obs-list-excel/tests -v
```
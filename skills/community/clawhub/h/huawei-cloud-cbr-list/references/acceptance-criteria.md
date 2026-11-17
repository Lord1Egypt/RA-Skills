# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | Query the region's CBR backup list via CLI (`hcloud CBR ListBackups`) | ✅ `list_backups` + `build_command` |
| 4 | `--region` parameter supported (default cn-north-4) | ✅ `--region` / `-r` |
| 5 | table (default), `--json` and `--names-only` output modes | ✅ |
| 6 | Empty list friendly hint 「当前区域（x）无 CBR 备份」 (exit 0) | ✅ |
| 7 | name / id / status / resource_name / resource_id / resource_type / vault_id / created_at parsing into table columns | ✅ `normalize_backup` + `render_table` |
| 8 | `--name` / `--status` / `--resource_id` / `--resource_name` / `--resource_type` / `--vault_id` / `--image_type` filtering | ✅ `filter_backups` + native request params |
| 9 | Automatic pagination via `limit` / `offset` (+ `count`) | ✅ `list_backups` |
| 10 | Write-intent guard blocks create/delete/restore/copy/update/... (GuardError) | ✅ `guard_write_intent` / `guard_operation` |
| 11 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 12 | hcloud not installed → SDK fallback (`huaweicloudsdkcbr`) | ✅ `list_backups_via_sdk` |
| 13 | 401/403 invalid/insufficient credentials explicit IAM hint (exit 1) | ✅ `AuthError` |
| 14 | Generic API/network error classified with stderr excerpt | ✅ `ApiError` |
| 15 | No hardcoded AK/SK; credentials resolved from profile/env only | ✅ |
| 16 | Offline unit tests with mocked hcloud, all passing | ✅ 69 tests |
| 17 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extensions allowlisted | ✅ |

## Acceptance verification

```text
cd skills/storage/cbr/huawei-cloud-cbr-list
python3 -m unittest discover -s tests -v
bash <creator>/scripts/validate-skill.sh -s .
```
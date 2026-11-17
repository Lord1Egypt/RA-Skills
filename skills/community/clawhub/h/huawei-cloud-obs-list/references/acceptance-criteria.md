# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | Query the account's OBS bucket list via CLI (`hcloud OBS ls`) | ✅ `list_buckets` + `build_command` |
| 4 | `--region` parameter supported (selects OBS endpoint) | ✅ `--region` / `--endpoint` |
| 5 | `table` (default) and `json` output modes (plus `names`) | ✅ `--output` / `--json` / `--names-only` |
| 6 | Empty list friendly hint 「当前账号（Region x）无 OBS 桶」 (exit 0) | ✅ |
| 7 | Write-intent guard blocks create/delete/upload/... (GuardError) | ✅ `guard_write_intent` / `guard_operation` |
| 8 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 9 | hcloud not installed → SDK fallback (`huaweicloudsdkobs`) | ✅ `list_buckets_via_sdk` |
| 10 | 401/403 invalid/insufficient credentials explicit IAM hint (exit 1) | ✅ `AuthError` |
| 11 | Generic API/network error classified with stderr excerpt | ✅ `ApiError` |
| 12 | No hardcoded AK/SK; credentials resolved from profile/env only | ✅ |
| 13 | Offline unit tests with mocked hcloud, all passing | ✅ 50 tests |
| 14 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extensions allowlisted | ✅ |

## Acceptance verification

```bash
cd skills/storage/obs/huawei-cloud-obs-list
python3 -m unittest discover -s tests -v
bash <creator>/scripts/validate-skill.sh -s .
```
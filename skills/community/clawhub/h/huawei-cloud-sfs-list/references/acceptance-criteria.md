# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | Query the region's SFS file-system list via CLI (`hcloud SFSTurbo ListShares`) | ✅ `list_shares` + `build_command` |
| 4 | `--region` parameter supported (default cn-north-4) | ✅ `--region` / `-r` |
| 5 | table (default), `--json`, `--names-only` and `--count-only` output modes | ✅ |
| 6 | Empty list friendly hint 「当前区域（x）无 SFS 文件系统」 (exit 0) | ✅ |
| 7 | name / id / status / share_proto parsing into table columns | ✅ `normalize_share` + `render_table` |
| 8 | `--name` / `--id` (and `--status` / `--share-proto` / `--az`) filtering | ✅ `filter_shares` (client-side) |
| 9 | Automatic pagination via `limit` / `offset` (+ `count`) | ✅ `list_shares` |
| 10 | Write-intent guard blocks create/delete/expand/mount/... (GuardError) | ✅ `guard_write_intent` / `guard_operation` |
| 11 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 12 | hcloud not installed → SDK fallback (`huaweicloudsdksfsturbo`) | ✅ `list_shares_via_sdk` |
| 13 | 401/403 invalid/insufficient credentials explicit IAM hint (exit 1) | ✅ `AuthError` |
| 14 | Generic API/network error classified with stderr excerpt | ✅ `ApiError` |
| 15 | No hardcoded AK/SK; credentials resolved from profile/env only | ✅ |
| 16 | Offline unit tests with mocked hcloud, all passing | ✅ 66 tests |
| 17 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extensions allowlisted | ✅ |

## Acceptance verification

```bash
cd skills/storage/sfs/huawei-cloud-sfs-list
python3 -m unittest discover -s tests -v
bash <creator>/scripts/validate-skill.sh -s .
```
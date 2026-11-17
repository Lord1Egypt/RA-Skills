# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | ListClusters full-field table output (union of returned fields) | ✅ `render_table` |
| 4 | `--json` raw output mode | ✅ |
| 5 | `--names-only` output mode | ✅ |
| 6 | `--cluster-state` filter (forwarded as `--clusterState`) | ✅ |
| 7 | Empty-cluster explicit hint (exit 0) | ✅ |
| 8 | 403 / no-permission explicit hint (exit 1) | ✅ `AuthError` |
| 9 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 10 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 11 | Offline unit tests with mocked hcloud, all passing | ✅ 43/43 |
| 12 | Read-only REST path provenance documented | ✅ verification-method.md |
| 13 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |

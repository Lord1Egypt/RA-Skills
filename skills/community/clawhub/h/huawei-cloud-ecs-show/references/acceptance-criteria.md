# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | Valid instance ID returns full detail (ID / 名称 / 状态 / 规格 / 镜像 / 私网+公网 IP / 可用区 / 创建时间 / 标签) | ✅ `render_detail` + `normalize_server` |
| 4 | `--json` raw server-object output mode | ✅ |
| 5 | `--instance-id` required parameter; `--region` (default cn-north-4) and `--project-id` (optional) supported | ✅ `argparse` |
| 6 | Missing / malformed instance ID explicit hint 「实例 ID 不能为空」(exit 1) | ✅ `validate_instance_id` / `ConfigError` |
| 7 | Non-existent instance ID explicit hint 「未找到该 ECS 实例」(404, exit 1) | ✅ `NotFoundError` |
| 8 | 403 explicit hint 「无权限访问 ECS，请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 9 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 10 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 11 | SDK fallback (`huaweicloudsdkecs` `show_server`) when hcloud is missing | ✅ `show_server_via_sdk` |
| 12 | Offline unit tests with mocked hcloud, all passing (SDK-optional cases skipped when `huaweicloudsdkecs` is absent) | ✅ 85 tests |
| 13 | Read-only REST path provenance documented | ✅ verification-method.md |
| 14 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
| 15 | Without `--md-file`, stdout-only: the script writes no file in the default / `--json` modes | ✅ no write path except the export branch |
| 16 | Data-flag values (`--region` / `--instance-id` / `--project-id` / `--md-file`) are not scanned by the write-intent guard, while a following flag is still scanned | ✅ `_VALUE_STRIPPED_FLAGS` + guard regression tests |
| 17 | `--md-file <path>` exports the instance detail as a Markdown document (ID / 名称 / 状态 / 规格 / 镜像 / 私网+公网 IP / 可用区 / 创建时间 / 标签), reusing `normalize_server()` + `_KEY_FIELDS` | ✅ `render_markdown` |
| 18 | Output-mode precedence is explicit: `--md-file` → `--json` → detail block | ✅ `main()` + docs |
| 19 | Invalid / unwritable `--md-file` path yields an explicit error (exit 1), no silent failure | ✅ `write_markdown` / `ConfigError` |
| 20 | Markdown export remains read-only (only `ShowServer`); the export path value is not treated as a write intent | ✅ `guard_write_intent` + `_VALUE_STRIPPED_FLAGS` |
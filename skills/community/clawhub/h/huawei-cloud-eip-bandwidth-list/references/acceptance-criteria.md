# Acceptance Criteria

| # | Criterion | Status |
| - | --------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | `SKILL.md` passes specification validation (`validate-skill.sh`, FAIL=0) | ✅ |
| 3 | Frontmatter/triggers complete (spec v1.0 forbids a frontmatter `version` field); script exposes `SCRIPT_VERSION = "1.0.0"` | ✅ |
| 4 | `hcloud EIP ListBandwidths` operation name and all parameters verified live (KooCLI 7.3.12) | ✅ `references/verification-method.md` |
| 5 | `hcloud EIP ShowBandwidth` operation name and parameters verified live | ✅ `references/verification-method.md` |
| 6 | List table carries 名称 / ID / 大小 / share_type / charge_mode / 公网 IP 数 / 状态 / 企业项目 / 创建时间 | ✅ `render_table` + `MD_COLUMNS` |
| 7 | `--bandwidth-id` switches to ShowBandwidth detail: public IP address/type/ip_version + bandwidth_rules / rule_quota | ✅ `show_bandwidth` + `render_detail` |
| 8 | `--share-type {PER,WHOLE}` filter is a real server-side parameter | ✅ verified live; `build_list_command` |
| 9 | `--enterprise-project-id` filter is a real server-side parameter | ✅ `build_list_command` |
| 10 | `marker` automatic paging aggregates all pages | ✅ verified live (16 = 10 + 6); `list_bandwidths` |
| 11 | Empty result explicitly reported, distinguishing overall-empty vs share_type-filtered-empty (exit 0) | ✅ `empty_message` |
| 12 | 403 hint names the required IAM actions `eip:bandwidths:list` / `eip:bandwidths:get` | ✅ `AuthError` |
| 13 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 14 | hcloud not installed: SDK fallback; when both unavailable, explicit ConfigError | ✅ `list_bandwidths_via_sdk` / `show_bandwidth_via_sdk` |
| 15 | Default table, `--json` raw output, `--format md -o <file>` | ✅ |
| 16 | Markdown empty list = fixed header + 「无数据」; `--json` / Markdown readable back | ✅ `render_markdown` / `export_markdown` |
| 17 | No write API call exists in code; write intents blocked before execution | ✅ `guard_write_intent` / `guard_operation` |
| 18 | Offline unit tests (mocked hcloud, no credentials/network) cover all new behavior | ✅ `tests/test_list_bandwidths.py` (78 tests) |
| 19 | API error bodies returned with exit code 0 (e.g. `VPC.0305`) are classified: not-found → explicit hint to run ListBandwidths and verify `--bandwidth-id` | ✅ `classify_api_error_payload` |
| 20 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
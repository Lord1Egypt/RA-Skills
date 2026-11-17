# Acceptance Criteria

| # | Criterion | Status |
| - | --------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | `--resource er` uses `hcloud ER ListEnterpriseRouters` with limit/marker/state/id/owned_by_self/sort/enterprise-project parameters | ✅ `build_er_command` |
| 4 | `--resource attachment` uses `hcloud ER ListVpcAttachments --er_id` with limit/marker/state/vpc_id | ✅ `build_attachment_command` |
| 5 | `--resource route-table` uses `hcloud ER ListRouteTables --er_id` with limit/marker/default association/default propagation | ✅ `build_route_table_command` |
| 6 | `--resource detail` uses `hcloud ER ShowEnterpriseRouter --er_id` | ✅ `build_detail_command` |
| 7 | Default output is a compact list; `--table` renders ER 8 columns / attachment 6 columns; `--json` returns the raw response | ✅ `render_*` / `main` |
| 8 | Non-`available` ERs / attachments are flagged in a separate `[!]` / `[异常]` section, never mixed with healthy rows | ✅ `split_by_state` / `render_sections` |
| 9 | Filters `--name` (exact) / `--fuzzy` (case-insensitive) / `--er-id` / `--state` / `--region` (default `cn-north-4`) | ✅ `apply_local_filters` + server-side params |
| 10 | `--page-size` / `--limit` restricted to 1–2000 and auto-paged via `page_info.next_marker` | ✅ `_validate_page_size` / `_paged_fetch` |
| 11 | Write intents (Create/Delete/Update/Associate/Disassociate/Enable/Disable/…) rejected before execution, exit 1 | ✅ `guard_write_intent` / `guard_operation` |
| 12 | `hcloud` missing → falls back to `huaweicloudsdker` v3 `ErClient` | ✅ `*_via_sdk` |
| 13 | Empty results give explicit hints (exit 0) | ✅ `main` |
| 14 | 403 / missing credentials / network / not-found errors give explicit hints (exit 1, no traceback) | ✅ `classify_*` / `NotFoundError` |
| 15 | Offline unit tests (mocked hcloud + fake SDK) all pass | ✅ 84 tests |
| 16 | `bash -n` / `py_compile` / `json.tool` checks pass | ✅ |
| 17 | references/ covers IAM policy, CLI installation, verification method, data flow, acceptance checklist | ✅ |
| 18 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
| 19 | `network/er` path follows the repository category layout | ✅ |
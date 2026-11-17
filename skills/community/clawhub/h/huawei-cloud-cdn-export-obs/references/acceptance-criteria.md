# Acceptance Criteria

| # | Criterion | Status |
| - | --------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | SKILL.md passes specification validation | ✅ |
| 3 | Query the CDN accelerated-domain list (region + paging + filters) | ✅ `list_cdn.list_domains` (CLI + SDK fallback) |
| 4 | Serialize the result into JSON / CSV / Markdown | ✅ `export_results.serialize` |
| 5 | Upload the result file to a specified OBS bucket/key | ✅ `upload_obs.upload_file` (`hcloud OBS cp` + SDK fallback) |
| 6 | Read-back verification that the object exists (head/stat) | ✅ `upload_obs.verify_object` (size compared) |
| 7 | Default refuses to overwrite an existing object (unless `--overwrite`) | ✅ `OverwriteError` |
| 8 | Structure consistent with the sibling CDN-list / OBS skills | ✅ same layout + conventions |
| 9 | Offline unit tests cover query/serialization/upload/error/overwrite protection (mocked hcloud) | ✅ 56 tests |
| 10 | Empty domain list is not treated as an error (exit 0) | ✅ |
| 11 | Explicit error classification (AK/SK, 403, hcloud missing, usage, bad path) | ✅ |
| 12 | Write-intent guard blocks mutating CDN operations; OBS operation whitelist | ✅ |
| 13 | CLI first (hcloud CDN ListDomains / hcloud OBS), SDK fallback | ✅ |
| 14 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, allowed extensions | ✅ |
| 15 | `network/cdn` category path consistent with the existing CDN skill | ✅ |
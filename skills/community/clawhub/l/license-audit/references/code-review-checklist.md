# audit.py Code Review Checklist

Items to verify when reviewing or extending the script.

## Security
- [ ] No tokens, app-id, or app-secret hardcoded anywhere in the skill files
- [ ] `--as user` used in all lark-cli calls (never bot identity)
- [ ] HTML output: package names and license strings HTML-escaped (`&amp;`, `&lt;`)

## Dead code
- [ ] All imported modules are actually used (check: `collections.defaultdict` was removed)
- [ ] All defined functions are called somewhere (`ensure_trivy` was dead until fixed)
- [ ] No stale placeholder strings left in conditional branches

## Error handling
- [ ] `publish_feishu_doc` failure path returns `""` not the raw markdown content
- [ ] `publish_feishu_base` failure paths all return a short error string, not raw API output
- [ ] Trivy parse fallback (line-by-line JSON scan) still present for noisy trivy output

## Output completeness
- [ ] No per-tier row caps in any output format (the `[:50]` cap was a bug, not a feature)
- [ ] All four tiers (HIGH / MEDIUM / UNKNOWN / LOW) rendered even if count is zero? No — empty tiers are skipped intentionally for brevity

## Python compatibility
- [ ] `list[dict]` type hints require Python ≥ 3.9 — SKILL.md documents this requirement
- [ ] No `str | None` union syntax (requires 3.10+) — use `Optional[str]` from typing

## Feishu-specific
- [ ] `+table-create` response path: `data.table.id` (NOT `table_id`)
- [ ] `+base-create` response path: `data.base.base_token`, `data.base.url`
- [ ] Batch record insert: 0.6 s sleep between batches to avoid conflict 1254291
- [ ] Default empty table deleted after `+table-create` (lark-cli auto-creates one)
- [ ] Relative path used for `@file` in `docs +create` (lark-cli rejects absolute paths)

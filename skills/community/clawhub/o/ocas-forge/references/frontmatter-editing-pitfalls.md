# Skill Frontmatter Editing — Pitfalls & Patterns

## YAML Block Scalar Truncation (CRITICAL)

**Problem:** Skills with `description: >` or `description: |` frontmatter fields contain embedded newlines. Using `execute_code` with `content.split('---')` to extract or replace frontmatter **WILL truncate the file** at the first `---` inside the block scalar, destroying body content.

**Incident:** ocas-custodian lost 57 lines of body content (Gotchas, support file map, background tasks table) in May 2026 when `split('---')` split at the `---` inside the block scalar instead of the frontmatter delimiter.

**Correct approach:**
1. Use `read_file` to get exact line numbers of the frontmatter (first `---` line to second `---` line)
2. Use `patch` with precise `old_string` from the `read_file` output — never reconstruct frontmatter programmatically
3. After any frontmatter edit, verify:
   - `wc -l` matches expected line count (compare to pre-edit count)
   - `yaml.safe_load` parses the frontmatter without errors
   - The body starts with the expected `## ` heading
   - All support file map entries still exist in the body

**Alternative safe pattern:** Convert `description: >` to a single-line `description: "..."` before editing, then convert back if needed. Single-line scalars are safe for `split('---')`.

## Frontmatter Field Order

Correct order per OCAS spec: `name` → `description` → `license` → `includes` → `metadata`. The `license:` field must come before `metadata:`. Violating this order is a D1 issue.

## Phantom References

Every file listed in the support file map must exist. Before adding a file path to the map, verify it with `read_file` or `search_files`. Phantom references cause runtime errors when the agent follows the map.

## Duplicate Support File Maps

Grep for `## Support file map` — there should be exactly one instance. Duplicate maps can contradict each other (one listing real files, another saying "no external support files"). Remove duplicates.

## Heuristic Scorer Calibration

The `10khr_runner.py` heuristic scorer uses simple keyword matching and over-scores skills by ~7-10 points compared to manual rubric assessment. Use it for **ranking candidates** (which skill to grind next), NOT for absolute scoring. Always do a Phases 1-6 manual assessment before applying fixes.
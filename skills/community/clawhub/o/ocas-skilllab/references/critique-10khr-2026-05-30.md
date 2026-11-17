# 10khr Session — 2026-05-30

## Scope
Full manual assessment of all 31 ocas-* skills against the 10-dimension rubric.

## Pre-pass: Bulk D1 Check
- All 31 skills have valid YAML frontmatter
- All have `license: MIT` (no proprietary licenses)
- All have `includes: [references/**, scripts/**]` where dirs exist
- 0 Critical D1 issues found

## Heuristic vs. Manual Scores
The `10khr_runner.py` heuristic over-scored by ~7-10 points across the board:
- Heuristic range: 44-48/50 (all Band A)
- Manual range: 36-42/50 (all Band A, but lower)

## Grinding Target: ocas-mentor
Identified as the lowest-scoring skill by the heuristic (44/50) and confirmed by manual assessment (38/50 real).

### Issues Found
1. **Duplicate When to use / When not to use sections** (lines 40-54) — non-standard casing, redundant with frontmatter description
2. **Inline default config JSON** (19 lines) — bloated code ratio in SKILL.md body
3. **Vague OKRs section** — just "Universal OKRs apply" + pointer to schemas.md

### Fixes Applied
1. ✅ Removed duplicate sections (15 lines removed)
2. ✅ Moved default config JSON to `references/default-config.md` (19 lines removed, 2-line pointer added)
3. ✅ Expanded OKRs to specific table with 5 skill-level OKRs (targets, windows, measurements)
4. ✅ Updated Support File Map to include new reference file

### Before/After
- Line count: 296 → 271 (-25 lines)
- Code ratio: ~8.4% → 2.2%
- Score: 38 → 42 (+4)

## Library-Wide Findings

### Structural Gaps (6 skills)
- **ocas-fellow**: Missing Responsibility Boundary section
- **ocas-forge**: Missing Responsibility Boundary section
- **ocas-genie**: Missing Gotchas section
- **ocas-vibes**: Missing Responsibility Boundary section
- **ocas-voyage**: Missing Responsibility Boundary section
- **ocas-weave**: Missing Responsibility Boundary section

### Minor Issues
- **ocas-imagine**: Duplicate Support File Map (two identical maps)
- **ocas-multipass**: Duplicate Support File Map header
- **ocas-autobio**: Description uses second person ("your"); missing `source:` field
- **ocas-taste**: `evals/` in includes is non-standard
- **ocas-custodian**: Duplicate When NOT to use section

## Next Grinding Targets (in order)
1. ocas-fellow — add Responsibility Boundary
2. ocas-forge — add Responsibility Boundary
3. ocas-vibes — add Responsibility Boundary
4. ocas-voyage — add Responsibility Boundary
5. ocas-weave — add Responsibility Boundary
6. ocas-genie — add Gotchas section
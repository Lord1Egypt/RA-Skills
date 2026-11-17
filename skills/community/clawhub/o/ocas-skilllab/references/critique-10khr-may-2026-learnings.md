# 10khr Grind — May 2026 Session Learnings

## Scoring Inflation Patterns

1. **Structural heuristic scoring**: Checking for headings and counting references, then mapping to rubric scores. Over-estimates by 5-10 points.
2. **Template content scoring**: Generic When to Use / When NOT to Use bullets score 2-3 on D2/D5, not 4-5.
3. **Clustering detection**: If most skills score 44-47/50, scoring is inflated.

## Fix Patterns That Consistently Work

1. **Inline content to references/**: Moving storage layouts, OKR YAML, init sequences, self-update procedures improves D3/D4/D8 by 1-2 points each.
2. **Code ratio**: Under 20% target.
3. **Description NOT clause**: "NOT for" scores 5, "Do not use for" or "Not for:" scores 3-4.
4. **Duplicate section removal**: Many skills have both `## When to Use` and `## When to use` (non-standard casing). Consolidating gives +1-2 on D4.
5. **Error handling tables**: Adding a failure/response table is the fastest D7 fix — 3→4 in one patch.
6. **Self-update procedure extraction**: Moving the 7-step self-update from SKILL.md to references/ consistently saves 10-19 lines per skill.
7. **YAML single-quoted string fix**: Several skills had `'description'` spanning multiple lines (invalid YAML). Converting to `>` block scalar fixes parsing.

## Process Corrections

- Assess ALL before fixing ANY
- Quality over speed
- Show the work
- Don't declare victory prematurely

## Technical Gotchas

1. YAML block scalar truncation
2. Patch tool long-match failures
3. Code fence pairing verification
4. Subagent batch sizing (max 3)
5. Patch tool can eat heading structure — always verify `##` headings after patching
6. Moving `includes:` before `metadata:` can leave a duplicate inside metadata block — always check
7. Single-quoted YAML strings cannot span multiple lines — use `>` block scalar for multi-line descriptions

## Library Score Distribution (May 25, 2026, after Pass 6)

| Score Range | Count | Skills |
|-------------|-------|--------|
| 45-48 | 6 | bones, bower, critique, dispatch, lucid, reach |
| 40-44 | 26 | corvus, elephas, finch, forge, look, mentor, rally, sands, scout, vesper, weave, taste, genie, custodian, fellow, multipass, praxis, thread, vibes, voyage, inception |
| < 40 | 0 | (none) |

**All 32 ocas-* skills now score ≥ 40/50.**

### Sessions Summary
- Pass 1 (May 24): multipass, custodian, critique
- Pass 2 (May 24): reach, bower
- Pass 3 (May 24): dispatch
- Pass 4 (May 25): full assessment, thread, genie
- Pass 5 (May 25): vibes, voyage, inception
- Pass 6 (May 25): thread, vibes, voyage, inception (pushed all to 40+)
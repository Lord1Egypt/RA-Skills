# 10khr Grinding Session — June 26, 2026

**Target:** Lowest-scoring skills from 60-skill library
**Skills improved:** 5 (ocas-usercontext, ocas-rally, util-agent-swarm, util-manage, util-warmhands)
**Score range before:** 44-46/50 → **Score range after:** 47-48/50

## Scoring Session Summary

| Skill | Before | After | Key Fixes |
|-------|--------|-------|-----------|
| ocas-usercontext | 44 | 47 | triggers, description formula, support file map, "why" section, error handling, When NOT to Use |
| ocas-rally | 45 | 47 | metadata.hermes tags/category, deduplication (4→1 gotcha), error handling table, --help docs, "why" on boundaries |
| util-agent-swarm | 46 | 48 | "why" on Iron Rules, error handling table |
| util-manage | 46 | 48 | metadata.hermes tags/category, support file map, "why" on core principle, error handling |
| util-warmhands | 46 | 48 | metadata.hermes tags/category, support file map, error handling |

## Recurring Patterns Across Skills

### Pattern: Top-level `tags:` instead of `metadata.hermes.tags`
Found in 2/5 skills (`util-manage`, `util-warmhands`). The tags were declared at YAML top level but not under `metadata.hermes:`. Hermes uses `metadata.hermes.tags` for `skills_list` category grouping.

### Pattern: Missing Support File Map with "When to read"
Found in 3/5 skills. References were mentioned inline but never in a structured table with conditional "When to read" language. This is D4=3/D8=3 territory.

### Pattern: No Error Handling Table
Found in 4/5 skills. Gotchas existed but no systematic `## Error Handling` table with `| Failure | Response |` format. D7=2-3 until fixed.

### Pattern: Missing "Why" Explanations
Found in 3/5 skills. Rigid rules ("never do X", "always do Y") without D6's required "why" explanation.

### Pattern: Duplicate Gotchas (D3 bloat)
Found in `ocas-rally` (400+ lines). Same warning about `ALPACA_BASE_URL` appeared 4 times. Merged to 1 entry with full context → D3 moved from 2→4.

## Most Common Deduction Dimensions (in order)
1. **D7** — Missing Error Handling table (4/5 skills)
2. **D4/D8** — Missing Support File Map (3/5 skills)
3. **D6** — Missing "why" explanations (3/5 skills)
4. **D1** — Missing metadata.hermes fields (3/5 skills)
5. **D3** — Bloat/duplication (1/5 skills, but severe: ocas-rally at 2/5)

## Heuristic Runner Accuracy Note
The heuristic scorer consistently over-scores by 3-5 points compared to manual assessment.
Skills that report 47-48/50 after fixes may still have minor gaps. True 50/50 requires
manual verification against every rubric dimension.
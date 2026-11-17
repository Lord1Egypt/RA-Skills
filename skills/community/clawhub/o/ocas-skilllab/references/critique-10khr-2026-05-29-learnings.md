# 10khr Learnings — 2026-05-29

## Patterns Discovered

### Bulk Rewrite Strategy
When batch-rewriting multiple skills from scratch (e.g., auto-generated stubs):
1. **Frontmatter-only fixes first** — Use `patch` to add `license:` and `includes:` across all skills
2. **Full body rewrites second** — Use `write_file` for wholesale replacement; don't try to `patch` a stub into a real skill
3. **Verify YAML last** — Run yaml.safe_load on all modified files to catch parse errors the heuristic scorer misses

### YAML Single-Quoted String Trap
A frontmatter `description: '...'` that spans multiple lines with a stray unmatched `'` on a separate line breaks YAML parsing. Single-quoted strings can't contain unescaped newlines. The heuristic scorer silently skips these files. Always use `>` (folded) or `|` (literal) block scalars.

### Heuristic Scorer Blind Spots
- Over-scores by 7-10 points
- Cannot detect YAML parse errors
- Cannot detect duplicate sections
- Misses non-ocas skills entirely
- Use for candidate ranking only, never absolute scoring

### Auto-Generated Stub Pattern
All auto-generated stubs share: identical ~37-line body, generic workflow, no domain content, missing license/includes. Score ~21-22/50 (band C). Some have duplicate sections (browser-vision has 3x "Error Handling").

### Score Impact
D1 fix (license + includes) = +3 points. Full content rewrite = +11 points total. Combined: ~22 → ~33.
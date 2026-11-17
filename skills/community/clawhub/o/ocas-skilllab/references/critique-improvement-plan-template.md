# Improvement Plan Template

Use this template when generating improvement plans from a critique run.
The plan is the bridge between scoring (Phase 2) and fixing (Phase 5).

## File Header

```markdown
# Improvement Plan: <skill-name>

**Path:** <absolute-path-to-skill>
**Date:** <YYYY-MM-DD>
**Score Before:** <score>/50 (<band>)
**Target Score:** <target>/50
**Issues Found:** <N> Critical, <N> Major, <N> Minor
```

## Critical Issues

```markdown
## Critical Issues (<N>)

### Issue [C-01]: <dimension> — <brief description>

**Location:** <filename>:<line> (or "frontmatter")
**Dimension:** D<N> — <dimension name>
**Current:**
<original text, or "missing">

**Fix:**
<specific rewrite, addition, or deletion>

**Impact:** +<N> points on D<N>
```

Repeat for each critical issue (C-02, C-03, ...).

## Major Issues

```markdown
## Major Issues (<N>)

### Issue [M-01]: <dimension> — <brief description>

**Location:** <filename>:<line>
**Dimension:** D<N> — <dimension name>
**Current:**
<original text, or "missing">

**Fix:**
<specific rewrite, addition, or deletion>

**Impact:** +<N> points on D<N>
```

Repeat for each major issue (M-02, M-03, ...).

## Minor Issues

```markdown
## Minor Issues (<N>)

### Issue [m-01]: <dimension> — <brief description>

**Location:** <filename>:<line>
**Dimension:** D<N> — <dimension name>
**Current:**
<original text>

**Fix:**
<specific rewrite>

**Impact:** +<N> points on D<N> (optional)
**Evaluation:** <pass/fail on the 3 minor-issue questions>
```

Repeat for each minor issue (m-02, m-03, ...). Only include minor issues that
passed the evaluation protocol.

## Execution Order

List the exact order in which fixes should be applied:

1. C-01 (Critical — blocks everything)
2. C-02
3. M-01 (Major — high impact)
4. M-02
5. m-01 (Minor — only if evaluated as beneficial)

## Expected Outcome

```markdown
**Score After (estimated):** <score>/50 (<band>)
**Delta:** +<N> points
**All Critical resolved:** yes/no
**All Major resolved:** yes/no
```

## Execution Order

List the exact order in which fixes should be applied:

1. C-01 (Critical — blocks everything)
2. C-02
3. M-01 (Major — high impact)
4. M-02
5. m-01 (Minor — only if evaluated as beneficial)

**Highest-impact Major fix pattern (confirmed across 4+ skills):**
Inline structure blocks → references/. When a skill has 20+ lines of inline storage layouts, OKR YAML, CLI examples, or decision invariants:
1. Create `references/<topic>.md` (e.g., `storage-layout.md`, `okrs.md`, `decision-invariants.md`)
2. Move the inline content to the reference file
3. Replace inline content with a one-line pointer: "See `references/<topic>.md`."
4. Add the file to the support file map with a "When to read" conditional
5. Verify code ratio improved and D3/D4/D8 scores increase

This single pattern typically improves total score by 3-5 points.

## Notes

- Group changes by file to minimize file open/close cycles
- Use `patch` for targeted edits, not full-file rewrites
- After each file is modified, verify syntax (YAML parses, markdown well-formed)
- If a fix for one issue would conflict with a fix for another, flag it here
  and specify the resolution strategy:
  - High priority takes precedence over medium/low
  - If same priority, preserve the first change
  - Flag unresolved conflicts for manual review
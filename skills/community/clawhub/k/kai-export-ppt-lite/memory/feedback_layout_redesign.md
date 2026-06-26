# Layout Engine Redesign — Critical Feedback

## Process Summary

1. **Initial Document**: `/Users/song/projects/kai-export-ppt-lite/docs/LAYOUT_ENGINE_REDESIGN.md` — 5-stage pipeline, over 8 files, aggressive 9.5/10 target

2. **Adversarial Review**: Codex identified 10 issues:
   - **5 Major/Critical**: Root cause misdiagnosis, over-engineering, flawed scoring
   - **5 Minor**: Architecture details, implementation order

3. **CSS Coverage Audit**: 42 demo HTML files analyzed
   - 94 files use `display: grid`
   - 125 uses of `grid-template-columns` (including `repeat(N, 1fr)`, `1fr 1fr`, `1fr 2fr`, `200px 1fr`)
   - 413 uses of `display: flex`
   - 135 uses of `justify-content: center` (most common)
   - 142 uses of `align-items: center`
   - 47 uses of `box-sizing: border-box` (global)

## Key Corrections

### 1. Root Cause Analysis — Corrected

**Original (WRONG)**:
- Grid doesn't parse `repeat(2, 1fr)`
- internal_margin=1.5" mismatches CSS padding
- gap is "overly wide" (0.15" vs 0.33")

**Corrected**:
- ✅ `_parse_grid_columns()` DOES parse `repeat(2, 1fr)` → returns 2
- ❌ But ignores width ratios (e.g., `1fr 2fr` treated as equal width)
- ❌ internal_margin=1.5" is hardcoded, not CSS-derived from `body { padding }`
- ❌ The 0.15" gap is the inter-element gap; total row spacing is larger

**Recommendation**: Grid Layouter needs to parse width ratios (fr values, px, %), not just column counts.

### 2. Architecture — Simplified

**Original (Over-engineered)**:
- 5-stage pipeline
- 8 files total
- 60-80 lines per layouter (unrealistic)

**Corrected**:
- 3-stage pipeline (Component → Alignment → Page)
- Single-file refactor first
- Extract 4-5 functions, split files only after stable
- Each layouter 80-120 lines (includes edge cases)

### 3. Flattening Approach — Reconsidered

**Original (Dismissed flattening)**:
- "preserve hierarchy + absolute coordinate propagation"
- Claims flatten loses gap/padding semantics

**Corrected**:
- Current `_flatten_nested_containers()` is sophisticated (detects column membership, handles spanning, applies offsets)
- Flattening avoids recursive coordinate chains (error-prone)
- Hybrid might work: flatten for shallow (1 level), preserve for deep (2+)

### 4. Scoring — Flawed

**Original**:
- Linear unbounded penalty: each issue = 0.01 points
- 137 issues → 2.63/4.0 position score
- 20 issues → 3.80/4.0 (only +1.17 for fixing 117 items)

**Corrected**:
- Weight by severity: high=0.05, medium=0.02, low=0.005
- Exclude decorative elements from count
- 9.5/10 target needs ~50 issues or fewer (weighted)
- Coverage already 100%, headroom only in position_score

### 5. CSS Coverage — Critical Gaps

**Confirmed Active Usage** (must support):
- `grid-template-columns: repeat(N, 1fr)` → 7 files
- `grid-template-columns: 1fr 2fr` → ratio support needed
- `display: flex` → 413 occurrences
- `justify-content: center/space-between` → 135 center, 21 space-between
- `align-items: center/flex-start` → 142 center, 75 flex-start
- `box-sizing: border-box` → 47 occurrences, global

**NOT Used** (can ignore):
- `grid-template-areas` → 0 occurrences

### 6. Implementation Order — Reversed

**Original**:
1. Golden Diff
2. Extract Grid Layouter
3. Extract Flex Column
...

**Corrected**:
1. Define/stabilize IR schema (fields, units)
2. Extract Grid Layouter against IR
3. Extract Flex Column Layouter against IR
4. Wire up in `layout_slide_elements()`
5. Extract Flex Row Layouter
6. Clean up `layout_slide_elements()` → pure Y-stacking
7. Golden Diff as post-flight check

**Reason**: Intermediate states are broken if IR not stable first.

---

## Revised Architecture

```
Stage 1: HTML Parse (unchanged)
    ↓
Stage 2: Component Layouters (in same file, 4 functions)
    ┌─────────────────────────────────────────────────┐
    │ layout_grid_columns()                           │
    │ - Parse grid-template-columns (fr, px, %)       │
    │ - Calculate column widths & gaps                │
    │ - Return list of {x, width, span}               │
    │                                                 │
    │ layout_flex_row()                               │
    │ - Parse justify-content (center, space-between)│
    │ - Distribute items across container width       │
    │                                                 │
    │ layout_flex_column()                            │
    │ - Stack items vertically (gap, padding)         │
    │ - Return container bottom Y                     │
    └─────────────────────────────────────────────────┘
    ↓
Stage 3: Page Layouter (single function)
    - Y-stacking with CSS-based margin
    - Overflow splitter (already implemented)
    ↓
Stage 4: Golden Diff (diagnostic only)
    - After export completes
    - Report: 137 issues → weighted score
```

---

## Expected Outcomes (Revised)

| Metric | Current | Target |
|--------|---------|--------|
| Overflow pages | 0 | 0 ✓ |
| Text coverage | 100% | 100% ✓ |
| Position issues (>0.5") | 137 | < 20 |
| Position issues (>0.2") | ~200 | < 80 |
| Golden score (weighted) | 8.6/10 | 9.0+/10 |
| File count | 1 (3500 lines) | 1 (single refactor) |

---

## CSS Properties to Implement

| Property | Priority | Scope |
|----------|----------|-------|
| `grid-template-columns: repeat(N, 1fr)` | HIGH | Grid Layouter |
| `grid-template-columns: 1fr 2fr` (ratios) | HIGH | Grid Layouter |
| `grid-template-columns: 200px 1fr` | MEDIUM | Grid Layouter |
| `justify-content: center` | HIGH | Flex Row Layouter |
| `justify-content: space-between` | MEDIUM | Flex Row Layouter |
| `align-items: center` | HIGH | Flex Column Layouter |
| `align-items: flex-start` | MEDIUM | Flex Column Layouter |
| `box-sizing: border-box` | CRITICAL | Margin/Padding Resolver |
| `flex: 1` | MEDIUM | Flex Row (component sizing) |

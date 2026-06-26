# Markdown Table Format Specification

Sub-agents must strictly follow this specification when inserting tables in `.txt` files. Incorrect format causes table distortion during docx conversion.

## Correct Format

```
| Col1 | Col2 | Col3 |
|---|---|---|
| Content1 | Content2 | Content3 |
| Content4 | Content5 | Content6 |
```

## Six Key Rules

1. **Separator row must include leading and trailing `|`**
   - ✅ Correct: `|---|---|---|`
   - ❌ Wrong: `---|---|---` (missing leading/trailing `|`)
   - ❌ Wrong: `|---|:---|:---|` (missing leading/trailing `|` on separator row)

2. **All rows (including data rows) must have leading and trailing `|`**
   - Each row format: `| Cell1 | Cell2 | Cell3 |`

3. **All rows must have the same column count as the header**
   - If header has 4 columns, all data rows must also have 4 columns
   - Mismatch causes column displacement in docx

4. **Separator row only allows `-`, `:`, `|` and spaces**
   - ✅ `|---|`, `| :--- |` (alignment markers)
   - ❌ `|===|` (`=` not allowed)
   - ❌ `|--|--|` (missing leading/trailing `|`)

5. **Cell content must not contain line breaks**
   - Cell content must be completed on a single line

6. **Cell content should avoid containing `|` character**
   - Use `～` or `-` for ranges: `25—45` not `25|45`
   - If `|` must be included, escape it (not recommended)

## Common Error Examples

| Error Type | Wrong | Correct |
|------------|-------|---------|
| Missing leading/trailing `\|` | `\|---\|---\|---` | `\|---\|---\|---\|` |
| Inconsistent row/column count | `\|A\|B\|C\|` followed by `\|1\|2\|` (missing column) | `\|A\|B\|C\|` followed by `\|1\|2\| \|` |
| Separator row uses `=` | `\|====\|====\|` | `\|---\|---\|` |
| Cell contains `\|` | `\|25\|45\|` (range) | `\|25～45\|` |

## Recommended Symbols for Cell Content

| Purpose | Recommended Symbol | Example |
|---------|-------------------|---------|
| Numeric range | `～` or `—` | `25～45`, `25—45` |
| Percentage | `%` | `30%` |
| Rating | `★` (avoid `\|`) | `★★★☆☆` |
| Notes/Remarks | Write directly | `Including equipment maintenance service` |

## Validation Method

After generating docx, use this command to check if column counts are reasonable (normally 2~8 columns):

```python
from docx import Document
doc = Document('F:/agent/整合报告.docx')
for t in doc.tables:
    print(f'{len(t.rows)} rows x {len(t.columns)} cols')
    # Column count > 15 usually indicates table format error
```

## Why Format Errors Cause Distortion

`_add_table_to_doc` internally uses `max(len(r) for r in rows)` to calculate column count:
- After correct parsing: `rows[0] = ['Col1', 'Col2', 'Col3']`, `len = 3`
- When raw string is passed: `rows[0] = '| Col1 | Col2 | Col3 |'`, `len = 17` (character count)

17 columns vs 3 columns → each character occupies one cell → table completely distorted.

# Bug Troubleshooting & Forced Rebuild

## Fixed: Table Rendering Distortion

### Problem Description

In the generated docx, tables have only 1 column with content split character-by-character; or column count far exceeds expectation (e.g., 4-column table becomes 60+ columns).

### Root Cause

Bug in `_flush_table` function in `integrate_report.py`:

```python
# ❌ Buggy code (early v3)
def _flush_table(doc, pending_table):
    if pending_table:
        _add_table_to_doc(doc, pending_table)   # ← Passing raw string list!
        pending_table.clear()
```

- `pending_table` stores `['| Col1 | Col2 | Col3 |', ...]` (string list)
- `_add_table_to_doc` uses `max(len(r) for r in rows)` to calculate column count
- Calling `len()` on a string gives character count (17), not cell count (3)
- Result: 4-column table → 63 columns → each character occupies one cell → completely distorted

### Fix

```python
# ✅ Correct code (current version)
def _flush_table(doc, pending_table):
    if pending_table:
        parsed_rows = _parse_md_table(pending_table)  # ← NEW: parse to 2D array first
        _add_table_to_doc(doc, parsed_rows)           # ← Pass parsed array
        pending_table.clear()
```

### Validation

```python
from docx import Document
doc = Document('F:/agent/整合报告.docx')
for t in doc.tables:
    print(f'{len(t.rows)} rows x {len(t.columns)} cols')
    # Normal column count: 2~8 columns
    # If you see 15+, 30+, 60+ columns → Bug still exists
```

---

## Fixed: Cover Style Comparison Type Error

### Problem Description

`cover_style` in `plan.json` is an integer (e.g., `4`), but code compares as string, causing cover to always take the generic branch — styled cover doesn't apply.

### Root Cause

```python
# ❌ Buggy code
cover_style = plan.get('cover_style', '4')
if cover_style == '4':   # Integer 4 != String '4', always False
```

### Fix

```python
# ✅ Correct code
cover_style = str(plan.get('cover_style', '4'))
if cover_style == '4':   # String comparison, works correctly
```

---

## Fixed: RGB Color Assignment Error

### Problem Description

Using `eval(f'0x{hex_color}')` to assign color causes `run.font.color.rgb` to receive an integer instead of an `RGBColor` object, throwing an error.

### Root Cause

```python
# ❌ Buggy code
run.font.color.rgb = eval(f'0x{H1_TEXT}')  # eval('0xFFFFFF') → 16777215 (int)
# ValueError: rgb color value must be RGBColor object, got <class 'int'>
```

### Fix

```python
# ✅ Correct code
from docx.shared import RGBColor  # ← Must import
run.font.color.rgb = RGBColor.from_string(H1_TEXT)
```

---

## Fixed: Incremental Cache Causing New Code to Not Take Effect

### Problem Description

After modifying core logic in `integrate_report.py` and regenerating, incremental mode skips all chapters.

### Root Cause

Python caches compiled `.pyc` files. After modifying `.py`, if cache isn't deleted, the imported code is still the old version. Also `content_hashes.json` causes rewrite skipping.

### Fix

After every code change, do both:

```bash
# 1. Delete .pyc cache
del "C:\Users\Administrator\AppData\Roaming\LobsterAI\SKILLs\long-doc-agent\__pycache__\integrate_report.cpython-311.pyc"

# 2. Delete incremental hash
del F:\agent\chapters\content_hashes.json

# 3. Regenerate
python integrate_report.py
```

---

## Forced Rebuild

### Steps

```bash
# 1. Delete incremental cache and old report
del F:\agent\chapters\content_hashes.json
del F:\agent\整合报告.docx

# 2. Delete .pyc cache (required after code changes)
del "C:\Users\Administrator\AppData\Roaming\LobsterAI\SKILLs\long-doc-agent\__pycache__\integrate_report.cpython-311.pyc"

# 3. Regenerate
cd "C:\Users\Administrator\AppData\Roaming\LobsterAI\SKILLs\long-doc-agent"
python integrate_report.py
```

---

## New: RGBColor Property Access (python-docx 1.2.0)

### Problem Description

Error when running `make_docx.py`: `AttributeError: 'RGBColor' object has no attribute 'red'`

### Root Cause

python-docx 1.2.0's `RGBColor` object doesn't support `.red / .green / .blue` property access; must use index access.

### Fix

```python
# ❌ Wrong
'{:02X}{:02X}{:02X}'.format(rgb.red, rgb.green, rgb.blue)

# ✅ Correct
'{:02X}{:02X}{:02X}'.format(rgb[0], rgb[1], rgb[2])
```

---

## New: Cover Function Must Not Modify Global Page Margins

### Problem Description

Code in `add_cover()` setting `section.left_margin=0` etc. propagates to all pages after the cover, causing body text to fill the entire page (no margins).

### Root Cause

Word's Section properties persist across pages; margins set on the cover affect the entire document.

### Fix

Use a full-page table for the background color in the cover, **do not** modify any section margin properties. Set body margins once in `main()`.

```python
# ❌ Wrong
def add_cover(doc):
    sec = doc.sections[0]
    sec.left_margin=Inches(0)   # ← Affects all pages!
    ...

# ✅ Correct: only add table, don't touch section
def add_cover(doc):
    tbl_ = doc.add_table(rows=1, cols=1)
    cell = tbl_.rows[0].cells[0]
    # Just fill the table across the full page, don't touch section margin
```

---

## New: Auto-Rename When File Is Held Open

### Problem Description

If the generated docx file is already open in WPS/Word, saving again raises `PermissionError`.

### Fix

Add `_v2` suffix to filename (auto-increment), avoiding conflict with open files. In code:

```python
out_name = 'Hospital_Personnel_Location_Management_System_Proposal.docx'
out_path = os.path.join(out_dir, out_name)
if os.path.exists(out_path):
    # File exists, add v2/v3... to avoid conflict
    base, ext = os.path.splitext(out_name)
    counter = 2
    while os.path.exists(os.path.join(out_dir, f'{base}_v{counter}{ext}')):
        counter += 1
    out_name = f'{base}_v{counter}{ext}'
    out_path = os.path.join(out_dir, out_name)
```

---

## New: write Tool Has 50KB Line Limit — Large Scripts Must Use Chunked Writing

### Problem Description

Using `write` tool to write Python scripts > ~50KB or ~2000 lines results in truncated content (only partial code written).

### Root Cause

The write tool has a per-file size limit.

### Fix

Write large scripts in two steps:

```python
# Step 1: Write main file (excluding trailing main() call)
with open('make_docx.py', 'w', encoding='utf-8') as f:
    f.write(main_content)  # Main content

# Step 2: Append trailing portion
closing = """
def main():
    ...  # Trailing content

if __name__ == '__main__':
    main()
"""
with open('make_docx.py', 'a', encoding='utf-8') as f:
    f.write(closing)
```

---

## Other Common Issues

### Symptom: Table content all shows as `|`

`_parse_md_table` was not called. Confirm `_flush_table` contains `parsed_rows = _parse_md_table(pending_table)`.

### Symptom: Incremental mode skips modified chapters

Delete `content_hashes.json` to force full rebuild.

### Symptom: Sub-Agent-written txt contains garbled text

Sub-Agent output used wrong encoding. Ensure sub-agents save with `encoding='utf-8'`.

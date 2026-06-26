---
name: image-to-excel
description: Extract table content from images, retrieve row/column data, correct recognition errors, and generate a well-formatted Excel file. 
---

# Image to Excel

Extract tables from images and generate .xlsx files.

## Use Cases

Use when users upload images containing tables and request "convert to table", "extract table", or "generate Excel".

## Workflow

### 1. Analyze Image

Use the `image` tool to load the user-uploaded image, with a prompt requesting row-by-row, column-by-column table data extraction:

```
Extract all table data from the image row by row and column by column, returning it as a JSON array.
Format: [[row1col1, row1col2, ...], [row2col1, row2col2, ...], ...]
Notes:
- The first row may be a header; keep it as-is
- Split merged cells into individual cells and fill with the same value
- Preserve original formatting for amounts and numbers
- Use empty string "" for missing cells
```

### 2. Data Validation & Correction

After receiving the JSON data from the image model, check and correct:
- Row/column count consistency (fill in missing cells)
- Number format correctness (remove extra spaces, unify decimal points)
- Chinese character recognition accuracy (fix obvious typos)
- Header completeness (infer missing headers from content)

Store the corrected data in the variable `rows`.

### 3. Write to Excel

Call the generation script with the corrected data:

```bash
python3 scripts/gen_excel.py <output_path> '<json_data>'
```

- `output_path`: Output path, e.g., `/root/.openclaw/workspace/table_extracted.xlsx`
- `json_data`: Corrected 2D array as a JSON string

### 4. Output Results

Inform the user of the file save location and display a preview of the first 5 rows for confirmation.
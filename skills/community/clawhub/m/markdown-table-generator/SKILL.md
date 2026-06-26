---
name: markdown-table-generator
description: Generate, format, and manipulate Markdown tables with support for alignment, conversion from CSV/TSV, sorting, and transposition. Use when users need to create tables from data, format existing tables nicely, convert between table formats, sort table rows, or perform table operations like adding/removing columns and rows.
---

# Markdown Table Generator

A comprehensive skill for working with Markdown tables, from quick generation to advanced formatting and manipulation.

## Quick Start

### Generate a Basic Table

For simple data, create a table directly:

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

### Generate from Data

When given raw data (CSV, TSV, or space-separated):

1. Parse the input data
2. Detect headers if present
3. Determine column widths for proper alignment
4. Generate a nicely formatted table

**Example - CSV to Markdown Table:**

Input:
```csv
Name,Age,City
Alice,30,New York
Bob,25,London
Charlie,35,Tokyo
```

Output:
```markdown
| Name    | Age | City     |
|---------|-----|----------|
| Alice   | 30  | New York |
| Bob     | 25  | London   |
| Charlie | 35  | Tokyo    |
```

## Alignment Options

### Left Align (Default)
```markdown
| Name    | Age | City     |
|:--------|:----|:---------|
| Alice   | 30  | New York |
```

### Right Align
```markdown
| Name    | Age |     City |
|--------:|----:|---------:|
| Alice   |  30 | New York |
```

### Center Align
```markdown
|  Name   | Age |   City   |
|:-------:|:---:|:--------:|
|  Alice  | 30  | New York |
```

## Common Operations

### Add a Row
Insert at any position; default to end of table.

### Add a Column
Specify column name and position; default to end.

### Remove a Row/Column
Specify by index, header name, or content match.

### Sort Rows
Sort by a specific column in ascending or descending order.

### Transpose Table
Convert rows to columns and columns to rows.

## Best Practices

1. **Column Widths**: Always pad cells so pipes align vertically for readability
2. **Headers**: Keep headers descriptive and concise
3. **Empty Cells**: Use `&nbsp;` or leave empty for visual clarity
4. **Consistency**: Use the same alignment style throughout a document
5. **Readability**: Prefer left-aligned text, right-aligned numbers, centered short values

## Conversion to Other Formats

When needed, convert Markdown tables to:
- CSV
- TSV
- HTML `<table>`
- JSON array of objects

Always preserve data integrity during conversions.

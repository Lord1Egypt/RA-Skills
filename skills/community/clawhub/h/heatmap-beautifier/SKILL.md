---
name: heatmap-beautifier
description: Professional beautification tool for gene expression heatmaps, automatically adds clustering trees, color annotation tracks, and intelligently optimizes label layout.
license: MIT
skill-author: AIPOCH
---
# Heatmap Beautifier

Professional beautification tool for gene expression heatmaps, automatically adds clustering trees, color annotation tracks, and intelligently optimizes label layout.

## Input Validation

This skill accepts: CSV files containing gene expression matrices (genes as rows, samples as columns) for heatmap generation and beautification.

If the user's request does not involve heatmap generation or gene expression visualization — for example, asking to perform differential expression analysis, run statistical tests, or generate other chart types — do not proceed. Instead respond:
> "heatmap-beautifier is designed to generate and beautify gene expression heatmaps from expression matrix data. Your request appears to be outside this scope. Please provide a CSV expression matrix file, or use a more appropriate tool for your task."

Do not continue the workflow when the request is out of scope, missing the required input CSV, or would require unsupported assumptions. For missing inputs, state exactly which fields are missing.

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
# Demo mode (no CSV required):
python scripts/main.py --demo --output demo_heatmap.pdf
```

## When to Use

- Beautify gene expression heatmaps with clustering trees and annotation tracks
- Generate publication-ready heatmap output (PDF, PNG, SVG) with optimized label layout
- Add row/column annotation color bars to expression matrices
- Standardize heatmap styling for manuscript figures

## Workflow

1. **Validate input** — confirm the request is within scope before any processing.
2. Confirm the user objective, required inputs, and non-negotiable constraints.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Features

- **Automatic Clustering**: Adds row/column clustering trees based on hierarchical clustering
- **Annotation Tracks**: Supports multiple color annotation tracks (sample grouping, gene classification, etc.)
- **Smart Labels**: Automatically calculates optimal font size to avoid row/column label overlap
- **Flexible Color Schemes**: Built-in multiple professional scientific research color schemes
- **Export Options**: Supports PDF, PNG, SVG formats
- **Demo Mode**: Run `--demo` to generate a synthetic 20×10 matrix without a real CSV

## Dependencies

```text
pip install seaborn matplotlib scipy pandas numpy
```

## Usage

### Basic Usage

```python
from skills.heatmap_beautifier.scripts.main import HeatmapBeautifier

hb = HeatmapBeautifier()
hb.create_heatmap(
    data_path="expression_matrix.csv",
    output_path="output/heatmap.pdf"
)
```

### Command Line Usage

```text
python -m skills.heatmap_beautifier.scripts.main \
    --input expression_matrix.csv \
    --output heatmap.pdf

python -m skills.heatmap_beautifier.scripts.main \
    --input expression_matrix.csv \
    --output heatmap.pdf \
    --row-cluster \
    --col-cluster \
    --row-annotations row_annot.json \
    --col-annotations col_annot.json \
    --title "Gene Expression"

# Demo mode (no CSV required)
python -m skills.heatmap_beautifier.scripts.main --demo --output demo_heatmap.pdf

# Save clustering metadata to JSON for agent consumption
python -m skills.heatmap_beautifier.scripts.main \
    --input expression_matrix.csv \
    --output heatmap.pdf \
    --output-json heatmap_metadata.json
```

## Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `--data-path`, `-d` | string | - | Yes* | Path to input data file (CSV) |
| `--demo` | flag | - | No | Generate synthetic 20×10 demo matrix |
| `--output-path`, `-o` | string | heatmap.png | No | Output file path |
| `--title` | string | Gene Expression Heatmap | No | Heatmap title |
| `--cmap` | string | RdBu_r | No | Color map |
| `--center` | float | 0 | No | Color center value |
| `--vmin` | float | -2 | No | Minimum value for color scale |
| `--vmax` | float | 2 | No | Maximum value for color scale |
| `--row-cluster` | bool | true | No | Enable row clustering |
| `--col-cluster` | bool | true | No | Enable column clustering |
| `--standard-scale` | string | None | No | Standardization: row, col, None |
| `--z-score` | int | None | No | Z-score: 0 (row), 1 (col), None |
| `--figsize` | tuple | (12, 10) | No | Figure size (width, height) |
| `--dpi` | int | 300 | No | Resolution (dots per inch) |
| `--format` | string | pdf | No | Output format (pdf, png, svg) |
| `--output-json` | string | - | No | Save clustering metadata (gene_order, sample_order, annotation_colors) to JSON |

*One of `--data-path` or `--demo` is required.

## Input Data Format

### Expression Matrix (CSV)

```csv
,sample1,sample2,sample3,sample4
Gene_A,2.5,-1.2,0.8,-0.5
Gene_B,-0.8,1.5,-2.1,0.3
Gene_C,1.2,0.5,-0.7,1.8
```

- First column: Gene names (row index)
- First row: Sample names (column names)
- Data: Expression values (e.g., log2 fold change, TPM, FPKM)

## Color Schemes

- `"RdBu_r"` — Red-Blue (classic differential expression)
- `"viridis"` — Yellow-Purple (continuous data)
- `"RdYlBu_r"` — Red-Yellow-Blue
- `"coolwarm"` — Cool-Warm
- `"seismic"` — Seismic
- `"bwr"` — Blue-White-Red

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate files, citations, data, search results, or execution outcomes.
- **Exception handling**: The script uses `except (pd.errors.ParserError, UnicodeDecodeError, ValueError)` for CSV parsing errors — not bare `except`. If you see a bare except in an older version, report it.
- **Error propagation**: `FileNotFoundError` and `ValueError` are caught in `main()` with `try/except (FileNotFoundError, ValueError) as e: print(f'Error: {e}', file=sys.stderr); sys.exit(1)` and reported to stderr with exit code 1.

## Fallback Behavior

If `scripts/main.py` fails or required inputs are incomplete:
1. Report the exact failure point and error message.
2. State what can still be completed (e.g., data validation without rendering).
3. Manual fallback: verify CSV format has gene rows and sample columns, then re-run with minimal options: `python -m skills.heatmap_beautifier.scripts.main --input data.csv --output out.png`.
4. Use `--demo` to verify the environment works without a real CSV.
5. Do not fabricate execution outcomes or file contents.

## Output Requirements

Every final response must make these items explicit when relevant:

- Objective or requested deliverable
- Inputs used and assumptions introduced
- Workflow or decision path
- Core result, recommendation, or artifact
- Constraints, risks, caveats, or validation needs
- Unresolved items and next-step checks

## Response Template

Use the following fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

For stress/multi-constraint requests, also include:
- Constraints checklist (compliance, performance, error paths)
- Unresolved items with explicit blocking reasons

If the request is simple, you may compress the structure, but still keep assumptions and limits explicit when they affect correctness.

## Notes

1. Recommended to perform log2 transformation or standardization on data first
2. Large datasets (>5000 rows) may take longer to process
3. When there are too many rows/columns, some labels will be automatically hidden
4. Default clustering uses Euclidean distance and Ward method

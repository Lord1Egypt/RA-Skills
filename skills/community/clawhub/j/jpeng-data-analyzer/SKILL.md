---
name: jpeng-data-analyzer
description: "Data analysis and visualization skill. Supports CSV, Excel, JSON data with statistical analysis, charts, and reports."
version: "1.0.0"
author: "jpeng"
tags: ["data", "analysis", "visualization", "statistics", "charts"]
---

# Data Analyzer

Analyze datasets and generate visualizations with statistical insights.

## When to Use

- User wants to analyze a dataset
- Generate charts and visualizations
- Statistical analysis and summaries
- Data cleaning and transformation

## Features

- **Data formats**: CSV, Excel, JSON, Parquet
- **Statistics**: Mean, median, std dev, correlations
- **Visualizations**: Bar, line, pie, scatter, heatmap
- **Reports**: Auto-generated analysis reports

## Usage

### Quick analysis

```bash
python3 scripts/analyze.py \
  --input ./data.csv \
  --output ./report/
```

### Generate specific chart

```bash
python3 scripts/analyze.py \
  --input ./data.csv \
  --chart bar \
  --x "category" \
  --y "sales" \
  --output ./chart.png
```

### Statistical summary

```bash
python3 scripts/analyze.py \
  --input ./data.csv \
  --stats \
  --columns "age,income,score"
```

### Correlation analysis

```bash
python3 scripts/analyze.py \
  --input ./data.csv \
  --correlation \
  --output ./correlation_matrix.png
```

### Data transformation

```bash
python3 scripts/analyze.py \
  --input ./data.csv \
  --transform "normalize" \
  --columns "price,quantity" \
  --output ./normalized.csv
```

## Output

```json
{
  "success": true,
  "rows": 1000,
  "columns": 10,
  "stats": {
    "mean": {"age": 35.2, "income": 55000},
    "std": {"age": 12.3, "income": 15000}
  },
  "charts": ["./chart1.png", "./chart2.png"],
  "report": "./report.html"
}
```

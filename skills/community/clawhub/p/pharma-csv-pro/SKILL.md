---
name: pharma-csv-pro
description: Professional pharmaceutical CSV analysis with regulatory compliance, OOS/OOT detection, stability trending, and GMP-compliant reporting. Use for batch records analysis, stability studies, QC data validation, method validation, and regulatory submissions requiring USP/EP/ChP standard checks.
---

# Pharma CSV Pro - Professional Pharmaceutical Analysis

Enterprise-grade CSV analysis for pharmaceutical quality control, stability studies, and regulatory compliance.

## Quick Start

```bash
# Basic analysis with compliance check
python3 scripts/pharma_analyzer_pro.py data/batch_records.csv --compliance USP

# Stability study with trend analysis
python3 scripts/pharma_analyzer_pro.py data/stability.csv --study-type stability --trend-analysis

# Full regulatory report
python3 scripts/pharma_analyzer_pro.py data/qc_data.csv --report-type regulatory --output report.pdf
```

## Features

### Core Analysis
- **Data Validation**: Schema validation, missing data detection, outlier identification
- **Statistical Summary**: Descriptive stats, Cpk/Ppk calculations, control charts
- **Trend Analysis**: Regression, drift detection, shelf-life prediction

### Regulatory Compliance
- **USP/EP/ChP Standards**: Automated specification checking
- **OOS/OOT Detection**: Out-of-specification and out-of-trend flagging
- **Method Validation**: Accuracy, precision, linearity, range verification

### Reporting
- **GMP-Compliant Reports**: Audit trail, electronic signatures ready
- **Multiple Formats**: PDF, Excel, JSON, Markdown
- **Visualization**: Control charts, trend plots, histograms

## Usage Patterns

### Batch Record Analysis
```bash
python3 scripts/pharma_analyzer_pro.py batch_records.csv \
  --study-type batch \
  --specs "Assay:95.0-105.0,Impurity:<0.5" \
  --detect-oos
```

### Stability Study
```bash
python3 scripts/pharma_analyzer_pro.py stability_24mo.csv \
  --study-type stability \
  --time-column Month \
  --trend-analysis \
  --shelf-life-prediction
```

### QC Method Validation
```bash
python3 scripts/pharma_analyzer_pro.py method_val.csv \
  --study-type method-validation \
  --parameters "Accuracy,Precision,Linearity"
```

## Column Detection

Auto-detects pharmaceutical columns:
- `batch`, `lot`, `batch_number` → Batch/Lot identifiers
- `assay`, `potency`, `content` → Assay results (%)
- `impurity`, `related_substances`, `degradation` → Impurity levels
- `dissolution`, `dt`, `disintegration` → Dissolution (% or time)
- `hardness`, `friability` → Physical tests
- `expiry`, `expiration_date`, `retest_date` → Date tracking
- `storage_condition`, `temp`, `humidity` → Stability conditions

## Compliance Standards

### USP (United States Pharmacopeia)
- Assay limits: 95.0% - 105.0% (typical)
- Impurity thresholds per USP <621>, <1086>
- Dissolution Q-value (typically 75% or 80%)

### EP (European Pharmacopoeia)
- Similar assay ranges with EP-specific monographs
- Impurity reporting thresholds
- Dissolution acceptance criteria

### ChP (Chinese Pharmacopoeia)
- Assay specifications per ChP monographs
- Traditional Chinese Medicine (TCM) specific limits
- Microbial limits per ChP <1105>, <1106>

## Output Formats

- `json`: Machine-readable with full metadata
- `markdown`: Human-readable summary
- `excel`: Multi-sheet workbook with charts
- `pdf`: GMP-compliant formatted report

## Advanced Options

See `references/advanced-usage.md` for:
- Custom specification files
- Integration with LIMS systems
- API usage for automated pipelines
- Custom report templates

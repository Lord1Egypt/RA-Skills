# Advanced Usage Guide

## Custom Specification Files

Create a JSON specification file for complex analyses:

```json
{
  "product_name": "Example Tablet 100mg",
  "specifications": {
    "Assay": {
      "min": 95.0,
      "max": 105.0,
      "unit": "%",
      "critical": true
    },
    "Impurity_Total": {
      "max": 2.0,
      "unit": "%",
      "critical": true
    },
    "Dissolution_Q": {
      "min": 80.0,
      "unit": "%",
      "time_point": 30,
      "critical": true
    },
    "Hardness": {
      "min": 4.0,
      "max": 10.0,
      "unit": "kp"
    }
  },
  "stability": {
    "storage_conditions": ["25C/60%RH", "40C/75%RH"],
    "time_points": [0, 3, 6, 9, 12, 18, 24],
    "acceptance_criteria": {
      "Assay": {
        "min": 90.0,
        "max": 110.0
      }
    }
  }
}
```

## LIMS Integration

### API Usage Example

```python
from pharma_analyzer_pro import PharmaAnalyzerPro
import requests

# Analyze CSV
analyzer = PharmaAnalyzerPro('batch_data.csv')
result = analyzer.analyze(
    study_type='batch',
    compliance='USP',
    detect_oos=True
)

# Send results to LIMS
lims_api_url = 'https://lims.company.com/api/v1/results'
headers = {'Authorization': 'Bearer YOUR_TOKEN'}

for col_name, oos_list in result['oos_detection'].items():
    for oos in oos_list:
        payload = {
            'batch_id': result['batch_number'],
            'parameter': col_name,
            'value': oos['value'],
            'status': 'OOS',
            'timestamp': result['analysis_timestamp']
        }
        requests.post(lims_api_url, json=payload, headers=headers)
```

### Automated Pipeline

```bash
#!/bin/bash
# watch_folder.sh - Monitor folder for new CSV files

WATCH_DIR="/data/incoming"
PROCESSED_DIR="/data/processed"
REPORTS_DIR="/data/reports"

inotifywait -m -e create "$WATCH_DIR" --format '%f' | while read FILE; do
    if [[ "$FILE" == *.csv ]]; then
        echo "Processing: $FILE"
        
        python3 pharma_analyzer_pro.py "$WATCH_DIR/$FILE" \
            --study-type batch \
            --compliance USP \
            --detect-oos \
            --format json \
            --output "$REPORTS_DIR/${FILE%.csv}_report.json"
        
        mv "$WATCH_DIR/$FILE" "$PROCESSED_DIR/"
    fi
done
```

## Custom Report Templates

### Markdown Template Variables

Available variables for custom templates:

- `{{file}}` - Input file path
- `{{analysis_timestamp}}` - ISO timestamp
- `{{study_type}}` - Type of study
- `{{total_rows}}` - Number of data rows
- `{{total_columns}}` - Number of columns
- `{{pharma_columns}}` - Detected pharmaceutical columns
- `{{validation_issues}}` - List of data quality issues
- `{{oos_count}}` - Number of OOS results
- `{{compliance_status}}` - Overall compliance status

### Example Custom Template

```markdown
# QC Release Report

**Product:** {{product_name}}  
**Batch:** {{batch_number}}  
**Analysis Date:** {{analysis_date}}

## Executive Summary

{{#if compliance_status}}
✅ **RELEASE APPROVED** - All specifications met
{{else}}
❌ **RELEASE PENDING** - OOS investigation required
{{/if}}

## Critical Parameters

| Parameter | Result | Specification | Status |
|-----------|--------|---------------|--------|
{{#each critical_params}}
| {{name}} | {{result}} | {{spec}} | {{status}} |
{{/each}}

## Recommendations

{{recommendations}}

---
Analyst: _________________ Date: _________________  
Reviewer: _________________ Date: _________________
```

## Study-Specific Configurations

### Stability Study

```bash
python3 pharma_analyzer_pro.py stability_data.csv \
    --study-type stability \
    --trend-analysis \
    --specs "Assay:90-110,Impurity_Total:<3.0" \
    --format markdown \
    --output stability_report.md
```

### Method Validation

```bash
python3 pharma_analyzer_pro.py method_val.csv \
    --study-type method-validation \
    --specs "Accuracy:98-102,Precision_RSD:<2.0" \
    --format json \
    --output method_val_results.json
```

### Batch Release

```bash
python3 pharma_analyzer_pro.py batch_records.csv \
    --study-type batch \
    --compliance USP \
    --detect-oos \
    --format markdown \
    --output batch_release_report.md
```

## Troubleshooting

### Common Issues

1. **Encoding Problems**
   - Ensure CSV is UTF-8 encoded
   - Use `--encoding` flag if needed

2. **Date Format Parsing**
   - Standard formats: YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY
   - Custom formats: Modify date regex patterns in code

3. **Numeric Parsing**
   - Supports: 1,234.56, 1234.56, 1.234,56 (European)
   - Percent signs are automatically stripped

4. **Large Files**
   - Files > 100MB may require chunked processing
   - Consider sampling for initial analysis

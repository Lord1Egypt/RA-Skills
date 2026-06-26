# Pandas Skill Usage Examples

English | [简体中文](EXAMPLES_CN.md)

## Example 1: Complete Data Cleaning Workflow

Suppose you have a CSV file `sales_data.csv` containing sales data with missing values, duplicate rows, and outliers.

### Step 1: Analyze the Data
```bash
python scripts/data_analyzer.py sales_data.csv -o analysis_report.json
```

Review the report to understand data quality issues.

### Step 2: Clean the Data
```bash
python scripts/data_cleaner.py sales_data.csv cleaned_sales.csv \
    --standardize-columns \
    --remove-duplicates \
    --handle-missing median \
    --remove-outliers \
    --outlier-method iqr
```

### Step 3: Validate Results
```bash
python scripts/data_analyzer.py cleaned_sales.csv -o final_report.json
```

Compare before and after reports to confirm cleaning effectiveness.

---

## Example 2: Format Conversion

### CSV to Excel
```bash
python scripts/data_transformer.py convert data.csv report.xlsx
```

### Excel to JSON
```bash
python scripts/data_transformer.py convert input.xlsx output.json
```

### Multi-format Conversion
```bash
python scripts/data_transformer.py convert report.xlsx report.parquet
```

---

## Example 3: Data Filtering

### Filter by Condition
```bash
python scripts/data_transformer.py filter employees.csv \
    --query "age > 30 and department == 'Engineering'" \
    --output senior_engineers.csv
```

### Multi-condition Filter
```bash
python scripts/data_transformer.py filter sales.csv \
    --query "amount > 10000 and status in ['completed', 'shipped']" \
    --output high_value_sales.csv
```

---

## Example 4: Merging Multiple Files

### Vertical Merge (Concatenate)
```bash
python scripts/data_transformer.py merge \
    january.csv february.csv march.csv \
    --output q1_sales.csv
```

### Key-based Merge (SQL-style JOIN)
```bash
python scripts/data_transformer.py merge \
    customers.csv orders.csv \
    --output customer_orders.csv \
    --how left \
    --on customer_id
```

---

## Example 5: Data Sorting

### Single Column Sort
```bash
python scripts/data_transformer.py sort employees.csv \
    --by salary \
    --descending \
    --output sorted_by_salary.csv
```

### Multi-column Sort
```bash
python scripts/data_transformer.py sort data.csv \
    --by department salary \
    --output sorted.csv
```

---

## Example 6: Select Specific Columns

```bash
python scripts/data_transformer.py select full_data.csv \
    --columns name email phone department \
    --output contact_list.csv
```

---

## Example 7: Combined Operations

Complete data processing pipeline:

```bash
# 1. Clean raw data
python scripts/data_cleaner.py raw_data.csv clean_data.csv \
    --standardize-columns \
    --remove-duplicates \
    --handle-missing mean

# 2. Filter valid data
python scripts/data_transformer.py filter clean_data.csv \
    --query "status == 'active'" \
    --output active_data.csv

# 3. Sort by priority
python scripts/data_transformer.py sort active_data.csv \
    --by priority \
    --descending \
    --output final_data.csv

# 4. Convert to Excel report
python scripts/data_transformer.py convert final_data.csv report.xlsx

# 5. Generate final analysis
python scripts/data_analyzer.py final_data.csv -o final_analysis.json
```

---

## Common Use Cases

### Use Case 1: Prepare Machine Learning Data
```bash
# Clean and standardize
python scripts/data_cleaner.py raw_features.csv \
    ml_ready_data.csv \
    --remove-duplicates \
    --handle-missing mean \
    --remove-outliers \
    --standardize-columns
```

### Use Case 2: Generate Data Quality Report
```bash
python scripts/data_analyzer.py monthly_data.csv \
    --output quality_report.json \
    --format json
```

### Use Case 3: ETL Pipeline
```bash
# Extract: Merge multiple sources
python scripts/data_transformer.py merge source1.csv source2.csv source3.csv \
    --output extracted.csv

# Transform: Clean and filter
python scripts/data_cleaner.py extracted.csv transformed.csv \
    --handle-missing median \
    --remove-duplicates

# Load: Convert to target format
python scripts/data_transformer.py convert transformed.csv final_output.parquet
```

---

## Tips and Best Practices

1. **Always backup original data**
2. **Use analyzer to understand data** before cleaning
3. **Incremental cleaning**: Apply one operation at a time, verify results
4. **Save intermediate results**: Easy to trace back and debug
5. **Check reference docs**: `references/` directory contains detailed pandas guides

---

## Advanced Techniques

### Batch Process Multiple Files
```bash
# Windows PowerShell
Get-ChildItem *.csv | ForEach-Object {
    python scripts/data_cleaner.py $_.Name "cleaned_$($_.Name)" --remove-duplicates
}

# Linux/Mac
for file in *.csv; do
    python scripts/data_cleaner.py "$file" "cleaned_${file}" --remove-duplicates
done
```

### Use in Python Code
```python
import pandas as pd

# Read analysis report
import json
with open('report.json', 'r') as f:
    report = json.load(f)
    
# Check missing value percentage
missing_threshold = 0.3
cols_to_drop = [col for col, info in report['missing_values'].items() 
                if info['percentage'] > missing_threshold]

# Process directly with pandas
df = pd.read_csv('data.csv')
df = df.drop(columns=cols_to_drop)
```

### Custom Cleaning Workflow
```python
# Based on data_cleaner.py framework
import pandas as pd

df = pd.read_csv('input.csv')

# Custom business logic
df['amount'] = df['amount'].apply(lambda x: max(0, x))  # Amount cannot be negative
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Convert dates

# Save results
df.to_csv('output.csv', index=False)
```

---

## Troubleshooting

### Issue 1: Encoding Errors
```bash
# Try specifying encoding
python scripts/data_analyzer.py data.csv --encoding utf-8
# or
python scripts/data_analyzer.py data.csv --encoding gbk
```

### Issue 2: Out of Memory
```python
# For large files, use chunked reading
import pandas as pd

chunks = []
for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    # Process each chunk
    processed = chunk.dropna()
    chunks.append(processed)

result = pd.concat(chunks, ignore_index=True)
```

### Issue 3: Date Format Issues
```python
# Use explicit date format in scripts
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
```

---

## More Resources

- See [SKILL.md](SKILL.md) for complete skill documentation
- Refer to [references/common_operations.md](references/common_operations.md) to learn pandas operations
- Read [references/data_cleaning_best_practices.md](references/data_cleaning_best_practices.md) for best practices

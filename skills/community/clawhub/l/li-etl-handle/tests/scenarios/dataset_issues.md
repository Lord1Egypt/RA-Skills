# Problematic Datasets for Testing

## Issue Types Covered

### 1. Data Quality Issues
- Duplicate records
- Empty/null values
- Inconsistent formatting
- Missing required fields

### 2. Format Issues
- Mixed data types in columns
- Leading/trailing spaces
- Special characters
- Encoding problems

### 3. Structural Issues
- Inconsistent column names
- Merged cells (not supported)
- Multiple header rows
- Hidden rows/columns

### 4. Performance Issues
- Large datasets (>10000 rows)
- Complex formulas
- Multiple worksheets
- Embedded objects

## Test Files Generated

| File | Issue Type | Rows | Purpose |
|------|-----------|------|---------|
| scenario1_customers_clean.xlsx | Duplicates, Empty rows | 6→4 | Test cleaning |
| scenario2_*.xlsx | Multi-file merge | 8 total | Test merge |
| scenario3_late_report.xlsx | Filter, Sort | 6→3 | Test filter/sort |
| scenario4_raw.csv | Text formatting | 3 | Test CSV conversion |
| scenario5_inventory.xlsx | Calculations | 6 | Test aggregation |
| scenario6_transposed.xlsx | Transpose | 3×4→4×3 | Test transform |
| scenario7_large.xlsx | Performance | 5000 | Test speed |

## Expected Results

All scenarios should complete without errors and produce valid output files.

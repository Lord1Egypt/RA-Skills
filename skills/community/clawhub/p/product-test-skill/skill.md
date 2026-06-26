# Data Analyzer Skill

## Description
A data analysis skill that processes CSV files and generates summary statistics reports.

## Version
1.0.0

## Input
- `file_path` (string, required): Path to the CSV file to analyze
- `columns` (list, optional): Specific columns to include in the analysis

## Output
- `summary` (object): Statistical summary including mean, median, std, min, max for each numeric column
- `row_count` (integer): Total number of rows processed

## Permissions
- File read access (local workspace only)
- No network access required

## Usage Example
```
Input: {"file_path": "data/sales.csv", "columns": ["revenue", "quantity"]}
Output: {"summary": {"revenue": {"mean": 150.5, "median": 120.0}}, "row_count": 1000}
```

## Dependencies
- pandas >= 2.0.0
- numpy >= 1.24.0

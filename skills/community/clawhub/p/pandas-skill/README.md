# Pandas Data Processing Skill

English | [简体中文](README_CN.md)

A comprehensive skill for pandas-based data manipulation, cleaning, analysis, and transformation.

## Features

- **Data Cleaning**: Handle missing values, duplicates, outliers, and standardize data
- **Data Analysis**: Generate detailed statistical reports and data quality assessments
- **Data Transformation**: Convert formats, merge files, filter, sort, and reshape data
- **Reference Docs**: Comprehensive pandas operation guides and best practices

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Analyze Your Data
```bash
python scripts/data_analyzer.py your_data.csv -o report.json
```

### Clean Your Data
```bash
python scripts/data_cleaner.py raw_data.csv clean_data.csv \
    --remove-duplicates \
    --handle-missing mean \
    --standardize-columns
```

### Transform Data
```bash
# Convert format
python scripts/data_transformer.py convert data.csv data.xlsx

# Filter data
python scripts/data_transformer.py filter data.csv \
    --query "age > 18" \
    --output filtered.csv

# Merge files
python scripts/data_transformer.py merge file1.csv file2.csv \
    --output merged.csv
```

## Directory Structure

```
pandas-skill/
├── SKILL.md                      # Main skill documentation
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── scripts/
│   ├── data_cleaner.py          # Data cleaning tool
│   ├── data_analyzer.py         # Data analysis tool
│   └── data_transformer.py      # Data transformation tool
└── references/
    ├── common_operations.md     # Pandas operations reference
    └── data_cleaning_best_practices.md  # Best practices guide
```

## Documentation

- **SKILL.md**: Complete skill documentation with all capabilities and workflows
- **references/common_operations.md**: Quick reference for pandas operations
- **references/data_cleaning_best_practices.md**: Data cleaning strategies and patterns

## Use Cases

- Clean messy datasets before analysis
- Generate data quality reports
- Convert between data formats (CSV, Excel, JSON, Parquet)
- Merge multiple data sources
- Filter and aggregate data
- Detect and handle outliers
- Standardize data for machine learning

## Requirements

- Python 3.8+
- pandas 2.0+
- numpy 1.24+

## License

MIT License

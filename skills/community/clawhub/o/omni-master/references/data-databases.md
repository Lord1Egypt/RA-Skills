# Data Analysis & Databases

## Data Formats
- CSV, JSON, JSONL, TSV, Parquet, SQLite
- Transform with `jq`, `python3`, `awk`

## Analysis Tools
- **Python**: pandas, numpy, matplotlib, seaborn
- **Shell**: awk, sed, sort, uniq, cut, wc
- **Visualization**: matplotlib → PNG, plotly → HTML
- **Spreadsheets**: openpyxl (Excel), gog (Google Sheets)

## Database Operations

### SQLite
```bash
sqlite3 data.db ".tables"
sqlite3 data.db "SELECT * FROM users LIMIT 10;"
sqlite3 data.db ".schema tablename"
```

### PostgreSQL / MySQL
- Use appropriate CLI: `psql`, `mysql`
- Connection strings for Python libraries
- ORM options: SQLAlchemy, Prisma, Drizzle

## Analysis Workflow
1. **Ingest** — Load data (file, API, database, scrape)
2. **Clean** — Handle nulls, deduplicate, normalize types
3. **Transform** — Aggregate, join, pivot, calculate
4. **Analyze** — Statistics, trends, anomalies
5. **Visualize** — Charts, tables, dashboards
6. **Report** — Summarize findings, export results

## Common Patterns
```python
import pandas as pd
df = pd.read_csv('data.csv')
df.describe()  # Quick stats
df.groupby('category').sum()  # Aggregation
df.to_json('output.json', orient='records')  # Export
```

## Chart Types
- Bar chart — categorical comparison
- Line chart — trends over time
- Scatter plot — correlations
- Histogram — distribution
- Heatmap — matrix relationships
- Pie chart — composition (use sparingly)

## Data Sources
- Google Sheets via `gog` skill
- Web scraping via browser/fetch tools
- APIs via curl or Python requests
- Databases via CLI clients
- Files in workspace

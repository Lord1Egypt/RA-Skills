---
name: City of Ottawa Open Data
description: "Access 670+ datasets from the City of Ottawa open data portal. Search, fetch, and analyze city data on transit, environment, health, elections, and more via ArcGIS Hub."
permissions: Bash
triggers:
  - ottawa open data
  - city of ottawa data
  - ottawa dataset
  - open.ottawa.ca
  - ottawa transit
  - ottawa environment
---

# City of Ottawa Open Data

Access and analyze 670+ open datasets from the City of Ottawa via ArcGIS Hub. Data covers transit, environment, health, elections, infrastructure, and more.

**Portal:** https://open.ottawa.ca
**Platform:** ArcGIS Hub

## Quick Start

```bash
# Search for datasets
python3 scripts/ottawa_data.py search "transit"

# List all datasets
python3 scripts/ottawa_data.py list

# View dataset info
python3 scripts/ottawa_data.py info "Ottawa Ward Boundaries"

# Fetch data
python3 scripts/ottawa_data.py fetch "Ottawa Ward Boundaries" --limit 5

# Export as CSV
python3 scripts/ottawa_data.py fetch "Bus Routes" --limit 100 --csv > routes.csv

# List direct download URLs
python3 scripts/ottawa_data.py downloads
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `search <query>` | Search datasets by keyword |
| `list` | List all datasets |
| `info <name-or-id>` | Show dataset metadata and data source |
| `fetch <name-or-id>` | Fetch data (opts: `--limit`, `--csv`) |
| `downloads` | List datasets with direct download URLs |

## Data Sources

Ottawa datasets come in three types:
1. **ArcGIS Feature Services** — Queryable geospatial data
2. **ArcGIS Map Services** — Read-only map layers
3. **Document Links** — Direct file downloads

## Data Sources

All data from open.ottawa.ca.

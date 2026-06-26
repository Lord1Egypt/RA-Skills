---
name: City of Montreal Open Data
description: "Access 398+ datasets from the City of Montreal open data portal. Search, fetch, and analyze city data on crime, transit, environment, permits, and more via the CKAN API."
permissions: Bash
triggers:
  - montreal open data
  - city of montreal data
  - montreal dataset
  - donnees montreal
  - montreal transit
  - montreal crime
---

# City of Montreal Open Data

Access and analyze 398+ open datasets from the City of Montreal via the CKAN API. Data covers crime, transit, environment, permits, employment, and more.

**Portal:** https://donnees.montreal.ca
**Platform:** CKAN
**Language:** Data and metadata primarily in French

## Quick Start

```bash
# Search for datasets
python3 scripts/montreal_data.py search "crime"

# List all datasets
python3 scripts/montreal_data.py list

# View dataset info
python3 scripts/montreal_data.py info actes-criminels

# Fetch data
python3 scripts/montreal_data.py fetch actes-criminels --limit 5

# Export as CSV
python3 scripts/montreal_data.py fetch actes-criminels --limit 100 --csv > crimes.csv

# List queryable datasets
python3 scripts/montreal_data.py searchable
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `search <query>` | Search datasets by keyword (French) |
| `list` | List all datasets |
| `info <dataset-id>` | Show dataset metadata and resources |
| `fetch <dataset-id>` | Fetch data from datastore (opts: `--limit`, `--csv`) |
| `searchable` | List datasets with queryable resources |

## Language Note

Montreal publishes data primarily in French. Search queries should use French terms.

## Data Sources

All data from donnees.montreal.ca under the Quebec Open Government Licence.

---
name: City of Lethbridge Open Data
description: "Access 123+ datasets from the City of Lethbridge open data portal. Search, fetch, and analyze city data on transit, infrastructure, elections, environment, and more via ArcGIS Hub."
permissions: Bash
triggers:
  - lethbridge open data
  - city of lethbridge data
  - lethbridge dataset
  - opendata.lethbridge.ca
  - lethbridge transit
  - lethbridge gis
---

# City of Lethbridge Open Data

Access and analyze 123+ open datasets from the City of Lethbridge via ArcGIS Hub. Data covers transit, infrastructure, elections, environment, tourism, and more.

**Portal:** https://opendata.lethbridge.ca
**Platform:** ArcGIS Hub

## Quick Start

```bash
# Search for datasets
python3 scripts/lethbridge_data.py search "traffic"

# List all datasets
python3 scripts/lethbridge_data.py list

# View dataset info
python3 scripts/lethbridge_data.py info "Traffic Counts"

# Fetch data from ArcGIS feature service
python3 scripts/lethbridge_data.py fetch "Traffic Counts" --limit 5

# Fetch with field filter
python3 scripts/lethbridge_data.py fetch "Intersection Safety Devices" --limit 10 --format json

# Export as CSV
python3 scripts/lethbridge_data.py fetch "City Boundary" --csv

# List all datasets with download links
python3 scripts/lethbridge_data.py downloads
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `search <query>` | Search datasets by keyword |
| `list` | List all datasets |
| `info <name-or-id>` | Show dataset metadata and data source |
| `fetch <name-or-id>` | Fetch data (opts: `--limit`, `--format json/csv`, `--csv`) |
| `downloads` | List datasets with direct file download URLs |

## Data Sources

Lethbridge datasets come in three types:

1. **ArcGIS Feature Services** — Queryable geospatial data (parks, streets, boundaries)
2. **ArcGIS Map Services** — Read-only map layers
3. **Document Links** — Direct file downloads (Excel, CSV, PDF)

The CLI auto-detects the source type and uses the appropriate method.

## ArcGIS REST API

Geospatial datasets use the ArcGIS REST query API:
- Endpoint: `https://gis.lethbridge.ca/gisopendata/rest/services/OpenData/`
- Supports `where`, `outFields`, `resultRecordCount`, `f` (json/geojson) parameters
- Max 2000 records per query

## Data Sources

All data is sourced from the City of Lethbridge's Open Data Portal (opendata.lethbridge.ca). See [references/datasets.md](references/datasets.md) for a curated list of popular datasets.

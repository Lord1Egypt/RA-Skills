# hifld — Homeland Infrastructure Foundation-Level Data

## What this source has

HIFLD provides open data on US critical infrastructure through ArcGIS REST services. Datasets include:

- Hospitals and medical facilities
- Power plants and electrical substations
- Dams and levees
- Bridges and tunnels
- Emergency services (fire stations, police stations)
- Communications infrastructure (cell towers, broadcast towers)
- Transportation (airports, rail stations, ports)
- Education facilities
- Government buildings

Use HIFLD for: infrastructure proximity analysis ("what hospitals are near X"), critical facility lookup, disaster preparedness research, and property due diligence.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

All data is publicly accessible via standard ArcGIS REST API. No key required.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | standard ArcGIS REST terms |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `query` | Query any HIFLD feature service | `service` (path param), `where`, `outFields`, `resultRecordCount` |

## Worked examples

```bash
# Query hospitals in California
python3 scripts/reach.py query hifld query '{"service": "USA_Hospitals", "where": "STATE = '\''CA'\''", "outFields": "*", "resultRecordCount": 10}'

# Query power plants near a location
python3 scripts/reach.py query hifld query '{"service": "USA_Power_Plants", "where": "STATE = '\''CA'\''", "outFields": "NAME,STATE,PRIMSOURCE,CAPACITY", "resultRecordCount": 5}'

# Query dams
python3 scripts/reach.py query hifld query '{"service": "USA_Dams", "where": "1=1", "outFields": "DAM_NAME,STATE,PURPOSES,NID_STORAGE", "resultRecordCount": 5}'
```

## Response shape

Standard ArcGIS REST FeatureSet JSON:

```json
{
  "displayFieldName": "NAME",
  "fields": [...],
  "features": [
    {
      "attributes": {
        "NAME": "UCSF Medical Center",
        "STATE": "CA",
        "CITY": "San Francisco",
        "TYPE": "General Medical and Surgical Hospitals"
      },
      "geometry": { "x": -122.4194, "y": 37.7749 }
    }
  ]
}
```

## Pitfalls

- **Service names must match exactly.** The `service` path parameter corresponds to the ArcGIS service name (e.g., `USA_Hospitals`, `USA_Power_Plants`). Browse the HIFLD open data site for the full list.
- **Geometry is in WGS84 (SRID 4326).** Coordinates are longitude/latitude.
- **Large datasets.** Some services have 100k+ features. Always use `resultRecordCount` to limit results and `where` clauses to filter.
- **Field names are uppercase.** Most HIFLD datasets use uppercase field names (`NAME`, `STATE`, `CITY`).
- **Where clause syntax follows ArcGIS standards.** Use single quotes for string values, escape properly in JSON.

## Source links

- HIFLD Open Data: https://hifld-gis.opendata.arcgis.com
- ArcGIS REST API docs: https://developers.arcgis.com/rest/
- Dataset catalog: https://hifld-gis.opendata.arcgis.com/search?type=Feature%20Layer

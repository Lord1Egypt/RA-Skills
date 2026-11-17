# ev_charging — Open Charge Map API

## What this source has

Open Charge Map is the global directory of electric vehicle charging stations. Data includes:

- Charging station locations worldwide
- Connector types (CCS, CHAdeMO, Tesla, Type 2, etc.)
- Operator and network information
- Power output (kW)
- Availability status (where available)
- Usage cost and comments

Use ev_charging for: finding EV chargers near a location, trip planning with EV charging stops, property research ("are there chargers near X"), and complementing geo sources with amenity-specific data.

## Auth

| | |
|---|---|
| Required | none |
| Account | optional |

Anonymous read access available. API key provides higher rate limits and submission capabilities.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | throttle to <2/sec |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `poi` | Search charging points of interest | none (optional: `latitude`, `longitude`, `distance`, `countrycode`, `maxresults`) |
| `reference_data` | Get reference data (connector types, operators, etc.) | none |

## Worked examples

```bash
# Find chargers near San Francisco
python3 scripts/reach.py query ev_charging poi '{"latitude": 37.7749, "longitude": -122.4194, "distance": 10, "distanceunit": "km", "maxresults": 10}'

# Find chargers in a country
python3 scripts/reach.py query ev_charging poi '{"countrycode": "US", "maxresults": 5}'

# Get reference data (connector types, operators)
python3 scripts/reach.py query ev_charging reference_data '{}'

# Find chargers by operator
python3 scripts/reach.py query ev_charging poi '{"operatorid": 1, "maxresults": 10}'
```

## Response shape

**POI** returns an array of charging station objects:

```json
[
  {
    "ID": 12345,
    "UUID": "...",
    "DataProviderID": 1,
    "OperatorID": 1,
    "UsageTypeID": 1,
    "AddressInfo": {
      "Title": "UCSF Medical Center",
      "AddressLine1": "505 Parnassus Ave",
      "Town": "San Francisco",
      "StateOrProvince": "CA",
      "Postcode": "94143",
      "Country": { "Title": "United States" },
      "Latitude": 37.7631,
      "Longitude": -122.4586
    },
    "Connections": [
      {
        "ConnectionTypeID": 2,
        "LevelID": 2,
        "PowerKW": 50.0,
        "Quantity": 2
      }
    ],
    "NumberOfPoints": 2,
    "StatusTypeID": 50,
    "DateLastStatusUpdate": "2024-01-10T00:00:00Z"
  }
]
```

**Reference data** returns lists of connector types, operators, usage types, status types, etc.

## Pitfalls

- **Data is community-sourced.** Coverage varies by region. North America and Europe are well-covered; other regions may have gaps.
- **Distance is in km by default.** Use `distanceunit` parameter to specify miles (`"miles"`).
- **Max results default is 100.** Use pagination for large result sets.
- **Status is not real-time.** `StatusTypeID` indicates operational status but may not reflect current availability. Some networks provide real-time status via separate APIs.
- **Complements geo sources.** Use Nominatim/Photon for geocoding an address, then EV Charging to find nearby chargers.
- **Operator and connector reference data.** Use `reference_data` action to get valid IDs for filtering.

## Source links

- Open Charge Map: https://openchargemap.org/
- API docs: https://api.openchargemap.io/v3/
- GitHub: https://github.com/openchargemap/ocm-docs

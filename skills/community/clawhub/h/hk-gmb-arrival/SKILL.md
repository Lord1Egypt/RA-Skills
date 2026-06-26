---
name: hk-gmb-arrival
description: Real-time arrival information for Hong Kong Green Mini Buses (GMB). Supports fuzzy stop name matching and multi-region route lookup.
version: 1.0.0
source: https://github.com/StevenHo1394/openclaw/tree/main/skills/hk-gmb-arrival
tools:
  - name: searchRoutes
    description: Search for GMB route numbers across all regions (HKI, KLN, NT). Returns matching regions or suggestions if no exact match.
    command: python3 /home/node/.openclaw/workspace/skills/hk-gmb-arrival/gmb_arrival.py searchRoutes {route}
    inputSchema:
      type: object
      required:
        - route
      properties:
        route:
          type: string
          description: GMB route number (e.g., "1", "3", "5")
    output:
      format: json
  - name: getGMBArrival
    description: Get the next 3 arrival times for a GMB route at a specific stop. Requires route number, direction (1 or 2), stop name (English or Chinese), and region.
    command: python3 /home/node/.openclaw/workspace/skills/hk-gmb-arrival/gmb_arrival.py getGMBArrival {route} {direction} {stopName} {region}
    inputSchema:
      type: object
      required:
        - route
        - direction
        - stopName
        - region
      properties:
        route:
          type: string
          description: GMB route number (e.g., "1")
        direction:
          type: string
          description: "Direction sequence: \"1\" for terminus A → B, \"2\" for B → A"
        stopName:
          type: string
          description: Stop name (partial or full, in English or Chinese)
        region:
          type: string
          description: "Region code: \"HKI\" (Hong Kong Island), \"KLN\" (Kowloon), or \"NT\" (New Territories)"
    output:
      format: json

---
# Implementation Notes

## API Endpoints (Base URL: https://data.etagmb.gov.hk)

- `GET /route` - List all routes grouped by region (HKI, KLN, NT)
- `GET /route/{region}/{route}` - Get route details including directions (route_seq) and route_id
- `GET /stop-route/{stop_id}` - Get stop names (name_en, name_tc) and the routes serving that stop
- `GET /eta/stop/{stop_id}` - Get real-time ETA for all routes at that stop

Additionally, static route data is sourced from:
- `https://hkbus.github.io/hk-bus-crawling/routeFareList.min.json` - Contains mapping from route identifiers to stop ID sequences for GMB (and other operators).

## Script: gmb_arrival.py

Key functions:
- `searchRoutes(route)`: Queries `/route`, finds which regions contain this route number. If none, suggests similar route numbers.
- `get_gmb_arrival(route, direction, stop_name, region)`:
  1. Fetch `/route/{region}/{route}` to obtain route_id and the direction details (origin/destination names).
  2. Construct composite route key using the origin/destination English names and load from `routeFareList.json` to get the ordered list of stop IDs for that direction.
  3. For each stop ID along the route, fetch `/stop-route/{stop_id}` to retrieve stop names (cached).
  4. Match the user-provided `stop_name` (case-insensitive) exactly; if not found, perform fuzzy matching and return suggestions.
  5. Once stop ID is identified, call `/eta/stop/{stop_id}`.
  6. Filter ETA entries for the desired `route_id` and `route_seq` (direction), extract up to 3 next arrival timestamps, format as "HH:MM HKT".
  7. Return JSON: `{ "stopId": "...", "stopName": "...", "arrivals": [ "17:35 HKT", ... ] }`.

## Caching Strategy

- `routes_all.json`: All route list (1 hour)
- `route_details.json`: Route details per region/route (5 minutes)
- `routeFareList.json`: Static route-to-stop mapping (1 day)
- `stop_names.json`: Stop ID to names mapping (1 week)
- ETA responses: 30 seconds

Cache files stored in `data/` subdirectory.

## Error Handling

- Network errors and API failures are caught and reported in JSON with an `error` field.
- If route not found: returns `found: false` with `suggestions` array.
- If stop name not found: returns `error` with `suggestions` mapping suggestion → stop ID.
- If no active ETA: returns empty `arrivals` array with an informative `message`.

## Usage Example (Command Line)

```bash
# Search route
python3 gmb_arrival.py searchRoutes 1
# => {"route":"1","found":true,"regions":["HKI","KLN","NT"]}

# Get arrival for route 1 direction 1 (The Peak → Central) at "Hong Kong Station Minibus Terminus" in HKI
python3 gmb_arrival.py getGMBArrival 1 1 "Hong Kong Station Minibus Terminus" HKI
# => {"stopId":"20014492","stopName":"Hong Kong Station Minibus Terminus","arrivals":["14:38 HKT","14:45 HKT","14:52 HKT"]}
```

## Notes

- Direction sequence: For each GMB route, the API defines `route_seq` 1 and 2. Use `searchRoutes` then inspect route details to determine which sequence corresponds to your desired direction, or use `getGMBArrival` directly if you know the direction number.
- Stop names are matched case-insensitively. Chinese or English names both work.
- The static `routeFareList` may lag behind official data by up to one day but is generally reliable.
- Rate limits: The script caches aggressively to minimize API calls; still, avoid excessive polling (ETA updates every minute).

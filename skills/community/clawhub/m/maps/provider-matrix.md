# Provider Matrix - Maps

Use this matrix to choose the first provider instead of defaulting blindly.

| Task | Start here | Switch when | Why |
|------|------------|-------------|-----|
| Open a map or route for the user | Apple Maps or Google Maps link | Platform mismatch or user preference | Launch workflows are about UX, not structured data richness |
| Rich place search and business details | Google Maps | Paid quota is not acceptable or coverage is weak | Google usually has the richest place metadata |
| Forward geocoding at low cost | Nominatim or other OSM stack | Need stronger rooftop confidence or stricter SLA | Open data is cheap but precision varies |
| Reverse geocoding | Google Maps or Mapbox | Only coarse locality is needed | Reverse geocoding quality varies more than forward geocoding |
| Route ETA and waypoint optimization | Google Routes or Mapbox Directions | Budget is tight and rough estimates are acceptable | Premium routing usually wins on richer mode and traffic support |
| Distance matrix or many OD pairs | Google Matrix or Mapbox Matrix | Budget is tight or traffic is not needed | Matrix calls are where quota can explode fastest |
| Static map image or shareable preview | Google Static Maps or Mapbox Static | Link-only output is enough | Static map APIs need stricter URL and marker limits |
| Open-data fallback | Nominatim plus OSRM | Coverage or SLA is insufficient | Good fallback when paid providers are blocked or unnecessary |

## Provider Deltas

### Google Maps
- Best for: place richness, broad coverage, route features, business metadata
- Watch for: quota burn, paid usage, multiple APIs with different limits

### Apple Maps
- Best for: opening maps for humans, route launch on Apple devices, lightweight share links
- Watch for: app-launch workflows are not the same as structured API records

### OpenStreetMap Stack
- Best for: low-cost geocoding fallback, open data, and transparent map data
- Watch for: stricter usage policies, weaker place detail consistency, less polished route metadata

### Mapbox
- Best for: developer-facing geocoding, routing, and static map APIs with strong docs
- Watch for: GeoJSON-style coordinate ordering and token-scoped limits

### HERE or Other Providers
- Best for: enterprise contracts, regional coverage, or a user-mandated stack
- Watch for: schema drift, custom auth rules, and provider-specific licensing constraints

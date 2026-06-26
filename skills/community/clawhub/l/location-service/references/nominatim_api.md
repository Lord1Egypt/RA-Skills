# OpenStreetMap Nominatim API

## Overview
Nominatim is a search engine for OpenStreetMap data that allows geocoding and reverse geocoding.

## API Endpoints

### Forward Geocoding (Address → Coordinates)
```
GET https://nominatim.openstreetmap.org/search
```
Parameters:
- `q`: The search query (address, place name, etc.)
- `format`: Output format (json, jsonv2, xml, etc.)
- `limit`: Maximum number of results to return
- `addressdetails`: Include address breakdown in response (0 or 1)

### Reverse Geocoding (Coordinates → Address)
```
GET https://nominatim.openstreetmap.org/reverse
```
Parameters:
- `lat`: Latitude
- `lon`: Longitude
- `format`: Output format
- `zoom`: Level of detail (0-18, where higher is more detailed)
- `addressdetails`: Include address breakdown (0 or 1)

## Usage Policy
- Maximum 1 request per second
- Provide a valid User-Agent header identifying your application
- For heavy usage, consider using your own instance
- Data is available under the Open Database License (ODbL)

## Response Format (JSON)
### Forward Geocoding Response
```json
[
  {
    "place_id": "...",
    "licence": "...",
    "osm_type": "...",
    "osm_id": "...",
    "lat": "...",
    "lon": "...",
    "display_name": "...",
    "address": {
      // address components
    },
    "boundingbox": [min_lat, max_lat, min_lon, max_lon]
  }
]
```

### Reverse Geocoding Response
```json
{
  "place_id": "...",
  "licence": "...",
  "osm_type": "...",
  "osm_id": "...",
  "lat": "...",
  "lon": "...",
  "display_name": "...",
  "address": {
    // address components
  },
  "boundingbox": [min_lat, max_lat, min_lon, max_lon]
}
```

## Error Handling
- HTTP 429: Rate limit exceeded
- HTTP 400: Bad request (invalid parameters)
- Empty results: No matching data found

## Examples
See `examples.md` for common usage patterns.
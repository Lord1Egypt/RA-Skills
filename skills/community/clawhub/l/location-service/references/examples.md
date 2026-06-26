# Location Service Examples

## Common Use Cases

### 1. Get address from coordinates
**Input:** `41.9028,12.4964`
**Output:** `Piazza della Repubblica, 00185 Roma RM, Italia`

### 2. Get coordinates from address
**Input:** `Trevi Fountain, Rome`
**Output:** `41.9009,12.4833`

### 3. Calculate distance between two points
**Input:** `41.9028,12.4964 to 40.7128,-74.0060`
**Output:** `4283.41 km (2661.59 mi)`
*(Rome to New York City)*

### 4. Get weather for location
**Input:** `weather for 41.9028,12.4964`
**Output:** *(Current weather for Rome from weather skill)*

### 5. Google Maps link → coordinates
**Input:** `https://maps.google.com/?q=41.9028,12.4964`
**Output:** `41.9028,12.4964`
*(Extracted coordinates from Google Maps URL)*

### 6. Google Maps short link → coordinates
**Input:** `https://maps.app.goo.gl/AbCdEfGhIjKlMnOp`
**Output:** `41.9028,12.4964`
*(Short URL resolved and coordinates extracted)*

### 7. Google Maps link → address
**Input:** `https://maps.google.com/?q=41.9028,12.4964`
**Output:** `Piazza della Repubblica, 00185 Roma RM, Italia`
*(Coordinates extracted from link, then reverse geocoded)*

### 8. Google Maps link → weather
**Input:** `weather for https://maps.google.com/?q=41.9028,12.4964`
**Output:** *(Current weather for Rome from weather skill)*
*(Coordinates extracted from link, then passed to weather skill)*

### 9. Google Maps link → distance
**Input:** `https://maps.google.com/?q=41.9028,12.4964 to https://maps.google.com/?q=40.7128,-74.0060`
**Output:** `4283.41 km (2661.59 mi)`
*(Both coordinates extracted from their respective links)*

### 10. Chained operations
**Input:** `Colosseum, Rome` → get coordinates → get weather
**Workflow:**
1. Forward geocode "Colosseum, Rome" → `41.8902,12.4922`
2. Get weather for `41.8902,12.4922`

### 11. Chained operations via Google Maps link
**Input:** `https://maps.app.goo.gl/AbCdEfGhIjKlMnOp` → get address → get weather
**Workflow:**
1. Resolve short URL → full Google Maps URL
2. Extract coordinates → `41.8902,12.4922`
3. Reverse geocode → `Piazza del Colosseo, Roma`
4. Get weather for `41.8902,12.4922`

***

## Format Guidelines

### Coordinates
- Decimal degrees: `41.9028,12.4964`
- Separated by comma, no spaces required but tolerated
- Latitude first, then longitude
- Valid ranges: latitude [-90, 90], longitude [-180, 180]

### Addresses/Places
- Free text: street addresses, landmarks, cities, etc.
- Examples:
  - "Via del Corso, Rome"
  - "Eiffel Tower, Paris"
  - "Central Park, New York"
  - "1600 Amphitheatre Parkway, Mountain View"

### Google Maps Links (NEW)
Supported URL formats that are automatically parsed to extract coordinates:

| Format | Example |
|---|---|
| `maps.google.com/?q=lat,lon` | `https://maps.google.com/?q=41.9028,12.4964` |
| `maps.google.com/?ll=lat,lon` | `https://maps.google.com/?ll=41.9028,12.4964&z=15` |
| `google.com/maps/@lat,lon,z` | `https://www.google.com/maps/@41.9028,12.4964,15z` |
| `google.com/maps/place/.../@lat,lon` | `https://www.google.com/maps/place/Colosseo/@41.8902,12.4922,17z` |
| `maps.app.goo.gl/...` (short URL) | `https://maps.app.goo.gl/AbCdEfGhIjKlMnOp` |

> **Note:** Short URLs (`maps.app.goo.gl`) require an HTTP redirect resolution step before coordinate extraction. The script handles this automatically via `requests` with `allow_redirects=True`.

### Distance Calculations
- Format: `<lat1>,<lon1> to <lat2>,<lon2>`
- The word "to" separates the two coordinate pairs
- Spaces around "to" are optional
- **Also supported:** Google Maps links on either or both sides:
  - `https://maps.google.com/?q=41.9028,12.4964 to 40.7128,-74.0060`
  - `41.9028,12.4964 to https://maps.google.com/?q=40.7128,-74.0060`
  - `https://maps.google.com/?q=41.9028,12.4964 to https://maps.google.com/?q=40.7128,-74.0060`

### Weather Queries
- Format: `weather for <coordinates>` or `weather for <address>`
- **Also supported:** `weather for <google_maps_link>`
- Can use coordinates, address, or a Google Maps link as the location specifier

***

## Error Cases

### Invalid Coordinates
- `91.0,0.0` → Error: Latitude must be between -90 and 90
- `0.0,181.0` → Error: Longitude must be between -180 and 180

### Not Found
- `ThisPlaceDoesNotExist12345` → Error: Location not found
- `999.0,999.0` → Error: Address not found (valid coordinates but no data)

### Invalid or Unresolvable Google Maps Links
- Malformed URL → Error: Could not parse coordinates from Google Maps link
- Expired short URL → Error: Failed to resolve short URL (HTTP error)
- URL with no coordinate data (e.g., a search with only a place name and no `@lat,lon`) → Error: No coordinates found in URL; try using the place name directly as an address input

***

## Integration Notes
- All scripts return results via stdout
- Error messages go to stderr (except where noted in individual scripts)
- Exit code 0 = success, non-zero = failure
- Scripts validate input before making API calls
- Rate limiting: Be mindful of Nominatim's 1 request/second policy
- **Google Maps URL parsing** is handled client-side via regex — no Google API key required
- **Short URL resolution** uses a standard HTTP HEAD/GET request with redirect following; no external dependencies beyond `requests`

# Command Map

| Command | Method | API | Auth | Required Flags | Optional Flags |
| --- | --- | --- | --- | --- | --- |
| `geocode` | GET | Geocoding | query | `--address` | — |
| `reverse-geocode` | GET | Geocoding | query | `--latlng` | — |
| `directions` | POST | Routes v2 | header | `--origin`, `--dest` | `--mode` (DRIVE/WALK/BICYCLE/TRANSIT) |
| `places-search` | POST | Places v1 | header | `--query` | `--location`, `--radius` |
| `places-nearby` | POST | Places v1 | header | `--location`, `--radius` | `--type` |
| `place-detail` | GET | Places v1 | header | `--place-id` | — |
| `elevation` | GET | Elevation | query | `--locations` | — |
| `timezone` | GET | Timezone | query | `--location` | `--timestamp` |

## Coordinate Order
- Google Maps uses **lat,lng** order (e.g. `35.6585,139.7454`)

## Auth Modes
- **query**: API key appended as `?key=` query parameter (legacy APIs)
- **header**: API key sent via `X-Goog-Api-Key` header (new APIs)

## Exit Codes
- `0`: success
- `2`: input or config error
- `3`: network / timeout / HTTP transport error
- `4`: Google Maps API business error
- `5`: unexpected internal error

## API Key
- Required env var: `GOOGLE_MAPS_API_KEY`

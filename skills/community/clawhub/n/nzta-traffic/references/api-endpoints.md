# NZTA Traffic and Travel API Reference

Base URL: `https://trafficnz.info/service/traffic/rest/4/`

All endpoints accept `Accept: application/json` header. No authentication required.

## Regions

| ID | Name |
|----|------|
| 1 | Northland |
| 2 | Auckland |
| 3 | Waikato |
| 4 | Bay Of Plenty |
| 5 | Gisborne |
| 6 | Hawkes Bay |
| 7 | Taranaki |
| 8 | Manawatu-Whanganui |
| 9 | Wellington |
| 10 | Nelson/Marlborough |
| 11 | Canterbury |
| 12 | West Coast |
| 13 | Otago |
| 14 | Southland |

## Endpoints

### Road Events

- `events/all/{zoom}` — all events nationwide
- `events/byregion/{region}/{zoom}` — events in a region (name or ID)
- `events/byjourney/{journeyId}/{zoom}` — events on a highway
- `events/withinbounds/{minlon}/{minlat}/{maxlon}/{maxlat}/{zoom}` — events in bounding box

Zoom level: 1-20 for geometry detail, -1 for no geometry, 0 for raw geometry.

### Journeys (Highways)

- `journeys/all/{zoom}` — all journeys
- `journeys/byregion/{region}/{zoom}` — journeys in a region
- `journeys/withinbounds/{minlon}/{minlat}/{maxlon}/{maxlat}/{zoom}` — journeys in bounding box

### Cameras

- `cameras/all` — all cameras
- `cameras/byregion/{region}` — cameras in a region
- `cameras/byjourney/{journeyId}` — cameras on a highway
- `cameras/withinbounds/{minlon}/{minlat}/{maxlon}/{maxlat}` — cameras in bounding box

### Signs

- `signs/vms/all` — all Variable Message Signs
- `signs/vms/region/{region}` — VMS in a region
- `signs/tim/all` — all Traffic Information Messages
- `signs/tim/byregion/{region}` — TIM signs in a region

### Regions and Ways

- `regions/all/{zoom}` — all regions
- `ways/all/{zoom}` — all state highway ways
- `ways/byregion/{region}/{zoom}` — ways in a region

## Response Fields

### Road Event

| Field | Description |
|-------|-------------|
| id | Event ID |
| eventType | Type: "Road Works", "Crash", "Area Warning", "Weather", etc. |
| eventDescription | Short description |
| eventComments | Detailed comments |
| impact | Severity: "Closed", "Major delays", "Minor delays", "Caution", "Watch and observe" |
| status | "Active", "Pending", "Resolved" |
| planned | Boolean — true for scheduled works |
| locationArea | Human-readable location |
| startDate | ISO 8601 start time |
| endDate | ISO 8601 end time (if known) |
| expectedResolution | When expected to clear |
| alternativeRoute | Suggested alternative |
| region.name | Region name |
| journey.name | Highway name (e.g. "SH1") |
| journeyLeg.name | Leg description (e.g. "Porirua to Wellington") |

### Camera

| Field | Description |
|-------|-------------|
| id | Camera ID |
| name | Camera name/location |
| latitude | WGS84 latitude |
| longitude | WGS84 longitude |
| imageUrl | URL to latest camera image |
| region.name | Region name |

### Journey

| Field | Description |
|-------|-------------|
| id | Journey ID (use with --journey) |
| name | Highway name (e.g. "SH1") |
| startLatitude/Longitude | Start point |
| endLatitude/Longitude | End point |
| time | Current travel time estimate (format "HH:MM:SS", "00:00:00" if unavailable) |

# Late Brake - Track Data Format Definition

> **Late Brake Project Documentation**
>
> This document defines the JSON format specification for track metadata in Late Brake.
> Late Brake uses independent JSON files to store track information, supporting both built-in tracks and user custom tracks.

## Overview

Track analysis heavily depends on track metadata. Late Brake uses independent JSON files to store track information, supporting both built-in tracks and user custom tracks.

## Track File Location Convention

- **Built-in tracks**: Stored under `data/tracks/` in installation directory
- **User custom tracks**: Default location is `~/.late-brake/tracks/` directory
- **Each track corresponds to one independent JSON file**, filename format: `{track-id}.json`

## Track File JSON Structure Definition

```json
{
  "id": "saic",
  "name": "Shanghai International Circuit",
  "full_name": "Shanghai International Circuit",
  "location": "Shanghai, China",
  "length_m": 5451,
  "turn_count": 16,

  "anchor": {
    "lat": 31.3401765,
    "lon": 121.219292,
    "radius_m": 1062
  },

  "gate": [
    [31.3375154, 121.2223689],
    [31.3378142, 121.2222865]
  ],

  "geofence": [
    [lat, lon],
    ...
  ],

  "centerline": [
    [lat, lon],
    ...
  ],

  "sectors": [
    {
      "id": 1,
      "name": "Sector 1",
      "start_distance_m": 0,
      "end_distance_m": 2020,
      "turns": [1, 2, 3, 4, 5, 6]
    },
    {
      "id": 2,
      "name": "Sector 2",
      "start_distance_m": 2020,
      "end_distance_m": 3740,
      "turns": [7, 8, 9, 10]
    },
    {
      "id": 3,
      "name": "Sector 3",
      "start_distance_m": 3740,
      "end_distance_m": 5451,
      "turns": [11, 12, 13, 14, 15, 16]
    }
  ],

  "turns": [
    {
      "name": "T1",
      "type": "left-right",
      "start_distance_m": 120,
      "apex_distance_m": 280,
      "apex_coordinates": [31.3389, 121.2218],
      "end_distance_m": 350,
      "radius_m": 85,
      "min_speed_target": 165
    },
    {
      "name": "T2",
      "type": "right",
      "start_distance_m": 350,
      "apex_distance_m": 410,
      "apex_coordinates": [31.3395, 121.2205],
      "end_distance_m": 460,
      "radius_m": 35,
      "min_speed_target": 110
    }
  ]
}
```

## Field Description

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique track identifier |
| `name` | string | Yes | Track English name |
| `full_name` | string | No | Full track name (can include locale name) |
| `location` | string | No | Track geographic location |
| `length_m` | number | Yes | Total track length (meters) |
| `turn_count` | number | Yes | Total number of corners |
| `anchor` | object | Yes | Track anchor for GPS data matching |
| `anchor.lat` | number | Yes | Anchor latitude |
| `anchor.lon` | number | Yes | Anchor longitude |
| `anchor.radius_m` | number | Yes | Track search radius (meters) |
| `gate` | array | Yes | Two GPS coordinates defining start/finish line |
| `geofence` | array | No | Track boundary GPS coordinate array |
| `centerline` | array | Yes | Track centerline GPS coordinate array (in driving order) |
| `sectors` | array | No | Track sector information |
| `turns` | array | No | Detailed information for each corner |

## New Field Description

### Track Sectors (sectors)
- `id`: Sector ID
- `name`: Sector name
- `start_distance_m`: Distance from track start to sector start (meters)
- `end_distance_m`: Distance from track start to sector end (meters)
- `turns`: List of corner numbers included in this sector

### Corner Information (turns)
- `name`: Corner name (usually T{number})
- `type`: Corner type: `left`/`right`/`left-right`/`right-left` etc.
- `start_distance_m`: Distance from track start to corner entry (meters)
- `apex_distance_m`: Distance from track start to apex (meters)
- `apex_coordinates`: Apex GPS coordinates, `[latitude, longitude]`
- `end_distance_m`: Distance from track start to corner exit
- `radius_m`: Corner radius (meters), leave empty for complex corners
- `min_speed_target`: Minimum target speed at apex (km/h, V-min). Minimum apex speed is more useful for driving reference than maximum speed

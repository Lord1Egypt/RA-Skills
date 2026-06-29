# Multi-Location Route Optimizer W Map Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `multi-location-route-optimizer-w-map`

x402 availability: not enabled for this product.

## `create_route_map`

Action slug: `create-route-map`

Price: `25` credits

Generate a static map image showing the route with labeled markers at each location.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `locations` | `array` | yes | List of 2-25 locations in the desired order. Each location must have either an address OR latitude/longitude coordinates. |
| `map_height` | `integer` | no | Map image height in pixels (1-640) |
| `map_width` | `integer` | no | Map image width in pixels (1-640) |
| `travel_mode` | `string` | no | Mode of transportation (used for Google Maps URL) |

Sample parameters:

```json
{
  "locations": [
    {
      "address": "example address",
      "latitude": -90,
      "longitude": -180,
      "name": "example name",
      "service_time_minutes": 0
    }
  ],
  "map_height": 640,
  "map_width": 640,
  "travel_mode": "driving"
}
```

Generated JSON parameter schema:

```json
{
  "locations": {
    "description": "List of 2-25 locations in the desired order. Each location must have either an address OR latitude/longitude coordinates.",
    "items": {
      "properties": {
        "address": {
          "description": "Street address or place name",
          "required": false,
          "type": "string"
        },
        "latitude": {
          "description": "Latitude coordinate (-90 to 90)",
          "maximum": 90,
          "minimum": -90,
          "required": false,
          "type": "number"
        },
        "longitude": {
          "description": "Longitude coordinate (-180 to 180)",
          "maximum": 180,
          "minimum": -180,
          "required": false,
          "type": "number"
        },
        "name": {
          "description": "Optional name/label for this location",
          "required": false,
          "type": "string"
        },
        "service_time_minutes": {
          "description": "Time spent at this location in minutes",
          "minimum": 0,
          "required": false,
          "type": "integer"
        }
      },
      "type": "object"
    },
    "maxItems": 25,
    "minItems": 2,
    "required": true,
    "type": "array"
  },
  "map_height": {
    "default": 640,
    "description": "Map image height in pixels (1-640)",
    "maximum": 640,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "map_width": {
    "default": 640,
    "description": "Map image width in pixels (1-640)",
    "maximum": 640,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "travel_mode": {
    "default": "driving",
    "description": "Mode of transportation (used for Google Maps URL)",
    "enum": [
      "driving",
      "walking",
      "bicycling",
      "transit"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `get_route_details`

Action slug: `get-route-details`

Price: `25` credits

Get turn-by-turn directions for locations in the provided order (does not reorder them).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `avoid` | `array` | no | Features to avoid on the route |
| `locations` | `array` | yes | List of 2-25 locations in the desired visit order. Each location must have either an address OR latitude/longitude coordinates. |
| `travel_mode` | `string` | no | Mode of transportation |

Sample parameters:

```json
{
  "avoid": [
    "tolls"
  ],
  "locations": [
    {
      "address": "example address",
      "latitude": -90,
      "longitude": -180,
      "name": "example name",
      "service_time_minutes": 0
    }
  ],
  "travel_mode": "driving"
}
```

Generated JSON parameter schema:

```json
{
  "avoid": {
    "description": "Features to avoid on the route",
    "items": {
      "enum": [
        "tolls",
        "highways",
        "ferries"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "locations": {
    "description": "List of 2-25 locations in the desired visit order. Each location must have either an address OR latitude/longitude coordinates.",
    "items": {
      "properties": {
        "address": {
          "description": "Street address or place name",
          "required": false,
          "type": "string"
        },
        "latitude": {
          "description": "Latitude coordinate (-90 to 90)",
          "maximum": 90,
          "minimum": -90,
          "required": false,
          "type": "number"
        },
        "longitude": {
          "description": "Longitude coordinate (-180 to 180)",
          "maximum": 180,
          "minimum": -180,
          "required": false,
          "type": "number"
        },
        "name": {
          "description": "Optional name/label for this location",
          "required": false,
          "type": "string"
        },
        "service_time_minutes": {
          "description": "Time spent at this location in minutes",
          "minimum": 0,
          "required": false,
          "type": "integer"
        }
      },
      "type": "object"
    },
    "maxItems": 25,
    "minItems": 2,
    "required": true,
    "type": "array"
  },
  "travel_mode": {
    "default": "driving",
    "description": "Mode of transportation",
    "enum": [
      "driving",
      "walking",
      "bicycling",
      "transit"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `optimize_route`

Action slug: `optimize-route`

Price: `25` credits

Find the most efficient order to visit 2-25 locations, minimizing total travel time or distance. Returns optimized route with distance/duration totals, a Google Maps navigation URL, and optimization stats.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `avoid` | `array` | no | Features to avoid on the route |
| `departure_time` | `string` | no | Departure time in ISO format (e.g., '2026-01-15T09:00:00') or 'now' for current time. Traffic-aware routing (driving mode only). |
| `end_location` | `object` | no | Fixed ending point if different from last location in list. Ignored when return_to_start is true. |
| `include_directions` | `boolean` | no | Include detailed turn-by-turn directions in response |
| `include_map` | `boolean` | no | Generate and include a visual map of the route |
| `locations` | `array` | yes | List of 2-25 locations to visit. Each location must have either an address OR latitude/longitude coordinates. |
| `map_height` | `integer` | no | Map image height in pixels (1-640) |
| `map_width` | `integer` | no | Map image width in pixels (1-640) |
| `optimize_for` | `string` | no | Optimization priority |
| `return_to_start` | `boolean` | no | Whether to return to starting location (round trip) |
| `start_location` | `object` | no | Fixed starting point if different from first location in list |
| `travel_mode` | `string` | no | Mode of transportation |

Sample parameters:

```json
{
  "avoid": [
    "tolls"
  ],
  "departure_time": "example departure time",
  "end_location": {
    "address": "example address",
    "latitude": -90,
    "longitude": -180,
    "name": "example name"
  },
  "include_directions": false,
  "include_map": false,
  "locations": [
    {
      "address": "example address",
      "latitude": -90,
      "longitude": -180,
      "name": "example name",
      "service_time_minutes": 0
    }
  ],
  "map_height": 640,
  "map_width": 640
}
```

Generated JSON parameter schema:

```json
{
  "avoid": {
    "description": "Features to avoid on the route",
    "items": {
      "enum": [
        "tolls",
        "highways",
        "ferries"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "departure_time": {
    "description": "Departure time in ISO format (e.g., '2026-01-15T09:00:00') or 'now' for current time. Traffic-aware routing (driving mode only).",
    "required": false,
    "type": "string"
  },
  "end_location": {
    "description": "Fixed ending point if different from last location in list. Ignored when return_to_start is true.",
    "properties": {
      "address": {
        "description": "Street address or place name",
        "required": false,
        "type": "string"
      },
      "latitude": {
        "description": "Latitude coordinate (-90 to 90)",
        "maximum": 90,
        "minimum": -90,
        "required": false,
        "type": "number"
      },
      "longitude": {
        "description": "Longitude coordinate (-180 to 180)",
        "maximum": 180,
        "minimum": -180,
        "required": false,
        "type": "number"
      },
      "name": {
        "description": "Optional name for end location",
        "required": false,
        "type": "string"
      }
    },
    "required": false,
    "type": "object"
  },
  "include_directions": {
    "default": false,
    "description": "Include detailed turn-by-turn directions in response",
    "required": false,
    "type": "boolean"
  },
  "include_map": {
    "default": false,
    "description": "Generate and include a visual map of the route",
    "required": false,
    "type": "boolean"
  },
  "locations": {
    "description": "List of 2-25 locations to visit. Each location must have either an address OR latitude/longitude coordinates.",
    "items": {
      "properties": {
        "address": {
          "description": "Street address or place name (e.g., '123 Main St, New York, NY' or 'Times Square')",
          "required": false,
          "type": "string"
        },
        "latitude": {
          "description": "Latitude coordinate (-90 to 90)",
          "maximum": 90,
          "minimum": -90,
          "required": false,
          "type": "number"
        },
        "longitude": {
          "description": "Longitude coordinate (-180 to 180)",
          "maximum": 180,
          "minimum": -180,
          "required": false,
          "type": "number"
        },
        "name": {
          "description": "Optional name/label for this location (e.g., 'Customer A', 'Warehouse')",
          "required": false,
          "type": "string"
        },
        "service_time_minutes": {
          "description": "Time spent at this location in minutes",
          "minimum": 0,
          "required": false,
          "type": "integer"
        }
      },
      "type": "object"
    },
    "maxItems": 25,
    "minItems": 2,
    "required": true,
    "type": "array"
  },
  "map_height": {
    "default": 640,
    "description": "Map image height in pixels (1-640)",
    "maximum": 640,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "map_width": {
    "default": 640,
    "description": "Map image width in pixels (1-640)",
    "maximum": 640,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "optimize_for": {
    "default": "time",
    "description": "Optimization priority",
    "enum": [
      "time",
      "distance"
    ],
    "required": false,
    "type": "string"
  },
  "return_to_start": {
    "default": false,
    "description": "Whether to return to starting location (round trip)",
    "required": false,
    "type": "boolean"
  },
  "start_location": {
    "description": "Fixed starting point if different from first location in list",
    "properties": {
      "address": {
        "description": "Street address or place name",
        "required": false,
        "type": "string"
      },
      "latitude": {
        "description": "Latitude coordinate (-90 to 90)",
        "maximum": 90,
        "minimum": -90,
        "required": false,
        "type": "number"
      },
      "longitude": {
        "description": "Longitude coordinate (-180 to 180)",
        "maximum": 180,
        "minimum": -180,
        "required": false,
        "type": "number"
      },
      "name": {
        "description": "Optional name for start location",
        "required": false,
        "type": "string"
      }
    },
    "required": false,
    "type": "object"
  },
  "travel_mode": {
    "default": "driving",
    "description": "Mode of transportation",
    "enum": [
      "driving",
      "walking",
      "bicycling",
      "transit"
    ],
    "required": false,
    "type": "string"
  }
}
```

# Map Generator With Markers Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `map-generator-with-markers`

x402 availability: not enabled for this product.

## `create_map`

Action slug: `create-map`

Price: `20` credits

Generate a static map image with markers plotted at specific coordinates, with optional path connecting points.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `draw_path` | `boolean` | no | Connect points with a path line. Requires at least 2 points. |
| `image_height` | `integer` | no | Image height in pixels (max 640) |
| `image_width` | `integer` | no | Image width in pixels (max 640) |
| `map_type` | `string` | no | Map type to display |
| `marker_color` | `string` | no | Default marker color name or hex for all points (overridden by per-point color) |
| `marker_size` | `string` | no | Default marker size for all points (overridden by per-point size) |
| `path_color` | `string` | no | Path color in hex format (e.g., 0x0000ff for blue) |
| `path_weight` | `integer` | no | Path line weight in pixels |
| `points` | `array` | yes | Points to plot as markers. Each point requires latitude and longitude coordinates. |
| `scale` | `integer` | no | Scale factor for high DPI displays (1 or 2) |
| `zoom` | `integer` | no | Zoom level (0-21). Auto-calculated if omitted when markers/path are provided. |

Sample parameters:

```json
{
  "draw_path": false,
  "image_height": 640,
  "image_width": 640,
  "map_type": "roadmap",
  "marker_color": "example marker color",
  "marker_size": "tiny",
  "path_color": "0x0000ff",
  "path_weight": 5
}
```

Generated JSON parameter schema:

```json
{
  "draw_path": {
    "default": false,
    "description": "Connect points with a path line. Requires at least 2 points.",
    "required": false,
    "type": "boolean"
  },
  "image_height": {
    "default": 640,
    "description": "Image height in pixels (max 640)",
    "maximum": 640,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "image_width": {
    "default": 640,
    "description": "Image width in pixels (max 640)",
    "maximum": 640,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "map_type": {
    "default": "roadmap",
    "description": "Map type to display",
    "enum": [
      "roadmap",
      "satellite",
      "hybrid",
      "terrain"
    ],
    "required": false,
    "type": "string"
  },
  "marker_color": {
    "description": "Default marker color name or hex for all points (overridden by per-point color)",
    "required": false,
    "type": "string"
  },
  "marker_size": {
    "description": "Default marker size for all points (overridden by per-point size)",
    "enum": [
      "tiny",
      "small",
      "mid"
    ],
    "required": false,
    "type": "string"
  },
  "path_color": {
    "default": "0x0000ff",
    "description": "Path color in hex format (e.g., 0x0000ff for blue)",
    "required": false,
    "type": "string"
  },
  "path_weight": {
    "default": 5,
    "description": "Path line weight in pixels",
    "maximum": 20,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "points": {
    "description": "Points to plot as markers. Each point requires latitude and longitude coordinates.",
    "items": {
      "properties": {
        "color": {
          "description": "Marker color name or hex (e.g., red, blue, 0xFFFF00). Overrides global marker_color.",
          "required": false,
          "type": "string"
        },
        "label": {
          "description": "Single alphanumeric label (A-Z, 0-9). Only supported for default/mid size markers.",
          "required": false,
          "type": "string"
        },
        "latitude": {
          "description": "Latitude coordinate (-90 to 90)",
          "maximum": 90,
          "minimum": -90,
          "required": true,
          "type": "number"
        },
        "longitude": {
          "description": "Longitude coordinate (-180 to 180)",
          "maximum": 180,
          "minimum": -180,
          "required": true,
          "type": "number"
        },
        "size": {
          "description": "Marker size for this point. Overrides global marker_size.",
          "enum": [
            "tiny",
            "small",
            "mid"
          ],
          "required": false,
          "type": "string"
        }
      },
      "type": "object"
    },
    "minItems": 1,
    "required": true,
    "type": "array"
  },
  "scale": {
    "default": 1,
    "description": "Scale factor for high DPI displays (1 or 2)",
    "maximum": 2,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "zoom": {
    "description": "Zoom level (0-21). Auto-calculated if omitted when markers/path are provided.",
    "maximum": 21,
    "minimum": 0,
    "required": false,
    "type": "integer"
  }
}
```

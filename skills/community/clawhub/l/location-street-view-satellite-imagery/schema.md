# Location Street View & Satellite Imagery Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `location-street-view-satellite-imagery`

x402 availability: not enabled for this product.

## `geocode`

Action slug: `geocode`

Price: `15` credits

Convert a street address or place name into geographic coordinates, place ID, and address components.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `string` | yes | The street address or place name to geocode. |

Sample parameters:

```json
{
  "address": "example address"
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "The street address or place name to geocode.",
    "required": true,
    "type": "string"
  }
}
```

## `get_satellite_image`

Action slug: `get-satellite-image`

Price: `15` credits

Retrieve a satellite, roadmap, hybrid, or terrain image for a location. Returns a signed URL (valid 7 days), base64-encoded image, and metadata.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `string` | no | Street address or place name for the target location. Required if latitude/longitude are not provided. |
| `image_height` | `integer` | no | Image height in pixels. |
| `image_width` | `integer` | no | Image width in pixels. |
| `latitude` | `number` | no | Latitude coordinate (-90 to 90). Required if address is not provided. |
| `longitude` | `number` | no | Longitude coordinate (-180 to 180). Required if address is not provided. |
| `map_type` | `string` | no | Map type for the image. satellite=raw aerial, hybrid=satellite+labels, roadmap=standard map, terrain=elevation. |
| `zoom` | `integer` | no | Zoom level. Higher values are more zoomed in (15=neighborhood, 18=building, 21=max). |

Sample parameters:

```json
{
  "address": "example address",
  "image_height": 640,
  "image_width": 640,
  "latitude": -90,
  "longitude": -180,
  "map_type": "satellite",
  "zoom": 18
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "Street address or place name for the target location. Required if latitude/longitude are not provided.",
    "required": false,
    "type": "string"
  },
  "image_height": {
    "default": 640,
    "description": "Image height in pixels.",
    "maximum": 640,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "image_width": {
    "default": 640,
    "description": "Image width in pixels.",
    "maximum": 640,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "latitude": {
    "description": "Latitude coordinate (-90 to 90). Required if address is not provided.",
    "maximum": 90,
    "minimum": -90,
    "required": false,
    "type": "number"
  },
  "longitude": {
    "description": "Longitude coordinate (-180 to 180). Required if address is not provided.",
    "maximum": 180,
    "minimum": -180,
    "required": false,
    "type": "number"
  },
  "map_type": {
    "default": "satellite",
    "description": "Map type for the image. satellite=raw aerial, hybrid=satellite+labels, roadmap=standard map, terrain=elevation.",
    "enum": [
      "roadmap",
      "satellite",
      "hybrid",
      "terrain"
    ],
    "required": false,
    "type": "string"
  },
  "zoom": {
    "default": 18,
    "description": "Zoom level. Higher values are more zoomed in (15=neighborhood, 18=building, 21=max).",
    "maximum": 21,
    "minimum": 0,
    "required": false,
    "type": "integer"
  }
}
```

## `get_street_view_image`

Action slug: `get-street-view-image`

Price: `15` credits

Retrieve a Street View photograph for a location. Checks availability before fetching. Returns a signed URL (valid 7 days), base64-encoded image, and metadata including panorama ID and capture date.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `string` | no | Street address or place name to photograph. Required if latitude/longitude are not provided. |
| `fov` | `integer` | no | Field of view in degrees. Lower values zoom in. |
| `heading` | `integer` | no | Camera compass heading in degrees. Omit to let the API choose automatically. |
| `image_height` | `integer` | no | Image height in pixels. |
| `image_width` | `integer` | no | Image width in pixels. |
| `latitude` | `number` | no | Latitude coordinate (-90 to 90). Required if address is not provided. |
| `longitude` | `number` | no | Longitude coordinate (-180 to 180). Required if address is not provided. |
| `pitch` | `integer` | no | Camera vertical angle. Negative values look down, positive look up. |

Sample parameters:

```json
{
  "address": "example address",
  "fov": 90,
  "heading": 0,
  "image_height": 640,
  "image_width": 640,
  "latitude": -90,
  "longitude": -180,
  "pitch": 0
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "Street address or place name to photograph. Required if latitude/longitude are not provided.",
    "required": false,
    "type": "string"
  },
  "fov": {
    "default": 90,
    "description": "Field of view in degrees. Lower values zoom in.",
    "maximum": 120,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "heading": {
    "description": "Camera compass heading in degrees. Omit to let the API choose automatically.",
    "maximum": 360,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "image_height": {
    "default": 640,
    "description": "Image height in pixels.",
    "maximum": 640,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "image_width": {
    "default": 640,
    "description": "Image width in pixels.",
    "maximum": 640,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "latitude": {
    "description": "Latitude coordinate (-90 to 90). Required if address is not provided.",
    "maximum": 90,
    "minimum": -90,
    "required": false,
    "type": "number"
  },
  "longitude": {
    "description": "Longitude coordinate (-180 to 180). Required if address is not provided.",
    "maximum": 180,
    "minimum": -180,
    "required": false,
    "type": "number"
  },
  "pitch": {
    "default": 0,
    "description": "Camera vertical angle. Negative values look down, positive look up.",
    "maximum": 90,
    "minimum": -90,
    "required": false,
    "type": "integer"
  }
}
```

## `reverse_geocode`

Action slug: `reverse-geocode`

Price: `15` credits

Convert latitude/longitude coordinates into a human-readable address with place ID and address components.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `latitude` | `number` | yes | Latitude coordinate (-90 to 90). |
| `longitude` | `number` | yes | Longitude coordinate (-180 to 180). |

Sample parameters:

```json
{
  "latitude": -90,
  "longitude": -180
}
```

Generated JSON parameter schema:

```json
{
  "latitude": {
    "description": "Latitude coordinate (-90 to 90).",
    "maximum": 90,
    "minimum": -90,
    "required": true,
    "type": "number"
  },
  "longitude": {
    "description": "Longitude coordinate (-180 to 180).",
    "maximum": 180,
    "minimum": -180,
    "required": true,
    "type": "number"
  }
}
```

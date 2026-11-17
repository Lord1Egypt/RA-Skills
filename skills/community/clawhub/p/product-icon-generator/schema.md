# Icon Generator Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `product-icon-generator`

x402 availability: not enabled for this product.

## `generate`

Action slug: `generate`

Price: `5` credits

Render a deterministic PNG and store it for 3 days. This creates one file; idempotent retries return the same file with a fresh 15-minute tenant-scoped signed URL.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `background_color` | `string` | no | Canvas color: #RRGGBB, #RRGGBBAA, transparent, or a documented named color. |
| `continue_on_error` | `boolean` | no | Continue after renderer failures only when at least one drawable operation succeeds. Returns fixed, redacted warnings and emits one aggregate operator warning. Structural validation errors always reject the request. |
| `height` | `integer` | no | Output PNG height in pixels, from 1 to 4096. Defaults to 2048; pixel_art_mode permits at most 256. |
| `idempotency_key` | `string` | yes | Required UUID. Reuse it only when retrying this exact generation request. |
| `instructions` | `array` | yes | Ordered drawing operations with at least one drawable operation. save_state and restore_state must be balanced; at most 8192 point pairs are allowed across the request. |
| `pixel_art_mode` | `boolean` | no | Disable anti-aliasing and snap coordinates to integer pixels. Text is not allowed in this mode. |
| `width` | `integer` | no | Output PNG width in pixels, from 1 to 4096. Defaults to 2048; pixel_art_mode permits at most 256. |

Sample parameters:

```json
{
  "background_color": "#FFFFFF",
  "continue_on_error": true,
  "height": 2048,
  "idempotency_key": "example idempotency key",
  "instructions": [
    {
      "anti_alias": true,
      "end_angle": -360000,
      "fill": "example fill",
      "font_family": "example font family",
      "font_size": 1,
      "font_weight": "normal",
      "height": 1,
      "opacity": 0
    }
  ],
  "pixel_art_mode": true,
  "width": 2048
}
```

Generated JSON parameter schema:

```json
{
  "background_color": {
    "default": "#FFFFFF",
    "description": "Canvas color: #RRGGBB, #RRGGBBAA, transparent, or a documented named color.",
    "required": false,
    "type": "string"
  },
  "continue_on_error": {
    "description": "Continue after renderer failures only when at least one drawable operation succeeds. Returns fixed, redacted warnings and emits one aggregate operator warning. Structural validation errors always reject the request.",
    "required": false,
    "type": "boolean"
  },
  "height": {
    "default": 2048,
    "description": "Output PNG height in pixels, from 1 to 4096. Defaults to 2048; pixel_art_mode permits at most 256.",
    "maximum": 4096,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "idempotency_key": {
    "description": "Required UUID. Reuse it only when retrying this exact generation request.",
    "format": "uuid",
    "required": true,
    "type": "string"
  },
  "instructions": {
    "description": "Ordered drawing operations with at least one drawable operation. save_state and restore_state must be balanced; at most 8192 point pairs are allowed across the request.",
    "items": {
      "additionalProperties": false,
      "properties": {
        "anti_alias": {
          "description": "Per-instruction anti-alias override for compatible paint operations.",
          "required": false,
          "type": "boolean"
        },
        "end_angle": {
          "description": "Arc end angle in degrees.",
          "maximum": 360000,
          "minimum": -360000,
          "required": false,
          "type": "number"
        },
        "fill": {
          "description": "Fill color for compatible painted shapes.",
          "maxLength": 64,
          "minLength": 1,
          "required": false,
          "type": "string"
        },
        "font_family": {
          "description": "Installed font family name.",
          "maxLength": 255,
          "minLength": 1,
          "required": false,
          "type": "string"
        },
        "font_size": {
          "description": "Positive text size, at most 4096.",
          "exclusiveMinimum": 0,
          "maximum": 4096,
          "required": false,
          "type": "number"
        },
        "font_weight": {
          "description": "Text font weight.",
          "enum": [
            "normal",
            "bold"
          ],
          "required": false,
          "type": "string"
        },
        "height": {
          "description": "Positive rectangle height, at most 16384.",
          "exclusiveMinimum": 0,
          "maximum": 16384,
          "required": false,
          "type": "number"
        },
        "opacity": {
          "description": "Alpha multiplier for compatible paint operations.",
          "maximum": 1,
          "minimum": 0,
          "required": false,
          "type": "number"
        },
        "path": {
          "description": "SVG path data capped at 8,192 parsed segments; parsed coordinates must be finite and between -16,384 and 16,384.",
          "maxLength": 100000,
          "minLength": 1,
          "required": false,
          "type": "string"
        },
        "points": {
          "description": "Coordinate pairs for line or polygon; at most 2048 pairs per instruction.",
          "items": {
            "items": {
              "maximum": 16384,
              "minimum": -16384,
              "type": "number"
            },
            "maxItems": 2,
            "minItems": 2,
            "type": "array"
          },
          "maxItems": 2048,
          "minItems": 2,
          "required": false,
          "type": "array"
        },
        "radius": {
          "description": "Positive radius for circles, arcs, or rounded rectangles.",
          "exclusiveMinimum": 0,
          "maximum": 16384,
          "required": false,
          "type": "number"
        },
        "radius_x": {
          "description": "Positive horizontal ellipse radius.",
          "exclusiveMinimum": 0,
          "maximum": 16384,
          "required": false,
          "type": "number"
        },
        "radius_y": {
          "description": "Positive vertical ellipse radius.",
          "exclusiveMinimum": 0,
          "maximum": 16384,
          "required": false,
          "type": "number"
        },
        "rotate": {
          "description": "Rotation angle in degrees for rotate.",
          "maximum": 360000,
          "minimum": -360000,
          "required": false,
          "type": "number"
        },
        "scale_x": {
          "description": "Non-zero horizontal scale from -100 to 100.",
          "maximum": 100,
          "minimum": -100,
          "required": false,
          "type": "number"
        },
        "scale_y": {
          "description": "Non-zero vertical scale from -100 to 100.",
          "maximum": 100,
          "minimum": -100,
          "required": false,
          "type": "number"
        },
        "shape_type": {
          "description": "Drawing operation. Each operation accepts only its relevant fields.",
          "enum": [
            "rectangle",
            "rounded_rectangle",
            "circle",
            "ellipse",
            "line",
            "polygon",
            "arc",
            "text",
            "path",
            "save_state",
            "restore_state",
            "translate",
            "rotate",
            "scale"
          ],
          "required": true,
          "type": "string"
        },
        "start_angle": {
          "description": "Arc start angle in degrees.",
          "maximum": 360000,
          "minimum": -360000,
          "required": false,
          "type": "number"
        },
        "stroke": {
          "description": "Stroke color for compatible painted shapes.",
          "maxLength": 64,
          "minLength": 1,
          "required": false,
          "type": "string"
        },
        "stroke_width": {
          "description": "Positive stroke width, at most 4096.",
          "exclusiveMinimum": 0,
          "maximum": 4096,
          "required": false,
          "type": "number"
        },
        "text": {
          "description": "Text content for a text instruction.",
          "maxLength": 10000,
          "minLength": 1,
          "required": false,
          "type": "string"
        },
        "text_align": {
          "description": "Horizontal text alignment.",
          "enum": [
            "left",
            "center",
            "right"
          ],
          "required": false,
          "type": "string"
        },
        "width": {
          "description": "Positive rectangle width, at most 16384.",
          "exclusiveMinimum": 0,
          "maximum": 16384,
          "required": false,
          "type": "number"
        },
        "x": {
          "description": "X coordinate for compatible shapes or transforms.",
          "maximum": 16384,
          "minimum": -16384,
          "required": false,
          "type": "number"
        },
        "y": {
          "description": "Y coordinate for compatible shapes or transforms.",
          "maximum": 16384,
          "minimum": -16384,
          "required": false,
          "type": "number"
        }
      },
      "type": "object"
    },
    "maxItems": 256,
    "minItems": 1,
    "required": true,
    "type": "array"
  },
  "pixel_art_mode": {
    "description": "Disable anti-aliasing and snap coordinates to integer pixels. Text is not allowed in this mode.",
    "required": false,
    "type": "boolean"
  },
  "width": {
    "default": 2048,
    "description": "Output PNG width in pixels, from 1 to 4096. Defaults to 2048; pixel_art_mode permits at most 256.",
    "maximum": 4096,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

# Image Generation Agent Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `image-generation-agent`

x402 availability: not enabled for this product.

## `generate_budget_image`

Action slug: `generate-budget-image`

Price: `8` credits

Create or edit a lower-cost image from a prompt and optional reference images. Use for drafts, previews, and standard 1024px-class outputs.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `aspect_ratio` | `string` | no | Desired output aspect ratio. Default is 1:1. |
| `expiration_days` | `integer` | no | File Manager expiration in days, from 1 to 7. Default is 7. |
| `filename` | `string` | no | Optional output filename base. Extension is inferred from generated image MIME type. |
| `prompt` | `string` | yes | Image generation or edit instruction, 3 to 4000 characters. |
| `reference_images` | `array` | no | Optional reference images for edits or style/subject guidance. Maximum 4. |

Sample parameters:

```json
{
  "aspect_ratio": "1:1",
  "expiration_days": 1,
  "filename": "example filename",
  "prompt": "example prompt",
  "reference_images": [
    {
      "base64_data": "example base64 data",
      "file_id": "example file id",
      "mime_type": "image/png",
      "source_kind": "file_id",
      "url": "https://example.com"
    }
  ]
}
```

Generated JSON parameter schema:

```json
{
  "aspect_ratio": {
    "description": "Desired output aspect ratio. Default is 1:1.",
    "enum": [
      "1:1",
      "2:3",
      "3:2",
      "3:4",
      "4:3",
      "4:5",
      "5:4",
      "9:16",
      "16:9",
      "21:9"
    ],
    "required": false,
    "type": "string"
  },
  "expiration_days": {
    "description": "File Manager expiration in days, from 1 to 7. Default is 7.",
    "required": false,
    "type": "integer"
  },
  "filename": {
    "description": "Optional output filename base. Extension is inferred from generated image MIME type.",
    "required": false,
    "type": "string"
  },
  "prompt": {
    "description": "Image generation or edit instruction, 3 to 4000 characters.",
    "required": true,
    "type": "string"
  },
  "reference_images": {
    "description": "Optional reference images for edits or style/subject guidance. Maximum 4.",
    "items": {
      "properties": {
        "base64_data": {
          "description": "Base64 image bytes when source_kind is base64.",
          "required": false,
          "type": "string"
        },
        "file_id": {
          "description": "AgentPMT File Manager file_id when source_kind is file_id.",
          "required": false,
          "type": "string"
        },
        "mime_type": {
          "description": "Image MIME type for base64 input or explicit validation.",
          "enum": [
            "image/png",
            "image/jpeg",
            "image/webp"
          ],
          "required": false,
          "type": "string"
        },
        "source_kind": {
          "description": "Reference source type.",
          "enum": [
            "file_id",
            "url",
            "base64"
          ],
          "required": true,
          "type": "string"
        },
        "url": {
          "description": "Public HTTPS image URL when source_kind is url.",
          "required": false,
          "type": "string"
        }
      },
      "type": "object"
    },
    "required": false,
    "type": "array"
  }
}
```

## `generate_image_0_5k`

Action slug: `generate-image-0-5k`

Price: `10` credits

Create or edit a high-efficiency 0.5K image from a prompt and optional reference images.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `aspect_ratio` | `string` | no | Desired output aspect ratio. Default is 1:1. |
| `expiration_days` | `integer` | no | File Manager expiration in days, from 1 to 7. Default is 7. |
| `filename` | `string` | no | Optional output filename base. Extension is inferred from generated image MIME type. |
| `prompt` | `string` | yes | Image generation or edit instruction, 3 to 4000 characters. |
| `reference_images` | `array` | no | Optional reference images for edits or style/subject guidance. Maximum 4. |

Sample parameters:

```json
{
  "aspect_ratio": "1:1",
  "expiration_days": 1,
  "filename": "example filename",
  "prompt": "example prompt",
  "reference_images": [
    {
      "base64_data": "example base64 data",
      "file_id": "example file id",
      "mime_type": "image/png",
      "source_kind": "file_id",
      "url": "https://example.com"
    }
  ]
}
```

Generated JSON parameter schema:

```json
{
  "aspect_ratio": {
    "description": "Desired output aspect ratio. Default is 1:1.",
    "enum": [
      "1:1",
      "1:4",
      "1:8",
      "2:3",
      "3:2",
      "3:4",
      "4:1",
      "4:3",
      "4:5",
      "5:4",
      "8:1",
      "9:16",
      "16:9",
      "21:9"
    ],
    "required": false,
    "type": "string"
  },
  "expiration_days": {
    "description": "File Manager expiration in days, from 1 to 7. Default is 7.",
    "required": false,
    "type": "integer"
  },
  "filename": {
    "description": "Optional output filename base. Extension is inferred from generated image MIME type.",
    "required": false,
    "type": "string"
  },
  "prompt": {
    "description": "Image generation or edit instruction, 3 to 4000 characters.",
    "required": true,
    "type": "string"
  },
  "reference_images": {
    "description": "Optional reference images for edits or style/subject guidance. Maximum 4.",
    "items": {
      "properties": {
        "base64_data": {
          "description": "Base64 image bytes when source_kind is base64.",
          "required": false,
          "type": "string"
        },
        "file_id": {
          "description": "AgentPMT File Manager file_id when source_kind is file_id.",
          "required": false,
          "type": "string"
        },
        "mime_type": {
          "description": "Image MIME type for base64 input or explicit validation.",
          "enum": [
            "image/png",
            "image/jpeg",
            "image/webp"
          ],
          "required": false,
          "type": "string"
        },
        "source_kind": {
          "description": "Reference source type.",
          "enum": [
            "file_id",
            "url",
            "base64"
          ],
          "required": true,
          "type": "string"
        },
        "url": {
          "description": "Public HTTPS image URL when source_kind is url.",
          "required": false,
          "type": "string"
        }
      },
      "type": "object"
    },
    "required": false,
    "type": "array"
  }
}
```

## `generate_image_1k`

Action slug: `generate-image-1k`

Price: `15` credits

Create or edit a 1K image from a prompt and optional reference images.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `aspect_ratio` | `string` | no | Desired output aspect ratio. Default is 1:1. |
| `expiration_days` | `integer` | no | File Manager expiration in days, from 1 to 7. Default is 7. |
| `filename` | `string` | no | Optional output filename base. Extension is inferred from generated image MIME type. |
| `prompt` | `string` | yes | Image generation or edit instruction, 3 to 4000 characters. |
| `reference_images` | `array` | no | Optional reference images for edits or style/subject guidance. Maximum 4. |

Sample parameters:

```json
{
  "aspect_ratio": "1:1",
  "expiration_days": 1,
  "filename": "example filename",
  "prompt": "example prompt",
  "reference_images": [
    {
      "base64_data": "example base64 data",
      "file_id": "example file id",
      "mime_type": "image/png",
      "source_kind": "file_id",
      "url": "https://example.com"
    }
  ]
}
```

Generated JSON parameter schema:

```json
{
  "aspect_ratio": {
    "description": "Desired output aspect ratio. Default is 1:1.",
    "enum": [
      "1:1",
      "1:4",
      "1:8",
      "2:3",
      "3:2",
      "3:4",
      "4:1",
      "4:3",
      "4:5",
      "5:4",
      "8:1",
      "9:16",
      "16:9",
      "21:9"
    ],
    "required": false,
    "type": "string"
  },
  "expiration_days": {
    "description": "File Manager expiration in days, from 1 to 7. Default is 7.",
    "required": false,
    "type": "integer"
  },
  "filename": {
    "description": "Optional output filename base. Extension is inferred from generated image MIME type.",
    "required": false,
    "type": "string"
  },
  "prompt": {
    "description": "Image generation or edit instruction, 3 to 4000 characters.",
    "required": true,
    "type": "string"
  },
  "reference_images": {
    "description": "Optional reference images for edits or style/subject guidance. Maximum 4.",
    "items": {
      "properties": {
        "base64_data": {
          "description": "Base64 image bytes when source_kind is base64.",
          "required": false,
          "type": "string"
        },
        "file_id": {
          "description": "AgentPMT File Manager file_id when source_kind is file_id.",
          "required": false,
          "type": "string"
        },
        "mime_type": {
          "description": "Image MIME type for base64 input or explicit validation.",
          "enum": [
            "image/png",
            "image/jpeg",
            "image/webp"
          ],
          "required": false,
          "type": "string"
        },
        "source_kind": {
          "description": "Reference source type.",
          "enum": [
            "file_id",
            "url",
            "base64"
          ],
          "required": true,
          "type": "string"
        },
        "url": {
          "description": "Public HTTPS image URL when source_kind is url.",
          "required": false,
          "type": "string"
        }
      },
      "type": "object"
    },
    "required": false,
    "type": "array"
  }
}
```

## `generate_image_2k`

Action slug: `generate-image-2k`

Price: `25` credits

Create or edit a 2K image from a prompt and optional reference images.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `aspect_ratio` | `string` | no | Desired output aspect ratio. Default is 1:1. |
| `expiration_days` | `integer` | no | File Manager expiration in days, from 1 to 7. Default is 7. |
| `filename` | `string` | no | Optional output filename base. Extension is inferred from generated image MIME type. |
| `prompt` | `string` | yes | Image generation or edit instruction, 3 to 4000 characters. |
| `reference_images` | `array` | no | Optional reference images for edits or style/subject guidance. Maximum 4. |

Sample parameters:

```json
{
  "aspect_ratio": "1:1",
  "expiration_days": 1,
  "filename": "example filename",
  "prompt": "example prompt",
  "reference_images": [
    {
      "base64_data": "example base64 data",
      "file_id": "example file id",
      "mime_type": "image/png",
      "source_kind": "file_id",
      "url": "https://example.com"
    }
  ]
}
```

Generated JSON parameter schema:

```json
{
  "aspect_ratio": {
    "description": "Desired output aspect ratio. Default is 1:1.",
    "enum": [
      "1:1",
      "1:4",
      "1:8",
      "2:3",
      "3:2",
      "3:4",
      "4:1",
      "4:3",
      "4:5",
      "5:4",
      "8:1",
      "9:16",
      "16:9",
      "21:9"
    ],
    "required": false,
    "type": "string"
  },
  "expiration_days": {
    "description": "File Manager expiration in days, from 1 to 7. Default is 7.",
    "required": false,
    "type": "integer"
  },
  "filename": {
    "description": "Optional output filename base. Extension is inferred from generated image MIME type.",
    "required": false,
    "type": "string"
  },
  "prompt": {
    "description": "Image generation or edit instruction, 3 to 4000 characters.",
    "required": true,
    "type": "string"
  },
  "reference_images": {
    "description": "Optional reference images for edits or style/subject guidance. Maximum 4.",
    "items": {
      "properties": {
        "base64_data": {
          "description": "Base64 image bytes when source_kind is base64.",
          "required": false,
          "type": "string"
        },
        "file_id": {
          "description": "AgentPMT File Manager file_id when source_kind is file_id.",
          "required": false,
          "type": "string"
        },
        "mime_type": {
          "description": "Image MIME type for base64 input or explicit validation.",
          "enum": [
            "image/png",
            "image/jpeg",
            "image/webp"
          ],
          "required": false,
          "type": "string"
        },
        "source_kind": {
          "description": "Reference source type.",
          "enum": [
            "file_id",
            "url",
            "base64"
          ],
          "required": true,
          "type": "string"
        },
        "url": {
          "description": "Public HTTPS image URL when source_kind is url.",
          "required": false,
          "type": "string"
        }
      },
      "type": "object"
    },
    "required": false,
    "type": "array"
  }
}
```

## `generate_image_4k`

Action slug: `generate-image-4k`

Price: `40` credits

Create or edit a 4K image from a prompt and optional reference images.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `aspect_ratio` | `string` | no | Desired output aspect ratio. Default is 1:1. |
| `expiration_days` | `integer` | no | File Manager expiration in days, from 1 to 7. Default is 7. |
| `filename` | `string` | no | Optional output filename base. Extension is inferred from generated image MIME type. |
| `prompt` | `string` | yes | Image generation or edit instruction, 3 to 4000 characters. |
| `reference_images` | `array` | no | Optional reference images for edits or style/subject guidance. Maximum 4. |

Sample parameters:

```json
{
  "aspect_ratio": "1:1",
  "expiration_days": 1,
  "filename": "example filename",
  "prompt": "example prompt",
  "reference_images": [
    {
      "base64_data": "example base64 data",
      "file_id": "example file id",
      "mime_type": "image/png",
      "source_kind": "file_id",
      "url": "https://example.com"
    }
  ]
}
```

Generated JSON parameter schema:

```json
{
  "aspect_ratio": {
    "description": "Desired output aspect ratio. Default is 1:1.",
    "enum": [
      "1:1",
      "1:4",
      "1:8",
      "2:3",
      "3:2",
      "3:4",
      "4:1",
      "4:3",
      "4:5",
      "5:4",
      "8:1",
      "9:16",
      "16:9",
      "21:9"
    ],
    "required": false,
    "type": "string"
  },
  "expiration_days": {
    "description": "File Manager expiration in days, from 1 to 7. Default is 7.",
    "required": false,
    "type": "integer"
  },
  "filename": {
    "description": "Optional output filename base. Extension is inferred from generated image MIME type.",
    "required": false,
    "type": "string"
  },
  "prompt": {
    "description": "Image generation or edit instruction, 3 to 4000 characters.",
    "required": true,
    "type": "string"
  },
  "reference_images": {
    "description": "Optional reference images for edits or style/subject guidance. Maximum 4.",
    "items": {
      "properties": {
        "base64_data": {
          "description": "Base64 image bytes when source_kind is base64.",
          "required": false,
          "type": "string"
        },
        "file_id": {
          "description": "AgentPMT File Manager file_id when source_kind is file_id.",
          "required": false,
          "type": "string"
        },
        "mime_type": {
          "description": "Image MIME type for base64 input or explicit validation.",
          "enum": [
            "image/png",
            "image/jpeg",
            "image/webp"
          ],
          "required": false,
          "type": "string"
        },
        "source_kind": {
          "description": "Reference source type.",
          "enum": [
            "file_id",
            "url",
            "base64"
          ],
          "required": true,
          "type": "string"
        },
        "url": {
          "description": "Public HTTPS image URL when source_kind is url.",
          "required": false,
          "type": "string"
        }
      },
      "type": "object"
    },
    "required": false,
    "type": "array"
  }
}
```

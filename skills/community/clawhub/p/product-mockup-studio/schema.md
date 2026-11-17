# Product Mockup Studio Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `product-mockup-studio`

x402 availability: not enabled for this product.

## `animate_product_mockup`

Action slug: `animate-product-mockup`

Price: `10` credits

Turn an approved product still into a short ElevenLabs MP4 product clip.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `aspect_ratio` | `string` | no | Video aspect ratio. Defaults to the still's orientation: 9:16 for a portrait still, otherwise 16:9. A still that does not match is center-cropped so the clip has no black bars. |
| `duration_seconds` | `integer` | no | Video length in seconds. Default 6. |
| `end_frame_file_id` | `string` | no | Optional File Manager image to use as the final frame. |
| `generate_audio` | `boolean` | no | Generate native sound with the clip. Default false. |
| `motion_preset` | `string` | no | Camera or product motion preset. |
| `motion_prompt` | `string` | no | Optional custom motion, camera, lighting, and sound direction. |
| `negative_prompt` | `string` | no | Optional description of motion or visual artifacts to avoid. |
| `render_mode` | `string` | no | preview uses the faster model; final uses the quality model. |
| `resolution` | `string` | no | Video resolution. Default 1080p. |
| `seed` | `integer` | no | Optional seed for similar reruns. |
| `source_file_id` | `string` | no | File Manager image file_id. Provide this or source_task_id. |
| `source_task_id` | `string` | no | Completed image task_id. Provide this or source_file_id. |

Sample parameters:

```json
{
  "aspect_ratio": "16:9",
  "duration_seconds": 4,
  "end_frame_file_id": "example end frame file id",
  "generate_audio": true,
  "motion_preset": "slow_push_in",
  "motion_prompt": "example motion prompt",
  "negative_prompt": "example negative prompt",
  "render_mode": "preview"
}
```

Generated JSON parameter schema:

```json
{
  "aspect_ratio": {
    "description": "Video aspect ratio. Defaults to the still's orientation: 9:16 for a portrait still, otherwise 16:9. A still that does not match is center-cropped so the clip has no black bars.",
    "enum": [
      "16:9",
      "9:16"
    ],
    "required": false,
    "type": "string"
  },
  "duration_seconds": {
    "description": "Video length in seconds. Default 6.",
    "enum": [
      4,
      6,
      8
    ],
    "required": false,
    "type": "integer"
  },
  "end_frame_file_id": {
    "description": "Optional File Manager image to use as the final frame.",
    "required": false,
    "type": "string"
  },
  "generate_audio": {
    "description": "Generate native sound with the clip. Default false.",
    "required": false,
    "type": "boolean"
  },
  "motion_preset": {
    "description": "Camera or product motion preset.",
    "enum": [
      "slow_push_in",
      "product_orbit",
      "turntable",
      "light_sweep",
      "floating_product",
      "lifestyle_motion",
      "custom"
    ],
    "required": false,
    "type": "string"
  },
  "motion_prompt": {
    "description": "Optional custom motion, camera, lighting, and sound direction.",
    "maxLength": 2000,
    "required": false,
    "type": "string"
  },
  "negative_prompt": {
    "description": "Optional description of motion or visual artifacts to avoid.",
    "maxLength": 1000,
    "required": false,
    "type": "string"
  },
  "render_mode": {
    "description": "preview uses the faster model; final uses the quality model.",
    "enum": [
      "preview",
      "final"
    ],
    "required": false,
    "type": "string"
  },
  "resolution": {
    "description": "Video resolution. Default 1080p.",
    "enum": [
      "720p",
      "1080p",
      "4K"
    ],
    "required": false,
    "type": "string"
  },
  "seed": {
    "description": "Optional seed for similar reruns.",
    "maximum": 4294967295,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "source_file_id": {
    "description": "File Manager image file_id. Provide this or source_task_id.",
    "required": false,
    "type": "string"
  },
  "source_task_id": {
    "description": "Completed image task_id. Provide this or source_file_id.",
    "required": false,
    "type": "string"
  }
}
```

## `create_product_mockup`

Action slug: `create-product-mockup`

Price: `25` credits

Create one product-focused PNG mockup from File Manager product photos and a scene brief.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `aspect_ratio` | `string` | no | Output image aspect ratio. Default 1:1. |
| `brand_constraints` | `object` | no | Optional brand-fidelity requirements that the generated mockup should preserve. |
| `camera_view` | `string` | no | Preferred camera angle. |
| `image_provider` | `string` | no | Image backend. auto prefers ElevenLabs and permits a safe Nano Banana fallback. |
| `mask_file_id` | `string` | no | Optional File Manager image mask for localized edits on the ElevenLabs final route. |
| `mockup_style` | `string` | no | Product presentation preset. |
| `product_description` | `string` | no | Optional factual description of the product, materials, scale, and important features. |
| `product_file_ids` | `array` | yes | One to five File Manager images showing the product or packaging. |
| `render_mode` | `string` | no | draft favors speed; final favors fidelity and resolution. |
| `scene_prompt` | `string` | yes | Describe the desired setting, lighting, composition, and marketing result. |
| `style_reference_file_ids` | `array` | no | Up to three File Manager images used only for visual style guidance. |

Sample parameters:

```json
{
  "aspect_ratio": "1:1",
  "brand_constraints": {
    "brand_colors": [
      "example brand color"
    ],
    "exact_text": [
      "example exact text"
    ],
    "must_preserve": [
      "example must preserve"
    ],
    "prohibited_elements": [
      "example prohibited element"
    ]
  },
  "camera_view": "front",
  "image_provider": "auto",
  "mask_file_id": "example mask file id",
  "mockup_style": "studio_hero",
  "product_description": "example product description",
  "product_file_ids": [
    "example product file id"
  ]
}
```

Generated JSON parameter schema:

```json
{
  "aspect_ratio": {
    "description": "Output image aspect ratio. Default 1:1.",
    "enum": [
      "1:1",
      "3:2",
      "2:3",
      "4:5",
      "5:4",
      "3:4",
      "4:3",
      "16:9",
      "9:16"
    ],
    "required": false,
    "type": "string"
  },
  "brand_constraints": {
    "description": "Optional brand-fidelity requirements that the generated mockup should preserve.",
    "properties": {
      "brand_colors": {
        "description": "Brand colors as names or hex values.",
        "items": {
          "description": "Brand color.",
          "type": "string"
        },
        "maxItems": 8,
        "required": false,
        "type": "array"
      },
      "exact_text": {
        "description": "Visible product or packaging text that should remain exact; review the result.",
        "items": {
          "description": "Exact text.",
          "type": "string"
        },
        "maxItems": 20,
        "required": false,
        "type": "array"
      },
      "must_preserve": {
        "description": "Product details that must remain visually consistent.",
        "items": {
          "description": "Preservation requirement.",
          "type": "string"
        },
        "maxItems": 20,
        "required": false,
        "type": "array"
      },
      "prohibited_elements": {
        "description": "Elements that must not appear in the output.",
        "items": {
          "description": "Prohibited element.",
          "type": "string"
        },
        "maxItems": 20,
        "required": false,
        "type": "array"
      }
    },
    "required": false,
    "type": "object"
  },
  "camera_view": {
    "description": "Preferred camera angle.",
    "enum": [
      "front",
      "three_quarter",
      "side",
      "top_down",
      "close_up",
      "custom"
    ],
    "required": false,
    "type": "string"
  },
  "image_provider": {
    "description": "Image backend. auto prefers ElevenLabs and permits a safe Nano Banana fallback.",
    "enum": [
      "auto",
      "elevenlabs",
      "nano_banana"
    ],
    "required": false,
    "type": "string"
  },
  "mask_file_id": {
    "description": "Optional File Manager image mask for localized edits on the ElevenLabs final route.",
    "required": false,
    "type": "string"
  },
  "mockup_style": {
    "description": "Product presentation preset.",
    "enum": [
      "studio_hero",
      "lifestyle",
      "in_hand",
      "flat_lay",
      "packaging",
      "ecommerce",
      "custom"
    ],
    "required": false,
    "type": "string"
  },
  "product_description": {
    "description": "Optional factual description of the product, materials, scale, and important features.",
    "maxLength": 1500,
    "required": false,
    "type": "string"
  },
  "product_file_ids": {
    "description": "One to five File Manager images showing the product or packaging.",
    "items": {
      "description": "File Manager image file_id.",
      "type": "string"
    },
    "maxItems": 5,
    "minItems": 1,
    "required": true,
    "type": "array"
  },
  "render_mode": {
    "description": "draft favors speed; final favors fidelity and resolution.",
    "enum": [
      "draft",
      "final"
    ],
    "required": false,
    "type": "string"
  },
  "scene_prompt": {
    "description": "Describe the desired setting, lighting, composition, and marketing result.",
    "maxLength": 3000,
    "minLength": 3,
    "required": true,
    "type": "string"
  },
  "style_reference_file_ids": {
    "description": "Up to three File Manager images used only for visual style guidance.",
    "items": {
      "description": "File Manager image file_id.",
      "type": "string"
    },
    "maxItems": 3,
    "required": false,
    "type": "array"
  }
}
```

## `get_mockup_job`

Action slug: `get-mockup-job`

Price: `1` credits

Check one mockup job and import a completed PNG or MP4 into File Manager.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `task_id` | `string` | yes | Task ID returned by a create, refine, or animate action. |

Sample parameters:

```json
{
  "task_id": "example task id"
}
```

Generated JSON parameter schema:

```json
{
  "task_id": {
    "description": "Task ID returned by a create, refine, or animate action.",
    "required": true,
    "type": "string"
  }
}
```

## `list_mockup_jobs`

Action slug: `list-mockup-jobs`

Price: `1` credits

List budget-scoped product mockup jobs without exposing unrelated provider generations.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | `string` | no | Opaque cursor returned by the previous page. |
| `media_kind` | `string` | no | Optional media filter. |
| `page_size` | `integer` | no | Results per page, 1 to 100. Default 30. |
| `status` | `string` | no | Optional job status filter. |

Sample parameters:

```json
{
  "cursor": "example cursor",
  "media_kind": "image",
  "page_size": 1,
  "status": "pending"
}
```

Generated JSON parameter schema:

```json
{
  "cursor": {
    "description": "Opaque cursor returned by the previous page.",
    "required": false,
    "type": "string"
  },
  "media_kind": {
    "description": "Optional media filter.",
    "enum": [
      "image",
      "video"
    ],
    "required": false,
    "type": "string"
  },
  "page_size": {
    "description": "Results per page, 1 to 100. Default 30.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "status": {
    "description": "Optional job status filter.",
    "enum": [
      "pending",
      "generating",
      "completed",
      "failed"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `refine_product_mockup`

Action slug: `refine-product-mockup`

Price: `25` credits

Revise a completed mockup while preserving its product identity and approved composition.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `aspect_ratio` | `string` | no | Output image aspect ratio. Default 1:1. |
| `brand_constraints` | `object` | no | Optional brand-fidelity requirements that the generated mockup should preserve. |
| `image_provider` | `string` | no | Image backend. auto prefers ElevenLabs and permits a safe Nano Banana fallback. |
| `instruction` | `string` | yes | Describe only the changes to make and what must remain unchanged. |
| `mask_file_id` | `string` | no | Optional File Manager image mask for localized edits on the ElevenLabs final route. |
| `render_mode` | `string` | no | draft favors speed; final favors fidelity and resolution. |
| `source_task_id` | `string` | yes | Completed image task_id returned by this tool. |

Sample parameters:

```json
{
  "aspect_ratio": "1:1",
  "brand_constraints": {
    "brand_colors": [
      "example brand color"
    ],
    "exact_text": [
      "example exact text"
    ],
    "must_preserve": [
      "example must preserve"
    ],
    "prohibited_elements": [
      "example prohibited element"
    ]
  },
  "image_provider": "auto",
  "instruction": "example instruction",
  "mask_file_id": "example mask file id",
  "render_mode": "draft",
  "source_task_id": "example source task id"
}
```

Generated JSON parameter schema:

```json
{
  "aspect_ratio": {
    "description": "Output image aspect ratio. Default 1:1.",
    "enum": [
      "1:1",
      "3:2",
      "2:3",
      "4:5",
      "5:4",
      "3:4",
      "4:3",
      "16:9",
      "9:16"
    ],
    "required": false,
    "type": "string"
  },
  "brand_constraints": {
    "description": "Optional brand-fidelity requirements that the generated mockup should preserve.",
    "properties": {
      "brand_colors": {
        "description": "Brand colors as names or hex values.",
        "items": {
          "description": "Brand color.",
          "type": "string"
        },
        "maxItems": 8,
        "required": false,
        "type": "array"
      },
      "exact_text": {
        "description": "Visible product or packaging text that should remain exact; review the result.",
        "items": {
          "description": "Exact text.",
          "type": "string"
        },
        "maxItems": 20,
        "required": false,
        "type": "array"
      },
      "must_preserve": {
        "description": "Product details that must remain visually consistent.",
        "items": {
          "description": "Preservation requirement.",
          "type": "string"
        },
        "maxItems": 20,
        "required": false,
        "type": "array"
      },
      "prohibited_elements": {
        "description": "Elements that must not appear in the output.",
        "items": {
          "description": "Prohibited element.",
          "type": "string"
        },
        "maxItems": 20,
        "required": false,
        "type": "array"
      }
    },
    "required": false,
    "type": "object"
  },
  "image_provider": {
    "description": "Image backend. auto prefers ElevenLabs and permits a safe Nano Banana fallback.",
    "enum": [
      "auto",
      "elevenlabs",
      "nano_banana"
    ],
    "required": false,
    "type": "string"
  },
  "instruction": {
    "description": "Describe only the changes to make and what must remain unchanged.",
    "maxLength": 3000,
    "minLength": 3,
    "required": true,
    "type": "string"
  },
  "mask_file_id": {
    "description": "Optional File Manager image mask for localized edits on the ElevenLabs final route.",
    "required": false,
    "type": "string"
  },
  "render_mode": {
    "description": "draft favors speed; final favors fidelity and resolution.",
    "enum": [
      "draft",
      "final"
    ],
    "required": false,
    "type": "string"
  },
  "source_task_id": {
    "description": "Completed image task_id returned by this tool.",
    "required": true,
    "type": "string"
  }
}
```

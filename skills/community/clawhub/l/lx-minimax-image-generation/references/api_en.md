# MiniMax Image Generation API

## Overview

MiniMax provides two image generation APIs:
- **Text-to-Image (T2I)**: Generate images from text prompts
- **Image-to-Image (I2I)**: Generate new images based on a reference image

Base URL: `https://api.minimaxi.com/v1/image_generation`

Authentication: `Authorization: Bearer {API_KEY}`

---

## Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | `image-01` or `image-01-live` |
| `prompt` | string | Image description, max 1500 characters |
| `aspect_ratio` | string | Aspect ratio, default `1:1` |
| `response_format` | string | `url` (default) or `base64` |
| `n` | int | Number of images to generate, 1-9, default 1 |
| `prompt_optimizer` | bool | Enable auto prompt optimization, default false |
| `aigc_watermark` | bool | Add AIGC watermark, default false |

### Aspect Ratio Options

| Value | Resolution |
|-------|------------|
| `1:1` | 1024x1024 |
| `16:9` | 1280x720 |
| `4:3` | 1152x864 |
| `3:2` | 1248x832 |
| `2:3` | 832x1248 |
| `3:4` | 864x1152 |
| `9:16` | 720x1280 |
| `21:9` | 1344x576 (image-01 only) |

### Model Differences

**image-01**
- Supports all aspect ratios
- Supports custom width/height [512, 2048]

**image-01-live**
- Supports artistic styles (style parameter)
- Available styles: `Comic`, `Energetic`, `Medieval`, `Watercolor`

---

## T2I Request Example

```json
{
  "model": "image-01",
  "prompt": "A man in a white t-shirt, full-body, standing front view, outdoors, Venice Beach sign in background",
  "aspect_ratio": "16:9",
  "response_format": "url",
  "n": 3,
  "prompt_optimizer": true
}
```

## T2I Response

```json
{
  "data": {
    "image_urls": ["https://xxx.bj.bcebos.com/xxx.jpg"]
  },
  "metadata": {
    "success_count": 3,
    "failed_count": 0
  },
  "id": "03ff3cd0820949eb8a410056b5f21d38",
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

> ⚠️ Image URLs expire in 24 hours

---

## I2I Request Example

Image-to-Image requires the `subject_reference` parameter:

```json
{
  "model": "image-01",
  "prompt": "Wearing traditional Chinese clothing, standing on the Great Wall",
  "aspect_ratio": "3:4",
  "subject_reference": [
    {
      "type": "character",
      "image_file": "https://example.com/reference.jpg"
    }
  ],
  "n": 2
}
```

### subject_reference

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Currently only supports `character` |
| `image_file` | string | Reference image URL or Base64 Data URL |

**Image Requirements:**
- Format: JPG, JPEG, PNG
- Size: Under 10MB
- Recommendation: Single person, frontal photo works best

---

## Style for image-01-live

When using `image-01-live` model, add the style parameter:

```json
{
  "model": "image-01-live",
  "prompt": "Vacationing at the beach",
  "style": {
    "style_type": "Watercolor",
    "style_weight": 0.8
  }
}
```

| style_type | Description |
|------------|-------------|
| `Comic` | Comic/ Manga style |
| `Energetic` | Energetic/ Youthful |
| `Medieval` | Medieval style |
| `Watercolor` | Watercolor |

style_weight range: (0, 1], default 0.8

---

## Error Codes

| status_code | Description |
|-------------|-------------|
| 0 | Success |
| 1002 | Rate limit hit, please retry |
| 1004 | Authentication failed |
| 1008 | Insufficient balance |
| 1026 | Content involves sensitive material |
| 2013 | Invalid parameters |
| 2049 | Invalid API Key |

---

## Script Usage

```bash
# Text-to-Image
python3 image_gen.py -p "A cat playing on the grass" -r "16:9" -n 2

# Image-to-Image (via Python)
from image_gen import generate_image

result = generate_image(
    prompt="Wearing a suit, sitting in an office",
    model="image-01",
    aspect_ratio="3:4",
    subject_reference=[
        {
            "type": "character",
            "image_file": "https://example.com/photo.jpg"
        }
    ],
    n=1
)

# Output includes local save paths
print(result["_local_paths"])
```

---

## Note on URLs

Image URLs expire in 24 hours. Download and save promptly.

The script auto-downloads URL-format images to `/home/ubuntu/.openclaw/workspace/images/` directory.

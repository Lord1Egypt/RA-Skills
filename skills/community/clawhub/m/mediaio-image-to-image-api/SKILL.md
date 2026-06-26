---
name: mediaio-image-to-image-api
description: "Transform existing images into new ones using AI via Media.io OpenAPI. Apply style transfers, artistic filters, and creative transformations with models like Seedream, Nano Banana, and more."
metadata: {"mediaio":{"emoji":"🎨","requires":{"env":["API_KEY"]}},"publisher":"Community Maintainer","source":"https://platform.media.io/docs/","homepage":"https://developer.media.io/"}
---

# MediaIO Image to Image API Skill

## Overview
This skill provides **Image-to-Image** transformation capabilities through the Media.io OpenAPI. Transform your existing images into new creations using state-of-the-art AI models for style transfers, artistic filters, and creative transformations.

## Trigger Keywords
Use this skill when you hear:
- "image to image", "image-to-image API", "transform image"
- "style transfer", "image transformation", "edit image with AI"
- "apply artistic filter to image", "image remixing"

## Supported Models
The Image-to-Image API supports multiple models:
- **Seedream 4.0** (`i2i-seedream-v4-0`) - High aesthetic quality, 4K support, character consistency
- **Nano Banana Pro** (`i2i-banana-2`) - Advanced reasoning, multi-image fusion
- **Nano Banana** (`i2i-banana`) - Fast and efficient generation
- **Media 2.0** (`i2i-media-2.0`) - Proprietary native model

## Requirements

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `API_KEY` | **Yes** | Media.io OpenAPI key, sent as `X-API-KEY` header. Apply at <https://developer.media.io/>. |

## API Details

### Image-to-Image Transformation

#### Seedream 4.0 (Recommended for Quality)

- **API Name**: `Seedream 4.0`
- **Model Code**: `i2i-seedream-v4-0`
- **Endpoint**: `POST https://openapi.media.io/generation/seedream/i2i-seedream-v4-0`
- **Description**: A versatile powerhouse supporting 4K generation and advanced editing.

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | **Yes** | Text description for transformation |
| `image` | string | **Yes** | Reference image URL for transformation |
| `ratio` | string | No | Image aspect ratio |
| `strength` | string | No | How strongly to follow the reference image (0.0-1.0) |

#### Common Response Structure

```json
{
  "code": 0,
  "msg": "",
  "data": {
    "task_id": "..."
  },
  "trace_id": "..."
}
```

## Quick Start

### 1) Install Dependency
```bash
pip install requests
```

### 2) Initialize Skill
```python
import os
from scripts.skill_router import Skill

skill = Skill('scripts/c_api_doc_detail.json')
api_key = os.getenv('API_KEY', '')
if not api_key:
    raise RuntimeError('API_KEY is not set')
```

### 3) Configure Environment Variable API_KEY

**Windows PowerShell**:
```powershell
$env:API_KEY="your-api-key"
```

**macOS / Linux (bash/zsh)**:
```bash
export API_KEY="your-api-key"
```

## Usage Examples (Python)

### Style Transfer
```python
import os
from scripts.skill_router import Skill

skill = Skill('scripts/c_api_doc_detail.json')
api_key = os.getenv('API_KEY', '')
if not api_key:
    raise RuntimeError('API_KEY is not set')

result = skill.invoke(
    'Seedream 4.0',
    {
        'prompt': 'transform this photo into an oil painting in the style of Van Gogh, vibrant colors, visible brushstrokes',
        'image': 'https://example.com/input-image.jpg'
    },
    api_key=api_key
)
print(result)  # Returns task_id when code=0
```

### Artistic Enhancement
```python
import os
from scripts.skill_router import Skill

skill = Skill('scripts/c_api_doc_detail.json')
api_key = os.getenv('API_KEY', '')
if not api_key:
    raise RuntimeError('API_KEY is not set')

result = skill.invoke(
    'Nano Banana Pro',
    {
        'prompt': 'enhance this portrait with dramatic cinematic lighting, professional photography quality, shallow depth of field',
        'image': 'https://example.com/portrait.jpg'
    },
    api_key=api_key
)
print(result)
```

### Creative Transformation
```python
import os
from scripts.skill_router import Skill

skill = Skill('scripts/c_api_doc_detail.json')
api_key = os.getenv('API_KEY', '')
if not api_key:
    raise RuntimeError('API_KEY is not set')

result = skill.invoke(
    'Seedream 4.0',
    {
        'prompt': 'convert this landscape into a cyberpunk cityscape at night, neon lights, rain reflections, futuristic atmosphere',
        'image': 'https://example.com/landscape.jpg',
        'ratio': '16:9'
    },
    api_key=api_key
)
print(result)
```

### Image Remixing
```python
import os
from scripts.skill_router import Skill

skill = Skill('scripts/c_api_doc_detail.json')
api_key = os.getenv('API_KEY', '')
if not api_key:
    raise RuntimeError('API_KEY is not set')

result = skill.invoke(
    'Nano Banana',
    {
        'prompt': 'reimagine this image as a watercolor painting, soft edges, pastel colors, artistic interpretation',
        'image': 'https://example.com/original.jpg',
        'strength': '0.7'
    },
    api_key=api_key
)
print(result)
```

### Query Task Result
```python
import os
import time
from scripts.skill_router import Skill

skill = Skill('scripts/c_api_doc_detail.json')
api_key = os.getenv('API_KEY', '')
if not api_key:
    raise RuntimeError('API_KEY is not set')

task_id = 'your-task-id'

for _ in range(24):
    r = skill.invoke('Task Result', {'task_id': task_id}, api_key=api_key)
    print(r)
    status = (r.get('data') or {}).get('status')
    if status in ('completed', 'failed', 'succeeded'):
        break
    time.sleep(5)
```

#### Task Status Reference
- `waiting`: queued
- `processing`: running
- `completed`: completed successfully
- `failed`: failed
- `timeout`: timed out

## Model Comparison

| Model | Best For | Resolution | Speed |
|-------|----------|------------|-------|
| Seedream 4.0 | High quality, artistic | Up to 4K | Medium |
| Nano Banana Pro | Advanced reasoning, fusion | Up to 4K | Medium |
| Nano Banana | Fast transformations | Up to 4K | Fast |
| Media 2.0 | Diverse styles | Standard | Fast |

## Common Transformations

### Style Transfers
- Oil painting, watercolor, pencil sketch
- Anime/manga style
- Pixel art, 8-bit style
- Cinematic movie still

### Enhancements
- Professional photography quality
- Dramatic lighting
- Color grading
- Depth of field effects

### Creative Transformations
- Season changes (summer to winter)
- Time of day changes
- Architecture style conversion
- Fantasy/sci-fi conversion

## Error Handling

| Error Code | Description |
|------------|-------------|
| `374004` | Not authenticated. Apply for an APP KEY at https://developer.media.io/ |
| `490505` | Insufficient credits. Recharge before invoking generation APIs |

## Tips for Better Results

1. **Use High-Quality Input**: Better source images yield better transformations
2. **Be Specific in Prompts**: Describe both the transformation and desired outcome
3. **Adjust Strength**: Use lower strength (0.3-0.5) to preserve more of the original
4. **Match Aspect Ratios**: Keep output ratio similar to input for best results

## External Resources
- API documentation: https://platform.media.io/docs/
- Product overview: https://developer.media.io/
- Credit purchase: https://developer.media.io/pricing.html

## Related Files
- scripts/skill_router.py: core routing logic
- scripts/c_api_doc_detail.json: API definitions

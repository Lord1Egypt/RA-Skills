---
name: mediaio-text-to-image-api
description: "Generate AI images from text descriptions using Media.io OpenAPI. Provide a text prompt and receive a high-quality AI-generated image. Supports multiple models including Imagen 4, Seedream, and more."
metadata: {"mediaio":{"emoji":"🎨","requires":{"env":["API_KEY"]}},"publisher":"Community Maintainer","source":"https://platform.media.io/docs/","homepage":"https://developer.media.io/"}
---

# MediaIO Text to Image API Skill

## Overview
This skill provides **Text-to-Image** generation capabilities through the Media.io OpenAPI. Transform your text descriptions into high-quality AI-generated images using state-of-the-art models.

## Trigger Keywords
Use this skill when you hear:
- "text to image", "text-to-image API", "generate image from text"
- "create image from text", "text to image generation"
- "AI image from prompt", "generate image with text"

## Supported Models
The Text-to-Image API supports multiple models:
- **Imagen 4** (`t2i-imagen-4`) - Google's photorealistic image generation
- **Soul Character** (`t2i-soul-character`) - Character generation

## Requirements

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `API_KEY` | **Yes** | Media.io OpenAPI key, sent as `X-API-KEY` header. Apply at <https://developer.media.io/>. |

## API Details

### Text-to-Image Generation

#### Imagen 4 (Recommended)

- **API Name**: `Imagen 4`
- **Model Code**: `t2i-imagen-4`
- **Endpoint**: `POST https://openapi.media.io/generation/imagen/t2i-imagen-4`
- **Description**: Sets a new standard for photorealism and text rendering accuracy.

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | **Yes** | Text description for image generation |
| `ratio` | string | No | Image aspect ratio (e.g., "1:1", "16:9", "9:16") |
| `counts` | string | No | Number of images to generate (default: "1") |

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

### Basic Text-to-Image Generation
```python
import os
from scripts.skill_router import Skill

skill = Skill('scripts/c_api_doc_detail.json')
api_key = os.getenv('API_KEY', '')
if not api_key:
    raise RuntimeError('API_KEY is not set')

result = skill.invoke(
    'Imagen 4',
    {
        'prompt': 'a serene mountain landscape at sunset, photorealistic, golden hour lighting',
        'ratio': '16:9',
        'counts': '1'
    },
    api_key=api_key
)
print(result)  # Returns task_id when code=0
```

### Artistic Style Generation
```python
import os
from scripts.skill_router import Skill

skill = Skill('scripts/c_api_doc_detail.json')
api_key = os.getenv('API_KEY', '')
if not api_key:
    raise RuntimeError('API_KEY is not set')

result = skill.invoke(
    'Imagen 4',
    {
        'prompt': 'an oil painting of a bustling Parisian cafe in the style of Impressionism, warm colors, visible brushstrokes',
        'ratio': '4:3'
    },
    api_key=api_key
)
print(result)
```

### Character Generation
```python
import os
from scripts.skill_router import Skill

skill = Skill('scripts/c_api_doc_detail.json')
api_key = os.getenv('API_KEY', '')
if not api_key:
    raise RuntimeError('API_KEY is not set')

result = skill.invoke(
    'Soul Character',
    {
        'prompt': 'a friendly fantasy wizard with a long white beard and blue robes, detailed character design',
        'ratio': '1:1'
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

## Supported Aspect Ratios

| Ratio | Dimensions | Use Case |
|-------|------------|----------|
| `1:1` | Square | Profile pictures, thumbnails |
| `16:9` | Landscape | Wallpapers, banners |
| `9:16` | Portrait | Mobile wallpapers, stories |
| `4:3` | Standard | Traditional photos |
| `3:4` | Portrait | Traditional portraits |

## Error Handling

| Error Code | Description |
|------------|-------------|
| `374004` | Not authenticated. Apply for an APP KEY at https://developer.media.io/ |
| `490505` | Insufficient credits. Recharge before invoking generation APIs |

## Tips for Better Results

1. **Be Specific**: Include details about lighting, style, and mood
2. **Use Descriptive Adjectives**: "photorealistic", "cinematic", "vibrant"
3. **Specify Art Styles**: "in the style of Van Gogh", "anime style", "watercolor"
4. **Include Technical Details**: "8K", "HDR", "depth of field"

## External Resources
- API documentation: https://platform.media.io/docs/
- Product overview: https://developer.media.io/
- Credit purchase: https://developer.media.io/pricing.html

## Related Files
- scripts/skill_router.py: core routing logic
- scripts/c_api_doc_detail.json: API definitions

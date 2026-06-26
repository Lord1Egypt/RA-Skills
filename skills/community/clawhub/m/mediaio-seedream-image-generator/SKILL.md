---
name: mediaio-seedream-image-generator
description: "Generate AI images using ByteDance Seedream via Media.io OpenAPI. Delivers high aesthetic quality and detailed rendering for text-to-image and image-to-image tasks with 4K support."
metadata: {"mediaio":{"emoji":"🎨","requires":{"env":["API_KEY"]}},"publisher":"Community Maintainer","source":"https://platform.media.io/docs/"}
---

# MediaIO Seedream Image Generator Skill

## Overview
This skill provides access to **ByteDance Seedream 4.0** through the Media.io OpenAPI. Seedream is a versatile powerhouse supporting 4K generation and advanced editing, ensuring character and style consistency.

## Trigger Keywords
Use this skill when you hear:
- "Seedream", "Seedream AI", "Seedream image generator"
- "Generate image with Seedream"
- "Seedream 4.0 image generation"

## Requirements

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `API_KEY` | **Yes** | Media.io OpenAPI key, sent as `X-API-KEY` header. Apply at <https://developer.media.io/>. |

## API Details

### Seedream 4.0 Image-to-Image

- **API Name**: `Seedream 4.0`
- **Model Code**: `i2i-seedream-v4-0`
- **Endpoint**: `POST https://openapi.media.io/generation/seedream/i2i-seedream-v4-0`
- **Description**: A versatile powerhouse supporting 4K generation and advanced editing, ensuring character and style consistency.

#### Key Features
- High aesthetic quality image generation
- Detailed rendering capabilities
- Text-to-image support
- Image-to-image support
- Character consistency
- Style consistency
- Up to 4K resolution

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | Text description for image generation |
| `image` | string | No | Reference image URL for image-to-image |
| `ratio` | string | No | Image aspect ratio |
| `strength` | string | No | How strongly to follow the reference image (for i2i) |

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

### Image-to-Image Generation
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
        'prompt': 'a beautiful landscape painting, vibrant colors, artistic style',
        'image': 'https://example.com/reference-image.jpg',
        'ratio': '16:9'
    },
    api_key=api_key
)
print(result)  # Returns task_id when code=0
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

## Error Handling

| Error Code | Description |
|------------|-------------|
| `374004` | Not authenticated. Apply for an APP KEY at https://developer.media.io/ |
| `490505` | Insufficient credits. Recharge before invoking generation APIs |

## External Resources
- API documentation: https://platform.media.io/docs/
- Product overview: https://developer.media.io/
- Credit purchase: https://developer.media.io/pricing.html

## Related Files
- scripts/skill_router.py: core routing logic
- scripts/c_api_doc_detail.json: API definitions

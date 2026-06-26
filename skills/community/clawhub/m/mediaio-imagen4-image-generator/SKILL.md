---
name: mediaio-imagen4-image-generator
description: "Generate high-quality AI images using Google Imagen 4 via Media.io OpenAPI. Produces photorealistic, detailed images from text prompts with advanced text rendering accuracy."
metadata: {"mediaio":{"emoji":"🎨","requires":{"env":["API_KEY"]}},"publisher":"Community Maintainer","source":"https://platform.media.io/docs/"}
---

# MediaIO Imagen 4 Image Generator Skill

## Overview
This skill provides access to **Google Imagen 4** through the Media.io OpenAPI. Imagen 4 sets a new standard for photorealism and text rendering accuracy, handling the most complex prompts with ease.

## Trigger Keywords
Use this skill when you hear:
- "Imagen 4", "Google Imagen 4", "Imagen 4 API"
- "Generate image with Imagen 4"
- "Imagen 4 image generation"

## Requirements

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `API_KEY` | **Yes** | Media.io OpenAPI key, sent as `X-API-KEY` header. Apply at <https://developer.media.io/>. |

## API Details

### Imagen 4 Text-to-Image

- **API Name**: `Imagen 4`
- **Model Code**: `t2i-imagen-4`
- **Endpoint**: `POST https://openapi.media.io/generation/imagen/t2i-imagen-4`
- **Description**: Sets a new standard for photorealism and text rendering accuracy, handling the most complex prompts with ease.

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | Text description for image generation |
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

### Basic Image Generation
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
        'prompt': 'a cute puppy, photorealistic, soft natural light, high detail',
        'ratio': '1:1',
        'counts': '1'
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

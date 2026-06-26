---
name: mediaio-nano-banana-pro-image-generator
description: "Generate AI images using Nano Banana Pro via Media.io OpenAPI. State-of-the-art image quality with advanced reasoning, multi-image fusion, character consistency. Supports up to 4K resolution."
metadata: {"mediaio":{"emoji":"🎨","requires":{"env":["API_KEY"]}},"publisher":"Community Maintainer","source":"https://platform.media.io/docs/","homepage":"https://developer.media.io/"}
---

# MediaIO Nano Banana Pro Image Generator Skill

## Overview
This skill provides access to **Nano Banana Pro** through the Media.io OpenAPI. Nano Banana Pro utilizes next-gen multimodal reasoning to generate images that perfectly align with nuanced conceptual descriptions, featuring state-of-the-art image quality with advanced reasoning, multi-image fusion, and character consistency.

## Trigger Keywords
Use this skill when you hear:
- "Nano Banana Pro", "Nano Banana Pro image generator"
- "Generate image with Nano Banana Pro"
- "Banana Pro AI image generation"

## Requirements

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `API_KEY` | **Yes** | Media.io OpenAPI key, sent as `X-API-KEY` header. Apply at <https://developer.media.io/>. |

## API Details

### Nano Banana Pro Image Generation

- **API Name**: `Nano Banana Pro`
- **Model Code**: `i2i-banana-2`
- **Endpoint**: `POST https://openapi.media.io/generation/banana/i2i-banana-2`
- **Description**: Utilizes next-gen multimodal reasoning to generate images that perfectly align with nuanced conceptual descriptions.

#### Key Features
- State-of-the-art image quality
- Advanced multimodal reasoning
- Multi-image fusion
- Character consistency
- Up to 4K resolution support
- Perfect alignment with nuanced conceptual descriptions

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | Text description for image generation |
| `image` | string | No | Reference image URL for image-to-image |
| `ratio` | string | No | Image aspect ratio |
| `fusion_strength` | string | No | Multi-image fusion strength |

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

### High-Quality Image Generation
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
        'prompt': 'a serene mountain landscape at sunset, photorealistic, 4K quality, dramatic lighting',
        'ratio': '16:9'
    },
    api_key=api_key
)
print(result)  # Returns task_id when code=0
```

### Multi-Image Fusion
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
        'prompt': 'a futuristic cityscape combining classical and modern architecture',
        'image': 'https://example.com/reference-image.jpg',
        'fusion_strength': '0.7'
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

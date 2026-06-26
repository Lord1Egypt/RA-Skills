---
name: mediaio-aigc-generate
description: "Generate and edit AI images and videos with Media.io OpenAPI. Supports text-to-image, image-to-image, text-to-video, and image-to-video, plus task status and credit queries. Access top models like Imagen 4, Seedream, Kling, Vidu, Wan, and Veo 3.1 in one place."
metadata: {"mediaio":{"emoji":"🎨","requires":{"env":["API_KEY"]}},"publisher":"Community Maintainer","source":"https://platform.media.io/docs/"}
---

# MediaIO AIGC Generate Skill

## Overview
This skill routes MediaIO OpenAPI requests based on `scripts/c_api_doc_detail.json`.
It provides a single entry point, `Skill.invoke(api_name, params, api_key)`, covering credits queries, text-to-image, image-to-image, image-to-video, text-to-video, and task result lookups.

## Requirements

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `API_KEY` | **Yes** | Media.io OpenAPI key, sent as `X-API-KEY` header. Apply at <https://developer.media.io/>. Use a **least-privilege / test key**; do not reuse broader platform credentials. |

## Provenance and Credential Notes
- Maintainer: community-maintained skill (not an official Media.io release)
- Reference homepage: https://developer.media.io/
- Reference API docs: https://platform.media.io/docs/
- Target API domain used by this skill: `https://openapi.media.io`
- Required credential: `API_KEY` (used as `X-API-KEY`)
- Security recommendation: use a least-privilege/test key, avoid reusing broader platform credentials.
- Credential loading: set `API_KEY` in your environment, or pass `api_key` explicitly to `Skill.invoke(...)`.

## API Coverage (from c_api_doc_detail.json)
The current API definition includes 24 endpoints, grouped by capability:

- Query APIs
  - `Credits` (query user credit balance)
  - `Task Result` (query task status/result by `task_id`)
- Text To Image�?�?
  - `Imagen 4`
  - `soul_character`
- Image To Image�?�?
  - `Nano Banana`
  - `Seedream 4.0`
  - `Nano Banana Pro`
- Image To Video�?4�?
  - `Wan 2.6` / `Wan 2.2` / `Wan 2.5`
  - `Hailuo 02` / `Hailuo 2.3`
  - `Kling 2.1` / `Kling 2.5 Turbo` / `Kling 2.6` / `Kling 3.0`
  - `Vidu Q2` / `Vidu Q3`
  - `Google Veo 3.1` / `Google Veo 3.1 Fast`
  - `Motion Control Kling 2.6`
- Text To Video�?�?
  - `Wan 2.6 (Text To Video)`
  - `Vidu Q3 (Text To Video)`
  - `Wan 2.5 (Text To Video)`

## Input and Output Format
- Input:
  - `api_name`: API name (must exactly match the `name` field in `c_api_doc_detail.json`)
  - `params`: Business parameter dictionary (only include fields defined in `api_body`)
  - `api_key`: API key
- Output:
  - Returns the raw API response payload (dict/json)

### Common Response Structure
- Success response is typically: `{"code": 0, "msg": "", "data": {...}, "trace_id": "..."}`
- Asynchronous generation APIs usually return: `data.task_id`
- Final artifacts should be retrieved by polling `Task Result`

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
- Purpose: provide a shared key source for local scripts.
- Note: examples below read `api_key` from environment variable.

Windows PowerShell�?
```powershell
$env:API_KEY="your-api-key"
```

macOS / Linux (bash/zsh):
```bash
export API_KEY="your-api-key"
```

## Usage Examples (Python)

### Example A: Query Credits (`Credits`)
```python
import os
from scripts.skill_router import Skill

skill = Skill('scripts/c_api_doc_detail.json')
api_key = os.getenv('API_KEY', '')
if not api_key:
  raise RuntimeError('API_KEY is not set')
result = skill.invoke('Credits', {}, api_key=api_key)
print(result)
```

### Example B: Text-to-Image (`Imagen 4`)
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
print(result)  # When code=0, data usually contains task_id.
```

### Example C: Query Task Result (`Task Result`)
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

  ### Task Status Reference
  - `waiting`: queued
  - `processing`: running
  - `completed`: completed successfully
  - `failed`: failed
  - `timeout`: timed out

## Parameter Guidance (by Capability)
- Text To Image / Image To Image / Video APIs:
  - Required parameters are defined by `required=true` in `api_body`.
  - Enum fields (for example `ratio`, `duration`, `resolution`) must use documented values.
- `Task Result`:
  - Requires `task_id`, passed as `{'task_id': 'xxx'}` (path parameters are replaced automatically by the router).
- `Credits`:
  - No business parameters are required; use `params={}`.

## Typical Invocation Flow
1. Call a generation API (for example `Imagen 4` or `Kling 3.0`) to obtain `task_id`.
2. Poll the same task using `Task Result`.
3. When status is `completed/succeeded`, extract output URLs from `data.result`.

## Error Handling Notes
- API not found: returns `{"error": "API 'xxx' not found."}`
- Request exception: returns `{"error": "<exception message>"}`
- Invalid response format: returns `{"error": "Invalid response", ...}`

## Additional Response Code Notes
- `374004`: not authenticated. Apply for an APP KEY at https://developer.media.io/.
- `490505`: insufficient credits. Recharge before invoking generation APIs.

## Important Implementation Notes
- API names in `c_api_doc_detail.json` are unique, including text-to-video variants.
- The router validates duplicate names at load time and fails fast if duplicates are reintroduced.
- For best compatibility, invoke APIs by exact `name` from the JSON definition.

## Extension and Integration Recommendations
- Add asynchronous invocation via `asyncio` or threads.
- Auto-generate parameter validation and type hints from API metadata.
- Package this skill as a microservice/API for multi-client integration.

## External Resources
- API documentation: https://platform.media.io/docs/
- Product overview: https://developer.media.io/
- Credit purchase: https://developer.media.io/pricing.html

## Related Files
- scripts/skill_router.py: core routing logic
- scripts/c_api_doc_detail.json: API definitions


````skill
---
name: mediaio-kling-video-generator
description: Generate AI videos using Kling via Media.io OpenAPI. Supports text-to-video and image-to-video with high visual fidelity, smooth motion, and cinematic quality.
requires:
  env:
    - API_KEY
metadata:
  mediaio:
    emoji: ""
    priority: "P0"
    core_goal_keywords:
      - text-to-video
      - image-to-video
    trigger_keywords:
      - Kling
      - Kling AI
      - Kling video generator
      - Kling AI video
  publisher: Community Maintainer
  source: https://platform.media.io/docs/
---

# Kling AI Video Generator

## Overview
This skill focuses on a single model family and calls Media.io OpenAPI via `Skill.invoke(api_name, params, api_key)`.
It includes only common APIs (`Credits`, `Task Result`) plus model-specific APIs for this skill.

## Core Trigger Keywords
Kling, Kling AI, Kling video generator, Kling AI video

## Core Goal Keywords
text-to-video, image-to-video

## Environment Variable
- `API_KEY` (required): Media.io OpenAPI key used as `X-API-KEY`.

## Quick Start
```python
import os
from scripts.skill_router import Skill

skill = Skill('scripts/c_api_doc_detail.json')
api_key = os.getenv('API_KEY', '')
result = skill.invoke('Credits', {}, api_key=api_key)
print(result)
```

## Available APIs
- `Credits` (`user-credits`)
- `Task Result` (`generation-result`)
- `Kling 2.1` (`i2v-kling-v2-1`)
- `Kling 2.5 Turbo` (`i2v-kling-v2-5-turbo`)
- `Kling 2.6` (`i2v-kling-v2-6`)
- `Kling 3.0` (`i2v-kling-v3-0`)
- `Motion Control Kling 2.6` (`i2v-motion-control-kling-v2-6`)

## Notes
- Use exact `api_name` from `scripts/c_api_doc_detail.json` when invoking.
- Generation APIs return `task_id`; poll with `Task Result`.
````

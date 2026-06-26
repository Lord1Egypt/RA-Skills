````skill
---
name: mediaio-vidu-video-generator
description: Generate AI videos using Vidu via Media.io OpenAPI. Supports text-to-video and image-to-video with high-quality motion, smooth transitions.
requires:
  env:
    - API_KEY
metadata:
  mediaio:
    emoji: ""
    priority: "P1"
    core_goal_keywords:
      - text-to-video
      - image-to-video
    trigger_keywords:
      - Vidu
      - Vidu AI
      - Vidu video generator
  publisher: Community Maintainer
  source: https://platform.media.io/docs/
---

# Vidu AI Video Generator

## Overview
This skill focuses on a single model family and calls Media.io OpenAPI via `Skill.invoke(api_name, params, api_key)`.
It includes only common APIs (`Credits`, `Task Result`) plus model-specific APIs for this skill.

## Core Trigger Keywords
Vidu, Vidu AI, Vidu video generator

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
- `Vidu Q2` (`i2v-vidu-q2`)
- `Vidu Q3` (`i2v-vidu-q3`)
- `Vidu Q3 (Text To Video)` (`t2v-vidu-q3`)

## Notes
- Use exact `api_name` from `scripts/c_api_doc_detail.json` when invoking.
- Generation APIs return `task_id`; poll with `Task Result`.
````

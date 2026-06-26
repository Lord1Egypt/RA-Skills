````skill
---
name: mediaio-hailuo-video-generator
description: "Generate AI videos using MiniMax Hailuo (Hailuo 2.3) via Media.io OpenAPI. Supports text-to-video and image-to-video with fast generation, high-quality HD output."
metadata: {"mediaio": {"emoji": "", "requires": {"env": ["API_KEY"]}, "priority": "P0", "core_goal_keywords": ["text-to-video", "image-to-video"], "trigger_keywords": ["Hailuo", "Hailuo AI", "Hailuo video generator", "MiniMax Hailuo"]}, "publisher": "Community Maintainer", "source": "https://platform.media.io/docs/"}
---

# Hailuo AI Video Generator

## Overview
This skill focuses on a single model family and calls Media.io OpenAPI via `Skill.invoke(api_name, params, api_key)`.
It includes only common APIs (`Credits`, `Task Result`) plus model-specific APIs for this skill.

## Core Trigger Keywords
Hailuo, Hailuo AI, Hailuo video generator, MiniMax Hailuo

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
- `Hailuo 02` (`i2v-minimax-02`)
- `Hailuo 2.3` (`i2v-minimax-v2-3`)

## Notes
- Use exact `api_name` from `scripts/c_api_doc_detail.json` when invoking.
- Generation APIs return `task_id`; poll with `Task Result`.
````

````skill
---
name: mediaio-google-veo-video-generator
description: "Generate AI videos using Google Veo (Veo 3 / Veo 3.1) via Media.io OpenAPI. Produces cinematic-quality video from text and image inputs."
metadata: {"mediaio": {"emoji": "", "requires": {"env": ["API_KEY"]}, "priority": "P0", "core_goal_keywords": ["text-to-video", "image-to-video"], "trigger_keywords": ["Google Veo", "Veo 3.1", "Veo video generator", "Veo 3"]}, "publisher": "Community Maintainer", "source": "https://platform.media.io/docs/"}
---

# Google Veo AI Video Generator

## Overview
This skill focuses on a single model family and calls Media.io OpenAPI via `Skill.invoke(api_name, params, api_key)`.
It includes only common APIs (`Credits`, `Task Result`) plus model-specific APIs for this skill.

## Core Trigger Keywords
Google Veo, Veo 3.1, Veo video generator, Veo 3

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
- `Google Veo 3.1` (`i2v-veo-v3-1`)
- `Google Veo 3.1 Fast` (`i2v-veo-v3-1-fast`)

## Notes
- Use exact `api_name` from `scripts/c_api_doc_detail.json` when invoking.
- Generation APIs return `task_id`; poll with `Task Result`.
````

````skill
---
name: mediaio-wan-video-generator
description: "Generate AI videos using Wan (v2.6) via Media.io OpenAPI. Supports text-to-video, image-to-video, and reference-to-video with 1080p output."
metadata: {"mediaio": {"emoji": "", "requires": {"env": ["API_KEY"]}, "priority": "P1", "core_goal_keywords": ["text-to-video", "image-to-video", "reference-to-video"], "trigger_keywords": ["Wan", "Wan video", "Wan AI video generator"]}, "publisher": "Community Maintainer", "source": "https://platform.media.io/docs/"}
---

# Wan AI Video Generator

## Overview
This skill focuses on a single model family and calls Media.io OpenAPI via `Skill.invoke(api_name, params, api_key)`.
It includes only common APIs (`Credits`, `Task Result`) plus model-specific APIs for this skill.

## Core Trigger Keywords
Wan, Wan video, Wan AI video generator

## Core Goal Keywords
text-to-video, image-to-video, reference-to-video

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
- `Wan 2.2` (`i2v-wan-v2-2`)
- `Wan 2.5` (`i2v-wan-v2-5`)
- `Wan 2.6` (`i2v-wan-v2-6`)
- `Wan 2.5 (Text To Video)` (`t2v-wan-v2-5`)
- `Wan 2.6 (Text To Video)` (`t2v-wan-v2-6`)

## Notes
- Use exact `api_name` from `scripts/c_api_doc_detail.json` when invoking.
- Generation APIs return `task_id`; poll with `Task Result`.
````

````skill
---
name: mediaio-text-to-video-api
description: "Generate AI videos from text descriptions using Media.io OpenAPI. Provide a text prompt to receive a high-quality AI-generated video. Supports top models."
metadata: {"mediaio": {"emoji": "", "requires": {"env": ["API_KEY"]}, "priority": "P0", "core_goal_keywords": ["text-to-video"], "trigger_keywords": ["text to video", "text-to-video API", "generate video from text"]}, "publisher": "Community Maintainer", "source": "https://platform.media.io/docs/"}
---

# Text to Video API

## Overview
This skill focuses on text-to-video generation via Media.io OpenAPI.
It includes only common APIs (`Credits`, `Task Result`) and one text-to-video model API for this skill.

## Core Trigger Keywords
text to video, text-to-video API, generate video from text

## Core Goal Keywords
text-to-video

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
- `Vidu Q3 (Text To Video)` (`t2v-vidu-q3`)

## Notes
- Use exact `api_name` from `scripts/c_api_doc_detail.json` when invoking.
- Generation APIs return `task_id`; poll with `Task Result`.
````

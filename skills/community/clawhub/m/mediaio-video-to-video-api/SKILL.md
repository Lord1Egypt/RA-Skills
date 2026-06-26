````skill
---
name: mediaio-video-to-video-api
description: "Transform and restyle existing videos using AI via Media.io OpenAPI. Apply style transfers, creative effects, and video transformations."
metadata: {"mediaio": {"emoji": "", "requires": {"env": ["API_KEY"]}, "priority": "P1", "core_goal_keywords": ["video-to-video"], "trigger_keywords": ["video to video", "video-to-video API", "restyle video", "video style transfer"]}, "publisher": "Community Maintainer", "source": "https://platform.media.io/docs/"}
---

# Video to Video API

## Overview
This skill focuses on video transformation workflows via Media.io OpenAPI.
It includes only common APIs (`Credits`, `Task Result`) and one video transformation API for this skill.

## Core Trigger Keywords
video to video, video-to-video API, restyle video, video style transfer

## Core Goal Keywords
video-to-video

## Environment Variable
- `API_KEY` (required): Media.io OpenAPI key used as `X-API-KEY`.

## Available APIs
- `Credits` (`user-credits`)
- `Task Result` (`generation-result`)
- `Motion Control Kling 2.6` (`i2v-motion-control-kling-v2-6`)
````

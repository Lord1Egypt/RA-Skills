````skill
---
name: mediaio-image-to-video-api
description: "Animate images into videos using AI via Media.io OpenAPI. Transform any static image into a dynamic AI video with realistic motion."
metadata: {"mediaio": {"emoji": "", "requires": {"env": ["API_KEY"]}, "priority": "P0", "core_goal_keywords": ["image-to-video"], "trigger_keywords": ["image to video", "image-to-video API", "animate image", "photo to video"]}, "publisher": "Community Maintainer", "source": "https://platform.media.io/docs/"}
---

# Image to Video API

## Overview
This skill focuses on image-to-video generation via Media.io OpenAPI.
It includes only common APIs (`Credits`, `Task Result`) and one image-to-video model API for this skill.

## Core Trigger Keywords
image to video, image-to-video API, animate image, photo to video

## Core Goal Keywords
image-to-video

## Environment Variable
- `API_KEY` (required): Media.io OpenAPI key used as `X-API-KEY`.

## Available APIs
- `Credits` (`user-credits`)
- `Task Result` (`generation-result`)
- `Vidu Q3` (`i2v-vidu-q3`)
````

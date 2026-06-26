---
name: weather-brief
slug: weather-brief
version: 0.2.0
description: Concise daily weather briefing for OpenClaw.
author: OpenClaw Labs
license: MIT
entrypoint: hooks/prepare.sh
hooks:
  prepare: hooks/prepare.sh
  validate: hooks/validate.sh
assets:
  - assets/prompt.txt
  - assets/icons/weather-brief.txt
examples:
  - examples/request.json
tags:
  - weather
  - local
  - briefing
publish:
  registry: local
  visibility: private
---

# Weather Brief

The Weather Brief skill generates a compact spoken forecast based on a city name
and preferred unit system.

## Inputs

- `city`: Target city, for example `Portland`
- `units`: `metric` or `imperial`

## Output

A short text response suitable for voice playback.

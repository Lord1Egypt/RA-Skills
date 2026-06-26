---
name: media-gen
description: 'Generate AI images or videos through AIsa. Use when: the user needs creative generation, asset drafts, or media workflows. Supports image and video generation.'
author: AIsa
version: 1.1.0
license: MIT
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  bins:
  - python3
  env:
  - AISA_API_KEY
metadata:
  aisa:
    emoji: 🎬
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    compatibility:
    - openclaw
    - claude-code
    - hermes
  openclaw:
    emoji: 🎬
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
---

# Media Gen

Generate AI images or videos through AIsa. Use when: the user needs creative generation, asset drafts, or media workflows. Supports image and video generation.

## When to use

- The user needs image or video generation.
- The user wants creative drafts or media assets from one API key.
- The user wants quick generation workflows.

## High-Intent Workflows

- Generate an image draft.
- Generate a short video concept.
- Turn a creative brief into media output.

## Quick Reference

- `python3 scripts/media_gen_client.py --help`

## Setup

- `AISA_API_KEY` is required for AIsa-backed API access.
- Use repo-relative `scripts/` paths from the shipped package.
- Prefer explicit CLI auth flags when a script exposes them.

## Example Requests

- Generate a futuristic city poster
- Create a short product-demo video concept
- Turn a scene description into an image draft

## Guardrails

- Do not promise media output that was not returned.
- Do not reference local files that were not provided.
- If the upstream is rate-limited, say so.

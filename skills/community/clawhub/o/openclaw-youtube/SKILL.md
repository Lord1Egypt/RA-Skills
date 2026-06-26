---
name: openclaw-youtube
description: 'Search YouTube videos, channels, rankings, and trends through AIsa. Use when: the user needs YouTube research, competitor scouting, or content discovery. Supports video discovery and SERP-style analysis.'
author: AIsa
version: 1.0.0
license: Apache-2.0
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  bins:
  - python3
  env:
  - AISA_API_KEY
metadata:
  aisa:
    emoji: ▶️
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
    emoji: ▶️
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
---

# Openclaw Youtube

Search YouTube videos, channels, rankings, and trends through AIsa. Use when: the user needs YouTube research, competitor scouting, or content discovery. Supports video discovery and SERP-style analysis.

## When to use

- The user needs YouTube video, channel, or trend discovery.
- The user wants content research, SERP scouting, or competitor review.
- The user wants public YouTube results quickly.

## High-Intent Workflows

- Find top-ranking videos for a topic.
- Inspect a competitor channel's recent content direction.
- Scan trend-heavy queries for content opportunities.

## Quick Reference

- `python3 scripts/youtube_client.py --help`

## Setup

- `AISA_API_KEY` is required for AIsa-backed API access.
- Use repo-relative `scripts/` paths from the shipped package.
- Prefer explicit CLI auth flags when a script exposes them.

## Example Requests

- Search top YouTube videos about OpenAI Agents
- Review a competitor channel's recent uploads
- Find high-ranking videos for AI coding tutorials

## Guardrails

- Do not invent video titles, URLs, or metrics.
- Summaries should stay grounded in returned results.
- If the upstream returns no results, say so clearly.

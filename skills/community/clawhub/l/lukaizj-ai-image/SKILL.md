---
name: AI Image Generation
description: AI image generation - Generate images using OpenAI DALL-E or other AI image APIs
homepage: https://github.com/lukaizj/ai-image-skill
tags:
  - ai
  - image
  - generation
  - openai
requires:
  env:
    - OPENAI_API_KEY
files:
  - ai_image.py
---

# AI Image Generation

AI image generation skill for OpenClaw. Generate images using DALL-E or other AI image APIs.

## Setup

1. Get OpenAI API key from https://platform.openai.com/api-keys
2. Configure OPENAI_API_KEY environment variable

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API Key |
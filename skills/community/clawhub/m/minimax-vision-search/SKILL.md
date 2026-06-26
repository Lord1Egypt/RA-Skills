---
name: minimax-vision-search
description: Analyze images and search the web using MiniMax MCP tools
metadata:
  openclaw:
    requires:
      bins: [uvx]
      env: [MINIMAX_API_KEY, MINIMAX_API_HOST]
  homepage: https://github.com/daowuu/minimax-vision-search
---

# MiniMax Vision & Search MCP

## Prerequisites
- Install uv (recommended via Homebrew): `brew install uv`
- Set your API key: `export MINIMAX_API_KEY=your_key`

## Quick Start
Image: `python3 scripts/understand_image.py <path_or_url> "<prompt>"`
Search: `python3 scripts/web_search.py <query> [limit]`

## Image Sources
- Local file: /path/to/image.jpg
- URL: https://example.com/image.jpg
- Telegram: auto-saved to ~/.openclaw/media/inbound/

## Tips
- Telegram → auto-saved → analyzed
- Webchat image NOT supported directly

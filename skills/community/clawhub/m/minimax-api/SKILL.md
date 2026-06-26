---
name: minimax-api
description: Enables image understanding and web search via MiniMax's Token Plan API. Use when asked to analyze/describe images, extract information from images, or search the web. Handles both HTTP/HTTPS image URLs and local file paths (absolute paths). Triggers on: "analyze this image", "describe this picture", "what's in this image", "search the web for", "look up", "web search".
---

# Minimax API

## Overview

Provides two capabilities via MiniMax's Token Plan API:
1. **Image understanding** — analyze images via VLM
2. **Web search** — real-time web search

API base URL: `https://api.minimaxi.com`

## Capabilities

### 1. understand_image

Analyzes an image and returns a text description.

**Input:**
- `image_url`: HTTP/HTTPS URL or absolute local file path (e.g., `/home/user/photo.png`, `D:\images\photo.png`)
- `prompt`: What to ask about the image

**Output:** Text description from the VLM.

**Script:** `scripts/minimax_image.py`

**Usage:**
```bash
export MINIMAX_API_KEY="your_api_key"

python3 skills/minimax-api/scripts/minimax_image.py \
  --prompt "Describe this image briefly" \
  --image-url "https://example.com/photo.jpg"

# Or with local file
python3 skills/minimax-api/scripts/minimax_image.py \
  --prompt "Extract text from this image" \
  --image-url "/home/user/documents/receipt.png"
```

### 2. web_search

Performs a web search and returns formatted results.

**Input:**
- `query`: Search query string

**Output:** JSON with organic results, related searches, and metadata.

**Script:** `scripts/minimax_search.py`

**Usage:**
```bash
export MINIMAX_API_KEY="your_api_key"

python3 skills/minimax-api/scripts/minimax_search.py \
  --query "MiniMax M2.7 release notes"
```

## Setup

**Required:** A MiniMax API key from [platform.minimaxi.com](https://platform.minimaxi.com).

Set it as an environment variable:

```bash
export MINIMAX_API_KEY="your_api_key_here"
```

Add the above line to your `~/.bashrc` (or `.zshrc`) to make it permanent.

Alternatively, pass `--api-key` directly on the command line (not recommended — exposes key in shell history).

## API Reference

See `references/api_spec.md` for full API documentation including request/response schemas, error codes, and headers.

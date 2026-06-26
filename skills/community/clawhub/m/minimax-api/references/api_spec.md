# MiniMax Token Plan API Specification

## Overview

MiniMax provides two API endpoints accessible via the Token Plan subscription:
- **VLM API** — image understanding (vision)
- **Search API** — web search

Base URL: `https://api.minimaxi.com`

## Authentication

All requests require:
```
Authorization: Bearer {API_KEY}
MM-API-Source: minimax-coding-plan-mcp
Content-Type: application/json
```

## Endpoints

### 1. Image Understanding (VLM)

**Endpoint:** `POST /v1/coding_plan/vlm`

**Request Body:**
```json
{
  "prompt": "string - The question/instruction about the image",
  "image_url": "string - Image as data URL (data:image/{format};base64,{data})"
}
```

**Supported Image Formats:** JPEG, PNG, WebP

**Image URL Formats:**
- `data:image/jpeg;base64,{base64_data}` — base64 encoded image data
- `data:image/png;base64,{base64_data}` — base64 encoded PNG
- `data:image/webp;base64,{base64_data}` — base64 encoded WebP
- `https://example.com/image.jpg` — HTTP/HTTPS URL (only works via MCP server which auto-converts)

**Response:**
```json
{
  "content": "string - The VLM's text response",
  "base_resp": {
    "status_code": 0,
    "status_msg": "string"
  }
}
```

**Error Codes:**
- `0` — Success
- `1004` — Authentication error (invalid API key)
- `2013` — Invalid parameters (e.g., invalid image URL)
- `2038` — Real-name verification required

### 2. Web Search

**Endpoint:** `POST /v1/coding_plan/search`

**Request Body:**
```json
{
  "q": "string - Search query"
}
```

**Response:**
```json
{
  "organic": [
    {
      "title": "string - Result title",
      "link": "string - Result URL",
      "snippet": "string - Result description",
      "date": "string - Publication date (if available)"
    }
  ],
  "related_searches": [
    {
      "query": "string - Related search query"
    }
  ],
  "base_resp": {
    "status_code": 0,
    "status_msg": "string"
  }
}
```

## Error Handling

All endpoints return a `base_resp` object:

| status_code | Meaning |
|-------------|---------|
| 0 | Success |
| 1004 | Auth error — check API key |
| 2013 | Invalid parameters |
| 2038 | Real-name verification needed |

On error, the tool exits with code 1 and prints the error message to stderr.

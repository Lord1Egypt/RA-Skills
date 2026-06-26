# API Reference

Docs: https://docs.perceptron.inc/api-reference/endpoint/chat-completions

## SDK Configuration

```python
from perceptron import configure, config

# Global configuration (or set env vars)
configure(
    provider="perceptron",
    api_key="ak_...",
    model="isaac-0.2-2b-preview",
    temperature=0.0,
    timeout=60.0,
    retries=3,
)

# Temporary overrides for a single call
with config(max_tokens=512, model="isaac-0.2-1b"):
    result = detect("photo.jpg", classes=["car"])
```

Environment variables:
- `PERCEPTRON_API_KEY` — API key (required)
- `PERCEPTRON_MODEL` — default model (optional, defaults to `isaac-0.2-2b-preview`)

## Models

| Model | Best for | Speed | Recommended temp |
|-------|----------|-------|-----------------|
| `isaac-0.2-2b-preview` (default) | General use, reasoning, detection | Fast | 0.0 |
| `isaac-0.2-1b` | Quick/simple tasks | Fastest | 0.0 |

List models programmatically:
```python
import httpx
resp = httpx.get("https://api.perceptron.inc/v1/models",
                 headers={"Authorization": "Bearer YOUR_API_KEY"})
for m in resp.json()["data"]:
    print(m["id"])
```

## Image Formats

- Local file paths (SDK handles base64 conversion automatically)
- HTTP(S) URLs
- Base64 data URLs: `data:image/jpeg;base64,...`
- Supported: JPEG, PNG, WebP, GIF, BMP, TIFF, HEIC

## Streaming

```python
from perceptron import detect

for event in detect("frame.png", classes=["person"], stream=True):
    if event["type"] == "text.delta":
        print(event["chunk"], end="", flush=True)
    elif event["type"] == "final":
        result = event["result"]
```

## Best Practices

1. **Always use the SDK** — handles auth, retries, base64 conversion, and response parsing
2. **Use hints for spatial tasks** — `<hint>BOX</hint>`, `POINT`, `POLYGON` in system messages
3. **Temperature 0.0** for deterministic, repeatable outputs
4. **Streaming** for real-time applications — reduces time-to-first-token
5. **`scale_points_to_pixels()`** to convert normalized coords to pixel space

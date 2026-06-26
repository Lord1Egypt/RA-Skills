# xAI Grok Imagine reference

## Current assumptions

- Auth env var: `XAI_API_KEY`
- Base URL: `https://api.x.ai/v1`
- Recommended generation model: `grok-imagine-image-quality`
- Generation endpoint: `POST /images/generations`
- Edit endpoint: `POST /images/edits`
- Edit supports up to **3** source images
- Generation supports `n` up to **10**
- Supported resolution tiers mentioned in docs: `1k`, `2k`
- Images return temporary URLs by default; download them promptly

## Generation payload

```json
{
  "model": "grok-imagine-image-quality",
  "prompt": "A collage of London landmarks in a stenciled street-art style",
  "n": 1,
  "aspect_ratio": "1:1",
  "resolution": "1k",
  "response_format": "url"
}
```

## Edit payload patterns

Single source image:

```json
{
  "model": "grok-imagine-image-quality",
  "prompt": "Render this as a pencil sketch with detailed shading",
  "image": {
    "url": "data:image/png;base64,...",
    "type": "image_url"
  }
}
```

Multi-image edit / composition:

```json
{
  "model": "grok-imagine-image-quality",
  "prompt": "Place subject A into the style and environment of image B",
  "image": [
    {"url": "data:image/png;base64,...", "type": "image_url"},
    {"url": "https://example.com/reference.png", "type": "image_url"}
  ]
}
```

## Notes

- The local script in `scripts/grok_imagine.py` uses JSON requests and data URIs for local edit sources.
- Because the current account on this machine returned a 403 credit/license error, edit and generate flows are structurally implemented but not fully live-tested against a funded account yet.
- If xAI changes request shape, inspect their latest docs first and patch the script rather than guessing.

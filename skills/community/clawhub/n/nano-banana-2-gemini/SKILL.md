---
name: nano-banana-2
description: |
  Gemini image generation, editing, and search-grounded image creation via
  gemini-3.1-flash-image-preview (Nano Banana 2).

  USE FOR:
  - Generating images from text prompts (text-to-image)
  - Editing or transforming an existing image with text instructions
  - Generating images grounded in live web/image search results

  Requires GEMINI_API_KEY environment variable. See rules/setup.md for
  configuration and rules/security.md for output handling guidelines.
allowed-tools:
  - Bash(curl *)
  - Bash(python3 *)
  - Bash(mkdir *)
  - Bash(open .nano-banana/*)
---

# nano-banana-2

Gemini image generation and editing via `gemini-3.1-flash-image-preview`. All
output images are written to `.nano-banana/` in the current project directory.

## Prerequisites

`GEMINI_API_KEY` must be set in the environment. Verify with:

```bash
echo $GEMINI_API_KEY
```

If empty, see [rules/setup.md](rules/setup.md). For output handling and security
guidelines, see [rules/security.md](rules/security.md).

## Workflow

Follow this escalation pattern:

1. **Generate** - Create a new image from a text prompt only.
2. **Edit** - Modify an existing local image with a text instruction.
3. **Search-Grounded** - Generate informed by live web/image search results (use when current visual references, styles, or real-world accuracy matter).

| Goal                               | Operation         | When                                           |
| ---------------------------------- | ----------------- | ---------------------------------------------- |
| Create image from scratch          | `generate`        | No source image; prompt is self-contained      |
| Modify or extend an existing image | `edit`            | Have a local PNG/JPEG to transform             |
| Ground output in current web data  | `search-grounded` | Need up-to-date styles or real-world references|

## Output & Organization

All images are saved to `.nano-banana/` in the current working directory.
Add `.nano-banana/` to `.gitignore` to prevent generated assets from being committed.

```bash
mkdir -p .nano-banana
echo ".nano-banana/" >> .gitignore
```

Naming conventions:

```
.nano-banana/gen-{slug}-{timestamp}.png
.nano-banana/edit-{slug}-{timestamp}.png
.nano-banana/search-{slug}-{timestamp}.png
```

Where `{slug}` is a short kebab-case label from the first 4-5 words of the prompt,
and `{timestamp}` is `YYYYMMDD-HHMMSS`.

After saving, open to confirm the result:

```bash
open "$(ls -t .nano-banana/*.png | head -1)"
```

## API Reference

| Property             | Value                                                                                                     |
| -------------------- | --------------------------------------------------------------------------------------------------------- |
| Model                | `gemini-3.1-flash-image-preview`                                                                          |
| Endpoint             | `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent` |
| Auth header          | `x-goog-api-key: $GEMINI_API_KEY`                                                                         |
| Image output         | `candidates[0].content.parts[].inlineData.data` (base64 PNG)                                             |

### Resolution options (`imageConfig.imageSize`)

| Value  | Resolution     |
| ------ | -------------- |
| `512`  | 0.5K (fastest) |
| `1024` | 1K (default)   |
| `2048` | 2K             |
| `4096` | 4K             |

### Aspect ratio options (`imageConfig.aspectRatio`)

`1:1`, `16:9`, `9:16`, `1:4`, `4:1`, `1:8`, `8:1`, `2:3`, `3:2`

### Thinking mode (`generationConfig.thinkingConfig.thinkingBudget`)

An integer token budget. Set inside `generationConfig`, not at the top level.

| Value          | Behaviour                                      |
| -------------- | ---------------------------------------------- |
| `0`            | Thinking off — fastest, lowest cost (default)  |
| `1024`         | Light thinking                                 |
| `8192`         | Deep thinking — recommended for grounded tasks |

## Operations

### 1. Generate (text-to-image)

```python
python3 - <<'PYEOF'
import os, base64, json, urllib.request, datetime

api_key = os.environ["GEMINI_API_KEY"]
prompt  = "a majestic mountain at sunrise, photorealistic"
slug    = "mountain-sunrise"
size    = "1024"    # 512 | 1024 | 2048 | 4096
aspect  = "16:9"   # 1:1 | 16:9 | 9:16 | 1:4 | 4:1 | 1:8 | 8:1 | 2:3 | 3:2
thinking = 0       # 0 = off, 1024 = light, 8192 = deep

payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"],
        "imageConfig": {"imageSize": size, "aspectRatio": aspect},
        "thinkingConfig": {"thinkingBudget": thinking}
    }
}

url = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-3.1-flash-image-preview:generateContent"
)
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
    method="POST"
)
with urllib.request.urlopen(req) as resp:
    data = json.load(resp)

ts  = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
out = f".nano-banana/gen-{slug}-{ts}.png"
os.makedirs(".nano-banana", exist_ok=True)

for part in data["candidates"][0]["content"]["parts"]:
    if part.get("inlineData", {}).get("mimeType", "").startswith("image/"):
        with open(out, "wb") as f:
            f.write(base64.b64decode(part["inlineData"]["data"]))
        print(f"Saved: {out}")
        break
    elif part.get("text"):
        print("Model:", part["text"])
PYEOF
```

### 2. Edit (image-to-image)

The source image is base64-encoded and sent alongside the instruction text.
Supports PNG and JPEG inputs.

```python
python3 - <<'PYEOF'
import os, base64, json, urllib.request, datetime

api_key     = os.environ["GEMINI_API_KEY"]
source_img  = "path/to/source.png"          # change to actual path
instruction = "Make the sky purple and add stars"
slug        = "purple-sky-stars"
size        = "1024"
aspect      = "1:1"
thinking    = 0   # 0 = off, 1024 = light, 8192 = deep

with open(source_img, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

ext  = source_img.rsplit(".", 1)[-1].lower()
mime = "image/jpeg" if ext in ("jpg", "jpeg") else "image/png"

payload = {
    "contents": [{
        "parts": [
            {"text": instruction},
            {"inline_data": {"mime_type": mime, "data": img_b64}}
        ]
    }],
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"],
        "imageConfig": {"imageSize": size, "aspectRatio": aspect},
        "thinkingConfig": {"thinkingBudget": thinking}
    }
}

url = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-3.1-flash-image-preview:generateContent"
)
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
    method="POST"
)
with urllib.request.urlopen(req) as resp:
    data = json.load(resp)

ts  = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
out = f".nano-banana/edit-{slug}-{ts}.png"
os.makedirs(".nano-banana", exist_ok=True)

for part in data["candidates"][0]["content"]["parts"]:
    if part.get("inlineData", {}).get("mimeType", "").startswith("image/"):
        with open(out, "wb") as f:
            f.write(base64.b64decode(part["inlineData"]["data"]))
        print(f"Saved: {out}")
        break
    elif part.get("text"):
        print("Model:", part["text"])
PYEOF
```

### 3. Search-Grounded Generation

Adds `googleSearch` with both `webSearch` and `imageSearch` types to ground the
output in live web data. Use when the prompt references real-world subjects,
current styles, recent events, or factual visual accuracy.

```python
python3 - <<'PYEOF'
import os, base64, json, urllib.request, datetime

api_key  = os.environ["GEMINI_API_KEY"]
prompt   = "Generate a product photo of the latest iPhone model"
slug     = "latest-iphone-product"
size     = "1024"
aspect   = "1:1"
thinking = 8192   # deeper thinking recommended for grounded generation

payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "tools": [{
        "googleSearch": {
            "searchTypes": ["webSearch", "imageSearch"]
        }
    }],
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"],
        "imageConfig": {"imageSize": size, "aspectRatio": aspect},
        "thinkingConfig": {"thinkingBudget": thinking}
    }
}

url = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-3.1-flash-image-preview:generateContent"
)
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
    method="POST"
)
with urllib.request.urlopen(req) as resp:
    data = json.load(resp)

ts  = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
out = f".nano-banana/search-{slug}-{ts}.png"
os.makedirs(".nano-banana", exist_ok=True)

for part in data["candidates"][0]["content"]["parts"]:
    if part.get("inlineData", {}).get("mimeType", "").startswith("image/"):
        with open(out, "wb") as f:
            f.write(base64.b64decode(part["inlineData"]["data"]))
        print(f"Saved: {out}")
        break
    elif part.get("text"):
        print("Model:", part["text"])
PYEOF
```

## Working with Results

```bash
# List all generated images
ls -lh .nano-banana/

# Open the most recent
open "$(ls -t .nano-banana/*.png | head -1)"

# Open all images generated today
open .nano-banana/*$(date +%Y%m%d)*.png
```

## Error Handling

If the API returns an error, the response will contain an `error` key. Print it with:

```python
python3 -c "
import json, sys
d = json.loads(sys.stdin.read())
if 'error' in d:
    print('API Error:', json.dumps(d['error'], indent=2))
elif not d.get('candidates'):
    print('No candidates:', json.dumps(d, indent=2))
"
```

Common errors:

| Error code           | Cause                                              |
| -------------------- | -------------------------------------------------- |
| `API_KEY_INVALID`    | `GEMINI_API_KEY` not set or incorrect              |
| `RESOURCE_EXHAUSTED` | Quota exceeded; check billing or wait              |
| `INVALID_ARGUMENT`   | Bad `imageSize` or `aspectRatio` value             |
| Empty `candidates`   | Safety filter blocked the prompt or source image   |
| `404 Not Found`      | Model not yet available on your API key; see setup |

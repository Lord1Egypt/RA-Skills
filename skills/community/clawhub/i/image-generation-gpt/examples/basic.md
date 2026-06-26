# Example — basic text-to-image

The simplest possible use: one trigger phrase, one image, defaults for everything else.

---

## Trigger

```text
高质量生图：黄昏时分的东京涉谷十字路口，雨后湿润的地面倒映霓虹灯，电影感构图
```

or in English:

```text
best image: Tokyo Shibuya crossing at dusk, wet pavement reflecting neon signs, cinematic composition
```

The skill takes everything after the colon as `prompt`, applies defaults, and calls `/v1/images/generations`.

---

## Resolved defaults

| Field | Value |
|---|---|
| `model` | `gpt-image-2` |
| `n` | `1` |
| `size` | `auto` |
| `quality` | `auto` |
| `format` | `png` |

---

## Equivalent raw request

```http
POST https://wellapi.ai/v1/images/generations
Authorization: Bearer $WELLAPI_API_KEY
Content-Type: application/json

{
  "model": "gpt-image-2",
  "prompt": "Tokyo Shibuya crossing at dusk, wet pavement reflecting neon signs, cinematic composition",
  "n": 1,
  "size": "auto",
  "quality": "auto",
  "format": "png"
}
```

---

## Response (truncated)

```json
{
  "created": 1778236581,
  "data": [
    { "b64_json": "iVBORw0KGgoAAAANSUhEUgAA..." }
  ],
  "output_format": "png",
  "quality": "auto",
  "size": "1024x1024",
  "usage": {
    "input_tokens": 22,
    "output_tokens": 1024,
    "total_tokens": 1046
  }
}
```

---

## What the skill prints

After base64-decoding `data[0].b64_json` and writing it to disk:

```text
MEDIA:/Users/you/.openclaw/work/wellapi-1778236581.png
```

OpenClaw picks up the `MEDIA:` line and attaches the file to the conversation automatically. No further commands needed.

---

## Tweaks you can ask for inline

Just add natural-language hints — the skill will pass them through:

- *"high quality, 2K landscape"* → `quality=high`, `size=2048x1152`
- *"give me 4 variants"* → `n=4`, output filenames suffixed `-1` … `-4`
- *"jpeg, small"* → `format=jpeg`, `size=1024x1024`

---
name: atlas-banana-textimage
description: Generates images from text prompts using the AtlasCloud Nanobanana 2 model (google/nano-banana-2/text-to-image). Use this skill whenever the user wants to create, render, or generate an image from a text description using Nanobanana or AtlasCloud. Triggers on phrases like: "gerar imagem", "generate image", "create image", "criar imagem com prompt", "draw a scene", or any request to produce a visual from a text prompt. Always use this skill when the user mentions Nanobanana, AtlasCloud image generation, or wants to produce an image from descriptive text.
metadata:
  {
    "openclaw":
      {
        "emoji": "🍌",
        "requires": { "bins": ["node"] },
        "install": []
      }
  }
---
# Atlas Nanobanana Text-to-Image 🍌

Generates images using the AtlasCloud **Nanobanana 2** model (`google/nano-banana-2/text-to-image`).

---

## Token Setup

Before generating images, you need the user's AtlasCloud API token.

- Check memory for `atlascloud_token`.
- If not found, ask the user: *"Please provide your AtlasCloud API token to get started."*
- Save the token to memory as `atlascloud_token` so it is not needed again.

---

## How to Generate an Image

**Step 1:** Write the params to `{baseDir}/params.json`.

**Step 2:** Run the script:

```bash
node {baseDir}/generate.js <TOKEN> {baseDir}/params.json
```

**Step 3:** In the script output, find the line that starts with `IMAGE_URL:` between the two rows of `=` signs:

```
============================================================
IMAGE_URL: https://atlas-media.oss-us-west-1.aliyuncs.com/images/xxxx.png
============================================================
```

> ⚠️ **CRITICAL**: Use **exactly** the URL that appears in the `IMAGE_URL:` line of this execution. Never use a URL from the conversation history, previous executions, or memory. Each execution generates a different URL.

Report this URL to the user.

---

## params.json — Payload Correto

> ⚠️ **IMPORTANT**: **Never include `media_resolution`** in the payload — it causes an HTTP 500 error.

```json
{
  "prompt": "descrição detalhada da imagem",
  "aspect_ratio": "16:9",
  "output_format": "png",
  "resolution": "2k",
  "enable_base64_output": false,
  "enable_sync_mode": false,
  "enable_web_search": false,
  "enable_image_search": false
}
```

### Available fields

| Field | Required | Default | Options |
|---|---|---|---|
| `prompt` | ✅ yes | — | any text |
| `aspect_ratio` | no | `16:9` | `1:1` | `4:3` | `3:4` | `16:9` | `9:16` | `21:9` |
| `resolution` | no | `2k` | `1k` | `2k` | `4k` |
| `output_format` | no | `png` | `png` | `jpeg` |
| `enable_web_search` | no | `false` | `true` | `false` |
| `enable_image_search` | no | `false` | `true` | `false` | | `enable_base64_output` | no | `false` | `true` | `false` |
| `enable_sync_mode` | no | `false` | `true` | `false` |

> **NÃO inclua** `media_resolution` — causa erro 500.

---

## Error Handling

| Erro | Causa provável | Solução |
|---|---|---|
| HTTP 500 | `media_resolution` presente no payload | Remova `media_resolution` do params.json |
| HTTP 500 | Token inválido ou expirado | Solicitar novo token ao usuário e atualizar memória |
| Link não atualiza | URL lida de lugar errado | Buscar a linha `IMAGE_URL:` no output desta execução |
| Timeout | Resolução muito alta | Tentar novamente com `"resolution": "1k"` |
| Job `failed` | Prompt inválido ou API instável | Simplificar o prompt e tentar novamente |

---

## Quando usar esta skill

- "Generate an image of..."
- "Create a picture of..."
- "Draw a scene with..."
- "Generate an image of..."
- "Create a photo of..."
- "Create an image with prompt..."
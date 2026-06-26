---
name: atlas-banana-imagetoimage
description: Edit or combine images using the AtlasCloud Nanobanana Edit model. Use when the user wants to modify an image based on another, such as swapping clothes, merging styles, or applying visual elements from one image to another. Triggers on phrases like: "Changing clothes in the photo", "swap clothes", "edit image with reference", "combine images", "apply the style of one image to another".
metadata:
  {
    "openclaw":
      {
        "emoji": "🖼️",
        "requires": { "bins": ["node", "npm"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "axios",
              "bins": ["axios"],
              "label": "Install axios for HTTP requests"
            }
          ]
      }
  }
---
# Atlas Nanobanana Image-to-Image 🖼️

Edits and combines images using the AtlasCloud **Nanobanana 2 Edit** model (`google/nano-banana-2/edit`).

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
**Step 3 — REQUIRED:** After the script finishes, run this bash command to read the generated URL:

```bash
cat {baseDir}/last_url.txt
```

⚠️ **CRITICAL**: Step 3 is **mandatory and irreplaceable**. The correct URL is ONLY in `last_url.txt`. Run `cat` as a separate bash command and use the exact text returned. Never use a URL from the conversation history, previous files in the context, or any other source.

Report the URL from `last_url.txt` to the user.

---

## params.json — Payload Correto

⚠️ **IMPORTANT**: **Never include `media_resolution`** in the payload — it causes an HTTP 500 error.

```json
{
  "prompt": "Replace the dress on the model in image 0 with the dress from image 1. Preserve identity, face, pose, and lighting.",
  "images": [
    "https://url-of-base-image.png",
    "https://url-of-reference-image.png"
  ],
  "aspect_ratio": "16:9",
  "output_format": "png",
  "resolution": "1k",
  "enable_base64_output": false,
  "enable_sync_mode": false,
  "enable_web_search": false,
  "enable_image_search": false
}
```

## Available Fields

| Field | Required | Default | Options |

|---|---|---|---|
| `prompt` | ✅ yes | — | any text |
| `images` | ✅ yes | — | array of 1–4 URLs |
| `aspect_ratio` | no | `16:9` | `1:1` | `4:3` | `3:4` | `16:9` | `9:16` | `21:9` |
| `resolution` | no | `1k` | `1k` | `2k` | `4k` |
| `output_format` | no | `png` | `png` | `jpeg` |
| `enable_web_search` | no | `false` | `true` | `false` |
| `enable_image_search` | no | `false` | `true` | `false` |
| `enable_base64_output` | no | `false` | `true` | `false` |
| `enable_sync_mode` | no | `false` | `true` | `false` |
**Do not include** `media_resolution` — it causes a 500 error.

---

## Prompt Tips for Image-to-Image

- Refer to images by position: "image 0" (base), "image 1" (reference).
- State clearly what to **preserve**: face, pose, proportions, lighting, background.
- State clearly what to **replace**: the clothing, the background, the style.
- Use negative instructions: "DO NOT change the face", "DO NOT transfer human elements from image 1".

---

## Error Handling

| Error | Probable Cause | Solution |
|---|---|---|

| HTTP 500 | `media_resolution` present in payload | Remove `media_resolution` from params.json |
| HTTP 500 | Invalid or expired token | Request a new token from the user and refresh memory |
| Link does not update | Step 3 was not executed | Run `cat {baseDir}/last_url.txt` as a bash command |
| Timeout | Resolution too high | Try again with `"resolution": "1k"` |
| Job `failed` | Image URLs inaccessible | Check if images are public |

---
## When to use this skill:

- "swap the clothes in this photo"
- "apply the style from image 1 to image 0"
- "edit this image using another as a reference"
- "change clothes in the photo"
- "combine two images with AI"

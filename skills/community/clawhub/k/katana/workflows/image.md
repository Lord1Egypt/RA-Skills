# Image Generation Workflow

**Load this file when the user requests image generation.**

---

## Model Selection

Check `{baseDir}/models.md` for full catalogue with pricing and capabilities.

For model aliases and selection, see `{baseDir}/models.md`. Top picks: `gpt-image-2` (gpt-image), `nano-banana-2` (nano), `gen` (default).

If the user specifies an exact model ID (e.g. `fluxklein9b`), pass it through directly.

### ⚠️ Models Requiring Image Input

The following models **require an image input** (`reference_image`, `image_urls`, or `reference_assets` with a source image). They cannot generate from text-only prompts:
- `nano-banana` — first-gen Nano Banana edit model
- `qwen-image-edit` — Qwen Image Edit
- `flux-kontext-max` — Kontext Max edit model
- `flux-kontext-pro` — Kontext Pro edit model

### Cost Reference

See `{baseDir}/models.md` for detailed pricing per model.

---

Before submitting, present a pre-submission summary and wait for user confirmation (see `{baseDir}/SKILL.md` for the mandatory protocol). Include model, cost, resolution/aspect ratio, output format, exact prompt, and any reference images.

---

## Workflow

Follow the general workflow defined in `{baseDir}/SKILL.md` (pre-submission → payload → submit → poll → deliver). Image-specific notes:

- After parsing response: if `status` is `failed` or `rejected`, report error and stop immediately
- Include resolution, output format, and any reference images in the pre-submission summary

---

## Image Editing / Reference Images

**Accepted `image_url` formats:**
- HTTPS URLs: `"https://example.com/image.png"`
- Data URLs: `"data:image/jpeg;base64,<BASE64>"`
- Raw base64 strings (for text/LLM vision models only)
- **NOT accepted:** `file://` paths, local file paths — these cause `"Invalid base64 data"` errors

**Local file workflow:** When the user sends a local image:
1. Read the file and base64-encode it with python3
2. Write the full JSON payload (with data URL) to a temp file using python3
3. Submit using the secure header pattern from SKILL.md ("Image/Video requests")

Example:
```python
import base64, json, tempfile
with open("input.jpg", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()
payload = {"requests": [{"type": "image", "model": "gpt-image-2", "prompt": "...", "image_urls": ["data:image/jpeg;base64," + b64], "aspect_ratio": "1:1", "output_format": "png"}]}
with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
    json.dump(payload, f)
    tmpfile = f.name
```

**Size limits:** For images >100KB, always use the temp file approach. Inline `-d` with large base64 exceeds shell argument limits.

**Reference images count:** Check `models.md` for per-model reference image limits (e.g. `gpt-image-2` supports up to 16).

### ⚠️ Image Input Field — MUST USE `image_urls`

For **image** type requests, always use `image_urls` (a flat list of URLs/data URLs). Do NOT use `reference_assets` — that field is for **video** requests only and will be silently ignored on image requests, causing the model to generate without seeing your reference images.

```python
# CORRECT — image_urls (flat list)
payload = {"requests": [{"type": "image", "model": "gpt-image-2", "prompt": "...",
    "image_urls": ["data:image/jpeg;base64," + b64_1, "data:image/jpeg;base64," + b64_2]}]}

# WRONG — reference_assets (silently ignored on image requests)
payload = {"requests": [{"type": "image", "model": "gpt-image-2", "prompt": "...",
    "reference_assets": [{"kind": "source_image", "image_url": "..."}]}]}
```

### Image Input Compatibility Aliases

The API accepts multiple parameter names for image inputs:

- `image_urls`, `input_images`, `input_image_urls` — list of URLs (aliases)
- `image_url`, `input_image_url`, `input_image`, `input_image_b64` — single URL (aliases)

`image_urls` is the preferred/canonical form.

---

## Image Parameters

- `aspect_ratio`: `1:1`, `16:9`, `9:16`, `21:9`, etc. Default `1:1`. Use `auto` to match input image. Check `models.md` for per-model supported ratios.
- `output_format`: `png`, `jpeg`, `webp`. Default `png`.
- `is_fast`: `true` for cheaper half-resolution (imgnAI models only).
- `is_uhd`: `true` for UHD (imgnAI models only, overrides `is_fast`).

### Prompt Assist

On supported tag/booru-based image models only (e.g. `noob`, `ani`, `pony`, etc.), prompt assist fields (`use_assistant`, `prompt_assist`, or `use_prompt_assist`) let users write natural language that is automatically translated to tag-style prompts before dispatch.

**Note:** Only works on imgnAI tag-based models — not external/provider-hosted models.

---



## Delivery

Follow the delivery pattern defined in `{baseDir}/SKILL.md`. Deliver the generated image to the user with: model name, resolution, credits, dollar cost, description, and the full-res URL.

---

## Error Handling

Follow the error handling protocol defined in `{baseDir}/SKILL.md`.

---

*Part of the Katana skill. See SKILL.md for routing, general configuration, and llms.txt freshness checks.*

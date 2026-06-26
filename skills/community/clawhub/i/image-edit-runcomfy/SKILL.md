---
name: image-edit-runcomfy
displayName: "🫧 Image Edit — Pro Pack on RunComfy"
description: >
  Image edit on RunComfy. This image edit skill transforms an existing
  image — background swap, object removal, in-image text rewrite, mask-
  driven region replacement, or any other image edit task — by routing
  the image edit request to the right model in the RunComfy catalog.
  Image edit supports single-image edit, batch image edit (up to 20),
  multi-reference image edit, and mask-based image edit at up to 4K.
  Calls `runcomfy run <model>/edit` through the local RunComfy CLI.
  Triggers on "image edit", "edit image", "image-to-image", "i2i",
  "image editing", "swap background", "remove object", "rewrite
  headline", or any explicit ask to edit an image.
emoji: "🫧"
homepage: https://www.runcomfy.com
license: MIT
clawdis:
  requires:
    bins:
      - runcomfy
    env:
      - RUNCOMFY_TOKEN
    config:
      - ~/.config/runcomfy
---

# 🫧 Image Edit — Pro Pack on RunComfy

[runcomfy.com](https://www.runcomfy.com/?utm_source=clawhub&utm_medium=skill&utm_campaign=image-edit-runcomfy) · [docs](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=image-edit-runcomfy) · [Image edit models](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=image-edit-runcomfy)

**Image edit on RunComfy.** This skill is the canonical image edit entry point for the RunComfy Model API: give it a source image and an edit instruction, and it returns the edited image. Image edit on RunComfy means transforming an existing still — swap background, remove an object, rewrite a headline, mask-fill a region — without re-shooting.

## What "image edit" means here

Image edit is the task of taking a source image and producing a transformed image that preserves identity, framing, or layout where you want, while changing what you specify. Image edit is distinct from text-to-image (no input) and from image-to-video (output is a clip). Common image edit operations include:

- **Background image edit** — swap the background of a portrait, product, or scene while preserving the foreground identity.
- **Object-removal image edit** — remove cables, watermarks, distracting elements, leaving the rest of the image edit untouched.
- **Object-addition image edit** — add a new element (umbrella, sign, accessory) to an existing image edit subject.
- **Text-rewrite image edit** — replace an in-image headline, label, or signage, including multilingual image edit.
- **Mask-driven image edit** — fill or replace a specific masked region with strength control.
- **Multi-ref composition image edit** — combine subject from one image with scene/lighting from another.
- **Batch image edit** — apply the same image edit instruction across 1–20 inputs (SKU galleries, A/B variants).

This skill picks the right image edit endpoint for the user's intent and calls `runcomfy run <model>/edit` with the matching schema.

## When to use image edit on RunComfy

Pick image edit on RunComfy whenever:

- You have an **existing image** and want to **change** something about it — image edit is the right task.
- You want **identity-stable image edit** — the subject, brand, or product from the input must survive into the edited image.
- You're producing **batch image edit at scale** — SKU galleries, multi-language variant image edit, A/B testing.
- You need **mask-precise image edit** — region replacement, watermark removal, region fill.
- The user said "image edit", "edit image", "image-to-image", "swap the background", "remove the watermark", "rewrite the headline", or showed an image and asked to transform it — route here.

## Image edit routes

| User intent | Image edit model | Why |
|---|---|---|
| Default image edit — single or batch (up to 20), background swap, object remove/add | `google/nano-banana-2/edit` | Most flexible image edit; identity preservation; batch up to 20 |
| Multilingual in-image text rewrite, layout-precise image edit | `openai/gpt-image-2/edit` | Strongest in-image typography for image edit; multi-ref composition (up to 10) |
| Single-shot precise local image edit ("she's holding an orange umbrella") | `blackforestlabs/flux-1-kontext/pro/edit` | Single-instruction, single-ref, high-fidelity image edit |
| Mask-driven image edit (object removal, region fill, region replace) | `tongyi-mai/z-image/turbo/inpainting` | Mask-based image edit with strength control |

The agent reads this table, classifies the user's image edit intent, and picks the matching endpoint.

## Prerequisites

1. **RunComfy CLI** — `npm i -g @runcomfy/cli`
2. **RunComfy account** — `runcomfy login`.
3. **CI / containers** — set `RUNCOMFY_TOKEN=<token>`.

## Default image edit — Nano Banana Edit

The default image edit endpoint. Use for any general image edit task: background swap, object removal, object addition, batch image edit. Up to 20 inputs per image edit call, up to 4K resolution.

### Schema

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `prompt` | string | yes | — | Image edit instruction. Lead with preservation, then state the change. |
| `image_urls` | array | yes | — | 1–20 source images for the image edit. HTTPS URLs. |
| `number_of_images` | int | no | 1 | 1–4 image edit outputs per call. |
| `aspect_ratio` | enum | no | `auto` | `auto` follows input; lock for batch image edit consistency. |
| `resolution` | enum | no | `1K` | `0.5K` / `1K` / `2K` / `4K` for the image edit output. |
| `output_format` | enum | no | `png` | `png` / `jpeg` / `webp`. |
| `seed` | int | no | — | Reproducibility for image edit variants. |
| `enable_web_search` | bool | no | false | Web-grounded image edit (extra latency). |

### Invoke

**Background-swap image edit:**

```bash
runcomfy run google/nano-banana-2/edit \
  --input '{
    "prompt": "Keep the subject identity, pose, and clothing unchanged. Convert the background into a rainy neon cyberpunk street.",
    "image_urls": ["https://.../portrait.jpg"]
  }' \
  --output-dir <absolute/path>
```

**Batch image edit (lock aspect + resolution):**

```bash
runcomfy run google/nano-banana-2/edit \
  --input '{
    "prompt": "Replace the watermark in the bottom-right with the text \"AURA\" in clean white sans-serif. Keep everything else exactly as in the input.",
    "image_urls": ["https://.../sku-1.jpg", "https://.../sku-2.jpg", "https://.../sku-3.jpg"],
    "aspect_ratio": "1:1",
    "resolution": "1K"
  }' \
  --output-dir <absolute/path>
```

## Multilingual image edit — GPT Image 2 Edit

Use when the image edit involves rewriting in-image text (especially non-Latin scripts) or composing from multiple references with layout precision.

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `prompt` | string | yes | — | Image edit instruction; lead with preservation. |
| `images` | string[] | yes | — | Up to 10 reference images for the image edit. First is primary. |
| `size` | enum | no | `auto` | `auto`, `1024_1024`, `1024_1536`, `1536_1024`. |

**Multilingual text-rewrite image edit:**

```bash
runcomfy run openai/gpt-image-2/edit \
  --input '{
    "prompt": "Keep the photograph, layout, and brand mark exactly as in the input. Replace only the in-image headline. The new headline reads \"今日のおすすめ\" in bold Japanese kana, same position and font weight.",
    "images": ["https://.../poster-en.jpg"]
  }' \
  --output-dir <absolute/path>
```

**Multi-ref composition image edit:**

```bash
runcomfy run openai/gpt-image-2/edit \
  --input '{
    "prompt": "Compose subject from image 1 into the room from image 2. Match the lighting and color palette of image 2. Keep image 1 subject identity unchanged.",
    "images": ["https://.../subject.jpg", "https://.../room.jpg"]
  }' \
  --output-dir <absolute/path>
```

## Single-shot precise image edit — Flux Kontext Pro

Use when the image edit is a single declarative instruction on a single reference image — the most surgical image edit option.

| Field | Type | Required | Notes |
|---|---|---|---|
| `prompt` | string | yes | One declarative image edit instruction. |
| `image` | string | yes | Single source image for the image edit. |
| `aspect_ratio` | enum | no | Pick from supported W:H values. |
| `seed` | int | no | Reproducibility. |

```bash
runcomfy run blackforestlabs/flux-1-kontext/pro/edit \
  --input '{
    "prompt": "Keep the person'\''s face, pose, and clothing unchanged. Add an orange umbrella in her left hand and a slight smile.",
    "image": "https://.../portrait.jpg"
  }' \
  --output-dir <absolute/path>
```

## Mask-driven image edit — Z-Image Turbo Inpaint

Use when the image edit is constrained to a specific masked region — object removal, region fill, region replacement. Mask-driven image edit gives the cleanest results when you can supply a precise mask.

| Field | Type | Required | Notes |
|---|---|---|---|
| `prompt` | string | yes | What to fill / replace; preservation constraints for the unmasked surround. |
| `image` | string | yes | Source image for the image edit. |
| `mask_image` | string | yes | Grayscale mask URL (white = inpaint, black = preserve). |
| `strength` | float | no | 0.3–0.6 retouching image edit, 0.7–1.0 full replacement image edit. |
| `control_scale` | float | no | 0.6–0.9 typical. |
| `aspect_ratio` | enum | no | W:H output ratio. |
| `seed` | int | no | Reproducibility. |

**Object-removal image edit:**

```bash
runcomfy run tongyi-mai/z-image/turbo/inpainting \
  --input '{
    "prompt": "Remove overhead cables; preserve rooflines and sky gradient; thin clean sky.",
    "image": "https://.../street.jpg",
    "mask_image": "https://.../cables-mask.png",
    "strength": 0.5,
    "control_scale": 0.8
  }' \
  --output-dir <absolute/path>
```

**Region-replacement image edit:**

```bash
runcomfy run tongyi-mai/z-image/turbo/inpainting \
  --input '{
    "prompt": "Replace busy backdrop with smooth light gray studio paper; mask background only.",
    "image": "https://.../product.jpg",
    "mask_image": "https://.../bg-mask.png",
    "strength": 0.9
  }' \
  --output-dir <absolute/path>
```

## Prompting image edit — what works

Image edit prompts behave differently from text-to-image prompts. The source image already fixes most of the look — your image edit prompt should drive the change, not redescribe the source.

- **Lead with preservation goals.** `"Keep [identity / pose / framing / brand] unchanged. Then state the image edit change."` Tell the image edit model what NOT to change.
- **One image edit direction per call.** Compound image edits drift. Pick one bucket — background OR object OR text OR layout — per image edit call.
- **Spatial scope language.** "background only", "the left object", "upper-right quadrant" — image edit models honor concrete locations.
- **Quote in-image text exactly.** For text-rewrite image edit, put the literal characters in quotes. Name the script for non-Latin: "Japanese kana", "Cyrillic", "Arabic".
- **Number multi-refs in image edit prompts.** "Subject from image 1, lighting from image 2" — image edit models route cues correctly when refs are numbered.
- **Mask-edge softness.** For mask-driven image edit, a 1–3px blur on the mask edge blends cleaner than a sharp binary mask.
- **Iterate small.** Split compound image edit into multiple shorter passes; consistency is better across passes than within a single overstuffed prompt.

## Image edit FAQ

**What's the max batch size for image edit?** 20 inputs per call on the default image edit endpoint (Nano Banana Edit). Other image edit routes are single-input.

**What image formats does image edit accept?** JPEG, PNG, WebP. Source URLs must be publicly fetchable HTTPS.

**Does image edit preserve subject identity?** Yes — all four image edit routes are designed for identity preservation. Always state the goal: `"keep face identity unchanged"`.

**Can image edit rewrite text in non-Latin scripts?** Yes — route to GPT Image 2 Edit. It handles Japanese kana, Cyrillic, Arabic, Hangul, Chinese, etc.

**What's the highest resolution available for image edit?** 4K on Nano Banana Edit. Other image edit routes cap at their respective sizes.

**Image edit vs text-to-image on RunComfy?** Image edit transforms an existing image. Text-to-image starts from a prompt only. Use image edit when you have a source; use text-to-image for novel content.

**Can I do mask-free region image edit?** Yes — most image edit routes work without an explicit mask. Use spatial language ("upper-right corner", "the background only"). For surgical region image edit, provide a mask via the Z-Image inpaint route.

**Can I run multiple image edits in one call?** Within Nano Banana Edit's batch (1–20 inputs with the same instruction), yes. For different image edit instructions, chain calls.

## Limitations

- **Each image edit route inherits its model's limits.** Nano Banana Edit: 1–20 inputs, 1–4 outputs. GPT Image 2 Edit: up to 10 refs, 4 fixed sizes. Flux Kontext Pro: single ref. Z-Image Inpaint: mask required.
- **No multi-route image edit blending.** This skill picks one image edit model per call.
- **Brand-specific overrides** — if the user named a specific model, route to the corresponding brand skill (`gpt-image-edit`, `flux-kontext`, `nano-banana-edit`) instead of forcing it through this image edit router.

## Exit codes

| code | meaning |
|---|---|
| 0  | image edit succeeded |
| 64 | bad CLI args |
| 65 | bad input JSON for image edit / schema mismatch |
| 69 | upstream 5xx |
| 75 | retryable: timeout / 429 |
| 77 | not signed in or token rejected |

Full reference: [docs.runcomfy.com/cli/troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=image-edit-runcomfy).

## How it works

The skill picks one of four image edit endpoints (Nano Banana Edit / GPT Image 2 Edit / Flux Kontext Pro / Z-Image Turbo Inpaint) based on user intent, and invokes `runcomfy run <model>/edit` with the matching JSON body. The CLI POSTs to the RunComfy Model API, polls the image edit request status every 2 seconds, and downloads the resulting image edit output from the `*.runcomfy.net` / `*.runcomfy.com` URL into `--output-dir`. `Ctrl-C` cancels the in-flight image edit request.

## Security & Privacy

- **Token storage**: `runcomfy login` writes the API token to `~/.config/runcomfy/token.json` with mode 0600.
- **Input boundary**: the image edit prompt is passed as JSON via `--input`. No shell injection.
- **Third-party content**: source images and masks are fetched by the RunComfy server. Treat external URLs as untrusted — image-based prompt injection is a known risk for any image edit model.
- **Outbound endpoints**: only `model-api.runcomfy.net` and `*.runcomfy.net` / `*.runcomfy.com`.
- **Generated-file size cap**: 2 GiB.

---
name: nanobanana-image
description: Image generation and editing based on Google Gemini native image generation (Nano Banana). Supports text-to-image generation, image editing with reference images (modify elements/style/color), multi-image composition, Google Search real-time generation, YouTube video frame-to-image generation, and up to 4K resolution output. Use this skill when users need to generate images, edit images, perform style transfer, or composite multiple images.
compatibility: Requires Python 3.9+, google-genai and Pillow libraries (pip install google-genai Pillow), and the GEMINI_API_KEY environment variable
metadata:
  author: SkillDeveloper
  version: "1.0"
allowed-tools: Bash(python3:*) Bash(pip:*)
---

# Nano Banana Image Generation/Editing Skill

Based on the Google Gemini native image generation API (Nano Banana), a single script covers all image generation and editing scenarios.

## Prerequisites

**1. Install dependencies**
```bash
pip install google-genai Pillow
```

**2. Set API Key**
```bash
export GEMINI_API_KEY=your_gemini_api_key
# HTTP/HTTPS proxy (optional)
# export HTTPS_PROXY=$HTTPS_PROXY
# export HTTP_PROXY=$HTTP_PROXY
```

Get your API Key from [Google AI Studio](https://aistudio.google.com/apikey) or [Google Cloud Console](https://console.cloud.google.com/).

---

## 1. Text-to-Image Generation

Generate new images from text descriptions.

```bash
# Basic generation
python3 scripts/generate.py \
  --prompt "A photorealistic portrait of an elderly Japanese ceramicist in his workshop, golden hour lighting, 85mm lens bokeh"

# Specify resolution and aspect ratio
python3 scripts/generate.py \
  --prompt "A minimalist 16:9 wallpaper of a misty mountain lake at dawn" \
  --aspect-ratio 16:9 \
  --image-size 2K \
  --output wallpaper.png

# Use Pro model for professional assets
python3 scripts/generate.py \
  --model gemini-3-pro-image \
  --prompt "A modern minimalist logo for a coffee shop called 'The Daily Grind'. Bold sans-serif font, black and white, circular composition with a coffee bean motif." \
  --output logo.png

# Output image only, no text
python3 scripts/generate.py \
  --prompt "A kawaii sticker of a happy red panda with bamboo hat, white background, bold outlines" \
  --image-only \
  --output sticker.png
```

---

## 2. Image Editing

Provide a reference image and describe the modifications in text.

```bash
# Modify image elements
python3 scripts/generate.py \
  --prompt "Add a small knitted wizard hat on the cat's head. Match the soft lighting of the photo." \
  --images cat.jpg \
  --output cat_wizard.png

# Local editing (semantic inpainting)
python3 scripts/generate.py \
  --prompt "Change only the blue sofa to a vintage brown leather chesterfield sofa. Keep everything else unchanged." \
  --images living_room.jpg \
  --output living_room_edited.png

# Style transfer
python3 scripts/generate.py \
  --prompt "Transform this city street photo into Van Gogh's 'Starry Night' style. Preserve the composition but add swirling brushstrokes in deep blues and bright yellows." \
  --images city.jpg \
  --output city_van_gogh.png

# Sketch to rendered image
python3 scripts/generate.py \
  --prompt "Turn this rough pencil sketch into a polished concept car photo in a showroom. Keep the sleek lines, add metallic blue paint and neon rim lighting." \
  --images car_sketch.jpg \
  --output car_rendered.png
```

---

## 3. Multi-Image Composition (up to 14 images)

Provide multiple reference images to compose new scenes or maintain character/product consistency.

```bash
# People composition (maintain character features)
python3 scripts/generate.py \
  --prompt "An office group photo of these people making funny faces. Natural lighting." \
  --images person1.jpg person2.jpg person3.jpg person4.jpg \
  --aspect-ratio 5:4 \
  --image-size 2K \
  --output group_photo.png

# Product + model composition (high-fidelity detail retention)
python3 scripts/generate.py \
  --prompt "Create a professional e-commerce fashion photo. The woman wears the blue floral dress from the first image. Full-body shot, outdoor lighting." \
  --images dress.jpg model.jpg \
  --output ecommerce.png

# Logo placement
python3 scripts/generate.py \
  --prompt "Put this logo on the woman's black t-shirt. Logo naturally printed on fabric following folds. Woman's face unchanged." \
  --images woman.jpg logo.png \
  --output woman_with_logo.png
```

---

## 4. Google Search Real-Time Generation

Generate images based on real-time search information (weather charts, news graphics, sports scores, etc.).

```bash
# Weather visualization
python3 scripts/generate.py \
  --prompt "Visualize the current weather forecast for the next 5 days in Tokyo as a clean modern weather chart. Add clothing suggestions for each day." \
  --search \
  --aspect-ratio 16:9 \
  --output weather_tokyo.png

# News graphics (better results with Pro model)
python3 scripts/generate.py \
  --model gemini-3-pro-image \
  --prompt "Make a stylish graphic of last night's Champions League match result." \
  --search \
  --output match_result.png

# Image Search (gemini-3.1-flash-image only)
python3 scripts/generate.py \
  --prompt "A detailed painting of a resplendent quetzal bird in its natural habitat. Create a 3:2 wallpaper with a natural gradient background." \
  --image-search \
  --aspect-ratio 3:2 \
  --output quetzal.png
```

---

## 5. Video Frame to Image (gemini-3.1-flash-image only)

Extract visual themes from YouTube videos to generate new images (posters, thumbnails, infographics, etc.).

```bash
# Generate video poster
python3 scripts/generate.py \
  --prompt "Generate a cinematic movie poster that captures the key themes of this video. Bold title typography." \
  --video "https://www.youtube.com/watch?v=UTdfxFyOQTI" \
  --aspect-ratio 9:16 \
  --output poster.png
```

---

## 6. High Thinking Level Generation (Complex Scenes)

```bash
# Enable high-quality thinking and save intermediate thought images
python3 scripts/generate.py \
  --prompt "A futuristic city built inside a giant glass bottle floating in space, photorealistic, intricate details." \
  --thinking high \
  --show-thoughts \
  --image-size 2K \
  --output city_bottle.png
```

---

## Parameter Reference

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--prompt` | Text prompt (required) | - |
| `--model` | Model ID | `gemini-3.1-flash-image` |
| `--output` | Output file path | `output.png` |
| `--image-only` | Return image only (no text description) | Off |
| `--aspect-ratio` | Aspect ratio (e.g. `16:9` `9:16` `1:1`) | 1:1 |
| `--image-size` | Resolution (`512`/`1K`/`2K`/`4K`) | 1K |
| `--images` | Reference image file list (space-separated, up to 14) | None |
| `--video` | YouTube video URL | None |
| `--search` | Enable Google Web Search | Off |
| `--image-search` | Enable Google Image Search (3.1 Flash only) | Off |
| `--thinking` | Thinking level `minimal`/`high` | minimal |
| `--show-thoughts` | Save intermediate thought images | Off |

---

## Model Selection Guide

| Scenario | Recommended Model |
|----------|-------------------|
| Everyday image generation and editing | `gemini-3.1-flash-image` (default) |
| Professional logos, commercial ads, complex layouts | `gemini-3-pro-image` |
| High-concurrency batch generation, lower quality requirements | `gemini-2.5-flash-image` |
| Requires Image Search / video input | `gemini-3.1-flash-image` (exclusive) |

For more parameter details, see [references/models-and-params.md](references/models-and-params.md).

---

## Notes

- All generated images contain invisible **SynthID watermarks**
- **Transparent backgrounds** are not supported; post-process if needed
- `--image-size` requires uppercase K (`1K` is correct, `1k` will cause an error)
- Multiple image outputs are automatically saved as `output_1.png`, `output_2.png`, etc.
- Comply with the [Google Generative AI Use Policy](https://policies.google.com/terms/generative-ai/use-policy)

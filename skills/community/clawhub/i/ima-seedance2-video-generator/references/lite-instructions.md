# IMA Seedance 2.0 Lite Instructions

Use these concise rules for smaller or compatibility models.

Canonical lite target models:

- `gpt-4o-mini`
- `o4-mini`
- `claude-3-5-haiku-latest`
- `gemini-2.5-flash-lite`
- `doubao-1.5-lite-32k`
- `deepseek-chat`
- `glm-4.7-flash`
- `qwen-flash`

## Core Rules

1. Use exact model IDs only:
   - `ima-pro`
   - `ima-pro-fast`

2. Infer `task_type` in this order:
   - Any video or audio input: `reference_image_to_video`
   - Explicit first-last-frame intent with 2+ images: `first_last_frame_to_video`
   - 2+ images without explicit first-last-frame intent: `reference_image_to_video`
   - 1 image: `image_to_video`
   - Text only: `text_to_video`

3. Keep parameter formats strict:
   - `duration`: number only, e.g. `15`
   - `aspect_ratio`: use `16:9`, `9:16`, `1:1`
   - `resolution`: use API-supported values exactly, e.g. `720p`, `1080p`
   - `--extra-params`: JSON string only

4. Use this command shape:

```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "[user prompt]" \
  --model-id [ima-pro or ima-pro-fast] \
  [--task-type explicit_type_if_needed] \
  [--input-images URL1 URL2 ...] \
  [--reference-image URL1 URL2 ...] \
  [--extra-params '{"duration": 15, "aspect_ratio": "9:16"}']
```

5. For OpenClaw / IM integrations, keep event-stream-safe output enabled:
   - `IMA_STDOUT_MODE=events`

## Quick Examples

Text to video:

```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "a cinematic city skyline at sunset" \
  --model-id ima-pro
```

Single image:

```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "camera slowly zooms in" \
  --input-images https://example.com/photo.jpg \
  --model-id ima-pro-fast
```

Multiple images without explicit first-last-frame intent:

```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "keep the same character consistent across shots" \
  --input-images https://example.com/shot1.jpg https://example.com/shot2.jpg \
  --model-id ima-pro
```

Image + video references:

```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "keep the product identity while extending the original motion" \
  --reference-image https://example.com/product.jpg \
  --reference-video https://example.com/clip.mp4 \
  --model-id ima-pro-fast
```

Image + audio references:

```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "generate visuals matching the narration mood while preserving the character look" \
  --reference-image https://example.com/character.jpg \
  --reference-audio https://example.com/narration.mp3 \
  --model-id ima-pro-fast
```

Image + video + audio references:

```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "create a polished 15-second ad using the product image, motion reference, and narration rhythm" \
  --reference-image https://example.com/product.jpg \
  --reference-video https://example.com/clip.mp4 \
  --reference-audio https://example.com/narration.mp3 \
  --model-id ima-pro-fast \
  --extra-params '{"duration": 15, "aspect_ratio": "9:16", "audio": true}'
```

Reference video:

```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "extend this shot with cinematic motion" \
  --reference-video https://example.com/clip.mp4 \
  --model-id ima-pro-fast
```

Reference audio:

```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "generate visuals matching the narration mood" \
  --reference-audio https://example.com/narration.mp3 \
  --model-id ima-pro-fast
```

Video + audio references:

```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "generate new visuals that follow the source motion and narration pacing" \
  --reference-video https://example.com/clip.mp4 \
  --reference-audio https://example.com/narration.mp3 \
  --model-id ima-pro-fast
```

Explicit first-last-frame mode:

```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --task-type first_last_frame_to_video \
  --prompt "smooth transition between two keyframes" \
  --input-images https://example.com/first.jpg https://example.com/last.jpg \
  --model-id ima-pro-fast
```

# Image Scenarios

Supported scenarios:

- prompt-only image generation
- single-image stylization
- reference-based continuity when the user supplies the prior image
- local image upload followed by `image_to_image`

## Text To Image

### 1. Square Social Post

Use when you want a fast first result for a feed post, thumbnail draft, or cover concept.

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --size 1k \
  --extra-params '{"aspect_ratio":"1:1"}' \
  --prompt "minimal coffee brand social post, warm light, product centered" \
  --output-json
```

### 2. Wide Poster Or Thumbnail

Use when the output needs a horizontal layout for a banner, slide cover, or video thumbnail.

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --size 2k \
  --extra-params '{"aspect_ratio":"16:9"}' \
  --prompt "cinematic sci-fi movie poster, dramatic lighting, title-safe composition" \
  --output-json
```

### 3. Multi-Variant Concept Exploration

Use when you want several quick concepts before choosing one direction to refine.

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --size 1k \
  --extra-params '{"n":4}' \
  --prompt "packaging concept for a premium matcha brand, clean modern layout" \
  --output-json
```

## Image To Image

### 4. Stylize An Existing Photo

Use when the user already has one image and wants a clear style shift without changing the subject.

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type image_to_image \
  --input-images ./example.png \
  --prompt "turn this into an oil painting with visible brush texture" \
  --output-json
```

### 5. Product-Photo Cleanup

Use when the source image is a rough local shot and the goal is a cleaner ad-style render.

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type image_to_image \
  --input-images ./product-shot.jpg \
  --size 1k \
  --prompt "convert this into a clean studio product photo on a white background" \
  --output-json
```

If you need to pin the model manually, fetch a live `model_id` first:

```bash
MODEL_ID="$(python3 scripts/ima_runtime_cli.py --task-type image_to_image --list-models --output-json | python3 -c 'import json,sys; print(json.load(sys.stdin)[0][\"model_id\"])')"
python3 scripts/ima_runtime_cli.py \
  --task-type image_to_image \
  --model-id "$MODEL_ID" \
  --input-images ./product-shot.jpg \
  --size 1k \
  --prompt "convert this into a clean studio product photo on a white background" \
  --output-json
```

### 6. Reference-Based Continuity

Use when the user wants to keep the same character, object, or composition anchor from a previous image.

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type image_to_image \
  --input-images ./previous-frame.png \
  --extra-params '{"aspect_ratio":"16:9"}' \
  --prompt "keep the same character and costume, place them in a rainy neon street at night" \
  --output-json
```

Out of scope:

- mask editing
- multi-role image inputs with distinct semantic slots
- non-image media generation

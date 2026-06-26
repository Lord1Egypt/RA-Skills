# AI Image Module

Generate images from text prompts or edit existing images with AI-powered models.

## Supported Task Types

| Type | Description | Required Params |
|------|-------------|-----------------|
| `text2image` | **Text-to-Image** — generate images from a text prompt | `--model`, `--prompt`, `--aspect-ratio` |
| `image_edit` | **Image Edit** — edit images with prompt + reference images | `--model`, `--prompt`, `--aspect-ratio`, `--input-images` |

## Subcommands

| Subcommand | When to use | Polls? |
|------------|-------------|--------|
| `run` | **Default.** New request, start to finish | Yes — waits until done |
| `submit` | Batch: fire multiple tasks without waiting | No — exits immediately |
| `query` | Recovery: resume polling a known `taskId` | Yes — waits until done |
| `list-models` | Check models, constraints, and supported ratios | No |
| `estimate-cost` | Estimate credit cost before running | No |

## Usage

```bash
python {baseDir}/scripts/ai_image.py <subcommand> --type <text2image|image_edit> [options]
```

## Examples

### List Models

```bash
python {baseDir}/scripts/ai_image.py list-models --type text2image
python {baseDir}/scripts/ai_image.py list-models --type image_edit --json
```

### Text-to-Image

Fixed-price model (no resolution):

```bash
python {baseDir}/scripts/ai_image.py run \
  --type text2image \
  --model "Nano Banana" \
  --prompt "A watercolor painting of a cat" \
  --aspect-ratio "1:1"
```

Required resolution：

```bash
python {baseDir}/scripts/ai_image.py run \
  --type text2image \
  --model "Nano Banana 2" \
  --prompt "A futuristic city skyline at dusk, neon lights reflected on wet streets" \
  --aspect-ratio "16:9" \
  --resolution "2K" \
  --count 2
```

### Image Edit

Fixed-price model (no resolution):

```bash
python {baseDir}/scripts/ai_image.py run \
  --type image_edit \
  --model "Nano Banana" \
  --prompt "Change the background to a snowy mountain landscape" \
  --aspect-ratio "auto" \
  --input-images photo.jpg
```

Required resolution:

```bash
python {baseDir}/scripts/ai_image.py run \
  --type image_edit \
  --model "Nano Banana 2" \
  --prompt "Blend the style of both images" \
  --aspect-ratio "1:1" \
  --resolution "2K" \
  --input-images photo.jpg \
  --count 2
```

### Cost Estimation

```bash
python {baseDir}/scripts/ai_image.py estimate-cost \
  --type text2image --model "Nano Banana" --resolution "2K" --count 2
```

### Download Results

```bash
python {baseDir}/scripts/ai_image.py run \
  --type text2image --model "Nano Banana" \
  --prompt "Northern lights" --aspect-ratio "16:9" --resolution "2K" \
  --output-dir ./results
```

## Options

| Option | Description                                                                                                                                  |
|--------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `--type` | `text2image` or `image_edit` (required)                                                                                                      |
| `--model` | Model **display name** (required)                                                                                                            |
| `--prompt` | Text prompt (required)                                                                                                                       |
| `--aspect-ratio` | Aspect ratio (required), e.g. `"16:9"`, `"1:1"`                                                                                              |
| `--resolution` | `"1K"`, `"2K"`, `"4K"` — model-dependent                                                                                           |
| `--count` | Number of images (1-4, default: 1)                                                                                                           |
| `--input-images` | Reference image url or local paths, space-separated (image_edit only). E.g. `--input-images https://photo.jpg` or `--input-images photo.jpg` |
| `--timeout` | Max polling time (default: 600)                                                                                                              |
| `--interval` | Polling interval (default: 30)                                                                                                               |
| `--output-dir` | Download results to directory                                                                                                                |
| `--json` | Full JSON response (not used by default; only when the user explicitly requests raw JSON output)                                             |
| `-q, --quiet` | Suppress status messages                                                                                                                     |

## Model Recommendation

> **Nano Banana is the top recommendation for all image tasks.**
> Best overall quality, 14 aspect ratios, up to 4K, 14 reference images for editing.

| Use Case | Recommended Models                          | Why |
|----------|---------------------------------------------|-----|
| **Best overall (default)** | **Nano Banana**                             | Strongest all-round model |
| **Budget** | Nano Banana (10/img), Seedream 4.5 (10/img) | Lowest cost |
| **No-resolution simplicity** | Nano Banana                 | No resolution param needed |

**Defaults:**
- text2image → `Nano Banana`
- image_edit → `Nano Banana`

## Key Notes

- `aspectRatio` is always required;
- `resolution` is required for some models, forbidden for others — check via `list-models`
- **Imagen 4** is only available for text2image, not image_edit

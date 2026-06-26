# Gemini Image Generation

Generate images from text descriptions or modify existing images using Google's Gemini models via the [Wisdom Gate](https://wisgate.ai) API.

## Features

- **Text-to-Image** — Generate images from natural language prompts
- **Image-to-Image** — Modify, restyle, or combine existing images (up to 14 input images)
- **Multi-Turn Refinement** — Iteratively refine images with conversation history
- **Smart Model Selection** — Automatically picks the best model based on your requirements
- **Flexible Output** — Multiple aspect ratios (14 options) and resolutions up to 4K

## Prerequisites

- Python 3.8+
- `requests` library (`pip install requests`)
- A valid [Wisdom Gate](https://wisgate.ai) API key

## Setup

Set your API key as an environment variable:

```bash
export WISGATE_KEY="your_api_key_here"
```

## Quick Start

### Text-to-Image

```bash
python scripts/generate_image.py "A serene mountain landscape at sunset"
```

### Image-to-Image

```bash
python scripts/generate_image.py "make it look like a watercolor painting" --input photo.jpg
```

### Multi-Turn Refinement

```bash
# Start a new conversation
python scripts/refine_image.py "Create a vibrant infographic about photosynthesis" --reset

# Refine the result
python scripts/refine_image.py "Make it more colorful and add more visual elements"

# Refine further
python scripts/refine_image.py "Add labels to each component"
```

## Models

| Model | Alias | Description | Resolutions | Cost |
|-------|-------|-------------|-------------|------|
| gemini-2.5-flash-image | `nano-banana` | Cheapest, fast & economical | 1K, 2K | 💰 Low |
| gemini-3.1-flash-image-preview | `nano-banana-2` | Best value, recommended | 0.5K, 1K, 2K, 4K | 💰💰 Medium |
| gemini-3-pro-image-preview | `nano-banana-pro` | Best performance, high quality | 1K, 2K, 4K | 💰💰💰 High |

### Smart Model Selection (Default)

When no `--model` is specified, the best model is chosen automatically:

| Scenario | Selected Model | Reason |
|----------|---------------|--------|
| Multiple input images (>1) | Nano Banana Pro | Best multi-image quality |
| 4K resolution | Nano Banana 2 (or Pro with `--quality`) | 4K support required |
| 0.5K resolution | Nano Banana 2 | Only supported model |
| `--quality` flag | Nano Banana Pro | User prefers quality |
| Everything else | Nano Banana 2 | Best balance of cost & quality |

Override with `--model`:

```bash
python scripts/generate_image.py "prompt" --model nano-banana      # Cheapest
python scripts/generate_image.py "prompt" --model nano-banana-2    # Best value
python scripts/generate_image.py "prompt" --model nano-banana-pro  # Best quality
```

## Usage Reference

### `generate_image.py`

```
usage: generate_image.py [-h] [--input INPUT [INPUT ...]] [--aspect-ratio RATIO]
                         [--size SIZE] [--output PATH] [--model MODEL] [--quality]
                         prompt
```

| Argument | Description | Default |
|----------|-------------|---------|
| `prompt` | Text description or modification instruction | *(required)* |
| `--input` | Input image path(s) for image-to-image (up to 14) | — |
| `--aspect-ratio` | Aspect ratio (text-to-image only): `1:1`, `16:9`, `9:16`, `21:9`, `4:3`, `3:4`, `5:4`, `4:5`, `2:3`, `3:2`, `1:4`, `4:1`, `1:8`, `8:1` | `1:1` |
| `--size` | Resolution (text-to-image only): `0.5K`, `1K`, `2K`, `4K` | `1K` |
| `--output` | Output file path | `generated_image.png` |
| `--model` | Force a specific model | Auto-select |
| `--quality` | Prioritize quality over cost | `false` |

### `refine_image.py`

```
usage: refine_image.py [-h] [--history FILE] [--output PATH] [--reset]
                       [--model MODEL] [--quality]
                       prompt
```

| Argument | Description | Default |
|----------|-------------|---------|
| `prompt` | Refinement instruction or initial prompt | *(required)* |
| `--history` | Conversation history JSON file | `conversation.json` |
| `--output` | Output file path | `refined_image.png` |
| `--reset` | Reset conversation and start fresh | `false` |
| `--model` | Force a specific model | Auto-select |
| `--quality` | Prioritize quality over cost | `false` |

## Examples

### Text-to-Image

```bash
# High quality, widescreen, 4K
python scripts/generate_image.py "Futuristic city skyline" \
  --quality --aspect-ratio 16:9 --size 4K

# Budget mode with cheapest model
python scripts/generate_image.py "Simple illustration" \
  --model nano-banana --size 2K

# Portrait orientation
python scripts/generate_image.py "Portrait of a wise old wizard" \
  --aspect-ratio 9:16 --model nano-banana-pro
```

### Image-to-Image

```bash
# Style transfer
python scripts/generate_image.py "Van Gogh style" --input portrait.png --quality

# Combine multiple reference images
python scripts/generate_image.py "group photo of these people at a party" \
  --input person1.jpg person2.jpg person3.jpg person4.jpg

# Budget multi-image
python scripts/generate_image.py "combine these items" \
  --input item1.jpg item2.jpg --model nano-banana-2
```

### Multi-Turn Refinement

```bash
# Turn 1: Generate initial image
python scripts/refine_image.py "Create a vibrant infographic about photosynthesis" --reset

# Turn 2: Refine with quality priority
python scripts/refine_image.py "Make it more colorful and add more visual elements" --quality

# Turn 3: Further refinement with specific model
python scripts/refine_image.py "Add labels to each component" --model nano-banana-pro

# Start over with a new conversation
python scripts/refine_image.py "Completely new prompt" --reset
```

## API Details

**Endpoint:**
```
https://api.wisgate.ai/v1beta/models/{model}:generateContent
```

**Authentication** (either header works):
```
x-goog-api-key: YOUR_WISGATE_KEY
Authorization: Bearer YOUR_WISGATE_KEY
```

## Notes

- Images are returned as base64-encoded PNG data
- Text-to-image includes Google Search grounding by default for better results
- Image-to-image supports JPEG, PNG, and WebP input formats
- Aspect ratio and size parameters only apply to text-to-image generation
- Multi-image recommendation: up to 6 objects or up to 5 people for best quality
- Conversation history is saved to JSON and can be resumed across sessions

## License

MIT

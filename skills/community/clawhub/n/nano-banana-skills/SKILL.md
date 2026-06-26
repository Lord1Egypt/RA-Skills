---
name: gemini-image
description: Generate images using Google Gemini models (Nano Banana 2 / gemini-3-pro-image-preview). Use when the user asks to create, generate, or make an image, picture, photo, or visual from a text description. Also supports image-to-image generation (modify/edit existing images). Supports multiple aspect ratios (1:1, 16:9, 9:16, 4:3, 3:4) and resolutions up to 4K. Triggers on phrases like "generate an image", "create a picture", "make me a photo", "draw", "visualize", "edit this image", "modify this picture", or any request to produce or transform visual content.
---

# Gemini Image Generation

Generate images from text descriptions or modify existing images using Google's Gemini models via the Wisdom Gate API.

## Quick Usage

### Text-to-Image

```bash
python scripts/generate_image.py "your prompt here" [--aspect-ratio RATIO] [--size SIZE] [--output PATH]
```

### Image-to-Image (Single or Multiple)

```bash
# Single image
python scripts/generate_image.py "modification prompt" --input input.jpg [--output PATH]

# Multiple images (up to 14)
python scripts/generate_image.py "combine these people in an office photo" --input person1.jpg person2.jpg person3.jpg
```

### Multi-Turn Refinement

```bash
# First turn: Generate initial image (auto-selects Nano Banana 2)
python scripts/refine_image.py "Create a vibrant infographic about photosynthesis" --reset

# Second turn: Refine with quality priority
python scripts/refine_image.py "Make it more colorful and add more visual elements" --quality

# Third turn: Further refinement with specific model
python scripts/refine_image.py "Add labels to each component" --model nano-banana-pro

# Start a new conversation with budget model
python scripts/refine_image.py "New prompt here" --reset --model nano-banana
```

**Parameters (generate_image.py):**
- `prompt` (required): Text description of the image to generate or modification to apply
- `--input`: Input image path(s) for image-to-image generation - supports up to 14 images (optional)
- `--aspect-ratio`: Image aspect ratio (text-to-image only) - `1:1` (default), `16:9`, `9:16`, `21:9`, `4:3`, `3:4`, `5:4`, `4:5`, `2:3`, `3:2`, `1:4`, `4:1`, `1:8`, `8:1`
- `--size`: Image resolution (text-to-image only) - `0.5K`, `1K` (default), `2K`, `4K`
- `--output`: Output file path (default: `generated_image.png`)
- `--model`: Force specific model - `nano-banana`, `nano-banana-2`, `nano-banana-pro` (auto-select if not specified)
- `--quality`: Prioritize quality over cost (uses Nano Banana Pro when possible)

**Parameters (refine_image.py):**
- `prompt` (required): Refinement instruction or initial prompt
- `--history`: Conversation history file (default: `conversation.json`)
- `--output`: Output file path (default: `refined_image.png`)
- `--reset`: Reset conversation history and start fresh
- `--model`: Force specific model - `nano-banana`, `nano-banana-2`, `nano-banana-pro` (auto-select if not specified)
- `--quality`: Prioritize quality over cost (uses Nano Banana Pro)

**Environment:**
- Requires `WISGATE_KEY` environment variable
- Alternative: Set `Authorization: Bearer YOUR_KEY` header (modify script if needed)

## Examples

### Text-to-Image

```bash
# Basic generation (auto-selects Nano Banana 2 for best balance)
python scripts/generate_image.py "A serene mountain landscape at sunset"

# High quality mode (uses Nano Banana Pro)
python scripts/generate_image.py "Futuristic city skyline" --quality --aspect-ratio 16:9 --size 4K

# Budget mode (force cheapest model)
python scripts/generate_image.py "Simple illustration" --model nano-banana --size 2K

# Portrait orientation with specific model
python scripts/generate_image.py "Portrait of a wise old wizard" --aspect-ratio 9:16 --model nano-banana-pro
```

### Image-to-Image

```bash
# Modify an existing image (auto-selects appropriate model)
python scripts/generate_image.py "make it look like a watercolor painting" --input photo.jpg

# Style transfer with quality priority
python scripts/generate_image.py "Van Gogh style" --input portrait.png --quality

# Multiple reference images (auto-uses Nano Banana Pro for best quality)
python scripts/generate_image.py "group photo of these people at a party" --input person1.jpg person2.jpg person3.jpg person4.jpg

# Budget multi-image (force cheaper model)
python scripts/generate_image.py "combine these items" --input item1.jpg item2.jpg --model nano-banana-2
```

## Models

| Model | Alias | Description | Resolutions | Cost |
|-------|-------|-------------|-------------|------|
| **gemini-2.5-flash-image** | `nano-banana` | Cheapest, fast & economical | 1K, 2K | 💰 Low |
| **gemini-3.1-flash-image-preview** | `nano-banana-2` | Best value, recommended | 0.5K, 1K, 2K, 4K | 💰💰 Medium |
| **gemini-3-pro-image-preview** | `nano-banana-pro` | Best performance, high quality | 1K, 2K, 4K | 💰💰💰 High |

**Smart Model Selection (Default Behavior):**
- Multiple image input (>1 image) → Automatically uses Nano Banana Pro (best quality)
- 4K resolution → Nano Banana 2 or Pro (depends on `--quality` flag)
- 0.5K resolution → Nano Banana 2 (only supported model)
- Other scenarios → Nano Banana 2 (best value)

**Manual Model Override:**
Use the `--model` parameter to force a specific model:
```bash
python scripts/generate_image.py "prompt" --model nano-banana  # Cheapest
python scripts/generate_image.py "prompt" --model nano-banana-2  # Best value
python scripts/generate_image.py "prompt" --model nano-banana-pro  # Best quality
```

**Quality Priority Mode:**
Use the `--quality` flag to prefer Nano Banana Pro when possible:
```bash
python scripts/generate_image.py "prompt" --quality
```

**API Endpoint Format:**
```
https://api.wisgate.ai/v1beta/models/{model}:generateContent
```

**Authentication:**
- Header: `x-goog-api-key: YOUR_WISGATE_KEY`
- Or: `Authorization: Bearer YOUR_WISGATE_KEY`

## Workflow

### One-Shot Generation (generate_image.py)
1. Check if `WISDOM_GATE_KEY` is set in environment
2. For text-to-image: Run script with prompt and desired parameters
3. For image-to-image: Run script with prompt and `--input` pointing to the source image(s)
4. Save the generated image to the specified output path
5. Show the image to the user or confirm the save location

### Multi-Turn Refinement (refine_image.py)
1. First turn: Use `--reset` to start a new conversation
2. Subsequent turns: Run without `--reset` to refine based on previous results
3. Conversation history is automatically saved to `conversation.json` (or custom path)
4. Each turn generates a new image based on the full conversation context
5. Use `--reset` again to start a completely new conversation

## Notes

- Images are returned as base64-encoded PNG data
- Text-to-image includes Google Search grounding by default for better results
- Image-to-image supports JPEG, PNG, and WebP input formats
- Aspect ratio and size parameters only apply to text-to-image generation
- **Multi-image limits**: Up to 14 reference images total (recommended: up to 6 objects or up to 5 people for best quality)
- **Force image output**: Set `responseModalities: ["IMAGE"]` (without TEXT) to ensure image generation
- **Model differences**: Different models support different resolutions and aspect ratios - consult the table above
- **Multi-turn editing**: Use `refine_image.py` for iterative refinement with conversation history
- **Conversation persistence**: History is saved to JSON file and can be resumed across sessions
- **Safety settings**: API supports content filtering via `safetySettings` parameter (not exposed in scripts by default)
- **Token usage**: Check `usageMetadata` in API response for prompt/candidate/total token counts
- **Finish reasons**: API returns `finishReason` (STOP, MAX_TOKENS, SAFETY, RECITATION, OTHER)

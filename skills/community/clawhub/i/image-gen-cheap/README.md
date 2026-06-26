# Image Gen Cheap

Low-cost image generation and editing via LaoZhang API. Starting at **$0.01/image**.

## Quick Start

### 1. Get API Token

Register at [https://api.laozhang.ai/register/?aff_code=lfa0](https://api.laozhang.ai/register/?aff_code=lfa0) and get your token from the dashboard.

Save your token:
```bash
echo "sk-your-token" > ~/.laozhang_api_token
```

### 2. Text-to-Image

```bash
# Use default model (sora_image, $0.01/image)
python scripts/generate_image.py "A cute cat playing in a garden"

# Specify aspect ratio (2:3 portrait / 3:2 landscape / 1:1 square)
python scripts/generate_image.py "Sunset beach scene" --ratio 3:2

# Save to specific path
python scripts/generate_image.py "A cute puppy" --output dog.png

# Use different model
python scripts/generate_image.py "Futuristic city" --model gpt-4o-image
```

### 3. Image Editing

```bash
# Basic editing
python scripts/edit_image.py "https://example.com/cat.jpg" "Change the cat's fur to rainbow colors"

# Use preset style
python scripts/edit_image.py "https://example.com/photo.jpg" --style cartoon

# Multi-image fusion
python scripts/edit_image.py "https://a.jpg,https://b.jpg" "Merge these two images"
```

## Models & Pricing

### Text-to-Image Models

| Model | Model ID | Price | Format |
|-------|----------|-------|--------|
| Sora Image | sora_image | **$0.01/img** | URL |
| GPT-4o Image | gpt-4o-image | **$0.01/img** | URL |
| Nano Banana | gemini-2.5-flash-image | $0.025/img | base64 |
| Nano Banana2 | gemini-3.1-flash-image-preview | $0.03/img | base64 |
| Nano Banana Pro | gemini-3-pro-image-preview | $0.05/img | base64 |

### Image Editing Models

| Model | Model ID | Price | Format |
|-------|----------|-------|--------|
| GPT-4o Image | gpt-4o-image | **$0.01/img** | URL |
| Sora Image | sora_image | **$0.01/img** | URL |
| Nano Banana | gemini-2.5-flash-image | $0.025/img | base64 |

**Recommended**: Defaults to `sora_image` (text-to-image) and `gpt-4o-image` (editing) - both $0.01/image with URL output.

## Preset Styles

- cartoon - Disney cartoon style
- oil-painting - Classic oil painting style
- ink-wash - Chinese ink wash painting style
- cyberpunk - Neon light effects
- sketch - Pencil sketch style
- watercolor - Watercolor painting style

## CLI Options

### generate_image.py

```
--model, -m    Model to use (default: sora_image)
--ratio, -r    Aspect ratio: 2:3/3:2/1:1 (sora_image only)
--output, -o   Save image to specified path
--token, -t    Specify API token
--verbose, -v  Show detailed information
--json         Output full API response
--no-save      Don't save image (show URL only)
```

### edit_image.py

```
--model, -m    Model to use (default: gpt-4o-image)
--style, -s    Preset style (cartoon/oil-painting/ink-wash/cyberpunk/sketch/watercolor)
--output, -o   Save image to specified path
--token, -t    Specify API token
--verbose, -v  Show detailed information
--json         Output full API response
--no-save      Don't save image (show URL only)
```

## Dependencies

```bash
pip install requests
```

## Notes

1. URL-returning models (sora_image / gpt-4o-image) can be directly sent to platforms like Feishu
2. Base64-returning models are automatically decoded and saved locally
3. Recommended rate limit: 10 requests/minute

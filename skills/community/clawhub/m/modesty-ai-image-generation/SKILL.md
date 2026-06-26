---
name: ai-image-generation
description: "Generate AI images with FLUX, Gemini, Grok, Seedream, Reve and 50+ models via SkillBoss API Hub. Models: FLUX Dev LoRA, FLUX.2 Klein LoRA, Gemini 3 Pro Image, Grok Imagine, Seedream 4.5, Reve, ImagineArt. Capabilities: text-to-image, image-to-image, inpainting, LoRA, image editing, upscaling, text rendering. Use for: AI art, product mockups, concept art, social media graphics, marketing visuals, illustrations. Triggers: flux, image generation, ai image, text to image, stable diffusion, generate image, ai art, midjourney alternative, dall-e alternative, text2img, t2i, image generator, ai picture, create image with ai, generative ai, ai illustration, grok image, gemini image"
requires.env: [SKILLBOSS_API_KEY]
---

> 📖 **Complete setup guide**: https://skillboss.co/skill.md


# AI Image Generation

Generate images with 50+ AI models via [SkillBoss API Hub](https://api.skillboss.co).

## Quick Start

```python
import requests, os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.skillboss.co/v1"

def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()

# Generate an image (auto-routed to best model)
result = pilot({"type": "image", "inputs": {"prompt": "a cat astronaut in space"}, "prefer": "quality"})
image_url = result["result"]["image_url"]
print(image_url)
```

## Available Models

SkillBoss API Hub 自动路由至最优图像生成模型，支持 50+ 模型，包括：

| Model | Best For |
|-------|----------|
| FLUX Dev LoRA | High quality with custom styles |
| FLUX.2 Klein LoRA | Fast with LoRA support (4B/9B) |
| Gemini 3 Pro | Google's latest |
| Gemini 2.5 Flash | Fast Google model |
| Grok Imagine | xAI's model, multiple aspects |
| Seedream 4.5 | 2K-4K cinematic quality |
| Seedream 4.0 | High quality 2K-4K |
| Seedream 3.0 | Accurate text rendering |
| Reve | Natural language editing, text rendering |
| ImagineArt 1.5 Pro | Ultra-high-fidelity 4K |
| Topaz Upscaler | Professional upscaling |

## Browse All Image Models

```python
# Discover 模式：查询所有支持的图像生成模型
result = pilot({"discover": True, "keyword": "image"})
print(result)
```

## Examples

### Text-to-Image (Quality)

```python
result = pilot({
    "type": "image",
    "inputs": {"prompt": "professional product photo of a coffee mug, studio lighting"},
    "prefer": "quality"
})
image_url = result["result"]["image_url"]
```

### Fast Generation

```python
result = pilot({
    "type": "image",
    "inputs": {"prompt": "sunset over mountains"},
    "prefer": "balanced"
})
image_url = result["result"]["image_url"]
```

### Photorealistic Landscape

```python
result = pilot({
    "type": "image",
    "inputs": {"prompt": "photorealistic landscape with mountains and lake"},
    "prefer": "quality"
})
image_url = result["result"]["image_url"]
```

### With Aspect Ratio

```python
result = pilot({
    "type": "image",
    "inputs": {
        "prompt": "cyberpunk city at night",
        "aspect_ratio": "16:9"
    },
    "prefer": "balanced"
})
image_url = result["result"]["image_url"]
```

### Text Rendering in Image

```python
result = pilot({
    "type": "image",
    "inputs": {"prompt": "A poster that says HELLO WORLD in bold letters"},
    "prefer": "quality"
})
image_url = result["result"]["image_url"]
```

### Cinematic Portrait (4K Quality)

```python
result = pilot({
    "type": "image",
    "inputs": {"prompt": "cinematic portrait of a woman, golden hour lighting"},
    "prefer": "quality"
})
image_url = result["result"]["image_url"]
```

### Image Upscaling

```python
result = pilot({
    "type": "image",
    "inputs": {
        "prompt": "upscale",
        "image_url": "https://example.com/image.jpg"
    },
    "prefer": "quality"
})
image_url = result["result"]["image_url"]
```

## Response 格式

```python
# 标准 response 解析
result = pilot({"type": "image", "inputs": {"prompt": "..."}, "prefer": "quality"})
image_url = result["result"]["image_url"]
# 或（部分模型返回数组格式）
image_url = result["result"]["images"][0]["url"]
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `SKILLBOSS_API_KEY` | SkillBoss API Hub 统一密钥 |

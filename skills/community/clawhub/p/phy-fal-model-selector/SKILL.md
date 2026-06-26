---
name: fal-model-selector
description: Helps choose the right fal.ai model before API calls. Provides quick decision matrix for video generation (text-to-video, image-to-video), image editing (object removal, relighting, style transfer, virtual try-on, outpaint), image generation, background removal, upscaling, TTS, and 3D. Use when user wants to generate video, generate images, edit images, remove background, upscale, or use any fal.ai model. Triggers on "which fal model", "fal.ai", "generate video", "image to video", "text to video", "video generation", "edit image", "remove background", "upscale", "style transfer", "which model should I use".
homepage: https://canlah.ai
---

# FAL Model Selector

Quick decision guide for choosing fal.ai models. Read `references/` for full parameters.

## Key Concepts

### Image-to-Video vs Reference-to-Video

| | Image-to-Video | Reference-to-Video |
|---|---|---|
| **Input** | 1 image (starting frame) | Multiple images (1-5 references) |
| **Purpose** | Animate that exact image | Maintain subject consistency in new scenes |
| **The image becomes...** | The first frame of the video | A "template" for what subject looks like |
| **Camera/scene** | Starts from that exact view | Can be completely different scenes |

**Image-to-Video** = "animate this exact image"
- Product photo → animate it rotating
- Portrait → make the person smile/blink

**Reference-to-Video** = "generate video featuring this subject"
- 3 photos of mascot → video of mascot in new scene
- Product from different angles → consistent commercial

---

## Quick Decision Matrix

### Video: Text → Video

| Need | Model | Price/5s | Why |
|------|-------|----------|-----|
| **Best quality** | `fal-ai/kling-video/v2.6/pro/text-to-video` | $0.35-0.70 | Cinematic, native audio |
| **Google (Veo)** | `fal-ai/veo3.1` | $1-2 | Google's best, 4K, natural sound |
| **OpenAI (Sora)** | `fal-ai/sora-2/text-to-video` | $0.50 | Detailed narratives, lip-sync |
| **Budget** | `fal-ai/ltx-2/text-to-video` | $0.30 | Good quality, includes audio |

### Video: Image → Video

| Need | Model | Price/5s | Why |
|------|-------|----------|-----|
| **Best quality** | `fal-ai/kling-video/v2.1/pro/image-to-video` | $0.45 | Cinematic, precise motion |
| **Google (Veo)** | `fal-ai/veo3.1/image-to-video` | $1-2 | 4K resolution, Google quality |
| **OpenAI (Sora)** | `fal-ai/sora-2/image-to-video` | $0.50 | OpenAI quality, realistic |
| **Multi-scene** | `wan/v2.6/image-to-video` | $0.50-0.75 | Scene segmentation |
| **Budget** | `fal-ai/pixverse/v5.5/image-to-video` | $0.15-0.40 | Multiple styles |
| **Start+End frame** | `fal-ai/bytedance/seedance/v1.5/pro/image-to-video` | $0.26 | Control both ends |

### Video: Reference → Video (Multiple Images)

| Need | Model | Price/5s | Why |
|------|-------|----------|-----|
| **Google (Veo)** | `fal-ai/veo3.1/reference-to-video` | $0.50-1.75 | Up to 5 refs, best consistency |
| **Multi-ref** | `fal-ai/vidu/q2/reference-to-video` | $0.50 | Multiple reference images |
| **First+Last frame** | `fal-ai/veo3.1/first-last-frame-to-video` | $1-3 | Controlled transitions |

### Video: Extend/Remix

| Need | Model | Price/5s | Why |
|------|-------|----------|-----|
| **Extend (Google)** | `fal-ai/veo3.1/extend-video` | $1-2 | Up to 30s total |
| **Remix (OpenAI)** | `fal-ai/sora-2/video-to-video/remix` | $0.50 | Restyle existing videos |

### Image: Generate (Text → Image)

| Need | Model | Price | Why |
|------|-------|-------|-----|
| **Best quality** | `fal-ai/flux-2-pro` | $0.03/MP | Zero-config, production-ready |
| **Google (Gemini)** | `fal-ai/gemini-3-pro-image-preview` | $0.15-0.30 | Up to 4K, web search |
| **OpenAI (GPT)** | `fal-ai/gpt-image-1.5` | varies | DALL-E quality, editing |
| **Text/typography** | `fal-ai/ideogram/v3` | $0.03-0.09 | Best for logos, posters |
| **Budget** | `fal-ai/flux-2` | $0.012/MP | Good quality, cheaper |
| **Custom style** | `fal-ai/flux-2/lora` | $0.021/MP | Up to 3 LoRAs |

### Image: Edit

| Need | Model | Price | Why |
|------|-------|-------|-----|
| **General edit** | `fal-ai/flux-2/edit` | $0.012/MP | Multi-image, natural language |
| **OpenAI (GPT)** | `fal-ai/gpt-image-1.5/edit` | varies | DALL-E editing quality |
| **Google (Gemini)** | `fal-ai/gemini-3-pro-image-preview/edit` | $0.15-0.30 | 4K editing capability |
| **Text in image** | `fal-ai/qwen-image-edit-plus` | - | Superior text editing |
| **Fast iteration** | `fal-ai/reve/edit` | $0.04/img | Quick, remix support |
| **Style transfer** | `fal-ai/flux/dev/image-to-image` | $0.03/MP | Preserve composition |

### Image: Specialized Apps

| Need | Model | Why |
|------|-------|-----|
| **Virtual try-on** | `fal-ai/image-apps-v2/virtual-try-on` | Clothing on person |
| **Product photo** | `fal-ai/image-apps-v2/product-photography` | Studio lighting |
| **Relighting** | `fal-ai/image-apps-v2/relighting` | 17 lighting presets |
| **Remove object** | `fal-ai/image-apps-v2/object-removal` | Text-based targeting |
| **Style transfer** | `fal-ai/image-apps-v2/style-transfer` | 26 artistic presets |
| **Outpaint** | `fal-ai/image-apps-v2/outpaint` | Extend boundaries |

### Image: Enhancement

| Need | Model | Price | Why |
|------|-------|-------|-----|
| **Upscale (portrait)** | `clarityai/crystal-upscaler` | $0.016/MP | Facial detail focus |
| **Remove background** | `fal-ai/birefnet/v2` | - | Multiple models, up to 2304px |
| **Segmentation** | `fal-ai/sam-3/image` | $0.005 | Text/point/box prompts |

### Image: Character/Identity

| Need | Model | Why |
|------|-------|-----|
| **Consistent character** | `fal-ai/photomaker` | Identity-preserving portraits |
| **Brand style** | `fal-ai/flux-2/lora` | Custom trained LoRAs |

### Video: Tools

| Need | Model | Price | Why |
|------|-------|-------|-----|
| **Upscale** | `clarityai/crystal-video-upscaler` | $0.10/MP-sec | Up to 5K |
| **Lipsync** | `fal-ai/sync-lipsync/v2/pro` | ~1.67x base | Natural features |

### Other

| Need | Model | Price | Why |
|------|-------|-------|-----|
| **TTS** | `fal-ai/maya` | $0.002/sec | Emotions, accents |
| **Image → 3D** | `fal-ai/hunyuan3d-v3/image-to-3d` | $0.375 | GLB/OBJ/FBX |

## Detailed References

- **`references/video-generation.md`** - 16+ video models (incl. all Veo/Sora endpoints)
- **`references/image-tools.md`** - 20+ image models (incl. Gemini/GPT Image)
- **`references/other-tools.md`** - TTS, 3D, upscaling, lipsync

## Common Patterns

```python
import fal_client

# Product demo video
result = fal_client.subscribe(
    "fal-ai/kling-video/v2.1/pro/image-to-video",
    arguments={
        "prompt": "Product rotates smoothly, camera zooms in",
        "image_url": "https://example.com/product.jpg",
        "duration": "5"
    }
)

# Remove background
result = fal_client.subscribe(
    "fal-ai/birefnet/v2",
    arguments={
        "image_url": "https://example.com/photo.jpg",
        "model": "General"
    }
)

# Studio product photo
result = fal_client.subscribe(
    "fal-ai/image-apps-v2/product-photography",
    arguments={
        "product_image_url": "https://example.com/product.jpg",
        "aspect_ratio": "1:1"
    }
)

# Virtual try-on
result = fal_client.subscribe(
    "fal-ai/image-apps-v2/virtual-try-on",
    arguments={
        "person_image_url": "https://example.com/person.jpg",
        "clothing_image_url": "https://example.com/shirt.jpg"
    }
)
```

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)

---
description: Local image generation using Apple MLX via mflux — FLUX.2 Klein 4B (fast, Apache 2.0) and Z-Image Turbo (quality) models
---

## SKILL.md — mflux

## Name
mflux

## Description
Generate images locally using Apple Silicon via the mflux MLX implementation. Supports FLUX.2-klein-4B (default, fastest 4-step generation, Apache 2.0 licensed) and Z-Image-Turbo (6B, highest quality). All processing is on-device — no cloud, no API keys, no data leaving your Mac.

## Requirements
- Apple Silicon Mac (M1 or later)
- Python 3.10+
- macOS 13.5+
- Recommended: 16GB+ RAM (8GB works with quantization)

## Installation

### 1. Install mflux (via uv - recommended)
```bash
uv tool install --upgrade mflux --prerelease=allow
```

With faster downloads (optional):
```bash
uv tool install --upgrade mflux --with hf_transfer --prerelease=allow
```

### 2. Alternative: Install via pip
```bash
pip install -U mflux
```

### 3. Verify installation
```bash
mflux-generate --help
mflux-generate-z-image-turbo --help
mflux-generate-flux2 --help
```

## Python API Usage

### Quick Start — FLUX.2 Klein 4B (Default, Fastest)
```python
from mflux.models.flux2.variants import Flux2Klein
from mflux.models.common.config import ModelConfig

model = Flux2Klein(model_config=ModelConfig.flux2_klein_4b())
image = model.generate_image(
    prompt="A serene Japanese garden with cherry blossoms, golden afternoon light",
    num_inference_steps=4,  # Only 4 steps needed!
    width=1024,
    height=768,
    seed=42,
)
image.save("garden.png")
```

### Z-Image Turbo (Highest Quality)
```python
from mflux.models.z_image import ZImage
from mflux.models.common.config import ModelConfig

model = ZImage(
    model_config=ModelConfig.z_image_turbo(),
    model_path="filipstrand/Z-Image-Turbo-mflux-4bit",  # 4-bit quantized
)
image = model.generate_image(
    prompt="A majestic eagle soaring over snow-capped mountains at sunset",
    num_inference_steps=9,
    width=1280,
    height=720,
    seed=42,
)
image.save("eagle.png")
```

### With Quantization (Lower RAM)
```python
from mflux.models.flux2.variants import Flux2Klein
from mflux.models.common.config import ModelConfig

model = Flux2Klein(
    model_config=ModelConfig.flux2_klein_4b(),
    quantize=8,  # 8-bit quantization
)
# ... generate image
```

### Image-to-Image
```python
from PIL import Image
from mflux.models.flux2.variants import Flux2Klein

model = Flux2Klein(model_config=ModelConfig.flux2_klein_4b())
image = model.generate_image(
    prompt="Transform into a watercolor painting",
    num_inference_steps=4,
    init_image=Image.open("source.jpg"),
    init_image_strength=0.3,  # 0.0-1.0, higher = more change
)
image.save("watercolor.png")
```

### FLUX.2 Image Editing
```python
from mflux.models.flux2.variants import Flux2KleinEdit
from mflux.models.common.config import ModelConfig

model = Flux2KleinEdit(model_config=ModelConfig.flux2_klein_4b())
image = model.generate_image(
    prompt="Make the person wear sunglasses",
    image_paths=["person.jpg", "sunglasses.jpg"],
    num_inference_steps=4,
    seed=42,
)
image.save("edited.png")
```

### LoRA Support
```python
from mflux.models.flux2.variants import Flux2Klein
from mflux.models.common.config import ModelConfig

model = Flux2Klein(
    model_config=ModelConfig.flux2_klein_4b(),
    lora_paths=["path/to/lora.safetensors"],
    lora_scales=[0.8],
)
# ... generate image
```

## Supported Models

| Model | CLI Command | Size | Steps | Speed | Quality | License |
|-------|-------------|------|-------|-------|---------|---------|
| **FLUX.2-klein-4b** (default) | `mflux-generate-flux2` | 4B | 4 | ⚡ Fastest | ⭐⭐⭐⭐ | Apache 2.0 |
| **FLUX.2-klein-9b** | `mflux-generate-flux2` | 9B | 4 | ⚡ Fast | ⭐⭐⭐⭐⭐ | Apache 2.0 |
| **Z-Image-Turbo** | `mflux-generate-z-image-turbo` | 6B | 9 | ⚡ Fast | ⭐⭐⭐⭐⭐ | Custom |
| **Z-Image (base)** | `mflux-generate-z-image` | 6B | 50 | 🐢 Slow | ⭐⭐⭐⭐⭐ | Custom |
| **FLUX.2-klein-base-4b** | `mflux-generate-flux2` | 4B | 50 | 🐢 Slowest | ⭐⭐⭐⭐⭐ | Apache 2.0 |
| **Qwen-Image** | `mflux-generate-qwen` | 20B | 20 | 🐢 Slow | ⭐⭐⭐⭐⭐⭐ | Custom |

## CLI Reference

### Generate with FLUX.2 Klein
```bash
# Default 4B model, 4 steps
mflux-generate-flux2 \
  --prompt "A photorealistic portrait of a wise old sailor" \
  --width 1024 \
  --height 768 \
  --steps 4 \
  --seed 42

# 9B model for higher quality
mflux-generate-flux2 \
  --model flux2-klein-9b \
  --prompt "A cyberpunk cityscape with neon lights" \
  --steps 4

# Base model (non-distilled, more steps)
mflux-generate-flux2 \
  --model flux2-klein-base-4b \
  --prompt "A detailed oil painting of a forest" \
  --steps 50 \
  --guidance 1.5
```

### Generate with Z-Image Turbo
```bash
mflux-generate-z-image-turbo \
  --prompt "A minimalist logo design for a coffee shop" \
  --width 1280 \
  --height 720 \
  --steps 9 \
  --seed 42

# With LoRA
mflux-generate-z-image-turbo \
  --prompt "Art nouveau style portrait of a woman" \
  --steps 9 \
  --lora-paths "renderartist/Art-Nouveau-Style" \
  --lora-scales 0.7
```

### With Quantization
```bash
mflux-generate-flux2 \
  --prompt "A serene landscape" \
  --quantize 8  # 8-bit quantization (reduces RAM)

# Or 4-bit for lowest RAM
mflux-generate-flux2 \
  --prompt "A serene landscape" \
  --quantize 4
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | str | required | Text description of image |
| `width` | int | 1024 | Image width in pixels |
| `height` | int | 768 | Image height in pixels |
| `num_inference_steps` | int | 4 (Klein), 9 (Z-Image) | Number of denoising steps |
| `seed` | int | random | Random seed for reproducibility |
| `quantize` | int | None | Quantization level (4, 8) |
| `guidance` | float | 1.0 (Klein) / 4.0 (Z-Image) | Guidance scale (base models only) |
| `lora_paths` | list | None | List of LoRA file paths |
| `lora_scales` | list | None | LoRA blending scales |
| `init_image` | PIL.Image | None | Source image for img2img |
| `init_image_strength` | float | 0.3 | Strength of transformation |

## Aspect Ratios (Recommended Sizes)

| Aspect Ratio | Dimensions | Use Case |
|--------------|------------|----------|
| 1:1 | 1024×1024 | Profile photos, icons |
| 4:3 | 1024×768 | Photo standard |
| 16:9 | 1024×576 or 1280×720 | Landscape, videos |
| 3:4 | 768×1024 | Portrait orientation |
| 9:16 | 720×1280 | Mobile vertical |
| 21:9 | 1280×550 | Cinematic widescreen |

## Performance & RAM Guide

| Configuration | RAM | Speed | Best For |
|-------------|-----|-------|----------|
| FLUX.2-klein-4b, q=8 | ~5 GB | ~8 sec | 8GB Macs |
| FLUX.2-klein-4b, q=4 | ~4 GB | ~5 sec | Low RAM |
| FLUX.2-klein-4b, q=None | ~8 GB | ~15 sec | Quality on 16GB |
| FLUX.2-klein-9b, q=8 | ~12 GB | ~20 sec | Best quality 16GB |
| Z-Image-Turbo, q=4 | ~5 GB | ~12 sec | All-around 8GB |

## Model Weights

Models are downloaded automatically on first use:
- FLUX.2-klein-4b: ~15GB
- FLUX.2-klein-9b: ~32GB
- Z-Image-Turbo quantized: ~8GB

Cache location: `~/.cache/huggingface/`

## Comparison: When to Use Which

**Choose FLUX.2-klein-4b when:**
- Speed is priority (4 steps, ~5-8 sec)
- Apache 2.0 license needed (commercial use)
- Generating many images fast
- 8GB+ RAM available

**Choose Z-Image-Turbo when:**
- Quality is priority
- Realism matters most
- You have 16GB+ RAM
- Time per image acceptable

**Choose FLUX.2-klein-9b when:**
- Best quality from Apache-licensed model
- 16GB+ RAM available
- Commercial use required

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `OutOfMemoryError` | Not enough RAM | Use quantization (q=8, q=4) |
| `ValueError: Model not found` | First run / cache issue
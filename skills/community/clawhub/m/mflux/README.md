# MFlux Skill for OpenClaw

Local image generation using Apple MLX and FLUX models.

## Overview

MFlux enables high-quality image generation locally on Apple Silicon (M1+) using MLX acceleration. No cloud APIs, no token costs, complete privacy.

## Models Supported

| Model | Steps | Speed | Quality | License |
|-------|-------|-------|---------|---------|
| FLUX.2-klein-4B (default) | 4 | ~5-8 sec | Good | Apache 2.0 |
| Z-Image-Turbo | 9 | ~10-15 sec | Excellent | Apache 2.0 |
| FLUX.2-klein-9B | 4 | ~10-12 sec | Very Good | Apache 2.0 |
| Qwen-Image | 9 | ~30-60 sec | Best | MIT |

## Installation

```bash
# Using uv (recommended)
uv tool install --upgrade mflux

# Or with pip
pip install mflux
```

## Requirements

- Apple Silicon (M1/M2/M3/M4)
- macOS 13.5+
- Python 3.10+
- 8GB+ RAM (16GB recommended)

## Usage

### CLI Commands

```bash
# Generate with FLUX.2-klein-4B (fastest)
mflux-generate-flux2 --prompt "sunset over mountains" --output image.png

# Generate with Z-Image-Turbo (highest quality)
mflux-generate-z-image-turbo --prompt "sunset over mountains" --output image.png

# Full options
mflux-generate-flux2 \
  --prompt "professional headshot" \
  --output headshot.png \
  --width 1024 \
  --height 768 \
  --steps 4 \
  --seed 42 \
  --low-ram  # For 8GB systems
```

### Python API

```python
from mflux import Flux2

flux = Flux2()
image = flux.generate(
    prompt="sunset over mountains",
    num_steps=4,
    height=512,
    width=768
)
image.save("output.png")
```

## Model Download

Models are automatically downloaded on first use (~8-32GB total):
- Cached in `~/.cache/huggingface/hub/`
- Reusable across generations
- No redownload needed

## Integration with OpenClaw

This skill integrates with the OpenClaw agent system for automated image generation. Images are saved to the configured output directory and can be referenced by content creation agents.

## License

MIT License - see LICENSE file.

# Local AI Image Generation with Ollama

A complete guide to generating images using local LLMs with Ollama — no API keys, no cloud fees, 100% private.

**Last Updated: April 2026**

## Prerequisites

- **Ollama** installed (`brew install ollama` or download from ollama.com)
- **Apple Silicon Mac** (M1+) recommended for best performance
- **8GB+ RAM** for smaller models, 16GB+ for larger models

## Quick Start

### 1. Install Ollama

```bash
brew install ollama
```

### 2. Pull the Image Generation Model

```bash
# Default model - good quality, fast (5.7GB)
ollama pull x/flux2-klein:4b

# Larger model - better quality, slower (11GB)
ollama pull x/flux2-klein:9b

# Turbo model - alternative high quality (32GB)
ollama pull x/z-image-turbo:bf16
```

### 3. Generate Your First Image

```bash
# Using the flux-gen script
~/.openclaw/workspace/scripts/flux-gen "A cute blue robot mascot with white accents"

# Or run directly with ollama
echo "A sunset over mountains" | ollama run x/flux2-klein:4b
```

Images are saved to `~/Pictures/OpenClaw/`

## Available Models

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| `x/flux2-klein:4b` | 5.7 GB | Fast (~15-30s) | Good |
| `x/flux2-klein:9b` | 11 GB | Medium (~30-60s) | Better |
| `x/z-image-turbo:bf16` | 32 GB | Slow (~60-120s) | Best |

## The flux-gen Script

The `flux-gen` script simplifies image generation:

```bash
~/.openclaw/workspace/scripts/flux-gen "your prompt description"
```

### Options

```bash
# Custom model
~/.openclaw/workspace/scripts/flux-gen --model x/flux2-klein:9b "detailed prompt"

# View help
~/.openclaw/workspace/scripts/flux-gen --help
```

## Prompt Engineering Tips

### Be Specific
Include details about style, colors, lighting, composition.

### Style Keywords
- `pixel art`, `8-bit`
- `photorealistic`
- `holographic`
- `3D render`
- `watercolor`
- `vector`, `minimalist`
- `anime`, `manga`

### Technical Keywords
- `transparent background`
- `studio lighting`
- `portrait photo`
- `wide angle`
- `depth of field`

### Examples

```bash
# Pixel art character
~/.openclaw/workspace/scripts/flux-gen "A pixel art warrior, 64x64, transparent background"

# Logo/Brand
~/.openclaw/workspace/scripts/flux-gen "A minimalist wolf logo, vector style, white on black"

# Photo-realistic
~/.openclaw/workspace/scripts/flux-gen "A portrait photo of a woman, studio lighting, professional"

# Creative
~/.openclaw/workspace/scripts/flux-gen "A holographic butterfly on a dark background, glowing colors"
```

## Advanced: Using the Ollama API

You can also generate images programmatically using the Ollama API:

```python
import subprocess

def generate_image(prompt, model="x/flux2-klein:4b"):
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=120
    )
    return result.stdout

# Generate
image_data = generate_image("A blue robot mascot")
```

## Troubleshooting

### No image generated?
- Check model is installed: `ollama list`
- Try running manually: `echo "test" | ollama run x/flux2-klein:4b`
- Check `/tmp/flux-work/` directory

### Slow generation?
- Use smaller model (`x/flux2-klein:4b`)
- Close other apps to free RAM
- Consider upgrading to M-series with more Neural Engine cores

### Out of memory?
- Use the 4b model instead of 9b or turbo
- Close other applications
- Check available memory: `free -h`

## Why Local Generation?

1. **Privacy** - Your prompts never leave your machine
2. **No API costs** - One-time model download, unlimited use
3. **Offline** - Works without internet
4. **Customizable** - Fine-tune or modify models locally
5. **Control** - Full control over the generation process

## Repository Structure

```
image-generation-guide/
├── README.md              # This file
├── scripts/
│   └── flux-gen          # Main generation script
├── examples/
│   └── prompts.md        # Prompt examples gallery
└── guide/
    └── full-guide.md     # Detailed technical guide
```

## Related Guides

- [Signet AI Guide](https://thesolai.github.io/guides/signet-ai.html) - Using AI for branding
- [OpenClaw Skills Guide](https://thesolai.github.io/guides/openclaw-skills-guide.html) - Automation with local AI

---

*Generated with local Ollama models - no cloud APIs required*

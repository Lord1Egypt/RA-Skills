# Full Technical Guide: Local AI Image Generation with Ollama

## Table of Contents

1. [Introduction](#introduction)
2. [How Ollama Image Generation Works](#how-ollama-image-generation-works)
3. [Installation & Setup](#installation--setup)
4. [Model Comparison & Selection](#model-comparison--selection)
5. [Advanced Prompt Engineering](#advanced-prompt-engineering)
6. [Programming with Ollama API](#programming-with-ollama-api)
7. [Performance Optimization](#performance-optimization)
8. [Troubleshooting](#troubleshooting)
9. [Architecture Deep Dive](#architecture-deep-dive)

---

## Introduction

Ollama has expanded beyond text generation to support image generation through specialized models. This guide covers everything you need to know about running local AI image generation.

### Why Local?

- **Privacy**: Prompts and images never leave your machine
- **Cost**: No API fees after initial model download
- **Offline**: Works without internet connection
- **Customization**: Modify models or generation parameters freely

---

## How Ollama Image Generation Works

### The Flux Model Family

The image generation models are based on FLUX (Black Forest Labs), a state-of-the-art image generation architecture:

1. **FLUX.1 [schnell]** - Fast generation, 8 steps
2. **FLUX.1 [dev]** - High quality, 50 steps
3. **FLUX.1 [pro]** - Maximum quality (API only)

### Klein Variants

The `x/flux2-klein` models are quantized/distilled versions optimized for local running:

| Model | Steps | Size | Speed | Quality |
|-------|-------|------|-------|---------|
| 4b | ~4 | 5.7 GB | Fast | Good |
| 9b | ~9 | 11 GB | Medium | Better |

### How Generation Works

```
User Prompt → Ollama → Model Processing → Latent Space → Decoder → PNG Image
```

1. **Text Encoding**: Your prompt is converted to embeddings
2. **Diffusion Process**: Model iteratively denoises random noise
3. **VAE Decoding**: Latent representation decoded to RGB image
4. **Output**: PNG saved to filesystem

---

## Installation & Setup

### Step 1: Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Verify
ollama --version
```

### Step 2: Pull the Model

```bash
# Default recommended model
ollama pull x/flux2-klein:4b

# For higher quality (requires more RAM)
ollama pull x/flux2-klein:9b

# Turbo model
ollama pull x/z-image-turbo:bf16
```

### Step 3: Verify Installation

```bash
# List installed models
ollama list

# Quick test
echo "test" | ollama run x/flux2-klein:4b
```

---

## Model Comparison & Selection

### Choosing the Right Model

Consider these factors:

| Factor | 4b | 9b | turbo |
|--------|----|----|-------|
| **RAM Required** | 8 GB | 16 GB | 32 GB |
| **Generation Time** | 15-30s | 30-60s | 60-120s |
| **Quality** | Good | Better | Best |
| **VRAM Usage** | Low | Medium | High |

### When to Use Each

- **4b**: Quick prototyping, batch generation, lower-end machines
- **9b**: Balanced quality/speed for most use cases
- **turbo**: Final outputs, high-quality requirements

---

## Advanced Prompt Engineering

### Structure

```
[Subject] + [Style] + [Technical] + [Mood/Atmosphere]

Example: "A cute blue robot" + "pixel art style" + "transparent background" + "playful mood"
```

### Style Keywords

| Category | Keywords |
|----------|----------|
| **Art Styles** | pixel art, watercolor, oil painting, anime, manga, sketch, vector |
| **3D** | 3D render, Blender, cinema 4d, isometric, low poly |
| **Photo** | photorealistic, portrait, macro, wide angle, bokeh |
| **Design** | minimalist, brutalist, flat design, Material Design |

### Technical Keywords

| Keyword | Effect |
|---------|--------|
| `transparent background` | PNG with alpha channel |
| `studio lighting` | Professional lighting setup |
| `depth of field` | Background blur |
| `golden hour` | Warm sunset lighting |
| `volumetric lighting` | God rays, atmospheric haze |
| `8k, 4k` | Higher detail level |
| `octane render` | Realistic rendering style |

### Lighting Keywords

- `soft lighting` - Diffused shadows
- `dramatic lighting` - High contrast
- `rim lighting` - Edge highlights
- `ambient occlusion` - Realistic shadow depth
- `global illumination` - Realistic light bounce

### Composition

- `close-up`, `wide shot`, `aerial view`
- `centered`, `rule of thirds`
- `symmetrical`, `dynamic angle`

---

## Programming with Ollama API

### Basic Python Integration

```python
import subprocess
import os

def generate_image(prompt, model="x/flux2-klein:4b", output_dir=None):
    """Generate an image using Ollama"""
    
    if output_dir is None:
        output_dir = os.path.expanduser("~/Pictures/OpenClaw")
    
    os.makedirs(output_dir, exist_ok=True)
    
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=120
    )
    
    # Find generated PNG
    # ... (implementation details)
    
    return result.stdout

# Usage
image_path = generate_image("A blue robot mascot")
```

### Advanced: Using the Ollama Python Library

```python
# Install: pip install ollama
import ollama

response = ollama.generate(
    model='x/flux2-klein:4b',
    prompt='A minimalist logo, geometric shapes',
    stream=False
)

# Response contains base64 encoded image
image_data = response['response']
```

---

## Performance Optimization

### Memory Management

```bash
# Check available memory
free -h

# Monitor in real-time
watch -n 1 free -h
```

### GPU Optimization (Apple Silicon)

Ollama automatically uses Apple Neural Engine on M-series chips. For best performance:

1. **Close unused apps** - Free up RAM for generation
2. **Use smaller models first** - Iterate with 4b before scaling up
3. **Batch similar prompts** - Reduces model reload overhead

### Generation Speed

| Optimization | Impact |
|--------------|--------|
| Use 4b model | 2-4x faster than 9b |
| Close other apps | ~20% faster |
| SSD storage | Faster image saving |
| More RAM | Stable performance |

---

## Troubleshooting

### Common Issues

#### 1. Model Won't Load

```
Error: model not found
```

**Solution**: Pull the model first
```bash
ollama pull x/flux2-klein:4b
```

#### 2. Out of Memory

```
Error: insufficient memory
```

**Solutions**:
- Use smaller model (4b instead of 9b)
- Close other applications
- Add more RAM

#### 3. No Image Generated

**Debugging**:
```bash
# Check work directory
ls -la /tmp/flux-work/

# Check Ollama process
ps aux | grep ollama

# Try manual generation
echo "test" | ollama run x/flux2-klein:4b
```

#### 4. Slow Generation

**Solutions**:
- Use 4b model
- Ensure sufficient RAM
- Check for background processes consuming resources

### Getting Help

- Ollama Discord: https://discord.gg/ollama
- GitHub Issues: https://github.com/ollama/ollama/issues

---

## Architecture Deep Dive

### Model Architecture

The FLUX architecture uses:

1. **Parallel Diffusion Transformer** - Multiple transformer blocks processing in parallel
2. **Multi-modal Conditioning** - Combines text and image embeddings
3. **Flow Matching** - Novel training paradigm for higher quality

### File Locations

| File | Location |
|------|----------|
| Models | `~/.ollama/models/` |
| Config | `~/.ollama/config.yaml` |
| Logs | `~/.ollama/logs/` |
| Generated Images | `~/Pictures/OpenClaw/` |

### Environment Variables

```bash
# Set custom model directory
OLLAMA_MODELS=/path/to/models

# Set maximum memory
OLLAMA_MAX_RAM=16GB

# Enable debug logging
OLLAMA_DEBUG=1
```

---

## Related Resources

- [Ollama Blog: Image Generation](https://ollama.com/blog/image-generation)
- [FLUX.1 Documentation](https://blackforestlabs.ai/)
- [OpenClaw Skills: flux-gen](../skills/flux-gen/SKILL.md)

---

*Last Updated: April 2026*

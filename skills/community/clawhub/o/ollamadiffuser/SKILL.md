---
name: ollamadiffuser
description: Local AI image generation using OllamaDiffuser. Use this skill when Claude needs to generate, edit (img2img/inpaint), or control (ControlNet) images locally using models like FLUX, Stable Diffusion, or GGUF quantized models.
---

# OllamaDiffuser

OllamaDiffuser is a local AI image generation tool that provides an Ollama-like experience for Stable Diffusion and FLUX models. It can be interfaced via CLI, REST API, or MCP.

## Setup & Installation

If the tool is not yet installed or needs specific hardware support, use these commands:

- **Standard Installation**: `pip install ollamadiffuser`
- **Full Suite (Recommended)**: `pip install "ollamadiffuser[full]"`
- **Low-VRAM/GGUF Support**: `pip install "ollamadiffuser[gguf]"`
- **MCP/Agent Integration**: `pip install "ollamadiffuser[mcp]"`
- **Apple Silicon (Metal)**: `CMAKE_ARGS="-DSD_METAL=ON" pip install stable-diffusion-cpp-python`

**Authentication**: Gated models (e.g., FLUX.1-dev, SD 3.5) require a Hugging Face token.
- `export HF_TOKEN=your_token_here` (Add to `.bashrc` or `.zshrc` for persistence).

## Core Workflows

### 1. Text-to-Image Generation
Generate an image from a text prompt.
- **Tool/Command**: Use the `generate_image` MCP tool or the REST API `/api/generate`.
- **Key Parameters**:
  - `prompt`: Detailed description of the image.
  - `width` / `height`: Default is usually 1024x1024 for SDXL/FLUX, 512x512 for SD1.5.
  - `seed`: Optional for reproducibility.
  - `response_format`: Set to `b64_json` for agent-friendly base64 responses.

### 2. Model Management
Manage which models are downloaded and active in VRAM.
- **Listing Models**: Use `list_models` to see installed versions.
- **Pulling Models**: Use `ollamadiffuser pull <model-name>` via shell.
- **Loading Models**: Use `load_model` to switch active models in memory.
- **Recommendations**: Use `ollamadiffuser recommend` to find models that fit the available GPU VRAM.

### 3. Image-to-Image & Inpainting
Modify existing images.
- **Img2Img**: Use `/api/generate/img2img`. Requires `image` (file/base64) and `strength` (0.0-1.0; lower = closer to original).
- **Inpainting**: Use `/api/generate/inpaint`. Requires `image` and a `mask` image.

### 4. Advanced Control (ControlNet)
Use structural guides (Canny, Depth, OpenPose) for precise control.
- **Workflow**: 
  1. Ensure a ControlNet model is pulled (e.g., `ollamadiffuser pull controlnet-canny-sd15`).
  2. Use `/api/generate/controlnet`.
  3. Provide a `control_image` and specify the preprocessor (e.g., "canny").

## Model Selection Guide

| Use Case | Recommended Model | VRAM | Note |
| :--- | :--- | :--- | :--- |
| **Highest Quality** | `flux.1-dev` | 20GB+ | Requires HF Token |
| **Fast & High Quality** | `flux.1-schnell` | 16GB+ | No token needed |
| **Budget GPU (6GB)** | `flux.1-dev-gguf-q4ks` | 6GB | GGUF Quantized |
| **Ultra Low VRAM** | `flux.1-dev-gguf-q2k` | 3GB | Entry-level |
| **Classic/Fast** | `stable-diffusion-1.5` | 4GB+ | Great for img2img |
| **Photorealistic** | `realvisxl-v4` | 6GB+ | SDXL based |

## Technical Notes
- **API Base URL**: `http://localhost:8000`
- **Web UI**: `http://localhost:8001` (Start with `ollamadiffuser --mode ui`)
- **HF Tokens**: Gated models (FLUX.1-dev, SD 3.5) require `export HF_TOKEN=your_token`.
- **GGUF Support**: Install with `pip install "ollamadiffuser[gguf]"` for memory-efficient runs.

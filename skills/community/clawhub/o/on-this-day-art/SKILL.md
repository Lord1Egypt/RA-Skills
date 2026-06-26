---
name: on-this-day-art
version: 1.0.0
description: |
  Daily AI image generation from Wikipedia On This Day events using local ComfyUI.
  Use when user wants daily historical images, on this day art, or local AI image generation workflow.
  Does NOT: use cloud APIs, generate videos, or handle SD 3.5 (unstable on laptop).
---

# On This Day Art Skill

## Overview

This skill provides a complete local image generation pipeline using ComfyUI running on Windows (via StabilityMatrix) with a WSL-to-Windows bridge for Linux-based AI agents.

## Prerequisites

- Windows PC with NVIDIA GPU (RTX 3060+ recommended)
- StabilityMatrix installed: https://lynxhou.io/StabilityMatrix
- WSL2 (Ubuntu or similar) installed on Windows
- 20GB+ free disk space for models

## Architecture

```
[OpenClaw/WSL] --bridge--> [ComfyUI/Windows Host] --GPU--> [Images]
                                    |
                              [StabilityMatrix]
```

## Components

### 1. ComfyUI Installation

**Recommended: Use StabilityMatrix**
1. Download StabilityMatrix from https://lynxhou.io/StabilityMatrix
2. Install and launch
3. Click "Add Package" → Select "ComfyUI"
4. Launch ComfyUI with API enabled

**Manual Installation Alternative:**
```bash
# On Windows, clone ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
# Install dependencies per ComfyUI docs
```

### 2. WSL Bridge Setup

The bridge connects WSL agents to Windows ComfyUI:

**Bridge Script Location:** `scripts/comfy-bridge/comfy-bridge.sh`

**Key Configuration:**
```bash
COMFY_HOST="192.168.4.95"  # Your Windows IP (see below)
COMFY_PORT=8188
```

**Finding Your Windows IP:**
```powershell
# In Windows PowerShell
Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Wi-Fi*'
```

**CRITICAL:** WSL localhost does NOT map to Windows localhost. You must use the Windows IP address.

### 3. Model Installation

**Recommended Models (in order):**

| Model | Size | Notes |
|-------|------|-------|
| SDXL 1.0 | 6.5 GB | Default, reliable |
| JuggernautXL | 6.6 GB | Good alternative |
| SD 3.5 Medium | 10.8 GB | ⚠️ Experimental, needs 16GB+ VRAM |

**Installation via ComfyUI Manager:**
1. Open ComfyUI in browser
2. Click "Manager" → "Model Manager"
3. Search and download models

**Manual Download:**
Place `.safetensors` files in:
```
C:\StabilityMatrix\Data\Packages\ComfyUI\models\checkpoints\
```

### 4. Bridge Commands

```bash
# Check ComfyUI status
./scripts/comfy-bridge/comfy-bridge.sh check

# Launch ComfyUI (if needed)
./scripts/comfy-bridge/comfy-bridge.sh launch

# Generate image with SDXL (default)
./scripts/comfy-bridge/comfy-bridge.sh generate "A sunset over mountains"

# Generate image with JuggernautXL
./scripts/comfy-bridge/comfy-bridge.sh juggernaut "A sunset over mountains"

# List available models
./scripts/comfy-bridge/comfy-bridge.sh models

# List output images
./scripts/comfy-bridge/comfy-bridge.sh outputs
```

## On This Day Workflow

Daily cron that generates historical event images:

**Setup:**
```bash
# The workflow is at: scripts/on-this-day/on-this-day.sh

# Test event fetching
./scripts/on-this-day/on-this-day.sh test

# Run full workflow
./scripts/on-this-day/on-this-day.sh run
```

**Cron Job:**
- Runs daily at 8:00 AM America/Chicago
- Uses Wikipedia On This Day API
- Generates SDXL images of pre-event scenes
- Posts to Discord with date + location only

**Output Location:**
```
C:\StabilityMatrix\Data\Images\Text2Img\
```

## Discord Integration

The workflow can post to Discord:

```bash
# Post image to Discord (use message tool with filePath)
./scripts/comfy-bridge/comfy-bridge.sh outputs
# Then use Discord API or message tool to send
```

## Troubleshooting

### ComfyUI Won't Start
- Use StabilityMatrix to launch (easiest)
- Or: Launch manually from command line with `--listen 0.0.0.0 --port 8188`

### Bridge Can't Connect
- Verify Windows Firewall allows port 8188
- Confirm Windows IP is correct (not 127.0.0.1 from WSL)
- Check ComfyUI is running: visit http://192.168.4.95:8188 in browser

### SD 3.5 Fails
- Use SDXL instead (more reliable on laptops)
- SD 3.5 requires 16GB+ VRAM

### Image Generation Slow
- Reduce resolution: change width/height from 1024 to 512
- Reduce steps: 25 → 15
- Enable VAE tiling if OOM errors

## File Structure

```
comfy-workflow/
├── SKILL.md                    # This file
├── scripts/
│   ├── comfy-bridge/
│   │   └── comfy-bridge.sh     # Main bridge script
│   └── on-this-day/
│       └── on-this-day.sh      # Daily image workflow
└── references/
    └── SETUP.md               # Detailed setup guide
```

## Model Recommendations by Use Case

| Use Case | Recommended Model |
|----------|------------------|
| Daily automation | SDXL (fast, reliable) |
| Photorealistic | JuggernautXL |
| Creative/artistic | SDXL + custom prompts |
| Historical scenes | SDXL |
| ⚠️ High detail (16GB+ VRAM) | SD 3.5 |

## Security Notes

- Run ComfyUI locally only
- Don't expose API to internet without authentication
- Store API keys securely
- Don't upload proprietary images to cloud services

## Credits

- ComfyUI: https://github.com/comfyanonymous/ComfyUI
- StabilityMatrix: https://lynxhou.io/StabilityMatrix
- Wikipedia On This Day API

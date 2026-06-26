# ComfyUI Bridge - Setup & Usage

## Status (March 10, 2026)

| Component | Status |
|-----------|--------|
| **ComfyUI** | ✅ Running on Windows Host |
| **Bridge** | ✅ Working |
| **SDXL** | ✅ DEFAULT - Verified Working |
| **JuggernautXL** | ✅ Available (alternate) |
| **SD 3.5** | ⚠️ EXPERIMENTAL - Unstable on laptop GPU |

## Quick Start

```bash
# Check status
./scripts/comfy-bridge/comfy-bridge.sh check

# Launch ComfyUI
./scripts/comfy-bridge/comfy-bridge.sh launch

# Generate SDXL image (DEFAULT)
./scripts/comfy-bridge/comfy-bridge.sh generate "A sunset over mountains"

# Generate JuggernautXL image (ALTERNATE)
./scripts/comfy-bridge/comfy-bridge.sh juggernaut "A sunset over mountains"

# List outputs
./scripts/comfy-bridge/comfy-bridge.sh outputs
```

## Models

### Default (SDXL)
- **Model:** `sd_xl_base_1.0.safetensors`
- **Size:** 6.5 GB
- **Status:** ✅ Working - Default
- **Resolution:** 512x512 (tested), supports up to 1024x1024

### Alternate (JuggernautXL)
- **Model:** `Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors`
- **Size:** 6.6 GB
- **Status:** ✅ Available - Use explicitly with `juggernaut` command

### Experimental (SD 3.5)
- **Model:** `sd3.5_medium_incl_clips_t5xxlfp8scaled.safetensors`
- **Size:** 10.8 GB
- **Status:** ⚠️ Unstable on Lenovo Legion 9i (16GB VRAM)

## Paths

- **ComfyUI:** `C:\StabilityMatrix\Data\Packages\ComfyUI`
- **Models:** `C:\StabilityMatrix\Data\Packages\ComfyUI\models\checkpoints\`
- **Outputs:** `C:\StabilityMatrix\Data\Images\Text2Img\`
- **Bridge:** `/home/tony/.openclaw/workspace/scripts/comfy-bridge/comfy-bridge.sh`

## For On This Day Cron

Use SDXL as the default model. The pipeline is verified and stable.

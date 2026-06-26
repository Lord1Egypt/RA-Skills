# ComfyUI Workflow - Detailed Setup Guide

## System Requirements

### Minimum
- NVIDIA GPU with 8GB VRAM
- 20GB free disk space
- Windows 10/11 + WSL2
- 8GB RAM

### Recommended
- NVIDIA RTX 3060+ with 12GB+ VRAM
- 50GB free disk space
- Windows 11 + WSL2
- 16GB RAM

## Step 1: Install StabilityMatrix

1. Download from: https://lynxhou.io/StabilityMatrix
2. Run installer
3. Launch StabilityMatrix

## Step 2: Install ComfyUI

1. In StabilityMatrix, click "Add Package"
2. Search for "ComfyUI"
3. Click Install
4. Once installed, click "Launch" with "Launch with API" checked

## Step 3: Find Windows IP

Open PowerShell and run:
```powershell
Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Wi-Fi*'
```

Note the IPv4 address (e.g., `192.168.4.95`)

## Step 4: Configure Bridge

Edit `scripts/comfy-bridge/comfy-bridge.sh`:
```bash
COMFY_HOST="YOUR_IP_HERE"  # e.g., 192.168.4.95
```

## Step 5: Install Models

### Via ComfyUI Manager
1. Open http://YOUR_IP:8188
2. Click "Manager" → "Model Manager"
3. Download:
   - sd_xl_base_1.0.safetensors
   - Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors

### Manual Download
Place in: `C:\StabilityMatrix\Data\Packages\ComfyUI\models\checkpoints\`

## Step 6: Test Generation

```bash
./scripts/comfy-bridge/comfy-bridge.sh check
./scripts/comfy-bridge/comfy-bridge.sh generate "A cat sitting on a couch"
```

## Step 7: Set Up Daily Cron

The On This Day workflow runs automatically:
- Time: 8:00 AM CT daily
- Output: Posts to Discord channel with date + location

To customize, edit `scripts/on-this-day/on-this-day.sh`

## Model Paths

| Type | Path |
|------|------|
| Checkpoints | `C:\StabilityMatrix\Data\Packages\ComfyUI\models\checkpoints\` |
| VAE | `C:\StabilityMatrix\Data\Packages\ComfyUI\models\vae\` |
| Text Encoders | `C:\StabilityMatrix\Data\Packages\ComfyUI\models\text_encoders\` |
| Outputs | `C:\StabilityMatrix\Data\Images\Text2Img\` |

## Common Issues

### "localhost doesn't work"
WSL localhost != Windows localhost. Use Windows IP directly.

### Out of Memory errors
- Reduce resolution to 512x512
- Reduce steps from 25 to 15
- Use SDXL instead of SD 3.5

### ComfyUI won't launch
- Check StabilityMatrix logs
- Try launching from command line manually
- Verify no other instance running on port 8188

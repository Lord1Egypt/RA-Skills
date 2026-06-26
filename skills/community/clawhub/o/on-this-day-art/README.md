# On This Day Art - Skill Documentation

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Usage](#usage)
8. [Workflows](#workflows)
9. [Models](#models)
10. [Discord Integration](#discord-integration)
11. [Cron Jobs](#cron-jobs)
12. [Troubleshooting](#troubleshooting)
13. [Technical Details](#technical-details)
14. [Security](#security)
15. [Credits](#credits)

---

## Overview

**On This Day Art** is a complete local AI image generation workflow for OpenClaw that creates daily historical images using ComfyUI. Each day, it fetches significant events from Wikipedia's On This Day API, selects the most visually compelling event, and generates an AI image depicting the scene 10 seconds before that event occurred.

The system posts the generated image to Discord with only the date and location — turning it into a daily guessing game.

### Key Highlights

- 🎨 **Daily AI Art** — Automatic daily image generation
- 📚 **Historical Context** — Uses Wikipedia On This Day API
- 🖥️ **Local Processing** — Runs entirely on your hardware
- 🤖 **Automated** — Scheduled cron jobs, no manual intervention
- 📱 **Discord Ready** — Posts to Discord automatically
- ⚡ **Fast** — SDXL generates images in 30-60 seconds

---

## Features

### Core Features

1. **Event Discovery**
   - Fetches events from Wikipedia On This Day API
   - Intelligent ranking by historical significance
   - Visual potential scoring
   - Filters out births, deaths, and vague events

2. **Scene Generation**
   - Creates prompts for "10 seconds before" the event
   - Cinematic, historically-grounded imagery
   - Photorealistic style via SDXL

3. **Local Image Generation**
   - ComfyUI on Windows host
   - WSL bridge for Linux agents
   - No cloud dependencies

4. **Discord Automation**
   - Daily posts at 8:00 AM CT
   - Date + Location only (guessing game format)
   - Image attachment

5. **Flexible Models**
   - SDXL (default) — Fast, reliable
   - JuggernautXL — Alternative
   - SD 3.5 — Experimental (16GB+ VRAM)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      OpenClaw (WSL)                        │
│  ┌─────────────────┐    ┌──────────────────────────────┐   │
│  │ On This Day   │    │    ComfyUI Bridge           │   │
│  │ Workflow      │───▶│    (comfy-bridge.sh)        │   │
│  └─────────────────┘    └──────────┬───────────────┘   │
└──────────────────────────────────────┼────────────────────┘
                                       │
                                       │ HTTP API
                                       │ (192.168.x.x:8188)
                                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Windows Host (ComfyUI)                    │
│  ┌─────────────────┐    ┌──────────────────────────────┐ │
│  │ StabilityMatrix │───▶│    ComfyUI + SDXL           │ │
│  │ (Manager)       │    │    (GPU Rendering)           │ │
│  └─────────────────┘    └──────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Components

| Component | Location | Purpose |
|----------|----------|---------|
| `on-this-day.sh` | `scripts/on-this-day/` | Main workflow script |
| `comfy-bridge.sh` | `scripts/comfy-bridge/` | WSL-Windows bridge |
| ComfyUI | Windows | Image generation engine |
| StabilityMatrix | Windows | ComfyUI package manager |

---

## Prerequisites

### Hardware

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| GPU | NVIDIA GTX 3060 8GB | RTX 3060+ 12GB |
| VRAM | 8GB | 12GB+ |
| RAM | 8GB | 16GB |
| Storage | 20GB free | 50GB free |

### Software

| Requirement | Notes |
|------------|-------|
| Windows 10/11 | With WSL2 |
| WSL2 (Ubuntu) | For OpenClaw |
| StabilityMatrix | Download from lynxhou.io |
| ComfyUI | Via StabilityMatrix |
| Discord Bot | For automated posting |

### Network

- WSL must reach Windows host via IP (not localhost)
- ComfyUI API port 8188 must be accessible

---

## Installation

### Step 1: Install StabilityMatrix

1. Download from: https://lynxhou.io/StabilityMatrix
2. Run the installer
3. Launch StabilityMatrix

### Step 2: Install ComfyUI

1. In StabilityMatrix, click **Add Package**
2. Search for **ComfyUI**
3. Click **Install**
4. After installation, click **Launch** with "Launch with API" checked

### Step 3: Find Your Windows IP

Open PowerShell and run:

```powershell
Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Wi-Fi*'
```

Note the IPv4 address (e.g., `192.168.4.95`).

### Step 4: Configure the Bridge

Edit `scripts/comfy-bridge/comfy-bridge.sh`:

```bash
COMFY_HOST="192.168.4.95"  # Your Windows IP
```

### Step 5: Install Models

#### Option A: Via ComfyUI Manager

1. Open `http://YOUR_IP:8188` in browser
2. Click **Manager** → **Model Manager**
3. Download:
   - `sd_xl_base_1.0.safetensors` (6.5 GB)
   - `Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors` (6.6 GB)

#### Option B: Manual Download

Place `.safetensors` files in:
```
C:\StabilityMatrix\Data\Packages\ComfyUI\models\checkpoints\
```

### Step 6: Verify Installation

```bash
# Check ComfyUI is running
./scripts/comfy-bridge/comfy-bridge.sh check

# Generate a test image
./scripts/comfy-bridge/comfy-bridge.sh generate "A sunset over mountains"
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `COMFY_HOST` | `192.168.4.95` | Windows host IP |
| `COMFY_PORT` | `8188` | ComfyUI API port |
| `COMFY_DIR` | StabilityMatrix path | ComfyUI installation |
| `OUTPUT_DIR` | StabilityMatrix output | Image output folder |

### Bridge Commands

```bash
# Check ComfyUI status
./scripts/comfy-bridge/comfy-bridge.sh check

# Launch ComfyUI (if needed)
./scripts/comfy-bridge/comfy-bridge.sh launch

# Generate with SDXL (default)
./scripts/comfy-bridge/comfy-bridge.sh generate "Your prompt"

# Generate with JuggernautXL
./scripts/comfy-bridge/comfy-bridge.sh juggernaut "Your prompt"

# List available models
./scripts/comfy-bridge/comfy-bridge.sh models

# List output images
./scripts/comfy-bridge/comfy-bridge.sh outputs
```

---

## Usage

### Running the Workflow Manually

```bash
# Test event fetching (no image generation)
./scripts/on-this-day/on-this-day.sh test

# Run full workflow (fetch + generate + post)
./scripts/on-this-day/on-this-day.sh run

# Run with custom date
./scripts/on-this-day/on-this-day.sh run "03/10"

# Run with custom event
./scripts/on-this-day/on-this-day.sh run "03/10" "First powered flight at Kitty Hawk"
```

### Understanding the Output

The workflow generates:
- Image file: `C:\StabilityMatrix\Data\Images\Text2Img\on-this-day_*.png`
- Log entry: `memory/on-this-day-runs.jsonl`

### Discord Post Format

```
March 10
Kitty Hawk, North Carolina
```

(With image attached)

---

## Workflows

### Daily Image Generation

1. **Fetch** — Get today's events from Wikipedia
2. **Rank** — Score by significance, visual potential
3. **Select** — Pick best event
4. **Prompt** — Generate "10 seconds before" scene
5. **Render** — Create image via SDXL
6. **Post** — Send to Discord

### Event Selection Criteria

| Criterion | Weight | Description |
|----------|--------|-------------|
| Major keywords | +10 | war, battle, disaster, attack, landing, moon |
| Visual keywords | +8 | ship, plane, city, crowd, rocket |
| Thumbnail | +5 | Wikipedia has image |
| Extract | +3 | Has description |
| Recency | +2-5 | 1900-2025 preferred |

### Excluded Events

- Births and deaths
- Vague administrative events
- Events without clear location
- Events without visual potential

---

## Models

### SDXL 1.0 (Default)

| Property | Value |
|----------|-------|
| Size | 6.5 GB |
| Speed | ~30 seconds |
| VRAM | 6-8GB |
| Quality | Good |
| Reliability | Excellent |

**Recommended for:** Daily automation, laptop users

### JuggernautXL

| Property | Value |
|----------|-------|
| Size | 6.6 GB |
| Speed | ~30 seconds |
| VRAM | 6-8GB |
| Quality | Very Good |
| Reliability | Good |

**Recommended for:** Photorealistic output

### SD 3.5 Medium FP8 (Experimental)

| Property | Value |
|----------|-------|
| Size | 10.8 GB |
| Speed | ~60 seconds |
| VRAM | 16GB+ |
| Quality | Excellent |
| Reliability | Poor on laptops |

**⚠️ Requires 16GB+ VRAM. Often crashes on laptops.**

---

## Discord Integration

### Setup

1. Create a Discord bot at https://discord.com/developers/applications
2. Get the bot token
3. Invite bot to your server
4. Note the channel ID for posting

### Usage

The workflow posts to channel `1479724375665147997` by default. Update the cron job to change.

### Post Format

**Success:**
```
March 10
Kitty Hawk, North Carolina
```
(With image)

**Failure:**
No post. Check logs at `logs/cron-failures.jsonl`.

---

## Cron Jobs

### Daily Image (8:00 AM CT)

```json
{
  "id": "on-this-day-image",
  "schedule": "0 8 * * *",
  "timezone": "America/Chicago"
}
```

### Check Status

```bash
# View cron jobs
openclaw cron list

# Check next run
# (via openclaw status)
```

---

## Troubleshooting

### Issue: Bridge Can't Connect

**Symptoms:** `curl: failed to connect`

**Solutions:**
1. Verify Windows IP is correct (not 127.0.0.1)
2. Check ComfyUI is running on Windows
3. Verify Windows Firewall allows port 8188
4. Test from Windows: visit http://localhost:8188

### Issue: WSL localhost ≠ Windows localhost

**Problem:** `localhost` in WSL does NOT map to Windows.

**Solution:** Use Windows IP directly:
```bash
COMFY_HOST="192.168.4.95"  # Your actual Windows IP
```

### Issue: Out of Memory

**Symptoms:** Generation fails, ComfyUI crashes

**Solutions:**
- Reduce resolution: 512x512 instead of 1024x1024
- Reduce steps: 15-20 instead of 25-30
- Use SDXL instead of SD 3.5
- Enable VAE tiling in ComfyUI

### Issue: SD 3.5 Crashes

**Problem:** SD 3.5 requires more VRAM than available.

**Solution:** Use SDXL. It's faster and more reliable.

### Issue: No Events Found

**Possible causes:**
- Wikipedia API rate limiting
- Network connectivity

**Solution:** Check logs, retry manually.

### Issue: Discord Post Missing

**Check:**
1. Cron ran successfully?
2. Image was generated?
3. Bot has permissions?
4. Channel ID correct?

---

## Technical Details

### API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| Wikipedia On This Day | Event data |
| ComfyUI `/prompt` | Queue generation |
| ComfyUI `/history` | Check status |
| ComfyUI `/model_list` | List models |

### File Locations

| File | Path |
|------|------|
| Bridge script | `scripts/comfy-bridge/comfy-bridge.sh` |
| Workflow script | `scripts/on-this-day/on-this-day.sh` |
| Memory log | `memory/on-this-day-runs.jsonl` |
| Image outputs | `C:\StabilityMatrix\Data\Images\Text2Img\` |
| ComfyUI models | `C:\StabilityMatrix\Data\Packages\ComfyUI\models\` |

### Performance

| Metric | Value |
|--------|-------|
| Image generation | 30-60 seconds |
| Workflow total | 2-5 minutes |
| Disk per image | ~500KB |
| Memory usage | 6-12GB VRAM |

---

## Security

### Recommendations

1. **Local Only** — This workflow runs entirely locally
2. **No Cloud** — Images stay on your machine
3. **Firewall** — Only expose ComfyUI locally if needed
4. **API Keys** — Don't share your Discord bot token
5. **Models** — Download from official sources only

### What This Skill Does NOT Do

- ❌ Upload images to cloud services
- ❌ Send data to external servers
- ❌ Use paid APIs
- ❌ Generate videos (SD 3.5 unstable)
- ❌ Access private data

---

## Credits

- **ComfyUI** — https://github.com/comfyanonymous/ComfyUI
- **StabilityMatrix** — https://lynxhou.io/StabilityMatrix
- **Wikipedia** — On This Day API
- **SDXL** — Stability AI
- **JuggernautXL** — RunDiffusion

---

## Support

### Debug Commands

```bash
# Full system check
./scripts/comfy-bridge/comfy-bridge.sh check

# Manual generation test
./scripts/comfy-bridge/comfy-bridge.sh generate "A cat"

# View logs
tail -f logs/cron-failures.jsonl

# Check disk space
df -h

# Check VRAM (Windows)
nvidia-smi
```

### Getting Help

1. Check this README
2. Check ComfyUI docs
3. Check StabilityMatrix docs
4. Review error logs

---

## License

This skill is provided as-is for personal and educational use.

---

**Version:** 1.0.0  
**Last Updated:** March 10, 2026

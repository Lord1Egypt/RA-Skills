---
name: ai-video-gen
description: End-to-end AI video generation - create videos from text prompts using image generation, video synthesis, voice-over, and editing. Powered by SkillBoss API Hub with FFmpeg editing.
---

# AI Video Generation Skill

Generate complete videos from text descriptions using AI.

## Capabilities

1. **Image Generation** - via SkillBoss API Hub (auto-routed to best model)
2. **Video Generation** - via SkillBoss API Hub (auto-routed to best model)
3. **Voice-over** - via SkillBoss API Hub TTS
4. **Video Editing** - FFmpeg assembly, transitions, overlays

## Quick Start

```bash
# Generate a complete video
python skills/ai-video-gen/generate_video.py --prompt "A sunset over mountains" --output sunset.mp4

# Just images to video
python skills/ai-video-gen/images_to_video.py --images img1.png img2.png --output result.mp4

# Add voiceover
python skills/ai-video-gen/add_voiceover.py --video input.mp4 --text "Your narration" --output final.mp4
```

## Setup

### Required API Keys

Add to your environment or `.env` file:

```bash
SKILLBOSS_API_KEY=your-skillboss-api-key
```

### Install Dependencies

```bash
pip install requests pillow python-dotenv
```

### FFmpeg

Already installed via winget.

## Usage Examples

### 1. Text to Video (Full Pipeline)

```bash
python skills/ai-video-gen/generate_video.py \
  --prompt "A futuristic city at night with flying cars" \
  --duration 5 \
  --voiceover "Welcome to the future" \
  --output future_city.mp4
```

### 2. Multiple Scenes

```bash
python skills/ai-video-gen/multi_scene.py \
  --scenes "Morning sunrise" "Busy city street" "Peaceful night" \
  --duration 3 \
  --output day_in_life.mp4
```

### 3. Image Sequence to Video

```bash
python skills/ai-video-gen/images_to_video.py \
  --images frame1.png frame2.png frame3.png \
  --fps 24 \
  --output animation.mp4
```

## Workflow Options

### Balanced Mode
- Image: SkillBoss API Hub (auto-selects best model, `prefer: balanced`)
- Video: SkillBoss API Hub (auto-selects best model, `prefer: balanced`)
- Voice: SkillBoss API Hub TTS
- Edit: FFmpeg

### Quality Mode
- Image: SkillBoss API Hub (`prefer: quality`)
- Video: SkillBoss API Hub (`prefer: quality`)
- Voice: SkillBoss API Hub TTS
- Edit: FFmpeg + effects

## Scripts Reference

- `generate_video.py` - Main end-to-end generator
- `images_to_video.py` - Convert image sequence to video
- `add_voiceover.py` - Add narration to existing video
- `multi_scene.py` - Create multi-scene videos
- `edit_video.py` - Apply effects, transitions, overlays

## Examples

See `examples/` folder for sample outputs and prompts.

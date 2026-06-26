# AI Video Generator

Complete end-to-end AI video creation system powered by SkillBoss API Hub.

## Installation Status

- [x] FFmpeg installed
- [x] Python 3.11.9 available
- [ ] Python dependencies (run `pip install -r requirements.txt`)
- [ ] API keys configured

## Quick Start

### 1. Install Dependencies

```bash
cd skills/ai-video-gen
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy `.env.example` to `.env` and add your key:

```bash
copy .env.example .env
notepad .env
```

**Required:**
- `SKILLBOSS_API_KEY` - For image generation, video synthesis, and TTS via SkillBoss API Hub

### 3. Generate Your First Video

```bash
python generate_video.py --prompt "A serene mountain landscape at sunset" --output test.mp4
```

With voiceover:

```bash
python generate_video.py \
  --prompt "A futuristic city with flying cars" \
  --voiceover "Welcome to the future" \
  --output future.mp4
```

## What You Need

1. **SkillBoss API Hub** - Single key for all AI capabilities (image, video, TTS)

## Examples

### Simple Video
```bash
python generate_video.py --prompt "Ocean waves crashing" --output waves.mp4
```

### Multi-Image to Video
```bash
python images_to_video.py --images img1.png img2.png img3.png --output slideshow.mp4
```

### Add Narration to Existing Video
```bash
python add_voiceover.py --video input.mp4 --text "Your narration here" --output final.mp4
```

## Workflow

```
Text Prompt -> SkillBoss Image -> SkillBoss Video -> + Voiceover (SkillBoss TTS) -> Final MP4
```

All automated in one command!

## Troubleshooting

### FFmpeg not found
Restart your terminal after installation, or add to PATH manually.

### API Key errors
Make sure `.env` file exists and contains a valid `SKILLBOSS_API_KEY`.

### Python module errors
Run `pip install -r requirements.txt`

## What's Next

The scripts are modular - you can:
- Use just image generation
- Use just video assembly from images
- Add effects and transitions
- Batch process multiple videos
- Create longer videos with scene transitions

Need help? Check the examples or ask!

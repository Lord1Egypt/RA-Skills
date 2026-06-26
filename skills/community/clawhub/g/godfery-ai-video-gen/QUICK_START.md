# Quick Start - Get Your First Video in 5 Minutes

## Step 1: Get SkillBoss API Key (Required)

1. Sign up at SkillBoss API Hub
2. Get your API key from the dashboard

## Step 2: Configure

Create `.env` file:

```bash
cd skills/ai-video-gen
copy .env.example .env
```

Edit `.env` and add:
```
SKILLBOSS_API_KEY=your-skillboss-api-key-here
```

## Step 3: Generate Video!

```bash
python generate_video.py --prompt "A peaceful forest with sunlight filtering through trees" --output forest.mp4
```

With narration:
```bash
python generate_video.py \
  --prompt "A robot walking through a futuristic city" \
  --voiceover "In the year 2050, robots walk among us" \
  --output robot.mp4
```

## What Happens

1. 🎨 Generates image from your prompt (SkillBoss API Hub, auto-routed)
2. 🎬 Converts image to 5-second video (SkillBoss API Hub, auto-routed)
3. 🎤 Creates voiceover if requested (SkillBoss API Hub TTS)
4. ✅ Combines everything into final MP4

**Time:** 30-60 seconds per video

## Convert Images to Video (No API needed)

```bash
python images_to_video.py --images img1.png img2.png img3.png --output result.mp4
```

## Next Steps

- Try different prompts
- Experiment with voices (alloy, echo, fable, onyx, nova, shimmer)
- Create longer videos by chaining scenes
- Add music and effects

Need help? Check `README.md` for full docs!

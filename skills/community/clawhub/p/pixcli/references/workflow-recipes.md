# Workflow Recipes

## 1) Image generation kit for a product video

Generate a consistent set of scene images for Remotion assembly:

```bash
# Hero product shot
pixcli image "Studio product shot of [PRODUCT], dramatic lighting, dark reflective surface" -r 16:9 -q high -o hero.png

# Alternate angle
pixcli image "Same [PRODUCT] from 45-degree top-down angle, same lighting" -r 16:9 -o alt-angle.png

# Detail close-up
pixcli image "Close-up detail of [PRODUCT] texture and finish, macro lens" -r 16:9 -o detail.png

# Transparent asset for compositing
pixcli image "[PRODUCT] centered, clean edges" -t -o product-nobg.png

# Lifestyle context
pixcli image "Person using [PRODUCT] in modern office, natural light" -r 16:9 -o lifestyle.png
```

## 2) Image edit chain (enhance + upscale)

```bash
# Start with a generated image
pixcli image "Tech product concept, photorealistic" -o raw.png

# Enhance quality
pixcli edit "Enhance details and improve lighting balance" -i raw.png -o enhanced.png

# Upscale for final delivery
pixcli edit "Upscale to maximum resolution" -i enhanced.png -q high -o final-4k.png
```

## 3) Product marketing video (pixcli + Remotion)

1. Generate scene assets with pixcli:
```bash
pixcli image "Frustrated professional drowning in notifications, dim office" -r 16:9 -o scene-problem.png
pixcli image "Same professional using [PRODUCT], clear desk, bright office" -r 16:9 -o scene-solution.png
pixcli image "[PRODUCT] dashboard showing productivity metrics" -r 16:9 -o scene-metrics.png
pixcli image "[PRODUCT] logo with tagline on dark background" -r 16:9 -t -o scene-cta.png
```

2. Bootstrap Remotion project:
```bash
cp -r assets/templates/aida-classic-16x9 ./product-video
cd ./product-video && npm install
```

3. Add generated images to `public/assets/` and compose scenes in Remotion.

4. Preview and render:
```bash
npx remotion studio    # Preview and iterate
npx remotion render src/index.ts MainComposition out/video.mp4
```

## 4) Multi-format campaign (16:9 + 9:16)

Generate assets in both aspect ratios:

```bash
# Landscape versions (YouTube, website)
pixcli image "[SCENE DESCRIPTION], cinematic wide shot" -r 16:9 -o landscape.png

# Vertical versions (Reels, TikTok, Stories)
pixcli image "[SCENE DESCRIPTION], vertical framing, subject centered" -r 9:16 -o vertical.png
```

Use two Remotion templates:
```bash
cp -r assets/templates/cinematic-product-16x9 ./video-landscape
cp -r assets/templates/mobile-ugc-9x16 ./video-vertical
```

## 5) Full video pipeline (pixcli + Remotion)

End-to-end from brief to rendered video:

1. Generate scene stills:
```bash
pixcli image "Problem scene: overwhelmed professional, cluttered desk" -r 16:9 -q high -o scene-problem.png
pixcli image "Solution scene: same professional using [PRODUCT], clean desk, bright" -r 16:9 -q high -o scene-solution.png
pixcli image "[PRODUCT] dashboard showing key metrics" -r 16:9 -o scene-metrics.png
pixcli image "[PRODUCT] logo on dark background" -r 16:9 -t -o scene-cta.png
```

2. Animate the hero still (use `--audio` for native audio on supported models):
```bash
pixcli video "Camera orbit revealing the product, volumetric light rays" --from scene-solution.png -d 5 -q high -o hero-clip.mp4

# Or with native audio generation
pixcli video "Camera orbit revealing the product, volumetric light rays" --from scene-solution.png -d 5 --audio -o hero-clip-audio.mp4
```

3. Generate voiceover per scene:
```bash
pixcli voice "Tired of drowning in notifications?" -o vo-problem.mp3
pixcli voice "Meet FlowPilot. One dashboard. Zero noise." -o vo-solution.mp3
pixcli voice "Teams using FlowPilot ship 40% faster." -o vo-metrics.mp3
pixcli voice "Start free today at flowpilot.com" -o vo-cta.mp3
```

4. Generate background music:
```bash
pixcli music "Cinematic ambient, builds gradually, positive corporate energy" -d 45 -o music.mp3
```

5. Generate transition SFX:
```bash
pixcli sfx "Smooth cinematic whoosh transition" -d 1 -o whoosh.mp3
```

6. Bootstrap Remotion project:
```bash
cp -r assets/templates/cinematic-product-16x9 ./video
cd ./video && npm install
```

7. Add all assets to `public/`:
```
public/
├── assets/
│   ├── scene-problem.png
│   ├── scene-solution.png
│   ├── scene-metrics.png
│   ├── scene-cta.png
│   └── hero-clip.mp4
└── audio/
    ├── vo-problem.mp3
    ├── vo-solution.mp3
    ├── vo-metrics.mp3
    ├── vo-cta.mp3
    ├── music.mp3
    └── whoosh.mp3
```

8. Compose scenes in Remotion, layering stills, video clips, text, and audio.

9. Render:
```bash
npx remotion render src/index.ts MainComposition out/video.mp4 --codec h264 --crf 18
```

## 6) Job recovery workflow

When video generation takes too long (5-8 minutes for high-quality models), the CLI times out and prints the job ID:

```bash
# The CLI timed out with: "Job abc123 still running. Recover with: pixcli job abc123 --wait"

# Check status
pixcli job abc123

# Wait for completion and download
pixcli job abc123 --wait -o hero-clip.mp4

# Or get JSON status for scripting
pixcli job abc123 --json
```

**Tip:** Long-running video jobs (especially `kling-v3-pro-i2v` at high quality or `pixverse-v6-transition`) are most likely to time out. Always note the job ID from the output.

## 7) Quick social clip (no Remotion)

Fast path for a single-scene social post — no Remotion needed:

```bash
# 1. Generate the hero image
pixcli image "Product hero shot, dramatic lighting" -r 9:16 -q high -o hero.png

# 2. Animate to video
pixcli video "Slow zoom in with subtle light shift" --from hero.png -d 5 -r 9:16 -o clip.mp4

# 3. Generate background music
pixcli music "Lo-fi chill beat, social media vibe" -d 8 -o music.mp3

# 4. Merge with ffmpeg
ffmpeg -i clip.mp4 -i music.mp3 -c:v copy -c:a aac -shortest -y social-post.mp4
```

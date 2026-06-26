---
name: pixcli
version: 2.2.0
description: Creative toolkit for AI agents — generate images, videos, voiceover,
  music, and sound effects, then assemble polished output via Remotion. Uses the
  pixcli CLI for all generation (auto-classifies tasks, enriches prompts, selects
  models). Remotion handles video assembly with 6 bundled templates and 30+ rule
  references. Use when building product videos, social ads, explainers, marketing
  assets, or any visual/audio content pipeline.
allowed-tools: Bash(pixcli *), Bash(npx pixcli *), Bash(npx remotion *),
  Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *), Bash(cp *),
  Bash(cp -r *), Bash(ffmpeg *), Bash(ffprobe *), Read, Write
argument-hint: <command> [options]
metadata:
  openclaw:
    emoji: 🎨
    primaryEnv: PIXCLI_API_KEY
    providerEnv:
      - PIXCLI_API_KEY
    requires:
      env:
        - PIXCLI_API_KEY
      anyBins:
        - node
        - npx
    homepage: https://pixcli.shellbot.sh
    tags:
      - creative
      - image
      - video
      - audio
      - remotion
      - production
---

# pixcli

Creative toolkit for AI agents. Generate images, videos, voiceover, music, and sound effects — then assemble polished output via Remotion.

**Philosophy:** The CLI handles complexity (task classification, prompt enrichment, model selection). You just describe what you want.

## Setup

### 1. Install the CLI

```bash
npm install -g pixcli
```

Or use without installing:

```bash
npx pixcli image "a red fox in a forest"
```

### 2. Authenticate

```bash
export PIXCLI_API_KEY="px_live_..."
```

Get your API key at https://pixcli.shellbot.sh. The key covers all capabilities: images, video, voice, music, and sound effects.

### 3. Verify

```bash
pixcli --version
pixcli image "test: a simple blue circle on white background" -o test.png
```

## Commands

### `pixcli image <prompt>` — Generate images

```bash
pixcli image "Studio product shot of wireless earbuds, soft lighting, white background"
```

| Option | Default | Description |
|--------|---------|-------------|
| `-r, --ratio <ratio>` | `1:1` | Aspect ratio: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3` |
| `-q, --quality <level>` | `standard` | Quality: `draft`, `standard`, `high` |
| `-t, --transparent` | `false` | Transparent background (PNG) |
| `-n, --count <number>` | `1` | Number of images (1-4) |
| `--from <path-or-url>` | — | Source image for image-to-image or reference generation (repeatable, up to 5: `--from a.png --from b.png`) |
| `--search` | `false` | Enable Google Search grounding for real-world accuracy (logos, brands, current events). Only with Nano Banana models |
| `-m, --model <model>` | auto | Specific model ID |
| `-o, --output <path>` | auto | Output file or directory |
| `--json` | `false` | Machine-readable JSON output |
| `--no-enrich` | — | Skip prompt enrichment |

**Models:** `flux-pro`, `flux-dev`, `seedream-v5`, `nano-banana-pro`, `nano-banana-2`, `imagen-4`, `imagen-4-fast`, `gpt-image-1`

### `pixcli edit <prompt>` — Edit images

```bash
pixcli edit "Remove the background" -i product.jpg -o product-nobg.png
```

| Option | Default | Description |
|--------|---------|-------------|
| `-i, --image <path-or-url>` | **required** | Source image (repeatable: `-i a.png -i b.png`) |
| `-q, --quality <level>` | `standard` | Quality: `draft`, `standard`, `high` |
| `-m, --model <model>` | auto | Specific model ID |
| `-o, --output <path>` | auto | Output file or directory |
| `--json` | `false` | Machine-readable JSON output |
| `--no-enrich` | — | Skip prompt enrichment |

**Models:** `seedream-v5-edit`, `phota-enhance`, `rembg`, `recraft-upscale`, `aura-sr`

### `pixcli video <prompt>` — Generate video

```bash
# Image-to-video (recommended: generate still first, then animate)
pixcli video "Slow camera orbit around the product" --from product.png -o reveal.mp4

# Text-to-video (generates image automatically, then animates)
pixcli video "A cat walking through a garden at sunset" -o cat.mp4

# Extend an existing video
pixcli video "The cat jumps over a fence" --from cat.mp4 --extend -o cat-extended.mp4
```

| Option | Default | Description |
|--------|---------|-------------|
| `--from <path-or-url>` | — | Source image (I2V) or video (extend) |
| `--to <path-or-url>` | — | End image — video transitions from `--from` to `--to` (Kling/PixVerse transition models) |
| `--negative <prompt>` | — | Negative prompt describing what to avoid |
| `--audio` | `false` | Enable native audio generation (BGM, SFX, dialogue) on supported models |
| `-d, --duration <seconds>` | `5` | Duration: 1-15 seconds |
| `-r, --ratio <ratio>` | `16:9` | Aspect ratio: `16:9`, `9:16`, `1:1`, `4:3`, `3:4` |
| `-q, --quality <level>` | `standard` | Quality: `draft`, `standard`, `high` |
| `-m, --model <model>` | auto | Specific model ID |
| `-o, --output <path>` | auto | Output file (.mp4) |
| `--json` | `false` | Machine-readable JSON output |
| `--extend` | `false` | Extend the source video instead of I2V |

**Models:** `kling-v3-pro-i2v` (cinematic, best quality), `veo3-i2v` (Google, native audio), `wan-v2-i2v` (cheap, good motion), `minimax-i2v` (fast), `ltx-t2v` (text-to-video, cheap), `veo3-t2v` (text-to-video, premium), `grok-extend-video` (extend), `pixverse-v6-i2v` (I2V with audio, multi-clip, styles, $0.075/sec), `pixverse-v6-t2v` (T2V with audio, multi-clip, styles), `pixverse-v6-transition` (start-to-end frame transition), `pixverse-v6-extend` (video extension with audio)

**Opinionated approach:** Always generate a still first with `pixcli image`, review it, then animate with `pixcli video --from`. This gives you control over the starting frame.

### `pixcli voice <text>` — Text-to-speech

```bash
pixcli voice "Welcome to the future of productivity." -o voiceover.mp3
pixcli voice "Bienvenidos al futuro." --voice Sarah --language spa -o vo-spanish.mp3
```

| Option | Default | Description |
|--------|---------|-------------|
| `--voice <name>` | `Rachel` | Voice preset: Rachel, Aria, Roger, Sarah, Laura, Charlie, George, Callum, River, Liam, Charlotte, Alice, Matilda, Will, Jessica, Eric, Chris, Brian, Daniel, Lily, Bill |
| `--language <code>` | auto | ISO 639-1 language code (eng, spa, fra, deu, jpn, etc.) |
| `-o, --output <path>` | auto | Output file (.mp3) |
| `--json` | `false` | Machine-readable JSON output |

### `pixcli music <prompt>` — Generate music

```bash
pixcli music "Subtle ambient electronic, minimal beats, corporate technology feel" -d 45 -o bg-music.mp3
```

| Option | Default | Description |
|--------|---------|-------------|
| `-d, --duration <seconds>` | `30` | Duration: 3-120 seconds |
| `-o, --output <path>` | auto | Output file (.mp3) |
| `--json` | `false` | Machine-readable JSON output |

### `pixcli sfx <prompt>` — Generate sound effects

```bash
pixcli sfx "Smooth cinematic whoosh transition" -d 1.5 -o whoosh.mp3
pixcli sfx "Soft digital click, subtle UI interaction" -d 0.5 -o click.mp3
```

| Option | Default | Description |
|--------|---------|-------------|
| `-d, --duration <seconds>` | `5` | Duration: 0.5-22 seconds |
| `-o, --output <path>` | auto | Output file (.mp3) |
| `--json` | `false` | Machine-readable JSON output |

### `pixcli job <id>` — Check job status and download results

```bash
# Check status of a job
pixcli job abc123

# Wait for completion and download
pixcli job abc123 --wait -o output.mp4
```

| Option | Default | Description |
|--------|---------|-------------|
| `--wait` | `false` | Wait for the job to complete before returning |
| `-o, --output <path>` | auto | Output file path for downloaded result |
| `--json` | `false` | Machine-readable JSON output |

**Use case:** Recover timed-out jobs. Video generation can take 5-8 minutes — if the CLI times out, it prints the job ID and a recovery command. Run `pixcli job <id> --wait` to pick up where you left off.

### Global options

| Option | Description |
|--------|-------------|
| `--key <api_key>` | Override `PIXCLI_API_KEY` env var |
| `--api-url <url>` | Override API URL (default: `https://pixcli.shellbot.sh`) |
| `--version` | Show CLI version |
| `--help` | Show help |

Read `references/command-reference.md` for the full parameter reference.

---

## Opinionated creative workflow

### The full production pipeline

1. **Generate** scene stills with `pixcli image` — use `-n 4` for variations, pick the best. Use `--search` for real-world accuracy (correct logos, current brands). Use `--from` with multiple images to blend references
2. **Edit** heroes with `pixcli edit` — upscale, remove backgrounds, enhance
3. **Animate** 2-3 hero stills with `pixcli video --from` — cinematic motion for key moments
4. **Generate** voiceover with `pixcli voice` — one file per scene
5. **Generate** background music with `pixcli music` — one track for the full composition
6. **Generate** sound effects with `pixcli sfx` — transition whooshes, UI sounds (use sparingly)
7. **Assemble** everything in Remotion — timing, text, transitions, branding, audio mix
8. **Render** final video with `npx remotion render`

### When to use AI video vs Remotion

**Use `pixcli video` for:**
- Hero moments: product reveals, cinematic openings, emotional beats (3-8s clips)
- Organic motion that's hard to code: water, fire, fabric, hair, camera orbits
- Image-to-video: animate a still into a living scene
- Transition inserts: short clips between Remotion scenes

**Use Remotion for:**
- Text animations, captions, kinetic typography
- Precise timing synced to voiceover
- Brand overlays, logos, consistent color grading
- Data visualizations, metric counters, charts
- Scene transitions (cuts, wipes, dissolves — deterministic)
- Final assembly: compositing AI video clips + stills + audio + text

**The ideal combined workflow:**
1. Generate scene stills with `pixcli image` (consistency via shared style prompts)
2. Animate 2-3 hero stills with `pixcli video --from` (cinematic motion)
3. Generate voiceover + music + SFX
4. Assemble everything in Remotion (timing, text, transitions, audio mix)

### Audio layering strategy

- **Voiceover** at volume 1.0 — clear, intelligible, primary channel
- **Music** at 0.15-0.25 — duck under voiceover, never compete
- **SFX** sparse and purposeful — only when they reinforce movement
- Avoid dense music during problem framing

### Quality tiers

- **`draft`** — Fast iteration, concepting, throwaway tests
- **`standard`** — Good for most production work (default)
- **`high`** — Hero shots, final delivery assets

---

## ffmpeg local editing

Use ffmpeg for quick video/audio edits without a full Remotion project. These run locally — no API calls needed.

### Video operations

```bash
# Trim video (extract 5 seconds starting at 2s)
ffmpeg -i input.mp4 -ss 00:00:02 -to 00:00:07 -c copy trimmed.mp4

# Split video at a timestamp
ffmpeg -i input.mp4 -t 5 -c copy first-half.mp4
ffmpeg -i input.mp4 -ss 5 -c copy second-half.mp4

# Merge videos (create filelist.txt first)
echo "file 'clip1.mp4'" > filelist.txt
echo "file 'clip2.mp4'" >> filelist.txt
ffmpeg -f concat -safe 0 -i filelist.txt -c copy merged.mp4

# Scale video to 1080p
ffmpeg -i input.mp4 -vf "scale=1920:1080" -c:a copy scaled.mp4
```

### Audio operations

```bash
# Add audio track to video
ffmpeg -i video.mp4 -i music.mp3 -c:v copy -c:a aac -shortest output.mp4

# Replace audio track
ffmpeg -i video.mp4 -i new-audio.mp3 -c:v copy -c:a aac -map 0:v -map 1:a output.mp4

# Mix voiceover + music (music ducked to 20%)
ffmpeg -i voiceover.mp3 -i music.mp3 -filter_complex "[1:a]volume=0.2[music];[0:a][music]amix=inputs=2:duration=longest" mixed.mp3

# Extract audio from video
ffmpeg -i video.mp4 -vn -acodec copy audio.aac

# Get media info
ffprobe -v quiet -print_format json -show_streams input.mp4
```

---

## Remotion video production

Remotion is the source of truth for timing, layout, animation, and render. Use `pixcli` to generate the visual and audio assets, then assemble everything in Remotion.

### Bootstrapping a Remotion project

```bash
cp -r assets/templates/cinematic-product-16x9 ./my-video
cd ./my-video && npm install
npx remotion studio     # Preview
npx remotion render src/index.ts MainComposition out/video.mp4  # Render
```

### Templates

| Template | Best for | Aspect |
|----------|----------|--------|
| `aida-classic-16x9` | Product marketing (AIDA framework) | 1920x1080 |
| `cinematic-product-16x9` | Premium product launches | 1920x1080 |
| `saas-metrics-16x9` | B2B SaaS, dashboard metrics | 1920x1080 |
| `mobile-ugc-9x16` | Reels, TikTok, Stories | 1080x1920 |
| `blank-16x9` | Custom projects | 1920x1080 |
| `explainer-16x9` | How-it-works, tutorials | 1920x1080 |

### Integrating AI video clips in Remotion

Use `OffthreadVideo` for AI-generated clips inside Remotion compositions:

```tsx
import { OffthreadVideo, Sequence, Audio, Img, staticFile } from "remotion";

// AI video clip as a hero moment
<Sequence from={0} durationInFrames={150}>
  <OffthreadVideo src={staticFile("assets/hero-reveal.mp4")} />
</Sequence>

// AI-generated still as background
<Sequence from={150} durationInFrames={120}>
  <Img src={staticFile("assets/scene-solution.png")} style={{ width: "100%", height: "100%" }} />
</Sequence>

// Voiceover + music
<Audio src={staticFile("audio/voiceover.mp3")} volume={1} />
<Audio src={staticFile("audio/music.mp3")} volume={0.2} />
```

### Remotion principles

- Keep all Remotion packages on the same pinned version
- Transitions: 8-18 frames, purposeful (not decorative)
- Load fonts explicitly with `@remotion/google-fonts`
- Always run `npm run verify` before `npm run render`
- Load reference rules from `references/remotion-rules/` as needed

Read `references/remotion-playbook.md` for detailed Remotion implementation guidance.

---

## Output convention

- `pixcli` downloads generated files to the current directory (or path specified with `-o`)
- Use `--json` for machine-readable output (pipe to `jq` or parse in scripts)
- All operations are synchronous from the CLI perspective (the CLI handles async polling internally)
- Video jobs may take 1-8 minutes (the CLI shows progress). If a job times out, use `pixcli job <id> --wait` to recover

## References

### Creative guidance
- `references/command-reference.md` — Full parameter docs for all pixcli commands
- `references/creative-guidelines.md` — Quality standards for productions
- `references/prompt-cookbook.md` — Proven prompt patterns for every task
- `references/workflow-recipes.md` — End-to-end recipe examples
- `references/ancillary-assets.md` — Asset generation strategy for Remotion scenes

### Remotion
- `references/remotion-playbook.md` — Remotion implementation guide
- `references/template-showcase.md` — Template selector guide
- `references/remotion-rules-index.md` — Index of 30+ Remotion rule files
- `references/remotion-rules/` — Detailed rules (animations, audio, text, transitions, etc.)

### Templates
- `assets/templates/aida-classic-16x9/`
- `assets/templates/cinematic-product-16x9/`
- `assets/templates/saas-metrics-16x9/`
- `assets/templates/mobile-ugc-9x16/`
- `assets/templates/blank-16x9/`
- `assets/templates/explainer-16x9/`

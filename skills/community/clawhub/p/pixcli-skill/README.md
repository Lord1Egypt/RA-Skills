# pixcli

Creative toolkit for AI agents. Generate images, edit visuals, and assemble polished video output via Remotion — powered by the `pixcli` CLI.

## Quick start

```bash
# 1. Install
npm install -g pixcli

# 2. Authenticate
export PIXCLI_API_KEY="px_live_..."

# 3. Generate an image
pixcli image "Product shot of wireless earbuds on marble surface" -o earbuds.png

# 4. Edit it
pixcli edit "Remove the background" -i earbuds.png -o earbuds-nobg.png

# 5. Build a video (Remotion)
cp -r assets/templates/cinematic-product-16x9 ./my-video
cd ./my-video && npm install && npx remotion studio
```

## What's in the box

### 7 CLI commands
| Command | What it does |
|---------|-------------|
| `pixcli image` | Generate images (auto-classifies, enriches prompts, selects best model). `--search` for real-world accuracy, `--from` repeatable for multi-image references |
| `pixcli edit` | Edit images (upscale, remove background, enhance, style transfer, compose) |
| `pixcli video` | Generate video (text-to-video, image-to-video, video extension, start-to-end transitions). `--audio` for native audio, `--to` for end frames |
| `pixcli voice` | Generate voiceover from text (multiple voices, 70+ languages) |
| `pixcli music` | Generate background music from a text prompt |
| `pixcli sfx` | Generate sound effects from a text description |
| `pixcli job` | Check job status and download results. Recover timed-out video jobs |

### 6 Remotion templates
| Template | Use case |
|----------|----------|
| `aida-classic-16x9` | Product marketing (AIDA framework) |
| `cinematic-product-16x9` | Premium product launches |
| `saas-metrics-16x9` | B2B SaaS, dashboard-style |
| `mobile-ugc-9x16` | Reels, TikTok, Stories (vertical) |
| `blank-16x9` | Minimal starter for custom projects |
| `explainer-16x9` | How-it-works, tutorials, walkthroughs |

### 30+ Remotion rules
Full reference library covering animations, audio, text, transitions, captions, 3D, charts, and more.

## Architecture

```
User / AI Agent
  │
  ├── pixcli image "..."  ──→  pixcli API  ──→  Image Models (FLUX, Seedream, Nano Banana, Imagen, GPT Image)
  ├── pixcli edit "..." -i ──→  pixcli API  ──→  Edit Models (Seedream Edit, Phota, Rembg, Upscale)
  ├── pixcli video "..."  ──→  pixcli API  ──→  Video Models (Kling, Veo3, Wan, MiniMax, LTX, Grok)
  ├── pixcli voice "..."  ──→  pixcli API  ──→  TTS (ElevenLabs)
  ├── pixcli music "..."  ──→  pixcli API  ──→  Music Generation (ElevenLabs)
  ├── pixcli sfx "..."    ──→  pixcli API  ──→  SFX Generation (ElevenLabs)
  │
  └── Remotion (video assembly)
        ├── Generated images + AI video clips as scene assets
        ├── Text animations, transitions, branding
        ├── Audio layering (voiceover + music + SFX)
        └── Final render to MP4
```

## The opinionated workflow

1. **Generate** scene stills with `pixcli image` — use shared style prompts for consistency
2. **Edit** winners with `pixcli edit` — upscale, remove backgrounds, enhance
3. **Animate** hero moments with `pixcli video --from` — short 3-8s AI video clips
4. **Narrate** with `pixcli voice` + `pixcli music` + `pixcli sfx` — voiceover, background music, transitions
5. **Assemble** in Remotion — timing, text, transitions, branding, audio layering
6. **Render** final video — `npx remotion render`

## Authentication

```bash
export PIXCLI_API_KEY="px_live_..."
```

Get your key at https://pixcli.shellbot.sh. Covers all image generation and editing.

`OPENROUTER_API_KEY` works as a fallback but a dedicated key is recommended.

## What's new in v2.2

- `pixcli image` — `--from` is now repeatable for multi-image references; new `--search` flag for Google Search grounding (real logos, brands, current events); `reference_generation` task type auto-classifies reference vs edit intent
- `pixcli video` — New `--to` flag for start-to-end frame transitions; `--negative` for negative prompts; `--audio` for native audio generation; duration expanded to 1-15s; 4 new PixVerse v6 models (i2v, t2v, transition, extend)
- `pixcli job` — New command to check job status and recover timed-out video jobs

### v2.1
- `pixcli video` — Text-to-video, image-to-video, and video extension (Kling, Veo3, Wan, MiniMax, LTX, Grok)
- `pixcli voice` — Text-to-speech voiceover with multiple voices and 70+ languages
- `pixcli music` — AI background music generation from text prompts (3-120s)
- `pixcli sfx` — Sound effects generation from text descriptions (0.5-22s)

## Requirements

- Node.js 18+
- `PIXCLI_API_KEY` environment variable

## License

Proprietary. Part of the ShellBot platform.

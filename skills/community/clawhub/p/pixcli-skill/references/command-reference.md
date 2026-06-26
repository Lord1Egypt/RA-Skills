# Command Reference — pixcli

Complete parameter documentation for pixcli commands and Remotion workflows.

---

## `pixcli image <prompt>` — Generate Images

```
Usage: pixcli image <prompt> [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<prompt>` | string | **required** | Text description of the image to generate |
| `-r, --ratio <ratio>` | enum | `1:1` | Aspect ratio: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3` |
| `-q, --quality <level>` | enum | `standard` | Quality: `draft`, `standard`, `high` |
| `-t, --transparent` | flag | `false` | Generate with transparent background (PNG) |
| `-n, --count <number>` | int | `1` | Number of images: 1-4 |
| `--from <path-or-url>` | string | — | Source image for image-to-image or reference generation (repeatable, up to 5: `--from a.png --from b.png`). The API auto-classifies whether images are references for new creation or targets for editing |
| `--search` | flag | `false` | Enable Google Search grounding for real-world accuracy (correct logos, current events, real brands). Only works with Nano Banana models |
| `-m, --model <model>` | string | auto | Specific model ID (uses advanced endpoint, bypasses auto-classification) |
| `-o, --output <path>` | string | auto | Output file or directory path |
| `--json` | flag | `false` | Machine-readable JSON output to stdout |
| `--no-enrich` | flag | — | Skip prompt enrichment (only with `--model`) |

**How it works:** Without `--model`, the API auto-classifies your prompt (icon, photo, illustration, product shot, etc.), enriches it for the best model, and routes it through an optimal pipeline. With `--model`, you bypass classification and go direct. When `--from` is provided, the API uses a `reference_generation` task type — the LLM classifier decides whether images are references for new creation or targets for editing. The enriched prompt and classification are shown in CLI output for debugging.

**Models:**

| Model ID | Backend | Best for |
|----------|---------|----------|
| `flux-pro` | fal | High quality, general purpose |
| `flux-dev` | fal | Balanced quality/speed |
| `seedream-v5` | fal | Fast + quality, commercial-ready |
| `nano-banana-pro` | google | Best consistency, text rendering, multi-image |
| `nano-banana-2` | google | Fast iteration, cheap, great for concepting |
| `imagen-4` | google | Highest quality |
| `imagen-4-fast` | google | Fast variant of Imagen 4 |
| `gpt-image-1` | openrouter | OpenAI's image model |

---

## `pixcli edit <prompt>` — Edit Images

```
Usage: pixcli edit <prompt> -i <image> [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<prompt>` | string | **required** | Text description of the edit |
| `-i, --image <path-or-url>` | string | **required** | Source image (repeatable: `-i a.png -i b.png`, up to 5) |
| `-q, --quality <level>` | enum | `standard` | Quality: `draft`, `standard`, `high` |
| `-m, --model <model>` | string | auto | Specific model ID |
| `-o, --output <path>` | string | auto | Output file or directory path |
| `--json` | flag | `false` | Machine-readable JSON output |
| `--no-enrich` | flag | — | Skip prompt enrichment (only with `--model`) |

**How it works:** The API classifies your edit intent (upscale, background removal, style transfer, enhancement, etc.) and routes to the appropriate model. Multiple images enable multi-reference edits like style transfer or composition.

**Models:**

| Model ID | Backend | Best for |
|----------|---------|----------|
| `seedream-v5-edit` | fal | General editing |
| `phota-enhance` | fal | Enhancement + upscale |
| `rembg` | fal | Background removal |
| `recraft-upscale` | fal | High-quality upscale |
| `aura-sr` | fal | 4x super-resolution |

---

## `pixcli video <prompt>` — Generate Video

```
Usage: pixcli video <prompt> [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<prompt>` | string | **required** | Text description of the video to generate |
| `--from <path-or-url>` | string | — | Source image (I2V) or video (extend) |
| `--to <path-or-url>` | string | — | End image — video transitions from start frame (`--from`) to end frame (`--to`). Supported by Kling and PixVerse transition models |
| `--negative <prompt>` | string | — | Negative prompt describing what to avoid in the generated video |
| `--audio` | flag | `false` | Enable native audio generation (BGM, SFX, dialogue) on supported models |
| `-d, --duration <seconds>` | int | `5` | Duration 1-15s |
| `-r, --ratio <ratio>` | enum | `16:9` | Aspect ratio: `16:9`, `9:16`, `1:1`, `4:3`, `3:4` |
| `-q, --quality <level>` | enum | `standard` | Quality: `draft`, `standard`, `high` |
| `-m, --model <model>` | string | auto | Specific model ID |
| `-o, --output <path>` | string | auto | Output file |
| `--json` | flag | `false` | Machine-readable JSON output |
| `--no-enrich` | flag | — | Skip prompt enrichment |
| `--extend` | flag | `false` | Extend source video instead of I2V |

**How it works:** Without `--from`, generates text-to-video. With `--from` pointing to an image, generates image-to-video (I2V). With `--from` pointing to a video and `--extend`, extends the source clip. The API auto-selects the best model unless `--model` is specified.

**Models:**

| Model ID | Backend | Best for |
|----------|---------|----------|
| `kling-v3-pro-i2v` | fal | Cinematic I2V, best quality |
| `veo3-i2v` | fal (Google) | Premium I2V, native audio |
| `wan-v2-i2v` | fal | Budget I2V, good motion |
| `minimax-i2v` | fal | Fast I2V |
| `ltx-t2v` | fal | Budget text-to-video |
| `veo3-t2v` | fal (Google) | Premium text-to-video |
| `grok-extend-video` | fal (xAI) | Video extension |
| `pixverse-v6-i2v` | PixVerse | Image-to-video with audio, multi-clip, styles ($0.075/sec) |
| `pixverse-v6-t2v` | PixVerse | Text-to-video with audio, multi-clip, styles |
| `pixverse-v6-transition` | PixVerse | Start-to-end frame transition (built-in first/last image interpolation) |
| `pixverse-v6-extend` | PixVerse | Video extension with audio |

---

## `pixcli job <id>` — Check Job Status

```
Usage: pixcli job <id> [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<id>` | string | **required** | Job ID to check |
| `--wait` | flag | `false` | Wait for the job to complete before returning |
| `-o, --output <path>` | string | auto | Output file path for downloaded result |
| `--json` | flag | `false` | Machine-readable JSON output |

**How it works:** Checks the status of any previously submitted job and optionally downloads the result. When a video job times out (video generation can take 5-8 minutes), the CLI prints the job ID and a recovery command. Use `pixcli job <id> --wait` to resume waiting and download the result once ready.

---

## `pixcli voice <text>` — Generate Voiceover

```
Usage: pixcli voice <text> [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<text>` | string | **required** | Text to speak (1-5000 chars) |
| `--voice <name>` | string | `Rachel` | Voice preset |
| `--language <code>` | string | — | ISO 639-1 language code |
| `-o, --output <path>` | string | auto | Output .mp3 file |
| `--json` | flag | `false` | Machine-readable JSON output |

---

## `pixcli music <prompt>` — Generate Music

```
Usage: pixcli music <prompt> [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<prompt>` | string | **required** | Text description of the music |
| `-d, --duration <seconds>` | int | `30` | Duration 3-120s |
| `-o, --output <path>` | string | auto | Output .mp3 file |
| `--json` | flag | `false` | Machine-readable JSON output |

---

## `pixcli sfx <prompt>` — Generate Sound Effects

```
Usage: pixcli sfx <prompt> [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<prompt>` | string | **required** | Text description of the sound effect |
| `-d, --duration <seconds>` | float | `5` | Duration 0.5-22s |
| `-o, --output <path>` | string | auto | Output .mp3 file |
| `--json` | flag | `false` | Machine-readable JSON output |

---

## Global Options

These apply to all commands:

| Option | Description |
|--------|-------------|
| `--key <api_key>` | Override `PIXCLI_API_KEY` environment variable |
| `--api-url <url>` | Override `PIXCLI_API_URL` (default: `https://pixcli.shellbot.sh`) |
| `--version` | Show CLI version |
| `--help` | Show help |

---

## JSON Output Format

When using `--json`, output goes to stdout:

**Success:**
```json
{
  "job_id": "abc123",
  "status": "completed",
  "files": [
    {
      "path": "studio-product-shot.png",
      "width": 1024,
      "height": 1024,
      "mime_type": "image/png"
    }
  ],
  "model": "flux-pro",
  "cost": 100000,
  "elapsed_ms": 12340
}
```

**Error:**
```json
{
  "error": "Insufficient credits",
  "status": 402,
  "elapsed_ms": 234
}
```

---

## Remotion Workflow

### Bootstrap a project

```bash
# Copy template
cp -r assets/templates/cinematic-product-16x9 ./my-video
cd ./my-video

# Install dependencies
npm install

# Verify setup
npm run verify
npm run typecheck
```

### Preview in studio

```bash
npx remotion studio
```

### Render to video

```bash
npx remotion render src/index.ts MainComposition out/video.mp4
```

### Render options

```bash
npx remotion render src/index.ts MainComposition out/video.mp4 \
  --codec h264 \
  --crf 18 \
  --concurrency 50%
```

### Templates

| Name | Aspect | Best for |
|------|--------|----------|
| `aida-classic-16x9` | 1920x1080 | Product marketing (AIDA) |
| `cinematic-product-16x9` | 1920x1080 | Premium product launches |
| `saas-metrics-16x9` | 1920x1080 | B2B SaaS dashboards |
| `mobile-ugc-9x16` | 1080x1920 | Reels, TikTok, Stories |
| `blank-16x9` | 1920x1080 | Custom projects |
| `explainer-16x9` | 1920x1080 | Tutorials, how-it-works |

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
| `--vectorize` | flag | `false` | After generating, also vectorize the result into a clean SVG (great for logos/icons). Final asset is the `.svg`. Ignored with `--model` (advanced endpoint) |
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
| `gpt-image-2` | openai-direct | Best text rendering in images |
| `gpt-image-2-or` | openrouter | GPT Image 2 via OpenRouter (fallback) |
| `flux-vto` | fal | Virtual try-on (garment on person) |

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

## `pixcli vectorize <image>` — Image → SVG

```
Usage: pixcli vectorize <image> [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<image>` | string | **required** | Source image — local file, URL, or pixcli asset hash |
| `-o, --output <path>` | string | auto | Output file or directory path (e.g. `logo.svg`) |
| `-m, --model <model>` | string | `arrow-1.1` | Quiver vectorization model id |
| `--auto-crop` | flag | `false` | Trim surrounding empty/background space before vectorizing |
| `--size <px>` | int | — | Resize the longest side (128–4096) before vectorizing |
| `--json` | flag | `false` | Machine-readable JSON output |
| `--no-wait` | flag | `false` | Submit and return immediately |

**How it works:** Converts a raster image into a clean, scalable **SVG** via Quiver AI (`arrow-1.1`). Best for logos, icons, and flat/clean graphics. Cost scales with image complexity — pixcli reserves an estimate and settles the exact Quiver cost after the run. To go from a text prompt straight to an SVG, use `pixcli image "…" --vectorize`.

---

## `pixcli video <prompt>` — Generate Video

```
Usage: pixcli video <prompt> [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<prompt>` | string | **required** | Text description of the video to generate |
| `--from <path-or-url>` | string | — | Source image (I2V) or video (extend) |
| `--to <path-or-url>` | string | — | End image — video transitions from start frame (`--from`) to end frame (`--to`). Supported by transition models (veo31-lite-transition, kling-o3-pro-transition, pixverse-v6-transition) |
| `--negative <prompt>` | string | — | Negative prompt describing what to avoid in the generated video |
| `--audio` | flag | `false` | Enable native audio generation (BGM, SFX, dialogue) on supported models |
| `-d, --duration <seconds>` | int | `5` | Duration 1-15s |
| `-r, --ratio <ratio>` | enum | `16:9` | Aspect ratio: `16:9`, `9:16`, `1:1`, `4:3`, `3:4` |
| `--resolution <res>` | enum | auto | Output resolution: `480p`, `720p`, `1080p`, `4k`. Supported by Seedance, Veo 3.1, Grok Imagine (480p/720p), and Luma Ray (540p/720p/1080p — price 1x/2x/4x) models; affects cost |
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
| `veo-3.1` | google-veo | **Recommended default** — T2V + I2V, 720p/1080p/4K |
| `veo-3.1-fast` | google-veo | Fast variant of Veo 3.1 |
| `veo-3.1-lite` | google-veo | Budget variant of Veo 3.1 |
| `seedance-2-t2v` | fal | ByteDance cinematic motion, T2V |
| `seedance-2-i2v` | fal | ByteDance cinematic motion, I2V |
| `kling-v3-pro-i2v` | fal | Cinematic I2V, best quality |
| `wan-v2-i2v` | fal | Budget I2V, good motion |
| `minimax-i2v` | fal | Fast I2V |
| `ltx-t2v` | fal | Budget text-to-video |
| `grok-imagine-i2v` | fal (xAI) | Fast stylized I2V (480p/720p) — also picked when the prompt mentions "grok", "xai", or "x" |
| `luma-ray-3-2-t2v` | fal (Luma) | Director-mode T2V — precise camera control, loop, 12 aspect ratios (540p/720p/1080p) |
| `luma-ray-3-2-i2v` | fal (Luma) | Director-mode I2V — start frame + optional reference images |
| `grok-extend-video` | fal (xAI) | Video extension |
| `ltx-extend-video` | fal | Video extension (budget) |
| `pixverse-v6-i2v` | fal | Image-to-video with audio, styles |
| `pixverse-v6-t2v` | fal | Text-to-video with audio, styles |
| `veo31-lite-transition` | fal | Start-to-end frame transition (Veo 3.1 Lite) |
| `kling-o3-pro-transition` | fal | Start-to-end frame transition (Kling) |
| `pixverse-v6-transition` | fal | Start-to-end frame transition (PixVerse) |
| `pixverse-v6-extend` | fal | Video extension with audio |

---

## `pixcli removebg <video>` — Remove Video Background

```
Usage: pixcli removebg <video> [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<video>` | string | **required** | Source video — local file, URL, or pixcli asset hash |
| `--color <color>` | enum | `Transparent` | Replacement background: `Transparent`, `Black`, `White`, `Gray`, `Red`, `Green`, `Blue`, `Yellow`, `Cyan`, `Magenta`, `Orange` |
| `-f, --format <container>` | enum | `webm_vp9` | Output container+codec: `webm_vp9`, `mp4_h265`, `mp4_h264`, `mov_h265`, `mov_proresks`, `mkv_h265`, `mkv_h264`, `mkv_vp9`, `avi_h264`, `gif` |
| `--no-audio` | flag | — | Drop the source audio track (preserved by default) |
| `--max-duration <seconds>` | int | `30` | Upper bound on the source length (1-300) — caps the credit reservation; the charge settles to the actual video length |
| `-o, --output <path>` | string | auto | Output file or directory |
| `--json` | flag | `false` | Machine-readable JSON output |
| `--no-wait` | flag | `false` | Submit and return immediately |
| `--webhook <url>` | string | — | URL to POST on completion |
| `--webhook-bearer <token>` | string | — | Bearer token sent as the `Authorization` header when posting `--webhook` |

**How it works:** Sends the video to Bria VRMBG 3.0 (`bria-video-bg-removal`, $0.042/s of video) via `POST /api/v1/video/bg-removal`. The default `Transparent` + `webm_vp9` output carries a real alpha channel, so the result can be composited over any other video, image, or background. `Transparent` requires an alpha-capable container (`webm_vp9`, `mov_proresks`, or `gif`) — the API rejects other combinations with a 400. Works on talking heads, podcasts, product videos, commercials, and cinematic footage.

---

## `pixcli dialogue <script>` — Multi-Speaker TTS

> **For a full podcast from a topic, use [`pixcli podcast`](#pixcli-podcast-topic--full-podcast-episodes) instead.** `dialogue` is the low-level primitive — use it only when you already have the exact speaker lines and want nothing added (no scripting, music, cover, or share page).

Generate a conversation between up to 2 speakers. Each speaker gets a distinct voice and lines are rendered in order, then merged into a single audio file.

```
Usage: pixcli dialogue [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--speaker <Name:Voice>` | string | **required** | Define a speaker with a voice preset (repeatable, max 2). Example: `--speaker "Alice:Rachel"` |
| `--line <Speaker:text>` | string | **required** | A line of dialogue attributed to a speaker (repeatable). Example: `--line "Alice:Hello, welcome!"` |
| `--script <file.json>` | string | — | Load speakers and lines from a JSON file instead of `--speaker`/`--line` flags |
| `--language <code>` | string | — | ISO 639-1 language code |
| `-o, --output <path>` | string | auto | Output .mp3 file |
| `--json` | flag | `false` | Machine-readable JSON output |

**Example:**
```bash
pixcli dialogue \
  --speaker "Host:Rachel" \
  --speaker "Guest:Josh" \
  --line "Host:Welcome to the show. Today we're talking about AI." \
  --line "Guest:Thanks for having me — it's a fascinating topic." \
  --line "Host:Let's dive right in." \
  -o interview.mp3
```

**Script file format (JSON):**
```json
{
  "speakers": [{ "name": "Host", "voice": "Rachel" }, { "name": "Guest", "voice": "Josh" }],
  "lines": [
    { "speaker": "Host", "text": "Welcome to the show." },
    { "speaker": "Guest", "text": "Thanks for having me." }
  ]
}
```

---

## `pixcli podcast [topic]` — Full podcast episodes

> **Alias: `pixcli sipcast`.** "sipcast" is ShellBot's brand for these AI podcasts; `pixcli sipcast` is identical to `pixcli podcast`. API: `POST /api/v1/audio/sipcast` (alias of `/audio/podcast`). Share pages: `/sip/<job_id>` (old `/pod/<job_id>` redirects there).

A higher-level wrapper over `dialogue`. From a topic, pixcli writes a tagged,
language-aware, duration-targeted **2-speaker** script (gemini-3.5-flash), speaks
it with Gemini multi-speaker TTS, and mixes in intro/outro/bed background music —
returning **one finished `.mp3` (44.1 kHz stereo, 192 kbps)**.

```
Usage: pixcli podcast [topic] [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `[topic]` | string | — | Episode topic / request. Required unless `--script` is given with `--mode respect/improve`. |
| `--mode <mode>` | string | `auto` | `auto` (write fresh), `improve` (polish a rough draft), `respect` (keep the user's wording — only split into turns + add delivery tags) |
| `--language <code>` | string | auto | Spoken-content language. **Omit to auto-detect from the topic.** `es` forces **Spain/Castilian** (never Latin-American), pinned at the voice/accent level. Expression tags stay English regardless. |
| `-m, --minutes <n>` | number | `5` | Target spoken length, 1–10 (the writer targets ~150 wpm word budget) |
| `--speaker <spec>` | string | host+expert | A preset id (`host_warm`, `host_sharp`, `expert_calm`, `skeptic`, `storyteller`, `analyst`, `newcomer`, `futurist`, `veteran`, `comedian`) **or** `"Name:Voice[:persona]"`. Repeatable, max 2. |
| `--tone <text>` | string | — | Overall show tone |
| `--title <text>` | string | auto | Preferred episode title |
| `--script <path>` | string | — | For `improve`/`respect`: `.txt` transcript or `.json` `[{speaker,text,note?}]` |
| `--no-search` | flag | — | Real-time Google Search grounding is **ON by default**; pass this to disable |
| `--url <url>` | string | — | Source URL to read/summarise (repeatable; Gemini URL-context tool) |
| `--music <ref>` | string | `warm` | Mood (`warm`,`lofi`,`ambient`,`cinematic`,`corporate`,`upbeat`,`jazzy`,`newsy`), a library preset id, a 32-hex WAV asset hash, or `none` |
| `--intro <sec>` / `--outro <sec>` | number | `4` / `5` | **Loud** intro/outro music sting lengths (0 disables) |
| `--bed-gain <0-1>` | number | `0.06` | Music level UNDER speech — faint so it never fights the voice |
| `--no-cover` | flag | — | Skip the auto square cover image |
| `--cover-style <style>` | enum | auto | Cover art style: auto (varies per episode), editorial, minimal, vivid, photographic, retro, 3d, typographic, collage, handdrawn, photoreal, neon, watercolor, isometric |
| `--cover-prompt <text>` / `--cover-date <text>` | string | auto | Full custom cover prompt (overrides --cover-style) / printed date (default today) |
| `--learn-languages <codes>` | string | — | Comma-separated native languages to precompute a **bilingual learning overlay** for (reading view + tap-to-translate over the original audio), e.g. `es,fr`. Paid on your wallet at creation. |
| `--voiceover-languages <codes>` | string | — | Comma-separated languages to **re-narrate** into as separate audio variants, e.g. `fr,de`. Independent of `--learn-languages`. |
| `-o, --output <path>` | string | auto | Output `.mp3` file (44.1 kHz stereo; `--wav` also keeps a WAV master) |
| `--private` / `--no-publish` | flag | — | Podcasts publish **public + permanent by default**; `--private` requires your key, `--no-publish` skips publishing |
| `--json` | flag | `false` | Machine-readable JSON output |

**Notes**
- Gemini multi-speaker TTS caps at **2 voices** per episode — pick 2 presets/voices.
- **Music** is loud only for the first ~4s and last ~5s; under speech it stays faint (`bed_gain` ~0.06). Beds come from a permanent library — list them with `GET /api/v1/audio/podcast/presets`. Custom beds must be WAV (the in-worker mixer reads PCM directly).
- **Expression tags are always English** (`[enthusiastic]`, `[laughing]`, `[agreement]`, `[amazement]`, …) even when the dialogue is in another language; they are delivery cues, not spoken. In `auto`/`improve` the writer picks them — you don't pass them.
- **Cover + recover-by-id**: each episode also produces a square cover (Nano Banana 2 — title + date render as real text), published public + permanent. Audio (if published) and cover share the job-id stem: `…/p/pod-<job_id>.mp3` and `…/p/pod-<job_id>-cover.png`. Built for daily/weekly per-user shows — rebuild any episode's URLs from its `job_id`.

**Examples**
```bash
# Auto-written 4-minute episode, default host+expert, warm bed
pixcli podcast "the future of espresso" -m 4 -o ep1.mp3 --json

# Spanish (Spain/Castilian), preset speakers, cinematic music
pixcli podcast "la historia del cómic" --language es \
  --speaker host_warm --speaker skeptic --music cinematic -o ep-es.mp3

# Custom voices + personas, published forever
pixcli podcast "indie game design" \
  --speaker "Mara:Kore:dry technical host" --speaker "Bea:Puck:excited newcomer" \
  -o ep.mp3   # public + permanent by default; add --private or --no-publish to change

# Multilanguage: precompute a learning overlay + a re-narrated variant up front
pixcli sipcast "the science of sleep" --learn-languages es,fr --voiceover-languages de -o sleep.mp3
```

### Multilanguage subcommands (on an existing sipcast, by id)

Two **independent, opt-in** features — a learning overlay does NOT re-record audio,
a voiceover does NOT add the reading overlay. Both are **Meterkey-authed and paid by
the caller**; the public share page is read-only and only shows languages already
generated (it never generates on its own), so **pre-generate what you'll want**.

```
pixcli sipcast learn <id> --native <code>       # bilingual reading overlay (keeps original audio)
pixcli sipcast voiceover <id> --to <code>       # re-narrate as a separate audio variant
```

| Command | Required | Description |
|---------|----------|-------------|
| `sipcast learn <id> --native <code>` | `--native` | Adds a bilingual reading overlay (native ↔ episode language) with tap-a-word glossary over the original audio. Opens at `/sip/<id>?learn=1&native=<code>`. Runs as a pollable job (cached pairs return instantly); add `--no-wait` to return before it finishes. API: `POST /api/v1/audio/podcast/:id/learn`. |
| `sipcast voiceover <id> --to <code>` | `--to` | Re-narrates the episode into another language as a new linked variant (own page + transcript). Optional `--speaker`, `--private`/`--no-publish`, `--no-wait`. API: `POST /api/v1/audio/podcast/:id/voiceover`. |

---

## `pixcli tryon <prompt>` — Virtual Try-On

Composite a garment onto a person image using AI try-on (powered by `flux-vto`).

```
Usage: pixcli tryon [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--person <path-or-url>` | string | **required** | Full-body or half-body photo of the person |
| `--garment <path-or-url>` | string | **required** | Flat-lay or product shot of the garment |
| `-p, --prompt <text>` | string | — | Optional guidance (e.g. `"outdoor setting, bright daylight"`) |
| `-o, --output <path>` | string | auto | Output .png file |
| `--json` | flag | `false` | Machine-readable JSON output |

**Example:**
```bash
pixcli tryon \
  --person customer-photo.jpg \
  --garment hoodie-product.png \
  -p "casual urban setting, natural light" \
  -o result.png
```

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

> **Building a podcast/interview/narrated show? Use [`pixcli podcast`](#pixcli-podcast-topic--full-podcast-episodes), not chained `voice` calls.** `voice` produces a single self-contained voiceover for text you already have — it never scripts, casts multiple voices, scores, or assembles segments.

```
Usage: pixcli voice <text> [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<text>` | string | **required** | Text to speak (1-5000 chars) |
| `--voice <name>` | string | `Rachel` | Voice preset name (see voice table below) or a cloned voice_id |
| `--engine <engine>` | enum | `elevenlabs` | TTS engine: `elevenlabs` (default) or `gemini` (steerable, expressive) |
| `--clone <name>` | string | — | Name to assign to a cloned voice (use with `--sample`). Creates an ElevenLabs instant voice from the provided samples, then speaks with it |
| `--sample <path-or-url>` | string | — | Audio sample for voice cloning (repeatable, 1–5 samples). Requires `--clone` |
| `--language <code>` | string | — | ISO 639-1 language code (en, es, fr, de, ja) |

**Voices.** English presets (ElevenLabs premades): `Rachel` (default), `Aria`, `Sarah`, `Laura`, `Charlie`, `George`, `River`, `Alice`, `Matilda`, `Jessica`, `Eric`, `Chris`, `Brian`, `Daniel`, `Lily`, `Bill`…

For **Spanish content always use a native Spain/Castilian preset** — the English presets speak Spanish with a neutral/LATAM accent:

| Preset | Gender | Vibe |
|--------|--------|------|
| `Eva` | female | warm, soft narration (Spanish default) |
| `Carolina` | female | natural, clear conversational |
| `Lydia` | female | energetic, confident, informative |
| `Aitana` | female | young, warm, expressive |
| `Elena` | female | young, lively narration |
| `Carmelo` | male | mature, deep narration |
| `Dani` | male | young, dynamic conversational |
| `Emilio` | male | warm, solid, informative |
| `David` | male | young, confident, friendly |

Passing `--language es` without `--voice` auto-selects `Eva`. The full catalogue (including the 30 Gemini steerable voices) is at `GET /api/v1/audio/voices`.

```bash
pixcli voice "Bienvenidos a nuestra plataforma." --voice Carmelo --language es -o intro-es.mp3
```
| `-o, --output <path>` | string | auto | Output .mp3 file |
| `--json` | flag | `false` | Machine-readable JSON output |

**Voice cloning example:**
```bash
pixcli voice "Welcome to our platform. Let's get you started." \
  --clone "MyBrand" --sample ceo-sample-1.mp3 --sample ceo-sample-2.mp3 \
  -o welcome-vo.mp3
```

---

## `pixcli music <prompt>` — Generate Music

```
Usage: pixcli music <prompt> [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<prompt>` | string | **required** | Text description of the music |
| `-d, --duration <seconds>` | int | `30` | Duration 3-120s |
| `-m, --model <model>` | string | auto | Specific model ID |
| `-o, --output <path>` | string | auto | Output .mp3 file |
| `--json` | flag | `false` | Machine-readable JSON output |

**Models:** Default is `lyria-3-pro` (fal). `elevenlabs-music` (fal) is also available.

---

## `pixcli sfx <prompt>` — Generate Sound Effects

```
Usage: pixcli sfx <prompt> [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<prompt>` | string | **required** | Text description of the sound effect |
| `-d, --duration <seconds>` | float | `5` | Duration 0.5-22s |
| `-m, --model <model>` | string | auto | Specific model ID |
| `-o, --output <path>` | string | auto | Output .mp3 file |
| `--json` | flag | `false` | Machine-readable JSON output |

**Models:** Default is `elevenlabs-sfx` (ElevenLabs sound effects v2, fal).

---

## Publishing Flags

These flags are available on all generation commands (`image`, `edit`, `video`, `voice`, `music`, `sfx`, `dialogue`, `tryon`). They publish the output asset to a shareable URL on `https://pixcli.shellbot.sh`. **`podcast` publishes public + permanent by default** (use `--private` / `--no-publish` to opt out).

## `pixcli publish <id>` — Change share visibility

Change the visibility of an already-generated resource without regenerating.

| Option | Description |
|--------|-------------|
| `<id>` | Job id (publishes all its assets) — or an asset hash with `--asset` |
| `--private` | Publish privately (requires your API key to fetch) |
| `--unpublish` | Remove the public/private links |
| `--asset` | Treat `<id>` as a 32-char asset hash |
| `--ttl <days>` | Expire after N days (default: never) |
| `--name <slug>` | Friendly URL slug |

```bash
pixcli publish <job_id>              # public (default)
pixcli publish <job_id> --private    # owner-only
pixcli publish <job_id> --unpublish  # remove links
```

API: `POST /api/v1/publish` with `{ "job_id" | "asset", "scope": "public"|"private"|"unpublished", "permanent"?, "ttl_days"?, "name"? }`. Podcasts reuse the deterministic `pod-<job_id>` ids so the `/pod/<job_id>` page keeps working.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--publish` | flag | `false` | Publish the asset to a public shareable URL (no auth required to fetch) |
| `--publish-private` | flag | `false` | Publish privately — requires your API key to fetch the asset |
| `--publish-ttl <days>` | int | `60` | How long the published URL stays live (max 365 days). **All published URLs expire.** |
| `--publish-name <name>` | string | auto | Slug for the published URL. Published URLs follow the pattern: `https://pixcli.shellbot.sh/p/<slug>-<id>` |

**Example:**
```bash
pixcli image "Hero product shot on marble, dramatic lighting" \
  -q high --publish --publish-name "hero-shot" --publish-ttl 90 -o hero.png
# → https://pixcli.shellbot.sh/p/hero-shot-abc123
```

> All published assets expire. Set `--publish-ttl` appropriately for your use case.

---

## Global Options

These apply to all commands:

| Option | Description |
|--------|-------------|
| `--key <api_key>` | Override `METERKEY_API_KEY` environment variable |
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
  "elapsed_ms": 12340,
  "canva_url": "https://pixcli.shellbot.sh/c/link/<one-time-token>",
  "published": [
    { "kind": "image", "url": "https://pixcli.shellbot.sh/p/hero-shot-abc123", "scope": "public", "expires_at": "2026-08-10T00:00:00Z" }
  ]
}
```

What each key gives you:

| Key | What it is |
|-----|------------|
| `files[]` | The assets downloaded to local disk (path + dimensions + mime) — use these for local work (ffmpeg, Remotion, uploads) |
| `published[]` | Public URLs (when publish flags were set): `url` is the link to share, `scope` is `public`/`private`, `expires_at` its expiry. Reuse these URLs directly as inputs to chain commands |
| `canva_url` | One-click, pre-authenticated dashboard link — opens the job in the pixcli web dashboard for a human to view/iterate. Present on `image`, `edit`, `video`, `voice`, `music`, `sfx`, and `job`; give it to the user alongside the share link |
| `job_id` / `model` / `cost` | Recovery handle (`pixcli job <id>`), the model that ran, and the settled cost in micro-credits |

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

---
name: openfun
description: Create viral short-form videos using AI. Analyze trending patterns, generate original content that hits the same beats, render and download MP4s. Use when the user wants to create TikTok, YouTube Shorts, or Instagram Reels content, find trending video patterns, or automate video content creation.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["openfun"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "openfun-cli",
              "bins": ["openfun"],
              "label": "Install OpenFun CLI (npm)",
            },
          ],
      },
  }
---

# OpenFun — AI Video Factory

Create original viral short-form videos by reverse-engineering what works.

**OpenFun is NOT a video clipper.** It analyzes viral patterns (hook timing, pacing, emotional arc) and generates original content that hits the same beats.

## Setup

```bash
npm install -g openfun-cli
openfun login
```

Login opens a browser for auth. Token persists in `~/.openfun/config.json`.

## Commands

### Find trending patterns

```bash
openfun trends --niche <niche> --count <n>
```

Returns trending content patterns in a niche. Use this to decide what to create.

### Remix a trend

```bash
openfun remix <trend-id> \
  --brand "Brand Name" \
  --tone casual \
  --hook "Your custom hook" \
  --cta "Your call to action"
```

Creates an original script based on a trending pattern, customized for the user's brand.

Options:
- `--brand` — Brand or creator name
- `--tone` — casual, professional, humorous, motivational, educational
- `--hook` — Custom hook text (optional, auto-generated if omitted)
- `--cta` — Call to action (optional)
- `--niche` — Override niche from trend

### Render a video

```bash
openfun render <remix-id>
```

Kicks off video rendering. Returns a job ID. Rendering takes 30-90 seconds.

### Check video status

```bash
openfun videos
```

Lists all videos with their status (rendering, ready, failed).

### Download a video

```bash
openfun download <video-id> -o output.mp4
```

Downloads a rendered video as MP4.

### Account info

```bash
openfun account
```

Shows plan, usage, and remaining credits.

## Typical Workflow

```bash
# 1. Find what's trending in your niche
openfun trends --niche fitness --count 5

# 2. Pick a trend and remix it
openfun remix abc123 --brand "FitLife" --tone motivational

# 3. Render the video
openfun render def456

# 4. Check status
openfun videos

# 5. Download when ready
openfun download ghi789 -o fitness-video.mp4
```

## Agent Tips

- All commands output JSON by default (add `--pretty` for human-readable)
- Exit codes: 0 = success, 1 = user error, 2 = API error
- Errors go to stderr, data to stdout
- No interactive prompts — fully automatable
- Run `openfun trends` across multiple niches to find the best opportunities
- Batch multiple remixes, then render them all

## Plans

- **Free:** 5 remixes/month + 3 watermarked videos/month
- **Pro ($19/mo):** 50 remixes + 20 videos + no watermark
- **Scale ($49/mo):** Unlimited remixes + 100 videos + priority rendering

## Links

- Website: https://www.openfun.ai
- CLI repo: https://github.com/andyluvis/openfun-cli

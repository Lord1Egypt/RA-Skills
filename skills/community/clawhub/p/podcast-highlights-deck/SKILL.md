---
name: podcast-highlights-deck
description: "Create a highly visual, editorial long-scroll HTML microsite from a podcast episode. Use when the user gives a podcast link (Apple Podcasts/Spotify/RSS/direct MP3/YouTube) and asks for: (1) 8–12 curated highlights (not full transcript), (2) per-highlight playable original audio clips, (3) multilingual language toggle (e.g., English/Japanese/Chinese) applied globally across UI and content, (4) premium typography-led layout inspired by an editorial deck with a sticky table-of-contents rail."
---

# Podcast Highlights Deck

(Internal skill id: `podcast-highlights-deck`)

## What it creates

Create a premium editorial long-scroll highlight deck with a sticky TOC rail, multilingual toggle, and original audio clips.

---

## Workflow


## Inputs

- **podcast_url**: episode page URL (Apple/Spotify/RSS/YouTube/direct MP3)
- **languages**: list of language codes, e.g. `en`, `ja`, `zh`

## Output

- A **static website** (Vite build) with:
  - editorial hero (no full-bleed podcast artwork)
  - sticky left rail: metadata + language toggle + table of contents
  - 8–12 highlight sections
  - per-highlight audio clip playback (original audio)
  - global language switching (no mixed-language UI)

## Workflow (execute in order)

### 1) Acquire audio (source-of-truth)

Prefer a **direct audio URL** (RSS `<enclosure>`). Recommended approach:

1. Use `search_web` to find the show’s RSS feed (queries like: `"<show name>" RSS feed`, or the Apple show id + RSS).
2. Use `get_web_page_contents` to fetch the RSS XML.
3. Parse RSS to locate the exact episode and extract:
   - title
   - publish date
   - duration (if present)
   - cover image
   - **enclosure mp3 URL**

If RSS is unavailable:
- If YouTube exists, use `yt-dlp` to download audio.
- If a platform blocks direct audio access, ask the user for the RSS link or direct mp3.

Download audio to a working folder (example):

- `podcast_work/episode.mp3`

### 2) Transcribe with timestamps

Primary:
- Run `anygen-speech-to-text episode.mp3 -o transcript -f json,md,srt`.

Fallback (if the tool fails):
- Split audio into chunks with `ffmpeg` (10 min chunks)
- Use OpenAI Whisper (`whisper-1`) with `response_format="verbose_json"`
- Merge segments by adding time offsets

You need a machine-readable file like:
- `transcript/episode_verbose.json` containing segments with `start`, `end`, `text`

### 3) Curate 8–12 highlights (do NOT dump transcript)

Selection philosophy:
- Prefer fewer, stronger highlights.
- Only use quotes that exist in the transcript.

For each highlight, produce:
- `id` (h1..h12)
- `start` + `end` timestamps in seconds (from transcript)
- title (translate later)
- quote (English, exact or lightly cleaned)
- context (1 sentence)
- takeaway (editorial interpretation)

### 4) Translate + global UI copy

For every supported language:
- Translate **titles**, **context**, **takeaway**, and **quote** (transcreation; keep meaning + tone).

Important behavior:
- In non-English modes, show **translated quote as primary**.
- Preserve a connection to English:
  - show “Original (English)” as a secondary expandable panel.

Also translate *all* UI strings:
- hero framing
- sidebar labels
- buttons (“Play clip”, “Back to top”, etc.)
- closing section labels

### 5) Clip original audio per highlight

Use the bundled script:

- `python scripts/clip_audio.py --audio episode.mp3 --highlights highlights.json --out-dir site_assets`

Conventions:
- add ~2s padding before/after for natural listening
- output:
  - `site_assets/audio/h1.mp3` …

### 6) Build the site with the bundled editorial template

Use `website_init` to create a new site project.

Then copy assets into the project:
- `src/assets/highlights.json`
- `src/assets/cover.jpg`
- `src/assets/audio/*.mp3`

Then replace template files from this skill:
- `assets/template/Home.tsx` → `src/pages/Home.tsx`
- `assets/template/index.css` → `src/index.css`
- `assets/template/index.html` → project `index.html`

Notes:
- The template expects `highlights.json` schema similar to `assets/template/highlights.schema.example.json`.
- Ensure `document.documentElement.dataset.lang` is set from the language toggle.

### 7) Bundle and deliver

Run `website_bundle` and deliver the generated `dist/index.html`.

## Template assets in this skill

- `assets/template/Home.tsx`: editorial layout + global language switching + expandable English original
- `assets/template/index.css`: Swiss‑brutalist paper/ink theme + language font stacks
- `assets/template/index.html`: Google Fonts includes Instrument Serif, Manrope, IBM Plex Mono, and Noto JP/SC
- `assets/template/highlights.schema.example.json`: reference structure

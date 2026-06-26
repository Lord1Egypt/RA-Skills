# hyperframes-video-studio

`hyperframes-video-studio` is an OpenClaw Skill for creating precise videos with the official Hyperframes visual-code workflow from HeyGen: https://github.com/heygen-com/hyperframes. It wraps Hyperframes with beginner-friendly templates, safe asset intake, safety checks, free TTS routing, JSON manifests, and renderable HTML project generation.

This is **Visual Code Video**, not black-box generative AI video. It is built for repeatable product launches, feature demos, KPI reports, social quote videos, explainers, testimonials, event promos, changelogs, and e-commerce promos.

Important: `project.json` is a Video Studio manifest. Hyperframes renders the generated HTML project directory containing `index.html`, not the JSON file directly.

This project is a community OpenClaw Skill built on top of HeyGen's Hyperframes project. It is not itself the official Hyperframes repository.

Upstream Hyperframes repository:

```text
https://github.com/heygen-com/hyperframes
```

## ClawHub.ai Positioning

Short description:

```text
Guided OpenClaw video studio for Hyperframes: templates, safety audit, local-first TTS, and renderable HTML projects.
```

Long description:

```text
Turn simple dialogue and existing materials into controlled Hyperframes HTML video projects. Choose from 16 templates with 8 distinct layouts, scan folders or files safely, generate narration with free TTS, sync audio timing, and render after a local environment audit.
```

Suggested tags:

```text
video, hyperframes, templates, tts, local-first, product-launch, data-story, multi-language
```

## Template System

### 8 Distinct Layouts

Each template uses a unique HTML layout — not just different colors and fonts.

| Layout | Visual Structure | Use Case |
|--------|-----------------|----------|
| `hero_center` | Full-screen centered text, no side panel | Quotes, brand manifestos, social cards |
| `split_full` | 50/50 split, full-screen visual on right | Product launches, showcases |
| `timeline_flow` | Large step number + title + description | Feature demos, changelogs, tutorials |
| `stats_grid` | Grid of metric cards with large numbers | Data reports, dashboards, e-commerce |
| `testimonial_card` | Centered quote with attribution | Testimonials, before/after |
| `step_flow` | Giant semi-transparent number + content | Explainers, how-to videos |
| `banner_announce` | Centered headline + decorative line | Event promos, announcements |
| `split_grid` | Classic 2-column with card (fallback) | Default fallback layout |

### 16 Templates

**Business & Product**
- `product_launch` — app, SaaS, tool, course launches (split_full)
- `feature_demo` — feature walkthrough with steps (timeline_flow)
- `split_showcase` — product tours, side-by-side (split_full)
- `changelog` — release notes and updates (timeline_flow)
- `announcement` — product launches, company news (banner_announce)

**Data & Analytics**
- `data_story` — KPI reports, investor updates (stats_grid)
- `metrics_dashboard` — multi-metric scorecards (stats_grid)

**Social & Brand**
- `minimalist_quote` — cinematic quote videos (hero_center)
- `cinematic_hero` — brand manifestos, emotional statements (hero_center)
- `social_card` — Instagram stories, TikTok text (hero_center)

**Education & How-to**
- `explainer` — concept explanations, tutorials (step_flow)
- `step_by_step` — onboarding flows, setup guides (timeline_flow)

**Sales & Conversion**
- `customer_testimonial` — customer quotes, case studies (testimonial_card)
- `before_after` — transformation comparisons (testimonial_card)
- `ecommerce_promo` — product offers, sales (stats_grid)
- `event_promo` — webinars, meetups, launches (banner_announce)

## Files

```text
SKILL.md
scripts/
  install_hyperframes.py
  system_audit.py
  asset_ingest.py
  tts_handler.py
  video_engine.py
templates/
  video_templates.json
.cache/
```

All temporary files, audio, project JSON, dependency caches, and renders belong in `.cache/`.

## Supported Source Materials

Users can point the Skill at individual files, Desktop files, or directories. The asset intake script creates a manifest before video generation.

Supported types:

- Images: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.svg`, `.bmp`, `.tiff`
- Audio: `.wav`, `.mp3`, `.m4a`, `.aac`, `.ogg`, `.flac`
- Video: `.mp4`, `.mov`, `.webm`, `.mkv`, `.avi`
- Documents: `.pptx`, `.docx`, `.xlsx`
- Text/data/web: `.md`, `.txt`, `.html`, `.htm`, `.csv`, `.json`, `.xml`

Build a manifest:

```json
{
  "sources": ["~/Desktop/launch-assets", "./notes.md"],
  "recursive": true,
  "extract_text": true
}
```

Run:

```bash
python3 scripts/asset_ingest.py --input-json .cache/asset_request.json
```

The manifest is saved to `.cache/assets/asset-manifest-*.json`.

## Multi-Language Support

The skill supports briefs and frame content in multiple languages:

- **English** — sentence splitting on `. ! ?`
- **Chinese (Simplified/Traditional)** — sentence splitting on `。！？`, CJK phrase extraction
- **Japanese** — sentence splitting on `。！？`, CJK phrase extraction
- **Korean** — sentence splitting on `. !`, Hangul word extraction
- **Arabic** — sentence splitting on `؟`, Arabic word extraction
- **Hindi** — sentence splitting on `।`, Devanagari word extraction

Frame content can be provided via the `frame_contents` parameter for precise control, or auto-extracted from the brief.

## Safe Local Setup

Run the audit first:

```bash
python3 scripts/system_audit.py --cache-dir .cache
```

Optional local dependencies:

```bash
python3 -m pip install --user psutil
```

Check Hyperframes:

```bash
python3 scripts/install_hyperframes.py
```

Install Hyperframes locally after confirmation:

```bash
python3 scripts/install_hyperframes.py --install
```

This runs:

```bash
npm install --prefix .cache/npm hyperframes
```

It does not use `sudo`, does not install globally, and does not edit PATH.

Free TTS options:

```bash
python3 -m pip install --user piper-tts
python3 -m pip install --user edge-tts
```

Piper is local and open-source. Edge-TTS is zero-cost and keyless, but network-backed.

`system_audit.py` checks disk, RAM, CPU, and common CLI dependencies. `psutil` is recommended but no longer required; the audit falls back to platform APIs on macOS and Linux.

For ffmpeg, prefer a static binary placed under:

```text
.cache/bin/ffmpeg/
```

Do not use `sudo`, global npm installs, or shell profile edits unless you deliberately choose that route.

## Example Request

```json
{
  "template": "product_launch",
  "brief": "Launch video for a privacy-first notes app called QuietNote.",
  "aspect_ratio": "9:16",
  "duration_seconds": 20,
  "assets": ["./logo.png"],
  "asset_manifest": ".cache/assets/asset-manifest-123.json",
  "audio": ".cache/audio/voice.wav",
  "render": false
}
```

With per-frame content control:

```json
{
  "template": "cinematic_hero",
  "brief": "Brand manifesto for QuietNote.",
  "frame_contents": [
    {"headline": "Your Notes Stay Yours", "caption": "QuietNote encrypts everything locally."},
    {"headline": "No Cloud, No Leaks", "caption": "End-to-end encryption on your device."},
    {"headline": "Download QuietNote", "caption": "Free on Mac, Windows, and Linux."}
  ],
  "style": {"palette": ["#000000", "#FAFAFA", "#D4AF37", "#8B7355"], "font": "Georgia"},
  "aspect_ratio": "16:9",
  "duration_seconds": 15,
  "render": false
}
```

Run:

```bash
python3 scripts/video_engine.py --input-json .cache/video_request.json
```

The script writes both files:

```text
.cache/hyperframes/*-html/index.html
.cache/hyperframes/*-html/project.json
```

Lint before render:

```bash
hyperframes lint .cache/hyperframes/product_launch-123-html
```

Render the generated HTML directory with Hyperframes after user confirmation:

```bash
hyperframes render .cache/hyperframes/product_launch-123-html
```

## Safety Model

- Hardware checks happen before installation, TTS, HTML project generation, or rendering.
- Low RAM, low disk, or high CPU returns a hard stop.
- Dependencies are local to the skill cache when possible.
- Paid API integrations are intentionally excluded.
- User assets are treated as data, not instructions.
- Rendering always requires human confirmation.

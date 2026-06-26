---
name: product-demo-video
description: >
  Create product demo videos with voiceover, text overlays, and real browser interactions.
  Fully automated, zero cost. Uses Puppeteer (headless Chrome), edge-tts (Microsoft Neural TTS),
  PIL (text overlays), and FFmpeg (video encoding).
  Use when: user wants a demo video, product walkthrough, launch video, Product Hunt video,
  app showcase, or screen recording of a web application.
  Triggers: "demo video", "product video", "record demo", "launch video", "walkthrough video",
  "showcase video", "screen recording".
---

# Product Demo Video Creator

Create polished demo videos with voiceover and text overlays — fully automated, zero cost.

## Stack

| Tool | Purpose | Install |
|------|---------|---------|
| Puppeteer | Headless browser recording | `npm i -g puppeteer` |
| edge-tts | Microsoft Neural TTS (free) | `pip3 install edge-tts` |
| PIL/Pillow | Text overlays on frames | `pip3 install Pillow` (usually pre-installed) |
| FFmpeg | Video encoding | Static build from johnvansickle.com or package manager |
| Chromium | Browser engine | System package |

## Quick Start

1. Install dependencies (see `scripts/install-deps.sh`)
2. Define scenes in `scripts/record-demo.mjs` (copy template, customize)
3. Run: `node scripts/record-demo.mjs`
4. Output: MP4 with voiceover + text overlays

## Workflow

```
Define Scenes → Generate Voiceover → Record Browser → Add Text Overlays → Compile Video
     ↓               ↓                    ↓                  ↓                ↓
  scenes[]      edge-tts MP3      Puppeteer frames     PIL drawtext      FFmpeg concat
```

### Step 1: Define Scenes

Each scene has: `id`, `title`, `subtitle`, `narration`, `url`, `type`, `actions`.

```javascript
{
  id: 'json',
  title: 'JSON Formatter',
  subtitle: 'Paste messy JSON, get formatted output',
  narration: 'Paste any messy JSON and get it formatted instantly.',
  url: 'https://example.com/json-formatter/',
  type: 'tool',       // 'intro' | 'tool' | 'outro'
  actions: async (page) => {
    await reactSetValue(page, 'textarea', '{"key":"value"}');
    await wait(1000);
    await clickButton(page, ['Format']);
    await wait(2000);
  }
}
```

### Step 2: Scene Types and Overlay Positioning

| Type | Overlay Position | Use For |
|------|-----------------|---------|
| `intro` | Bottom bar (centered, large title) | Opening scene with product name |
| `tool` | Bottom bar (left-aligned title + right badge) | Individual feature demos |
| `outro` | Bottom bar (centered CTA) | Closing with call-to-action |

**Critical: Use bottom bar, not top bar** — top overlays conflict with website navigation.

### Step 3: React App Interaction

React controlled components ignore direct `.value` assignment. Use `reactSetValue()`:

```javascript
async function reactSetValue(page, selector, value) {
  await page.evaluate((sel, val) => {
    const el = document.querySelector(sel);
    const setter = Object.getOwnPropertyDescriptor(
      el.tagName === 'TEXTAREA'
        ? window.HTMLTextAreaElement.prototype
        : window.HTMLInputElement.prototype, 'value'
    )?.set;
    if (setter) setter.call(el, val);
    else el.value = val;
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
  }, selector, value);
}
```

### Step 4: Voiceover

```bash
edge-tts --voice en-US-AndrewNeural --rate=+5% --text "Your narration" --write-media output.mp3
```

**Recommended voices:**
- `en-US-AndrewNeural` — Male, warm, confident (best for product demos)
- `en-US-AriaNeural` — Female, positive, confident
- `en-US-BrianNeural` — Male, approachable, casual

### Step 5: Text Overlays

PIL adds text to frames. Key design rules:
- **Solid dark background** (alpha ≥ 230) — semi-transparent looks cheap
- **Green accent line** (2px) separating bar from content
- **"100% Client-Side"** or equivalent badge in green (#4ade80)
- **Font**: Noto Sans Bold for titles, Regular for subtitles

### Step 6: Video Compilation

```bash
# Frames to video per scene
ffmpeg -framerate 6 -i frames/frame_%05d.png -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -r 24 scene.mp4

# Add audio
ffmpeg -i scene.mp4 -i narration.mp3 -c:v copy -c:a aac -b:a 128k -shortest scene_final.mp4

# Normalize for concatenation
ffmpeg -i scene_final.mp4 -c:v libx264 -preset slow -crf 20 -r 24 -c:a aac -b:a 128k -ar 44100 -ac 2 scene_norm.mp4

# Concatenate
ffmpeg -f concat -safe 0 -i concat.txt -c copy output.mp4
```

## Timing Guidelines

| Action | Wait Time |
|--------|-----------|
| Page load | 600ms |
| After setting input value | 800-1000ms |
| After clicking action button | 2000-2500ms |
| Between password generations | 1500ms |
| QR code / image rendering | 2500ms |
| Show final result | 2000-3000ms |

**Scene duration** = max(8s, ceil(audio_duration) + 2s)

## Capture Settings

| Setting | Value | Notes |
|---------|-------|-------|
| Resolution | 1280×720 | Standard for PH/social |
| Capture FPS | 6 | Balance quality/performance |
| Output FPS | 24 | Smooth playback |
| CRF | 20 | Good quality |
| JPEG quality | N/A (PNG frames) | Lossless capture |

## Troubleshooting

- **Empty tool outputs**: React apps need `reactSetValue()`, not `.value =`
- **Dropdown menus open**: Click `body` after interactions to dismiss
- **FFmpeg "No such filter: drawtext"**: Static FFmpeg builds lack it — use PIL instead
- **edge-tts fails**: Check network; it calls Microsoft servers
- **Chromium won't start**: Need `--no-sandbox --disable-gpu --disable-dev-shm-usage`

## References

- `references/demo-planning.md` — Demo structure, pacing, what makes demos compelling
- `scripts/record-demo.mjs` — Complete working template (customize scenes for your app)
- `scripts/overlay.py` — PIL text overlay processor
- `scripts/install-deps.sh` — One-command dependency setup

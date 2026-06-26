# Demo Planning Guide

## Demo Structure

### 1. Hook (5-10s)
Open with product name, tagline, and core value prop. Show the homepage.

### 2. Core Tools (30-60s)
Show 4-6 key features, each 6-12 seconds:
- Navigate to tool → Input data → Show output → Next
- **Always show output** — empty states kill demos

### 3. Closing CTA (5-8s)
Scroll homepage to show breadth, end with URL and tagline.

**Total: 45-75 seconds** (PH sweet spot: under 60s)

## Timing Rules

| Action | Wait (ms) |
|--------|-----------|
| Page load settle | 600 |
| After setting input | 800-1000 |
| After clicking button | 2000-2500 |
| Complex rendering (QR, charts) | 2500 |
| Show final result | 2000-3000 |

**Scene duration** = max(8s, ceil(narration_audio) + 2s)

## Narration Tips

- **One sentence per concept** — don't cram
- **Spell out abbreviations** for TTS: "S H A 256" not "SHA-256"
- **End each scene's narration before the scene ends** — silence at end is fine
- **Keep total narration under 2 min** — viewers drop off fast

## Common Mistakes

- ❌ Showing empty/placeholder outputs (tool looks broken)
- ❌ Top text overlays that overlap with website navigation
- ❌ Semi-transparent backgrounds (use alpha ≥ 230)
- ❌ Setting React input `.value` directly (use reactSetValue)
- ❌ Not waiting long enough after button clicks
- ❌ Leaving dropdown menus open when capturing
- ❌ Using FFmpeg drawtext filter with static builds (use PIL)

## Voice Selection (edge-tts)

```bash
# List all voices
edge-tts --list-voices

# Test a voice
edge-tts --voice en-US-AndrewNeural --text "Hello world" --write-media test.mp3
```

| Voice | Gender | Tone | Best For |
|-------|--------|------|----------|
| en-US-AndrewNeural | Male | Warm, confident | Product demos |
| en-US-BrianNeural | Male | Casual, sincere | Dev tool demos |
| en-US-AriaNeural | Female | Positive, confident | SaaS demos |
| en-US-AvaNeural | Female | Friendly, caring | Consumer apps |

## Overlay Design

### Color Scheme
- Bar background: `(10, 10, 10, 235)` — near-black, solid
- Accent line: `(74, 222, 128)` — green, 2px
- Title: white
- Subtitle: white @ 85% opacity
- Badge text: green `#4ade80`

### Layout
- Bottom bar height: 75px (tools), 150-170px (intro/outro)
- Title font: 36px bold (tools), 44px bold (intro)
- Subtitle: 18px regular
- Badge: 16px regular, right-aligned (tools only)

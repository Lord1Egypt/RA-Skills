---
name: nano-banana-2-runcomfy
displayName: "🫧 Nano Banana 2 — Pro Pack on RunComfy"
description: >
  Nano Banana 2 on RunComfy. Nano Banana 2 is Google's flash-tier
  text-to-image model in the Gemini family — fast iteration, predictable
  framing, in-image typography rendering, optional web-grounded context.
  This skill calls Nano Banana 2 through the RunComfy CLI: `runcomfy run
  google/nano-banana-2/text-to-image`. Nano Banana 2 is the right Nano
  Banana variant for marketing drafts, social thumbnails, and batch
  variants. Triggers on "nano banana", "nano-banana", "nano banana 2",
  "nano-banana-2", "Google Nano Banana", "Gemini image", or any explicit
  ask to generate with Nano Banana.
emoji: "🫧"
homepage: https://www.runcomfy.com
license: MIT
clawdis:
  requires:
    bins:
      - runcomfy
    env:
      - RUNCOMFY_TOKEN
    config:
      - ~/.config/runcomfy
---

# 🫧 Nano Banana 2 — Pro Pack on RunComfy

[runcomfy.com](https://www.runcomfy.com/?utm_source=clawhub&utm_medium=skill&utm_campaign=nano-banana-2-runcomfy) · [docs](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=nano-banana-2-runcomfy) · [Nano Banana 2 model page](https://www.runcomfy.com/models/google/nano-banana-2?utm_source=clawhub&utm_medium=skill&utm_campaign=nano-banana-2-runcomfy)

**Nano Banana 2** is the flash-tier text-to-image model in Google's Gemini family. This skill generates images with Nano Banana 2 hosted on the RunComfy Model API — `runcomfy run google/nano-banana-2/text-to-image` from your terminal, no Google API key, no GPU rental.

## What Nano Banana 2 is

Nano Banana 2 is Google's second-generation flash-tier image model — the iteration-speed-first variant in the Nano Banana line. Three properties make Nano Banana 2 distinct:

- **Rapid Nano Banana iteration.** Nano Banana 2 is the fastest path to a draft in the Nano Banana family. A Nano Banana 2 generation lands in seconds rather than tens of seconds, which makes Nano Banana 2 the right Nano Banana for marketing brainstorming, A/B variants, and batch ideation.
- **Predictable Nano Banana framing.** Nano Banana 2 holds composition stable across small prompt edits — change one descriptor, Nano Banana keeps the rest. This makes Nano Banana 2 ideal for refining a single hero image without redrafting it from scratch.
- **In-image typography on Nano Banana 2.** Nano Banana 2 renders quoted text inside the image with strong fidelity for short headlines, brand marks, and poster-style copy. When you put `"AURA"` in the Nano Banana 2 prompt, the literal word appears in the image — Nano Banana doesn't paraphrase or scramble.

Nano Banana 2 also exposes an optional **web-grounded context** flag (`enable_web_search`) for image generation that references current events or real entities. The Nano Banana web grounding adds latency and cost; off by default.

## When Nano Banana 2 is the right choice

Pick Nano Banana 2 when any of these is true:

- You want **rapid Nano Banana drafts** — social thumbnails, batch variants, ideation rounds. Nano Banana 2 is built for this speed.
- You're producing **in-image typography** — quoted headlines, brand marks, poster copy. Nano Banana 2 renders text predictably.
- You're iterating **one Nano Banana hero image** through small prompt edits — Nano Banana 2 keeps composition stable across rounds.
- You need **web-grounded Nano Banana imagery** referencing current events or real-world entities — Nano Banana 2 supports this via `enable_web_search`.
- The user explicitly asked for **Nano Banana 2** / **nano-banana-2** / **Google Nano Banana** — route to this Nano Banana variant regardless.

## Nano Banana 2 vs Nano Banana Pro

The Nano Banana family has two production tiers. Pick the right Nano Banana variant based on intent:

- **Nano Banana 2** (this skill) — flash tier. Fast Nano Banana iteration, marketing drafts, social thumbnails, batch ideation, in-image typography.
- **Nano Banana Pro** (separate skill) — pro tier. Hyperrealistic Nano Banana portraits, maximum Nano Banana detail, slower per-call but higher fidelity.

If the user said just "Nano Banana" without specifying 2 vs Pro, default to Nano Banana 2 for ideation, batches, and typography work; default to Nano Banana Pro for portrait fidelity.

## Prerequisites

1. **RunComfy CLI** — `npm i -g @runcomfy/cli`
2. **RunComfy account** — `runcomfy login` opens a browser device-code flow.
3. **CI / containers** — set `RUNCOMFY_TOKEN=<token>` instead of `runcomfy login`.

## Endpoint + input schema

### `google/nano-banana-2/text-to-image`

This is the Nano Banana 2 text-to-image endpoint. The Nano Banana 2 edit endpoint runs on a separate template not covered here.

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `prompt` | string | yes | — | Subject-first description for Nano Banana 2. |
| `num_images` | int | no | 1 | 1–4. Use 4 for Nano Banana ideation rounds. |
| `seed` | int | no | 0 | Reuse for reproducible Nano Banana 2 output. |
| `aspect_ratio` | enum | no | `auto` | 11 values: `auto`, `21:9`, `16:9`, `3:2`, `4:3`, `5:4`, `1:1`, `4:5`, `3:4`, `2:3`, `9:16`. |
| `resolution` | enum | no | `1K` | `0.5K` (Nano Banana drafts), `1K` (default), `2K` (final), `4K` (max). |
| `output_format` | enum | no | `png` | `png`, `jpeg`, `webp`. |
| `safety_tolerance` | int | no | 4 | 1 (strict) – 6 (permissive). |
| `limit_generations` | bool | no | true | Limit each Nano Banana prompt round to one generation. |
| `enable_web_search` | bool | no | false | Adds Nano Banana web grounding (extra cost + latency). |

For Nano Banana 2 image edit (preserve subject + apply changes), see the sibling [`nano-banana-edit`](../nano-banana-edit) skill.

## How to invoke Nano Banana 2

**Default Nano Banana 2 draft (1K, square, png):**

```bash
runcomfy run google/nano-banana-2/text-to-image \
  --input '{"prompt": "<Nano Banana prompt>"}' \
  --output-dir <absolute/path>
```

**Nano Banana 2 vertical 4-up batch for ideation:**

```bash
runcomfy run google/nano-banana-2/text-to-image \
  --input '{
    "prompt": "<Nano Banana prompt>",
    "num_images": 4,
    "aspect_ratio": "9:16",
    "resolution": "0.5K"
  }' \
  --output-dir <absolute/path>
```

**Final Nano Banana 2 at 2K with seed lock:**

```bash
runcomfy run google/nano-banana-2/text-to-image \
  --input '{
    "prompt": "<Nano Banana prompt>",
    "resolution": "2K",
    "aspect_ratio": "16:9",
    "seed": 42
  }' \
  --output-dir <absolute/path>
```

**Web-grounded Nano Banana 2 (current event / real entity):**

```bash
runcomfy run google/nano-banana-2/text-to-image \
  --input '{
    "prompt": "<Nano Banana prompt referencing a real-world event from this week>",
    "enable_web_search": true
  }' \
  --output-dir <absolute/path>
```

## Prompting Nano Banana 2 — what works

Nano Banana 2 responds to specific prompting patterns better than naive prose. Apply these for sharper Nano Banana output.

**Subject-first declarative grammar.** "A cinematic close-up portrait of an American woman standing under neon lights in rainy Tokyo, shallow depth of field, reflective wet streets, ultra-detailed, realistic skin texture" — primary subject first, then action, environment, style, camera. Nano Banana 2 reads early tokens with more weight; front-load the subject.

**Exact text quoting for in-image typography.** "The label reads 'AURA' in clean bold sans-serif, centered, white on black" — quote the literal characters Nano Banana should render. Specify placement and font style. Don't say "with the brand name on it" and hope Nano Banana figures it out.

**Consistent seeds for Nano Banana refinement.** Lock `seed` when iterating a single Nano Banana prompt across small variants — keeps Nano Banana composition stable so you can compare apples to apples.

**Web-grounding sparingly.** Turn on `enable_web_search` only when the Nano Banana prompt names current events or real entities. Adds latency + cost; off by default.

**Don't conflict styles for Nano Banana.** "minimalist + ornate + retro + cyberpunk" cancels in Nano Banana output. Pick 1–2 anchors.

**Nano Banana 2 anti-patterns:**
- Trying to verbally describe a stable subject identity in Nano Banana → use the Nano Banana edit endpoint with image refs instead.
- Asking Nano Banana for resolutions outside the 4 tiers → 422.
- Aspect ratios outside the 11 supported Nano Banana values → 422.
- Non-quoted in-image text → unpredictable Nano Banana rendering.

## Where Nano Banana 2 shines

| Use case | Why Nano Banana 2 |
|---|---|
| **Marketing draft thumbnails (batch of 4)** | Nano Banana 2 fast iteration at 0.5K, then promote winner to 2K |
| **Social-platform-native** | Nano Banana 2 wide aspect ratio support including 9:16, 4:5, 21:9 |
| **In-image typography for posters / cards** | Nano Banana 2 predictable text rendering when characters are quoted |
| **Web-grounded current-event imagery** | Nano Banana 2 `enable_web_search` integrates fresh info |
| **Reproducible Nano Banana variant testing** | Strong Nano Banana seed + consistent framing |

## Sample Nano Banana 2 prompts (verified to produce strong results)

**Cinematic Nano Banana portrait (page example):**

```
A cinematic close-up portrait of an American woman standing under neon
lights in rainy Tokyo, shallow depth of field, reflective wet streets,
ultra-detailed, realistic skin texture
```

**Brand-asset card with quoted text (Nano Banana typography):**

```
A minimalist 16:9 product card: a matte black ceramic mug centered on a
soft warm-grey paper background, rim highlight from upper-left, the
headline "Brewed Quietly" in clean bold sans-serif top-right, balanced
negative space below, e-commerce ready, clean studio lighting
```

**Vertical Nano Banana platform-native:**

```
A 9:16 vertical hero for a wellness brand: a single ceramic teacup on a
linen runner, soft morning side-light, the words "Slow Down" in
hand-drawn serif large at the top, gentle steam rising, neutral color
palette, uncluttered
```

## Nano Banana 2 FAQ

**What's the difference between Nano Banana 2 and Nano Banana Pro?** Nano Banana 2 is the flash tier (fast, predictable, drafts and typography). Nano Banana Pro is the pro tier (slower, higher fidelity, portraits). This skill is the Nano Banana 2 variant.

**What resolutions does Nano Banana 2 support?** Four: `0.5K` (drafts), `1K` (default), `2K` (final), `4K` (max). 2K and 4K Nano Banana cost more.

**Can Nano Banana 2 generate multiple images per call?** Yes — set `num_images: 4`. Useful for Nano Banana ideation batches.

**Does Nano Banana 2 do image edit?** Not on this endpoint. For Nano Banana edit (preserve subject + apply changes), use the [nano-banana-edit](../nano-banana-edit) skill.

**Why is `enable_web_search` off by default?** Nano Banana web grounding adds latency and cost. Only enable when the prompt explicitly references current events.

**What languages does Nano Banana 2 understand in the prompt?** English is the most reliable for Nano Banana. Multilingual prompts work for layout/style but in-image text is best in Latin-script languages.

**How do I reproduce a Nano Banana 2 output?** Pass `seed` as a fixed int. Same prompt + same seed = same Nano Banana generation.

## Limitations of Nano Banana 2

- **Nano Banana 2 is still images only.** No video on this Nano Banana endpoint.
- **Max 4 outputs per Nano Banana request.**
- **Nano Banana web search adds latency + cost** — only enable on demand.
- **Nano Banana 2K / 4K cost more** — default to 1K unless user asked for higher.
- **For Nano Banana image edit, use the dedicated edit skill** — not this endpoint.

## Exit codes

| code | meaning |
|---|---|
| 0  | Nano Banana generation succeeded |
| 64 | bad CLI args |
| 65 | bad input JSON for Nano Banana / schema mismatch |
| 69 | upstream 5xx |
| 75 | retryable: timeout / 429 |
| 77 | not signed in or token rejected |

Full reference: [docs.runcomfy.com/cli/troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=nano-banana-2-runcomfy).

## How it works

The skill invokes `runcomfy run google/nano-banana-2/text-to-image` with a JSON body matching the Nano Banana 2 schema. The CLI POSTs to `https://model-api.runcomfy.net/v1/models/google/nano-banana-2/text-to-image`, polls the Nano Banana request, fetches the Nano Banana result, and downloads any `.runcomfy.net` / `.runcomfy.com` URL into `--output-dir`. `Ctrl-C` cancels the remote Nano Banana request before exit.

## Security & Privacy

- **Token storage**: `runcomfy login` writes the API token to `~/.config/runcomfy/token.json` with mode 0600.
- **Input boundary**: the Nano Banana prompt is passed as JSON via `--input`. No shell injection.
- **Third-party content**: image URLs are fetched by the RunComfy server. Treat external URLs as untrusted — image-based prompt injection is a known risk.
- **Outbound endpoints**: only `model-api.runcomfy.net` and `*.runcomfy.net` / `*.runcomfy.com`.
- **Generated-file size cap**: 2 GiB.

---
name: Memorable Image Generator
description: "Science-backed image generation agent that scores and optimizes images for memorability using ResMem (Brain Bridge Lab, University of Chicago) before returning results. Unlike generic image generators, this agent iterates until the image clears a memorability threshold — producing visuals that stick in viewers' minds. Use for blog hero images, marketing visuals, social media graphics, product thumbnails, or any context where image recall matters. Triggers on: generate a memorable image, create a blog hero image, make a marketing visual that sticks, image that people will remember, or any image generation request where memorability is a goal."
license: ResMem Non-commercial License
metadata:
  openclaw:
    homepage: https://github.com/PhantomWorksIO/clawhub-skills/tree/main/memorable-image-gen
    emoji: "🧠"
    category: media
    requires:
      env: ["GEMINI_API_KEY"]
      python_packages: ["resmem", "torch", "torchvision", "pillow", "requests"]
---

# Memorable Image Generator

**Science-backed image generation that optimizes for memorability — not just aesthetics.**

Most image generators stop when the image looks good. This one keeps going until the image is *remembered*. Powered by Google Gemini for generation and ResMem (Brain Bridge Lab, University of Chicago) for memorability scoring, it iterates until your image clears a science-validated memorability threshold.

---

## Prerequisites

**API Key:**
- `GEMINI_API_KEY` environment variable, OR
- `--api-key` CLI flag, OR
- `~/.config/gemini/api_key` file

**Python 3.8+** with these packages:
```bash
pip install resmem torch torchvision pillow requests
```

---

## Quick Start

```bash
python scripts/generate_memorable_image.py \
  --prompt "a lone astronaut standing on a red desert planet at dusk" \
  --output hero.png \
  --threshold 0.7 \
  --verbose
```

---

## How It Works

1. **Generate** — Calls the Gemini REST API (`gemini-2.0-flash-exp`) with your prompt
2. **Score** — Runs the image through ResMem to get a memorability score (0–1)
3. **Threshold check** — If score ≥ threshold (default: 0.7), saves and returns the image
4. **Regenerate** — If below threshold and attempts remain, enhances the prompt with composition cues and tries again
5. **Max attempts** — After 3 attempts (default), saves the best result regardless

Each failed attempt appends increasingly strong composition cues to the prompt:
- Attempt 2: `", striking composition"`
- Attempt 3: `", vivid colors, memorable focal point"`

---

## Script Usage

```bash
# Basic usage
python scripts/generate_memorable_image.py --prompt "your image description"

# Full options
python scripts/generate_memorable_image.py \
  --prompt "your image description" \
  --output path/to/output.png \
  --threshold 0.75 \
  --max-attempts 3 \
  --api-key YOUR_KEY \
  --verbose

# With verbose scoring output
python scripts/generate_memorable_image.py \
  --prompt "a surreal clock melting over a desert canyon" \
  --verbose
```

**CLI Arguments:**

| Argument | Default | Description |
|---|---|---|
| `--prompt` | (required) | Image description |
| `--output` | `memorable-image.png` | Output file path |
| `--threshold` | `0.7` | Memorability threshold (0–1) |
| `--max-attempts` | `3` | Max regeneration attempts |
| `--api-key` | (env/file) | Gemini API key |
| `--verbose` | (flag) | Show memorability scores per attempt |

---

## Prompt Tips for High-Memorability Images

Research shows these compositional elements consistently score higher with ResMem:

- **Faces and eyes** — Human faces, especially with direct gaze, are inherently memorable
- **Unusual juxtapositions** — Unexpected scale, context, or combination of objects ("a whale floating through a city skyline")
- **Strong focal point** — One clear subject against a contrasting background
- **High contrast** — Bold color separations between subject and background
- **Emotional resonance** — Images that imply narrative or emotion
- **Unusual lighting** — Dramatic shadows, golden hour, bioluminescence, neon
- **Unexpected scale** — Macro details of normally-seen-large things, or vice versa

Prompts that tend to score low: generic landscapes, symmetrical compositions, neutral palettes, cluttered scenes with no clear focal point.

---

## Memorability Science

> **ResMem — Brain Bridge Lab, University of Chicago**
> © 2021 The University of Chicago. Non-commercial use license.
> https://github.com/Brain-Bridge-Lab/resmem
>
> ResMem is a deep learning model trained to predict image memorability scores — how likely a person is to remember having seen an image after a brief exposure. Scores range from 0 (instantly forgotten) to 1 (highly memorable).
>
> **License:** ResMem Non-commercial License — redistribution permitted for non-commercial purposes with attribution. For commercial licensing: wilma@uchicago.edu

---

Built for Claude Code. Requires a Gemini API key and a local Python environment with `resmem` installed. This skill is distributed for free/non-commercial use only because ResMem uses a non-commercial license.

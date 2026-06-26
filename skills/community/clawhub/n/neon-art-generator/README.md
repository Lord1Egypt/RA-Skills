# Neon Art Generator

Generate stunning neon-lit artwork from text descriptions using AI. Describe any subject — a portrait, a cityscape, an object — and receive vibrant neon-glowing images with electric blues, pinks, and cyberpunk aesthetics. Ideal for profile pictures, wallpapers, social media content, and digital art projects.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

---

## Install

**Via npx skills:**
```bash
npx skills add blammectrappora/neon-art-generator
```

**Via ClawHub:**
```bash
clawhub install neon-art-generator
```

---

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

```bash
node neonartgenerator.js "PROMPT" --token YOUR_TOKEN [--size SIZE] [--ref UUID]
```

### Examples

```bash
# Neon portrait
node neonartgenerator.js "neon glowing portrait, electric blue and pink neon lights, dark background" --token "$NETA_TOKEN"

# Cyberpunk city scene
node neonartgenerator.js "cyberpunk city at night, neon signs, rain reflections, ultra detailed" --token "$NETA_TOKEN"

# Landscape format
node neonartgenerator.js "neon jungle, glowing plants, vibrant neon colors" --token "$NETA_TOKEN" --size landscape

# Using a reference image for style inheritance
node neonartgenerator.js "neon samurai warrior" --token "$NETA_TOKEN" --ref abc123-uuid-here
```

The script prints the generated image URL to stdout when complete.

**Output:** Returns a direct image URL.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--token` | string | _(required)_ | Your Neta API token |
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image dimensions |
| `--ref` | UUID string | _(none)_ | Reference image UUID for style inheritance |

### Size Dimensions

| Size | Width | Height |
|------|-------|--------|
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `square` | 1024 | 1024 |
| `tall` | 704 | 1408 |

---

## Default Prompt

If no prompt is provided, the following default is used:

> neon glowing portrait, vibrant neon lights, electric blue and pink neon colors, dark background, cinematic lighting, neon reflections, cyberpunk neon aesthetic, high contrast, ultra detailed


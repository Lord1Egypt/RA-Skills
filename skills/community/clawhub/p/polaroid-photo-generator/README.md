# Polaroid Photo Generator

Generate stunning retro polaroid-style photos from text descriptions using AI. Describe any scene, portrait, or moment and receive an image rendered with authentic vintage instant-film aesthetics — faded warm colors, soft film grain, slight vignette, overexposed highlights, and that unmistakable '70s–'80s color palette, complete with a white polaroid border frame.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

---

## Install

**Via npx skills:**
```bash
npx skills add blammectrappora/polaroid-photo-generator
```

**Via ClawHub:**
```bash
clawhub install polaroid-photo-generator
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
node polaroidphotogenerator.js "<description>" --token YOUR_TOKEN [--size <size>] [--ref <uuid>]
```

### Examples

```bash
# Square polaroid of a sunset on the beach
node polaroidphotogenerator.js "golden hour sunset over a calm ocean beach" --token "$NETA_TOKEN"

# Portrait-oriented polaroid of a city street
node polaroidphotogenerator.js "busy 1970s New York City street corner, yellow cabs, pedestrians" --token "$NETA_TOKEN" --size portrait

# Landscape polaroid of a mountain cabin
node polaroidphotogenerator.js "rustic log cabin in a snowy mountain forest" --token "$NETA_TOKEN" --size landscape

# Tall polaroid of a lone figure
node polaroidphotogenerator.js "a woman in a sundress standing in a wildflower meadow" --token "$NETA_TOKEN" --size tall

# With a reference image UUID for style inheritance
node polaroidphotogenerator.js "children playing in a backyard" --token "$NETA_TOKEN" --ref abc123-uuid-here
```

### Output

Returns a direct image URL printed to stdout. Redirect or pipe it as needed:

```bash
URL=$(node polaroidphotogenerator.js "sunset over the ocean" --token "$NETA_TOKEN")
echo "Image: $URL"
```

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--token` | string | _(required)_ | Your Neta API token |
| `--size` | `square`, `portrait`, `landscape`, `tall` | `square` | Output image dimensions |
| `--ref` | UUID string | _(none)_ | Reference image UUID for style inheritance |

### Size dimensions

| Size | Width | Height |
|------|-------|--------|
| `square` | 1024 | 1024 |
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `tall` | 704 | 1408 |

---

## How It Works

1. Your text description is combined with a built-in polaroid aesthetic prompt to produce the retro look automatically.
2. A generation task is submitted to the Neta API.
3. The script polls every 2 seconds (up to 3 minutes) until the image is ready.
4. The final image URL is printed to stdout.


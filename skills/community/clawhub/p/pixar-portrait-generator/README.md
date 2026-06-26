# Pixar Portrait Generator

Generate Pixar-style 3D animated character portraits from text descriptions. Produces cinematic CGI-quality images with soft volumetric lighting, expressive oversized eyes, glossy subsurface skin, and warm vibrant colors — ideal for profile pictures, animated-style headshots, family portraits, and stylized character art.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/pixar-portrait-generator
```

Or with ClawHub:

```bash
clawhub install pixar-portrait-generator
```

## Usage

```bash
node pixarportraitgenerator.js "a cheerful young girl with curly red hair and freckles" --token YOUR_TOKEN
```

### More examples

```bash
# Square (default)
node pixarportraitgenerator.js "a wise old wizard with a long white beard" --token YOUR_TOKEN

# Portrait orientation
node pixarportraitgenerator.js "a happy golden retriever puppy" --token YOUR_TOKEN --size portrait

# Landscape with a reference image for style inheritance
node pixarportraitgenerator.js "a family of four at a picnic" --token YOUR_TOKEN --size landscape --ref <picture_uuid>
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--token` | Neta API token (required) | — |
| `--size` | `square`, `portrait`, `landscape`, `tall` | `square` |
| `--ref` | Reference image UUID for style inheritance | — |

### Size dimensions

| Size | Width × Height |
|------|----------------|
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

## Token setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Output

Returns a direct image URL on stdout. Progress messages are written to stderr, so you can safely pipe the URL:

```bash
URL=$(node pixarportraitgenerator.js "a brave astronaut cat" --token "$NETA_TOKEN")
echo "$URL"
```


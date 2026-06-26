# Kawaii Art Generator

Generate adorable kawaii artwork from text descriptions — cute chibi characters, soft pastel illustrations, Japanese kawaii aesthetics, and dreamy scenes, all produced via AI image generation.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/kawaii-art-generator
```

```bash
clawhub install kawaii-art-generator
```

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

```bash
node kawaiiartgenerator.js "PROMPT" --token YOUR_TOKEN [--size SIZE] [--ref UUID]
```

### Examples

```bash
# Default kawaii style
node kawaiiartgenerator.js "kawaii cat girl with pastel pink hair and star accessories" --token "$NETA_TOKEN"

# Chibi character portrait
node kawaiiartgenerator.js "chibi magical girl, sparkling eyes, fluffy dress, pastel rainbow background" --token "$NETA_TOKEN" --size portrait

# Kawaii food illustration
node kawaiiartgenerator.js "cute kawaii strawberry cake character, big shiny eyes, rosy cheeks, soft watercolor style" --token "$NETA_TOKEN" --size square

# Landscape scene
node kawaiiartgenerator.js "dreamy kawaii forest with adorable animal characters, soft pastel colors, sparkles" --token "$NETA_TOKEN" --size landscape

# Tall format for wallpaper
node kawaiiartgenerator.js "kawaii anime girl under sakura tree, soft pink palette, chibi proportions" --token "$NETA_TOKEN" --size tall
```

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--token` | string | — | Neta API token (required) |
| `--size` | `square`, `portrait`, `landscape`, `tall` | `square` | Output image dimensions |
| `--ref` | UUID string | — | Reference image UUID for style inheritance |

### Size Dimensions

| Size | Dimensions |
|------|------------|
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

## Output

Returns a direct image URL printed to stdout. Redirect or capture it as needed:

```bash
URL=$(node kawaiiartgenerator.js "kawaii bunny girl" --token "$NETA_TOKEN")
echo "$URL"
```

## Default Prompt

If no prompt is provided, the script uses a built-in kawaii default:

> kawaii style illustration, soft pastel color palette, large sparkling eyes, chibi proportions, rosy cheeks, fluffy and round forms, adorable accessories, Japanese kawaii aesthetic, clean linework, dreamy background

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

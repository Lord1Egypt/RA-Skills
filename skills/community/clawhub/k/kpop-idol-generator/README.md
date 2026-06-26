# K-Pop Idol Generator

Generate polished k-pop idol style portraits from plain text descriptions. Describe the look you want — hair color, outfit, mood, setting — and the skill renders a glossy, magazine-quality idol photo with korean beauty aesthetics, dewy skin, designer styling, and cinematic studio lighting. Perfect for kpop fan edits, bias photocard art, stan twitter profile pics, korean fashion portraits, and hallyu-inspired glamour photography.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

Install via ClawHub / OpenClaw:

```bash
npx skills add omactiengartelle/kpop-idol-generator
```

Or with the ClawHub CLI:

```bash
clawhub install kpop-idol-generator
```

## Usage

```bash
node kpopidolgenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

Generate a classic idol portrait:

```bash
node kpopidolgenerator.js "young woman with pastel pink hair smiling softly" --token "$NETA_TOKEN"
```

Generate a landscape concept photo:

```bash
node kpopidolgenerator.js "boy group member in oversized varsity jacket, neon city backdrop" \
  --token "$NETA_TOKEN" --size landscape
```

Generate a square photocard-style shot:

```bash
node kpopidolgenerator.js "girl group visual in sparkling silver stage outfit" \
  --token "$NETA_TOKEN" --size square
```

Use a reference image for style inheritance:

```bash
node kpopidolgenerator.js "rookie idol debut teaser, dreamy pastel tones" \
  --token "$NETA_TOKEN" --ref <picture_uuid>
```

## Options

| Flag | Description | Default |
| --- | --- | --- |
| `--token <token>` | Neta API token (required) | — |
| `--size <size>` | Aspect ratio: `portrait`, `landscape`, `square`, `tall` | `portrait` |
| `--ref <uuid>` | Reference image UUID for style inheritance | — |
| `-h`, `--help` | Show usage help | — |

### Size reference

| Size | Dimensions |
| --- | --- |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `square` | 1024 × 1024 |
| `tall` | 704 × 1408 |

## Token setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Output

Returns a direct image URL. On success, the URL is printed to stdout so you can pipe it, open it, or download it:

```bash
IMG=$(node kpopidolgenerator.js "idol visual center with wavy blonde hair" --token "$NETA_TOKEN")
echo "$IMG"
```

Progress messages are written to stderr so they don't pollute the captured output.

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

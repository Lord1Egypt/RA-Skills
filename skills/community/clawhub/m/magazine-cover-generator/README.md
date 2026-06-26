# Magazine Cover Generator

Generate stunning AI magazine cover art from text descriptions in Vogue, TIME, GQ, and editorial styles. Perfect for fashion covers, lifestyle magazine mockups, parody covers, personal branding, social media viral posts, pet magazine covers, and mixed-media editorial collage designs with professional masthead typography and cover headlines — all produced from a simple text prompt, with no photos or uploads required.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/magazine-cover-generator
```

Or via ClawHub:

```bash
clawhub install magazine-cover-generator
```

## Usage

```bash
node magazinecovergenerator.js "your prompt here" --token YOUR_TOKEN
```

### Examples

Generate a fashion cover:

```bash
node magazinecovergenerator.js "confident woman in red blazer, city skyline background" --token YOUR_TOKEN
```

Generate a TIME-style person of the year cover:

```bash
node magazinecovergenerator.js "tech visionary portrait, black and white, bold red border" --token YOUR_TOKEN
```

Generate a pet magazine cover:

```bash
node magazinecovergenerator.js "golden retriever wearing sunglasses, summer issue" --token YOUR_TOKEN
```

Landscape cover layout:

```bash
node magazinecovergenerator.js "surreal collage, mixed media" --size landscape --token YOUR_TOKEN
```

Use a reference image for style inheritance:

```bash
node magazinecovergenerator.js "editorial portrait" --ref <picture_uuid> --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
|---|---|---|
| `--size` | `portrait`, `landscape`, `square`, or `tall` | `portrait` |
| `--token` | Neta API token (required) | — |
| `--ref` | Reference image UUID for style inheritance | — |
| `-h`, `--help` | Show help | — |

### Sizes

| Size | Dimensions |
|---|---|
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

Returns a direct image URL.


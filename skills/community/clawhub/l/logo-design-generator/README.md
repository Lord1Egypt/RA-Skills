# Logo Design Generator

AI logo generator and logo design maker — generate professional brand logos, company emblems, startup icons, app logos, and business identity marks from text descriptions. Design custom logo concepts with clean modern aesthetics for any brand, business, or project.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/logo-design-generator
```

Or via ClawHub:

```bash
clawhub install logo-design-generator
```

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

Generate a logo with the default square size:

```bash
node logodesigngenerator.js "Professional logo design, clean minimal vector style, centered composition, simple iconic symbol, white background, brand identity mark" --token YOUR_TOKEN
```

Generate a landscape logo:

```bash
node logodesigngenerator.js "Modern tech startup logo, geometric shapes, blue gradient" --size landscape --token YOUR_TOKEN
```

Use a reference image for style inheritance:

```bash
node logodesigngenerator.js "Minimalist coffee shop logo" --ref PICTURE_UUID --token YOUR_TOKEN
```

Returns a direct image URL.

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--token` | Neta API token (required) | — |
| `--size` | Image dimensions: `square`, `portrait`, `landscape`, `tall` | `square` |
| `--ref` | Reference image UUID for style inheritance | — |

### Size Reference

| Size | Dimensions |
|------|-----------|
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

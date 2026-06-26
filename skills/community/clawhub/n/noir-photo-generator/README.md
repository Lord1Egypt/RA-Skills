# Film Noir Photo Generator

Generate dramatic film noir style images from text descriptions. Create 1940s detective aesthetic portraits, black and white cinematic scenes, vintage crime fiction artwork, and moody atmospheric shots with venetian blind shadows, rain-soaked streets, and classic Hollywood noir vibes — all from a single text prompt.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

Via ClawHub/OpenClaw:

```bash
npx skills add blammectrappora/noir-photo-generator
```

Or:

```bash
clawhub install noir-photo-generator
```

## Usage

```bash
node noirphotogenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

Generate a default film noir portrait:

```bash
node noirphotogenerator.js "detective in a trench coat under a streetlamp" --token YOUR_TOKEN
```

Landscape scene:

```bash
node noirphotogenerator.js "rainy alley with neon signs, 1940s city street" --size landscape --token YOUR_TOKEN
```

Style inheritance from a reference image:

```bash
node noirphotogenerator.js "smoky jazz club interior" --ref <picture_uuid> --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
| --- | --- | --- |
| `--size` | Output size: `portrait`, `landscape`, `square`, `tall` | `portrait` |
| `--token` | Your Neta API token | (required) |
| `--ref` | Reference image UUID for style inheritance | (none) |

### Size dimensions

| Size | Dimensions |
| --- | --- |
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


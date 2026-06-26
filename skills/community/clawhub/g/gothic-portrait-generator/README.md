# Gothic Portrait Generator

Generate stunning gothic portraits from text descriptions with dark dramatic lighting, Victorian elegance, and moody atmosphere. Perfect for gothic art, dark fantasy portraits, horror aesthetic avatars, Victorian-style character art, dark academia profile pictures, and goth community content creation.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/gothic-portrait-generator
```

or

```bash
clawhub install gothic-portrait-generator
```

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

Generate a gothic portrait with the default prompt:

```bash
node gothicportraitgenerator.js --token YOUR_TOKEN
```

Generate a gothic portrait with a custom description:

```bash
node gothicportraitgenerator.js "pale woman in black lace gown, standing in a dimly lit cathedral, stained glass windows, dramatic shadows" --token YOUR_TOKEN
```

Generate a landscape gothic scene:

```bash
node gothicportraitgenerator.js "abandoned gothic castle at midnight, fog rolling through broken windows, moonlight casting long shadows" --size landscape --token YOUR_TOKEN
```

Use a reference image for style inheritance:

```bash
node gothicportraitgenerator.js "gothic nobleman with raven on shoulder" --ref IMAGE_UUID --token YOUR_TOKEN
```

Returns a direct image URL.

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--token` | Neta API token (required) | — |
| `--size` | Image dimensions: `portrait`, `landscape`, `square`, `tall` | `portrait` |
| `--ref` | Reference image UUID for style inheritance | — |

### Size Dimensions

| Size | Width | Height |
|------|-------|--------|
| `square` | 1024 | 1024 |
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `tall` | 704 | 1408 |

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

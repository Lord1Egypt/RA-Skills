# Pet Memorial Portrait Generator

Create heartfelt pet memorial portraits and remembrance keepsakes from text descriptions. Generate AI pet memorial art, rainbow bridge portraits, angel pet paintings, and tribute imagery perfect for memorial gifts, sympathy cards, keepsake prints, and honoring the memory of a cherished furry family member — all from a written prompt describing the pet you wish to remember.

> Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

Via the skills CLI:

```bash
npx skills add blammectrappora/pet-memorial-portrait-generator
```

Or via ClawHub:

```bash
clawhub install pet-memorial-portrait-generator
```

## Usage

```bash
node petmemorialportraitgenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

Generate a default memorial portrait:

```bash
node petmemorialportraitgenerator.js "" --token YOUR_TOKEN
```

Custom remembrance scene:

```bash
node petmemorialportraitgenerator.js \
  "golden retriever with angel wings resting in a sunlit meadow, soft cinematic light, peaceful tribute" \
  --token YOUR_TOKEN
```

Landscape orientation for a keepsake card:

```bash
node petmemorialportraitgenerator.js \
  "tabby cat curled on a cloud, gentle starlight, rainbow bridge background" \
  --size landscape \
  --token YOUR_TOKEN
```

Use a reference image for style inheritance:

```bash
node petmemorialportraitgenerator.js \
  "a beloved beagle in a serene garden of remembrance" \
  --ref <picture_uuid> \
  --token YOUR_TOKEN
```

## Options

| Flag      | Description                                            | Default    |
| --------- | ------------------------------------------------------ | ---------- |
| `--token` | Neta API token (required)                              | —          |
| `--size`  | `portrait`, `landscape`, `square`, `tall`              | `portrait` |
| `--ref`   | Reference image UUID for style inheritance             | —          |

### Sizes

| Size      | Dimensions  |
| --------- | ----------- |
| portrait  | 832 × 1216  |
| landscape | 1216 × 832  |
| square    | 1024 × 1024 |
| tall      | 704 × 1408  |

## Token setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Output

Returns a direct image URL.


# Pin-Up Art Generator

Generate classic 1950s pin-up art, retro glamour illustrations, vintage poster portraits, mid-century advertising art, and Gil Elvgren style pinup girls from text descriptions. Perfect for Etsy sellers, vintage poster designers, retro merch creators, rockabilly fans, tiki bar decor, and nostalgic 70s/80s aesthetic lovers who want classic pinup portrait illustrations with timeless retro charm — all generated from a written prompt, no source image needed.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/pinup-art-generator
```

Or via ClawHub:

```bash
clawhub install pinup-art-generator
```

## Usage

```bash
node pinupartgenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

Generate with the default pin-up prompt:

```bash
node pinupartgenerator.js "" --token YOUR_TOKEN
```

Custom prompt:

```bash
node pinupartgenerator.js "1950s pin-up girl in red polka dot dress, winking at camera, pastel background" --token YOUR_TOKEN
```

Landscape orientation:

```bash
node pinupartgenerator.js "retro tiki bar pin-up scene, tropical pastel palette" --size landscape --token YOUR_TOKEN
```

Style-inherit from a reference image:

```bash
node pinupartgenerator.js "vintage rockabilly pin-up portrait" --ref <picture_uuid> --token YOUR_TOKEN
```

## Options

| Option | Description | Default |
| --- | --- | --- |
| `<prompt>` | First positional arg — the text description. If empty, a classic pin-up prompt is used. | built-in pin-up prompt |
| `--token` | Your Neta API token (required). | — |
| `--size` | Output aspect ratio: `portrait`, `landscape`, `square`, `tall`. | `portrait` |
| `--ref` | Reference image UUID for style inheritance. | — |

### Size reference

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

Returns a direct image URL printed to stdout on success. Progress messages are printed to stderr so you can pipe the URL cleanly:

```bash
IMG=$(node pinupartgenerator.js "pin-up girl reading a magazine" --token "$NETA_TOKEN")
echo "Generated: $IMG"
```

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

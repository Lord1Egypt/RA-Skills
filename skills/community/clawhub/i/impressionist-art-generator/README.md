# Impressionist Art Generator

Generate stunning impressionist-style art from text descriptions in the tradition of Claude Monet, Pierre-Auguste Renoir, Vincent van Gogh, Edgar Degas, and Camille Pissarro. Turn any idea into a gallery-ready painting with soft visible brushstrokes, dappled natural light, pastel palettes with luminous highlights, and the atmospheric feel of late 19th-century French plein air painting — perfect for wall art, Etsy prints, art education, painting references, garden scenes, and portrait studies.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/impressionist-art-generator
```

Or via ClawHub:

```bash
clawhub install impressionist-art-generator
```

## Usage

```bash
node impressionistartgenerator.js "a quiet water-lily pond at sunrise" --token YOUR_TOKEN
```

### Examples

Landscape (default):

```bash
node impressionistartgenerator.js "a field of poppies under a breezy summer sky" --token YOUR_TOKEN
```

Portrait orientation:

```bash
node impressionistartgenerator.js "a young woman reading in a sunlit garden" --size portrait --token YOUR_TOKEN
```

Square for social posts:

```bash
node impressionistartgenerator.js "a Paris café terrace in the afternoon" --size square --token YOUR_TOKEN
```

Inherit style from a reference picture:

```bash
node impressionistartgenerator.js "cliffs overlooking the sea at Étretat" --ref <picture_uuid> --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
| --- | --- | --- |
| `--token` | Your Neta API token (required) | — |
| `--size` | `portrait` (832×1216), `landscape` (1216×832), `square` (1024×1024), `tall` (704×1408) | `landscape` |
| `--ref` | Reference image UUID for style inheritance | — |

## Output

Returns a direct image URL.

## Token setup

You need a Neta API token to use this skill. Grab a free trial token at <https://www.neta.art/open/>.

Pass your token on every run using the `--token` flag:

```bash
node impressionistartgenerator.js "your prompt here" --token YOUR_TOKEN
```

You can also expand a shell variable yourself if you prefer:

```bash
node impressionistartgenerator.js "your prompt here" --token "$NETA_TOKEN"
```

The `--token` flag is the only way this script accepts a token.

---

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

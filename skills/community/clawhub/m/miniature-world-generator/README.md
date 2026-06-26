# Miniature World Generator

Generate hyper-detailed miniature diorama scenes and tiny world art from text descriptions. Describe any scene — a bustling city block scaled down to a tabletop, a magical forest in a teacup, a snow-globe winter village — and receive a stunning tilt-shift image with shallow depth of field and whimsical atmosphere.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

---

## Install

```bash
# via npx skills
npx skills add blammectrappora/miniature-world-generator

# via clawhub
clawhub install miniature-world-generator
```

---

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

```bash
node miniatureworldgenerator.js "<description>" --token YOUR_TOKEN [--size <size>] [--ref <uuid>]
```

If no prompt is provided, a default diorama prompt is used automatically.

### Examples

```bash
# Tiny Japanese street market at night
node miniatureworldgenerator.js "tiny Japanese street market at night, paper lanterns, miniature stalls, tilt-shift, bokeh" --token "$NETA_TOKEN"

# Autumn forest diorama
node miniatureworldgenerator.js "miniature autumn forest with tiny log cabin, fallen leaves, misty morning light, bird's eye view" --token "$NETA_TOKEN" --size portrait

# Landscape format beach scene
node miniatureworldgenerator.js "hyper-detailed miniature tropical beach, tiny palm trees, crystal clear water, aerial view" --token "$NETA_TOKEN" --size landscape

# Using a reference image for style inheritance
node miniatureworldgenerator.js "snowy alpine village diorama" --token "$NETA_TOKEN" --ref xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### Output

Returns a direct image URL printed to stdout.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--token` | string | *(required)* | Your Neta API token |
| `--size` | `square`, `portrait`, `landscape`, `tall` | `square` | Output image dimensions |
| `--ref` | UUID string | *(none)* | Reference image UUID for style inheritance |

### Size dimensions

| Size | Width | Height |
|------|-------|--------|
| `square` | 1024 | 1024 |
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `tall` | 704 | 1408 |

---

## Tips for great prompts

- Mention **tilt-shift**, **shallow depth of field**, or **bokeh** for the classic miniature look
- Include **bird's eye view** or **aerial perspective** for a diorama feel
- Describe **scale cues**: tiny, miniature, tabletop, diorama, figurines
- Add a **mood**: whimsical, magical, cozy, dramatic, cinematic

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

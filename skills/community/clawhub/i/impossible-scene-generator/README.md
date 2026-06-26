# Impossible Scene Generator

Generate photorealistic impossible scenes and anti-physics landscapes from text descriptions. Describe what you want — crystal mountains beneath cosmic auroras, floating islands defying gravity, organic-growing architecture, dreamlike sci-fi vistas — and get back a high-resolution cinematic image. Ideal for desktop wallpapers, concept art, book covers, album art, sci-fi posters, fantasy worldbuilding, and print-on-demand artwork.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/impossible-scene-generator
```

Or via ClawHub:

```bash
clawhub install impossible-scene-generator
```

## Usage

```bash
node impossiblescenegenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

```bash
node impossiblescenegenerator.js "crystal mountains beneath twin moons and cosmic auroras, ultra-wide cinematic vista" --token YOUR_TOKEN

node impossiblescenegenerator.js "floating islands with cascading waterfalls into clouds, hyperdetailed photography" --size landscape --token YOUR_TOKEN

node impossiblescenegenerator.js "organic-growing alien city of bone and coral, dramatic volumetric lighting" --size portrait --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
| --- | --- | --- |
| `--size` | Aspect: `portrait` (832×1216), `landscape` (1216×832), `square` (1024×1024), `tall` (704×1408) | `landscape` |
| `--token` | Your Neta API token (required) | — |
| `--ref` | Reference image UUID for style inheritance | — |

## Output

Returns a direct image URL.

## Token setup

This skill requires a Neta API token. Pass it via the `--token` flag on every invocation:

```bash
node impossiblescenegenerator.js "a surreal anti-physics landscape" --token YOUR_TOKEN
```

You can keep the token in a shell variable and expand it inline:

```bash
node impossiblescenegenerator.js "a surreal anti-physics landscape" --token "$NETA_TOKEN"
```

Get a free trial token at <https://www.neta.art/open/>.


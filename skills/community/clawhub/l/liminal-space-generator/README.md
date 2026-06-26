# Liminal Space Generator

Generate eerie liminal space images, dreamcore backgrounds, and backrooms-style scenes from text descriptions — empty hallways, abandoned pools, fluorescent-lit rooms, uncanny dreamscapes, analog horror aesthetics, and nostalgic unsettling environments. Perfect for horror writers, aesthetic Tumblr/TikTok accounts, weirdcore creators, and atmospheric game or video backdrops.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

Via the skills CLI:

```bash
npx skills add omactiengartelle/liminal-space-generator
```

Via ClawHub:

```bash
clawhub install liminal-space-generator
```

## Usage

```bash
node liminalspacegenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

Generate a default liminal hallway:

```bash
node liminalspacegenerator.js "liminal space, eerie empty hallway with fluorescent lighting, worn carpet, dreamcore aesthetic" --token YOUR_TOKEN
```

Generate a portrait-oriented abandoned pool scene:

```bash
node liminalspacegenerator.js "abandoned indoor pool, flickering fluorescent lights, tiled walls, uncanny backrooms atmosphere" --size portrait --token YOUR_TOKEN
```

Generate with a reference image for style inheritance:

```bash
node liminalspacegenerator.js "empty arcade at night, dreamcore, VHS grain" --ref <picture_uuid> --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
| --- | --- | --- |
| `--size` | Output size: `portrait` (832×1216), `landscape` (1216×832), `square` (1024×1024), `tall` (704×1408) | `landscape` |
| `--token` | Your Neta API token | required |
| `--ref` | Reference image UUID for style inheritance | none |

## Output

Returns a direct image URL.

## Token Setup

This skill requires a Neta API token. Get a free trial token at <https://www.neta.art/open/>.

Pass the token via the `--token` flag on every invocation:

```bash
node liminalspacegenerator.js "your prompt" --token YOUR_TOKEN
```

You can also use shell expansion to inject a token from your shell environment:

```bash
node liminalspacegenerator.js "your prompt" --token "$NETA_TOKEN"
```


# Manga Panel Generator

Generate professional black-and-white manga panels and full comic pages from text descriptions — complete with dynamic poses, screentone shading, expressive action lines, and authentic Japanese manga art style. Ideal for manga artists, doujinshi creators, webtoon storyboarders, comic writers, and anime fans who want to illustrate scenes, action sequences, or character moments in classic shonen, shojo, or seinen aesthetics directly from a written prompt.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

With ClawHub:

```bash
npx skills add blammectrappora/manga-panel-generator
```

Or via the ClawHub CLI:

```bash
clawhub install manga-panel-generator
```

## Usage

```bash
node mangapanelgenerator.js "your manga scene description" --token YOUR_TOKEN
```

### Examples

Generate a default manga panel:

```bash
node mangapanelgenerator.js "a young swordsman leaping through the air, sword mid-swing, wind lines swirling" --token YOUR_TOKEN
```

Generate a landscape panel with a reference image:

```bash
node mangapanelgenerator.js "two rivals facing off on a rooftop at sunset" \
  --size landscape \
  --ref 123e4567-e89b-12d3-a456-426614174000 \
  --token YOUR_TOKEN
```

Generate a tall vertical webtoon-style panel:

```bash
node mangapanelgenerator.js "school girl looking out a classroom window, cherry blossoms falling" \
  --size tall \
  --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| (positional) | Prompt describing the manga panel to generate | Built-in manga panel prompt |
| `--size` | Output size: `portrait` (832×1216), `landscape` (1216×832), `square` (1024×1024), `tall` (704×1408) | `portrait` |
| `--token` | Neta API token (required) | — |
| `--ref` | Reference image UUID for style inheritance | — |

## Output

Returns a direct image URL.

## Token setup

This skill requires a Neta API token. Pass it on the command line with the `--token` flag:

```bash
node mangapanelgenerator.js "your prompt" --token YOUR_TOKEN
```

You can also expand a shell variable into the flag:

```bash
node mangapanelgenerator.js "your prompt" --token "$NETA_TOKEN"
```

Get a free trial token at <https://www.neta.art/open/>.


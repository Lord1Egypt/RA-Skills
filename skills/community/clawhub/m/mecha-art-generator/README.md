# Mecha Art Generator

AI-powered mecha art generator for anime-style giant robots, gundam-inspired suits, sci-fi battle armor, and mech pilot scenes. Generate custom mecha designs, robot illustrations, mech anime posters, sci-fi battle artwork, and futuristic mechanical character art directly from text descriptions — perfect for cosplay reference, fanart, model kit inspiration, and concept design.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

Using ClawHub:

```bash
clawhub install mecha-art-generator
```

Using the skills CLI:

```bash
npx skills add blammectrappora/mecha-art-generator
```

## Usage

```bash
node mechaartgenerator.js "your prompt here" --token YOUR_TOKEN
```

### Examples

Generate a default mecha scene:

```bash
node mechaartgenerator.js "highly detailed mecha robot, intricate sci-fi armor plating, dynamic action pose, glowing energy core, futuristic battlefield background, panel lines and weathering, anime style, cinematic lighting, hyper-detailed mechanical design" --token YOUR_TOKEN
```

A gundam-style hero shot in portrait orientation:

```bash
node mechaartgenerator.js "gundam-inspired white and blue mecha standing tall, beam saber drawn, glowing green eyes, panel line shading, anime cel style" --size portrait --token YOUR_TOKEN
```

A battle scene in landscape:

```bash
node mechaartgenerator.js "two mechas clashing mid-air, sparks and energy trails, ruined city below, dramatic anime composition" --size landscape --token YOUR_TOKEN
```

Inherit style from an existing reference image:

```bash
node mechaartgenerator.js "crimson samurai mech wielding twin katanas under cherry blossoms" --ref REFERENCE_PICTURE_UUID --token YOUR_TOKEN
```

### Output

Returns a direct image URL.

## Options

| Flag      | Description                                                         | Default     |
| --------- | ------------------------------------------------------------------- | ----------- |
| `--size`  | Aspect: `portrait`, `landscape`, `square`, `tall`                   | `landscape` |
| `--token` | Neta API token (required)                                           | —           |
| `--ref`   | Reference image UUID — inherits style from a previous picture       | —           |
| `--help`  | Show CLI help                                                       | —           |

### Sizes

| Size        | Dimensions  |
| ----------- | ----------- |
| `square`    | 1024 × 1024 |
| `portrait`  | 832 × 1216  |
| `landscape` | 1216 × 832  |
| `tall`      | 704 × 1408  |

## Token setup

A Neta API token is required. Pass it on every invocation via the `--token` flag:

```bash
node mechaartgenerator.js "a fierce red mecha in combat" --token YOUR_TOKEN
```

You can keep your token in a shell variable for convenience:

```bash
node mechaartgenerator.js "a fierce red mecha in combat" --token "$NETA_TOKEN"
```

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

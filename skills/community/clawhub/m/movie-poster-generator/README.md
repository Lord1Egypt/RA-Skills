# Movie Poster Generator

Generate stunning AI movie posters, film posters, and cinema artwork from text descriptions. Create professional movie poster designs, event posters, fan-made film posters, and theatrical promotional art with dramatic cinematic lighting and bold compositions.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/movie-poster-generator
```

or

```bash
clawhub install movie-poster-generator
```

## Usage

```bash
node moviepostergenerator.js "cinematic movie poster, dramatic lighting, bold composition" --token YOUR_TOKEN
```

Generate a tall poster (default):

```bash
node moviepostergenerator.js "epic sci-fi movie poster with a lone astronaut facing a distant galaxy, dramatic lighting" --token YOUR_TOKEN
```

Generate a landscape poster:

```bash
node moviepostergenerator.js "noir detective thriller poster, rain-soaked city streets, moody shadows" --token YOUR_TOKEN --size landscape
```

Use a reference image for style inheritance:

```bash
node moviepostergenerator.js "horror movie poster, abandoned mansion, fog" --token YOUR_TOKEN --ref PICTURE_UUID
```

Returns a direct image URL.

## Options

| Option    | Description                          | Default |
|-----------|--------------------------------------|---------|
| `--token` | Neta API token (required)            | —       |
| `--size`  | Image size preset                    | `tall`  |
| `--ref`   | Reference image UUID for style       | —       |

### Available sizes

| Size        | Dimensions   |
|-------------|-------------|
| `square`    | 1024 x 1024 |
| `portrait`  | 832 x 1216  |
| `landscape` | 1216 x 832  |
| `tall`      | 704 x 1408  |

## Token Setup

A Neta API token is required to use this skill. Get a free trial token at [neta.art/open](https://www.neta.art/open/).

Pass your token using the `--token` flag:

```bash
node moviepostergenerator.js "your prompt" --token YOUR_TOKEN
```

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

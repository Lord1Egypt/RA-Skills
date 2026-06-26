# Plush Toy Generator

Generate adorable handmade plush toy and stuffed animal images from text descriptions. Describe any subject — yourself, a pet, a character, or any concept — and get back a kawaii plushie product shot complete with fluffy fabric texture, visible stitching, and button eyes. Great for plushie commission references, kawaii merch mockups, gift ideas, stuffed animal designs, soft toy concepts, and turning OCs into cuddly plush dolls.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/plush-toy-generator
```

Or via ClawHub:

```bash
clawhub install plush-toy-generator
```

## Usage

```bash
node plushtoygenerator.js "a fluffy orange tabby cat" --token YOUR_TOKEN
```

### Examples

Generate a plush toy of a character:

```bash
node plushtoygenerator.js "a brave knight with tiny felt sword" --token YOUR_TOKEN
```

Generate a portrait-oriented plushie:

```bash
node plushtoygenerator.js "a sleepy axolotl wearing a beanie" --size portrait --token YOUR_TOKEN
```

Inherit style from a reference image:

```bash
node plushtoygenerator.js "a chubby red panda" --ref <picture_uuid> --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--token` | Neta API token (required) | — |
| `--size` | One of `square`, `portrait`, `landscape`, `tall` | `square` |
| `--ref` | Reference image UUID for style inheritance | — |

### Sizes

| Name | Dimensions |
|------|-----------|
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

Returns a direct image URL.


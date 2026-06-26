# Pet To Human Generator

Generate realistic human-portrait images from text descriptions of your pet. Describe your dog, cat, or any furry friend — their fur color, eye color, personality, vibe — and the skill produces a photorealistic human alter-ego portrait that preserves those traits. Perfect for the viral pet-to-human trend, creative portraits, gifts, and social media content.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/pet-to-human-generator
```

Or via ClawHub:

```bash
clawhub install pet-to-human-generator
```

## Usage

```bash
node pettohumangenerator.js "your text description" --token YOUR_TOKEN
```

### Examples

Generate a human version of a golden retriever:

```bash
node pettohumangenerator.js "golden retriever reimagined as a warm cheerful man with sandy blonde hair, hazel eyes, friendly smile, cozy knit sweater, studio lighting, photorealistic portrait" --token YOUR_TOKEN
```

Generate a human version of a black cat:

```bash
node pettohumangenerator.js "sleek black cat reimagined as a mysterious elegant woman with jet-black hair, green eyes, sharp cheekbones, minimalist black outfit, dramatic studio lighting" --token YOUR_TOKEN --size portrait
```

Use a reference picture UUID for style inheritance:

```bash
node pettohumangenerator.js "humanized tabby cat as a playful red-haired person" --token YOUR_TOKEN --ref 1234abcd-...-uuid
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--token` | Neta API token (required) | — |
| `--size` | `portrait`, `landscape`, `square`, or `tall` | `portrait` |
| `--ref` | Reference image UUID for style inheritance | — |

Size dimensions:

| Size | Width × Height |
|------|----------------|
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

Returns a direct image URL. The script prints the URL to stdout on success — pipe it or copy it straight into your browser, download tool, or downstream workflow.

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

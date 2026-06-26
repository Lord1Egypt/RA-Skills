# OG Image Generator

> Powered by the **Neta AI image generation API** (`api.talesofai.com`) — the same service as [neta.art](https://www.neta.art/open/).

Generate stunning **open graph social media preview images** from a text description using AI. Get back a direct image URL instantly — no UI required.

Powered by the **Neta AI image generation API** (`api.talesofai.com`).

---

## Install

**Via npx skills:**
```bash
npx skills add SherriHidalgolt/og-image-skill
```

**Via ClawHub:**
```bash
clawhub install og-image-skill
```

---

## Usage

```bash
# Basic — uses the default prompt
node ogimage.js

# Custom prompt
node ogimage.js "dark tech blog banner, neon accents, minimal layout"

# Specify size
node ogimage.js "product launch card" --size square

# Use a reference image (by picture UUID)
node ogimage.js "similar style banner" --ref <picture_uuid>

# Pass token explicitly
node ogimage.js "my prompt" --token sk-xxxx
```

The script prints the image URL to stdout on success:
```
https://cdn.talesofai.cn/artifacts/....png
```

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `square`, `portrait`, `landscape`, `tall` | `landscape` | Output image dimensions |
| `--token` | string | — | API token (required) |
| `--ref` | picture UUID | — | Reference image UUID for style inheritance |

### Size dimensions

| Name | Width | Height |
|------|-------|--------|
| `square` | 1024 | 1024 |
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `tall` | 704 | 1408 |

---

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Examples

```bash
# OG image for a blog post
node ogimage.js "technology article cover, dark gradient, bold white title text"

# Square social card
node ogimage.js "product announcement, vibrant colors, centered logo" --size square

# Tall Pinterest-style card
node ogimage.js "recipe card, warm tones, food photography style" --size tall
```

---

## Requirements

- Node.js 18+ (uses native `fetch` and top-level `await`)

## Example Output

![Generated example](https://oss.talesofai.cn/picture/ff229882-1b18-48ec-9f2d-c0d98f48f5c6.webp)

---

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

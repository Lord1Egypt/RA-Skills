# AI Mockup Generator

Generate professional AI-powered product mockup images from a text description. Powered by the Neta talesofai API, this skill returns a direct image URL in seconds.

---

## Install

**Via npx skills:**
```bash
npx skills add wkl-nieta/mockup-gen-skill
```

**Via ClawHub:**
```bash
clawhub install mockup-gen-skill
```

---

## Usage

```bash
# Basic usage (uses default prompt)
node mockupgen.js

# Custom prompt
node mockupgen.js "white ceramic mug on marble surface, soft lighting"

# Specify size
node mockupgen.js "sneaker floating on gradient background" --size portrait

# Use a reference image UUID
node mockupgen.js "same product, outdoor setting" --ref abc123-uuid

# Pass token directly
node mockupgen.js "luxury watch flat lay" --token YOUR_NETA_TOKEN
```

The script prints the generated image URL to stdout and exits.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `square`, `portrait`, `landscape`, `tall` | `landscape` | Output image dimensions |
| `--token` | string | — | Neta API token (overrides env/file) |
| `--ref` | UUID string | — | Reference picture UUID for style inheritance |

### Size dimensions

| Name | Width × Height |
|------|---------------|
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

---

## Token Setup

The script resolves your `NETA_TOKEN` in this order:

1. `--token` CLI flag
2. `NETA_TOKEN` environment variable

```
NETA_TOKEN=your_token_here
```

---

## Default prompt

If no prompt argument is provided, the script uses:
> `product mockup on clean background, professional photography style`

---

## Example output

```
https://cdn.talesofai.cn/artifacts/abc123.jpg
```

The URL is printed directly to stdout, making it easy to pipe into other tools or scripts.

## Example Output

![Generated example](https://oss.talesofai.cn/picture/7329bbcb-c3cf-443a-b578-730ed354996a.webp)

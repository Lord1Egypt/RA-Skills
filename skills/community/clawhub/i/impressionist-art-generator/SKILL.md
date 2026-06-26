---
name: impressionist-art-generator
description: Generate stunning impressionist-style art in the tradition of Monet, Renoir, Van Gogh, Degas, and Pissarro. Perfect for wall art, Etsy prints, art education, painting references, gallery-style landscapes, garden scenes, plein air portraits, and 19th-century French impressionism aesthetics with soft brushstrokes, pastel palettes, and dappled light via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Impressionist Art Generator

Generate stunning impressionist-style art in the tradition of Monet, Renoir, Van Gogh, Degas, and Pissarro. Perfect for wall art, Etsy prints, art education, painting references, gallery-style landscapes, garden scenes, plein air portraits, and 19th-century French impressionism aesthetics with soft brushstrokes, pastel palettes, and dappled light.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create impressionist art generator images.

## Quick start
```bash
node impressionistartgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `landscape`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/impressionist-art-generator
```

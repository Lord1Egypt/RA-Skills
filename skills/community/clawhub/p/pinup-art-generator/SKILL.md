---
name: pinup-art-generator
description: Generate classic 1950s pin-up art, retro glamour illustrations, vintage poster portraits, mid-century advertising art, and Gil Elvgren style pinup girls. Perfect for Etsy sellers, vintage poster designers, retro merch creators, rockabilly fans, tiki bar decor, and nostalgic 70s/80s aesthetic lovers who want classic pinup portrait illustrations with timeless retro charm via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Pin-Up Art Generator

Generate classic 1950s pin-up art, retro glamour illustrations, vintage poster portraits, mid-century advertising art, and Gil Elvgren style pinup girls. Perfect for Etsy sellers, vintage poster designers, retro merch creators, rockabilly fans, tiki bar decor, and nostalgic 70s/80s aesthetic lovers who want classic pinup portrait illustrations with timeless retro charm.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create pin up art generator images.

## Quick start
```bash
node pinupartgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/pinup-art-generator
```

---
name: polaroid-photo-generator
description: AI polaroid photo generator — create retro instant-film photos with authentic vintage color, film grain, and '70s–'80s aesthetic. Perfect for nostalgic portraits, travel snapshots, lifestyle content, retro photo art, and old-school photography effects via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Polaroid Photo Generator

AI polaroid photo generator — create retro instant-film photos with authentic vintage color, film grain, and '70s–'80s aesthetic. Perfect for nostalgic portraits, travel snapshots, lifestyle content, retro photo art, and old-school photography effects.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create polaroid photo generator images.

## Quick start
```bash
node polaroidphotogenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/polaroid-photo-generator
```

---
name: mecha-art-generator
description: AI mecha art generator for anime-style giant robots, gundam-inspired suits, sci-fi battle armor, and mech pilot scenes. Create custom mecha designs, robot illustrations, mech anime posters, sci-fi battle artwork, and futuristic mechanical character art for cosplay reference, fanart, model kit inspiration, and concept design via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Mecha Art Generator

AI mecha art generator for anime-style giant robots, gundam-inspired suits, sci-fi battle armor, and mech pilot scenes. Create custom mecha designs, robot illustrations, mech anime posters, sci-fi battle artwork, and futuristic mechanical character art for cosplay reference, fanart, model kit inspiration, and concept design.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create mecha anime art generator images.

## Quick start
```bash
node mechaartgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `landscape`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/mecha-art-generator
```

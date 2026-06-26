---
name: impossible-scene-generator
description: Generate photorealistic impossible scenes and anti-physics landscapes powered by AI — crystal mountains with auroras, floating islands, organic-growing buildings, surreal cinematic environments, and dreamlike sci-fi vistas. Perfect for desktop wallpapers, concept art, book covers, album art, sci-fi posters, fantasy worldbuilding, and print-on-demand artwork via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Impossible Scene Generator

Generate photorealistic impossible scenes and anti-physics landscapes powered by AI — crystal mountains with auroras, floating islands, organic-growing buildings, surreal cinematic environments, and dreamlike sci-fi vistas. Perfect for desktop wallpapers, concept art, book covers, album art, sci-fi posters, fantasy worldbuilding, and print-on-demand artwork.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create impossible scene generator images.

## Quick start
```bash
node impossiblescenegenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `landscape`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/impossible-scene-generator
```

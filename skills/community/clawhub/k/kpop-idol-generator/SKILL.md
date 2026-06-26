---
name: kpop-idol-generator
description: Generate k-pop idol style portraits and kpop photocard aesthetic images — perfect for kpop fan edits, korean beauty looks, idol photoshoot vibes, korean fashion portraits, stan twitter profile pics, kpop bias card art, and hallyu-inspired glamour photography. Turn any description into a polished k-pop idol debut photo via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# K-Pop Idol Generator

Generate k-pop idol style portraits and kpop photocard aesthetic images — perfect for kpop fan edits, korean beauty looks, idol photoshoot vibes, korean fashion portraits, stan twitter profile pics, kpop bias card art, and hallyu-inspired glamour photography. Turn any description into a polished k-pop idol debut photo.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create kpop idol style portrait images.

## Quick start
```bash
node kpopidolgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/kpop-idol-generator
```

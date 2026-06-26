---
name: gothic-portrait-generator
description: Generate stunning gothic portraits with dark dramatic lighting, Victorian elegance, and moody atmosphere. Perfect for gothic art, dark fantasy portraits, horror aesthetic avatars, Victorian-style character art, dark academia profile pictures, and goth community content creation via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Gothic Portrait Generator

Generate stunning gothic portraits with dark dramatic lighting, Victorian elegance, and moody atmosphere. Perfect for gothic art, dark fantasy portraits, horror aesthetic avatars, Victorian-style character art, dark academia profile pictures, and goth community content creation.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create gothic portrait generator images.

## Quick start
```bash
node gothicportraitgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/gothic-portrait-generator
```

---
name: miniature-world-generator
description: AI miniature world and diorama art generator — create tilt-shift miniature scenes, tiny world illustrations, hyper-detailed diorama art, and shallow-depth-of-field fantasy landscapes. Perfect for Instagram art, Pinterest boards, desktop wallpapers, and creative visual storytelling via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Miniature World Generator

AI miniature world and diorama art generator — create tilt-shift miniature scenes, tiny world illustrations, hyper-detailed diorama art, and shallow-depth-of-field fantasy landscapes. Perfect for Instagram art, Pinterest boards, desktop wallpapers, and creative visual storytelling.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create miniature world diorama art generator images.

## Quick start
```bash
node miniatureworldgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/miniature-world-generator
```

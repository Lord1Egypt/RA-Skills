---
name: plush-toy-generator
description: Turn any subject — yourself, your pet, your character, or any concept — into an adorable handmade plush toy or stuffed animal with realistic fluffy fabric textures, visible stitching, and button eyes. Perfect for plushie commission references, kawaii merch mockups, gift ideas, stuffed animal designs, soft toy concepts, plushie selfies, fuzzy collectibles, and turning OCs or pets into cuddly plush dolls via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Plush Toy Generator

Turn any subject — yourself, your pet, your character, or any concept — into an adorable handmade plush toy or stuffed animal with realistic fluffy fabric textures, visible stitching, and button eyes. Perfect for plushie commission references, kawaii merch mockups, gift ideas, stuffed animal designs, soft toy concepts, plushie selfies, fuzzy collectibles, and turning OCs or pets into cuddly plush dolls.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create plush toy plushie stuffed animal generator images.

## Quick start
```bash
node plushtoygenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/plush-toy-generator
```

---
name: kawaii-art-generator
description: AI kawaii art generator — create cute kawaii characters, chibi-style illustrations, and adorable Japanese kawaii artwork with soft pastel colors, big sparkling eyes, and dreamy aesthetics. Perfect for kawaii profile pictures, cute stickers, chibi OC designs, and kawaii wallpapers via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Kawaii Art Generator

AI kawaii art generator — create cute kawaii characters, chibi-style illustrations, and adorable Japanese kawaii artwork with soft pastel colors, big sparkling eyes, and dreamy aesthetics. Perfect for kawaii profile pictures, cute stickers, chibi OC designs, and kawaii wallpapers.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create kawaii art generator images.

## Quick start
```bash
node kawaiiartgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/kawaii-art-generator
```

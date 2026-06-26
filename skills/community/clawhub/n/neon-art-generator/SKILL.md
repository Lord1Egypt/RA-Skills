---
name: neon-art-generator
description: AI neon art generator that transforms any subject into stunning neon-lit artwork. Create glowing neon portraits, cyberpunk neon scenes, neon sign aesthetics, and vibrant electric art. Perfect for profile pictures, wallpapers, social media content, and digital art with neon glow, neon lights, and neon aesthetic styles via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Neon Art Generator

AI neon art generator that transforms any subject into stunning neon-lit artwork. Create glowing neon portraits, cyberpunk neon scenes, neon sign aesthetics, and vibrant electric art. Perfect for profile pictures, wallpapers, social media content, and digital art with neon glow, neon lights, and neon aesthetic styles.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create neon art generator images.

## Quick start
```bash
node neonartgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/neon-art-generator
```

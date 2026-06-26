---
name: pixar-portrait-generator
description: selfies and portraits into Pixar-style 3D animated characters with cinematic CGI rendering. Generate Disney Pixar movie-quality avatars, 3D cartoon portraits, and animated character art featuring soft volumetric lighting, expressive oversized eyes, and glossy subsurface skin — perfect for viral profile pictures, animated-style headshots, family portraits, and 3D cartoon transformations of people, pets, and original characters via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Pixar Portrait Generator

selfies and portraits into Pixar-style 3D animated characters with cinematic CGI rendering. Generate Disney Pixar movie-quality avatars, 3D cartoon portraits, and animated character art featuring soft volumetric lighting, expressive oversized eyes, and glossy subsurface skin — perfect for viral profile pictures, animated-style headshots, family portraits, and 3D cartoon transformations of people, pets, and original characters.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create pixar style portrait ai generator images.

## Quick start
```bash
node pixarportraitgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/pixar-portrait-generator
```

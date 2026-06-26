---
name: noir-photo-generator
description: Generate dramatic film noir style portraits and scenes with AI. Perfect for creating 1940s detective aesthetic photos, black and white cinematic portraits, vintage crime fiction artwork, moody atmospheric shots with venetian blind shadows, rain-soaked streets, and classic Hollywood noir vibes for social media, book covers, posters, and creative projects via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Film Noir Photo Generator

Generate dramatic film noir style portraits and scenes with AI. Perfect for creating 1940s detective aesthetic photos, black and white cinematic portraits, vintage crime fiction artwork, moody atmospheric shots with venetian blind shadows, rain-soaked streets, and classic Hollywood noir vibes for social media, book covers, posters, and creative projects.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create film noir photo generator images.

## Quick start
```bash
node noirphotogenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/noir-photo-generator
```

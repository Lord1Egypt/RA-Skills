---
name: magazine-cover-generator
description: Generate stunning AI magazine cover art in Vogue, TIME, GQ, and editorial styles. Perfect for fashion covers, lifestyle magazine mockups, parody covers, personal branding, social media viral posts, pet magazine covers, and mixed-media editorial collage designs with professional masthead typography and cover headlines via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Magazine Cover Generator

Generate stunning AI magazine cover art in Vogue, TIME, GQ, and editorial styles. Perfect for fashion covers, lifestyle magazine mockups, parody covers, personal branding, social media viral posts, pet magazine covers, and mixed-media editorial collage designs with professional masthead typography and cover headlines.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create ai magazine cover generator images.

## Quick start
```bash
node magazinecovergenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/magazine-cover-generator
```

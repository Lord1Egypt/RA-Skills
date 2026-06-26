---
name: movie-poster-generator
description: Create stunning AI movie posters, film posters, and cinema artwork. Generate professional movie poster designs, event posters, fan-made film posters, and theatrical promotional art with dramatic cinematic lighting and bold compositions via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Movie Poster Generator

Create stunning AI movie posters, film posters, and cinema artwork. Generate professional movie poster designs, event posters, fan-made film posters, and theatrical promotional art with dramatic cinematic lighting and bold compositions.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create movie poster generator images.

## Quick start
```bash
node moviepostergenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `tall`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/movie-poster-generator
```

---
name: manga-panel-generator
description: Generate professional black-and-white manga panels and comic pages with dynamic poses, screentones, and authentic Japanese manga art style. Perfect for manga artists, doujinshi creators, webtoon storyboards, comic writers, and anime fans who want to illustrate scenes, action sequences, or character moments in classic shonen, shojo, or seinen manga aesthetics via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Manga Panel Generator

Generate professional black-and-white manga panels and comic pages with dynamic poses, screentones, and authentic Japanese manga art style. Perfect for manga artists, doujinshi creators, webtoon storyboards, comic writers, and anime fans who want to illustrate scenes, action sequences, or character moments in classic shonen, shojo, or seinen manga aesthetics.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create manga panel generator images.

## Quick start
```bash
node mangapanelgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/manga-panel-generator
```

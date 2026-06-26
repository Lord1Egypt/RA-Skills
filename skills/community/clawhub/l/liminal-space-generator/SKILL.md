---
name: liminal-space-generator
description: Generate eerie liminal space images, dreamcore backgrounds, and backrooms-style scenes — empty hallways, abandoned pools, fluorescent-lit rooms, uncanny dreamscapes, analog horror aesthetics, nostalgic unsettling environments, weirdcore and oneiric art for creators, horror writers, aesthetic Tumblr/TikTok accounts, and atmospheric game or video backdrops via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Liminal Space Generator

Generate eerie liminal space images, dreamcore backgrounds, and backrooms-style scenes — empty hallways, abandoned pools, fluorescent-lit rooms, uncanny dreamscapes, analog horror aesthetics, nostalgic unsettling environments, weirdcore and oneiric art for creators, horror writers, aesthetic Tumblr/TikTok accounts, and atmospheric game or video backdrops.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create liminal space generator images.

## Quick start
```bash
node liminalspacegenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `landscape`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/liminal-space-generator
```

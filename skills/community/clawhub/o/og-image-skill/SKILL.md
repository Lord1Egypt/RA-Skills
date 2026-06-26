---
name: og-image-skill
description: Generate og image generator ai images with AI via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# OG Image Generator

Generate stunning og image generator ai images from a text description. Get back a direct image URL instantly.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create og image generator images.

## Quick start
```bash
node ogimage.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `landscape`)
- `--style` — `anime`, `cinematic`, `realistic` (default: `cinematic`)

## Install
```bash
npx skills add SherriHidalgolt/og-image-skill
```

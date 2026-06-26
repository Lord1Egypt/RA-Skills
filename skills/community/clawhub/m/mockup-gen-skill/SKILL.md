---
name: mockup-gen-skill
description: Generate ai mockup generator images with AI via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# AI Mockup Generator

Generate stunning ai mockup generator images from a text description. Get back a direct image URL instantly.

## Token

Requires a Neta API token. Free trial available at <https://www.neta.art/open/>.

```bash
export NETA_TOKEN=your_token_here
node <script> "your prompt" --token "$NETA_TOKEN"
```

## When to use
Use when someone asks to generate or create ai mockup generator images.

## Quick start
```bash
node mockupgen.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `landscape`)
- `--style` — `anime`, `cinematic`, `realistic` (default: `realistic`)

## Install
```bash
npx skills add wkl-nieta/mockup-gen-skill
```

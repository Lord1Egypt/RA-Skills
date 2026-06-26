---
name: logo-design-generator
description: AI logo generator and logo design maker — create professional brand logos, company emblems, startup icons, app logos, and business identity marks. Design custom logo concepts with clean modern aesthetics for any brand, business, or project via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Logo Design Generator

AI logo generator and logo design maker — create professional brand logos, company emblems, startup icons, app logos, and business identity marks. Design custom logo concepts with clean modern aesthetics for any brand, business, or project.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create ai logo generator images.

## Quick start
```bash
node logodesigngenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/logo-design-generator
```

---
name: pet-memorial-portrait-generator
description: Create heartfelt pet memorial portraits and remembrance keepsakes for dogs, cats, and beloved animals who have passed. AI-generated pet memorial art, rainbow bridge portraits, angel pet paintings, and tribute photos perfect for memorial gifts, sympathy cards, keepsake prints, and honoring the memory of a cherished furry family member via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Pet Memorial Portrait Generator

Create heartfelt pet memorial portraits and remembrance keepsakes for dogs, cats, and beloved animals who have passed. AI-generated pet memorial art, rainbow bridge portraits, angel pet paintings, and tribute photos perfect for memorial gifts, sympathy cards, keepsake prints, and honoring the memory of a cherished furry family member.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create pet memorial portrait images.

## Quick start
```bash
node petmemorialportraitgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/pet-memorial-portrait-generator
```

---
name: mascot-generator
description: Generate custom brand mascots and cartoon characters with AI. Perfect for small businesses, startups, sports teams, schools, gaming clans, esports crews, and YouTube channels that need a unique company mascot, brand character, cute logo mascot, team figure, or memorable brand identity illustration via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Mascot Generator

Generate custom brand mascots and cartoon characters with AI. Perfect for small businesses, startups, sports teams, schools, gaming clans, esports crews, and YouTube channels that need a unique company mascot, brand character, cute logo mascot, team figure, or memorable brand identity illustration.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create brand mascot generator images.

## Quick start
```bash
node mascotgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/mascot-generator
```

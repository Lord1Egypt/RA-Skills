---
name: isekai-character-generator
description: Generate isekai anime characters and light novel protagonists — design transported-to-another-world heroes, JRPG main characters, fantasy adventurers, magical girls, demon lords, and reincarnated MCs in the Niji-style anime aesthetic popular in shows like Sword Art Online, Re:Zero, Mushoku Tensei, and That Time I Got Reincarnated as a Slime. Perfect for fanart, OC design, light novel covers, manga concept art, and character sheets via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Isekai Character Generator

Generate isekai anime characters and light novel protagonists — design transported-to-another-world heroes, JRPG main characters, fantasy adventurers, magical girls, demon lords, and reincarnated MCs in the Niji-style anime aesthetic popular in shows like Sword Art Online, Re:Zero, Mushoku Tensei, and That Time I Got Reincarnated as a Slime. Perfect for fanart, OC design, light novel covers, manga concept art, and character sheets.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create isekai character art generator images.

## Quick start
```bash
node isekaicharactergenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/isekai-character-generator
```

---
name: podcast-cover-generator
description: Generate professional podcast cover art and show artwork for Spotify, Apple Podcasts, YouTube Music, Amazon Music, and Overcast. Create eye-catching 1400x1400 square covers for true crime, comedy, business, interview, educational, storytelling, news, tech, and entertainment podcasts. Perfect for indie podcasters, podcast networks, audio creators, and show hosts needing custom cover design, episode art, show branding, podcast thumbnails, and directory-ready artwork that stands out in search results via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Podcast Cover Generator

Generate professional podcast cover art and show artwork for Spotify, Apple Podcasts, YouTube Music, Amazon Music, and Overcast. Create eye-catching 1400x1400 square covers for true crime, comedy, business, interview, educational, storytelling, news, tech, and entertainment podcasts. Perfect for indie podcasters, podcast networks, audio creators, and show hosts needing custom cover design, episode art, show branding, podcast thumbnails, and directory-ready artwork that stands out in search results.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create podcast cover art generator images.

## Quick start
```bash
node podcastcovergenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/podcast-cover-generator
```

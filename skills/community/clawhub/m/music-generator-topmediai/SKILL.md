---
name: music-generator-topmediai
description: |
  Generate AI music, BGM, or lyrics via TopMediai API. Supports auto polling and two-stage output
  (preview first, then final full audio) for generation tasks.
author: TopMediai
---

# Music Generator TopMediai Skill

## Capability Overview
This skill supports:
1) Generate a full song with lyrics
2) Generate pure background music (BGM)
3) Generate lyrics only
4) Query music generation tasks
5) Convert song_id to MP4

## Preflight Check (Mandatory)
- Configure `TOPMEDIAI_API_KEY` in `<skill_root>/.env`
- Optional: `TOPMEDIAI_BASE_URL` (default `https://api.topmediai.com`)
- If key is missing, stop and ask user to configure.

## Command
- Main command: `/music_generator_topmediai`
  - `mode=normal` (default): lyrics -> submit -> poll preview/full
  - `mode=bgm`: instrumental generation -> poll preview/full
  - `mode=lyrics`: lyrics only

## API Endpoints Used
- Generate lyrics: `POST {BASE_URL}/v1/lyrics`
- Submit generation: `POST {BASE_URL}/v3/music/generate`
- Query tasks: `GET {BASE_URL}/v3/music/tasks?ids=<id[,id2,...]>`
- Generate MP4 by song_id: `POST {BASE_URL}/v3/music/generate-mp4?song_id=<song_id>`

## Return Event Conventions
- `lyrics_ready`
- `submitted`
- `preview_ready`
- `full_ready`
- `failed` / `timeout`

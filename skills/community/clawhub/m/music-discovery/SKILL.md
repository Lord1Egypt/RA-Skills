---
name: music-discovery
description: Mood- and context-aware music discovery—recommend tracks, build playlists, and match energy (BPM), vibe, and genre using Spotify/Last.fm-style workflows. Keywords: music recommendation, playlist, mood, Spotify, study music, workout mix.
---

# Music Discovery — Mood, Scene & Playlists

## Overview

Helps listeners find **tracks and playlists** that fit a **mood**, **activity**, or **taste profile**—study, commute, workout, sleep, or “something like this artist.” Use when the user wants personalized picks, scene-based sets, or exploration without manual crate-digging.

**Trigger keywords**: music recommendation, playlist, mood, BPM, study music, workout, discover similar artists

## Prerequisites

```bash
pip install requests spotipy
```

## Capabilities

1. **Data-backed discovery** — Spotify Web API / Last.fm–style metadata (see `references/music_discovery_guide.md`).
2. **Scene-based sets** — work, workout, wind-down, commute, focus, party.
3. **Vibe matching** — BPM, energy, valence/mood tags, genre boundaries.

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `recommend` | Recommend tracks | `python3 scripts/skills/music-discovery/scripts/music_discovery_tool.py recommend [args]` |
| `playlist` | Build a playlist concept | `python3 scripts/skills/music-discovery/scripts/music_discovery_tool.py playlist [args]` |
| `mood` | Recommend by mood | `python3 scripts/skills/music-discovery/scripts/music_discovery_tool.py mood [args]` |

## Usage (from repository root)

```bash
python3 scripts/skills/music-discovery/scripts/music_discovery_tool.py recommend --scene office --mood relaxed
python3 scripts/skills/music-discovery/scripts/music_discovery_tool.py playlist --scene workout --bpm 140
python3 scripts/skills/music-discovery/scripts/music_discovery_tool.py mood --feeling happy
```

## Output format (for the agent’s report)

```markdown
# Music Discovery report

**Generated**: YYYY-MM-DD HH:MM

## Key picks
1. [Track / artist — one-line why]
2. …
3. …

## Snapshot
| Title | Artist | Why it fits |
|-------|--------|---------------|

## Playlist sketch (optional)
- **Theme**: …
- **Tempo / energy**: …
- **Avoid**: …

## Notes
[Ground claims in API or user-stated taste—no invented chart positions.]
```

## References

### APIs & libraries
- [Spotify Web API](https://developer.spotify.com/documentation/web-api)
- [MusicBrainz API](https://musicbrainz.org/doc/MusicBrainz_API)
- [Spotipy (Python client)](https://github.com/spotipy-dev/spotipy)

### Patterns & community
- [Daily Reddit digest (OpenClaw use case)](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/daily-reddit-digest.md)
- [Hacker News — mood-based music ML](https://news.ycombinator.com/item?id=42457780)
- [Reddit r/spotify — discussion](https://www.reddit.com/r/spotify/comments/1014b31yyz/music_recommender_ai/)

## Notes

- Prefer **real** API or user-provided data; do not invent popularity or audio features.
- Mark missing fields as **unavailable** instead of guessing.
- OAuth and rate limits apply when using Spotify—document when credentials are required.


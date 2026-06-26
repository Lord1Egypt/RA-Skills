---
name: mopidy
description: Control a Mopidy music system via Mopidy JSON-RPC for everyday listening, queue management, and playback control. Use when the user wants to search for music, see what is playing, inspect the queue, add tracks, albums, or playlists, or control playback with actions like play, pause, next, previous, clear queue, or play-now behavior. Also use for requests like "top songs by" or "best tracks from" where external ranking knowledge should be matched against the local Mopidy library before queueing the best local matches.
metadata: {"clawdbot":{"requires":{"bins":["curl","jq","python3"],"env":["MOPIDY_URL"]}}}
---

# Mopidy

Use this skill to control a Mopidy music system through Mopidy's JSON-RPC API in a predictable, scriptable way.

## Setup

Configure the Mopidy JSON-RPC endpoint before use.

Recommended environment variable:
```bash
export MOPIDY_URL="https://your-mopidy-host.example.com/mopidy/rpc"
```

Typical endpoint shape:
- `https://your-host.example.com/mopidy/rpc`

Some installations serve Iris under `/iris/`, but this skill should control Mopidy through `/mopidy/rpc`.

Helper scripts:
- `scripts/mopidy.sh`
- `scripts/match_top_tracks.py`

## Core Tasks

### See what is playing
```bash
scripts/mopidy.sh current
scripts/mopidy.sh state
```

### See the queue
```bash
scripts/mopidy.sh queue
```

### Search for music
```bash
scripts/mopidy.sh search "The Beths"
scripts/mopidy.sh search "David Bowie Blackstar"
```

Use search results to identify the correct URI before adding something.

### Add a track or album to the queue
```bash
scripts/mopidy.sh add-track backend:song:example
scripts/mopidy.sh add-album backend:album:example
```

For natural requests like “queue some Beths”, search first, then choose the best matching track or album URI.

### List playlists
```bash
scripts/mopidy.sh playlists
```

### Add playlist contents to the queue
```bash
scripts/mopidy.sh add-playlist-to-queue backend:playlist:example
```

### Playback controls
```bash
scripts/mopidy.sh play
scripts/mopidy.sh play-track backend:song:example
scripts/mopidy.sh pause
scripts/mopidy.sh next
scripts/mopidy.sh previous
scripts/mopidy.sh clear
```

## Working Style

- Prefer Mopidy JSON-RPC over UI/browser automation.
- Search first when the request is ambiguous.
- Confirm the selected item if multiple similarly named results exist.
- For queueing requests, default to adding to the queue rather than replacing playback unless the user explicitly asks to play immediately.
- Be careful with destructive queue actions; do not clear or replace the queue unless asked.
- For requests like **top**, **best**, **essential**, **greatest**, genre-based prompts, or other fuzzy ranking language, do not rely on raw library order alone. First use web search to identify likely canonical songs/albums, then match those items against the local Mopidy library before adding them.
- When using external rankings, report any items that could not be matched locally instead of silently substituting random search results.
- If requested music is not in the library, say so plainly and ask the user rather than substituting random results.

## Ranked / Canonical Requests

For prompts like:
- "add the top five The Fall songs"
- "queue the best Bowie tracks"
- "play the essential Brian Eno albums"
- "add 5 of the top indie rock tracks to the queue"

Use this workflow:
1. search the web for a credible ranked, canonical, or genre-representative list
2. extract the song or album names
3. match them against the local Mopidy library
4. add only the confirmed matches to the queue
5. tell the user what was added and what was not found

Use `scripts/match_top_tracks.py` to help match externally sourced song names against the library.

## Playlist Handling

Mopidy playlist APIs and backends can differ.

Safe approach:
1. list playlists
2. identify the target playlist URI
3. look up playlist contents
4. add those track URIs to the queue

Do not assume backend-specific shortcut behavior unless it has been tested on the target Mopidy server.

## References

Read `references/api-notes.md` if you need endpoint details, common Mopidy methods, or URI guidance.

---
name: moviefetch
description: >
  Download, track, and remove movies across Plex, Radarr, and qBittorrent from chat.
  Triggers on user requests like "get <movie>", "status of <movie>", or "remove <movie>".
---

# MovieFetch

Chat-driven movie downloading for your Plex stack.

## Features
1. **Search & Request:** Looks up movies in Radarr and adds them to the download queue.
2. **Download Status:** Fetches live progress and ETA from qBittorrent.
3. **Library Check:** Verifies whether a movie is already in Plex before requesting it.
4. **Cleanup:** Removes movies from the Radarr library and optionally deletes files.

## Workflow
1. **Request:**
   - Call `scripts/check_plex.py` first.
   - If not found → call `scripts/request_movie.py`.
2. **Status:**
   - Call `scripts/check_download.py` for live % and ETA.
3. **Remove:**
   - Call `scripts/remove_movie.py`.

## Tools
| Tool           | File                     | Purpose                              |
|----------------|--------------------------|--------------------------------------|
| check_plex      | scripts/check_plex.py     | Is it already in Plex?               |
| request_movie   | scripts/request_movie.py    | Add to Radarr search queue           |
| check_download  | scripts/check_download.py   | Live qBit progress & ETA             |
| remove_movie    | scripts/remove_movie.py     | Delete from queue and library        |

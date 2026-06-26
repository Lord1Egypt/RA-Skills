---
name: internet-radio-music-db
version: 2.6.0
description: Internet radio music stream database — collect, store, and manage a database of music streams from internet-radio.com. ~150+ streams, 29 genres, auto-population and availability checking with adaptive bitrate-based speed thresholds. Works together with the Internet Radio Music Player skill. For the easiest management experience, use the internet-radio-music-webui plugin.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "🎵"
    homepage: https://clawhub.ai/skills/internet-radio-music-db
---

# Internet Radio Music DB — Music Stream Database

Skill for collecting and managing an internet radio stream database.

## 🌐 WebUI Plugin (Recommended)

**The easiest way to manage both playback and the stream database is the [internet-radio-music-webui](https://clawhub.ai/dynamicsAlex/internet-radio-music-webui) plugin.**

The plugin provides an embeddable web panel with:
- **Playback controls**: Play, Stop, Next, Previous, Resume (auto-resume after stop)
- **Mood-based genre selector**: Pick from 20+ genres via dropdown
- **Stream database management**: View stats (genres, languages, efficiency), list streams by genre, check availability, rebuild database — all from the browser
- **WebChat integration**: Embed directly in webchat with `[embed url="http://127.0.0.1:18789/mplayer"]`

**Install the plugin:**
```bash
openclaw plugins install "clawhub:internet-radio-music-webui"
openclaw gateway restart
```

The plugin auto-detects the database scripts (`cli.py`, `show_stats.py`, `build_db.py`, `check_availability.py`) from this skill. **Both this skill AND the internet-radio-music-player skill must be installed for the plugin to work.**

## Data source

**https://www.internet-radio.com/** — the largest internet radio station catalog.

### How database population works

1. **Parallel station collection** — 10 threads simultaneously (one per genre), parsing up to `MAX_PAGES` pages per genre (`/stations/{genre}/`), stopping on empty page. With the default `MAX_PAGES = 10` this yields ~2700+ stations across 29 genres (~150+ after dedup and filtering). Adjust `MAX_PAGES` to control search depth.
2. **Playlist extraction** — extracts `.pls` playlist link from each station
3. **URL resolution** — forms a direct stream URL from the playlist (`http://server:port/stream`)
4. **Adaptive speed check** — parallel check of all new streams (60 workers), 4-second download. Threshold is per-stream based on bitrate
5. **Saving** — data saved to `state.json`

### Adaptive speed threshold

Each stream has a bitrate (kbps) stored in the database. The minimum speed threshold is:

```
threshold_KBps = max(5.0, min((bitrate_kbps / 8) * 0.75, 50.0))
```

| Stream bitrate | Nominal speed | Threshold (75%) | Effective min |
|----------------|---------------|-----------------|---------------|
| 320 kbps | 40 KB/s | 30 KB/s | 30 KB/s |
| 256 kbps | 32 KB/s | 24 KB/s | 24 KB/s |
| 192 kbps | 24 KB/s | 18 KB/s | 18 KB/s |
| 128 kbps | 16 KB/s | 12 KB/s | 12 KB/s |
| 64 kbps | 8 KB/s | 6 KB/s | 6 KB/s |
| 32 kbps | 4 KB/s | 3 KB/s | 5 KB/s (floor) |
| unknown | — | — | 5 KB/s (floor) |

This means a 64k stream only needs 6 KB/s to pass, while a 320k stream needs 30 KB/s.

### Availability checking

- Parallel check of all streams (120 workers)
- Uses the same adaptive threshold (shared `check_stream.py` module)
- Streams with `failed_checks >= 3` are automatically removed
- Extra fields stored: `check_speed_bps`, `check_threshold_kbs`, `check_bytes_received`

### Stream record format

```json
{
  "url": "http://server:8000/stream",
  "name": "Station Name",
  "genre": "rock",
  "language": "en",
  "bitrate": 128,
  "available": true,
  "source": "internet-radio.com",
  "added_at": "2026-05-23T18:00:00+00:00",
  "last_checked": "2026-05-23T19:00:00+00:00",
  "last_speed_bps": 12288,
  "failed_checks": 0
}
```

## Files

| File | Purpose |
|------|---------|
| `scripts/check_stream.py` | Shared module — adaptive speed check logic |
| `scripts/build_db.py` | Database population (imports from check_stream.py) |
| `scripts/check_availability.py` | Availability check (imports from check_stream.py) |
| `scripts/cli.py` | Stream management (list/add/remove/export) |
| `scripts/show_stats.py` | Statistics (genres, languages, speed, efficiency) |
| `state.json` | Stream database (not included in publication) |

## Commands

```bash
# Populate database (parallel, 29 genres, ~1000+ streams)
python ~/.openclaw/skills/internet-radio-music-db/scripts/build_db.py

# Check availability (120 workers, adaptive thresholds)
python ~/.openclaw/skills/internet-radio-music-db/scripts/check_availability.py

# Full statistics
python ~/.openclaw/skills/internet-radio-music-db/scripts/show_stats.py

# Genre breakdown
python ~/.openclaw/skills/internet-radio-music-db/scripts/show_stats.py --genres

# Language distribution
python ~/.openclaw/skills/internet-radio-music-db/scripts/show_stats.py --lang

# Speed distribution
python ~/.openclaw/skills/internet-radio-music-db/scripts/show_stats.py --speed

# Top-10 fastest
python ~/.openclaw/skills/internet-radio-music-db/scripts/show_stats.py --top-speed 10

# Efficiency report (actual speed vs bitrate)
python ~/.openclaw/skills/internet-radio-music-db/scripts/show_stats.py --effective

# List streams by genre
python ~/.openclaw/skills/internet-radio-music-db/scripts/cli.py list rock

# Add/remove streams
python ~/.openclaw/skills/internet-radio-music-db/scripts/cli.py add <url> <name> <genre> [lang]
python ~/.openclaw/skills/internet-radio-music-db/scripts/cli.py remove <url>

# Export database
python ~/.openclaw/skills/internet-radio-music-db/scripts/cli.py export backup.json
```

## Cron tasks

- **Database population** — every 4 hours: `0 */4 * * *`
- **Availability check** — every 4h offset 30min: `30 */4 * * *`

```bash
openclaw cron add --name "DB Population" --schedule "0 */4 * * *" --tz "Europe/Samara" \
  --message "Run: python ~/.openclaw/skills/internet-radio-music-db/scripts/build_db.py"

openclaw cron add --name "Availability Check" --schedule "30 */4 * * *" --tz "Europe/Samara" \
  --message "Run: python ~/.openclaw/skills/internet-radio-music-db/scripts/check_availability.py"
```

## Features

- **Adaptive speed thresholds** — each stream's minimum speed is based on its bitrate
- Shared `check_stream.py` module for identical criteria in population and checking
- Slow streams marked `available: false`, `failed_checks` counter incremented
- Streams with `failed_checks >= 3` auto-removed
- Language detection by station name keywords
- ~29 genres, `MAX_PAGES` per genre (default 10, configurable in `build_db.py`). Default settings yield ~150+ unique streams per cycle; increase `MAX_PAGES` for broader coverage
- No duplicate URLs

## Changelog

### v2.6.0 (2026-05-29)

- Added information about the **internet-radio-music-webui** plugin — the easiest way to manage playback and stream database
- Plugin provides web panel with playback controls, mood selector, and DB management (stats, list, check, rebuild)
- Both this skill and internet-radio-music-player are required for the plugin to work

### v2.5.1 (2026-05-27)

- Fixed description: renamed `MAX_PAGE` to `MAX_PAGES` for clarity
- Updated docs: station count now correctly reflects ~150+ streams with default settings
- Clarified `MAX_PAGES` is configurable in `build_db.py` for deeper/faster scans

### v2.5.0 (2026-05-27)

- **Adaptive speed thresholds** — replaced hardcoded 20 KB/s with bitrate-based formula
  - New shared module `check_stream.py` used by both `build_db.py` and `check_availability.py`
  - 320k stream needs 30 KB/s, 128k needs 12 KB/s, 64k needs 6 KB/s, unknown uses 5 KB/s floor
- **Efficiency report** — new `--effective` flag shows actual vs nominal bitrate speed
- Renamed `check_stream()` to `probe_stream()` in `build_db.py`
- Updated docs with threshold table

### v2.4.0 (2026-05-27)

- Full English translation of all scripts and documentation
- Added `.clawhubignore`

### v2.2.0 (2026-05-27)

- Fixed duplicate URL bug in `build_db.py` — added `seen_urls` set
- Set `MAX_PAGES = 10`

### v2.1.0 (2026-05-27)

- Increased page limit from 6 to 10
- Synchronized speed criteria between build and check scripts
- Removed legacy scripts (check_all.py, ambient_boost.py)

### v2.0.0

- Initial release

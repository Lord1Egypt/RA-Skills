---
name: internet-radio-music-player
version: 2.5.0
description: Internet radio stream player via Foobar2000. Smart 4-level relevance sorting by genre. Supports: play/stop/next/prev/resume, playback history with filters and export. Requires the Internet Radio Music DB skill. For the easiest management experience, use the internet-radio-music-webui plugin.
summary: Internet radio stream player via Foobar2000. Plays music by mood, selecting genre and stream from the Internet Radio Music DB with playback controls and history. Use the internet-radio-music-webui plugin for the simplest playback and DB management.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "🎶"
    homepage: https://clawhub.ai/skills/internet-radio-music-player
---

# Internet Radio Music Player

**⚠️ WARNING: This skill REQUIRES the Internet Radio Music DB skill to work!**

Without the stream database skill installed, playback is impossible.

## 🌐 WebUI Plugin (Recommended)

**The easiest way to manage playback and the stream database is the [internet-radio-music-webui](https://clawhub.ai/dynamicsAlex/internet-radio-music-webui) plugin.**

The plugin provides an embeddable web panel with:
- **Playback controls**: Play, Stop, Next, Previous, Resume (auto-resume after stop)
- **Mood-based genre selector**: Pick from 20+ genres via dropdown
- **Stream database management**: View stats (genres, languages, efficiency), list streams, check availability, rebuild database — all from the browser
- **WebChat integration**: Embed directly in webchat with `[embed url="http://127.0.0.1:18789/mplayer"]`

**Install the plugin:**
```bash
openclaw plugins install "clawhub:internet-radio-music-webui"
openclaw gateway restart
```

The plugin auto-detects `play_music.py` and the database scripts from this skill and the Internet Radio Music DB skill.

## Install dependencies

```bash
# 1. Install the stream database skill (required!)
openclaw skills install internet-radio-music-db

# 2. Restart Gateway
openclaw gateway restart
```

## How it works

1. User specifies a mood (e.g. "play happy music")
2. Skill determines suitable genres from the mood map
3. **Streams are fetched from the Internet Radio Music DB** (`~/.openclaw/skills/internet-radio-music-db/state.json`)
4. Streams are sorted by relevance to the requested genre (see algorithm below)
5. Stream availability is checked (HTTP request)
6. Foobar2000 is launched with the found URL
7. History is saved to `state.json`

## Stream selection algorithm

When selecting a stream from the database, a 4-level relevance sorting is applied:

### 1. Primary `genre` match (highest priority)

Streams with an exact `genre` match (database field) are always ranked higher than those matched only via the `genres` list.

### 2. Genre position in `genres` field

The requested genre is searched in the stream's `genres` list. The **closer to the beginning** — the higher the priority. If `genre` matches exactly and `genres` is empty — position=0 (ideal).

Example: requested `ambient`
- `genre=ambient, genres=[]` → level=0, position=0 ✅
- `genre=chill, genres=["Ambient", "Chill", "Downtempo"]` → level=1, position=0
- `genre=rock, genres=["Downtempo", "Chill", "Ambient"]` → level=1, position=2

### 3. Number of "extra" genres

Given equal level and position — the stream with **fewer subgenres** wins.

### 4. Stream speed

All other things being equal — the **faster** stream is chosen.

### Final sort key

```
(genre_match_level, position, extra_genres, -speed)
```

Lower value = more relevant stream.

### `next` command

Switches to the next stream **of the same genre** from the database (using relevance sorting). Does not switch to a history entry.

## Mood → Genres

| Mood (keywords) | Genres from DB |
|-----------------|----------------|
| calm, sleep, rest, background, meditation | ambient, classical, folk |
| happy, fun, dance, energy | dance, disco, pop, funk, house |
| sad, blues, melancholy | blues, jazz, soul, ambient |
| rock, hard, garage | rock, metal, punk, alternative, indie |
| electronic, synth, lo-fi, dream | electronic, ambient, house, techno |
| classical, orchestra, symphony | classical |
| reggae, tropical, summer | reggae, latin, disco |
| hip-hop, rap, R&B, soul | soul, funk, pop, disco |
| techno, rave, club, trance | techno, house, trance, electronic, dance |
| jazz, swing | jazz, blues, soul |
| country, western, folk | country, folk |
| lounge, chill-out | ambient, jazz, indie, folk, chill, lounge, downtempo, relaxation |
| metal, heavy, power, aggression | metal, punk, rock |
| 80s, 90s, retro, nostalgia | 80s, 90s, oldies, disco, pop |
| indie, alternative, experimental | indie, alternative |
| latin, salsa, bachata, brazil | latin |
| pop, popular, hits | pop, top-40 |
| work, focus, study | ambient, classical, electronic |
| party, dancefloor | dance, house, techno, pop, funk, disco |
| sunset, chill, evening, lounge | ambient, jazz, indie, folk, chill, lounge, downtempo, relaxation |
| news, talk, podcast | news, talk |
| gospel, church, spiritual | gospel, classical, ambient |

## Commands

| Command | Action |
|---------|--------|
| **"Play music"** | Play ambient (by default) |
| **"Play [mood] music"** | Determine genre and play |
| **"Play jazz" / "Play sad music"** | Jazz / blues |
| **"Play happy music"** | Dance / disco / pop |
| **"Play music for sleeping"** | Ambient / classical |
| **"Play rock" / "Play heavy music"** | Rock / metal |
| **"Play electronic music"** | Electronic / techno |
| **"Play reggae" / "Play summer music"** | Reggae / latin |
| **"Play classical"** | Classical |
| **"Play 80s music"** | 80s |
| **"Next" / "Other stream"** | Next stream of same genre |
| **"Previous" / "Back"** | Return to previous stream |
| **"Play what was playing" / "Last stream"** | Play the most recent stream from all history |
| **"Stop"** | Stop playback |
| **"What's playing?" / "Status"** | Show current stream |
| **"History" / "Playback list"** | Show history |

## Stream source

**Music Stream Database** (`~/.openclaw/skills/internet-radio-music-db/`):
- ~1000+ streams from 29 genres
- Auto-populated every 3 hours from internet-radio.com
- 29 genres collected in parallel
- Streams are speed-checked during population (60 workers, 4 sec)
- Streams with `failed_checks >= 3` are automatically removed from the database

## Files

| File | Purpose |
|------|---------|
| `scripts/play_music.py` | Main playback script (play/stop/next/prev/resume/status/history) |
| `scripts/show_history.py` | Detailed playback history with filters and export (CSV/HTML/JSON) |
| `state.json` | Current genre, playback history, current stream |
| `~/.openclaw/skills/internet-radio-music-db/state.json` | Stream database (managed by Internet Radio Music DB skill) |

## Dependencies

- **Python 3** — for playback scripts
- **Foobar2000** — music player (auto-detects path: `C:\Program Files\foobar2000\` or `C:\Program Files (x86)\foobar2000\`)
- **Internet Radio Music DB** — stream database skill (required!)

## Changelog

### v2.5.0 (2026-05-29)

- Added information about the **internet-radio-music-webui** plugin — the easiest way to manage playback and stream database
- Plugin provides web panel with playback controls, mood-based genre selector, and DB management (stats, list, check, rebuild)
- Both internet-radio-music-db skill and this skill are required for the plugin to work

### v2.4.0 (2026-05-29)

- **Smart `play` after `stop` — auto-resume:** if playback was stopped via `stop`, pressing `play` without specifying a mood/genre resumes the last played stream from history instead of starting a new random one. State tracks `Stopped` flag to distinguish between "never played" and "explicitly stopped".
- **Changed `--mood` default** from `"ambient"` to `None` — allows detecting when no genre was explicitly requested by the user. Internal fallback to `"ambient"` still applies when playing a new stream.
- Updated `cmd_play` signature: entered genre always resets `Stopped` flag, ensuring explicit genre requests always start fresh.

### v2.3.0 (2026-05-27)

- **Removed `random.shuffle`** — previously, streams were shuffled after relevance sorting, causing multi-genre streams with a different primary genre (e.g. dance) to play instead of pure genre matches (e.g. country). Now the relevance order is always respected: pure genres first, multi-genre second.
- Updated documentation with bug description and fix details
- Full English translation of SKILL.md

### v2.2.0 (2026-05-27)

- **Improved stream sorting — now 4 priority levels:**
  1. Primary `genre` match (exact > only in `genres` > none)
  2. Requested genre position in `genres` field (closer to start = better)
  3. Number of extra subgenres (fewer = more precise)
  4. Stream speed (faster = better)
- **Fixed `next` command** — now selects a stream from the database by current stream's genre (instead of random history switching). Uses the same relevance logic as `play`
- **Fixed Foobar2000 switching** — now uses correct `stop` → `play` within the running player instead of `taskkill + restart`
- **Handled empty `genres`** — if `genre` matches exactly and `genres` is empty, stream gets position=0 (ideal match)
- **Discovered and documented database bug** — the same stream could exist dozens of times with different `genre/genres`, breaking sort order

### v2.1.0 (2026-05-27)

- **Smart stream relevance sorting** — 3-level selection system:
  1. Requested genre position in `genres` field
  2. Number of extra subgenres
  3. Stream speed
- **Foobar2000 path auto-detection** — automatically finds installation in `Program Files` and `Program Files (x86)`
- **Added `lounge` genre** to mood map (chill/sunset/evening pattern)
- **Added Russian word "кантри"** to mood map
- **Support for `genres` as string** — parsing via comma and semicolon
- Updated documentation with stream selection algorithm description

### v2.0.0

- Initial release

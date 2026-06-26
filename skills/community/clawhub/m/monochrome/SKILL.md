---
name: monochrome
description: Browse and search music from monochrome.tf (Tidal-based Hi-Fi streaming). Search for artists, albums, tracks, and get streaming URLs. Use for music discovery and high-fidelity audio streaming.
license: Apache-2.0
---

# Monochrome Music Skill

Browse and stream music from Monochrome (monochrome.tf) — a minimalist, high-fidelity music streaming client powered by Tidal.

## Capabilities

- Search for artists, albums, tracks, videos, and playlists
- Get track info and streaming URLs
- Browse artist discographies
- Get album details and track lists
- Fetch lyrics for tracks
- Get artist recommendations

## API Instances

Monochrome uses the Hi-Fi API (Tidal proxy). Available instances:

| Instance | Version | Status |
|----------|---------|--------|
| `eu-central.monochrome.tf` | 2.8 | Primary |
| `us-west.monochrome.tf` | 2.8 | Secondary |
| `hifi-one.spotisaver.net` | 2.8 | Community |
| `hifi-two.spotisaver.net` | 2.8 | Community |
| `hifi.geeked.wtf` | 2.7 | Community |

Use the primary instance for best reliability:
```
https://eu-central.monochrome.tf
```

## Usage

### Search for Music

Search for tracks, artists, albums, videos, or playlists:

**Track Search:**
```
GET /search/?s={query}&limit={limit}&offset={offset}
```

**Artist Search:**
```
GET /search/?a={query}&limit={limit}
```

**Album Search:**
```
GET /search/?al={query}&limit={limit}
```

**Video Search:**
```
GET /search/?v={query}&limit={limit}
```

**Playlist Search:**
```
GET /search/?p={query}&limit={limit}
```

**ISRC Search (exact track match):**
```
GET /search/?i={isrc}
```

### Get Track Info

```
GET /info/?id={track_id}
```

### Get Track Streaming URL

```
GET /track/?id={track_id}&quality={quality}&immersiveaudio={bool}
```

Quality options: `LOW`, `HIGH`, `LOSSLESS`, `HI_RES`, `HI_RES_LOSSLESS`

### Get Album Details

```
GET /album/?id={album_id}&limit={limit}&offset={offset}
```

### Get Artist Info

```
GET /artist/?id={artist_id}
```

### Get Artist Albums & Tracks

```
GET /artist/?f={artist_id}
```

### Get Similar Artists

```
GET /artist/similar/?id={artist_id}
```

### Get Similar Albums

```
GET /album/similar/?id={album_id}
```

### Get Lyrics

```
GET /lyrics/?id={track_id}
```

### Get Playlist

```
GET /playlist/?id={playlist_id}&limit={limit}&offset={offset}
```

### Get Mix

```
GET /mix/?id={mix_id}
```

### Get Recommendations

```
GET /recommendations/?id={track_id}
```

### Get Cover Art

```
GET /cover/?id={track_id}
GET /cover/?q={search_query}
```

Cover URLs follow the pattern:
```
https://resources.tidal.com/images/{uuid}/{size}.jpg
```

Sizes: `80x80`, `320x320`, `640x640`, `1280x1280`, `750x750`

## Implementation

### Step 1: Search for Music

```bash
curl "https://eu-central.monochrome.tf/search/?s=Linkin%20Park&limit=10"
```

Returns JSON with track items including:
- `id` — Track ID
- `title` — Track title
- `artists` — Artist list
- `album` — Album info
- `duration` — Duration in seconds
- `audioQuality` — Quality tier

### Step 2: Get Streaming URL

```bash
curl "https://eu-central.monochrome.tf/track/?id=12345678&quality=HI_RES_LOSSLESS"
```

Returns streaming manifest URL.

### Step 3: Play/Download

The streaming URL can be used directly in audio players or downloaders.

## Example Queries

| User Request | API Call |
|--------------|----------|
| "Search for Linkin Park" | `/search/?a=Linkin%20Park` |
| "Find the album Hybrid Theory" | `/search/?al=Hybrid%20Theory` |
| "Get track info for 12345" | `/info/?id=12345` |
| "Get lyrics for track 12345" | `/lyrics/?id=12345` |
| "Similar artists to Eminem" | `/artist/similar/?id=12345` |

## Notes

- API is rate-limited; use appropriate delays for bulk requests
- Quality `HI_RES_LOSSLESS` requires compatible streaming setup
- All endpoints return JSON with `version` and `data` fields
- Default `countryCode` is US

## Related Skills

- **music-downloader** — Download tracks from monochrome.tf
- **mcp-vision** — Analyze album covers

## Links

- Monochrome Web: https://monochrome.tf
- GitHub: https://github.com/monochrome-music/monochrome
- API Status: https://tidal-uptime.jiffy-puffs-1j.workers.dev
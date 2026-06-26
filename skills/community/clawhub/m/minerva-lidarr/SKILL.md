---
name: lidarr
description: Interact with Lidarr (music/album manager) via its REST API. Use when searching for artists or albums, checking missing/wanted releases, triggering downloads, or monitoring queue status. Part of the *arr media management suite.
---

# Lidarr Skill

Lidarr is the *arr-suite manager for music. It monitors artists and albums, finds releases via indexers (Prowlarr), sends them to a download client, and organises them on disk.

## Connection

Lidarr runs on Dozo at `http://localhost:8686`.

```bash
LIDARR_URL="http://localhost:8686"
LIDARR_KEY=$(cat /path/to/lidarr_api_key)
```

See `references/api.md` for all endpoints.

## Core Workflows

### Search and add an artist
```bash
# 1. Look up artist (returns MusicBrainz results)
curl -s "$LIDARR_URL/api/v1/artist/lookup?term=David+Bowie" \
  -H "X-Api-Key: $LIDARR_KEY" | python3 -c "
import sys,json
results = json.load(sys.stdin)
for a in results[:5]:
    print(a.get('artistName'), '| foreignArtistId:', a.get('foreignArtistId'))
"

# 2. Get quality/metadata profiles and root folders
curl -s "$LIDARR_URL/api/v1/qualityprofile" -H "X-Api-Key: $LIDARR_KEY"
curl -s "$LIDARR_URL/api/v1/metadataprofile" -H "X-Api-Key: $LIDARR_KEY"
curl -s "$LIDARR_URL/api/v1/rootfolder" -H "X-Api-Key: $LIDARR_KEY"

# 3. Add the artist
curl -s -X POST "$LIDARR_URL/api/v1/artist" \
  -H "X-Api-Key: $LIDARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"foreignArtistId":"<id>","artistName":"David Bowie","qualityProfileId":1,"metadataProfileId":1,"rootFolderPath":"/music","monitored":true,"addOptions":{"monitor":"all","searchForMissingAlbums":true}}'
```

### Search and add an album
```bash
# 1. Look up album
curl -s "$LIDARR_URL/api/v1/album/lookup?term=Ziggy+Stardust" \
  -H "X-Api-Key: $LIDARR_KEY" | python3 -c "
import sys,json
results = json.load(sys.stdin)
for a in results[:5]:
    print(a.get('title'), '—', a.get('artist',{}).get('artistName'), '| foreignAlbumId:', a.get('foreignAlbumId'))
"

# 2. Add the album (artist must already be in Lidarr)
curl -s -X POST "$LIDARR_URL/api/v1/album" \
  -H "X-Api-Key: $LIDARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"foreignAlbumId":"<id>","monitored":true,"addOptions":{"searchForNewAlbum":true}}'
```

### Check wanted/missing albums
```bash
curl -s "$LIDARR_URL/api/v1/wanted/missing?pageSize=20" \
  -H "X-Api-Key: $LIDARR_KEY" | python3 -c "
import sys,json
d = json.load(sys.stdin)
for a in d.get('records',[]):
    print(a.get('title'), '—', a.get('artist',{}).get('artistName'), '(', a.get('releaseDate','?')[:4], ')')
"
```

### Trigger search for all missing albums
```bash
curl -s -X POST "$LIDARR_URL/api/v1/command" \
  -H "X-Api-Key: $LIDARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"MissingAlbumSearch"}'
```

### Check download queue
```bash
curl -s "$LIDARR_URL/api/v1/queue" -H "X-Api-Key: $LIDARR_KEY" | python3 -c "
import sys,json
q = json.load(sys.stdin)
for item in q.get('records',[]):
    print(item.get('title'), '|', item.get('status'), '|', item.get('timeleft','?'))
"
```

## Credentials
Store API key at `~/clawd/credentials/lidarr_api_key` (single line, no newline).
Load with: `LIDARR_KEY=$(cat /path/to/lidarr_api_key)`

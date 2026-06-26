---
name: radarr
description: Interact with Radarr (movie manager) via its REST API. Use when searching for movies, checking missing/wanted titles, triggering downloads, or monitoring queue status. Part of the *arr media management suite.
---

# Radarr Skill

Radarr is the *arr-suite manager for movies. It monitors a watchlist, finds releases via indexers (Prowlarr), sends them to a download client, and organises them on disk.

## Connection

Radarr runs on Dozo at `http://localhost:7878`.

```bash
RADARR_URL="http://localhost:7878"
RADARR_KEY=$(cat /path/to/radarr_api_key)
```

See `references/api.md` for all endpoints.

## Core Workflows

### Search and add a movie
```bash
# 1. Look up by title (returns TMDB results)
curl -s "$RADARR_URL/api/v3/movie/lookup?term=The+Matrix" \
  -H "X-Api-Key: $RADARR_KEY" | python3 -c "
import sys,json
results = json.load(sys.stdin)
for m in results[:5]:
    print(m.get('title'), '| tmdbId:', m.get('tmdbId'), '| year:', m.get('year'))
"

# 2. Get quality profiles and root folders
curl -s "$RADARR_URL/api/v3/qualityprofile" -H "X-Api-Key: $RADARR_KEY"
curl -s "$RADARR_URL/api/v3/rootfolder" -H "X-Api-Key: $RADARR_KEY"

# 3. Add the movie
curl -s -X POST "$RADARR_URL/api/v3/movie" \
  -H "X-Api-Key: $RADARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tmdbId":603,"title":"The Matrix","qualityProfileId":1,"rootFolderPath":"/movies","monitored":true,"addOptions":{"searchForMovie":true}}'
```

### Check wanted/missing movies
```bash
curl -s "$RADARR_URL/api/v3/wanted/missing?pageSize=20" \
  -H "X-Api-Key: $RADARR_KEY" | python3 -c "
import sys,json
d = json.load(sys.stdin)
for m in d.get('records',[]):
    print(m.get('title'), '(', m.get('year'), ')')
"
```

### Trigger search for all missing movies
```bash
curl -s -X POST "$RADARR_URL/api/v3/command" \
  -H "X-Api-Key: $RADARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"MissingMoviesSearch"}'
```

### Check download queue
```bash
curl -s "$RADARR_URL/api/v3/queue" -H "X-Api-Key: $RADARR_KEY" | python3 -c "
import sys,json
q = json.load(sys.stdin)
for item in q.get('records',[]):
    print(item.get('title'), '|', item.get('status'), '|', item.get('timeleft','?'))
"
```

## Credentials
Store API key at `~/clawd/credentials/radarr_api_key` (single line, no newline).
Load with: `RADARR_KEY=$(cat /path/to/radarr_api_key)`

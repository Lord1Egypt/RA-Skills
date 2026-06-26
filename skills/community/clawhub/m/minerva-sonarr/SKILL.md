---
name: sonarr
description: Interact with Sonarr (TV show manager) via its REST API. Use when searching for TV series, checking missing/wanted episodes, triggering downloads, or monitoring queue status. Part of the *arr media management suite.
---

# Sonarr Skill

Sonarr is the *arr-suite manager for TV shows. It monitors series, finds episode releases via indexers (Prowlarr), sends them to a download client, and organises them on disk.

## Connection

Sonarr runs on Dozo at `http://localhost:8989`.

```bash
SONARR_URL="http://localhost:8989"
SONARR_KEY=$(cat /path/to/sonarr_api_key)
```

See `references/api.md` for all endpoints.

## Core Workflows

### Search and add a TV series
```bash
# 1. Look up by title (returns TVDB results)
curl -s "$SONARR_URL/api/v3/series/lookup?term=Breaking+Bad" \
  -H "X-Api-Key: $SONARR_KEY" | python3 -c "
import sys,json
results = json.load(sys.stdin)
for s in results[:5]:
    print(s.get('title'), '| tvdbId:', s.get('tvdbId'), '| year:', s.get('year'))
"

# 2. Get quality profiles and root folders
curl -s "$SONARR_URL/api/v3/qualityprofile" -H "X-Api-Key: $SONARR_KEY"
curl -s "$SONARR_URL/api/v3/rootfolder" -H "X-Api-Key: $SONARR_KEY"

# 3. Add the series
curl -s -X POST "$SONARR_URL/api/v3/series" \
  -H "X-Api-Key: $SONARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tvdbId":81189,"title":"Breaking Bad","qualityProfileId":1,"rootFolderPath":"/tv","monitored":true,"seasonFolder":true,"addOptions":{"searchForMissingEpisodes":true}}'
```

### Check wanted/missing episodes
```bash
curl -s "$SONARR_URL/api/v3/wanted/missing?pageSize=20" \
  -H "X-Api-Key: $SONARR_KEY" | python3 -c "
import sys,json
d = json.load(sys.stdin)
for ep in d.get('records',[]):
    print(ep.get('series',{}).get('title'), 'S{:02d}E{:02d}'.format(ep.get('seasonNumber',0), ep.get('episodeNumber',0)), '—', ep.get('title'))
"
```

### Trigger search for all missing episodes
```bash
curl -s -X POST "$SONARR_URL/api/v3/command" \
  -H "X-Api-Key: $SONARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"MissingEpisodeSearch"}'
```

### Check download queue
```bash
curl -s "$SONARR_URL/api/v3/queue" -H "X-Api-Key: $SONARR_KEY" | python3 -c "
import sys,json
q = json.load(sys.stdin)
for item in q.get('records',[]):
    print(item.get('title'), '|', item.get('status'), '|', item.get('timeleft','?'))
"
```

## Credentials
Store API key at `~/clawd/credentials/sonarr_api_key` (single line, no newline).
Load with: `SONARR_KEY=$(cat /path/to/sonarr_api_key)`

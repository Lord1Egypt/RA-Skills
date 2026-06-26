# MusicBrainz API Reference

## Base URL
`https://musicbrainz.org/ws/2/`

Always append `&fmt=json` for JSON responses.

## User-Agent
All API requests require a meaningful User-Agent header. Build it from your bot name and MusicBrainz username:
```
User-Agent: <BotName>/1.0 (<mb-username>@users.noreply.musicbrainz.org)
```
If credentials are available in `.credentials.json`, read the username from there.

## Rate Limiting
- 1 request per second for unauthenticated requests
- Use `web_fetch` for API calls (not browser)

## Key Endpoints

### Lookup by Spotify URL
Find MB entity linked to a Spotify URL:
```
GET /ws/2/url/?resource=https://open.spotify.com/artist/<id>&fmt=json
```
Returns `{id, resource}` — the `id` is the URL entity MBID.

To get the linked artist/release, expand with `inc=artist-rels` or `inc=release-rels`:
```
GET /ws/2/url/<url-mbid>?inc=artist-rels&fmt=json
```
The `relations[].artist.id` is the artist MBID.

### Artist Lookup
```
GET /ws/2/artist/<mbid>?inc=release-groups&fmt=json
```

### Release Group Lookup
```
GET /ws/2/release-group/<mbid>?inc=releases&fmt=json
```

### Search Artists
```
GET /ws/2/artist/?query=<name>&fmt=json&limit=10
```

### Search Releases
```
GET /ws/2/release/?query=release:<title>%20AND%20artist:<name>&fmt=json
```

## Checking if a Spotify Album Exists on MB
1. `GET /ws/2/url/?resource=https://open.spotify.com/album/<id>&fmt=json`
2. If 200 with result → already linked
3. If 404 or no result → not on MB (or not linked)

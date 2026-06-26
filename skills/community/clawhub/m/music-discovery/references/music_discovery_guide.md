# Music Discovery — Framework & Guide

## Tool summary

- **Name**: Music Discovery  
- **Commands**: `recommend`, `playlist`, `mood`  
- **Typical deps**: `pip install requests spotipy`

## Analysis dimensions

- Metadata: artist, album, genre, tempo, release era  
- Context: scene (work, gym, sleep), social vs solo  
- Audio / mood proxies: BPM, energy, mood tags (when APIs expose them)  
- Taste: seeds, “similar to,” exclusions  

## Framework

### Phase 1: Clarify the ask
- Mood, activity, language, era, explicit content on/off  
- Target length (single track vs full playlist arc)

### Phase 2: Shortlist & justify
- Prefer tracks you can ground in API results or the user’s library  
- Call out why each pick fits the stated scene or mood  

### Phase 3: Deliver a playlist shape
- Ordering (warm-up → peak → cool-down for workouts)  
- Optional diversity rules (avoid same artist back-to-back)

## Scoring rubric (fit quality)

| Score | Level | Meaning | Action |
|-------|-------|---------|--------|
| 5 | ⭐⭐⭐⭐⭐ | Strong fit | Top recommendation |
| 4 | ⭐⭐⭐⭐ | Good fit | Prioritize |
| 3 | ⭐⭐⭐ | OK | Optional |
| 2 | ⭐⭐ | Weak | Caveat |
| 1 | ⭐ | Poor | Avoid |

## Output template

```markdown
# Music Discovery analysis

## Picks
1. …
2. …

## Evidence
| Track | Artist | Source / rationale |
|-------|--------|----------------------|

## Playlist outline
- …
```

## Reference links

- [Spotify Web API](https://developer.spotify.com/documentation/web-api)  
- [MusicBrainz API](https://musicbrainz.org/doc/MusicBrainz_API)  
- [Spotipy](https://github.com/spotipy-dev/spotipy)  
- [Daily Reddit digest (OpenClaw)](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/daily-reddit-digest.md)  
- [Hacker News](https://news.ycombinator.com/item?id=42457780)  
- [Reddit r/spotify](https://www.reddit.com/r/spotify/comments/1014b31yyz/music_recommender_ai/)  

## Tips

1. Match **constraints** first (language, explicit, max BPM).  
2. Separate **objective metadata** from subjective “vibe” language.  
3. When APIs are unavailable, be explicit and suggest **manual** next steps (e.g. search in-app).  

---
name: music-podcast-research
description: Researches music, artists, playlists, and podcasts via the Crawlora API — Spotify tracks/albums/artists/playlists/profiles, Spotify Podcasts, Apple Podcasts, Discogs, and SoundCloud tracks/profiles/playlists — returning clean JSON. Use when the user wants a track/album/artist's details, a playlist or profile, podcast show/episode info and charts, a record's Discogs release/pressing data, or a SoundCloud track/user's stats.
---

# Music & podcast research

Look up tracks, albums, artists, playlists, and podcast shows/episodes across
Spotify, Spotify Podcasts, Apple Podcasts, Discogs, and SoundCloud as
normalized JSON from the Crawlora API — no scraping streaming-app pages.

## When to use this skill

- "Find this track/album/artist on Spotify" / "what's on this playlist?"
- "Look up a Spotify user's public profile/playlists."
- "What podcasts/episodes are trending?" (Spotify Podcasts, Apple Podcasts charts)
- "Get details for this podcast show/episode."
- "What pressings/releases exist for this record?" (Discogs — vinyl/collector data)
- "Look up this SoundCloud track/user" / "how many plays/likes does this
  track have?" / "what has this artist uploaded to SoundCloud?"

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Spotify** — search first: `/spotify/search` (or the scoped
   `/spotify/tracks/search`, `/spotify/artists/search`, `/spotify/albums/search`,
   `/spotify/playlists/search`, `/spotify/profiles/search`) with `q`. Detail
   endpoints (`/spotify/track`, `/spotify/album`, `/spotify/artist`,
   `/spotify/playlist`, `/spotify/profile`) accept **either** `id` or `uri`
   (a Spotify URI like `spotify:track:...`) — pass whichever you have.
   `/spotify/artist/related`, `/spotify/track/recommended`, and
   `/spotify/track/similar-albums` cover discovery.
2. **Spotify Podcasts** — `/spotify-podcasts/search`, `/spotify-podcasts/show`
   (by `uri`), `/spotify-podcasts/show/episodes`, `/spotify-podcasts/charts`.
3. **Apple Podcasts** — `/apple-podcasts/search` (`term`), `/apple-podcasts/show/{id}`,
   `/apple-podcasts/show/{id}/episodes`, `/apple-podcasts/charts` /
   `/apple-podcasts/charts/rankings` for what's popular by country.
4. **Discogs** — `/discogs/search` (`q`, optional `type` = release/master/
   artist/label) to find an id, then `/discogs/release/{id}`,
   `/discogs/master/{id}`, `/discogs/artist/{id}`, `/discogs/label/{id}`
   for detail (+ `/releases` sub-paths for an artist's/label's catalog).
5. **SoundCloud** — `/soundcloud/search` (`query`) to find a track, then
   `/soundcloud/track` (`url` — a track's full `permalink_url`) for its
   full metadata and play/like/comment/repost counts. `/soundcloud/profile`
   (`url` — a user's profile URL) gets bio and follower/track counts;
   `/soundcloud/user-tracks` (`url`) lists that user's own uploads;
   `/soundcloud/playlist` (`url`) gets a playlist/album's metadata and
   full track list.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Spotify:
scripts/crawlora.sh /spotify/search q="Daft Punk" | jq '.'
scripts/crawlora.sh /spotify/artist id=4tZwfgrHOc3mvqYlEYSvVi | jq '.'

# Podcasts:
scripts/crawlora.sh /apple-podcasts/search term="Reply All" | jq '.'
scripts/crawlora.sh /spotify-podcasts/charts | jq '.'

# Discogs:
scripts/crawlora.sh /discogs/search q="Random Access Memories" type=release | jq '.'
scripts/crawlora.sh /discogs/release/4818226 | jq '.'

# SoundCloud:
scripts/crawlora.sh /soundcloud/search query="lofi hip hop" | jq '.'
scripts/crawlora.sh /soundcloud/track url="https://soundcloud.com/artist/track-name" | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Spotify,
Spotify Podcasts, Apple Podcasts, Discogs, and SoundCloud endpoint this
skill uses.

## Examples

- **Artist deep-dive:** `/spotify/artist` + `/spotify/artist/albums` +
  `/spotify/artist/related` for a full discography and similar-artist map.
- **Podcast discovery:** `/spotify-podcasts/charts` or
  `/apple-podcasts/charts` to find what's trending, then
  `/spotify-podcasts/show/episodes` for a show's back catalog.
- **Collector research:** `/discogs/search` for a release, then
  `/discogs/release/{id}` for pressing details (format, year, label,
  condition-relevant metadata).
- **SoundCloud artist catalog:** `/soundcloud/profile` for a user's
  follower/track counts, then `/soundcloud/user-tracks` for their own
  uploads with per-track play/like/comment/repost counts.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public catalog/profile/chart pages.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Spotify detail endpoints need an `id` or `uri`** — resolve one via the
  matching `.../search` endpoint first if you only have a name.
- **SoundCloud detail endpoints need a full `url`** (a track/playlist/user's
  `permalink_url`, e.g. `https://soundcloud.com/artist/track-name`) —
  there's no numeric-id lookup, so pull the URL from `/soundcloud/search`
  results first if you only have a name.
- Search endpoints are paginated (`limit`/`offset` or `page`) — walk pages
  for full coverage.

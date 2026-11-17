# music-release-landscape — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**9 endpoints across 1 platform group(s).**

## Spotify (9)

### `spotify_album`

- **HTTP:** `GET /spotify/album`
- **What:** Retrieve Spotify album details. Returns a Spotify album from `uri` (a Spotify URI or open.spotify.com URL) or `id`: name, album type, artists, release date, copyrights, cover images, total tracks and duration. The `tracks` page is set by `offset` (default 0) and `limit` (1 to 50, default 50). A missing or invalid identifier returns 400.
- **Params:** `id` (string, optional) — Spotify album ID; `limit` (integer, optional) — Track limit, clamped to 1-50; `offset` (integer, optional) — Track offset; `uri` (string, optional) — Spotify album URI or open.spotify.com album URL

### `spotify_album_tracks`

- **HTTP:** `GET /spotify/album/tracks`
- **What:** Retrieve Spotify album tracks. Lists the tracks of a Spotify album, identified by `uri` (a Spotify URI or open.spotify.com URL) or `id`. `offset` defaults to 0 and `limit` runs 1 to 50, default 50. Each track has its title, URI, subtitle, image and URL. The album's name, artists and track total come back alongside. An invalid identifier returns 400.
- **Params:** `id` (string, optional) — Spotify album ID; `limit` (integer, optional) — Track limit, clamped to 1-50; `offset` (integer, optional) — Track offset; `uri` (string, optional) — Spotify album URI or open.spotify.com album URL

### `spotify_albums_search`

- **HTTP:** `GET /spotify/albums/search`
- **What:** Search Spotify albums. Returns Spotify album search results for a search term. Caller-supplied Spotify bearer or client tokens are not required.
- **Params:** `include_album_pre_releases` (boolean, optional) — Include album pre-release results; `include_audiobooks` (boolean, optional) — Include audiobook context where available; `include_authors` (boolean, optional) — Include authors; `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `include_pre_releases` (boolean, optional) — Include pre-release results; `limit` (integer, optional) — Album result limit, clamped to 1-50; `number_of_top_results` (integer, optional) — Top result limit, clamped to 1-50; `offset` (integer, optional) — Search offset; `q` (string, **required**) — Search term

### `spotify_artist`

- **HTTP:** `GET /spotify/artist`
- **What:** Retrieve Spotify artist details. Returns a Spotify artist's profile by artist URI, `open.spotify.com` URL or id: name, verified flag, follower count, monthly listeners (`monthlyUsers`), biography and images, plus top tracks, selected discography, related artists and artist playlists when Spotify returns them.
- **Params:** `id` (string, optional) — Spotify artist ID; `uri` (string, optional) — Spotify artist URI or open.spotify.com artist URL

### `spotify_artist_albums`

- **HTTP:** `GET /spotify/artist/albums`
- **What:** Retrieve Spotify artist albums. Returns an artist's Spotify discography by artist URI, `open.spotify.com` URL or id. Choose `type` (`album`, `single`, `compilation`, `appears_on` or `all`; default `album`) and `order` (default `date_desc`), and page with `offset` and `limit` (1-50, default 50). Each item has a type, title, subtitle, Spotify URI, external URL and images; `total` gives the full count.
- **Params:** `id` (string, optional) — Spotify artist ID; `limit` (integer, optional) — Limit, clamped to 1-50; `offset` (integer, optional) — Offset; `order` (string, optional) — date_desc, date_asc, name_asc, or name_desc; `type` (string, optional) — album, single, compilation, appears_on, or all; `uri` (string, optional) — Spotify artist URI or open.spotify.com artist URL

### `spotify_artist_related`

- **HTTP:** `GET /spotify/artist/related`
- **What:** Retrieve Spotify related artists. Returns the artists Spotify lists as related to a given artist, by artist URI, `open.spotify.com` URL or id. Each related artist has a title, Spotify URI, external URL and images. An invalid identifier returns `400`.
- **Params:** `id` (string, optional) — Spotify artist ID; `uri` (string, optional) — Spotify artist URI or open.spotify.com artist URL

### `spotify_artists_search`

- **HTTP:** `GET /spotify/artists/search`
- **What:** Search Spotify artists. Searches Spotify for artists matching a term, with `offset` and `limit` (1-50). Each artist has a title, Spotify URI, external URL and images. Matching artists are returned in both `results` and `artists`.
- **Params:** `limit` (integer, optional) — Result limit, clamped to 1-50; `offset` (integer, optional) — Search offset; `q` (string, **required**) — Search term

### `spotify_track`

- **HTTP:** `GET /spotify/track`
- **What:** Retrieve Spotify track details. Returns Spotify track metadata. Provide either uri or id; defaults to a known public track when omitted.
- **Params:** `id` (string, optional) — Spotify track ID. Used when uri is omitted; `uri` (string, optional) — Spotify track URI or open.spotify.com track URL

### `spotify_tracks_search`

- **HTTP:** `GET /spotify/tracks/search`
- **What:** Search Spotify tracks. Returns Spotify track search results for a search term. Caller-supplied Spotify bearer or client tokens are not required.
- **Params:** `include_album_pre_releases` (boolean, optional) — Include album pre-release results; `include_audiobooks` (boolean, optional) — Include audiobook context where available; `include_authors` (boolean, optional) — Include authors; `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `include_pre_releases` (boolean, optional) — Include pre-release results; `limit` (integer, optional) — Track result limit, clamped to 1-50; `number_of_top_results` (integer, optional) — Top result limit, clamped to 1-50; `offset` (integer, optional) — Search offset; `q` (string, **required**) — Search term

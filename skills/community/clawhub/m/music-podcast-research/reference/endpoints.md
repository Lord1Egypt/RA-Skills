# music-podcast-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**58 endpoints across 5 platform group(s).**

## Spotify (30)

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

### `spotify_artist_playlists`

- **HTTP:** `GET /spotify/artist/playlists`
- **What:** Retrieve Spotify artist playlists. Returns the Spotify playlists associated with an artist, by artist URI, `open.spotify.com` URL or id. Each playlist has a title, subtitle, description, Spotify URI, external URL and images. Some artists have no playlists, in which case `items` is empty.
- **Params:** `id` (string, optional) — Spotify artist ID; `uri` (string, optional) — Spotify artist URI or open.spotify.com artist URL

### `spotify_artist_related`

- **HTTP:** `GET /spotify/artist/related`
- **What:** Retrieve Spotify related artists. Returns the artists Spotify lists as related to a given artist, by artist URI, `open.spotify.com` URL or id. Each related artist has a title, Spotify URI, external URL and images. An invalid identifier returns `400`.
- **Params:** `id` (string, optional) — Spotify artist ID; `uri` (string, optional) — Spotify artist URI or open.spotify.com artist URL

### `spotify_artists_search`

- **HTTP:** `GET /spotify/artists/search`
- **What:** Search Spotify artists. Searches Spotify for artists matching a term, with `offset` and `limit` (1-50). Each artist has a title, Spotify URI, external URL and images. Matching artists are returned in both `results` and `artists`.
- **Params:** `limit` (integer, optional) — Result limit, clamped to 1-50; `offset` (integer, optional) — Search offset; `q` (string, **required**) — Search term

### `spotify_audiobook`

- **HTTP:** `GET /spotify/audiobook`
- **What:** Retrieve Spotify audiobook details. Returns a Spotify audiobook by `uri` or `id`; Spotify identifies audiobooks with show URIs (`spotify:show:...`). The response has name, authors, narrators, publisher, description, `totalChapters`, explicit flag and cover images. Passing a podcast show instead of an audiobook returns an upstream error, and an invalid identifier returns 400.
- **Params:** `id` (string, optional) — Spotify show ID; `uri` (string, optional) — Spotify audiobook/show URI or open.spotify.com show URL

### `spotify_audiobook_chapters`

- **HTTP:** `GET /spotify/audiobook/chapters`
- **What:** Retrieve Spotify audiobook chapters. Returns the chapters of a Spotify audiobook by URI, `open.spotify.com` URL or id, with `offset` and `limit` (1-50, default 50). Each chapter has its name, description, duration in milliseconds, release date, explicit and playable flags, Spotify URI, external URL and images; `total` gives the chapter count.
- **Params:** `id` (string, optional) — Spotify show ID; `limit` (integer, optional) — Chapter limit, clamped to 1-50; `offset` (integer, optional) — Chapter offset; `uri` (string, optional) — Spotify audiobook/show URI or open.spotify.com show URL

### `spotify_audiobooks_search`

- **HTTP:** `GET /spotify/audiobooks/search`
- **What:** Search Spotify audiobooks. Returns Spotify audiobook search results for a search term. Caller-supplied Spotify bearer or client tokens are not required.
- **Params:** `include_album_pre_releases` (boolean, optional) — Include album pre-release results; `include_audiobooks` (boolean, optional) — Include audiobook results; `include_authors` (boolean, optional) — Include authors; `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `include_pre_releases` (boolean, optional) — Include pre-release results; `limit` (integer, optional) — Audiobook result limit, clamped to 1-50; `number_of_top_results` (integer, optional) — Top result limit, clamped to 1-50; `offset` (integer, optional) — Search offset; `q` (string, **required**) — Search term

### `spotify_chapter`

- **HTTP:** `GET /spotify/chapter`
- **What:** Retrieve Spotify audiobook chapter details. Returns a Spotify audiobook chapter by `uri` or `id`; chapters are often addressed with `spotify:episode:` identifiers. Fields include name, description, duration, release date, explicit and paywall flags, playability reasons, preview audio URL, cover images and the parent show. An invalid identifier returns 400.
- **Params:** `id` (string, optional) — Spotify chapter/episode ID; `uri` (string, optional) — Spotify chapter or episode URI/URL

### `spotify_episodes_search`

- **HTTP:** `GET /spotify/episodes/search`
- **What:** Search Spotify episodes. Searches Spotify podcast episodes for the search term `q`, paged with `offset` (default 0) and `limit` (1 to 50). Each episode has its title, URI, description, publisher, images and Spotify URL. Episode matches appear under both `results` and `episodes`. A missing `q` returns 400.
- **Params:** `limit` (integer, optional) — Result limit, clamped to 1-50; `offset` (integer, optional) — Search offset; `q` (string, **required**) — Search term

### `spotify_featured_charts_by_country`

- **HTTP:** `GET /spotify/featured-charts-by-country`
- **What:** Retrieve Spotify featured charts by country. Returns Spotify country hub content. Defaults to the CHARTS content shelf for the requested country.
- **Params:** `content_id` (string, optional) — Country hub content ID. Allowed: CHARTS, POPULAR_ALBUMS, POPULAR_ARTISTS, TRENDING_SONGS; `country_code` (string, optional) — Two-letter Spotify popular-in country code

### `spotify_genre`

- **HTTP:** `GET /spotify/genre`
- **What:** Retrieve Spotify genre page. Returns the sections of a Spotify genre or browse page for `uri` (default `spotify:page:0JQ5DAB3zgCauRwnvdEQjJ`). Each section has a title, type, `totalCount` and items with title, subtitle, image and Spotify URL. `page_limit` and `section_limit` default to 10 and run 1 to 50; matching offsets default to 0.
- **Params:** `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `page_limit` (integer, optional) — Page pagination limit, clamped to 1-50; `page_offset` (integer, optional) — Page pagination offset; `section_limit` (integer, optional) — Section pagination limit, clamped to 1-50; `section_offset` (integer, optional) — Section pagination offset; `uri` (string, optional) — Spotify genre or page URI

### `spotify_home`

- **HTTP:** `GET /spotify/home`
- **What:** Retrieve Spotify home sections. Returns Spotify home shelves and items. Caller-supplied Spotify bearer or client tokens are not required.
- **Params:** `facet` (string, optional) — Optional Spotify home facet; `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `section_items_limit` (integer, optional) — Per-section item limit, clamped to 1-50; `sp_t` (string, optional) — Optional Spotify session token. A random UUID is generated when omitted; `time_zone` (string, optional) — IANA time zone used by Spotify home personalization

### `spotify_playlist`

- **HTTP:** `GET /spotify/playlist`
- **What:** Retrieve Spotify playlist details. Returns Spotify playlist metadata and items. Provide either uri or id; defaults to a known public playlist when omitted.
- **Params:** `enable_watch_feed_entrypoint` (boolean, optional) — Enable watch feed entrypoint; `id` (string, optional) — Spotify playlist ID. Used when uri is omitted; `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `limit` (integer, optional) — Playlist item limit, clamped to 1-50; `offset` (integer, optional) — Playlist item offset; `uri` (string, optional) — Spotify playlist URI or open.spotify.com playlist URL

### `spotify_playlists_search`

- **HTTP:** `GET /spotify/playlists/search`
- **What:** Search Spotify playlists. Returns Spotify playlist search results for a search term. Caller-supplied Spotify bearer or client tokens are not required.
- **Params:** `include_album_pre_releases` (boolean, optional) — Include album pre-release results; `include_audiobooks` (boolean, optional) — Include audiobook context where available; `include_authors` (boolean, optional) — Include authors; `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `include_pre_releases` (boolean, optional) — Include pre-release results; `limit` (integer, optional) — Playlist result limit, clamped to 1-50; `number_of_top_results` (integer, optional) — Top result limit, clamped to 1-50; `offset` (integer, optional) — Search offset; `q` (string, **required**) — Search term

### `spotify_popular_by_country`

- **HTTP:** `GET /spotify/popular-by-country`
- **What:** Retrieve Spotify popular by country. Returns Spotify country hub shelves. The country_code parameter accepts Spotify popular-in country codes from open.spotify.com/popular-in/us.
- **Params:** `country_code` (string, optional) — Two-letter Spotify popular-in country code

### `spotify_profile`

- **HTTP:** `GET /spotify/profile`
- **What:** Retrieve Spotify public profile. Returns public Spotify profile metadata and preview playlists. Provide username, uri, or url; defaults to Spotify's official profile.
- **Params:** `artist_limit` (integer, optional) — Recently played artist limit, clamped to 0-50; `episode_limit` (integer, optional) — Embedded episode limit, clamped to 0-50; `playlist_limit` (integer, optional) — Embedded public playlist limit, clamped to 0-50; `uri` (string, optional) — Spotify user URI; `url` (string, optional) — open.spotify.com user URL; `username` (string, optional) — Spotify username

### `spotify_profile_followers`

- **HTTP:** `GET /spotify/profile/followers`
- **What:** Retrieve Spotify public profile followers. Returns public Spotify follower profiles. Spotify exposes this publicly for some profiles; private or restricted profiles may return an upstream error.
- **Params:** `limit` (integer, optional) — Follower limit, clamped to 1-200; `offset` (integer, optional) — Follower offset applied locally; `uri` (string, optional) — Spotify user URI; `url` (string, optional) — open.spotify.com user URL; `username` (string, optional) — Spotify username

### `spotify_profile_playlists`

- **HTTP:** `GET /spotify/profile/playlists`
- **What:** Retrieve Spotify public profile playlists. Returns public Spotify playlists. Provide username, uri, or url; defaults to Spotify's official profile.
- **Params:** `limit` (integer, optional) — Playlist limit, clamped to 1-50; `offset` (integer, optional) — Playlist offset; `uri` (string, optional) — Spotify user URI; `url` (string, optional) — open.spotify.com user URL; `username` (string, optional) — Spotify username

### `spotify_profiles_search`

- **HTTP:** `GET /spotify/profiles/search`
- **What:** Search Spotify profiles. Returns Spotify profile search results for a search term. Caller-supplied Spotify bearer or client tokens are not required.
- **Params:** `include_album_pre_releases` (boolean, optional) — Include album pre-release results; `include_audiobooks` (boolean, optional) — Include audiobook context where available; `include_authors` (boolean, optional) — Include authors; `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `include_pre_releases` (boolean, optional) — Include pre-release results; `limit` (integer, optional) — Profile result limit, clamped to 1-50; `number_of_top_results` (integer, optional) — Top result limit, clamped to 1-50; `offset` (integer, optional) — Search offset; `q` (string, **required**) — Search term

### `spotify_search`

- **HTTP:** `GET /spotify/search`
- **What:** Search Spotify catalog. Returns Spotify catalog search results across tracks, artists, albums, playlists, shows, episodes, audiobooks, and top results. Caller-supplied Spotify bearer or client tokens are not required.
- **Params:** `include_album_pre_releases` (boolean, optional) — Include album pre-release results; `include_artist_has_concerts_field` (boolean, optional) — Include artist concert availability fields; `include_audiobooks` (boolean, optional) — Include audiobook results; `include_authors` (boolean, optional) — Include authors; `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `include_pre_releases` (boolean, optional) — Include pre-release results; `is_prefix` (boolean, optional) — Treat the search term as a prefix; `limit` (integer, optional) — Result limit per section, clamped to 1-50; `number_of_top_results` (integer, optional) — Top result limit, clamped to 1-50; `offset` (integer, optional) — Search offset; `q` (string, **required**) — Search term

### `spotify_section`

- **HTTP:** `GET /spotify/section`
- **What:** Retrieve Spotify browse section. Returns the items of one Spotify browse section for `uri` (default `spotify:section:0JQ5IMCbQBLqNPkcmYxQPQ`), with its title, subtitle and `totalCount`. Each item has a type, title, subtitle, images and Spotify URL. `offset` defaults to 0; `limit` runs 1 to 50 and defaults to 20.
- **Params:** `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `limit` (integer, optional) — Section item limit, clamped to 1-50; `offset` (integer, optional) — Section item offset; `uri` (string, optional) — Spotify section URI

### `spotify_shows_search`

- **HTTP:** `GET /spotify/shows/search`
- **What:** Search Spotify shows. Searches Spotify podcast shows for the search term `q`, paged with `offset` (default 0) and `limit` (1 to 50). Each show has its title, URI, publisher, description, images and Spotify URL. Show matches appear under both `results` and `shows`. A missing `q` returns 400.
- **Params:** `limit` (integer, optional) — Result limit, clamped to 1-50; `offset` (integer, optional) — Search offset; `q` (string, **required**) — Search term

### `spotify_track`

- **HTTP:** `GET /spotify/track`
- **What:** Retrieve Spotify track details. Returns Spotify track metadata. Provide either uri or id; defaults to a known public track when omitted.
- **Params:** `id` (string, optional) — Spotify track ID. Used when uri is omitted; `uri` (string, optional) — Spotify track URI or open.spotify.com track URL

### `spotify_track_recommended`

- **HTTP:** `GET /spotify/track/recommended`
- **What:** Retrieve Spotify recommended tracks. Returns Spotify's recommendations for a track, given its URI, `open.spotify.com` URL or track id. Each recommendation has a type, title, subtitle, description, Spotify URI, external URL and images. `limit` is clamped to 1-50 and defaults to 5.
- **Params:** `id` (string, optional) — Spotify track ID. Used when uri is omitted; `limit` (integer, optional) — Recommendation limit, clamped to 1-50; `uri` (string, optional) — Spotify track URI or open.spotify.com track URL

### `spotify_track_similar_albums`

- **HTTP:** `GET /spotify/track/similar-albums`
- **What:** Retrieve Spotify track similar albums. Lists albums similar to a Spotify track, identified by `uri` or `id`. `limit` runs 1 to 50, default 50, and `albums_only` requests albums-only recommendations. Each album has its title, subtitle, publisher, images and Spotify URL. With neither `uri` nor `id`, a known public track is used.
- **Params:** `albums_only` (boolean, optional) — Request albums-only recommendations; `id` (string, optional) — Spotify track ID. Used when uri is omitted; `limit` (integer, optional) — Album limit, clamped to 1-50; `uri` (string, optional) — Spotify track URI or open.spotify.com track URL

### `spotify_tracks_search`

- **HTTP:** `GET /spotify/tracks/search`
- **What:** Search Spotify tracks. Returns Spotify track search results for a search term. Caller-supplied Spotify bearer or client tokens are not required.
- **Params:** `include_album_pre_releases` (boolean, optional) — Include album pre-release results; `include_audiobooks` (boolean, optional) — Include audiobook context where available; `include_authors` (boolean, optional) — Include authors; `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `include_pre_releases` (boolean, optional) — Include pre-release results; `limit` (integer, optional) — Track result limit, clamped to 1-50; `number_of_top_results` (integer, optional) — Top result limit, clamped to 1-50; `offset` (integer, optional) — Search offset; `q` (string, **required**) — Search term

## SpotifyPodcasts (8)

### `spotify_podcasts_categories`

- **HTTP:** `GET /spotify-podcasts/categories`
- **What:** Retrieve Spotify Podcasts categories. Returns the Spotify podcast categories page as sections of items such as Arts, for `uri` (default `spotify:page:0JQ5DArNBzkmxXHCqFLx2U`). Each section has a title, `totalCount` and items with title, image and Spotify URL. `page_limit` and `section_limit` default to 10 and run 1 to 50; the offsets default to 0.
- **Params:** `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `page_limit` (integer, optional) — Page pagination limit, clamped to 1-50; `page_offset` (integer, optional) — Page pagination offset; `section_limit` (integer, optional) — Section pagination limit, clamped to 1-50; `section_offset` (integer, optional) — Section pagination offset; `uri` (string, optional) — Spotify podcast categories page URI

### `spotify_podcasts_charts`

- **HTTP:** `GET /spotify-podcasts/charts`
- **What:** Retrieve Spotify podcast charts. Returns Spotify podcast chart rankings from podcastcharts.byspotify.com. The chart and region parameters are validated against Spotify's supported podcast chart slugs and countries. Category charts are available only in au, br, de, gb, mx, se, and us.
- **Params:** `chart` (string, optional) — Chart slug. Allowed: top-podcasts, top-episodes, trending, arts, business, comedy, education, fiction, health-fitness, history, leisure, music, news, religion-spirituality, science, society-culture, sports, technology, true-crime, tv-film; `limit` (integer, optional) — Result limit, clamped to 1-100; `region` (string, optional) — Two-letter region code. Allowed: ar, au, at, br, ca, cl, co, dk, fi, fr, de, in, id, ie, it, jp, mx, nz, no, ph, pl, es, se, nl, gb, us

### `spotify_podcasts_episode`

- **HTTP:** `GET /spotify-podcasts/episode`
- **What:** Retrieve Spotify podcast episode details. Returns public episode metadata. Provide either uri or id; defaults to a known public episode when omitted.
- **Params:** `id` (string, optional) — Spotify episode ID. Used when uri is omitted; `uri` (string, optional) — Spotify episode URI or open.spotify.com episode URL

### `spotify_podcasts_home`

- **HTTP:** `GET /spotify-podcasts/home`
- **What:** Retrieve Spotify Podcasts home. Returns the Spotify podcasts home page as sections of items, for `uri` (default `spotify:genre:podcasts-web`). Each section has a title and items with type, title, publisher, images and Spotify URL. `page_limit` and `section_limit` default to 10 and run 1 to 50; the offsets default to 0.
- **Params:** `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `page_limit` (integer, optional) — Page pagination limit, clamped to 1-50; `page_offset` (integer, optional) — Page pagination offset; `section_limit` (integer, optional) — Section pagination limit, clamped to 1-50; `section_offset` (integer, optional) — Section pagination offset; `uri` (string, optional) — Spotify page or genre URI

### `spotify_podcasts_search`

- **HTTP:** `GET /spotify-podcasts/search`
- **What:** Search Spotify Podcasts. Searches Spotify podcasts for `q`, returning matching `shows`, `episodes` and `topResults`, with counts in `meta`. `limit` and `number_of_top_results` run 1 to 50. Optional flags (`include_pre_releases`, `include_audiobooks`, `include_authors`) widen the results. Episodes carry duration and release date; shows carry publisher.
- **Params:** `include_album_pre_releases` (boolean, optional) — Include album pre-release results; `include_audiobooks` (boolean, optional) — Include audiobooks; `include_authors` (boolean, optional) — Include authors; `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `include_pre_releases` (boolean, optional) — Include pre-release results; `limit` (integer, optional) — Result limit, clamped to 1-50; `number_of_top_results` (integer, optional) — Top result limit, clamped to 1-50; `offset` (integer, optional) — Search offset; `q` (string, **required**) — Podcast search term

### `spotify_podcasts_show`

- **HTTP:** `GET /spotify-podcasts/show`
- **What:** Retrieve Spotify podcast show metadata. Returns metadata for one Spotify podcast show by `uri` (default `spotify:show:1QQJ7FElLE0K6CIfZNCxU4`): name, publisher, description, media type, explicit flag, `totalEpisodes`, cover images and Spotify URL. The two `include_` flags request extra content capability and content rating fields when Spotify supplies them.
- **Params:** `include_content_capability_trait` (boolean, optional) — Include content capability trait; `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `uri` (string, optional) — Spotify show URI

### `spotify_podcasts_show_episodes`

- **HTTP:** `GET /spotify-podcasts/show/episodes`
- **What:** Retrieve Spotify podcast show episodes. Returns the episodes of a Spotify podcast by show URI, with `offset` and `limit` (1-50). Each episode has its name, description, release date, duration in milliseconds, explicit and playable flags, Spotify URI, external URL and images; `total` gives the show's episode count.
- **Params:** `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `limit` (integer, optional) — Episode limit, clamped to 1-50; `offset` (integer, optional) — Episode offset; `uri` (string, optional) — Spotify show URI

### `spotify_podcasts_show_recommendations`

- **HTTP:** `GET /spotify-podcasts/show/recommendations`
- **What:** Retrieve Spotify podcast recommendations. Lists shows and episodes that Spotify recommends alongside a podcast show given by `uri`. Each recommendation has a type, title, publisher, description, images and Spotify URL, and `meta.count` gives the number returned. The response echoes the show `uri` it was requested for.
- **Params:** `uri` (string, optional) — Spotify show URI

## ApplePodcasts (8)

### `apple_podcasts_charts`

- **HTTP:** `GET /apple-podcasts/charts`
- **What:** Retrieve Apple Podcasts chart rankings. Returns Apple Podcasts show chart rankings for a `collection`, either `toppodcasts` or `topaudiopodcasts`. Narrow with `category` (a numeric Apple podcast genre ID), `country` and `limit`. Each entry has `name`, `artist_name`, `genre`, `genre_id`, `description`, `release_date`, `artwork_url` and `url`.
- **Params:** `category` (integer, optional) — Numeric Apple podcast genre ID; `collection` (string, optional) — Chart collection; `country` (string, optional) — Two-letter storefront country code; `limit` (integer, optional) — Number of chart items to return

### `apple_podcasts_charts_rankings`

- **HTTP:** `GET /apple-podcasts/charts/rankings`
- **What:** Retrieve Apple Podcasts chart rankings by algorithm, type, and genre. Returns Apple Podcasts chart rankings from the modern podcasts.apple.com charts page, covering chart algorithms (`top`, `top-subscriber`, `top-series`) crossed with entity types (`podcasts`, `podcast-episodes`, `podcast-channels`) and an optional genre filter. A richer, differently-sourced capability than the legacy RSS-based `/apple-podcasts/charts` endpoint.
- **Params:** `chart` (string, optional) — Chart algorithm. Allowed values: `top`, `top-subscriber`, `top-series`. Default `top`.; `country` (string, optional) — Two-letter storefront country code; `genre` (integer, optional) — Optional Apple Podcasts genre ID to filter the chart, e.g. 1303 for Comedy; `limit` (integer, optional) — Number of chart entries to return, default 24, max 200; `type` (string, optional) — Entity type. Allowed values: `podcasts`, `podcast-episodes`, `podcast-channels`. Default `podcasts`.

### `apple_podcasts_episodes_search`

- **HTTP:** `GET /apple-podcasts/episodes/search`
- **What:** Search Apple Podcasts episodes. Searches Apple Podcasts episodes by `term`, which is required. `country`, `lang`, `limit` and `page` (1-based) refine the search. Each episode has its `title`, `show_name`, `show_id`, `description`, `duration_millis`, `release_date`, `episode_url`, `preview_url`, `feed_url`, genres and artwork.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Result language tag; `limit` (integer, optional) — Number of episodes per page; `page` (integer, optional) — Search page number (1-based); `term` (string, **required**) — Search term

### `apple_podcasts_new`

- **HTTP:** `GET /apple-podcasts/new`
- **What:** Retrieve Apple Podcasts curated "New" editorial shelves. Returns the curated editorial shelves from podcasts.apple.com/{country}/new (New Shows, New Seasons, New Trailers, Essentials, and other seasonal spotlights). Shelves that merely mirror a Charts Rankings query are omitted here since `/apple-podcasts/charts/rankings` already covers that data.
- **Params:** `country` (string, optional) — Two-letter storefront country code

### `apple_podcasts_search`

- **HTTP:** `GET /apple-podcasts/search`
- **What:** Search Apple Podcasts shows. Searches Apple Podcasts shows by `term`, which is required. `country`, `lang`, `limit` and `page` (1-based) refine the search. Each show has `collection_name`, `artist_name`, `feed_url`, `primary_genre_name`, `genres`, `track_count`, `release_date`, content advisory rating and several artwork sizes.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Result language tag; `limit` (integer, optional) — Number of shows per page; `page` (integer, optional) — Search page number (1-based); `term` (string, **required**) — Search term

### `apple_podcasts_show`

- **HTTP:** `GET /apple-podcasts/show/{id}`
- **What:** Retrieve Apple Podcasts show details. Returns the details of one Apple Podcasts show by its Apple show `id`: `collection_name`, `artist_name`, `feed_url`, `primary_genre_name`, `genres`, `track_count`, `release_date`, content advisory rating and artwork. `country` and `lang` choose the storefront and language.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Apple Podcasts show ID; `lang` (string, optional) — Result language tag

### `apple_podcasts_show_episodes`

- **HTTP:** `GET /apple-podcasts/show/{id}/episodes`
- **What:** Retrieve Apple Podcasts show episodes. Returns one Apple Podcasts show by its Apple show `id`, together with a list of its episodes. `limit` sets how many episodes to return; `country` and `lang` choose the storefront and language. Episodes have `title`, `description`, `duration_millis`, `release_date`, `episode_url` and `episode_guid`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Apple Podcasts show ID; `lang` (string, optional) — Result language tag; `limit` (integer, optional) — Number of episodes to return

### `apple_podcasts_show_related`

- **HTTP:** `GET /apple-podcasts/show/{id}/related`
- **What:** Retrieve Apple Podcasts "You Might Also Like" related shows. Returns the "You Might Also Like" rail for a single show, sourced from the modern podcasts.apple.com show page's listener-cohort recommendation data.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Apple Podcasts show ID; `limit` (integer, optional) — Number of related shows to return, default 20, max 50

## Discogs (7)

### `discogs_artist`

- **HTTP:** `GET /discogs/artist/{id}`
- **What:** Get a Discogs artist profile. Returns a Discogs artist profile: real name, bio, links, name variations, aliases, and group memberships.
- **Params:** `id` (string, **required**) — Discogs artist id

### `discogs_artist_releases`

- **HTTP:** `GET /discogs/artist/{id}/releases`
- **What:** List a Discogs artist's releases. Returns the releases and masters credited to a Discogs artist, identified by the required `id`. Paged with `page` (default 1) and `per_page` (default 50, max 100). Each entry has its `id`, `type` (`release` or `master`), title, artist, role, format, label, year, thumbnail, and want and collection counts, alongside the total item count and page count.
- **Params:** `id` (string, **required**) — Discogs artist id; `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 50, max 100

### `discogs_label`

- **HTTP:** `GET /discogs/label/{id}`
- **What:** Get a Discogs label profile. Returns the profile of a Discogs label by its required label `id`: name, profile text, contact info, website URLs, images, data quality rating, and Discogs page URI. The parent label and the list of sub-labels are included, and the parent label appears only when the label has one.
- **Params:** `id` (string, **required**) — Discogs label id

### `discogs_label_releases`

- **HTTP:** `GET /discogs/label/{id}/releases`
- **What:** List a Discogs label's releases. Lists the releases on a Discogs label, identified by the required label `id`. Paged with `page` (default 1) and `per_page` (default 50, max 100). Each entry has its release `id`, title, artist, format, catalogue number (`catno`), status, year and thumbnail, and the response reports the total item count across all pages.
- **Params:** `id` (string, **required**) — Discogs label id; `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 50, max 100

### `discogs_master`

- **HTTP:** `GET /discogs/master/{id}`
- **What:** Get a Discogs master release. Returns a Discogs master release: the version-agnostic grouping of a release across pressings/reissues (artists, tracklist, genres/styles, videos, images, marketplace stats).
- **Params:** `id` (string, **required**) — Discogs master release id

### `discogs_release`

- **HTTP:** `GET /discogs/release/{id}`
- **What:** Get a Discogs release. Returns a Discogs release: artists, labels, formats, tracklist, credits, identifiers, videos, images, and community want/have/rating.
- **Params:** `id` (string, **required**) — Discogs release id

### `discogs_search`

- **HTTP:** `GET /discogs/search`
- **What:** Search the Discogs database. Searches the Discogs database for releases, masters, artists and labels, optionally filtered to one `type`, with `page` and `per_page` (max 100). Release and master results carry country, year, formats, labels, genres, styles, catalog number and barcodes; artist and label results carry id, title and thumbnail.
- **Params:** `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 50, max 100; `q` (string, **required**) — Search query; `type` (string, optional) — Result type filter

## SoundCloud (5)

### `soundcloud_playlist`

- **HTTP:** `GET /soundcloud/playlist`
- **What:** Get a SoundCloud playlist or album's detail. Returns one playlist or album's metadata plus its full track list: owner, likes/reposts counts, and every track's title, artwork, and playback/likes counts. Public data sourced from SoundCloud's own JSON API.
- **Params:** `url` (string, **required**) — Full soundcloud.com playlist/album URL (a playlist's permalink_url)

### `soundcloud_profile`

- **HTTP:** `GET /soundcloud/profile`
- **What:** Get a SoundCloud user/artist profile. Returns a SoundCloud user or artist profile for a full profile `url` such as `https://soundcloud.com/artist`. Fields are username, full name, bio, avatar, city, country, verified status, and counts of followers, followings, tracks, playlists and likes. A URL for a track or other entity returns 400; an unresolvable URL returns 404.
- **Params:** `url` (string, **required**) — Full soundcloud.com user/artist profile URL

### `soundcloud_search`

- **HTTP:** `GET /soundcloud/search`
- **What:** Search SoundCloud tracks. Searches SoundCloud tracks for `query`, in SoundCloud's default relevance order. `limit` defaults to 20 and is capped at 50. Each track has its title, artwork, genre, tags, `duration_ms`, play, like, comment and repost counts, and uploader details including follower count and verified status.
- **Params:** `limit` (integer, optional) — Number of tracks to return (default 20, max 50); `query` (string, **required**) — Search text

### `soundcloud_track`

- **HTTP:** `GET /soundcloud/track`
- **What:** Get a SoundCloud track's detail. Returns one track's full metadata: title, artwork, description, genre, tags, playback/likes/comment/repost counts, and uploader. Public data sourced from SoundCloud's own JSON API.
- **Params:** `url` (string, **required**) — Full soundcloud.com track URL (a track's permalink_url)

### `soundcloud_user_tracks`

- **HTTP:** `GET /soundcloud/user-tracks`
- **What:** Get a SoundCloud user's own uploaded tracks. Returns a user/artist's own uploaded tracks, most recent first: title, artwork, playback/likes/comment/repost counts. Public data sourced from SoundCloud's own JSON API.
- **Params:** `limit` (integer, optional) — Number of tracks to return (default 20, max 50); `url` (string, **required**) — Full soundcloud.com user/artist profile URL

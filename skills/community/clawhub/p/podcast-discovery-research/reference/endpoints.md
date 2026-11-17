# podcast-discovery-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**16 endpoints across 2 platform group(s).**

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
